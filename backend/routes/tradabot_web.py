"""
Backend API pour TRADABOT Web
Routes séparées pour éviter les conflits avec le reste du site
IMPORTANT: Accès uniquement pour les utilisateurs ayant payé le bot (300$ CAD)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from dependencies import get_current_user, get_db
from models import User, BotPreorderStatus
import os

router = APIRouter(prefix="/api/tradabot-web", tags=["tradabot-web"])
security = HTTPBearer(auto_error=False)

# Fonction pour vérifier si l'utilisateur a accès au bot
async def check_bot_access(current_user: User = Depends(get_current_user)):
    """Vérifie si l'utilisateur a payé le bot ou est admin"""
    db = get_db()
    
    # Admin a toujours accès
    if current_user.role.value == "admin":
        return current_user
    
    # Vérifier si l'utilisateur a une précommande payée
    preorder = await db.bot_preorders.find_one({
        "userId": current_user.id,
        "status": {"$in": [BotPreorderStatus.PAID.value, BotPreorderStatus.DELIVERED.value]}
    })
    
    if not preorder:
        raise HTTPException(
            status_code=403, 
            detail="Vous devez acheter le TRADABOT pour y accéder. Prix: 300$ CAD."
        )
    
    return current_user

# Models
class TradabotConfig(BaseModel):
    mt4Login: str
    mt4Password: str
    mt4Server: str
    channels: Dict[str, bool]
    lots: Dict[str, float]
    breakevenEnabled: bool

class BotToggle(BaseModel):
    status: str  # 'running' or 'stopped'

# Configuration
@router.get("/config")
async def get_config(current_user: User = Depends(check_bot_access)):
    """Récupère la configuration TRADABOT de l'utilisateur"""
    db = get_db()
    
    config = await db.tradabot_configs.find_one({"userId": current_user.id})
    
    if not config:
        # Configuration par défaut
        return {
            "mt4Login": "",
            "mt4Password": "",
            "mt4Server": "",
            "channels": {
                "forex": False,
                "crypto": False,
                "gold": False,
                "indices": False,
                "actions": False,
                "commodites": False
            },
            "lots": {
                "forex": 0.01,
                "crypto": 0.01,
                "gold": 0.01,
                "indices": 0.01,
                "actions": 0.01,
                "commodites": 0.01
            },
            "breakevenEnabled": True
        }
    
    # Retirer le _id de MongoDB
    config.pop('_id', None)
    config.pop('userId', None)
    
    return config

@router.post("/config")
async def save_config(config: TradabotConfig, current_user: User = Depends(check_bot_access)):
    """Sauvegarde la configuration TRADABOT"""
    db = get_db()
    
    config_dict = config.dict()
    config_dict['userId'] = current_user.id
    config_dict['updatedAt'] = datetime.utcnow().isoformat()
    
    await db.tradabot_configs.update_one(
        {"userId": current_user.id},
        {"$set": config_dict},
        upsert=True
    )
    
    return {"success": True, "message": "Configuration sauvegardée"}

# Signaux
@router.get("/signals")
async def get_signals(limit: int = 20, current_user: User = Depends(check_bot_access)):
    """Récupère les derniers signaux Telegram"""
    db = get_db()
    
    # Récupérer les signaux des dernières 24h
    signals = await db.telegram_signals.find().sort("timestamp", -1).limit(limit).to_list(length=limit)
    
    # Formater les signaux
    formatted_signals = []
    for signal in signals:
        formatted_signals.append({
            "type": signal.get("type", ""),
            "symbol": signal.get("symbol", ""),
            "entry": signal.get("entry", ""),
            "sl": signal.get("sl", ""),
            "tp1": signal.get("tp1", ""),
            "timestamp": signal.get("timestamp", "")
        })
    
    return formatted_signals

# Trades
@router.get("/trades")
async def get_trades(limit: int = 20, current_user: User = Depends(check_bot_access)):
    """Récupère l'historique des trades"""
    db = get_db()
    
    trades = await db.tradabot_trades.find(
        {"userId": current_user.id}
    ).sort("timestamp", -1).limit(limit).to_list(length=limit)
    
    # Formater les trades
    formatted_trades = []
    for trade in trades:
        formatted_trades.append({
            "type": trade.get("type", ""),
            "symbol": trade.get("symbol", ""),
            "lot": trade.get("lot", 0),
            "entry": trade.get("entry", 0),
            "status": trade.get("status", "open"),
            "profit": trade.get("profit", 0),
            "timestamp": trade.get("timestamp", "")
        })
    
    return formatted_trades

# Status du connecteur
@router.get("/connector-status")
async def get_connector_status(current_user: User = Depends(check_bot_access)):
    """Vérifie si le connecteur est en ligne"""
    db = get_db()
    
    # Vérifier le dernier heartbeat du connecteur
    connector = await db.tradabot_connectors.find_one(
        {"userId": current_user.id}
    )
    
    if not connector:
        return {
            "status": "disconnected",
            "botStatus": "stopped"
        }
    
    # Vérifier si le heartbeat est récent (moins de 30 secondes)
    last_seen = connector.get("lastSeen", "")
    if last_seen:
        try:
            last_seen_dt = datetime.fromisoformat(last_seen.replace('Z', '+00:00'))
            now = datetime.utcnow()
            diff = (now - last_seen_dt.replace(tzinfo=None)).total_seconds()
            
            if diff < 30:
                return {
                    "status": "connected",
                    "botStatus": connector.get("botStatus", "stopped")
                }
        except:
            pass
    
    return {
        "status": "disconnected",
        "botStatus": "stopped"
    }

# Toggle bot
@router.post("/toggle-bot")
async def toggle_bot(toggle: BotToggle, current_user: User = Depends(check_bot_access)):
    """Démarre ou arrête le bot"""
    db = get_db()
    
    # Mettre à jour le status dans la config
    await db.tradabot_configs.update_one(
        {"userId": current_user.id},
        {"$set": {"botStatus": toggle.status, "updatedAt": datetime.utcnow().isoformat()}},
        upsert=True
    )
    
    return {"success": True, "status": toggle.status}

# Heartbeat du connecteur
@router.post("/connector-heartbeat")
async def connector_heartbeat(heartbeat: dict, current_user: User = Depends(check_bot_access)):
    """Enregistre le heartbeat du connecteur"""
    db = get_db()
    
    await db.tradabot_connectors.update_one(
        {"userId": current_user.id},
        {"$set": {
            "userId": current_user.id,
            "lastSeen": heartbeat.get("lastSeen"),
            "botStatus": heartbeat.get("botStatus", "stopped"),
            "mt4Connected": heartbeat.get("mt4Connected", False)
        }},
        upsert=True
    )
    
    return {"success": True}

# Signaux en attente pour le connecteur
@router.get("/pending-signals")
async def get_pending_signals(current_user: User = Depends(check_bot_access)):
    """Retourne les signaux non encore tradés pour cet utilisateur"""
    db = get_db()
    
    # Récupérer la config pour voir quels canaux sont activés
    config = await db.tradabot_configs.find_one({"userId": current_user.id})
    
    if not config or config.get("botStatus") != "running":
        return []
    
    # Récupérer les signaux récents (dernière heure)
    from datetime import datetime, timedelta
    one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()
    
    signals = await db.telegram_signals.find({
        "timestamp": {"$gte": one_hour_ago}
    }).sort("timestamp", -1).limit(10).to_list(length=10)
    
    # Filtrer par canaux activés et signaux pas encore tradés
    pending = []
    for signal in signals:
        # Vérifier si le canal est activé
        channel = signal.get("channel", "").lower()
        if config.get("channels", {}).get(channel, False):
            # Vérifier si pas déjà tradé
            existing_trade = await db.tradabot_trades.find_one({
                "userId": current_user.id,
                "signalId": str(signal.get("_id"))
            })
            
            if not existing_trade:
                pending.append({
                    "id": str(signal.get("_id")),
                    "type": signal.get("type"),
                    "symbol": signal.get("symbol"),
                    "entry": signal.get("entry"),
                    "sl": signal.get("sl"),
                    "tp1": signal.get("tp1"),
                    "tp2": signal.get("tp2", ""),
                    "channel": signal.get("channel")
                })
    
    return pending

# Log trade
@router.post("/log-trade")
async def log_trade(trade_data: dict, current_user: User = Depends(check_bot_access)):
    """Enregistre un trade exécuté"""
    db = get_db()
    
    signal = trade_data.get("signal", {})
    
    trade_record = {
        "userId": current_user.id,
        "signalId": signal.get("id"),
        "type": signal.get("type"),
        "symbol": signal.get("symbol"),
        "lot": 0.01,  # Sera récupéré de la config
        "entry": float(signal.get("entry", 0)),
        "sl": float(signal.get("sl", 0)),
        "tp": float(signal.get("tp1", 0)),
        "ticket": trade_data.get("ticket"),
        "status": trade_data.get("status"),
        "profit": 0,
        "timestamp": trade_data.get("timestamp")
    }
    
    await db.tradabot_trades.insert_one(trade_record)
    
    return {"success": True}

# Télécharger le connecteur
@router.get("/download-connector")
async def download_connector(token: Optional[str] = None, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Télécharge le package du connecteur TRADABOT"""
    from auth_utils import decode_token
    
    # Essayer d'abord avec le token dans l'URL, sinon avec le header
    auth_token = token if token else (credentials.credentials if credentials else None)
    
    if not auth_token:
        raise HTTPException(status_code=401, detail="Token d'authentification requis")
    
    # Décoder le token
    payload = decode_token(auth_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token invalide")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")
    
    # Vérifier l'utilisateur
    db = get_db()
    user_dict = await db.users.find_one({"id": user_id})
    if not user_dict:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    
    user = User(**user_dict)
    
    # Vérifier l'accès au bot
    if user.role.value != "admin":
        preorder = await db.bot_preorders.find_one({
            "userId": user.id,
            "status": {"$in": [BotPreorderStatus.PAID.value, BotPreorderStatus.DELIVERED.value]}
        })
        
        if not preorder:
            raise HTTPException(
                status_code=403, 
                detail="Vous devez acheter le TRADABOT pour télécharger le connecteur."
            )
    
    # Vérifier que le fichier existe
    connector_path = "/app/tradabot-connector/TRADABOT_CONNECTOR_BUILD.zip"
    
    if not os.path.exists(connector_path):
        raise HTTPException(status_code=404, detail="Fichier connecteur introuvable")
    
    return FileResponse(
        path=connector_path,
        media_type="application/zip",
        filename="TRADABOT_CONNECTOR.zip",
        headers={
            "Content-Disposition": "attachment; filename=TRADABOT_CONNECTOR.zip",
            "Access-Control-Allow-Origin": "*"
        }
    )

# Liste des serveurs MT4/MT5
@router.get("/mt4-servers")
async def get_mt4_servers(current_user: User = Depends(check_bot_access)):
    """Retourne la liste des serveurs MT4/MT5 selon le rôle de l'utilisateur"""
    
    # Liste complète des serveurs (incluant démo et live)
    all_servers = [
        # Serveurs DÉMO (uniquement pour admin)
        "ICMarkets-Demo", "ICMarkets-Demo02", "ICMarkets-Demo03",
        "XM-Demo", "XM-Demo 2", "XM-Demo 3",
        "FXCM-USDDemo01", "FXCM-Demo",
        "Exness-Demo", "Exness-MT4Demo",
        
        # Serveurs LIVE (pour tous)
        "ICMarkets-Live", "ICMarkets-Live02", "ICMarkets-Live03",
        "XM-Real", "XM-Real 2", "XM-Real 3", "XM-Real 4",
        "FXCM-USDReal01", "FXCM-Real",
        "Exness-Real", "Exness-MT4Real", "Exness-MT4Real2",
        "Global-Prime", "Global-Prime-Live",
        "Pepperstone-Demo", "Pepperstone-Live", "Pepperstone-Live02",
        "FTMO-Demo", "FTMO-Live",
        "FBS-Real", "FBS-Real-2", "FBS-Real-MT4",
        "Tickmill-Live", "Tickmill-Live02",
        "HotForex-Real", "HotForex-Live",
        "OctaFX-Real", "OctaFX-Live",
        "RoboForex-Pro", "RoboForex-ProCent",
        "Admiral-Live", "Admiral-Real",
        "IG-Live", "IG-Real",
        "Plus500-Live",
        "eToro-Real",
        "AvaTrade-Live", "AvaTrade-Real",
        "OANDA-Live", "OANDA-fxTrade",
        "Forex.com-Live", "Forex.com-Real",
        "InteractiveBrokers-Live", "InteractiveBrokers-Pro",
        "Saxo-Live", "SaxoBank-Live",
        "CMC-Live", "CMCMarkets-Live"
    ]
    
    # Si admin, retourner tous les serveurs
    if current_user.role.value == "admin":
        return {"servers": all_servers}
    
    # Si client, retourner uniquement les serveurs LIVE (pas de "demo" dans le nom)
    live_servers = [s for s in all_servers if "demo" not in s.lower()]
    
    return {"servers": live_servers}
