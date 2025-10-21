from fastapi import APIRouter, HTTPException
from models import Formation, TelegramLink
from dependencies import get_db
from typing import List

router = APIRouter(prefix="/formations", tags=["Formations"])

# Initial formations data
INITIAL_FORMATIONS = [
    {
        "id": "1",
        "title": "Formation Trading Crypto",
        "description": "Apprenez les bases du trading de cryptomonnaies avec nos experts. Stratégies, analyses techniques et gestion de risque.",
        "price": 299.0,
        "duration": "8 heures",
        "level": "Débutant",
        "image": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
        "videoCount": 12,
        "telegramLinks": [
            {"name": "Canal Crypto VIP", "url": "https://t.me/tradalife_crypto"},
            {"name": "Groupe Support", "url": "https://t.me/tradalife_support"}
        ]
    },
    {
        "id": "2",
        "title": "Formation Trading Forex",
        "description": "Maîtrisez le marché des devises. Apprenez à trader les paires de devises majeures et exotiques.",
        "price": 349.0,
        "duration": "10 heures",
        "level": "Intermédiaire",
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
        "videoCount": 15,
        "telegramLinks": [
            {"name": "Canal Forex VIP", "url": "https://t.me/tradalife_forex"},
            {"name": "Signaux Forex", "url": "https://t.me/tradalife_signaux"}
        ]
    },
    {
        "id": "3",
        "title": "Formation Trading Gold",
        "description": "Spécialisez-vous dans le trading de l'or. Stratégies avancées et analyses de marché.",
        "price": 399.0,
        "duration": "6 heures",
        "level": "Avancé",
        "image": "https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500",
        "videoCount": 10,
        "telegramLinks": [
            {"name": "Canal Gold VIP", "url": "https://t.me/tradalife_gold"}
        ]
    },
    {
        "id": "4",
        "title": "Formation Indices Boursiers",
        "description": "Trading sur les indices majeurs: CAC40, DAX, S&P500. Stratégies et timing parfait.",
        "price": 279.0,
        "duration": "7 heures",
        "level": "Intermédiaire",
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
        "videoCount": 11,
        "telegramLinks": [
            {"name": "Canal Indices VIP", "url": "https://t.me/tradalife_indices"}
        ]
    },
    {
        "id": "5",
        "title": "Pack Complet Trading",
        "description": "Toutes nos formations réunies: Crypto, Forex, Gold, Indices, Commodités et Actions.",
        "price": 999.0,
        "duration": "50+ heures",
        "level": "Tous niveaux",
        "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=500",
        "videoCount": 60,
        "telegramLinks": [
            {"name": "Tous les canaux VIP", "url": "https://t.me/tradalife_vip"},
            {"name": "Support Premium", "url": "https://t.me/tradalife_premium"}
        ]
    }
]

@router.on_event("startup")
async def init_formations():
    """Initialize formations in database if not exists"""
    # Cette fonction est désactivée car les formations sont gérées manuellement
    # Les formations sont insérées/mises à jour directement dans MongoDB
    pass

@router.get("", response_model=List[Formation])
async def get_formations():
    db = get_db()
    formations = await db.formations.find().to_list(100)
    return [Formation(**f) for f in formations]

@router.get("/{formation_id}", response_model=Formation)
async def get_formation(formation_id: str):
    db = get_db()
    formation = await db.formations.find_one({"id": formation_id})
    
    if not formation:
        raise HTTPException(status_code=404, detail="Formation not found")
    
    return Formation(**formation)