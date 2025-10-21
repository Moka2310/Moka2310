import stripe
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Prix de l'abonnement mensuel : 150$ CAD
SUBSCRIPTION_PRICE_AMOUNT = 15000  # en cents (150.00 CAD)
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
                description="Accès mensuel aux signaux de trading sur tous les canaux Telegram (Forex, Crypto, Indices, etc.)",
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
