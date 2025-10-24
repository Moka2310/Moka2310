import os
import stripe
import paypalrestsdk
from typing import Optional

class StripePayment:
    @staticmethod
    async def create_payment_intent(amount: float, currency: str = "cad", metadata: dict = None):
        """Create a Stripe payment intent"""
        try:
            # Configure Stripe with environment variable
            stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_votre_cle_stripe_ici")
            
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={"enabled": True}
            )
            return {
                "success": True,
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def confirm_payment(payment_intent_id: str):
        """Confirm a Stripe payment"""
        try:
            # Configure Stripe with environment variable
            stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_votre_cle_stripe_ici")
            
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "success": True,
                "status": intent.status,
                "amount": intent.amount / 100
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class PayPalPayment:
    @staticmethod
    def _configure_paypal():
        """Configure PayPal with environment variables"""
        paypalrestsdk.configure({
            "mode": os.environ.get("PAYPAL_MODE", "sandbox"),
            "client_id": os.environ.get("PAYPAL_CLIENT_ID", "votre_client_id_paypal"),
            "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET", "votre_secret_paypal")
        })
    
    @staticmethod
    async def create_payment(amount: float, currency: str = "CAD", description: str = "", return_url: str = "", cancel_url: str = ""):
        """Create a PayPal payment"""
        try:
            # Configure PayPal before creating payment
            PayPalPayment._configure_paypal()
            
            # Get frontend URL from environment
            frontend_url = os.environ.get("FRONTEND_URL", "https://app.emergent.host")
            
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": return_url or f"{frontend_url}/payment-success",
                    "cancel_url": cancel_url or f"{frontend_url}/payment-cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": description,
                            "sku": "item",
                            "price": str(amount),
                            "currency": currency,
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": description
                }]
            })

            if payment.create():
                # Get approval URL
                for link in payment.links:
                    if link.rel == "approval_url":
                        return {
                            "success": True,
                            "payment_id": payment.id,
                            "approval_url": link.href
                        }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def execute_payment(payment_id: str, payer_id: str):
        """Execute/confirm a PayPal payment"""
        try:
            # Configure PayPal before executing payment
            PayPalPayment._configure_paypal()
            
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                return {
                    "success": True,
                    "status": payment.state,
                    "amount": float(payment.transactions[0].amount.total)
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def create_billing_plan(name: str, description: str, amount: float, currency: str = "CAD"):
        """Create a PayPal billing plan for subscriptions"""
        try:
            PayPalPayment._configure_paypal()
            
            billing_plan = paypalrestsdk.BillingPlan({
                "name": name,
                "description": description,
                "type": "INFINITE",
                "payment_definitions": [{
                    "name": "Regular Payments",
                    "type": "REGULAR",
                    "frequency": "MONTH",
                    "frequency_interval": "1",
                    "cycles": "0",
                    "amount": {
                        "value": str(amount),
                        "currency": currency
                    }
                }],
                "merchant_preferences": {
                    "setup_fee": {
                        "value": "0",
                        "currency": currency
                    },
                    "return_url": os.environ.get("FRONTEND_URL", "https://tradalife.com") + "/subscription-success",
                    "cancel_url": os.environ.get("FRONTEND_URL", "https://tradalife.com") + "/subscription-cancel",
                    "auto_bill_amount": "YES",
                    "initial_fail_amount_action": "CONTINUE",
                    "max_fail_attempts": "3"
                }
            })
            
            if billing_plan.create():
                # Activate the plan
                if billing_plan.replace([
                    {
                        "op": "replace",
                        "path": "/",
                        "value": {
                            "state": "ACTIVE"
                        }
                    }
                ]):
                    return {
                        "success": True,
                        "plan_id": billing_plan.id
                    }
            
            return {
                "success": False,
                "error": billing_plan.error if hasattr(billing_plan, 'error') else "Failed to create plan"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def create_billing_agreement(plan_id: str, name: str, description: str, start_date: str):
        """Create a billing agreement for a subscription"""
        try:
            PayPalPayment._configure_paypal()
            
            billing_agreement = paypalrestsdk.BillingAgreement({
                "name": name,
                "description": description,
                "start_date": start_date,
                "plan": {
                    "id": plan_id
                },
                "payer": {
                    "payment_method": "paypal"
                }
            })
            
            if billing_agreement.create():
                # Get approval URL
                for link in billing_agreement.links:
                    if link.rel == "approval_url":
                        return {
                            "success": True,
                            "approval_url": link.href,
                            "agreement_token": billing_agreement.token
                        }
            
            return {
                "success": False,
                "error": billing_agreement.error if hasattr(billing_agreement, 'error') else "Failed to create agreement"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def execute_billing_agreement(agreement_token: str):
        """Execute a billing agreement after user approval"""
        try:
            PayPalPayment._configure_paypal()
            
            billing_agreement = paypalrestsdk.BillingAgreement.execute(agreement_token)
            
            if billing_agreement:
                return {
                    "success": True,
                    "agreement_id": billing_agreement.id,
                    "state": billing_agreement.state
                }
            
            return {
                "success": False,
                "error": "Failed to execute agreement"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def cancel_billing_agreement(agreement_id: str):
        """Cancel a PayPal billing agreement"""
        try:
            PayPalPayment._configure_paypal()
            
            billing_agreement = paypalrestsdk.BillingAgreement.find(agreement_id)
            
            if billing_agreement.cancel({"note": "Canceling the agreement"}):
                return {
                    "success": True,
                    "message": "Agreement canceled"
                }
            
            return {
                "success": False,
                "error": "Failed to cancel agreement"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }