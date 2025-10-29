"""
Backend API pour TRADABOT Web
Routes séparées pour éviter les conflits avec le reste du site
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from dependencies import get_current_user, get_db
from models import User
import os

router = APIRouter(prefix="/api/tradabot-web", tags=["tradabot-web"])

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
async def get_config(current_user: User = Depends(get_current_user)):
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
async def save_config(config: TradabotConfig, current_user: User = Depends(get_current_user)):
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
async def get_signals(limit: int = 20, current_user: User = Depends(get_current_user)):
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
async def get_trades(limit: int = 20, current_user: User = Depends(get_current_user)):
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
async def get_connector_status(current_user: User = Depends(get_current_user)):
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
async def toggle_bot(toggle: BotToggle, current_user: User = Depends(get_current_user)):
    """Démarre ou arrête le bot"""
    db = get_db()
    
    # Mettre à jour le status dans la config
    await db.tradabot_configs.update_one(
        {"userId": current_user.id},
        {"$set": {"botStatus": toggle.status, "updatedAt": datetime.utcnow().isoformat()}},
        upsert=True
    )
    
    return {"success": True, "status": toggle.status}

# Télécharger le connecteur
@router.get("/download-connector")
async def download_connector():
    """Télécharge le connecteur MT4 léger"""
    connector_path = "/app/tradabot-connector/TradabotConnector.exe"
    
    if not os.path.exists(connector_path):
        raise HTTPException(status_code=404, detail="Connecteur non disponible")
    
    return FileResponse(
        path=connector_path,
        media_type='application/octet-stream',
        filename='TradabotConnector.exe',
        headers={
            "Content-Disposition": "attachment; filename=TradabotConnector.exe"
        }
    )
