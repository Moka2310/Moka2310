from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pymongo import MongoClient
from datetime import datetime, timezone
import uuid
import os
from typing import Optional

from models import SubscriptionCreate, SubscriptionResponse, Subscription, SubscriptionStatus
from dependencies import get_current_user, require_admin
from subscription_service import SubscriptionService, PayPalSubscriptionService
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
    Supporte Stripe et PayPal
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
        
        # Déterminer la méthode de paiement (Stripe par défaut si non spécifié)
        payment_method = getattr(subscription_data, 'paymentMethod', 'stripe')
        
        if payment_method == "stripe":
            # ===== STRIPE =====
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
                "paymentMethod": "stripe",
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
                "status": subscription_result['status'],
                "paymentMethod": "stripe"
            }
            
        elif payment_method == "paypal":
            # ===== PAYPAL (Nouvelle API REST) =====
            subscription_result = await PayPalSubscriptionService.create_subscription(
                telegram_username=subscription_data.telegramUsername,
                user_email=user_email
            )
            
            if subscription_result["success"]:
                # Créer l'enregistrement de l'abonnement dans la DB (en attente)
                subscription_id = str(uuid.uuid4())
                subscription_doc = {
                    "id": subscription_id,
                    "userId": user_id,
                    "paypalSubscriptionId": subscription_result['subscription_id'],
                    "paypalPlanId": subscription_result['plan_id'],
                    "status": "pending",  # En attente de l'approbation PayPal
                    "paymentMethod": "paypal",
                    "currentPeriodStart": datetime.now(timezone.utc).isoformat(),
                    "currentPeriodEnd": datetime.now(timezone.utc).isoformat(),
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
                        "paypalSubscriptionId": subscription_result['subscription_id'],
                        "subscriptionStatus": "pending",
                    }}
                )
                
                return {
                    "approvalUrl": subscription_result['approval_url'],
                    "subscriptionId": subscription_result['subscription_id'],
                    "status": "pending",
                    "paymentMethod": "paypal"
                }
            else:
                raise HTTPException(status_code=400, detail="Erreur lors de la création de l'abonnement PayPal")
        
        else:
            raise HTTPException(status_code=400, detail="Méthode de paiement non supportée")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NOTE: Cette route n'est plus utilisée avec la nouvelle API PayPal REST v1
# Les subscriptions PayPal sont maintenant activées automatiquement via le webhook
# @router.post("/execute-paypal-subscription")
# async def execute_paypal_subscription(...)


@router.post("/paypal-webhook")
async def paypal_webhook(request: Request):
    """
    Webhook pour recevoir les notifications PayPal
    """
    try:
        db = get_db()
        
        # Récupérer le payload
        payload = await request.json()
        event_type = payload.get('event_type')
        resource = payload.get('resource', {})
        
        print(f"📥 PayPal Webhook received: {event_type}")
        
        # Gérer les événements d'abonnement
        if event_type == 'BILLING.SUBSCRIPTION.CREATED':
            # Abonnement créé (en attente d'activation)
            agreement_id = resource.get('id')
            print(f"✅ Subscription created: {agreement_id}")
            
        elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            # Abonnement activé - IMPORTANT
            agreement_id = resource.get('id')
            
            # Trouver l'abonnement dans la DB
            subscription = await db.subscriptions.find_one({
                "paypalAgreementId": agreement_id
            })
            
            if subscription:
                # Mettre à jour le statut
                await db.subscriptions.update_one(
                    {"id": subscription['id']},
                    {"$set": {
                        "status": SubscriptionStatus.ACTIVE.value,
                        "updatedAt": datetime.now(timezone.utc).isoformat()
                    }}
                )
                
                # Mettre à jour l'utilisateur
                await db.users.update_one(
                    {"id": subscription['userId']},
                    {"$set": {"subscriptionStatus": SubscriptionStatus.ACTIVE.value}}
                )
                
                print(f"✅ Subscription activated: {agreement_id}")
                
                # TODO: Envoyer email de confirmation
                # TODO: Ajouter au Telegram
                
        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            # Abonnement annulé
            agreement_id = resource.get('id')
            
            subscription = await db.subscriptions.find_one({
                "paypalAgreementId": agreement_id
            })
            
            if subscription:
                await db.subscriptions.update_one(
                    {"id": subscription['id']},
                    {"$set": {
                        "status": SubscriptionStatus.CANCELED.value,
                        "updatedAt": datetime.now(timezone.utc).isoformat()
                    }}
                )
                
                await db.users.update_one(
                    {"id": subscription['userId']},
                    {"$set": {"subscriptionStatus": SubscriptionStatus.CANCELED.value}}
                )
                
                print(f"✅ Subscription cancelled: {agreement_id}")
                
                # TODO: Retirer du Telegram
                
        elif event_type == 'BILLING.SUBSCRIPTION.SUSPENDED':
            # Abonnement suspendu
            agreement_id = resource.get('id')
            
            subscription = await db.subscriptions.find_one({
                "paypalAgreementId": agreement_id
            })
            
            if subscription:
                await db.subscriptions.update_one(
                    {"id": subscription['id']},
                    {"$set": {
                        "status": SubscriptionStatus.PAST_DUE.value,
                        "updatedAt": datetime.now(timezone.utc).isoformat()
                    }}
                )
                
                print(f"⚠️ Subscription suspended: {agreement_id}")
                
        elif event_type == 'BILLING.SUBSCRIPTION.PAYMENT.FAILED':
            # Paiement échoué
            agreement_id = resource.get('id')
            print(f"❌ Payment failed for subscription: {agreement_id}")
            
            # TODO: Envoyer notification à l'utilisateur
            
        elif event_type == 'PAYMENT.SALE.COMPLETED':
            # Paiement complété (pour les formations et bot)
            sale_id = resource.get('id')
            print(f"✅ Payment completed: {sale_id}")
            
        elif event_type == 'PAYMENT.SALE.REFUNDED':
            # Remboursement
            sale_id = resource.get('id')
            print(f"💰 Payment refunded: {sale_id}")
        
        return {"status": "success", "event": event_type}
        
    except Exception as e:
        print(f"❌ Error processing PayPal webhook: {e}")
        # Retourner 200 quand même pour ne pas que PayPal réessaie indéfiniment
        return {"status": "error", "message": str(e)}


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

@router.get("/admin/all")
async def get_all_subscriptions_admin(current_user = Depends(require_admin)):
    """
    Récupérer tous les abonnements (ADMIN ONLY)
    """
    
    db = get_db()
    
    try:
        # Récupérer tous les abonnements
        subscriptions = list(db.subscriptions.find({}).sort("createdAt", -1))
        
        # Formater les données
        formatted_subs = []
        for sub in subscriptions:
            formatted_subs.append({
                "id": sub.get("id"),
                "userEmail": sub.get("userEmail"),
                "telegramUsername": sub.get("telegramUsername"),
                "paymentMethod": sub.get("paymentMethod", "stripe"),
                "status": sub.get("status"),
                "pricePerMonth": sub.get("pricePerMonth", 150.0),
                "createdAt": sub.get("createdAt"),
                "cancelAtPeriodEnd": sub.get("cancelAtPeriodEnd", False)
            })
        
        return formatted_subs
        
    except Exception as e:
        print(f"Error fetching subscriptions: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des abonnements")

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
    current_user = Depends(get_current_user)
):
    """
    Génère des liens d'invitation Telegram pour TOUS les canaux VIP
    """
    try:
        db = get_db()
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
