#!/usr/bin/env python3
"""
Setup script for Runway & Rivets eBay Lister
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created successfully")
            print("⚠️  Please edit .env file with your eBay API credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Runway & Rivets eBay Lister...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed during .env file creation")
        sys.exit(1)
    
    # Check if CSV file exists
    csv_files = list(Path(".").glob("*.csv"))
    if csv_files:
        print(f"✅ Found CSV file(s): {', '.join(f.name for f in csv_files)}")
    else:
        print("⚠️  No CSV files found in current directory")
    
    # Check if images directory exists
    if Path("images").exists():
        print("✅ Images directory found")
    else:
        print("⚠️  Images directory not found")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your eBay API credentials")
    print("2. Run: python token_manager.py setup")
    print("3. Run: python ebay_lister.py --dry-run")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 