"""
Routes pour l'intégration Telegram
"""
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencies import get_db
from telegram_service import telegram_service
from pydantic import BaseModel
from datetime import datetime, timezone
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/telegram", tags=["telegram"])

class TelegramConfigUpdate(BaseModel):
    chat_id: str

@router.get("/member-count")
async def get_telegram_member_count(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Récupère le nombre de membres Telegram (depuis le cache ou l'API)
    """
    try:
        # Récupérer depuis le cache MongoDB
        cached_data = await db.telegram_stats.find_one({"type": "member_count"})
        
        if cached_data:
            return {
                "count": cached_data.get("count", 4000),
                "last_updated": cached_data.get("last_updated"),
                "source": "cache"
            }
        
        # Si pas de cache, retourner valeur par défaut
        return {
            "count": 4000,
            "last_updated": None,
            "source": "default"
        }
        
    except Exception as e:
        logger.error(f"Error getting member count: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get member count")

@router.post("/sync-members")
async def sync_telegram_members(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Synchronise manuellement le nombre de membres depuis Telegram
    """
    try:
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not chat_id:
            raise HTTPException(
                status_code=400, 
                detail="TELEGRAM_CHAT_ID not configured. Please add your group/channel ID in .env"
            )
        
        # Récupérer le nombre de membres depuis l'API Telegram
        member_count = await telegram_service.get_chat_member_count(chat_id)
        
        if member_count is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch member count from Telegram. Check bot permissions."
            )
        
        # Mettre à jour dans MongoDB
        await db.telegram_stats.update_one(
            {"type": "member_count"},
            {
                "$set": {
                    "count": member_count,
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "chat_id": chat_id
                }
            },
            upsert=True
        )
        
        return {
            "success": True,
            "count": member_count,
            "message": "Member count synced successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing members: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@router.post("/update-chat-id")
async def update_telegram_chat_id(
    config: TelegramConfigUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Met à jour le chat_id Telegram dans la configuration
    """
    try:
        # Tester si le bot a accès au chat
        chat_info = await telegram_service.get_chat_info(config.chat_id)
        
        if not chat_info:
            raise HTTPException(
                status_code=400,
                detail="Cannot access this chat. Make sure the bot is added as admin."
            )
        
        # Sauvegarder dans MongoDB
        await db.settings.update_one(
            {"key": "telegram_chat_id"},
            {
                "$set": {
                    "value": config.chat_id,
                    "chat_title": chat_info.get("title", ""),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
            },
            upsert=True
        )
        
        return {
            "success": True,
            "chat_id": config.chat_id,
            "chat_title": chat_info.get("title"),
            "message": "Chat ID configured successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chat ID: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")

@router.get("/chat-info")
async def get_telegram_chat_info():
    """
    Récupère les informations du groupe Telegram configuré
    """
    try:
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not chat_id:
            raise HTTPException(
                status_code=400,
                detail="TELEGRAM_CHAT_ID not configured"
            )
        
        chat_info = await telegram_service.get_chat_info(chat_id)
        
        if not chat_info:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch chat info"
            )
        
        return {
            "chat_id": chat_id,
            "title": chat_info.get("title"),
            "type": chat_info.get("type"),
            "description": chat_info.get("description", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
