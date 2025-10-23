"""
Routes pour les précommandes du bot de copy trading
"""
from fastapi import APIRouter, HTTPException, Depends
from models import BotPreorder, BotPreorderCreate, BotPreorderResponse, BotPreorderStatus, User
from dependencies import get_db, get_current_user
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
        
        # Pour l'instant, on retourne juste l'ID de précommande
        # Le paiement Stripe sera géré côté frontend
        return {
            "preorderId": preorder.id,
            "price": preorder.price,
            "status": preorder.status,
            "message": "Précommande créée avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating bot preorder: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la précommande: {str(e)}")


@router.get("/availability")
async def get_preorder_availability():
    """
    Récupérer le nombre de précommandes disponibles (limite: 30)
    Accessible sans authentification
    """
    db = get_db()
    
    try:
        # Compter les précommandes payées ou en attente de paiement
        total_preorders = await db.bot_preorders.count_documents({
            "status": {"$in": ["pending_payment", "paid"]}
        })
        
        max_preorders = 30
        available = max(0, max_preorders - total_preorders)
        
        return {
            "total": max_preorders,
            "sold": total_preorders,
            "available": available,
            "is_available": available > 0
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
