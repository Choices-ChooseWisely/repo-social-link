#!/usr/bin/env python3
"""
Test script for Multi-AI Provider System
"""

import os
import sys
from pathlib import Path

def test_ai_providers():
    """Test AI provider system"""
    print("🧪 Testing Multi-AI Provider System")
    print("=" * 40)
    
    try:
        from ai_providers import AIProviderManager, AIService
        from user_config import UserConfigManager, UserInterface
        
        print("✅ AI providers module imported successfully")
        
        # Test provider manager
        provider_manager = AIProviderManager()
        providers = provider_manager.list_providers()
        
        print(f"✅ Found {len(providers)} AI providers:")
        for provider_id, provider in providers.items():
            print(f"   - {provider_id}: {provider.name}")
        
        # Test user config manager
        config_manager = UserConfigManager()
        print("✅ User configuration manager initialized")
        
        # Test encryption
        test_key = "test_api_key_123"
        encrypted = provider_manager.encrypt_api_key(test_key)
        decrypted = provider_manager.decrypt_api_key(encrypted)
        
        if test_key == decrypted:
            print("✅ API key encryption/decryption working")
        else:
            print("❌ API key encryption/decryption failed")
        
        # Test AI service
        ai_service = AIService()
        print("✅ AI service initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_interface():
    """Test user interface"""
    print("\n🧪 Testing User Interface")
    print("=" * 30)
    
    try:
        from user_config import UserInterface
        
        ui = UserInterface()
        print("✅ User interface initialized")
        
        # Test provider listing
        providers = ui.config_manager.list_all_providers()
        print(f"✅ Listed {len(providers)} providers")
        
        # Test user status (should show no config)
        ui.show_user_status("test_user")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_integration():
    """Test integration with main lister"""
    print("\n🧪 Testing Integration")
    print("=" * 25)
    
    try:
        from ebay_lister import EbayLister
        
        # Test lister initialization with AI
        lister = EbayLister("masterebaysheet_with_quantity_49items_2025-07-03.csv", 
                           user_id="test_user")
        
        print("✅ eBay lister initialized with AI support")
        
        if lister.ai_service:
            print("✅ AI service available in lister")
        else:
            print("⚠️  AI service not available (running in basic mode)")
        
        if lister.user_config_manager:
            print("✅ User config manager available in lister")
        else:
            print("⚠️  User config manager not available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_image_processing():
    """Test image processing capabilities"""
    print("\n🧪 Testing Image Processing")
    print("=" * 30)
    
    # Check if images directory exists
    images_dir = Path("images")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg"))
        print(f"✅ Found {len(image_files)} image files")
        
        if image_files:
            print(f"   Sample images: {[f.name for f in image_files[:3]]}")
        return True
    else:
        print("⚠️  Images directory not found")
        return False

def main():
    """Run all tests"""
    print("🚀 Multi-AI Provider System Test Suite")
    print("=" * 50)
    
    tests = [
        ("AI Providers", test_ai_providers),
        ("User Interface", test_user_interface),
        ("Integration", test_integration),
        ("Image Processing", test_image_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-AI system is ready.")
        print("\nNext steps:")
        print("1. Run: python ebay_lister.py --setup-ai --user-id your_user_id")
        print("2. Configure your AI provider and API key")
        print("3. Run: python ebay_lister.py --dry-run --user-id your_user_id")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 