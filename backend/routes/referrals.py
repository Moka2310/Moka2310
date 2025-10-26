"""
Routes pour le système de parrainage
"""
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from datetime import datetime
import uuid
import os
import re
from typing import List

from models import Referral, ReferralCreate, ReferralStatus, User
from dependencies import get_db, get_current_user, require_admin
from email_service import EmailService

router = APIRouter(prefix="/referrals", tags=["Referrals"])

def generate_referral_code(user_name: str) -> str:
    """Génère un code de parrainage basé sur le nom d'utilisateur"""
    # Nettoyer le nom: minuscules, remplacer espaces par tirets, garder alphanumériques
    code = user_name.lower()
    code = re.sub(r'[^a-z0-9\s-]', '', code)
    code = re.sub(r'\s+', '-', code)
    # Ajouter 4 chiffres aléatoires pour unicité
    import random
    code = f"{code}-{random.randint(1000, 9999)}"
    return code

@router.get("/my-code")
async def get_my_referral_code(current_user: User = Depends(get_current_user)):
    """
    Récupérer le code de parrainage de l'utilisateur connecté
    """
    db = get_db()
    
    try:
        # Vérifier si l'utilisateur a déjà un code
        user = await db.users.find_one({"id": current_user.id})
        
        if user and user.get('referralCode'):
            referral_code = user['referralCode']
        else:
            # Générer un nouveau code
            user_name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or user.get('email').split('@')[0]
            referral_code = generate_referral_code(user_name)
            
            # Vérifier l'unicité
            existing = await db.users.find_one({"referralCode": referral_code})
            while existing:
                user_name = f"{user_name}-{uuid.uuid4().hex[:4]}"
                referral_code = generate_referral_code(user_name)
                existing = await db.users.find_one({"referralCode": referral_code})
            
            # Sauvegarder dans le profil utilisateur
            await db.users.update_one(
                {"id": current_user.id},
                {"$set": {"referralCode": referral_code}}
            )
        
        # Compter les parrainages
        total_referrals = await db.referrals.count_documents({"referrerId": current_user.id})
        pending_referrals = await db.referrals.count_documents({
            "referrerId": current_user.id,
            "status": ReferralStatus.PENDING
        })
        completed_referrals = await db.referrals.count_documents({
            "referrerId": current_user.id,
            "status": {"$in": [ReferralStatus.COMPLETED, ReferralStatus.REWARDED]}
        })
        
        # URL du frontend
        frontend_url = os.environ.get('REACT_APP_BACKEND_URL', 'https://tradalife.com').replace('/api', '')
        referral_link = f"{frontend_url}/register?ref={referral_code}"
        
        return {
            "referralCode": referral_code,
            "referralLink": referral_link,
            "stats": {
                "total": total_referrals,
                "pending": pending_referrals,
                "completed": completed_referrals
            }
        }
    except Exception as e:
        print(f"Error getting referral code: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-referrals")
async def get_my_referrals(current_user: User = Depends(get_current_user)):
    """
    Récupérer la liste des parrainages de l'utilisateur
    """
    db = get_db()
    
    try:
        referrals = await db.referrals.find({
            "referrerId": current_user.id
        }).sort("createdAt", -1).to_list(100)
        
        return [Referral(**ref) for ref in referrals]
    except Exception as e:
        print(f"Error getting referrals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/all")
async def get_all_referrals_admin(current_user: User = Depends(require_admin)):
    """
    Récupérer tous les parrainages (admin only)
    """
    db = get_db()
    
    try:
        referrals = await db.referrals.find().sort("createdAt", -1).to_list(1000)
        
        # Stats
        total = len(referrals)
        pending = len([r for r in referrals if r.get('status') == 'pending'])
        completed = len([r for r in referrals if r.get('status') in ['completed', 'rewarded']])
        total_reward = sum([r.get('rewardAmount', 200) for r in referrals if r.get('status') in ['completed', 'rewarded']])
        
        return {
            "referrals": [Referral(**ref) for ref in referrals],
            "stats": {
                "total": total,
                "pending": pending,
                "completed": completed,
                "totalRewardAmount": total_reward
            }
        }
    except Exception as e:
        print(f"Error getting all referrals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/mark-rewarded/{referral_id}")
async def mark_referral_rewarded(
    referral_id: str,
    current_user: User = Depends(require_admin)
):
    """
    Marquer un parrainage comme récompensé (admin only)
    """
    db = get_db()
    
    try:
        result = await db.referrals.update_one(
            {"id": referral_id},
            {"$set": {
                "status": ReferralStatus.REWARDED,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Parrainage introuvable")
        
        return {"success": True, "message": "Parrainage marqué comme récompensé"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error marking rewarded: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def check_and_complete_referral(user_id: str, purchase_type: str, purchase_amount: float):
    """
    Fonction utilitaire pour vérifier et compléter un parrainage lors d'un achat
    Appelée depuis les routes de paiement
    """
    db = get_db()
    
    try:
        # Vérifier si l'utilisateur a été parrainé
        user = await db.users.find_one({"id": user_id})
        if not user or not user.get('referredBy'):
            return
        
        referral_code = user.get('referredBy')
        
        # Trouver le parrain
        referrer = await db.users.find_one({"referralCode": referral_code})
        if not referrer:
            return
        
        # Vérifier si le parrainage existe et est en attente
        referral = await db.referrals.find_one({
            "referralCode": referral_code,
            "referredUserId": user_id,
            "status": ReferralStatus.PENDING
        })
        
        if not referral:
            return
        
        # Compléter le parrainage
        await db.referrals.update_one(
            {"id": referral['id']},
            {"$set": {
                "status": ReferralStatus.COMPLETED,
                "purchaseType": purchase_type,
                "purchaseAmount": purchase_amount,
                "completedAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }}
        )
        
        # Envoyer notification à l'admin
        admin_email = os.environ.get('ADMIN_EMAIL', 'yafoy2310@gmail.com')
        
        email_service = EmailService()
        subject = f"🎉 Nouveau Parrainage Complété - {referrer.get('email')}"
        body = f"""
        <h2>Nouveau Parrainage Complété!</h2>
        
        <p><strong>Parrain:</strong> {referrer.get('firstName', '')} {referrer.get('lastName', '')} ({referrer.get('email')})</p>
        <p><strong>Filleul:</strong> {user.get('firstName', '')} {user.get('lastName', '')} ({user.get('email')})</p>
        
        <p><strong>Type d'achat:</strong> {purchase_type}</p>
        <p><strong>Montant:</strong> {purchase_amount}$ CAD</p>
        
        <p><strong>Récompense à verser:</strong> 200$ CAD</p>
        
        <p>Connectez-vous au panneau admin pour marquer cette récompense comme versée.</p>
        """
        
        await email_service.send_email(admin_email, subject, body)
        
        # Marquer la notification comme envoyée
        await db.referrals.update_one(
            {"id": referral['id']},
            {"$set": {"adminNotified": True}}
        )
        
        print(f"✅ Referral completed: {referrer.get('email')} -> {user.get('email')} ({purchase_type}: {purchase_amount}$ CAD)")
        
    except Exception as e:
        print(f"❌ Error checking referral: {e}")
        # Ne pas lever d'exception pour ne pas bloquer le paiement
