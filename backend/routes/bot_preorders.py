"""
Routes pour les précommandes du bot de copy trading
"""
from fastapi import APIRouter, HTTPException, Depends
from models import BotPreorder, BotPreorderCreate, BotPreorderResponse, BotPreorderStatus, User
from dependencies import get_db, get_current_user, require_admin
from datetime import datetime
import uuid
import logging

router = APIRouter(prefix="/bot-preorders", tags=["Bot Preorders"])
logger = logging.getLogger(__name__)

@router.post("/create", response_model=dict)
async def create_bot_preorder(
    preorder_data: BotPreorderCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Créer une précommande de bot
    Nécessite que l'utilisateur soit connecté
    Supporte Stripe et PayPal
    """
    db = get_db()
    
    try:
        # Vérifier la disponibilité (limite de 30 précommandes)
        total_preorders = await db.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        if total_preorders >= 30:
            raise HTTPException(
                status_code=400,
                detail="Toutes les précommandes ont été vendues. Merci de votre intérêt!"
            )
        
        # Vérifier si l'utilisateur a déjà une précommande active
        existing_preorder = await db.bot_preorders.find_one({
            "userId": current_user.id,
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        if existing_preorder:
            raise HTTPException(
                status_code=400,
                detail="Vous avez déjà une précommande active"
            )
        
        # Créer la précommande
        preorder = BotPreorder(
            id=str(uuid.uuid4()),
            userId=current_user.id,
            userEmail=current_user.email,
            price=300.0,
            status=BotPreorderStatus.PENDING_PAYMENT,
            paymentMethod=preorder_data.paymentMethod,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        await db.bot_preorders.insert_one(preorder.dict())
        
        logger.info(f"✅ Bot preorder created for user {current_user.email}: {preorder.id}")
        
        # Gérer le paiement selon la méthode choisie
        if preorder_data.paymentMethod == "stripe":
            # Import Stripe payment service
            from payment_service import StripePayment
            
            payment_result = await StripePayment.create_payment_intent(
                amount=300.0,
                currency="cad",
                metadata={
                    "preorder_id": preorder.id,
                    "user_id": current_user.id,
                    "type": "bot_preorder"
                }
            )
            
            if payment_result["success"]:
                # Update preorder with payment intent ID
                await db.bot_preorders.update_one(
                    {"id": preorder.id},
                    {"$set": {"stripePaymentIntentId": payment_result["payment_intent_id"]}}
                )
                
                return {
                    "preorderId": preorder.id,
                    "price": preorder.price,
                    "status": preorder.status,
                    "clientSecret": payment_result["client_secret"],
                    "paymentMethod": "stripe",
                    "message": "Précommande créée avec succès"
                }
            else:
                # Delete preorder if payment failed
                await db.bot_preorders.delete_one({"id": preorder.id})
                raise HTTPException(status_code=400, detail=f"Erreur Stripe: {payment_result['error']}")
        
        elif preorder_data.paymentMethod == "paypal":
            # Import PayPal payment service
            from payment_service import PayPalPayment
            
            payment_result = await PayPalPayment.create_payment(
                amount=300.0,
                currency="CAD",
                description="Pré-commande Bot de Copy Trading MT4 - Tradalife"
            )
            
            if payment_result["success"]:
                # Update preorder with PayPal payment ID
                await db.bot_preorders.update_one(
                    {"id": preorder.id},
                    {"$set": {"paypalPaymentId": payment_result["payment_id"]}}
                )
                
                return {
                    "preorderId": preorder.id,
                    "price": preorder.price,
                    "status": preorder.status,
                    "approvalUrl": payment_result["approval_url"],
                    "paymentMethod": "paypal",
                    "message": "Précommande créée avec succès"
                }
            else:
                # Delete preorder if payment failed
                await db.bot_preorders.delete_one({"id": preorder.id})
                raise HTTPException(status_code=400, detail=f"Erreur PayPal: {payment_result['error']}")
        
        else:
            await db.bot_preorders.delete_one({"id": preorder.id})
            raise HTTPException(status_code=400, detail="Méthode de paiement non supportée")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating bot preorder: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la précommande: {str(e)}")


@router.get("/initialize-fake-preorders")
async def initialize_fake_preorders(secret: str):
    """
    Créer 21 précommandes factices pour afficher 9/30 disponibles
    Utiliser avec: GET /api/bot-preorders/initialize-fake-preorders?secret=tradalife_init_2024
    """
    if secret != "tradalife_init_2024":
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    db = get_db()
    
    try:
        # Compter les précommandes existantes
        current_count = await db.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        # Créer 21 précommandes factices au total
        target_count = 21
        preorders_to_create = target_count - current_count
        
        if preorders_to_create <= 0:
            return {
                "success": True,
                "message": f"Déjà {current_count} précommandes. Aucune création nécessaire.",
                "current_sold": current_count,
                "available": 30 - current_count
            }
        
        # Créer les précommandes factices
        from datetime import datetime
        import uuid
        
        for i in range(preorders_to_create):
            fake_preorder = {
                "id": str(uuid.uuid4()),
                "userId": f"fake_user_{current_count + i}",
                "userEmail": f"fake_{current_count + i}@example.com",
                "price": 300.0,
                "status": "paid",
                "paymentMethod": "stripe",
                "stripePaymentIntentId": f"fake_pi_{current_count + i}",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
            await db.bot_preorders.insert_one(fake_preorder)
        
        final_count = await db.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        logger.info(f"✅ Created {preorders_to_create} fake preorders. Total: {final_count}")
        
        return {
            "success": True,
            "message": f"{preorders_to_create} précommandes factices créées",
            "preorders_created": preorders_to_create,
            "total_sold": final_count,
            "available": 30 - final_count
        }
        
    except Exception as e:
        logger.error(f"❌ Error creating fake preorders: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/availability")
async def get_preorder_availability():
    """
    Récupérer le nombre de précommandes disponibles (limite: 30)
    FORCE: Affiche toujours maximum 9 disponibles pour créer l'urgence
    Accessible sans authentification
    """
    db = get_db()
    
    try:
        # Compter les précommandes payées ou en attente de paiement
        total_preorders = await db.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        max_preorders = 30
        actual_available = max(0, max_preorders - total_preorders)
        
        # FORCER: Maximum 9 disponibles affichés (21 minimum vendus)
        # Cela crée l'urgence même si la BD n'a pas encore les précommandes factices
        min_sold = 21
        displayed_sold = max(min_sold, total_preorders)
        displayed_available = max_preorders - displayed_sold
        
        logger.info(f"📊 Bot availability: actual_sold={total_preorders}, displayed_sold={displayed_sold}, displayed_available={displayed_available}")
        
        return {
            "total": max_preorders,
            "sold": displayed_sold,
            "available": displayed_available,
            "is_available": displayed_available > 0
        }
    except Exception as e:
        logger.error(f"❌ Error fetching preorder availability: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de la disponibilité")


@router.get("/my-preorders", response_model=list[BotPreorderResponse])
async def get_my_preorders(current_user: User = Depends(get_current_user)):
    """
    Récupérer les précommandes de l'utilisateur connecté
    """
    db = get_db()
    
    try:
        preorders = await db.bot_preorders.find({"userId": current_user.id}).to_list(100)
        return [BotPreorderResponse(**preorder) for preorder in preorders]
    except Exception as e:
        logger.error(f"❌ Error fetching user preorders: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des précommandes")


@router.get("/status/{preorder_id}")
async def get_preorder_status(
    preorder_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Vérifier le statut d'une précommande
    """
    db = get_db()
    
    try:
        preorder = await db.bot_preorders.find_one({"id": preorder_id})
        
        if not preorder:
            raise HTTPException(status_code=404, detail="Précommande introuvable")
        
        # Vérifier que la précommande appartient à l'utilisateur
        if preorder.get("userId") != current_user.id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        return {
            "id": preorder.get("id"),
            "status": preorder.get("status"),
            "price": preorder.get("price"),
            "createdAt": preorder.get("createdAt"),
            "deliveredAt": preorder.get("deliveredAt"),
            "downloadLink": preorder.get("downloadLink")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching preorder status: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du statut")


@router.post("/confirm-payment/{preorder_id}")
async def confirm_preorder_payment(
    preorder_id: str,
    payment_intent_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Confirmer le paiement d'une précommande (appelé après succès Stripe)
    """
    db = get_db()
    
    try:
        preorder = await db.bot_preorders.find_one({"id": preorder_id})
        
        if not preorder:
            raise HTTPException(status_code=404, detail="Précommande introuvable")
        
        if preorder.get("userId") != current_user.id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Mettre à jour le statut
        await db.bot_preorders.update_one(
            {"id": preorder_id},
            {
                "$set": {
                    "status": BotPreorderStatus.PAID,
                    "stripePaymentIntentId": payment_intent_id,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"✅ Bot preorder {preorder_id} payment confirmed")
        
        # TODO: Envoyer email de confirmation
        
        return {
            "success": True,
            "message": "Paiement confirmé ! Vous recevrez le bot par email dès qu'il sera disponible."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error confirming payment: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la confirmation du paiement")


@router.post("/confirm-paypal-payment/{preorder_id}")
async def confirm_paypal_preorder_payment(
    preorder_id: str,
    payer_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Confirmer le paiement PayPal d'une précommande (appelé après approbation PayPal)
    """
    db = get_db()
    
    try:
        preorder = await db.bot_preorders.find_one({"id": preorder_id})
        
        if not preorder:
            raise HTTPException(status_code=404, detail="Précommande introuvable")
        
        if preorder.get("userId") != current_user.id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Exécuter le paiement PayPal
        from payment_service import PayPalPayment
        
        payment_id = preorder.get("paypalPaymentId")
        if not payment_id:
            raise HTTPException(status_code=400, detail="ID de paiement PayPal introuvable")
        
        payment_result = await PayPalPayment.execute_payment(payment_id, payer_id)
        
        if payment_result["success"]:
            # Mettre à jour le statut
            await db.bot_preorders.update_one(
                {"id": preorder_id},
                {
                    "$set": {
                        "status": BotPreorderStatus.PAID,
                        "updatedAt": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"✅ Bot preorder {preorder_id} PayPal payment confirmed")
            
            # TODO: Envoyer email de confirmation
            
            return {
                "success": True,
                "message": "Paiement PayPal confirmé ! Vous recevrez le bot par email dès qu'il sera disponible."
            }
        else:
            raise HTTPException(status_code=400, detail=f"Erreur PayPal: {payment_result['error']}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error confirming PayPal payment: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la confirmation du paiement PayPal")


@router.get("/admin/all")
async def get_all_preorders_admin(current_user: User = Depends(require_admin)):
    """
    Récupérer toutes les précommandes (admin only)
    """
    db = get_db()
    
    try:
        # Récupérer toutes les précommandes
        preorders = await db.bot_preorders.find().to_list(1000)
        
        # Exclure les fausses précommandes (celles avec fake_user)
        real_preorders = [
            p for p in preorders 
            if not p.get('userId', '').startswith('fake_user')
        ]
        
        # Calculer les statistiques
        total_real = len(real_preorders)
        paid_count = len([p for p in real_preorders if p.get('status') == 'paid'])
        pending_count = len([p for p in real_preorders if p.get('status') == 'pending_payment'])
        total_revenue = sum([p.get('price', 0) for p in real_preorders if p.get('status') == 'paid'])
        
        logger.info(f"📊 Admin preorders: {total_real} total, {paid_count} paid, {pending_count} pending")
        
        return {
            "preorders": real_preorders,
            "stats": {
                "total": total_real,
                "paid": paid_count,
                "pending": pending_count,
                "revenue": total_revenue
            }
        }
    except Exception as e:
        logger.error(f"❌ Error fetching admin preorders: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des précommandes")
