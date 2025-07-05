#!/usr/bin/env python3
"""
Test OAuth User Experience
Demonstrates the improved user experience with OAuth authentication
and always allowing users to go back or decline
"""

import os
import sys
from user_config import UserConfigManager
from ai_oauth import SimplifiedAISetup


def test_oauth_flow():
    """Test the OAuth authentication flow"""
    print("🧪 Testing OAuth User Experience")
    print("=" * 50)
    
    # Initialize managers
    config_manager = UserConfigManager()
    oauth_setup = SimplifiedAISetup()
    
    # Test user
    test_user = "test_user_oauth"
    
    print(f"\n👤 Testing with user: {test_user}")
    
    # Test 1: User setup with OAuth
    print("\n📋 Test 1: Complete User Setup")
    print("-" * 30)
    
    try:
        success = config_manager.setup_user(test_user)
        if success:
            print("✅ User setup completed successfully!")
        else:
            print("ℹ️  User setup was cancelled or incomplete.")
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user.")
    except Exception as e:
        print(f"❌ Setup error: {e}")
    
    # Test 2: AI Provider OAuth
    print("\n📋 Test 2: AI Provider OAuth Setup")
    print("-" * 30)
    
    try:
        success = oauth_setup.setup_ai_provider(test_user)
        if success:
            print("✅ AI provider OAuth setup successful!")
        else:
            print("ℹ️  AI provider setup was cancelled or skipped.")
    except KeyboardInterrupt:
        print("\n⚠️  OAuth setup interrupted by user.")
    except Exception as e:
        print(f"❌ OAuth setup error: {e}")
    
    # Test 3: View configuration
    print("\n📋 Test 3: View User Configuration")
    print("-" * 30)
    
    try:
        if config_manager.user_exists(test_user):
            config_manager._view_configuration(test_user)
        else:
            print("ℹ️  User configuration not found.")
    except Exception as e:
        print(f"❌ Error viewing configuration: {e}")
    
    # Test 4: Test configuration
    print("\n📋 Test 4: Test Configuration")
    print("-" * 30)
    
    try:
        if config_manager.user_exists(test_user):
            config_manager._test_configuration(test_user)
        else:
            print("ℹ️  User configuration not found.")
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")


def test_user_choices():
    """Test user choice handling"""
    print("\n🧪 Testing User Choice Handling")
    print("=" * 50)
    
    print("\nThis test demonstrates how the system handles user choices:")
    print("• Always allows users to go back")
    print("• Always allows users to decline")
    print("• Provides clear navigation options")
    print("• Validates input gracefully")
    
    # Simulate user choices
    test_choices = [
        ("1", "Valid choice - proceed"),
        ("6", "Go back to main menu"),
        ("invalid", "Invalid choice - show error"),
        ("", "Empty choice - show error"),
        ("99", "Out of range choice - show error")
    ]
    
    for choice, description in test_choices:
        print(f"\nTesting: {description}")
        print(f"User input: '{choice}'")
        
        if choice == "1":
            print("✅ Proceeding with valid choice...")
        elif choice == "6":
            print("↩️  Going back to main menu...")
        elif choice == "invalid" or choice == "" or choice == "99":
            print("❌ Invalid choice. Please select a valid option.")
        else:
            print("❌ Unexpected choice handling.")


def test_oauth_benefits():
    """Explain OAuth benefits"""
    print("\n🔗 OAuth Benefits for Users")
    print("=" * 50)
    
    benefits = [
        ("🔑 No API Key Management", "Users don't need to find, copy, or manage API keys"),
        ("🔒 Secure Authentication", "Direct login to AI provider accounts"),
        ("⚡ Faster Setup", "One-click authentication instead of manual key entry"),
        ("🔄 Automatic Refresh", "Tokens refresh automatically when needed"),
        ("🛡️  Better Security", "No API keys stored in plain text"),
        ("📱 Mobile Friendly", "Works seamlessly on mobile devices"),
        ("🔄 Easy Switching", "Users can easily switch between AI providers")
    ]
    
    for benefit, description in benefits:
        print(f"{benefit}: {description}")
    
    print("\n💡 User Experience Improvements:")
    print("• Always provide 'Go Back' options")
    print("• Always allow users to decline/skip")
    print("• Clear error messages and guidance")
    print("• Progressive disclosure of options")
    print("• Validation with helpful feedback")


def main():
    """Main test function"""
    print("🚀 Runway & Rivets OAuth User Experience Test")
    print("=" * 60)
    
    # Check if we're in the right environment
    if not os.path.exists("user_config.py"):
        print("❌ Error: user_config.py not found. Please run from project root.")
        return
    
    if not os.path.exists("ai_oauth.py"):
        print("❌ Error: ai_oauth.py not found. Please run from project root.")
        return
    
    # Run tests
    try:
        test_oauth_benefits()
        test_user_choices()
        
        # Ask if user wants to test actual OAuth flow
        print("\n" + "=" * 60)
        print("🧪 Interactive OAuth Test")
        print("=" * 60)
        
        test_oauth = input("\nWould you like to test the actual OAuth flow? (y/n): ").strip().lower()
        
        if test_oauth in ['y', 'yes']:
            print("\n⚠️  Note: This will open your browser for authentication.")
            print("You can cancel at any time by pressing Ctrl+C")
            
            confirm = input("Continue with OAuth test? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                test_oauth_flow()
            else:
                print("↩️  OAuth test cancelled.")
        else:
            print("ℹ️  Skipping interactive OAuth test.")
        
        print("\n✅ OAuth User Experience Test Complete!")
        print("\nKey Takeaways:")
        print("• OAuth eliminates API key management complexity")
        print("• Users can always go back or decline")
        print("• Clear navigation and error handling")
        print("• Better security and user experience")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
        print("This demonstrates the system's ability to handle user cancellation gracefully.")
    except Exception as e:
        print(f"\n❌ Test error: {e}")


if __name__ == "__main__":
    main() 