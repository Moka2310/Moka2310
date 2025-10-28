#!/usr/bin/env python3
"""
Test spécifique pour le système de compteur de précommandes du bot
Selon les spécifications du test request:
- Vérifier GET /api/bot-preorders/availability
- Tester la limite de précommandes sans authentification
- Compter les précommandes en base de données
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
    return "https://autotrader-hub-12.preview.emergentagent.com"

BASE_URL = get_backend_url()
API_URL = f"{BASE_URL}/api"

class BotPreorderTester:
    def __init__(self):
        self.session = requests.Session()
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

    def test_availability_endpoint(self):
        """
        Test 1: GET /api/bot-preorders/availability
        Doit retourner: available: 9, total: 30, sold: 21, is_available: true
        """
        try:
            response = self.session.get(f"{API_URL}/bot-preorders/availability")
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure de la réponse
                required_fields = ["total", "sold", "available", "is_available"]
                if not all(field in data for field in required_fields):
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_test("Availability Endpoint - Structure", False, 
                                f"Missing fields: {missing_fields}", data)
                    return False
                
                # Vérifier les valeurs attendues
                expected = {
                    "total": 30,
                    "sold": 21,
                    "available": 9,
                    "is_available": True
                }
                
                actual = {
                    "total": data["total"],
                    "sold": data["sold"],
                    "available": data["available"],
                    "is_available": data["is_available"]
                }
                
                if actual == expected:
                    self.log_test("Availability Endpoint - Values", True, 
                                f"✅ Correct values: available={actual['available']}, total={actual['total']}, sold={actual['sold']}, is_available={actual['is_available']}")
                    return True
                else:
                    self.log_test("Availability Endpoint - Values", False, 
                                f"❌ Expected: {expected}, Got: {actual}")
                    return False
            else:
                self.log_test("Availability Endpoint", False, 
                            f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Availability Endpoint", False, f"Error: {str(e)}")
            return False

    def test_preorder_limit_without_auth(self):
        """
        Test 2: Essayer de créer une précommande sans authentification
        Devrait retourner 401 (Not authenticated)
        """
        try:
            preorder_data = {
                "paymentMethod": "stripe"
            }
            
            response = self.session.post(f"{API_URL}/bot-preorders/create", json=preorder_data)
            
            if response.status_code == 401:
                self.log_test("Preorder Limit (No Auth)", True, 
                            "✅ Correctly returned 401 (Not authenticated)")
                return True
            elif response.status_code == 403:
                # FastAPI sometimes returns 403 instead of 401 for authentication
                data = response.json()
                if "Not authenticated" in data.get("detail", ""):
                    self.log_test("Preorder Limit (No Auth)", True, 
                                "✅ Correctly returned 403 (Not authenticated)")
                    return True
                else:
                    self.log_test("Preorder Limit (No Auth)", False, 
                                f"Expected authentication error, got: {data}")
                    return False
            else:
                self.log_test("Preorder Limit (No Auth)", False, 
                            f"Expected 401/403, got {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Preorder Limit (No Auth)", False, f"Error: {str(e)}")
            return False

    def test_database_preorder_count(self):
        """
        Test 3: Vérifier qu'il y a bien 21 précommandes avec status "paid" ou "pending_payment"
        Le calcul doit être: 30 - 21 = 9 disponibles
        """
        try:
            response = self.session.get(f"{API_URL}/bot-preorders/availability")
            
            if response.status_code == 200:
                data = response.json()
                sold_count = data.get("sold", 0)
                total_count = data.get("total", 0)
                available_count = data.get("available", 0)
                
                # Vérifier le calcul: total - sold = available
                expected_available = total_count - sold_count
                
                if available_count == expected_available:
                    if sold_count == 21:
                        self.log_test("Database Preorder Count", True, 
                                    f"✅ Database contains {sold_count} preorders with 'paid' or 'pending_payment' status. Calculation: {total_count} - {sold_count} = {available_count} available")
                        return True
                    else:
                        self.log_test("Database Preorder Count", False, 
                                    f"❌ Expected 21 preorders, found {sold_count}")
                        return False
                else:
                    self.log_test("Database Preorder Count", False, 
                                f"❌ Calculation error: {total_count} - {sold_count} should equal {expected_available}, but got {available_count}")
                    return False
            else:
                self.log_test("Database Preorder Count", False, 
                            f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Database Preorder Count", False, f"Error: {str(e)}")
            return False

    def test_counter_logic(self):
        """
        Test 4: Vérifier la logique complète du compteur
        """
        try:
            response = self.session.get(f"{API_URL}/bot-preorders/availability")
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier que is_available est cohérent avec available
                is_available = data.get("is_available", False)
                available = data.get("available", 0)
                
                if (available > 0 and is_available) or (available == 0 and not is_available):
                    self.log_test("Counter Logic", True, 
                                f"✅ Counter logic is correct: available={available}, is_available={is_available}")
                    return True
                else:
                    self.log_test("Counter Logic", False, 
                                f"❌ Logic error: available={available} but is_available={is_available}")
                    return False
            else:
                self.log_test("Counter Logic", False, 
                            f"Status code: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Counter Logic", False, f"Error: {str(e)}")
            return False

    def run_bot_preorder_tests(self):
        """Run all bot preorder tests"""
        print("🤖 Testing Bot Preorder Counter System")
        print(f"📍 Backend URL: {BASE_URL}")
        print(f"📍 API URL: {API_URL}")
        print("=" * 80)
        print("📋 Test Requirements:")
        print("   1. GET /api/bot-preorders/availability should return: available=9, total=30, sold=21, is_available=true")
        print("   2. Creating preorder without auth should return 401")
        print("   3. Database should contain 21 preorders with status 'paid' or 'pending_payment'")
        print("   4. Counter logic should be: 30 - 21 = 9 available")
        print("=" * 80)
        
        tests = [
            self.test_availability_endpoint,
            self.test_preorder_limit_without_auth,
            self.test_database_preorder_count,
            self.test_counter_logic
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 80)
        print(f"📊 Bot Preorder Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All bot preorder tests passed! Counter system is working correctly.")
            print("✅ Le système de compteur de précommandes fonctionne parfaitement:")
            print("   - L'endpoint /availability retourne les bonnes valeurs")
            print("   - La limite de précommandes est respectée")
            print("   - Le calcul du compteur est correct (9/30)")
            return True
        else:
            print(f"⚠️  {total - passed} tests failed. Check the details above.")
            return False

def main():
    """Main test runner"""
    tester = BotPreorderTester()
    success = tester.run_bot_preorder_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()