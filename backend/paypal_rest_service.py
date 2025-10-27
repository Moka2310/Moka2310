"""
PayPal REST API Service - Direct API calls (modern approach)
Using PayPal REST API v2 for subscriptions
"""
import os
import requests
import base64
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PayPalRESTService:
    """Modern PayPal REST API service using direct HTTP requests"""
    
    def __init__(self):
        self.client_id = os.environ.get('PAYPAL_CLIENT_ID')
        self.client_secret = os.environ.get('PAYPAL_CLIENT_SECRET')
        self.mode = os.environ.get('PAYPAL_MODE', 'sandbox')
        
        # Set API URL based on mode
        if self.mode == 'live':
            self.api_url = 'https://api-m.paypal.com'
        else:
            self.api_url = 'https://api-m.sandbox.paypal.com'
        
        self._access_token = None
        self._token_expires_at = 0
    
    def _get_access_token(self) -> str:
        """Get OAuth 2.0 access token"""
        import time
        
        # Return cached token if still valid
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        
        try:
            # Create Basic Auth header
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            response = requests.post(
                f"{self.api_url}/v1/oauth2/token",
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en_US",
                    "Authorization": f"Basic {auth_b64}"
                },
                data={"grant_type": "client_credentials"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self._access_token = token_data['access_token']
                # Cache token (expires in seconds - 1 hour buffer)
                self._token_expires_at = time.time() + token_data.get('expires_in', 32400) - 3600
                logger.info("✅ PayPal access token obtained")
                return self._access_token
            else:
                logger.error(f"❌ Failed to get PayPal token: {response.status_code} - {response.text}")
                raise Exception(f"PayPal authentication failed: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ PayPal token error: {e}")
            raise
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to PayPal API"""
        token = self._get_access_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        url = f"{self.api_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            logger.info(f"PayPal API {method} {endpoint}: {response.status_code}")
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "data": response.json() if response.text else {},
                    "status_code": response.status_code
                }
            else:
                logger.error(f"PayPal API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            logger.error(f"PayPal request error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_product(self, name: str, description: str) -> Dict[str, Any]:
        """Create a product for subscription plan"""
        data = {
            "name": name,
            "description": description,
            "type": "SERVICE",
            "category": "SOFTWARE"
        }
        
        result = self._make_request("POST", "/v1/catalogs/products", data)
        return result
    
    async def create_billing_plan(self, product_id: str, name: str, description: str, amount: float, currency: str = "CAD") -> Dict[str, Any]:
        """Create a billing plan for subscriptions using PayPal REST API v1"""
        
        data = {
            "product_id": product_id,
            "name": name,
            "description": description,
            "status": "ACTIVE",
            "billing_cycles": [
                {
                    "frequency": {
                        "interval_unit": "MONTH",
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 0,  # Infinite
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": str(amount),
                            "currency_code": currency
                        }
                    }
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee_failure_action": "CONTINUE",
                "payment_failure_threshold": 3
            }
        }
        
        result = self._make_request("POST", "/v1/billing/plans", data)
        return result
    
    async def create_subscription(self, plan_id: str, return_url: str, cancel_url: str) -> Dict[str, Any]:
        """Create a subscription"""
        
        data = {
            "plan_id": plan_id,
            "application_context": {
                "brand_name": "TRADALIFE",
                "locale": "fr-CA",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "SUBSCRIBE_NOW",
                "return_url": return_url,
                "cancel_url": cancel_url
            }
        }
        
        result = self._make_request("POST", "/v1/billing/subscriptions", data)
        
        if result.get("success"):
            subscription_data = result.get("data", {})
            subscription_id = subscription_data.get("id")
            
            # Extract approval URL
            approval_url = None
            for link in subscription_data.get("links", []):
                if link.get("rel") == "approve":
                    approval_url = link.get("href")
                    break
            
            return {
                "success": True,
                "subscription_id": subscription_id,
                "approval_url": approval_url,
                "status": subscription_data.get("status")
            }
        
        return result
    
    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details"""
        result = self._make_request("GET", f"/v1/billing/subscriptions/{subscription_id}")
        return result
    
    async def cancel_subscription(self, subscription_id: str, reason: str = "User requested cancellation") -> Dict[str, Any]:
        """Cancel a subscription"""
        data = {
            "reason": reason
        }
        
        result = self._make_request("POST", f"/v1/billing/subscriptions/{subscription_id}/cancel", data)
        return result


# Singleton instance
paypal_rest_service = PayPalRESTService()
