#!/usr/bin/env python3
"""
Runway & Rivets eBay Lister
Automated mass listing of vintage and collectible inventory to eBay using Inventory and Trading APIs.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ebay_lister.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

console = Console()


class EbayAuth:
    """Handles eBay OAuth 2.0 authentication and token management."""
    
    def __init__(self):
        self.client_id = os.getenv("EBAY_CLIENT_ID")
        self.client_secret = os.getenv("EBAY_CLIENT_SECRET")
        self.redirect_uri = os.getenv("EBAY_REDIRECT_URI")
        self.refresh_token = os.getenv("EBAY_REFRESH_TOKEN")
        self.environment = os.getenv("EBAY_ENVIRONMENT", "production")
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing required eBay OAuth credentials in .env file")
        
        # Set API endpoints based on environment
        if self.environment == "production":
            self.base_url = "https://api.ebay.com"
        else:
            self.base_url = "https://api.sandbox.ebay.com"
        
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if (self.access_token and self.token_expires_at and 
            datetime.now() < self.token_expires_at):
            return self.access_token
        
        if not self.refresh_token:
            raise ValueError("No refresh token available. Please obtain one first.")
        
        return self._refresh_access_token()
    
    def _refresh_access_token(self) -> str:
        """Refresh the access token using the refresh token."""
        url = f"{self.base_url}/identity/v1/oauth2/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account"
        }
        
        auth = (self.client_id, self.client_secret)
        
        try:
            response = requests.post(url, headers=headers, auth=auth, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 7200)  # Default 2 hours
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            # Update refresh token if provided
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]
                logger.info("Refresh token updated")
            
            logger.info("Access token refreshed successfully")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to refresh access token: {e}")
            raise
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json"
        }


class EbayLister:
    """Main class for handling eBay listing operations."""
    
    def __init__(self, csv_file: str, draft_mode: bool = True, user_id: str = "default_user"):
        self.auth = EbayAuth()
        self.csv_file = csv_file
        self.draft_mode = draft_mode
        self.user_id = user_id
        self.image_base_url = os.getenv("IMAGE_BASE_URL", "")
        self.auction_duration = int(os.getenv("AUCTION_DURATION", "7"))
        
        # Initialize AI service and user config
        try:
            from ai_providers import AIService
            from user_config import UserConfigManager
            self.ai_service = AIService()
            self.user_config_manager = UserConfigManager()
        except ImportError:
            logger.warning("AI providers not available - running in basic mode")
            self.ai_service = None
            self.user_config_manager = None
        
        # Load CSV data
        self.inventory_data = self._load_inventory_data()
        
        # Track processed items
        self.processed_items = []
        self.failed_items = []
    
    def _load_inventory_data(self) -> pd.DataFrame:
        """Load and validate inventory data from CSV."""
        try:
            df = pd.read_csv(self.csv_file)
            required_columns = ["Title", "Description", "Category", "Condition", "Photo Files"]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Clean and validate data
            df = df.dropna(subset=["Title", "Description"])  # Remove rows without title/description
            df["Quantity"] = df["Quantity"].fillna(1).astype(int)
            df["Estimated Median Sale Price"] = df["Estimated Median Sale Price"].fillna(0).astype(float)
            
            logger.info(f"Loaded {len(df)} items from {self.csv_file}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")
            raise
    
    def _load_config(self):
        """Load eBay configuration from JSON file."""
        try:
            with open('ebay_categories.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("ebay_categories.json not found, using default mappings")
            return {
                "category_mappings": {},
                "condition_mappings": {
                    "new": "NEW",
                    "very good": "VERY_GOOD", 
                    "good": "GOOD",
                    "fair": "FAIR",
                    "poor": "POOR"
                },
                "defaults": {
                    "default_category": "45100",
                    "default_condition": "GOOD"
                }
            }
    
    def _map_condition_to_ebay(self, condition: str) -> str:
        """Map condition values to eBay condition IDs."""
        config = self._load_config()
        condition_mapping = config.get("condition_mappings", {})
        default_condition = config.get("defaults", {}).get("default_condition", "GOOD")
        return condition_mapping.get(condition.lower(), default_condition)
    
    def _map_category_to_ebay(self, category: str) -> str:
        """Map category paths to eBay category IDs."""
        config = self._load_config()
        category_mapping = config.get("category_mappings", {})
        default_category = config.get("defaults", {}).get("default_category", "45100")
        return category_mapping.get(category, default_category)
    
    def _process_images(self, photo_files: str) -> List[str]:
        """Process image filenames into URLs."""
        if not photo_files or pd.isna(photo_files):
            return []
        
        # Split by comma and clean up filenames
        filenames = [f.strip() for f in photo_files.split(",") if f.strip()]
        
        # Convert to URLs if base URL is configured
        if self.image_base_url:
            return [f"{self.image_base_url.rstrip('/')}/{f.strip()}" for f in filenames]
        
        # For now, return filenames as-is (you'll need to upload to eBay Picture Services)
        return filenames
    
    def _create_listing_payload(self, item: pd.Series) -> Dict[str, Any]:
        """Create the eBay listing payload for an item."""
        config = self._load_config()
        defaults = config.get("defaults", {})
        policies = config.get("policies", {})
        
        # Calculate auction end time
        end_time = datetime.now() + timedelta(days=self.auction_duration)
        
        # Process images
        image_urls = self._process_images(str(item["Photo Files"]))
        
        # Enhance with AI analysis if available
        enhanced_data = self._enhance_with_ai(item, image_urls)
        
        # Create the listing payload
        payload = {
            "product": {
                "title": enhanced_data.get("title", item["Title"][:defaults.get("max_title_length", 80)]),
                "description": enhanced_data.get("description", item["Description"]),
                "aspects": {
                    "Brand": [enhanced_data.get("brand", item.get("eBay - Brand", defaults.get("default_brand", "Unbranded")))],
                    "Type": [enhanced_data.get("type", item.get("eBay - Type", defaults.get("default_type", "Collectible")))],
                    "Material": [enhanced_data.get("material", item.get("eBay - Material", defaults.get("default_material", "Mixed Materials")))],
                    "Color": [enhanced_data.get("color", item.get("eBay - Color", defaults.get("default_color", "Multicolor")))],
                    "Country/Region of Manufacture": [enhanced_data.get("country", item.get("eBay - Country/Region of Manufacture", defaults.get("default_country", "Unknown")))]
                }
            },
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": int(item["Quantity"])
                }
            },
            "condition": self._map_condition_to_ebay(str(item["Condition"])),
            "packageWeightAndSize": {
                "weight": {
                    "value": defaults.get("default_weight", 1.0),
                    "unit": defaults.get("default_weight_unit", "POUND")
                }
            },
            "price": {
                "value": enhanced_data.get("suggested_price", float(item["Estimated Median Sale Price"])),
                "currency": defaults.get("currency", "USD")
            },
            "format": "AUCTION",
            "marketplaceId": defaults.get("marketplace_id", "EBAY_US"),
            "categoryId": self._map_category_to_ebay(str(item["Category"])),
            "listingPolicies": {
                "fulfillmentPolicyId": policies.get("fulfillment_policy_id", "FREIGHT_SHIPPING"),
                "paymentPolicyId": policies.get("payment_policy_id", "PAYMENT_IMMEDIATE"),
                "returnPolicyId": policies.get("return_policy_id", "RETURN_30_DAYS")
            }
        }
        
        # Add images if available
        if image_urls:
            payload["product"]["imageUrls"] = image_urls[:defaults.get("max_images", 12)]
        
        # Set auction end time
        payload["auction"] = {
            "endTime": end_time.isoformat() + "Z"
        }
        
        return payload
    
    def _enhance_with_ai(self, item: pd.Series, image_urls: List[str]) -> Dict[str, Any]:
        """Enhance listing data with AI analysis if available."""
        if not self.ai_service or not self.user_config_manager:
            return {}
        
        # Check if user has AI configured
        if not self.user_config_manager.has_valid_ai_config(self.user_id):
            logger.info(f"User {self.user_id} has no AI configuration - using basic data")
            return {}
        
        try:
            # Get user's AI configuration
            user_config = self.user_config_manager.get_user_config(self.user_id)
            
            # Convert image URLs to local paths for AI analysis
            image_paths = []
            for url in image_urls:
                if url.startswith("http"):
                    # For now, skip external URLs - would need to download
                    continue
                else:
                    # Assume local file path
                    image_paths.append(url)
            
            if not image_paths:
                logger.warning("No local images found for AI analysis")
                return {}
            
            # Analyze with AI
            logger.info(f"Analyzing {len(image_paths)} images with AI for user {self.user_id}")
            ai_result = self.ai_service.analyze_item_images(image_paths, user_config)
            
            # Record usage
            from ai_providers import UsageTracker
            tracker = UsageTracker()
            tracker.record_usage(self.user_id, user_config.get("ai_provider"))
            
            # Extract and enhance data
            enhanced_data = {
                "title": ai_result.get("title", item["Title"]),
                "description": ai_result.get("description", item["Description"]),
                "brand": ai_result.get("brand", item.get("eBay - Brand", "Unknown")),
                "type": ai_result.get("type", item.get("eBay - Type", "Collectible")),
                "material": ai_result.get("material", item.get("eBay - Material", "Mixed Materials")),
                "color": ai_result.get("color", item.get("eBay - Color", "Multicolor")),
                "country": ai_result.get("country", item.get("eBay - Country/Region of Manufacture", "Unknown")),
                "suggested_price": self._extract_price_from_ai(ai_result.get("value_range", ""))
            }
            
            logger.info(f"AI enhancement completed for item: {enhanced_data.get('title', 'Unknown')}")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
            return {}
    
    def _extract_price_from_ai(self, value_range: str) -> float:
        """Extract numeric price from AI value range string."""
        import re
        
        # Look for price patterns like "$10-50", "$25", "10-50", etc.
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',  # $25, $25.50
            r'(\d+(?:\.\d{2})?)\s*-\s*(\d+(?:\.\d{2})?)',  # 10-50, 25.50-75.25
            r'\$(\d+(?:\.\d{2})?)\s*-\s*\$(\d+(?:\.\d{2})?)'  # $10-$50
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, value_range)
            if matches:
                if len(matches[0]) == 2:  # Range
                    try:
                        min_price = float(matches[0][0])
                        max_price = float(matches[0][1])
                        return (min_price + max_price) / 2  # Use average
                    except ValueError:
                        continue
                else:  # Single price
                    try:
                        return float(matches[0])
                    except ValueError:
                        continue
        
        return 0.0  # Default if no price found
    
    def create_listing(self, item: pd.Series) -> Optional[str]:
        """Create a single eBay listing."""
        try:
            payload = self._create_listing_payload(item)
            
            # Use Inventory API to create listing
            url = f"{self.auth.base_url}/sell/inventory/v1/inventory_item"
            
            response = requests.post(
                url,
                headers=self.auth.get_headers(),
                json=payload
            )
            
            if response.status_code == 201:
                listing_id = response.json().get("listingId")
                logger.info(f"Created listing {listing_id} for '{item['Title']}'")
                return listing_id
            else:
                logger.error(f"Failed to create listing for '{item['Title']}': {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating listing for '{item['Title']}': {e}")
            return None
    
    def process_inventory(self, start_index: int = 0, max_items: Optional[int] = None) -> None:
        """Process inventory items and create eBay listings."""
        items_to_process = self.inventory_data.iloc[start_index:]
        
        if max_items:
            items_to_process = items_to_process.head(max_items)
        
        total_items = len(items_to_process)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating eBay listings...", total=total_items)
            
            for idx, item in items_to_process.iterrows():
                try:
                    listing_id = self.create_listing(item)
                    
                    if listing_id:
                        self.processed_items.append({
                            "index": idx,
                            "title": item["Title"],
                            "listing_id": listing_id,
                            "status": "success"
                        })
                    else:
                        self.failed_items.append({
                            "index": idx,
                            "title": item["Title"],
                            "error": "Failed to create listing"
                        })
                    
                    # Rate limiting - eBay has API limits
                    time.sleep(1)
                    
                except Exception as e:
                    self.failed_items.append({
                        "index": idx,
                        "title": item["Title"],
                        "error": str(e)
                    })
                
                progress.advance(task)
    
    def generate_report(self) -> None:
        """Generate a summary report of the listing process."""
        console.print("\n" + "="*60)
        console.print("[bold blue]eBay Listing Report[/bold blue]")
        console.print("="*60)
        
        # Summary table
        table = Table(title="Listing Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        
        table.add_row("Total Items Processed", str(len(self.processed_items) + len(self.failed_items)))
        table.add_row("Successful Listings", str(len(self.processed_items)))
        table.add_row("Failed Listings", str(len(self.failed_items)))
        table.add_row("Success Rate", f"{(len(self.processed_items) / (len(self.processed_items) + len(self.failed_items)) * 100):.1f}%")
        
        console.print(table)
        
        # Failed items details
        if self.failed_items:
            console.print("\n[bold red]Failed Items:[/bold red]")
            for item in self.failed_items:
                console.print(f"• {item['title']}: {item['error']}")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_processed": len(self.processed_items) + len(self.failed_items),
                "successful": len(self.processed_items),
                "failed": len(self.failed_items),
                "success_rate": len(self.processed_items) / (len(self.processed_items) + len(self.failed_items)) * 100
            },
            "processed_items": self.processed_items,
            "failed_items": self.failed_items
        }
        
        report_file = f"listing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        console.print(f"\n[green]Detailed report saved to: {report_file}[/green]")


@click.command()
@click.option('--csv-file', default='masterebaysheet_with_quantity_49items_2025-07-03.csv', 
              help='Path to the CSV inventory file')
@click.option('--draft-mode', is_flag=True, default=True, 
              help='Create listings in draft mode (default: True)')
@click.option('--start-index', default=0, type=int, 
              help='Start processing from this index (0-based)')
@click.option('--max-items', type=int, 
              help='Maximum number of items to process')
@click.option('--dry-run', is_flag=True, 
              help='Show what would be created without actually creating listings')
@click.option('--user-id', default='default_user', 
              help='User ID for AI configuration')
@click.option('--setup-ai', is_flag=True, 
              help='Setup AI provider configuration')
def main(csv_file: str, draft_mode: bool, start_index: int, max_items: Optional[int], 
         dry_run: bool, user_id: str, setup_ai: bool):
    """Runway & Rivets eBay Lister - Automated mass listing tool."""
    
    console.print(Panel.fit(
        "[bold blue]Runway & Rivets eBay Lister[/bold blue]\n"
        "Automated mass listing of vintage and collectible inventory",
        border_style="blue"
    ))
    
    try:
        # Handle AI setup
        if setup_ai:
            try:
                from user_config import UserInterface
                ui = UserInterface()
                ui.setup_user_ai(user_id)
                return
            except ImportError:
                console.print("[red]Error: AI configuration not available[/red]")
                return
        
        # Validate CSV file exists
        if not os.path.exists(csv_file):
            console.print(f"[red]Error: CSV file '{csv_file}' not found[/red]")
            return
        
        # Initialize lister
        lister = EbayLister(csv_file, draft_mode, user_id)
        
        # Show AI status if available
        if lister.user_config_manager:
            try:
                from user_config import UserInterface
                ui = UserInterface()
                ui.show_user_status(user_id)
            except Exception as e:
                logger.warning(f"Could not show AI status: {e}")
        
        if dry_run:
            console.print("[yellow]DRY RUN MODE - No listings will be created[/yellow]")
            console.print(f"Would process {len(lister.inventory_data)} items from {csv_file}")
            return
        
        # Process inventory
        lister.process_inventory(start_index, max_items)
        
        # Generate report
        lister.generate_report()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 