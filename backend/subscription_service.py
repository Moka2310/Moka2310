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
    """Service pour gérer les abonnements PayPal"""
    
    @staticmethod
    async def create_or_get_billing_plan() -> str:
        """Crée ou récupère le Billing Plan PayPal pour l'abonnement à 150$/mois"""
        try:
            from payment_service import PayPalPayment
            
            # Pour l'instant, créer un nouveau plan à chaque fois
            # TODO: Stocker le plan_id en DB et le réutiliser
            plan_result = await PayPalPayment.create_billing_plan(
                name="Abonnement Signaux TRADALIFE - Mensuel",
                description="Accès mensuel aux signaux de trading sur tous les canaux Telegram (Forex, Crypto, Indices, Gold, Actions, Commodités)",
                amount=150.0,
                currency="CAD"
            )
            
            if plan_result["success"]:
                print(f"✅ PayPal Billing Plan créé: {plan_result['plan_id']}")
                return plan_result["plan_id"]
            else:
                raise Exception(f"Erreur création plan PayPal: {plan_result['error']}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la création du billing plan PayPal: {e}")
            raise
    
    @staticmethod
    async def create_subscription(telegram_username: str, user_email: str) -> Dict[str, Any]:
        """Crée un abonnement PayPal"""
        try:
            from payment_service import PayPalPayment
            
            # Créer ou récupérer le billing plan
            plan_id = await PayPalSubscriptionService.create_or_get_billing_plan()
            
            # Date de début (dans 5 minutes pour laisser le temps à l'utilisateur d'approuver)
            start_date = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
            
            # Créer le billing agreement
            agreement_result = await PayPalPayment.create_billing_agreement(
                plan_id=plan_id,
                name=f"Abonnement TRADALIFE - {telegram_username}",
                description=f"Abonnement mensuel signaux trading pour {user_email}",
                start_date=start_date
            )
            
            if agreement_result["success"]:
                return {
                    "success": True,
                    "approval_url": agreement_result["approval_url"],
                    "agreement_token": agreement_result["agreement_token"],
                    "plan_id": plan_id
                }
            else:
                raise Exception(f"Erreur création agreement PayPal: {agreement_result['error']}")
                
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
