"""
Simple test script for KYC Bot API endpoints.

Usage:
    python test_api.py [--url URL] [--customer-name NAME]

Examples:
    python test_api.py
    python test_api.py --url http://localhost:8080
    python test_api.py --customer-name "John Doe"
"""

import requests
import json
import argparse
import sys
from typing import Dict, Any


def test_health(base_url: str) -> bool:
    """Test health endpoint."""
    print("\n[TEST] Health Check")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Failed: Status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_investigation(base_url: str, customer_name: str) -> bool:
    """Test investigation endpoint."""
    print("\n[TEST] Investigation Endpoint")
    print("-" * 60)
    print(f"Customer: {customer_name}")
    
    try:
        payload = {"customer_name": customer_name}
        response = requests.post(
            f"{base_url}/api/v1/investigate",
            json=payload,
            timeout=300  # 5 minutes for investigation
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Investigation completed")
            print(f"   Risk Level: {data.get('risk_level', 'UNKNOWN')}")
            print(f"   Search Results: {len(data.get('search_results', []))} items")
            watchlist_matches = len(data.get('watchlist_results', {}).get('matches', []))
            print(f"   Watchlist Matches: {watchlist_matches}")
            
            if data.get('error'):
                print(f"   ⚠️  Warning: {data['error']}")
            
            # Show report preview
            report = data.get('final_report', '')
            if report:
                preview = report[:200] + "..." if len(report) > 200 else report
                print(f"\n   Report Preview:\n   {preview.replace(chr(10), chr(10) + '   ')}")
            
            return True
        else:
            print(f"❌ Failed: Status code {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out (investigation took too long)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_metrics(base_url: str) -> bool:
    """Test metrics endpoint."""
    print("\n[TEST] Metrics Endpoint")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/api/v1/metrics", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Metrics retrieved")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Failed: Status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run API tests."""
    parser = argparse.ArgumentParser(description="Test KYC Bot API endpoints")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8080",
        help="Base URL of the API (default: http://localhost:8080)"
    )
    parser.add_argument(
        "--customer-name",
        type=str,
        default="John Doe",
        help="Customer name for investigation test (default: John Doe)"
    )
    parser.add_argument(
        "--skip-investigation",
        action="store_true",
        help="Skip investigation test (faster)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("KYC Bot API Test Suite")
    print("=" * 60)
    print(f"Base URL: {args.url}")
    
    results = []
    
    # Test health
    results.append(("Health Check", test_health(args.url)))
    
    # Test metrics
    results.append(("Metrics", test_metrics(args.url)))
    
    # Test investigation (optional, takes longer)
    if not args.skip_investigation:
        results.append(("Investigation", test_investigation(args.url, args.customer_name)))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

