#!/usr/bin/env python3
"""
Supabase Database Manager
Handles all database operations for the Runway & Rivets eBay Lister
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
import asyncio
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase library not installed. Run: pip install supabase")

logger = logging.getLogger(__name__)


class ListingStatus(Enum):
    """Enum for listing status"""
    DRAFT = "draft"
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
    DELETED = "deleted"


@dataclass
class User:
    """User data model"""
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    ai_provider: Optional[str] = None
    ai_api_key_encrypted: Optional[str] = None
    ebay_app_id: Optional[str] = None
    ebay_cert_id: Optional[str] = None
    ebay_dev_id: Optional[str] = None
    ebay_refresh_token: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    usage_stats: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Listing:
    """Listing data model"""
    id: Optional[str] = None
    user_id: str = ""
    title: str = ""
    description: str = ""
    category: str = ""
    condition: str = ""
    estimated_price: str = ""
    brand: str = ""
    item_type: str = ""
    material: str = ""
    color: str = ""
    country_of_manufacture: str = ""
    image_urls: List[str] = None
    user_message: str = ""
    ai_provider: str = ""
    ai_generated: bool = True
    status: str = ListingStatus.DRAFT.value
    ebay_listing_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if self.image_urls is None:
            self.image_urls = []
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc).isoformat()


@dataclass
class AIUsage:
    """AI usage tracking model"""
    id: Optional[str] = None
    user_id: str = ""
    provider: str = ""
    model: str = ""
    tokens_used: int = 0
    cost: float = 0.0
    request_type: str = ""
    success: bool = True
    error_message: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()


class SupabaseManager:
    """Manages all Supabase database operations"""
    
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """Initialize Supabase client"""
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_ANON_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not SUPABASE_AVAILABLE:
            raise ImportError("Supabase library not installed. Run: pip install supabase")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required")
        
        try:
            self.client: Client = create_client(self.url, self.key)
            logger.info("✅ Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase client: {e}")
            raise
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and basic operations"""
        results = {
            "connection": False,
            "tables": {},
            "operations": {},
            "errors": []
        }
        
        try:
            # Test basic connection
            response = self.client.table("users").select("count", count="exact").limit(1).execute()
            results["connection"] = True
            logger.info("✅ Database connection successful")
            
            # Test table access
            tables_to_test = ["users", "listings", "ai_usage"]
            for table in tables_to_test:
                try:
                    response = self.client.table(table).select("*").limit(1).execute()
                    results["tables"][table] = "accessible"
                except Exception as e:
                    results["tables"][table] = f"error: {str(e)}"
                    results["errors"].append(f"Table {table}: {e}")
            
            # Test basic CRUD operations
            results["operations"] = self._test_crud_operations()
            
        except Exception as e:
            results["connection"] = False
            results["errors"].append(f"Connection failed: {e}")
            logger.error(f"❌ Database connection failed: {e}")
        
        return results
    
    def _test_crud_operations(self) -> Dict[str, str]:
        """Test basic CRUD operations"""
        operations = {}
        
        try:
            # Test CREATE
            test_user = User(
                id="test_user_crud",
                email="test@example.com",
                name="Test User"
            )
            self.create_user(test_user)
            operations["create"] = "success"
            
            # Test READ
            user = self.get_user("test_user_crud")
            if user:
                operations["read"] = "success"
            else:
                operations["read"] = "failed"
            
            # Test UPDATE
            test_user.name = "Updated Test User"
            self.update_user(test_user)
            updated_user = self.get_user("test_user_crud")
            if updated_user and updated_user.name == "Updated Test User":
                operations["update"] = "success"
            else:
                operations["update"] = "failed"
            
            # Test DELETE
            self.delete_user("test_user_crud")
            deleted_user = self.get_user("test_user_crud")
            if not deleted_user:
                operations["delete"] = "success"
            else:
                operations["delete"] = "failed"
                
        except Exception as e:
            operations["error"] = str(e)
            logger.error(f"CRUD test error: {e}")
        
        return operations
    
    # User Management Methods
    def create_user(self, user: User) -> bool:
        """Create a new user"""
        try:
            user_data = asdict(user)
            user_data["created_at"] = datetime.now(timezone.utc).isoformat()
            user_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.table("users").insert(user_data).execute()
            
            if response.data:
                logger.info(f"✅ User {user.id} created successfully")
                return True
            else:
                logger.error(f"❌ Failed to create user {user.id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating user {user.id}: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            
            if response.data:
                user_data = response.data[0]
                return User(**user_data)
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting user {user_id}: {e}")
            return None
    
    def update_user(self, user: User) -> bool:
        """Update user"""
        try:
            user_data = asdict(user)
            user_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.table("users").update(user_data).eq("id", user.id).execute()
            
            if response.data:
                logger.info(f"✅ User {user.id} updated successfully")
                return True
            else:
                logger.error(f"❌ Failed to update user {user.id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating user {user.id}: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        try:
            response = self.client.table("users").delete().eq("id", user_id).execute()
            
            if response.data:
                logger.info(f"✅ User {user_id} deleted successfully")
                return True
            else:
                logger.error(f"❌ Failed to delete user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error deleting user {user_id}: {e}")
            return False
    
    def list_users(self) -> List[User]:
        """List all users"""
        try:
            response = self.client.table("users").select("*").execute()
            
            users = []
            for user_data in response.data:
                users.append(User(**user_data))
            
            return users
            
        except Exception as e:
            logger.error(f"❌ Error listing users: {e}")
            return []
    
    # Listing Management Methods
    def create_listing(self, listing: Listing) -> Optional[str]:
        """Create a new listing"""
        try:
            listing_data = asdict(listing)
            listing_data["created_at"] = datetime.now(timezone.utc).isoformat()
            listing_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.table("listings").insert(listing_data).execute()
            
            if response.data:
                listing_id = response.data[0]["id"]
                logger.info(f"✅ Listing {listing_id} created successfully")
                return listing_id
            else:
                logger.error("❌ Failed to create listing")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating listing: {e}")
            return None
    
    def get_listing(self, listing_id: str) -> Optional[Listing]:
        """Get listing by ID"""
        try:
            response = self.client.table("listings").select("*").eq("id", listing_id).execute()
            
            if response.data:
                listing_data = response.data[0]
                return Listing(**listing_data)
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting listing {listing_id}: {e}")
            return None
    
    def update_listing(self, listing: Listing) -> bool:
        """Update listing"""
        try:
            listing_data = asdict(listing)
            listing_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.table("listings").update(listing_data).eq("id", listing.id).execute()
            
            if response.data:
                logger.info(f"✅ Listing {listing.id} updated successfully")
                return True
            else:
                logger.error(f"❌ Failed to update listing {listing.id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating listing {listing.id}: {e}")
            return False
    
    def delete_listing(self, listing_id: str) -> bool:
        """Delete listing"""
        try:
            response = self.client.table("listings").delete().eq("id", listing_id).execute()
            
            if response.data:
                logger.info(f"✅ Listing {listing_id} deleted successfully")
                return True
            else:
                logger.error(f"❌ Failed to delete listing {listing_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error deleting listing {listing_id}: {e}")
            return False
    
    def get_user_listings(self, user_id: str) -> List[Listing]:
        """Get all listings for a user"""
        try:
            response = self.client.table("listings").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            
            listings = []
            for listing_data in response.data:
                listings.append(Listing(**listing_data))
            
            return listings
            
        except Exception as e:
            logger.error(f"❌ Error getting listings for user {user_id}: {e}")
            return []
    
    def search_listings(self, user_id: str, query: str) -> List[Listing]:
        """Search listings by title or description"""
        try:
            response = self.client.table("listings").select("*").eq("user_id", user_id).or_(f"title.ilike.%{query}%,description.ilike.%{query}%").execute()
            
            listings = []
            for listing_data in response.data:
                listings.append(Listing(**listing_data))
            
            return listings
            
        except Exception as e:
            logger.error(f"❌ Error searching listings: {e}")
            return []
    
    # AI Usage Tracking Methods
    def log_ai_usage(self, usage: AIUsage) -> bool:
        """Log AI usage for tracking"""
        try:
            usage_data = asdict(usage)
            usage_data["created_at"] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.table("ai_usage").insert(usage_data).execute()
            
            if response.data:
                logger.info(f"✅ AI usage logged successfully")
                return True
            else:
                logger.error("❌ Failed to log AI usage")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error logging AI usage: {e}")
            return False
    
    def get_user_ai_usage(self, user_id: str, days: int = 30) -> List[AIUsage]:
        """Get AI usage for a user within specified days"""
        try:
            from datetime import timedelta
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            response = self.client.table("ai_usage").select("*").eq("user_id", user_id).gte("created_at", cutoff_date.isoformat()).order("created_at", desc=True).execute()
            
            usage_records = []
            for usage_data in response.data:
                usage_records.append(AIUsage(**usage_data))
            
            return usage_records
            
        except Exception as e:
            logger.error(f"❌ Error getting AI usage for user {user_id}: {e}")
            return []
    
    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        try:
            # Get total listings
            listings_response = self.client.table("listings").select("count", count="exact").eq("user_id", user_id).execute()
            total_listings = listings_response.count or 0
            
            # Get AI usage in last 30 days
            ai_usage = self.get_user_ai_usage(user_id, 30)
            total_ai_requests = len(ai_usage)
            total_cost = sum(usage.cost for usage in ai_usage)
            
            # Get active listings
            active_response = self.client.table("listings").select("count", count="exact").eq("user_id", user_id).eq("status", ListingStatus.ACTIVE.value).execute()
            active_listings = active_response.count or 0
            
            return {
                "total_listings": total_listings,
                "active_listings": active_listings,
                "ai_requests_30d": total_ai_requests,
                "ai_cost_30d": total_cost,
                "last_ai_usage": ai_usage[0].created_at if ai_usage else None
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting usage stats for user {user_id}: {e}")
            return {}
    
    # Database Schema Management
    def create_tables(self) -> Dict[str, bool]:
        """Create database tables (requires service role key)"""
        if not self.service_key:
            logger.error("❌ Service role key required for table creation")
            return {"error": "Service role key required"}
        
        results = {}
        
        try:
            # This would typically be done via SQL migrations
            # For now, we'll just test if tables exist
            tables = ["users", "listings", "ai_usage"]
            
            for table in tables:
                try:
                    response = self.client.table(table).select("count", count="exact").limit(1).execute()
                    results[table] = True
                except Exception as e:
                    results[table] = False
                    logger.error(f"❌ Table {table} not accessible: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error creating tables: {e}")
            results["error"] = str(e)
        
        return results
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get table schema information"""
        try:
            # This would require RPC call or direct SQL
            # For now, return expected schema
            schemas = {
                "users": {
                    "id": "text PRIMARY KEY",
                    "email": "text",
                    "name": "text",
                    "ai_provider": "text",
                    "ai_api_key_encrypted": "text",
                    "ebay_app_id": "text",
                    "ebay_cert_id": "text",
                    "ebay_dev_id": "text",
                    "ebay_refresh_token": "text",
                    "preferences": "jsonb",
                    "usage_stats": "jsonb",
                    "created_at": "timestamptz",
                    "updated_at": "timestamptz"
                },
                "listings": {
                    "id": "uuid PRIMARY KEY DEFAULT gen_random_uuid()",
                    "user_id": "text REFERENCES users(id)",
                    "title": "text",
                    "description": "text",
                    "category": "text",
                    "condition": "text",
                    "estimated_price": "text",
                    "brand": "text",
                    "item_type": "text",
                    "material": "text",
                    "color": "text",
                    "country_of_manufacture": "text",
                    "image_urls": "jsonb",
                    "user_message": "text",
                    "ai_provider": "text",
                    "ai_generated": "boolean",
                    "status": "text",
                    "ebay_listing_id": "text",
                    "created_at": "timestamptz",
                    "updated_at": "timestamptz"
                },
                "ai_usage": {
                    "id": "uuid PRIMARY KEY DEFAULT gen_random_uuid()",
                    "user_id": "text REFERENCES users(id)",
                    "provider": "text",
                    "model": "text",
                    "tokens_used": "integer",
                    "cost": "decimal",
                    "request_type": "text",
                    "success": "boolean",
                    "error_message": "text",
                    "created_at": "timestamptz"
                }
            }
            
            return schemas.get(table_name, {})
            
        except Exception as e:
            logger.error(f"❌ Error getting schema for {table_name}: {e}")
            return {}


# Utility functions
def create_supabase_manager() -> Optional[SupabaseManager]:
    """Create Supabase manager with environment variables"""
    try:
        return SupabaseManager()
    except Exception as e:
        logger.error(f"❌ Failed to create Supabase manager: {e}")
        return None


def test_supabase_connection() -> Dict[str, Any]:
    """Test Supabase connection and return results"""
    try:
        manager = create_supabase_manager()
        if manager:
            return manager.test_connection()
        else:
            return {
                "connection": False,
                "error": "Failed to create Supabase manager"
            }
    except Exception as e:
        return {
            "connection": False,
            "error": str(e)
        } 