import stripe
import os
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Prix de l'abonnement mensuel : 2$ CAD
SUBSCRIPTION_PRICE_AMOUNT = 200  # en cents (2.00 CAD)
SUBSCRIPTION_PRICE_CURRENCY = "cad"

class SubscriptionService:
    """Service pour gérer les abonnements Stripe"""
    
    @staticmethod
    async def create_or_get_price() -> str:
        """Crée ou récupère le Price ID pour l'abonnement mensuel à 150$"""
        try:
            # Rechercher si le price existe déjà
            prices = stripe.Price.list(
                active=True,
                type='recurring',
                limit=100
            )
            
            for price in prices.data:
                if (price.unit_amount == SUBSCRIPTION_PRICE_AMOUNT and 
                    price.currency == SUBSCRIPTION_PRICE_CURRENCY and
                    price.recurring.interval == 'month'):
                    print(f"Price existant trouvé: {price.id}")
                    return price.id
            
            # Créer le produit
            product = stripe.Product.create(
                name="Abonnement Signaux de Trading TRADALIFE",
                description="Accès mensuel aux signaux de trading sur tous les canaux Telegram (Forex, Crypto, Indices, Gold, Actions, Commodités)",
            )
            
            # Créer le price
            price = stripe.Price.create(
                product=product.id,
                unit_amount=SUBSCRIPTION_PRICE_AMOUNT,
                currency=SUBSCRIPTION_PRICE_CURRENCY,
                recurring={"interval": "month"},
            )
            
            print(f"Nouveau Price créé: {price.id}")
            return price.id
            
        except Exception as e:
            print(f"Erreur lors de la création/récupération du price: {e}")
            raise
    
    @staticmethod
    async def create_customer(email: str, name: str) -> str:
        """Crée un client Stripe"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={
                    'platform': 'tradalife'
                }
            )
            return customer.id
        except Exception as e:
            print(f"Erreur lors de la création du customer: {e}")
            raise
    
    @staticmethod
    async def create_subscription(
        customer_id: str,
        price_id: str,
        payment_method_id: str
    ) -> Dict[str, Any]:
        """Crée un abonnement Stripe avec paiement automatique"""
        try:
            # Attacher le payment method au customer
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id,
            )
            
            # Définir comme méthode de paiement par défaut
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )
            
            # Créer l'abonnement
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                payment_settings={
                    'save_default_payment_method': 'on_subscription',
                },
                expand=['latest_invoice.payment_intent'],
            )
            
            return {
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret,
                'status': subscription.status,
            }
            
        except Exception as e:
            print(f"Erreur lors de la création de l'abonnement: {e}")
            raise
    
    @staticmethod
    async def cancel_subscription(subscription_id: str, at_period_end: bool = True) -> bool:
        """Annule un abonnement"""
        try:
            if at_period_end:
                # Annuler à la fin de la période
                stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
            else:
                # Annuler immédiatement
                stripe.Subscription.cancel(subscription_id)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'annulation de l'abonnement: {e}")
            return False
    
    @staticmethod
    async def reactivate_subscription(subscription_id: str) -> bool:
        """Réactive un abonnement qui était prévu pour être annulé"""
        try:
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False
            )
            return True
        except Exception as e:
            print(f"Erreur lors de la réactivation de l'abonnement: {e}")
            return False
    
    @staticmethod
    async def get_subscription(subscription_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les détails d'un abonnement"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': datetime.fromtimestamp(subscription.current_period_start, tz=timezone.utc),
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end, tz=timezone.utc),
                'cancel_at_period_end': subscription.cancel_at_period_end,
            }
        except Exception as e:
            print(f"Erreur lors de la récupération de l'abonnement: {e}")
            return None
    
    @staticmethod
    def verify_webhook_signature(payload: bytes, sig_header: str, webhook_secret: str) -> Optional[Any]:
        """Vérifie la signature d'un webhook Stripe"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        except ValueError as e:
            print(f"Invalid payload: {e}")
            return None
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid signature: {e}")
            return None


