#!/usr/bin/env python3
"""
Comprehensive Supabase Database Test Suite
Tests all database operations and ensures functionality
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_manager import (
    SupabaseManager, User, Listing, AIUsage, 
    ListingStatus, create_supabase_manager, test_supabase_connection
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SupabaseTestSuite:
    """Comprehensive test suite for Supabase database operations"""
    
    def __init__(self):
        self.results = {
            "overall_status": "PENDING",
            "tests": {},
            "errors": [],
            "warnings": [],
            "performance": {},
            "summary": {}
        }
        self.manager = None
        self.test_user_id = f"test_user_{int(time.time())}"
        self.test_listing_id = None
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🧪 Starting Comprehensive Supabase Database Test Suite")
        print("=" * 60)
        
        try:
            # Initialize manager
            self._test_initialization()
            
            if not self.manager:
                self.results["overall_status"] = "FAILED"
                self.results["errors"].append("Failed to initialize Supabase manager")
                return self.results
            
            # Run all test categories
            self._test_connection()
            self._test_user_operations()
            self._test_listing_operations()
            self._test_ai_usage_operations()
            self._test_search_and_queries()
            self._test_performance()
            self._test_error_handling()
            self._test_data_integrity()
            
            # Cleanup
            self._cleanup_test_data()
            
            # Generate summary
            self._generate_summary()
            
        except Exception as e:
            logger.error(f"❌ Test suite failed: {e}")
            self.results["overall_status"] = "FAILED"
            self.results["errors"].append(f"Test suite error: {e}")
        
        return self.results
    
    def _test_initialization(self):
        """Test Supabase manager initialization"""
        print("\n🔧 Testing Initialization...")
        
        try:
            # Test environment variables
            required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if missing_vars:
                self.results["tests"]["initialization"] = "FAILED"
                self.results["errors"].append(f"Missing environment variables: {missing_vars}")
                print(f"❌ Missing environment variables: {missing_vars}")
                return
            
            # Test manager creation
            self.manager = create_supabase_manager()
            if self.manager:
                self.results["tests"]["initialization"] = "PASS"
                print("✅ Supabase manager initialized successfully")
            else:
                self.results["tests"]["initialization"] = "FAILED"
                self.results["errors"].append("Failed to create Supabase manager")
                print("❌ Failed to create Supabase manager")
                
        except Exception as e:
            self.results["tests"]["initialization"] = "ERROR"
            self.results["errors"].append(f"Initialization error: {e}")
            print(f"❌ Initialization error: {e}")
    
    def _test_connection(self):
        """Test database connection and basic operations"""
        print("\n🔌 Testing Database Connection...")
        
        try:
            # Test connection
            connection_results = self.manager.test_connection()
            
            if connection_results["connection"]:
                self.results["tests"]["connection"] = "PASS"
                print("✅ Database connection successful")
            else:
                self.results["tests"]["connection"] = "FAILED"
                self.results["errors"].append("Database connection failed")
                print("❌ Database connection failed")
                return
            
            # Test table access
            tables_status = connection_results.get("tables", {})
            for table, status in tables_status.items():
                if status == "accessible":
                    print(f"✅ Table '{table}' accessible")
                else:
                    print(f"⚠️  Table '{table}': {status}")
                    self.results["warnings"].append(f"Table {table}: {status}")
            
            # Test CRUD operations
            operations = connection_results.get("operations", {})
            for operation, status in operations.items():
                if status == "success":
                    print(f"✅ {operation.capitalize()} operation successful")
                else:
                    print(f"❌ {operation.capitalize()} operation failed")
                    self.results["errors"].append(f"{operation} operation failed")
            
            self.results["tests"]["basic_operations"] = "PASS" if all(
                status == "success" for status in operations.values()
            ) else "FAILED"
            
        except Exception as e:
            self.results["tests"]["connection"] = "ERROR"
            self.results["errors"].append(f"Connection test error: {e}")
            print(f"❌ Connection test error: {e}")
    
    def _test_user_operations(self):
        """Test user CRUD operations"""
        print("\n👤 Testing User Operations...")
        
        try:
            # Test CREATE
            test_user = User(
                id=self.test_user_id,
                email="test@example.com",
                name="Test User",
                ai_provider="openai",
                preferences={"auto_enhance": True, "draft_mode": True}
            )
            
            if self.manager.create_user(test_user):
                self.results["tests"]["user_create"] = "PASS"
                print("✅ User creation successful")
            else:
                self.results["tests"]["user_create"] = "FAILED"
                self.results["errors"].append("User creation failed")
                print("❌ User creation failed")
                return
            
            # Test READ
            retrieved_user = self.manager.get_user(self.test_user_id)
            if retrieved_user and retrieved_user.id == self.test_user_id:
                self.results["tests"]["user_read"] = "PASS"
                print("✅ User retrieval successful")
            else:
                self.results["tests"]["user_read"] = "FAILED"
                self.results["errors"].append("User retrieval failed")
                print("❌ User retrieval failed")
            
            # Test UPDATE
            test_user.name = "Updated Test User"
            test_user.preferences["draft_mode"] = False
            
            if self.manager.update_user(test_user):
                updated_user = self.manager.get_user(self.test_user_id)
                if updated_user and updated_user.name == "Updated Test User":
                    self.results["tests"]["user_update"] = "PASS"
                    print("✅ User update successful")
                else:
                    self.results["tests"]["user_update"] = "FAILED"
                    self.results["errors"].append("User update failed")
                    print("❌ User update failed")
            else:
                self.results["tests"]["user_update"] = "FAILED"
                self.results["errors"].append("User update operation failed")
                print("❌ User update operation failed")
            
            # Test LIST
            users = self.manager.list_users()
            if any(user.id == self.test_user_id for user in users):
                self.results["tests"]["user_list"] = "PASS"
                print("✅ User listing successful")
            else:
                self.results["tests"]["user_list"] = "FAILED"
                self.results["errors"].append("User listing failed")
                print("❌ User listing failed")
                
        except Exception as e:
            self.results["tests"]["user_operations"] = "ERROR"
            self.results["errors"].append(f"User operations error: {e}")
            print(f"❌ User operations error: {e}")
    
    def _test_listing_operations(self):
        """Test listing CRUD operations"""
        print("\n📝 Testing Listing Operations...")
        
        try:
            # Test CREATE
            test_listing = Listing(
                user_id=self.test_user_id,
                title="Test Vintage Jacket",
                description="A beautiful vintage leather jacket from the 1980s",
                category="Clothing, Shoes & Accessories > Men's Clothing > Jackets & Coats",
                condition="Used - Excellent",
                estimated_price="$150-250",
                brand="Unknown",
                item_type="Leather Jacket",
                material="Leather",
                color="Black",
                country_of_manufacture="Unknown",
                image_urls=["/api/images/test1.jpg", "/api/images/test2.jpg"],
                user_message="Vintage leather jacket from the 80s",
                ai_provider="openai",
                ai_generated=True,
                status=ListingStatus.DRAFT.value
            )
            
            self.test_listing_id = self.manager.create_listing(test_listing)
            if self.test_listing_id:
                self.results["tests"]["listing_create"] = "PASS"
                print("✅ Listing creation successful")
            else:
                self.results["tests"]["listing_create"] = "FAILED"
                self.results["errors"].append("Listing creation failed")
                print("❌ Listing creation failed")
                return
            
            # Test READ
            retrieved_listing = self.manager.get_listing(self.test_listing_id)
            if retrieved_listing and retrieved_listing.title == "Test Vintage Jacket":
                self.results["tests"]["listing_read"] = "PASS"
                print("✅ Listing retrieval successful")
            else:
                self.results["tests"]["listing_read"] = "FAILED"
                self.results["errors"].append("Listing retrieval failed")
                print("❌ Listing retrieval failed")
            
            # Test UPDATE
            test_listing.id = self.test_listing_id
            test_listing.title = "Updated Test Vintage Jacket"
            test_listing.status = ListingStatus.ACTIVE.value
            
            if self.manager.update_listing(test_listing):
                updated_listing = self.manager.get_listing(self.test_listing_id)
                if updated_listing and updated_listing.title == "Updated Test Vintage Jacket":
                    self.results["tests"]["listing_update"] = "PASS"
                    print("✅ Listing update successful")
                else:
                    self.results["tests"]["listing_update"] = "FAILED"
                    self.results["errors"].append("Listing update failed")
                    print("❌ Listing update failed")
            else:
                self.results["tests"]["listing_update"] = "FAILED"
                self.results["errors"].append("Listing update operation failed")
                print("❌ Listing update operation failed")
            
            # Test LIST
            listings = self.manager.get_user_listings(self.test_user_id)
            if any(listing.id == self.test_listing_id for listing in listings):
                self.results["tests"]["listing_list"] = "PASS"
                print("✅ Listing listing successful")
            else:
                self.results["tests"]["listing_list"] = "FAILED"
                self.results["errors"].append("Listing listing failed")
                print("❌ Listing listing failed")
                
        except Exception as e:
            self.results["tests"]["listing_operations"] = "ERROR"
            self.results["errors"].append(f"Listing operations error: {e}")
            print(f"❌ Listing operations error: {e}")
    
    def _test_ai_usage_operations(self):
        """Test AI usage tracking operations"""
        print("\n🤖 Testing AI Usage Operations...")
        
        try:
            # Test CREATE
            test_usage = AIUsage(
                user_id=self.test_user_id,
                provider="openai",
                model="gpt-4o",
                tokens_used=1500,
                cost=0.045,
                request_type="listing_generation",
                success=True
            )
            
            if self.manager.log_ai_usage(test_usage):
                self.results["tests"]["ai_usage_create"] = "PASS"
                print("✅ AI usage logging successful")
            else:
                self.results["tests"]["ai_usage_create"] = "FAILED"
                self.results["errors"].append("AI usage logging failed")
                print("❌ AI usage logging failed")
            
            # Test READ
            usage_records = self.manager.get_user_ai_usage(self.test_user_id, 1)
            if usage_records:
                self.results["tests"]["ai_usage_read"] = "PASS"
                print("✅ AI usage retrieval successful")
            else:
                self.results["tests"]["ai_usage_read"] = "FAILED"
                self.results["errors"].append("AI usage retrieval failed")
                print("❌ AI usage retrieval failed")
            
            # Test usage stats
            stats = self.manager.get_usage_stats(self.test_user_id)
            if stats:
                self.results["tests"]["ai_usage_stats"] = "PASS"
                print("✅ AI usage stats successful")
                print(f"   - Total listings: {stats.get('total_listings', 0)}")
                print(f"   - AI requests (30d): {stats.get('ai_requests_30d', 0)}")
                print(f"   - AI cost (30d): ${stats.get('ai_cost_30d', 0):.3f}")
            else:
                self.results["tests"]["ai_usage_stats"] = "FAILED"
                self.results["errors"].append("AI usage stats failed")
                print("❌ AI usage stats failed")
                
        except Exception as e:
            self.results["tests"]["ai_usage_operations"] = "ERROR"
            self.results["errors"].append(f"AI usage operations error: {e}")
            print(f"❌ AI usage operations error: {e}")
    
    def _test_search_and_queries(self):
        """Test search and query operations"""
        print("\n🔍 Testing Search and Queries...")
        
        try:
            # Test listing search
            search_results = self.manager.search_listings(self.test_user_id, "vintage")
            if search_results:
                self.results["tests"]["listing_search"] = "PASS"
                print("✅ Listing search successful")
            else:
                self.results["tests"]["listing_search"] = "FAILED"
                self.results["errors"].append("Listing search failed")
                print("❌ Listing search failed")
            
            # Test empty search
            empty_results = self.manager.search_listings(self.test_user_id, "nonexistent")
            if not empty_results:
                self.results["tests"]["empty_search"] = "PASS"
                print("✅ Empty search handling successful")
            else:
                self.results["tests"]["empty_search"] = "FAILED"
                self.results["errors"].append("Empty search handling failed")
                print("❌ Empty search handling failed")
                
        except Exception as e:
            self.results["tests"]["search_operations"] = "ERROR"
            self.results["errors"].append(f"Search operations error: {e}")
            print(f"❌ Search operations error: {e}")
    
    def _test_performance(self):
        """Test database performance"""
        print("\n⚡ Testing Performance...")
        
        try:
            import time
            
            # Test bulk operations
            start_time = time.time()
            
            # Create multiple test listings
            for i in range(5):
                listing = Listing(
                    user_id=self.test_user_id,
                    title=f"Performance Test Item {i}",
                    description=f"Test description {i}",
                    category="Test Category",
                    condition="Used",
                    estimated_price="$100",
                    image_urls=[f"/api/images/test{i}.jpg"]
                )
                self.manager.create_listing(listing)
            
            # Retrieve all listings
            listings = self.manager.get_user_listings(self.test_user_id)
            
            end_time = time.time()
            duration = end_time - start_time
            
            if duration < 10.0:  # Should complete in under 10 seconds
                self.results["tests"]["performance"] = "PASS"
                self.results["performance"]["bulk_operations"] = f"{duration:.2f}s"
                print(f"✅ Performance test passed ({duration:.2f}s)")
            else:
                self.results["tests"]["performance"] = "WARNING"
                self.results["performance"]["bulk_operations"] = f"{duration:.2f}s"
                self.results["warnings"].append(f"Performance test slow: {duration:.2f}s")
                print(f"⚠️  Performance test slow: {duration:.2f}s")
                
        except Exception as e:
            self.results["tests"]["performance"] = "ERROR"
            self.results["errors"].append(f"Performance test error: {e}")
            print(f"❌ Performance test error: {e}")
    
    def _test_error_handling(self):
        """Test error handling scenarios"""
        print("\n🚨 Testing Error Handling...")
        
        try:
            # Test invalid user ID
            invalid_user = self.manager.get_user("nonexistent_user")
            if invalid_user is None:
                self.results["tests"]["invalid_user_handling"] = "PASS"
                print("✅ Invalid user handling successful")
            else:
                self.results["tests"]["invalid_user_handling"] = "FAILED"
                self.results["errors"].append("Invalid user handling failed")
                print("❌ Invalid user handling failed")
            
            # Test invalid listing ID
            invalid_listing = self.manager.get_listing("nonexistent_listing")
            if invalid_listing is None:
                self.results["tests"]["invalid_listing_handling"] = "PASS"
                print("✅ Invalid listing handling successful")
            else:
                self.results["tests"]["invalid_listing_handling"] = "FAILED"
                self.results["errors"].append("Invalid listing handling failed")
                print("❌ Invalid listing handling failed")
            
            # Test empty user listings
            empty_listings = self.manager.get_user_listings("empty_user")
            if empty_listings == []:
                self.results["tests"]["empty_listings_handling"] = "PASS"
                print("✅ Empty listings handling successful")
            else:
                self.results["tests"]["empty_listings_handling"] = "FAILED"
                self.results["errors"].append("Empty listings handling failed")
                print("❌ Empty listings handling failed")
                
        except Exception as e:
            self.results["tests"]["error_handling"] = "ERROR"
            self.results["errors"].append(f"Error handling test error: {e}")
            print(f"❌ Error handling test error: {e}")
    
    def _test_data_integrity(self):
        """Test data integrity and validation"""
        print("\n🔒 Testing Data Integrity...")
        
        try:
            # Test user data integrity
            user = self.manager.get_user(self.test_user_id)
            if user and user.id == self.test_user_id:
                self.results["tests"]["user_data_integrity"] = "PASS"
                print("✅ User data integrity verified")
            else:
                self.results["tests"]["user_data_integrity"] = "FAILED"
                self.results["errors"].append("User data integrity failed")
                print("❌ User data integrity failed")
            
            # Test listing data integrity
            if self.test_listing_id:
                listing = self.manager.get_listing(self.test_listing_id)
                if listing and listing.user_id == self.test_user_id:
                    self.results["tests"]["listing_data_integrity"] = "PASS"
                    print("✅ Listing data integrity verified")
                else:
                    self.results["tests"]["listing_data_integrity"] = "FAILED"
                    self.results["errors"].append("Listing data integrity failed")
                    print("❌ Listing data integrity failed")
            
            # Test foreign key relationships
            if self.test_listing_id:
                listing = self.manager.get_listing(self.test_listing_id)
                user = self.manager.get_user(listing.user_id)
                if user:
                    self.results["tests"]["foreign_key_integrity"] = "PASS"
                    print("✅ Foreign key relationships verified")
                else:
                    self.results["tests"]["foreign_key_integrity"] = "FAILED"
                    self.results["errors"].append("Foreign key relationships failed")
                    print("❌ Foreign key relationships failed")
                    
        except Exception as e:
            self.results["tests"]["data_integrity"] = "ERROR"
            self.results["errors"].append(f"Data integrity test error: {e}")
            print(f"❌ Data integrity test error: {e}")
    
    def _cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧹 Cleaning Up Test Data...")
        
        try:
            # Delete test listing
            if self.test_listing_id:
                self.manager.delete_listing(self.test_listing_id)
                print("✅ Test listing deleted")
            
            # Delete test user
            self.manager.delete_user(self.test_user_id)
            print("✅ Test user deleted")
            
            self.results["tests"]["cleanup"] = "PASS"
            
        except Exception as e:
            self.results["tests"]["cleanup"] = "WARNING"
            self.results["warnings"].append(f"Cleanup warning: {e}")
            print(f"⚠️  Cleanup warning: {e}")
    
    def _generate_summary(self):
        """Generate test summary"""
        print("\n📊 Generating Test Summary...")
        
        # Count test results
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for status in self.results["tests"].values() if status == "PASS")
        failed_tests = sum(1 for status in self.results["tests"].values() if status == "FAILED")
        error_tests = sum(1 for status in self.results["tests"].values() if status == "ERROR")
        warning_tests = sum(1 for status in self.results["tests"].values() if status == "WARNING")
        
        # Determine overall status
        if failed_tests == 0 and error_tests == 0:
            self.results["overall_status"] = "PASSED"
        elif failed_tests > 0:
            self.results["overall_status"] = "FAILED"
        else:
            self.results["overall_status"] = "WARNING"
        
        # Generate summary
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "warnings": warning_tests,
            "success_rate": f"{(passed_tests / total_tests * 100):.1f}%" if total_tests > 0 else "0%"
        }
        
        # Print summary
        print(f"\n🎯 Test Summary:")
        print(f"   Overall Status: {self.results['overall_status']}")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Errors: {error_tests}")
        print(f"   Warnings: {warning_tests}")
        print(f"   Success Rate: {self.results['summary']['success_rate']}")
        
        if self.results["errors"]:
            print(f"\n❌ Errors:")
            for error in self.results["errors"]:
                print(f"   - {error}")
        
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings:")
            for warning in self.results["warnings"]:
                print(f"   - {warning}")


def main():
    """Run the comprehensive test suite"""
    # Check environment variables
    required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return
    
    # Run tests
    test_suite = SupabaseTestSuite()
    results = test_suite.run_all_tests()
    
    # Save results
    with open("supabase_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Test results saved to: supabase_test_results.json")
    
    # Exit with appropriate code
    if results["overall_status"] == "PASSED":
        print("🎉 All tests passed! Supabase database is fully functional.")
        sys.exit(0)
    elif results["overall_status"] == "WARNING":
        print("⚠️  Tests completed with warnings. Check results for details.")
        sys.exit(1)
    else:
        print("❌ Tests failed. Check results for details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 