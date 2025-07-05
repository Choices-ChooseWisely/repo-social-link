#!/usr/bin/env python3
"""
Test script for Runway & Rivets eBay Lister setup
"""

import os
import json
import sys
from pathlib import Path

def test_file_structure():
    """Test that all required files exist."""
    print("🔍 Testing file structure...")
    
    required_files = [
        "requirements.txt",
        "env_example.txt", 
        "ebay_lister.py",
        "token_manager.py",
        "setup.py",
        "ebay_categories.json",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_csv_file():
    """Test that CSV file exists and is readable."""
    print("\n🔍 Testing CSV file...")
    
    csv_files = list(Path(".").glob("*.csv"))
    if csv_files:
        print(f"✅ Found CSV file: {csv_files[0].name}")
        
        # Try to read first few lines
        try:
            with open(csv_files[0], 'r') as f:
                lines = f.readlines()[:5]
                print(f"✅ CSV file is readable ({len(lines)} lines tested)")
                return True
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return False
    else:
        print("⚠️  No CSV files found")
        return False

def test_config_file():
    """Test that configuration file is valid JSON."""
    print("\n🔍 Testing configuration file...")
    
    try:
        with open("ebay_categories.json", 'r') as f:
            config = json.load(f)
        
        required_keys = ["category_mappings", "condition_mappings", "defaults", "policies"]
        for key in required_keys:
            if key in config:
                print(f"✅ {key}")
            else:
                print(f"❌ Missing {key}")
                return False
        
        print(f"✅ Configuration file is valid JSON with {len(config['category_mappings'])} category mappings")
        return True
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def test_env_template():
    """Test that environment template exists."""
    print("\n🔍 Testing environment template...")
    
    try:
        with open("env_example.txt", 'r') as f:
            content = f.read()
        
        required_vars = [
            "EBAY_CLIENT_ID",
            "EBAY_CLIENT_SECRET", 
            "EBAY_REDIRECT_URI",
            "EBAY_REFRESH_TOKEN"
        ]
        
        for var in required_vars:
            if var in content:
                print(f"✅ {var}")
            else:
                print(f"❌ Missing {var}")
                return False
        
        print("✅ Environment template contains all required variables")
        return True
        
    except Exception as e:
        print(f"❌ Error reading environment template: {e}")
        return False

def test_images_directory():
    """Test that images directory exists and contains files."""
    print("\n🔍 Testing images directory...")
    
    images_dir = Path("images")
    if images_dir.exists():
        image_files = list(images_dir.glob("*.jpeg")) + list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png"))
        print(f"✅ Images directory found with {len(image_files)} image files")
        return True
    else:
        print("⚠️  Images directory not found")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Runway & Rivets eBay Lister Setup")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("CSV File", test_csv_file),
        ("Configuration", test_config_file),
        ("Environment Template", test_env_template),
        ("Images Directory", test_images_directory)
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
        print("🎉 All tests passed! Setup looks good.")
        print("\nNext steps:")
        print("1. Run: python setup.py")
        print("2. Edit .env file with your eBay credentials")
        print("3. Run: python token_manager.py setup")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 