class PayPalSubscriptionService:
    """Service pour gérer les abonnements PayPal avec la nouvelle API REST"""
    
    # Store created plan IDs to reuse them
    _cached_product_id = None
    _cached_plan_id = None
    
    @staticmethod
    async def create_or_get_product_and_plan() -> tuple[str, str]:
        """Crée ou récupère le Product et Plan PayPal pour l'abonnement à 2$/mois"""
        try:
            from paypal_rest_service import paypal_rest_service
            
            # Check if we have cached IDs (in-memory cache for now)
            if PayPalSubscriptionService._cached_product_id and PayPalSubscriptionService._cached_plan_id:
                print(f"✅ Using cached Product ID: {PayPalSubscriptionService._cached_product_id}")
                print(f"✅ Using cached Plan ID: {PayPalSubscriptionService._cached_plan_id}")
                return PayPalSubscriptionService._cached_product_id, PayPalSubscriptionService._cached_plan_id
            
            # Create product first
            product_result = await paypal_rest_service.create_product(
                name="TRADALIFE - Signaux de Trading VIP",
                description="Accès mensuel aux signaux de trading sur 6 canaux Telegram VIP (Forex, Crypto, Indices, Gold, Actions, Commodités)"
            )
            
            if not product_result.get("success"):
                raise Exception(f"Erreur création produit PayPal: {product_result.get('error')}")
            
            product_id = product_result['data']['id']
            print(f"✅ PayPal Product créé: {product_id}")
            
            # Create billing plan
            plan_result = await paypal_rest_service.create_billing_plan(
                product_id=product_id,
                name="Abonnement Signaux TRADALIFE - Mensuel (2$ CAD)",
                description="Abonnement mensuel à 2$ CAD pour accès aux signaux de trading",
                amount=2.0,
                currency="CAD"
            )
            
            if not plan_result.get("success"):
                raise Exception(f"Erreur création plan PayPal: {plan_result.get('error')}")
            
            plan_id = plan_result['data']['id']
            print(f"✅ PayPal Plan créé: {plan_id}")
            
            # Cache the IDs
            PayPalSubscriptionService._cached_product_id = product_id
            PayPalSubscriptionService._cached_plan_id = plan_id
            
            return product_id, plan_id
                
        except Exception as e:
            print(f"❌ Erreur lors de la création du produit/plan PayPal: {e}")
            raise
    
    @staticmethod
    async def create_subscription(telegram_username: str, user_email: str) -> Dict[str, Any]:
        """Crée un abonnement PayPal avec la nouvelle API REST"""
        try:
            from paypal_rest_service import paypal_rest_service
            
            # Get or create product and plan
            product_id, plan_id = await PayPalSubscriptionService.create_or_get_product_and_plan()
            
            # Get frontend URL for return/cancel URLs
            frontend_url = os.environ.get("FRONTEND_URL", "https://tradalife.com")
            
            # Create subscription
            subscription_result = await paypal_rest_service.create_subscription(
                plan_id=plan_id,
                return_url=f"{frontend_url}/subscription-success",
                cancel_url=f"{frontend_url}/subscription-cancel"
            )
            
            if subscription_result.get("success"):
                return {
                    "success": True,
                    "approval_url": subscription_result["approval_url"],
                    "subscription_id": subscription_result["subscription_id"],
                    "plan_id": plan_id
                }
            else:
                raise Exception(f"Erreur création subscription PayPal: {subscription_result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'abonnement PayPal: {e}")
            raise
    
    @staticmethod
    async def execute_subscription(agreement_token: str) -> Dict[str, Any]:
        """Exécute un abonnement PayPal après approbation de l'utilisateur"""
        try:
            from payment_service import PayPalPayment
            
            execute_result = await PayPalPayment.execute_billing_agreement(agreement_token)
            
            if execute_result["success"]:
                return {
                    "success": True,
                    "agreement_id": execute_result["agreement_id"],
                    "status": execute_result["state"]
                }
            else:
                raise Exception(f"Erreur exécution agreement PayPal: {execute_result['error']}")
                
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de l'abonnement PayPal: {e}")
            raise
    
    @staticmethod
    async def cancel_subscription(agreement_id: str) -> bool:
        """Annule un abonnement PayPal"""
        try:
            from payment_service import PayPalPayment
            
            cancel_result = await PayPalPayment.cancel_billing_agreement(agreement_id)
            
            return cancel_result["success"]
                
        except Exception as e:
            print(f"❌ Erreur lors de l'annulation de l'abonnement PayPal: {e}")
            return False
