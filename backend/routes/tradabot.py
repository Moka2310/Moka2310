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
    Accès si: email est yafoy2310@gmail.com OU a payé le bot OU admin lui a donné accès
    """
    try:
        db = get_db()
        user_id = current_user.id
        user_email = current_user.email
        
        # Si l'utilisateur est le super admin (yafoy2310@gmail.com), accès automatique
        if user_email == "yafoy2310@gmail.com":
            # Créer/Mettre à jour la config avec accès super admin
            config = await db.tradabot_configs.find_one({"userId": user_id})
            
            if not config:
                config = {
                    "id": str(uuid.uuid4()),
                    "userId": user_id,
                    "userEmail": user_email,
                    "hasAccess": True,
                    "accessGrantedBy": "super_admin",
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
                        "accessGrantedBy": "super_admin",
                        "accessGrantedAt": datetime.now(timezone.utc).isoformat()
                    }}
                )
            
            return {
                "hasAccess": True,
                "accessGrantedBy": "super_admin",
                "accessGrantedAt": datetime.now(timezone.utc).isoformat(),
                "isSuperAdmin": True
            }
        
        # Vérifier si configuration existe
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if config and config.get('hasAccess'):
            return {
                "hasAccess": True,
                "accessGrantedBy": config.get('accessGrantedBy'),
                "accessGrantedAt": config.get('accessGrantedAt'),
                "isSuperAdmin": False
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
                    "userEmail": user_email,
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
                "accessGrantedAt": datetime.now(timezone.utc).isoformat(),
                "isSuperAdmin": False
            }
        
        return {"hasAccess": False, "isSuperAdmin": False}
        
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
        
        # Ne pas retourner le mot de passe et retirer _id MongoDB
        if '_id' in config:
            del config['_id']
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
    current_admin=Depends(get_current_admin)
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

@router.get("/admin/users")
async def list_users_with_access(current_admin=Depends(get_current_admin)):
    """Liste tous les utilisateurs avec leur statut d'accès TRADABOT"""
    try:
        db = get_db()
        
        # Récupérer tous les utilisateurs
        users = await db.users.find({}).to_list(length=None)
        
        # Récupérer toutes les configs TRADABOT
        configs = await db.tradabot_configs.find({}).to_list(length=None)
        configs_dict = {c['userId']: c for c in configs}
        
        # Récupérer tous les paiements bot
        bot_preorders = await db.bot_preorders.find({"status": "paid"}).to_list(length=None)
        paid_users = {p['userId'] for p in bot_preorders}
        
        users_list = []
        for user in users:
            user_id = user.get('id')
            config = configs_dict.get(user_id, {})
            has_paid = user_id in paid_users
            is_admin = user.get('role') == 'admin'
            
            users_list.append({
                "userId": user_id,
                "email": user.get('email'),
                "firstName": user.get('firstName', ''),
                "lastName": user.get('lastName', ''),
                "isAdmin": is_admin,
                "hasPaid": has_paid,
                "hasAccess": config.get('hasAccess', False) or is_admin or has_paid,
                "accessGrantedBy": config.get('accessGrantedBy') if config else ('admin_auto' if is_admin else ('payment' if has_paid else None)),
                "accessGrantedAt": config.get('accessGrantedAt')
            })
        
        return {"users": users_list}
        
    except Exception as e:
        print(f"Error listing users: {e}")
        raise HTTPException(status_code=500, detail=str(e))
