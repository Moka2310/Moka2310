from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pymongo import MongoClient
from datetime import datetime, timezone
import uuid
import os
from typing import Optional

from models import SubscriptionCreate, SubscriptionResponse, Subscription, SubscriptionStatus
from dependencies import get_current_user
from subscription_service import SubscriptionService
from telegram_service import telegram_service
from email_service import EmailService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

# Configuration
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '-1002067865549')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# MongoDB connection
def get_db():
    mongo_url = os.environ['MONGO_URL']
    client = MongoClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'tradalife')]
    return db

@router.post("/create")
async def create_subscription(
    subscription_data: SubscriptionCreate,
    current_user = Depends(get_current_user)
):
    """
    Crée un nouvel abonnement mensuel à 150$/mois pour accéder aux signaux
    """
    try:
        db = get_db()
        user_id = current_user.id
        user_email = current_user.email
        user_name = f"{getattr(current_user, 'firstName', '') or ''} {getattr(current_user, 'lastName', '') or ''}".strip() or user_email
        
        # Vérifier si l'utilisateur a déjà un abonnement actif
        existing_user = db.users.find_one({"id": user_id})
        if existing_user and existing_user.get('subscriptionStatus') == SubscriptionStatus.ACTIVE.value:
            raise HTTPException(status_code=400, detail="Vous avez déjà un abonnement actif")
        
        # Créer ou récupérer le Price ID
        price_id = await SubscriptionService.create_or_get_price()
        
        # Créer le customer Stripe si nécessaire
        stripe_customer_id = existing_user.get('stripeCustomerId')
        if not stripe_customer_id:
            stripe_customer_id = await SubscriptionService.create_customer(user_email, user_name)
            # Sauvegarder le customer ID
            db.users.update_one(
                {"id": user_id},
                {"$set": {"stripeCustomerId": stripe_customer_id}}
            )
        
        # Créer l'abonnement
        subscription_result = await SubscriptionService.create_subscription(
            customer_id=stripe_customer_id,
            price_id=price_id,
            payment_method_id=subscription_data.paymentMethodId
        )
        
        # Créer l'enregistrement de l'abonnement dans la DB
        subscription_id = str(uuid.uuid4())
        subscription_doc = {
            "id": subscription_id,
            "userId": user_id,
            "stripeSubscriptionId": subscription_result['subscription_id'],
            "stripeCustomerId": stripe_customer_id,
            "status": subscription_result['status'],
            "priceId": price_id,
            "currentPeriodStart": datetime.now(timezone.utc).isoformat(),
            "currentPeriodEnd": datetime.now(timezone.utc).isoformat(),  # Sera mis à jour par le webhook
            "cancelAtPeriodEnd": False,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        
        db.subscriptions.insert_one(subscription_doc)
        
        # Mettre à jour l'utilisateur avec le username Telegram
        db.users.update_one(
            {"id": user_id},
            {"$set": {
                "telegramUsername": subscription_data.telegramUsername,
                "subscriptionId": subscription_result['subscription_id'],
                "subscriptionStatus": subscription_result['status'],
            }}
        )
        
        return {
            "clientSecret": subscription_result['client_secret'],
            "subscriptionId": subscription_result['subscription_id'],
            "status": subscription_result['status']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user = Depends(get_current_user)
):
    """
    Récupère le statut de l'abonnement de l'utilisateur
    """
    try:
        db = get_db()
        user_id = current_user.id
        user = db.users.find_one({"id": user_id})
        
        if not user or not user.get('subscriptionId'):
            raise HTTPException(status_code=404, detail="Aucun abonnement trouvé")
        
        subscription = db.subscriptions.find_one({"userId": user_id})
        if not subscription:
            raise HTTPException(status_code=404, detail="Abonnement introuvable")
        
        # Récupérer les infos depuis Stripe
        stripe_info = await SubscriptionService.get_subscription(user['subscriptionId'])
        
        return SubscriptionResponse(
            id=subscription['id'],
            status=stripe_info['status'] if stripe_info else subscription['status'],
            currentPeriodEnd=datetime.fromisoformat(subscription['currentPeriodEnd']),
            cancelAtPeriodEnd=subscription.get('cancelAtPeriodEnd', False),
            pricePerMonth=150.0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting subscription status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel")
async def cancel_subscription(
    current_user = Depends(get_current_user)
):
    """
    Annule l'abonnement à la fin de la période en cours
    """
    try:
        db = get_db()
        user_id = current_user.id
        user = db.users.find_one({"id": user_id})
        
        if not user or not user.get('subscriptionId'):
            raise HTTPException(status_code=404, detail="Aucun abonnement trouvé")
        
        # Annuler l'abonnement dans Stripe
        success = await SubscriptionService.cancel_subscription(
            user['subscriptionId'],
            at_period_end=True
        )
        
        if success:
            # Mettre à jour la DB
            db.subscriptions.update_one(
                {"userId": user_id},
                {"$set": {
                    "cancelAtPeriodEnd": True,
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            return {"message": "Abonnement annulé. Vous garderez l'accès jusqu'à la fin de la période en cours."}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de l'annulation")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error canceling subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reactivate")
async def reactivate_subscription(
    current_user = Depends(get_current_user)
):
    """
    Réactive un abonnement qui était prévu pour être annulé
    """
    try:
        db = get_db()
        user_id = current_user.id
        user = db.users.find_one({"id": user_id})
        
        if not user or not user.get('subscriptionId'):
            raise HTTPException(status_code=404, detail="Aucun abonnement trouvé")
        
        # Réactiver l'abonnement dans Stripe
        success = await SubscriptionService.reactivate_subscription(user['subscriptionId'])
        
        if success:
            # Mettre à jour la DB
            db.subscriptions.update_one(
                {"userId": user_id},
                {"$set": {
                    "cancelAtPeriodEnd": False,
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }}
            )
            
            return {"message": "Abonnement réactivé avec succès"}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de la réactivation")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error reactivating subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/invite-links")
async def get_telegram_invite_links(
    current_user = Depends(get_current_user),
    db: MongoClient = Depends(get_db)
):
    """
    Génère des liens d'invitation Telegram pour TOUS les canaux VIP
    """
    try:
        user_id = current_user.id
        user = db.users.find_one({"id": user_id})
        
        # Vérifier que l'utilisateur a un abonnement actif
        if not user or user.get('subscriptionStatus') != SubscriptionStatus.ACTIVE.value:
            raise HTTPException(
                status_code=403, 
                detail="Vous devez avoir un abonnement actif pour accéder aux canaux"
            )
        
        # Liste des canaux avec leurs Chat IDs
        channels = {
            "INDICES": os.environ.get('TELEGRAM_CHANNEL_INDICES'),
            "ACTIONS": os.environ.get('TELEGRAM_CHANNEL_ACTIONS'),
            "GOLD": os.environ.get('TELEGRAM_CHANNEL_GOLD'),
            "FOREX": os.environ.get('TELEGRAM_CHANNEL_FOREX'),
            "CRYPTO": os.environ.get('TELEGRAM_CHANNEL_CRYPTO'),
            "COMMODITES": os.environ.get('TELEGRAM_CHANNEL_COMMODITES'),
        }
        
        # Générer un lien d'invitation pour chaque canal
        invite_links = {}
        
        for channel_name, chat_id in channels.items():
            if not chat_id:
                continue
                
            invite_link = await telegram_service.create_chat_invite_link(chat_id, member_limit=1)
            
            if invite_link:
                invite_links[channel_name] = invite_link
            else:
                invite_links[channel_name] = None
        
        if not invite_links:
            raise HTTPException(status_code=500, detail="Impossible de créer les liens d'invitation")
        
        return {"inviteLinks": invite_links}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting invite links: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: Optional[str] = Header(None)):
    """
    Webhook pour recevoir les événements Stripe
    """
    try:
        payload = await request.body()
        
        # Vérifier la signature si le webhook secret est configuré
        if STRIPE_WEBHOOK_SECRET and stripe_signature:
            event = SubscriptionService.verify_webhook_signature(
                payload, stripe_signature, STRIPE_WEBHOOK_SECRET
            )
            if not event:
                raise HTTPException(status_code=400, detail="Invalid signature")
        else:
            import json
            event = json.loads(payload)
        
        # Traiter les différents types d'événements
        event_type = event['type']
        data = event['data']['object']
        
        db = get_db()
        
        if event_type == 'invoice.payment_succeeded':
            # Paiement réussi - activer/renouveler l'abonnement
            subscription_id = data['subscription']
            customer_id = data['customer']
            
            # Trouver l'utilisateur
            user = db.users.find_one({"stripeCustomerId": customer_id})
            if user:
                # Mettre à jour le statut
                db.users.update_one(
                    {"id": user['id']},
                    {"$set": {
                        "subscriptionStatus": SubscriptionStatus.ACTIVE.value,
                        "lastPaymentDate": datetime.now(timezone.utc).isoformat(),
                    }}
                )
                
                # Envoyer un email de confirmation
                email_service = EmailService()
                await email_service.send_subscription_confirmation(user['email'])
                
                print(f"Subscription activated for user {user['id']}")
        
        elif event_type == 'invoice.payment_failed':
            # Paiement échoué - marquer comme past_due
            subscription_id = data['subscription']
            customer_id = data['customer']
            
            user = db.users.find_one({"stripeCustomerId": customer_id})
            if user:
                db.users.update_one(
                    {"id": user['id']},
                    {"$set": {
                        "subscriptionStatus": SubscriptionStatus.PAST_DUE.value,
                    }}
                )
                
                # Envoyer un email de rappel
                email_service = EmailService()
                await email_service.send_payment_failed_reminder(user['email'])
                
                print(f"Payment failed for user {user['id']}")
        
        elif event_type == 'customer.subscription.updated':
            # Abonnement mis à jour
            subscription_id = data['id']
            status = data['status']
            current_period_end = data['current_period_end']
            
            # Mettre à jour dans la DB
            db.subscriptions.update_one(
                {"stripeSubscriptionId": subscription_id},
                {"$set": {
                    "status": status,
                    "currentPeriodEnd": datetime.fromtimestamp(current_period_end, tz=timezone.utc).isoformat(),
                    "cancelAtPeriodEnd": data.get('cancel_at_period_end', False),
                    "updatedAt": datetime.now(timezone.utc).isoformat(),
                }}
            )
            
            print(f"Subscription {subscription_id} updated to status: {status}")
        
        elif event_type == 'customer.subscription.deleted':
            # Abonnement annulé/expiré
            subscription_id = data['id']
            customer_id = data['customer']
            
            user = db.users.find_one({"stripeCustomerId": customer_id})
            if user:
                db.users.update_one(
                    {"id": user['id']},
                    {"$set": {
                        "subscriptionStatus": SubscriptionStatus.CANCELED.value,
                    }}
                )
                
                # TODO: Retirer l'utilisateur des canaux Telegram
                print(f"Subscription canceled for user {user['id']}")
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
