"""
Routes pour voir les membres inscrits
"""
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db, require_admin
from models import User
import logging

router = APIRouter(prefix="/members", tags=["Members"])
logger = logging.getLogger(__name__)

@router.get("/all", dependencies=[Depends(require_admin)])
async def get_all_members(current_user: User = Depends(require_admin)):
    """
    Récupérer tous les membres inscrits (ADMIN ONLY)
    """
    db = get_db()
    
    try:
        # Récupérer tous les utilisateurs
        users = await db.users.find({}).to_list(10000)
        
        # Formater les données
        members = []
        for user in users:
            members.append({
                "id": user.get("id"),
                "firstName": user.get("firstName", ""),
                "lastName": user.get("lastName", ""),
                "email": user.get("email"),
                "role": user.get("role", "user"),
                "kycStatus": user.get("kycStatus", "not_submitted"),
                "createdAt": user.get("createdAt"),
                "telegramUsername": user.get("telegramUsername", "")
            })
        
        # Trier par date d'inscription (plus récent en premier)
        members_sorted = sorted(members, key=lambda x: x.get("createdAt", ""), reverse=True)
        
        logger.info(f"✅ Retrieved {len(members_sorted)} members")
        
        return {
            "total": len(members_sorted),
            "members": members_sorted
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching members: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des membres")

@router.get("/stats", dependencies=[Depends(require_admin)])
async def get_members_stats(current_user: User = Depends(require_admin)):
    """
    Statistiques sur les membres (ADMIN ONLY)
    """
    db = get_db()
    
    try:
        # Compter tous les utilisateurs
        total_users = await db.users.count_documents({})
        
        # Compter par rôle
        admins = await db.users.count_documents({"role": "admin"})
        regular_users = total_users - admins
        
        # Compter par statut KYC
        kyc_approved = await db.users.count_documents({"kycStatus": "approved"})
        kyc_pending = await db.users.count_documents({"kycStatus": "pending_review"})
        kyc_rejected = await db.users.count_documents({"kycStatus": "rejected"})
        kyc_not_submitted = await db.users.count_documents({"kycStatus": "not_submitted"})
        
        return {
            "total_users": total_users,
            "regular_users": regular_users,
            "admins": admins,
            "kyc_stats": {
                "approved": kyc_approved,
                "pending": kyc_pending,
                "rejected": kyc_rejected,
                "not_submitted": kyc_not_submitted
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching members stats: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des statistiques")
