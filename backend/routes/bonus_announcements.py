"""
Routes pour gérer les annonces Bonus (carrousel)
"""
from fastapi import APIRouter, HTTPException, Depends
from pymongo import MongoClient
from datetime import datetime
import uuid
import os
from typing import List

from models import BonusAnnouncement, BonusAnnouncementCreate, BonusAnnouncementUpdate
from dependencies import get_db, require_admin

router = APIRouter(prefix="/bonus-announcements", tags=["Bonus Announcements"])

@router.get("/all", response_model=List[BonusAnnouncement])
async def get_all_announcements():
    """
    Récupérer toutes les annonces actives (public)
    """
    try:
        db = get_db()
        announcements = await db.bonus_announcements.find(
            {"isActive": True}
        ).sort("order", 1).to_list(100)
        
        return [BonusAnnouncement(**announcement) for announcement in announcements]
    except Exception as e:
        print(f"Error fetching announcements: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/all", response_model=List[BonusAnnouncement])
async def get_all_announcements_admin(current_user = Depends(require_admin)):
    """
    Récupérer toutes les annonces (admin only)
    """
    try:
        db = get_db()
        announcements = await db.bonus_announcements.find().sort("order", 1).to_list(100)
        
        return [BonusAnnouncement(**announcement) for announcement in announcements]
    except Exception as e:
        print(f"Error fetching announcements: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/create")
async def create_announcement(
    announcement_data: BonusAnnouncementCreate,
    current_user = Depends(require_admin)
):
    """
    Créer une nouvelle annonce (admin only)
    """
    try:
        db = get_db()
        
        announcement = BonusAnnouncement(
            id=str(uuid.uuid4()),
            titleFr=announcement_data.titleFr,
            titleEn=announcement_data.titleEn,
            descriptionFr=announcement_data.descriptionFr,
            descriptionEn=announcement_data.descriptionEn,
            imageUrl=announcement_data.imageUrl,
            linkUrl=announcement_data.linkUrl,
            order=announcement_data.order or 0,
            isActive=True,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        await db.bonus_announcements.insert_one(announcement.dict())
        
        return {
            "success": True,
            "message": "Annonce créée avec succès",
            "announcement": announcement
        }
    except Exception as e:
        print(f"Error creating announcement: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/admin/update/{announcement_id}")
async def update_announcement(
    announcement_id: str,
    announcement_data: BonusAnnouncementUpdate,
    current_user = Depends(require_admin)
):
    """
    Mettre à jour une annonce (admin only)
    """
    try:
        db = get_db()
        
        # Vérifier que l'annonce existe
        existing = await db.bonus_announcements.find_one({"id": announcement_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Annonce introuvable")
        
        # Préparer les données de mise à jour
        update_data = {k: v for k, v in announcement_data.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        await db.bonus_announcements.update_one(
            {"id": announcement_id},
            {"$set": update_data}
        )
        
        return {
            "success": True,
            "message": "Annonce mise à jour avec succès"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating announcement: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/admin/delete/{announcement_id}")
async def delete_announcement(
    announcement_id: str,
    current_user = Depends(require_admin)
):
    """
    Supprimer une annonce (admin only)
    """
    try:
        db = get_db()
        
        result = await db.bonus_announcements.delete_one({"id": announcement_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Annonce introuvable")
        
        return {
            "success": True,
            "message": "Annonce supprimée avec succès"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting announcement: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/toggle/{announcement_id}")
async def toggle_announcement(
    announcement_id: str,
    current_user = Depends(require_admin)
):
    """
    Activer/Désactiver une annonce (admin only)
    """
    try:
        db = get_db()
        
        announcement = await db.bonus_announcements.find_one({"id": announcement_id})
        if not announcement:
            raise HTTPException(status_code=404, detail="Annonce introuvable")
        
        new_status = not announcement.get("isActive", True)
        
        await db.bonus_announcements.update_one(
            {"id": announcement_id},
            {"$set": {
                "isActive": new_status,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        return {
            "success": True,
            "message": f"Annonce {'activée' if new_status else 'désactivée'} avec succès",
            "isActive": new_status
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error toggling announcement: {e}")
        raise HTTPException(status_code=500, detail=str(e))
