#!/usr/bin/env python3
"""
User Configuration Manager with OAuth Support
Handles user-specific settings, AI provider configuration, and OAuth authentication
"""

import os
import json
import logging
from typing import Dict, Optional, Any, List
from cryptography.fernet import Fernet
from ai_oauth import SimplifiedAISetup

logger = logging.getLogger(__name__)


class UserConfigManager:
    """Manages user-specific configurations with OAuth support"""
    
    def __init__(self, config_dir: str = "user_configs"):
        self.config_dir = config_dir
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        self.oauth_setup = SimplifiedAISetup()
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get existing encryption key or create new one"""
        key_file = ".encryption_key"
        
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
    
    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data).decode()
    
    def get_user_config_path(self, user_id: str) -> str:
        """Get path to user's configuration file"""
        return os.path.join(self.config_dir, f"{user_id}.json")
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user configuration exists"""
        return os.path.exists(self.get_user_config_path(user_id))
    
    def create_user(self, user_id: str) -> bool:
        """Create new user configuration"""
        try:
            if self.user_exists(user_id):
                print(f"⚠️  User '{user_id}' already exists.")
                return False
            
            # Default configuration
            config = {
                "user_id": user_id,
                "created_at": self._get_timestamp(),
                "ai_provider": None,
                "ai_api_key": None,
                "ebay_app_id": None,
                "ebay_cert_id": None,
                "ebay_dev_id": None,
                "ebay_refresh_token": None,
                "preferences": {
                    "auto_enhance_listings": True,
                    "draft_mode": True,
                    "image_analysis": True,
                    "metadata_generation": True
                },
                "usage_stats": {
                    "listings_created": 0,
                    "ai_requests": 0,
                    "last_used": None
                }
            }
            
            self._save_user_config(user_id, config)
            print(f"✅ User '{user_id}' created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {e}")
            return False
    
    def setup_user(self, user_id: str) -> bool:
        """Complete user setup with guided configuration"""
        print(f"\n👤 User Setup: {user_id}")
        print("=" * 50)
        
        # Create user if doesn't exist
        if not self.user_exists(user_id):
            if not self.create_user(user_id):
                return False
        
        # Main setup menu
        while True:
            print(f"\n📋 Setup Menu for {user_id}:")
            print("1. Configure AI Provider (OAuth/API Key)")
            print("2. Configure eBay API Credentials")
            print("3. View Current Configuration")
            print("4. Test Configuration")
            print("5. Complete Setup")
            print("6. Exit Setup")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._setup_ai_provider(user_id)
            elif choice == "2":
                self._setup_ebay_credentials(user_id)
            elif choice == "3":
                self._view_configuration(user_id)
            elif choice == "4":
                self._test_configuration(user_id)
            elif choice == "5":
                if self._validate_complete_setup(user_id):
                    print("✅ Setup completed successfully!")
                    return True
                else:
                    print("⚠️  Setup incomplete. Please configure required settings.")
            elif choice == "6":
                print("👋 Setup cancelled. You can return anytime.")
                return False
            else:
                print("❌ Invalid choice. Please select 1-6.")
    
    def _setup_ai_provider(self, user_id: str):
        """Setup AI provider with OAuth or manual API key"""
        print(f"\n🤖 AI Provider Setup for {user_id}")
        
        # Use the OAuth setup system
        success = self.oauth_setup.setup_ai_provider(user_id)
        
        if success:
            print("✅ AI provider configured successfully!")
        else:
            print("ℹ️  AI provider setup skipped or cancelled.")
    
    def _setup_ebay_credentials(self, user_id: str):
        """Setup eBay API credentials"""
        print(f"\n🛒 eBay API Setup for {user_id}")
        print("You'll need your eBay Developer credentials.")
        
        confirm = input("Continue with eBay setup? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("↩️  eBay setup cancelled.")
            return
        
        print("\nGet your credentials from: https://developer.ebay.com/my/keys")
        
        # App ID
        while True:
            app_id = input("Enter eBay App ID (or 'back' to go back): ").strip()
            if app_id.lower() == 'back':
                print("↩️  Going back...")
                return
            if app_id:
                break
            print("❌ App ID cannot be empty.")
        
        # Cert ID
        while True:
            cert_id = input("Enter eBay Cert ID (or 'back' to go back): ").strip()
            if cert_id.lower() == 'back':
                print("↩️  Going back...")
                return
            if cert_id:
                break
            print("❌ Cert ID cannot be empty.")
        
        # Dev ID
        while True:
            dev_id = input("Enter eBay Dev ID (or 'back' to go back): ").strip()
            if dev_id.lower() == 'back':
                print("↩️  Going back...")
                return
            if dev_id:
                break
            print("❌ Dev ID cannot be empty.")
        
        # Save credentials
        try:
            config = self._load_user_config(user_id)
            config["ebay_app_id"] = app_id
            config["ebay_cert_id"] = cert_id
            config["ebay_dev_id"] = dev_id
            self._save_user_config(user_id, config)
            print("✅ eBay credentials saved successfully!")
        except Exception as e:
            print(f"❌ Error saving credentials: {e}")
    
    def _view_configuration(self, user_id: str):
        """View current user configuration"""
        try:
            config = self._load_user_config(user_id)
            
            print(f"\n📊 Configuration for {user_id}:")
            print("=" * 40)
            
            # AI Provider
            ai_provider = config.get("ai_provider", "Not configured")
            print(f"🤖 AI Provider: {ai_provider}")
            
            # eBay Credentials
            ebay_app_id = config.get("ebay_app_id", "Not configured")
            print(f"🛒 eBay App ID: {ebay_app_id}")
            
            # Preferences
            prefs = config.get("preferences", {})
            print(f"⚙️  Auto-enhance listings: {prefs.get('auto_enhance_listings', False)}")
            print(f"⚙️  Draft mode: {prefs.get('draft_mode', False)}")
            
            # Usage Stats
            stats = config.get("usage_stats", {})
            print(f"📈 Listings created: {stats.get('listings_created', 0)}")
            print(f"📈 AI requests: {stats.get('ai_requests', 0)}")
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
    
    def _test_configuration(self, user_id: str):
        """Test current configuration"""
        print(f"\n🧪 Testing Configuration for {user_id}")
        
        try:
            config = self._load_user_config(user_id)
            
            # Test AI Provider
            if config.get("ai_provider"):
                print(f"✅ AI Provider: {config['ai_provider']} configured")
            else:
                print("⚠️  AI Provider: Not configured")
            
            # Test eBay Credentials
            if config.get("ebay_app_id"):
                print("✅ eBay App ID: Configured")
            else:
                print("⚠️  eBay App ID: Not configured")
            
            if config.get("ebay_cert_id"):
                print("✅ eBay Cert ID: Configured")
            else:
                print("⚠️  eBay Cert ID: Not configured")
            
            if config.get("ebay_dev_id"):
                print("✅ eBay Dev ID: Configured")
            else:
                print("⚠️  eBay Dev ID: Not configured")
            
        except Exception as e:
            print(f"❌ Error testing configuration: {e}")
    
    def _validate_complete_setup(self, user_id: str) -> bool:
        """Validate if user setup is complete"""
        try:
            config = self._load_user_config(user_id)
            
            # Check required fields
            required_fields = ["ebay_app_id", "ebay_cert_id", "ebay_dev_id"]
            missing_fields = [field for field in required_fields if not config.get(field)]
            
            if missing_fields:
                print(f"❌ Missing required fields: {', '.join(missing_fields)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating setup: {e}")
            return False
    
    def get_ai_provider(self, user_id: str) -> Optional[str]:
        """Get user's AI provider"""
        try:
            config = self._load_user_config(user_id)
            return config.get("ai_provider")
        except Exception as e:
            logger.error(f"Error getting AI provider: {e}")
            return None
    
    def get_ai_api_key(self, user_id: str) -> Optional[str]:
        """Get user's AI API key (decrypted)"""
        try:
            config = self._load_user_config(user_id)
            encrypted_key = config.get("ai_api_key")
            if encrypted_key:
                # Convert string back to bytes for decryption
                encrypted_bytes = encrypted_key.encode('latin1')
                return self._decrypt_data(encrypted_bytes)
            return None
        except Exception as e:
            logger.error(f"Error getting AI API key: {e}")
            return None
    
    def set_ai_provider(self, user_id: str, provider: str, api_key: str):
        """Set user's AI provider and API key"""
        try:
            config = self._load_user_config(user_id)
            config["ai_provider"] = provider
            # Convert bytes to base64 string for JSON serialization
            encrypted_bytes = self._encrypt_data(api_key)
            config["ai_api_key"] = encrypted_bytes.decode('latin1')  # Store as string
            self._save_user_config(user_id, config)
        except Exception as e:
            logger.error(f"Error setting AI provider: {e}")
            raise
    
    def get_ebay_credentials(self, user_id: str) -> Dict[str, Optional[str]]:
        """Get user's eBay credentials"""
        try:
            config = self._load_user_config(user_id)
            return {
                "app_id": config.get("ebay_app_id"),
                "cert_id": config.get("ebay_cert_id"),
                "dev_id": config.get("ebay_dev_id"),
                "refresh_token": config.get("ebay_refresh_token")
            }
        except Exception as e:
            logger.error(f"Error getting eBay credentials: {e}")
            return {}
    
    def set_ebay_refresh_token(self, user_id: str, refresh_token: str):
        """Set user's eBay refresh token"""
        try:
            config = self._load_user_config(user_id)
            config["ebay_refresh_token"] = refresh_token
            self._save_user_config(user_id, config)
        except Exception as e:
            logger.error(f"Error setting eBay refresh token: {e}")
            raise
    
    def get_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's preferences"""
        try:
            config = self._load_user_config(user_id)
            return config.get("preferences", {})
        except Exception as e:
            logger.error(f"Error getting preferences: {e}")
            return {}
    
    def update_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user's preferences"""
        try:
            config = self._load_user_config(user_id)
            config["preferences"].update(preferences)
            self._save_user_config(user_id, config)
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            raise
    
    def increment_usage(self, user_id: str, metric: str):
        """Increment usage statistics"""
        try:
            config = self._load_user_config(user_id)
            if "usage_stats" not in config:
                config["usage_stats"] = {}
            
            config["usage_stats"][metric] = config["usage_stats"].get(metric, 0) + 1
            config["usage_stats"]["last_used"] = self._get_timestamp()
            
            self._save_user_config(user_id, config)
        except Exception as e:
            logger.error(f"Error incrementing usage: {e}")
    
    def _load_user_config(self, user_id: str) -> Dict[str, Any]:
        """Load user configuration from file"""
        config_path = self.get_user_config_path(user_id)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"User configuration not found: {user_id}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _save_user_config(self, user_id: str, config: Dict[str, Any]):
        """Save user configuration to file"""
        config_path = self.get_user_config_path(user_id)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def list_users(self) -> List[str]:
        """List all configured users"""
        try:
            users = []
            for filename in os.listdir(self.config_dir):
                if filename.endswith('.json'):
                    user_id = filename[:-5]  # Remove .json extension
                    users.append(user_id)
            return users
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user configuration"""
        try:
            config_path = self.get_user_config_path(user_id)
            if os.path.exists(config_path):
                os.remove(config_path)
                print(f"✅ User '{user_id}' deleted successfully!")
                return True
            else:
                print(f"⚠️  User '{user_id}' not found.")
                return False
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return False


# Interactive CLI for user management
def main():
    """Interactive CLI for user configuration management"""
    config_manager = UserConfigManager()
    
    print("👤 Runway & Rivets User Configuration Manager")
    print("=" * 50)
    
    while True:
        print("\n📋 Main Menu:")
        print("1. Setup New User")
        print("2. Manage Existing User")
        print("3. List All Users")
        print("4. Delete User")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            user_id = input("Enter user ID: ").strip()
            if user_id:
                config_manager.setup_user(user_id)
            else:
                print("❌ User ID cannot be empty.")
        
        elif choice == "2":
            users = config_manager.list_users()
            if users:
                print("\nExisting users:")
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user}")
                
                try:
                    user_choice = int(input("\nSelect user number: ")) - 1
                    if 0 <= user_choice < len(users):
                        config_manager.setup_user(users[user_choice])
                    else:
                        print("❌ Invalid selection.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                print("ℹ️  No users found.")
        
        elif choice == "3":
            users = config_manager.list_users()
            if users:
                print("\nConfigured users:")
                for user in users:
                    print(f"• {user}")
            else:
                print("ℹ️  No users found.")
        
        elif choice == "4":
            users = config_manager.list_users()
            if users:
                print("\nSelect user to delete:")
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user}")
                
                try:
                    user_choice = int(input("\nSelect user number: ")) - 1
                    if 0 <= user_choice < len(users):
                        confirm = input(f"Are you sure you want to delete '{users[user_choice]}'? (y/n): ").strip().lower()
                        if confirm in ['y', 'yes']:
                            config_manager.delete_user(users[user_choice])
                        else:
                            print("↩️  Deletion cancelled.")
                    else:
                        print("❌ Invalid selection.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                print("ℹ️  No users found.")
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main() 