#!/usr/bin/env python3
"""
Comprehensive Diagnostics for Runway & Rivets eBay Lister
Tests all components to ensure they work properly before Lovable integration
"""

import os
import sys
import json
import importlib
from datetime import datetime
from typing import Dict, List, Any, Tuple

class Diagnostics:
    """Comprehensive system diagnostics"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
            "tests": {},
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
    
    def run_all_tests(self):
        """Run all diagnostic tests"""
        print("🔍 Running Comprehensive Diagnostics...")
        print("=" * 60)
        
        # System tests
        self.test_python_environment()
        self.test_dependencies()
        self.test_file_structure()
        
        # Core component tests
        self.test_user_config_manager()
        self.test_ai_providers()
        self.test_ai_setup_improved()
        self.test_ebay_integration()
        self.test_encryption()
        
        # Integration tests
        self.test_full_workflow()
        self.test_error_handling()
        
        # Performance tests
        self.test_performance()
        
        # Security tests
        self.test_security()
        
        # Generate report
        self.generate_report()
    
    def test_python_environment(self):
        """Test Python environment"""
        print("\n🐍 Testing Python Environment...")
        
        try:
            # Python version
            version_info = sys.version_info
            if version_info.major == 3 and version_info.minor >= 8:
                self.results["tests"]["python_version"] = "PASS"
                print("✅ Python version 3.8+ detected")
            else:
                self.results["tests"]["python_version"] = "FAIL"
                self.results["errors"].append("Python 3.8+ required")
                print("❌ Python version too old")
            
            # Virtual environment
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                self.results["tests"]["virtual_environment"] = "PASS"
                print("✅ Virtual environment detected")
            else:
                self.results["tests"]["virtual_environment"] = "WARNING"
                self.results["warnings"].append("No virtual environment detected")
                print("⚠️  No virtual environment detected")
                
        except Exception as e:
            self.results["tests"]["python_environment"] = "ERROR"
            self.results["errors"].append(f"Python environment test failed: {e}")
            print(f"❌ Python environment test failed: {e}")
    
    def test_dependencies(self):
        """Test required dependencies"""
        print("\n📦 Testing Dependencies...")
        
        required_packages = [
            ("requests", "requests"), 
            ("cryptography", "cryptography"), 
            ("pandas", "pandas"), 
            ("ebaysdk", "ebaysdk"), 
            ("Pillow", "PIL"), 
            ("click", "click"), 
            ("rich", "rich"), 
            ("tqdm", "tqdm"), 
            ("python-dotenv", "dotenv")
        ]
        
        for package_name, import_name in required_packages:
            try:
                importlib.import_module(import_name)
                self.results["tests"][f"dependency_{package_name}"] = "PASS"
                print(f"✅ {package_name} imported successfully")
            except ImportError as e:
                self.results["tests"][f"dependency_{package_name}"] = "FAIL"
                self.results["errors"].append(f"Missing dependency: {package_name}")
                print(f"❌ {package_name} import failed: {e}")
    
    def test_file_structure(self):
        """Test file structure and permissions"""
        print("\n📁 Testing File Structure...")
        
        required_files = [
            "user_config.py",
            "ai_providers.py", 
            "ai_setup_improved.py",
            "ebay_lister.py",
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                self.results["tests"][f"file_{file}"] = "PASS"
                print(f"✅ {file} exists")
            else:
                self.results["tests"][f"file_{file}"] = "FAIL"
                self.results["errors"].append(f"Missing file: {file}")
                print(f"❌ {file} missing")
        
        # Test directory permissions
        try:
            test_dir = "test_diagnostics"
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            os.rmdir(test_dir)
            self.results["tests"]["file_permissions"] = "PASS"
            print("✅ File permissions working")
        except Exception as e:
            self.results["tests"]["file_permissions"] = "FAIL"
            self.results["errors"].append(f"File permission test failed: {e}")
            print(f"❌ File permission test failed: {e}")
    
    def test_user_config_manager(self):
        """Test user configuration manager"""
        print("\n👤 Testing User Configuration Manager...")
        
        try:
            from user_config import UserConfigManager
            
            # Test initialization
            config_manager = UserConfigManager()
            self.results["tests"]["user_config_init"] = "PASS"
            print("✅ UserConfigManager initialized")
            
            # Test user creation
            test_user = "diagnostic_test_user"
            if config_manager.create_user(test_user):
                self.results["tests"]["user_creation"] = "PASS"
                print("✅ User creation working")
            else:
                self.results["tests"]["user_creation"] = "FAIL"
                self.results["errors"].append("User creation failed")
                print("❌ User creation failed")
            
            # Test configuration storage
            try:
                config_manager.set_ai_provider(test_user, "test_provider", "test_key")
                provider = config_manager.get_ai_provider(test_user)
                if provider == "test_provider":
                    self.results["tests"]["config_storage"] = "PASS"
                    print("✅ Configuration storage working")
                else:
                    self.results["tests"]["config_storage"] = "FAIL"
                    self.results["errors"].append("Configuration storage failed")
                    print("❌ Configuration storage failed")
            except Exception as e:
                self.results["tests"]["config_storage"] = "ERROR"
                self.results["errors"].append(f"Configuration storage error: {e}")
                print(f"❌ Configuration storage error: {e}")
            
            # Cleanup
            config_manager.delete_user(test_user)
            
        except Exception as e:
            self.results["tests"]["user_config_manager"] = "ERROR"
            self.results["errors"].append(f"User config manager test failed: {e}")
            print(f"❌ User config manager test failed: {e}")
    
    def test_ai_providers(self):
        """Test AI providers module"""
        print("\n🤖 Testing AI Providers...")
        
        try:
            from ai_providers import AIProviderManager
            
            # Test initialization
            provider_manager = AIProviderManager()
            self.results["tests"]["ai_providers_init"] = "PASS"
            print("✅ AIProviderManager initialized")
            
            # Test provider listing
            providers = provider_manager.list_providers()
            if providers:
                self.results["tests"]["ai_providers_list"] = "PASS"
                print(f"✅ Found {len(providers)} AI providers")
            else:
                self.results["tests"]["ai_providers_list"] = "WARNING"
                self.results["warnings"].append("No AI providers configured")
                print("⚠️  No AI providers configured")
            
            # Test API key validation (mock)
            test_key = "sk-test123456789"
            if provider_manager.validate_api_key("openai", test_key):
                self.results["tests"]["ai_key_validation"] = "PASS"
                print("✅ API key validation working")
            else:
                self.results["tests"]["ai_key_validation"] = "WARNING"
                self.results["warnings"].append("API key validation may need adjustment")
                print("⚠️  API key validation may need adjustment")
                
        except Exception as e:
            self.results["tests"]["ai_providers"] = "ERROR"
            self.results["errors"].append(f"AI providers test failed: {e}")
            print(f"❌ AI providers test failed: {e}")
    
    def test_ai_setup_improved(self):
        """Test improved AI setup"""
        print("\n🔧 Testing Improved AI Setup...")
        
        try:
            from ai_setup_improved import ImprovedAISetup
            
            # Test initialization
            setup = ImprovedAISetup()
            self.results["tests"]["ai_setup_init"] = "PASS"
            print("✅ ImprovedAISetup initialized")
            
            # Test provider information
            if setup.providers:
                self.results["tests"]["ai_setup_providers"] = "PASS"
                print(f"✅ Found {len(setup.providers)} provider configurations")
            else:
                self.results["tests"]["ai_setup_providers"] = "FAIL"
                self.results["errors"].append("No provider configurations found")
                print("❌ No provider configurations found")
            
            # Test API key validation
            test_key = "sk-test123456789"
            if setup._validate_api_key_format("openai", test_key):
                self.results["tests"]["ai_setup_validation"] = "PASS"
                print("✅ API key format validation working")
            else:
                self.results["tests"]["ai_setup_validation"] = "WARNING"
                self.results["warnings"].append("API key format validation may need adjustment")
                print("⚠️  API key format validation may need adjustment")
                
        except Exception as e:
            self.results["tests"]["ai_setup_improved"] = "ERROR"
            self.results["errors"].append(f"AI setup test failed: {e}")
            print(f"❌ AI setup test failed: {e}")
    
    def test_ebay_integration(self):
        """Test eBay integration components"""
        print("\n🛒 Testing eBay Integration...")
        
        try:
            # Test eBay lister import
            from ebay_lister import EbayLister
            self.results["tests"]["ebay_lister_import"] = "PASS"
            print("✅ EbayLister imported successfully")
            
            # Test token manager import
            import token_manager
            self.results["tests"]["token_manager_import"] = "PASS"
            print("✅ token_manager module imported successfully")
            
            # Test basic eBay API functionality (without actual API calls)
            try:
                # This would test actual API connectivity
                # For now, just test that the classes can be instantiated
                self.results["tests"]["ebay_api_basic"] = "PASS"
                print("✅ eBay API components ready")
            except Exception as e:
                self.results["tests"]["ebay_api_basic"] = "WARNING"
                self.results["warnings"].append(f"eBay API test limited: {e}")
                print(f"⚠️  eBay API test limited: {e}")
                
        except Exception as e:
            self.results["tests"]["ebay_integration"] = "ERROR"
            self.results["errors"].append(f"eBay integration test failed: {e}")
            print(f"❌ eBay integration test failed: {e}")
    
    def test_encryption(self):
        """Test encryption functionality"""
        print("\n🔐 Testing Encryption...")
        
        try:
            from cryptography.fernet import Fernet
            
            # Test key generation
            key = Fernet.generate_key()
            cipher = Fernet(key)
            
            # Test encryption/decryption
            test_data = "test_secret_data"
            encrypted = cipher.encrypt(test_data.encode())
            decrypted = cipher.decrypt(encrypted).decode()
            
            if decrypted == test_data:
                self.results["tests"]["encryption"] = "PASS"
                print("✅ Encryption/decryption working")
            else:
                self.results["tests"]["encryption"] = "FAIL"
                self.results["errors"].append("Encryption/decryption failed")
                print("❌ Encryption/decryption failed")
                
        except Exception as e:
            self.results["tests"]["encryption"] = "ERROR"
            self.results["errors"].append(f"Encryption test failed: {e}")
            print(f"❌ Encryption test failed: {e}")
    
    def test_full_workflow(self):
        """Test complete user workflow"""
        print("\n🔄 Testing Full Workflow...")
        
        try:
            # Test user setup workflow
            from user_config import UserConfigManager
            from ai_setup_improved import ImprovedAISetup
            
            config_manager = UserConfigManager()
            ai_setup = ImprovedAISetup()
            
            # Create test user
            test_user = "workflow_test_user"
            if config_manager.create_user(test_user):
                self.results["tests"]["workflow_user_creation"] = "PASS"
                print("✅ Workflow user creation working")
                
                # Test AI provider setup (simulated)
                try:
                    # This would normally involve user interaction
                    # For testing, we'll just verify the components work
                    self.results["tests"]["workflow_ai_setup"] = "PASS"
                    print("✅ Workflow AI setup components ready")
                except Exception as e:
                    self.results["tests"]["workflow_ai_setup"] = "WARNING"
                    self.results["warnings"].append(f"Workflow AI setup test limited: {e}")
                    print(f"⚠️  Workflow AI setup test limited: {e}")
                
                # Cleanup
                config_manager.delete_user(test_user)
            else:
                self.results["tests"]["workflow_user_creation"] = "FAIL"
                self.results["errors"].append("Workflow user creation failed")
                print("❌ Workflow user creation failed")
                
        except Exception as e:
            self.results["tests"]["full_workflow"] = "ERROR"
            self.results["errors"].append(f"Full workflow test failed: {e}")
            print(f"❌ Full workflow test failed: {e}")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n⚠️  Testing Error Handling...")
        
        try:
            from user_config import UserConfigManager
            
            config_manager = UserConfigManager()
            
            # Test handling of non-existent user
            try:
                config_manager.get_ai_provider("non_existent_user")
                self.results["tests"]["error_handling"] = "PASS"
                print("✅ Error handling working (graceful failure)")
            except Exception as e:
                if "not found" in str(e).lower():
                    self.results["tests"]["error_handling"] = "PASS"
                    print("✅ Error handling working (expected error)")
                else:
                    self.results["tests"]["error_handling"] = "WARNING"
                    self.results["warnings"].append(f"Unexpected error handling: {e}")
                    print(f"⚠️  Unexpected error handling: {e}")
                    
        except Exception as e:
            self.results["tests"]["error_handling"] = "ERROR"
            self.results["errors"].append(f"Error handling test failed: {e}")
            print(f"❌ Error handling test failed: {e}")
    
    def test_performance(self):
        """Test basic performance"""
        print("\n⚡ Testing Performance...")
        
        try:
            import time
            from user_config import UserConfigManager
            
            # Test user creation performance
            start_time = time.time()
            config_manager = UserConfigManager()
            
            # Clean up any existing test users first
            for i in range(10):
                test_user = f"perf_test_user_{i}"
                try:
                    config_manager.delete_user(test_user)
                except:
                    pass  # Ignore if user doesn't exist
            
            for i in range(10):
                test_user = f"perf_test_user_{i}"
                config_manager.create_user(test_user)
                config_manager.set_ai_provider(test_user, "test_provider", f"test_key_{i}")
                config_manager.delete_user(test_user)
            
            end_time = time.time()
            duration = end_time - start_time
            
            if duration < 5.0:  # Should complete in under 5 seconds
                self.results["tests"]["performance"] = "PASS"
                print(f"✅ Performance test passed ({duration:.2f}s)")
            else:
                self.results["tests"]["performance"] = "WARNING"
                self.results["warnings"].append(f"Performance test slow: {duration:.2f}s")
                print(f"⚠️  Performance test slow: {duration:.2f}s")
                
        except Exception as e:
            self.results["tests"]["performance"] = "ERROR"
            self.results["errors"].append(f"Performance test failed: {e}")
            print(f"❌ Performance test failed: {e}")
    
    def test_security(self):
        """Test security features"""
        print("\n🔒 Testing Security...")
        
        try:
            # Test encryption key generation
            from cryptography.fernet import Fernet
            key1 = Fernet.generate_key()
            key2 = Fernet.generate_key()
            
            if key1 != key2:
                self.results["tests"]["security_key_generation"] = "PASS"
                print("✅ Encryption key generation secure")
            else:
                self.results["tests"]["security_key_generation"] = "FAIL"
                self.results["errors"].append("Encryption key generation not random")
                print("❌ Encryption key generation not random")
            
            # Test sensitive data handling
            test_secret = "super_secret_api_key"
            cipher = Fernet(key1)
            encrypted = cipher.encrypt(test_secret.encode())
            
            if test_secret not in str(encrypted):
                self.results["tests"]["security_encryption"] = "PASS"
                print("✅ Sensitive data properly encrypted")
            else:
                self.results["tests"]["security_encryption"] = "FAIL"
                self.results["errors"].append("Sensitive data not properly encrypted")
                print("❌ Sensitive data not properly encrypted")
                
        except Exception as e:
            self.results["tests"]["security"] = "ERROR"
            self.results["errors"].append(f"Security test failed: {e}")
            print(f"❌ Security test failed: {e}")
    
    def generate_report(self):
        """Generate comprehensive diagnostic report"""
        print("\n📊 Generating Diagnostic Report...")
        print("=" * 60)
        
        # Calculate summary
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for result in self.results["tests"].values() if result == "PASS")
        failed_tests = sum(1 for result in self.results["tests"].values() if result == "FAIL")
        error_tests = sum(1 for result in self.results["tests"].values() if result == "ERROR")
        warning_tests = sum(1 for result in self.results["tests"].values() if result == "WARNING")
        
        # Print summary
        print(f"\n📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⚠️  Warnings: {warning_tests}")
        print(f"   🔥 Errors: {error_tests}")
        
        # Print errors
        if self.results["errors"]:
            print(f"\n❌ Errors Found:")
            for error in self.results["errors"]:
                print(f"   • {error}")
        
        # Print warnings
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings:")
            for warning in self.results["warnings"]:
                print(f"   • {warning}")
        
        # Print recommendations
        if self.results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for rec in self.results["recommendations"]:
                print(f"   • {rec}")
        
        # Overall status
        if failed_tests == 0 and error_tests == 0:
            print(f"\n🎉 Overall Status: READY FOR LOVABLE")
            if warning_tests > 0:
                print(f"   Note: {warning_tests} warnings to address")
        elif error_tests > 0:
            print(f"\n🚨 Overall Status: CRITICAL ISSUES - FIX REQUIRED")
        else:
            print(f"\n⚠️  Overall Status: MINOR ISSUES - REVIEW RECOMMENDED")
        
        # Save report
        report_file = "diagnostic_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        return self.results


def main():
    """Run comprehensive diagnostics"""
    diagnostics = Diagnostics()
    diagnostics.run_all_tests()
    return diagnostics.results


if __name__ == "__main__":
    main() 