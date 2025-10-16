#!/usr/bin/env python3
"""
Tradalife Backend API Test Suite
Tests all backend endpoints with realistic data
"""

import requests
import json
import sys
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    return "https://edushop-portal.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class TradalifeTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_data = None
        self.purchase_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data
        })
    
    def test_health_check(self):
        """Test API health check"""
        try:
            response = self.session.get(f"{API_URL}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    self.log_test("Health Check", True, f"API is running: {data.get('message')}")
                    return True
                else:
                    self.log_test("Health Check", False, "API responded but status not ok", data)
                    return False
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_register(self):
        """Test user registration"""
        try:
            # Use realistic test data
            user_data = {
                "email": "test@tradalife.com",
                "password": "Test123!"
            }
            
            response = self.session.post(f"{API_URL}/auth/register", json=user_data)
            
            if response.status_code == 200:
                data = response.json()
                if "user" in data and "token" in data:
                    self.token = data["token"]
                    self.user_data = data["user"]
                    self.log_test("User Registration", True, f"User registered: {data['user']['email']}")
                    return True
                else:
                    self.log_test("User Registration", False, "Missing user or token in response", data)
                    return False
            elif response.status_code == 400:
                # User might already exist, try to continue with login
                self.log_test("User Registration", True, "User already exists (expected for repeated tests)")
                return True
            else:
                self.log_test("User Registration", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_login(self):
        """Test user login"""
        try:
            credentials = {
                "email": "test@tradalife.com",
                "password": "Test123!"
            }
            
            response = self.session.post(f"{API_URL}/auth/login", json=credentials)
            
            if response.status_code == 200:
                data = response.json()
                if "user" in data and "token" in data:
                    self.token = data["token"]
                    self.user_data = data["user"]
                    self.log_test("User Login", True, f"Login successful: {data['user']['email']}")
                    return True
                else:
                    self.log_test("User Login", False, "Missing user or token in response", data)
                    return False
            else:
                self.log_test("User Login", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_get_me(self):
        """Test get current user endpoint"""
        if not self.token:
            self.log_test("Get Current User", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{API_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "email" in data:
                    self.log_test("Get Current User", True, f"User info retrieved: {data['email']}")
                    return True
                else:
                    self.log_test("Get Current User", False, "Invalid user data structure", data)
                    return False
            else:
                self.log_test("Get Current User", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get Current User", False, f"Error: {str(e)}")
            return False
    
    def test_get_formations(self):
        """Test get all formations"""
        try:
            response = self.session.get(f"{API_URL}/formations")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) >= 5:
                    self.log_test("Get All Formations", True, f"Retrieved {len(data)} formations")
                    return True
                else:
                    self.log_test("Get All Formations", False, f"Expected at least 5 formations, got {len(data) if isinstance(data, list) else 'invalid data'}", data)
                    return False
            else:
                self.log_test("Get All Formations", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get All Formations", False, f"Error: {str(e)}")
            return False
    
    def test_get_formation_by_id(self):
        """Test get specific formation"""
        try:
            response = self.session.get(f"{API_URL}/formations/1")
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "title" in data and "price" in data:
                    self.log_test("Get Formation by ID", True, f"Retrieved formation: {data['title']}")
                    return True
                else:
                    self.log_test("Get Formation by ID", False, "Invalid formation data structure", data)
                    return False
            else:
                self.log_test("Get Formation by ID", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get Formation by ID", False, f"Error: {str(e)}")
            return False
    
    def test_create_purchase(self):
        """Test create purchase"""
        if not self.token:
            self.log_test("Create Purchase", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            purchase_data = {
                "formationId": "1",
                "paymentMethod": "stripe"
            }
            
            response = self.session.post(f"{API_URL}/purchases/create", json=purchase_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "purchaseId" in data and "status" in data:
                    self.purchase_id = data["purchaseId"]
                    self.log_test("Create Purchase", True, f"Purchase created: {data['purchaseId']}")
                    return True
                else:
                    self.log_test("Create Purchase", False, "Invalid purchase response structure", data)
                    return False
            else:
                self.log_test("Create Purchase", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Create Purchase", False, f"Error: {str(e)}")
            return False
    
    def test_confirm_purchase(self):
        """Test confirm purchase"""
        if not self.token or not self.purchase_id:
            self.log_test("Confirm Purchase", False, "No auth token or purchase ID available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.post(f"{API_URL}/purchases/confirm/{self.purchase_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Confirm Purchase", True, f"Purchase confirmed: {data.get('message')}")
                    return True
                else:
                    self.log_test("Confirm Purchase", False, "Purchase confirmation failed", data)
                    return False
            else:
                self.log_test("Confirm Purchase", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Confirm Purchase", False, f"Error: {str(e)}")
            return False
    
    def test_get_my_purchases(self):
        """Test get user's purchases"""
        if not self.token:
            self.log_test("Get My Purchases", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{API_URL}/purchases/my-purchases", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Get My Purchases", True, f"Retrieved {len(data)} purchases")
                    return True
                else:
                    self.log_test("Get My Purchases", False, "Invalid purchases data structure", data)
                    return False
            else:
                self.log_test("Get My Purchases", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get My Purchases", False, f"Error: {str(e)}")
            return False
    
    def test_kyc_status(self):
        """Test get KYC status"""
        if not self.token:
            self.log_test("Get KYC Status", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{API_URL}/kyc/status", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "kycStatus" in data:
                    expected_status = "pending"
                    if data["kycStatus"] == expected_status:
                        self.log_test("Get KYC Status", True, f"KYC status: {data['kycStatus']}")
                        return True
                    else:
                        self.log_test("Get KYC Status", True, f"KYC status: {data['kycStatus']} (different from expected 'pending')")
                        return True
                else:
                    self.log_test("Get KYC Status", False, "Invalid KYC status response structure", data)
                    return False
            else:
                self.log_test("Get KYC Status", False, f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Get KYC Status", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print(f"🚀 Starting Tradalife Backend API Tests")
        print(f"📍 Backend URL: {BASE_URL}")
        print(f"📍 API URL: {API_URL}")
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_health_check,
            self.test_register,
            self.test_login,
            self.test_get_me,
            self.test_get_formations,
            self.test_get_formation_by_id,
            self.test_create_purchase,
            self.test_confirm_purchase,
            self.test_get_my_purchases,
            self.test_kyc_status
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Backend API is working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Check the details above.")
            return False

def main():
    """Main test runner"""
    tester = TradalifeTester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()