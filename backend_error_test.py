#!/usr/bin/env python3
"""
Tradalife Backend API Error Handling Tests
Tests error scenarios and edge cases
"""

import requests
import json
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    return "https://auto-trader-70.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class ErrorTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_invalid_login(self):
        """Test login with invalid credentials"""
        try:
            credentials = {
                "email": "invalid@test.com",
                "password": "wrongpassword"
            }
            
            response = self.session.post(f"{API_URL}/auth/login", json=credentials)
            
            if response.status_code == 401:
                self.log_test("Invalid Login Credentials", True, "Correctly returned 401 for invalid credentials")
                return True
            else:
                self.log_test("Invalid Login Credentials", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Login Credentials", False, f"Error: {str(e)}")
            return False
    
    def test_unauthorized_access(self):
        """Test accessing protected endpoint without token"""
        try:
            response = self.session.get(f"{API_URL}/auth/me")
            
            if response.status_code == 403:
                self.log_test("Unauthorized Access", True, "Correctly returned 403 for missing token")
                return True
            else:
                self.log_test("Unauthorized Access", False, f"Expected 403, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Unauthorized Access", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_formation_id(self):
        """Test getting non-existent formation"""
        try:
            response = self.session.get(f"{API_URL}/formations/999")
            
            if response.status_code == 404:
                self.log_test("Invalid Formation ID", True, "Correctly returned 404 for non-existent formation")
                return True
            else:
                self.log_test("Invalid Formation ID", False, f"Expected 404, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Formation ID", False, f"Error: {str(e)}")
            return False
    
    def test_duplicate_registration(self):
        """Test registering with existing email"""
        try:
            user_data = {
                "email": "test@tradalife.com",  # This should already exist from previous tests
                "password": "Test123!"
            }
            
            response = self.session.post(f"{API_URL}/auth/register", json=user_data)
            
            if response.status_code == 400:
                self.log_test("Duplicate Registration", True, "Correctly returned 400 for existing email")
                return True
            else:
                self.log_test("Duplicate Registration", False, f"Expected 400, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Duplicate Registration", False, f"Error: {str(e)}")
            return False
    
    def run_error_tests(self):
        """Run all error handling tests"""
        print(f"🔍 Starting Tradalife Backend Error Handling Tests")
        print(f"📍 API URL: {API_URL}")
        print("=" * 60)
        
        tests = [
            self.test_invalid_login,
            self.test_unauthorized_access,
            self.test_invalid_formation_id,
            self.test_duplicate_registration
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Error Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All error handling tests passed!")
            return True
        else:
            print(f"⚠️  {total - passed} error tests failed.")
            return False

def main():
    """Main test runner"""
    tester = ErrorTester()
    success = tester.run_error_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()