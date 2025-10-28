from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime, timezone
import uuid

from models import (
    TradabotConfig, 
    TradabotConfigCreate,
    TradabotAccessGrant,
    BotStatus
)
from dependencies import get_current_user, get_db, get_current_admin

router = APIRouter(prefix="/tradabot", tags=["tradabot"])

@router.get("/access")
async def check_bot_access(current_user=Depends(get_current_user)):
    """
    Vérifie si l'utilisateur a accès au bot TRADABOT
    Accès si: a payé le bot OU admin lui a donné accès
    """
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier si configuration existe
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if config and config.get('hasAccess'):
            return {
                "hasAccess": True,
                "accessGrantedBy": config.get('accessGrantedBy'),
                "accessGrantedAt": config.get('accessGrantedAt')
            }
        
        # Vérifier si l'utilisateur a payé le bot
        bot_preorder = await db.bot_preorders.find_one({
            "userId": user_id,
            "status": "paid"
        })
        
        if bot_preorder:
            # Créer/Mettre à jour la config avec accès
            if not config:
                config = {
                    "id": str(uuid.uuid4()),
                    "userId": user_id,
                    "userEmail": current_user.email,
                    "hasAccess": True,
                    "accessGrantedBy": "payment",
                    "accessGrantedAt": datetime.now(timezone.utc).isoformat(),
                    "botStatus": BotStatus.INACTIVE.value,
                    "isConnected": False,
                    "lotForex": 0.01,
                    "lotCrypto": 0.01,
                    "lotGold": 0.01,
                    "lotIndices": 0.01,
                    "lotActions": 0.01,
                    "lotCommodites": 0.01,
                    "channelForexEnabled": True,
                    "channelCryptoEnabled": True,
                    "channelGoldEnabled": True,
                    "channelIndicesEnabled": True,
                    "channelActionsEnabled": True,
                    "channelCommoditesEnabled": True,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }
                await db.tradabot_configs.insert_one(config)
            else:
                await db.tradabot_configs.update_one(
                    {"userId": user_id},
                    {"$set": {
                        "hasAccess": True,
                        "accessGrantedBy": "payment",
                        "accessGrantedAt": datetime.now(timezone.utc).isoformat()
                    }}
                )
            
            return {
                "hasAccess": True,
                "accessGrantedBy": "payment",
                "accessGrantedAt": datetime.now(timezone.utc).isoformat()
            }
        
        return {"hasAccess": False}
        
    except Exception as e:
        print(f"Error checking bot access: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_bot_config(current_user=Depends(get_current_user)):
    """Récupère la configuration du bot pour l'utilisateur"""
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(
                status_code=403, 
                detail="Vous devez acheter TRADABOT pour y accéder"
            )
        
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if not config:
            raise HTTPException(status_code=404, detail="Configuration non trouvée")
        
        # Ne pas retourner le mot de passe
        if 'mt4Password' in config:
            config['mt4Password'] = "***" if config['mt4Password'] else None
        
        return TradabotConfig(**config)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def update_bot_config(
    config_data: TradabotConfigCreate,
    current_user=Depends(get_current_user)
):
    """Met à jour la configuration du bot"""
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(
                status_code=403,
                detail="Vous devez acheter TRADABOT pour y accéder"
            )
        
        # Préparer les données de mise à jour
        update_data = {
            "updatedAt": datetime.now(timezone.utc).isoformat()
        }
        
        # Ajouter uniquement les champs fournis
        config_dict = config_data.dict(exclude_unset=True)
        update_data.update(config_dict)
        
        # Mise à jour dans la DB
        result = await db.tradabot_configs.update_one(
            {"userId": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Configuration non trouvée")
        
        return {"success": True, "message": "Configuration mise à jour"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating bot config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/grant-access")
async def admin_grant_bot_access(
    grant_data: TradabotAccessGrant,
    current_admin=Depends(get_current_admin_user)
):
    """Admin donne ou retire l'accès au bot à un utilisateur"""
    try:
        db = get_db()
        user_id = grant_data.userId
        
        # Vérifier que l'utilisateur existe
        user = await db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Vérifier si config existe
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if not config:
            # Créer nouvelle config
            config = {
                "id": str(uuid.uuid4()),
                "userId": user_id,
                "userEmail": user.get('email'),
                "hasAccess": grant_data.grantAccess,
                "accessGrantedBy": "admin" if grant_data.grantAccess else None,
                "accessGrantedAt": datetime.now(timezone.utc).isoformat() if grant_data.grantAccess else None,
                "botStatus": BotStatus.INACTIVE.value,
                "isConnected": False,
                "lotForex": 0.01,
                "lotCrypto": 0.01,
                "lotGold": 0.01,
                "lotIndices": 0.01,
                "lotActions": 0.01,
                "lotCommodites": 0.01,
                "channelForexEnabled": True,
                "channelCryptoEnabled": True,
                "channelGoldEnabled": True,
                "channelIndicesEnabled": True,
                "channelActionsEnabled": True,
                "channelCommoditesEnabled": True,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }
            await db.tradabot_configs.insert_one(config)
        else:
            # Mettre à jour
            await db.tradabot_configs.update_one(
                {"userId": user_id},
                {"$set": {
                    "hasAccess": grant_data.grantAccess,
                    "accessGrantedBy": "admin" if grant_data.grantAccess else None,
                    "accessGrantedAt": datetime.now(timezone.utc).isoformat() if grant_data.grantAccess else None,
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        action = "donné" if grant_data.grantAccess else "retiré"
        return {
            "success": True,
            "message": f"Accès {action} pour l'utilisateur {user.get('email')}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error granting bot access: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_bot_status(current_user=Depends(get_current_user)):
    """Récupère le status du bot (actif, inactif, etc.)"""
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if not config:
            return {
                "status": BotStatus.INACTIVE.value,
                "isConnected": False,
                "message": "Configuration non trouvée"
            }
        
        return {
            "status": config.get('botStatus', BotStatus.INACTIVE.value),
            "isConnected": config.get('isConnected', False),
            "lastConnectionCheck": config.get('lastConnectionCheck')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting bot status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
