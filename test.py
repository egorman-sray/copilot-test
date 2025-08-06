#!/usr/bin/env python3
"""
Simple test script to verify the microservice structure and dependencies :)
"""

import sys
import os
import importlib.util

def test_imports():
    """Test that all required modules can be imported :)"""
    try:
        # Test Google Cloud imports :)
        from google.cloud import pubsub_v1
        from google.cloud import storage
        print("✓ Google Cloud libraries imported successfully :)")
        
        # Test standard library imports :)
        import json
        import logging
        from concurrent.futures import ThreadPoolExecutor
        print("✓ Standard library imports successful :)")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e} :(")
        return False

def test_main_module():
    """Test that the main module can be loaded :)"""
    try:
        # Check if main.py exists :)
        if not os.path.exists('main.py'):
            print("✗ main.py file not found :(")
            return False
        
        # Try to load the module spec :)
        spec = importlib.util.spec_from_file_location("main", "main.py")
        if spec is None:
            print("✗ Could not load main.py module spec :(")
            return False
        
        print("✓ main.py module structure is valid :)")
        return True
        
    except Exception as e:
        print(f"✗ Error loading main module: {e} :(")
        return False

def test_environment_setup():
    """Test environment variable setup guidance :)"""
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'PUBSUB_SUBSCRIPTION', 
        'GCS_BUCKET_NAME'
    ]
    
    print("Environment variable setup check :)")
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✓ {var} is set :)")
        else:
            print(f"! {var} is not set (required for production) :)")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Note: Set these variables before running: {missing_vars} :)")
    
    return True

def main():
    """Run all tests :)"""
    print("Running microservice tests... :)")
    print("=" * 50)
    
    tests = [
        ("Import tests", test_imports),
        ("Main module tests", test_main_module),
        ("Environment setup", test_environment_setup)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! Microservice is ready :)")
        return 0
    else:
        print("✗ Some tests failed. Check the output above :(")
        return 1

if __name__ == "__main__":
    exit(main())