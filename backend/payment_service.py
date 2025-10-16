import os
import stripe
import paypalrestsdk
from typing import Optional

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_votre_cle_stripe_ici")

class StripePayment:
    @staticmethod
    async def create_payment_intent(amount: float, currency: str = "eur", metadata: dict = None):
        """Create a Stripe payment intent"""
        try:
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
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    async def confirm_payment(payment_intent_id: str):
        """Confirm a Stripe payment"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "success": True,
                "status": intent.status,
                "amount": intent.amount / 100
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e)
            }

# PayPal configuration
paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE", "sandbox"),  # sandbox or live
    "client_id": os.getenv("PAYPAL_CLIENT_ID", "votre_client_id_paypal"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET", "votre_secret_paypal")
})

class PayPalPayment:
    @staticmethod
    async def create_payment(amount: float, currency: str = "EUR", description: str = "", return_url: str = "", cancel_url: str = ""):
        """Create a PayPal payment"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": return_url or "https://videocourse.preview.emergentagent.com/payment-success",
                    "cancel_url": cancel_url or "https://videocourse.preview.emergentagent.com/payment-cancel"
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