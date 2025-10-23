"""
Routes pour exécuter les migrations manuellement
"""
from fastapi import APIRouter, Depends, HTTPException
from pymongo import MongoClient
import os
import logging

router = APIRouter(prefix="/migrations", tags=["migrations"])
logger = logging.getLogger(__name__)

# Secret key pour sécuriser l'endpoint
MIGRATION_SECRET = os.environ.get('MIGRATION_SECRET', 'tradalife_migration_2024')

@router.get("/force-update-images")
async def force_update_images(secret: str):
    """
    Force la mise à jour des images des formations
    Utiliser avec: GET /api/migrations/force-update-images?secret=tradalife_migration_2024
    Accessible depuis le navigateur
    """
    if secret != MIGRATION_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    try:
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        DB_NAME = os.environ.get('DB_NAME', 'tradalife')
        logger.info(f"🔗 Connecting to MongoDB: {MONGO_URL}")
        
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        
        # État avant
        formations_before = list(db.formations.find({}, {"title": 1, "price": 1, "image": 1, "_id": 0}))
        logger.info(f"📋 Formations BEFORE: {formations_before}")
        
        # Supprimer formation 1799
        result_delete = db.formations.delete_many({"price": 1799.0})
        
        # Mettre à jour Ultra
        result_ultra = db.formations.update_many(
            {"price": 1100.0},
            {"$set": {"image": "https://i.imgur.com/0wGvLuk.jpg"}}
        )
        
        # Mettre à jour Premium
        result_premium = db.formations.update_many(
            {"price": 700.0},
            {"$set": {"image": "https://i.imgur.com/CcllRfh.jpg"}}
        )
        
        # État après
        formations_after = list(db.formations.find({}, {"title": 1, "price": 1, "image": 1, "_id": 0}))
        logger.info(f"📋 Formations AFTER: {formations_after}")
        
        client.close()
        
        return {
            "success": True,
            "message": "Images mises à jour avec succès",
            "details": {
                "deleted_1799": result_delete.deleted_count,
                "updated_ultra": result_ultra.modified_count,
                "updated_premium": result_premium.modified_count,
                "formations_before": formations_before,
                "formations_after": formations_after
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error during migration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Migration error: {str(e)}")
