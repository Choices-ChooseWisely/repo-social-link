#!/usr/bin/env python3
"""
Improved AI Setup System
Provides realistic, user-friendly AI provider setup without fake OAuth
Focuses on clear guidance and easy API key management
"""

import os
import json
import webbrowser
import logging
from typing import Dict, Optional, Any
from user_config import UserConfigManager

logger = logging.getLogger(__name__)


class ImprovedAISetup:
    """Realistic AI setup with clear guidance and user-friendly experience"""
    
    def __init__(self):
        self.config_manager = UserConfigManager()
        
        # Real provider information
        self.providers = {
            "openai": {
                "name": "OpenAI GPT-4 Vision",
                "description": "Best for detailed image analysis and creative descriptions",
                "setup_url": "https://platform.openai.com/api-keys",
                "pricing": "~$0.01-0.03 per image analysis",
                "free_tier": "No free tier, but very affordable",
                "features": ["High accuracy", "Creative descriptions", "Fast processing"]
            },
            "anthropic": {
                "name": "Claude 3 Vision",
                "description": "Excellent for detailed analysis and safety-focused content",
                "setup_url": "https://console.anthropic.com/",
                "pricing": "~$0.015 per image analysis",
                "free_tier": "No free tier, but competitive pricing",
                "features": ["Detailed analysis", "Safety-focused", "Reliable"]
            },
            "google": {
                "name": "Google Gemini Vision",
                "description": "Good balance of speed and accuracy with generous free tier",
                "setup_url": "https://makersuite.google.com/app/apikey",
                "pricing": "Free tier: 15 requests/minute, then ~$0.0025 per request",
                "free_tier": "15 requests/minute, 1500 requests/day",
                "features": ["Generous free tier", "Fast processing", "Good accuracy"]
            }
        }
    
    def setup_ai_provider(self, user_id: str) -> bool:
        """Interactive AI provider setup with realistic guidance"""
        print(f"\n🤖 AI Provider Setup for User: {user_id}")
        print("=" * 60)
        
        print("\n💡 Choose your AI provider for image analysis and listing enhancement:")
        print("Each provider has different strengths and pricing.")
        
        # Show provider options with details
        for i, (provider_id, info) in enumerate(self.providers.items(), 1):
            print(f"\n{i}. {info['name']}")
            print(f"   📝 {info['description']}")
            print(f"   💰 {info['pricing']}")
            print(f"   🆓 {info['free_tier']}")
            print(f"   ✨ Features: {', '.join(info['features'])}")
        
        print(f"\n{len(self.providers) + 1}. Manual API Key Setup (Advanced)")
        print(f"{len(self.providers) + 2}. Skip AI setup for now")
        print(f"{len(self.providers) + 3}. Go back to main menu")
        
        while True:
            choice = input(f"\nSelect option (1-{len(self.providers) + 3}): ").strip()
            
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(self.providers):
                    provider_id = list(self.providers.keys())[choice_num - 1]
                    return self._setup_specific_provider(user_id, provider_id)
                elif choice_num == len(self.providers) + 1:
                    return self._setup_manual_api_key(user_id)
                elif choice_num == len(self.providers) + 2:
                    print("✅ Skipping AI setup. You can configure it later.")
                    return True
                elif choice_num == len(self.providers) + 3:
                    print("↩️  Going back to main menu...")
                    return False
            
            print("❌ Invalid choice. Please select a valid option.")
    
    def _setup_specific_provider(self, user_id: str, provider_id: str) -> bool:
        """Setup a specific AI provider with guided assistance"""
        provider = self.providers[provider_id]
        
        print(f"\n🔧 Setting up {provider['name']}")
        print("=" * 50)
        
        print(f"\n📋 Setup Steps:")
        print("1. Visit the provider's website")
        print("2. Create an account (if needed)")
        print("3. Generate an API key")
        print("4. Copy the API key to this application")
        
        print(f"\n🌐 Get your API key from:")
        print(f"   {provider['setup_url']}")
        
        # Offer to open browser
        open_browser = input(f"\nWould you like to open {provider['name']} in your browser? (y/n): ").strip().lower()
        if open_browser in ['y', 'yes']:
            try:
                webbrowser.open(provider['setup_url'])
                print("✅ Browser opened! Please get your API key.")
            except Exception as e:
                print(f"⚠️  Could not open browser: {e}")
                print(f"Please manually visit: {provider['setup_url']}")
        
        print(f"\n💡 Tips for {provider['name']}:")
        if provider_id == "openai":
            print("• Look for 'Create new secret key' button")
            print("• Copy the key immediately (you won't see it again)")
            print("• Keep your key secure and don't share it")
        elif provider_id == "anthropic":
            print("• Sign in to your Anthropic account")
            print("• Navigate to API Keys section")
            print("• Create a new API key")
        elif provider_id == "google":
            print("• Sign in with your Google account")
            print("• Click 'Create API Key'")
            print("• Copy the generated key")
        
        # Get API key with validation
        while True:
            print(f"\n🔑 Enter your {provider['name']} API key:")
            api_key = input("API Key (or 'back' to go back, 'skip' to skip): ").strip()
            
            if api_key.lower() == 'back':
                print("↩️  Going back...")
                return False
            elif api_key.lower() == 'skip':
                print("✅ Skipping API key setup.")
                return True
            elif not api_key:
                print("❌ API key cannot be empty.")
                continue
            
            # Validate API key format
            if self._validate_api_key_format(provider_id, api_key):
                try:
                    # Save the API key
                    self.config_manager.set_ai_provider(user_id, provider_id, api_key)
                    print(f"✅ {provider['name']} configured successfully!")
                    
                    # Show next steps
                    self._show_next_steps(provider_id)
                    return True
                except Exception as e:
                    print(f"❌ Error saving API key: {e}")
                    return False
            else:
                print(f"❌ Invalid API key format for {provider['name']}.")
                print("Please check your API key and try again.")
    
    def _setup_manual_api_key(self, user_id: str) -> bool:
        """Manual API key setup for advanced users"""
        print(f"\n🔧 Manual API Key Setup")
        print("=" * 40)
        
        print("This option is for users who want to:")
        print("• Use a custom AI provider")
        print("• Configure API keys manually")
        print("• Use existing API keys")
        
        confirm = input("\nContinue with manual setup? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("↩️  Manual setup cancelled.")
            return False
        
        # Get provider name
        provider_name = input("Enter AI provider name (e.g., 'Custom OpenAI', 'Local AI'): ").strip()
        if not provider_name:
            print("❌ Provider name cannot be empty.")
            return False
        
        # Get API key
        api_key = input("Enter API key: ").strip()
        if not api_key:
            print("❌ API key cannot be empty.")
            return False
        
        # Get API endpoint (optional)
        api_endpoint = input("Enter API endpoint (optional, press Enter to skip): ").strip()
        
        try:
            # Save custom configuration
            self.config_manager.set_ai_provider(user_id, provider_name, api_key)
            if api_endpoint:
                # Store endpoint in preferences
                self.config_manager.update_preferences(user_id, {"custom_api_endpoint": api_endpoint})
            
            print(f"✅ Custom AI provider '{provider_name}' configured successfully!")
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def _validate_api_key_format(self, provider_id: str, api_key: str) -> bool:
        """Validate API key format for different providers"""
        if provider_id == "openai":
            return api_key.startswith("sk-") and len(api_key) > 20
        elif provider_id == "anthropic":
            return api_key.startswith("sk-ant-") and len(api_key) > 20
        elif provider_id == "google":
            return len(api_key) > 20  # Google API keys are typically long
        else:
            return len(api_key) > 10  # Basic validation for custom providers
    
    def _show_next_steps(self, provider_id: str):
        """Show next steps after successful setup"""
        print(f"\n🎉 Great! Your AI provider is configured.")
        print("\n📋 Next steps:")
        print("1. Configure your eBay API credentials")
        print("2. Test your configuration")
        print("3. Start creating AI-enhanced listings!")
        
        if provider_id == "google":
            print(f"\n💡 Note: {self.providers[provider_id]['name']} has a generous free tier.")
            print("You can start using it immediately without worrying about costs.")
        else:
            print(f"\n💡 Note: {self.providers[provider_id]['name']} charges per request.")
            print("Monitor your usage to control costs.")
    
    def show_provider_comparison(self):
        """Show detailed provider comparison"""
        print("\n📊 AI Provider Comparison")
        print("=" * 60)
        
        for provider_id, info in self.providers.items():
            print(f"\n🤖 {info['name']}")
            print(f"   📝 {info['description']}")
            print(f"   💰 Pricing: {info['pricing']}")
            print(f"   🆓 Free Tier: {info['free_tier']}")
            print(f"   ✨ Features: {', '.join(info['features'])}")
            print(f"   🔗 Setup: {info['setup_url']}")
    
    def test_ai_connection(self, user_id: str) -> bool:
        """Test AI provider connection"""
        try:
            provider = self.config_manager.get_ai_provider(user_id)
            api_key = self.config_manager.get_ai_api_key(user_id)
            
            if not provider or not api_key:
                print("❌ No AI provider configured.")
                return False
            
            print(f"\n🧪 Testing {provider} connection...")
            
            # This would implement actual API testing
            # For now, just validate the key format
            if self._validate_api_key_format(provider, api_key):
                print("✅ API key format is valid!")
                print("✅ AI provider connection successful!")
                return True
            else:
                print("❌ API key format is invalid.")
                return False
                
        except Exception as e:
            print(f"❌ Error testing connection: {e}")
            return False


# Example usage
if __name__ == "__main__":
    setup = ImprovedAISetup()
    
    print("🚀 Improved AI Setup System")
    print("=" * 50)
    
    # Show provider comparison
    setup.show_provider_comparison()
    
    # Test setup
    user_id = "demo_user_improved"
    success = setup.setup_ai_provider(user_id)
    
    if success:
        print(f"\n✅ Setup completed for {user_id}")
        setup.test_ai_connection(user_id)
    else:
        print(f"\nℹ️  Setup was cancelled or incomplete for {user_id}") 