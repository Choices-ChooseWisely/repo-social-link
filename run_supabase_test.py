#!/usr/bin/env python3
"""
Simple Supabase Test Runner
Runs the comprehensive Supabase test suite with user-friendly output
"""

import os
import sys
import json
from datetime import datetime

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file:")
        print("SUPABASE_URL=https://your-project-id.supabase.co")
        print("SUPABASE_ANON_KEY=your-anon-key-here")
        print("\nSee SUPABASE_SETUP.md for detailed instructions.")
        return False
    
    print("✅ Environment variables configured")
    return True

def run_tests():
    """Run the Supabase test suite"""
    try:
        from test_supabase import SupabaseTestSuite
        
        print("🧪 Running Comprehensive Supabase Database Test Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run tests
        test_suite = SupabaseTestSuite()
        results = test_suite.run_all_tests()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"supabase_test_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Test results saved to: {filename}")
        
        # Return results
        return results
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements_api.txt")
        return None
    except Exception as e:
        print(f"❌ Test execution error: {e}")
        return None

def display_results(results):
    """Display test results in a user-friendly format"""
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    # Overall status
    status = results.get("overall_status", "UNKNOWN")
    status_emoji = "✅" if status == "PASSED" else "❌" if status == "FAILED" else "⚠️"
    print(f"{status_emoji} Overall Status: {status}")
    
    # Test breakdown
    tests = results.get("tests", {})
    if tests:
        print(f"\n📋 Test Breakdown:")
        for test_name, status in tests.items():
            emoji = "✅" if status == "PASS" else "❌" if status == "FAILED" else "⚠️" if status == "WARNING" else "❓"
            print(f"   {emoji} {test_name.replace('_', ' ').title()}: {status}")
    
    # Summary
    summary = results.get("summary", {})
    if summary:
        print(f"\n📈 Summary:")
        print(f"   Total Tests: {summary.get('total_tests', 0)}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Success Rate: {summary.get('success_rate', '0%')}")
    
    # Errors
    errors = results.get("errors", [])
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for error in errors:
            print(f"   • {error}")
    
    # Warnings
    warnings = results.get("warnings", [])
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"   • {warning}")
    
    # Performance
    performance = results.get("performance", {})
    if performance:
        print(f"\n⚡ Performance:")
        for metric, value in performance.items():
            print(f"   {metric.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 60)

def main():
    """Main function"""
    print("🗄️  Supabase Database Test Runner")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run tests
    results = run_tests()
    
    if results is None:
        print("❌ Test execution failed")
        sys.exit(1)
    
    # Display results
    display_results(results)
    
    # Exit with appropriate code
    status = results.get("overall_status", "UNKNOWN")
    if status == "PASSED":
        print("🎉 All tests passed! Supabase database is fully functional.")
        sys.exit(0)
    elif status == "WARNING":
        print("⚠️  Tests completed with warnings. Check results for details.")
        sys.exit(1)
    else:
        print("❌ Tests failed. Check results for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 