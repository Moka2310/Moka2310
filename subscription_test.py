#!/usr/bin/env python3
"""
Comprehensive Subscription System Backend Testing
Tests all subscription endpoints as requested in the review
"""

import requests
import json
import sys

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        pass
    return "https://payflow-fix-7.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class SubscriptionTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        self.test_user_email = "subscription_test@tradalife.com"
        
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
    
    def setup_test_user(self):
        """Setup test user for subscription testing"""
        try:
            # Try to register
            user_data = {
                "email": self.test_user_email,
                "password": "TestPass123!"
            }
            
            response = self.session.post(f"{API_URL}/auth/register", json=user_data)
            
            # Try to login regardless of registration result
            credentials = {
                "email": self.test_user_email,
                "password": "TestPass123!"
            }
            
            response = self.session.post(f"{API_URL}/auth/login", json=credentials)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data:
                    self.token = data["token"]
                    self.log_test("Setup Test User", True, f"User authenticated: {self.test_user_email}")
                    return True
                    
            self.log_test("Setup Test User", False, f"Failed to authenticate user: {response.status_code}")
            return False
            
        except Exception as e:
            self.log_test("Setup Test User", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_status_no_auth(self):
        """Test GET /api/subscriptions/status without authentication"""
        try:
            response = self.session.get(f"{API_URL}/subscriptions/status")
            
            if response.status_code in [401, 403]:
                self.log_test("GET /subscriptions/status (No Auth)", True, f"Correctly returned {response.status_code} for unauthenticated request")
                return True
            else:
                self.log_test("GET /subscriptions/status (No Auth)", False, f"Expected 401/403, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("GET /subscriptions/status (No Auth)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_status_no_subscription(self):
        """Test GET /api/subscriptions/status for user without subscription"""
        if not self.token:
            self.log_test("GET /subscriptions/status (No Subscription)", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{API_URL}/subscriptions/status", headers=headers)
            
            if response.status_code == 404:
                data = response.json()
                expected_message = "Aucun abonnement trouvé"
                if expected_message in data.get("detail", ""):
                    self.log_test("GET /subscriptions/status (No Subscription)", True, "Correctly returned 404 with proper French message")
                    return True
                else:
                    self.log_test("GET /subscriptions/status (No Subscription)", True, f"Returned 404 but different message: {data.get('detail')}")
                    return True
            else:
                self.log_test("GET /subscriptions/status (No Subscription)", False, f"Expected 404, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("GET /subscriptions/status (No Subscription)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_create_no_auth(self):
        """Test POST /api/subscriptions/create without authentication"""
        try:
            subscription_data = {
                "paymentMethodId": "pm_test_123",
                "telegramUsername": "@testuser"
            }
            
            response = self.session.post(f"{API_URL}/subscriptions/create", json=subscription_data)
            
            if response.status_code in [401, 403]:
                self.log_test("POST /subscriptions/create (No Auth)", True, f"Correctly returned {response.status_code} for unauthenticated request")
                return True
            else:
                self.log_test("POST /subscriptions/create (No Auth)", False, f"Expected 401/403, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/create (No Auth)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_create_invalid_data(self):
        """Test POST /api/subscriptions/create with invalid data"""
        if not self.token:
            self.log_test("POST /subscriptions/create (Invalid Data)", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            # Missing required fields
            invalid_data = {}
            
            response = self.session.post(f"{API_URL}/subscriptions/create", json=invalid_data, headers=headers)
            
            if response.status_code == 422:
                self.log_test("POST /subscriptions/create (Invalid Data)", True, "Correctly returned 422 for missing required fields")
                return True
            elif response.status_code == 400:
                self.log_test("POST /subscriptions/create (Invalid Data)", True, "Returned 400 for invalid data (acceptable)")
                return True
            else:
                self.log_test("POST /subscriptions/create (Invalid Data)", False, f"Expected 422/400, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/create (Invalid Data)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_invite_links_no_auth(self):
        """Test GET /api/subscriptions/invite-links without authentication"""
        try:
            response = self.session.get(f"{API_URL}/subscriptions/invite-links")
            
            if response.status_code in [401, 403]:
                self.log_test("GET /subscriptions/invite-links (No Auth)", True, f"Correctly returned {response.status_code} for unauthenticated request")
                return True
            else:
                self.log_test("GET /subscriptions/invite-links (No Auth)", False, f"Expected 401/403, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("GET /subscriptions/invite-links (No Auth)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_invite_links_no_subscription(self):
        """Test GET /api/subscriptions/invite-links for user without active subscription"""
        if not self.token:
            self.log_test("GET /subscriptions/invite-links (No Subscription)", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(f"{API_URL}/subscriptions/invite-links", headers=headers)
            
            if response.status_code == 403:
                data = response.json()
                expected_message = "Vous devez avoir un abonnement actif pour accéder aux canaux"
                if expected_message in data.get("detail", ""):
                    self.log_test("GET /subscriptions/invite-links (No Subscription)", True, "Correctly returned 403 with proper French message")
                    return True
                else:
                    self.log_test("GET /subscriptions/invite-links (No Subscription)", True, f"Returned 403 but different message: {data.get('detail')}")
                    return True
            else:
                self.log_test("GET /subscriptions/invite-links (No Subscription)", False, f"Expected 403, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("GET /subscriptions/invite-links (No Subscription)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_cancel_no_subscription(self):
        """Test POST /api/subscriptions/cancel for user without subscription"""
        if not self.token:
            self.log_test("POST /subscriptions/cancel (No Subscription)", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.post(f"{API_URL}/subscriptions/cancel", headers=headers)
            
            if response.status_code == 404:
                data = response.json()
                expected_message = "Aucun abonnement trouvé"
                if expected_message in data.get("detail", ""):
                    self.log_test("POST /subscriptions/cancel (No Subscription)", True, "Correctly returned 404 with proper French message")
                    return True
                else:
                    self.log_test("POST /subscriptions/cancel (No Subscription)", True, f"Returned 404 but different message: {data.get('detail')}")
                    return True
            else:
                self.log_test("POST /subscriptions/cancel (No Subscription)", False, f"Expected 404, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/cancel (No Subscription)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_reactivate_no_subscription(self):
        """Test POST /api/subscriptions/reactivate for user without subscription"""
        if not self.token:
            self.log_test("POST /subscriptions/reactivate (No Subscription)", False, "No auth token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.post(f"{API_URL}/subscriptions/reactivate", headers=headers)
            
            if response.status_code == 404:
                data = response.json()
                expected_message = "Aucun abonnement trouvé"
                if expected_message in data.get("detail", ""):
                    self.log_test("POST /subscriptions/reactivate (No Subscription)", True, "Correctly returned 404 with proper French message")
                    return True
                else:
                    self.log_test("POST /subscriptions/reactivate (No Subscription)", True, f"Returned 404 but different message: {data.get('detail')}")
                    return True
            else:
                self.log_test("POST /subscriptions/reactivate (No Subscription)", False, f"Expected 404, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/reactivate (No Subscription)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_webhook_invalid_data(self):
        """Test POST /api/subscriptions/webhook with invalid data"""
        try:
            # Test with empty payload
            response = self.session.post(f"{API_URL}/subscriptions/webhook", json={})
            
            if response.status_code == 400:
                self.log_test("POST /subscriptions/webhook (Invalid Data)", True, "Correctly returned 400 for invalid webhook data")
                return True
            else:
                self.log_test("POST /subscriptions/webhook (Invalid Data)", False, f"Expected 400, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/webhook (Invalid Data)", False, f"Error: {str(e)}")
            return False
    
    def test_subscription_webhook_valid_structure(self):
        """Test POST /api/subscriptions/webhook with valid structure"""
        try:
            # Test with valid webhook structure but test data
            webhook_data = {
                "type": "invoice.payment_succeeded",
                "data": {
                    "object": {
                        "subscription": "sub_test_123",
                        "customer": "cus_test_123"
                    }
                }
            }
            
            response = self.session.post(f"{API_URL}/subscriptions/webhook", json=webhook_data)
            
            # Should process without error even if customer doesn't exist
            if response.status_code == 200:
                self.log_test("POST /subscriptions/webhook (Valid Structure)", True, "Webhook processed successfully with test data")
                return True
            else:
                self.log_test("POST /subscriptions/webhook (Valid Structure)", False, f"Expected 200, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("POST /subscriptions/webhook (Valid Structure)", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_subscription_tests(self):
        """Run all subscription system tests as requested in the review"""
        print(f"🚀 Starting Comprehensive Subscription System Backend Testing")
        print(f"📍 Backend URL: {BASE_URL}")
        print(f"📍 API URL: {API_URL}")
        print("=" * 80)
        
        # Setup test user first
        if not self.setup_test_user():
            print("❌ Failed to setup test user. Cannot continue with authenticated tests.")
            return False
        
        # Test sequence as specified in the review request
        tests = [
            # 1. GET /api/subscriptions/status
            self.test_subscription_status_no_auth,
            self.test_subscription_status_no_subscription,
            
            # 2. POST /api/subscriptions/create
            self.test_subscription_create_no_auth,
            self.test_subscription_create_invalid_data,
            
            # 3. GET /api/subscriptions/invite-links
            self.test_subscription_invite_links_no_auth,
            self.test_subscription_invite_links_no_subscription,
            
            # 4. POST /api/subscriptions/cancel
            self.test_subscription_cancel_no_subscription,
            
            # 5. POST /api/subscriptions/reactivate
            self.test_subscription_reactivate_no_subscription,
            
            # 6. POST /api/subscriptions/webhook
            self.test_subscription_webhook_invalid_data,
            self.test_subscription_webhook_valid_structure,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 80)
        print(f"📊 Subscription System Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All subscription system tests passed! Backend endpoints are working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} subscription tests failed. Check the details above.")
            return False

def main():
    """Main test runner"""
    tester = SubscriptionTester()
    success = tester.run_comprehensive_subscription_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()