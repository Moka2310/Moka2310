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

from enum import Enum

class BotStatus(str, Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    ERROR = "error"

@router.post("/mt4/connect")
async def connect_mt4(
    mt4_data: dict,
    current_user=Depends(get_current_user)
):
    """
    Connecter MT4/MT5
    mt4_data: {
        "login": int,
        "password": str,
        "server": str,
        "platform": "MT4" ou "MT5"
    }
    """
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Récupérer ou créer la config
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if not config:
            # Créer une nouvelle config
            config = {
                "id": str(uuid.uuid4()),
                "userId": user_id,
                "mt4Login": mt4_data.get('login'),
                "mt4Server": mt4_data.get('server'),
                "mt4Platform": mt4_data.get('platform', 'MT4'),
                "mt4Connected": False,  # Sera True quand vraiment connecté
                "mt4ConnectionTest": True,  # Pour indiquer qu'on a essayé
                "channelForexEnabled": True,
                "channelCryptoEnabled": True,
                "channelGoldEnabled": True,
                "channelIndicesEnabled": True,
                "channelActionsEnabled": True,
                "channelCommoditesEnabled": True,
                "lotForex": 0.01,
                "lotCrypto": 0.01,
                "lotGold": 0.01,
                "lotIndices": 0.01,
                "lotActions": 0.01,
                "lotCommodites": 0.01,
                "breakevenEnabled": True,
                "botActive": False,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }
            await db.tradabot_configs.insert_one(config)
        else:
            # Mettre à jour
            await db.tradabot_configs.update_one(
                {"userId": user_id},
                {"$set": {
                    "mt4Login": mt4_data.get('login'),
                    "mt4Server": mt4_data.get('server'),
                    "mt4Platform": mt4_data.get('platform', 'MT4'),
                    "mt4ConnectionTest": True,
                    "updatedAt": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        return {
            "success": True,
            "message": "Configuration MT4 sauvegardée",
            "note": "La connexion réelle nécessite l'application desktop Windows"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error connecting MT4: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bot/start")
async def start_bot(current_user=Depends(get_current_user)):
    """Démarre le bot de trading"""
    try:
        db = get_db()
        user_id = current_user.id
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Mettre à jour le statut
        config = await db.tradabot_configs.find_one({"userId": user_id})
        
        if not config:
            raise HTTPException(status_code=404, detail="Configuration non trouvée. Configurez d'abord le bot.")
        
        await db.tradabot_configs.update_one(
            {"userId": user_id},
            {"$set": {
                "botActive": True,
                "botStatus": BotStatus.ACTIVE.value,
                "lastStartedAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "message": "Bot démarré",
            "status": BotStatus.ACTIVE.value
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error starting bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bot/stop")
async def stop_bot(current_user=Depends(get_current_user)):
    """Arrête le bot de trading"""
    try:
        db = get_db()
        user_id = current_user.id
        
        # Mettre à jour le statut
        await db.tradabot_configs.update_one(
            {"userId": user_id},
            {"$set": {
                "botActive": False,
                "botStatus": BotStatus.INACTIVE.value,
                "lastStoppedAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "message": "Bot arrêté",
            "status": BotStatus.INACTIVE.value
        }
        
    except Exception as e:
        print(f"Error stopping bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/signals/live")
async def get_live_signals(
    limit: int = 50,
    current_user=Depends(get_current_user)
):
    """Récupère les derniers signaux en temps réel"""
    try:
        db = get_db()
        
        # Vérifier l'accès
        access_check = await check_bot_access(current_user)
        if not access_check.get('hasAccess'):
            raise HTTPException(status_code=403, detail="Accès refusé")
        
        # Récupérer les signaux récents
        signals = await db.trade_signals.find().sort("createdAt", -1).limit(limit).to_list(length=limit)
        
        # Nettoyer les _id MongoDB
        for signal in signals:
            if '_id' in signal:
                del signal['_id']
        
        return {
            "signals": signals,
            "count": len(signals)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def get_bot_status(current_user=Depends(get_current_user)):
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
