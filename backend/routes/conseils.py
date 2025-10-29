"""
Routes pour gérer les conseils TRADABOT depuis le panel admin
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from dependencies import get_current_user, get_db
from models import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/conseils", tags=["conseils"])

class CapitalManagement(BaseModel):
    capital: str
    forex: str
    crypto: str
    gold: str
    indices: str
    actions: str
    risque: str
    color: str

class InstallationStep(BaseModel):
    numero: str
    titre: str
    description: str
    icon: str

class TradingTip(BaseModel):
    titre: str
    description: str
    iconColor: str

class FAQItem(BaseModel):
    question: str
    reponse: str

class ConseilsContent(BaseModel):
    capitalManagement: List[CapitalManagement]
    installationSteps: List[InstallationStep]
    tradingTips: List[TradingTip]
    faq: List[FAQItem]

@router.get("/content")
async def get_conseils_content():
    """Récupérer le contenu de la page Conseils"""
    db = get_db()
    
    try:
        # Récupérer le contenu depuis la DB
        content = await db.conseils_content.find_one({})
        
        if not content:
            # Retourner le contenu par défaut si rien en DB
            return get_default_content()
        
        # Retirer le _id de MongoDB
        content.pop('_id', None)
        return content
        
    except Exception as e:
        logger.error(f"Erreur récupération conseils: {e}")
        return get_default_content()

@router.post("/content")
async def update_conseils_content(
    content: ConseilsContent,
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour le contenu de la page Conseils (Admin seulement)"""
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    db = get_db()
    
    try:
        # Convertir en dict
        content_dict = content.dict()
        
        # Upsert dans la DB
        await db.conseils_content.update_one(
            {},
            {"$set": content_dict},
            upsert=True
        )
        
        logger.info(f"Conseils mis à jour par {current_user.email}")
        return {"success": True, "message": "Contenu mis à jour avec succès"}
        
    except Exception as e:
        logger.error(f"Erreur mise à jour conseils: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour")

def get_default_content():
    """Contenu par défaut de la page Conseils"""
    return {
        "capitalManagement": [
            {
                "capital": "500$ - 1,000$",
                "forex": "0.01",
                "crypto": "0.01",
                "gold": "0.01",
                "indices": "0.01",
                "actions": "0.01",
                "risque": "Très faible",
                "color": "from-green-500 to-emerald-600"
            },
            {
                "capital": "1,000$ - 2,500$",
                "forex": "0.02",
                "crypto": "0.01",
                "gold": "0.02",
                "indices": "0.02",
                "actions": "0.02",
                "risque": "Faible",
                "color": "from-blue-500 to-cyan-600"
            },
            {
                "capital": "2,500$ - 5,000$",
                "forex": "0.05",
                "crypto": "0.02",
                "gold": "0.03",
                "indices": "0.03",
                "actions": "0.03",
                "risque": "Modéré",
                "color": "from-yellow-500 to-orange-600"
            },
            {
                "capital": "5,000$ - 10,000$",
                "forex": "0.10",
                "crypto": "0.05",
                "gold": "0.08",
                "indices": "0.08",
                "actions": "0.08",
                "risque": "Équilibré",
                "color": "from-purple-500 to-pink-600"
            },
            {
                "capital": "10,000$+",
                "forex": "0.20",
                "crypto": "0.10",
                "gold": "0.15",
                "indices": "0.15",
                "actions": "0.15",
                "risque": "Agressif",
                "color": "from-red-500 to-rose-600"
            }
        ],
        "installationSteps": [
            {
                "numero": "1",
                "titre": "Achat du TRADABOT",
                "description": "Commandez le TRADABOT sur la page d'accueil pour 300$ CAD (paiement unique).",
                "icon": "DollarSign"
            },
            {
                "numero": "2",
                "titre": "Accès à l'interface",
                "description": "Une fois le paiement validé, accédez à /tradabot-web depuis votre tableau de bord.",
                "icon": "CheckCircle2"
            },
            {
                "numero": "3",
                "titre": "Télécharger le connecteur",
                "description": "Cliquez sur \"📥 Télécharger le Connecteur\" et sauvegardez le fichier ZIP.",
                "icon": "Download"
            },
            {
                "numero": "4",
                "titre": "Extraire et installer",
                "description": "Dézippez le fichier, exécutez TRADABOT_CONNECTOR.exe sur votre ordinateur Windows.",
                "icon": "BookOpen"
            },
            {
                "numero": "5",
                "titre": "Configuration MT4",
                "description": "Dans l'onglet Configuration, entrez vos identifiants MT4 (login, password, serveur).",
                "icon": "Shield"
            },
            {
                "numero": "6",
                "titre": "Choisir les lots",
                "description": "Configurez les lots selon votre capital (voir tableau ci-dessous).",
                "icon": "TrendingUp"
            },
            {
                "numero": "7",
                "titre": "Activer les canaux",
                "description": "Sélectionnez les canaux Telegram que vous souhaitez copier (Forex, Crypto, Gold, etc.).",
                "icon": "CheckCircle2"
            },
            {
                "numero": "8",
                "titre": "Lancer le bot",
                "description": "Cliquez sur \"▶ DÉMARRER LE BOT\" et laissez le connecteur tourner en arrière-plan.",
                "icon": "CheckCircle2"
            }
        ],
        "tradingTips": [
            {
                "titre": "Ne jamais risquer plus de 2% par trade",
                "description": "La règle d'or du money management. Même avec des signaux de qualité, le risque doit être maîtrisé.",
                "iconColor": "text-yellow-400"
            },
            {
                "titre": "Utilisez un compte RÉEL (pas DEMO)",
                "description": "Les clients doivent obligatoirement connecter un compte réel pour une exécution optimale des ordres.",
                "iconColor": "text-blue-400"
            },
            {
                "titre": "Laissez le connecteur actif 24/7",
                "description": "Pour ne manquer aucun signal, gardez votre ordinateur allumé avec le connecteur en marche.",
                "iconColor": "text-green-400"
            },
            {
                "titre": "Activez le Breakeven automatique",
                "description": "Cette option sécurise vos trades en déplaçant le stop-loss au point d'entrée une fois en profit.",
                "iconColor": "text-purple-400"
            },
            {
                "titre": "Diversifiez les canaux",
                "description": "N'activez pas tous les canaux si vous avez un petit capital. Commencez par Forex et Gold.",
                "iconColor": "text-pink-400"
            },
            {
                "titre": "Surveillez votre marge",
                "description": "Assurez-vous d'avoir suffisamment de marge disponible pour que tous les trades puissent s'ouvrir.",
                "iconColor": "text-red-400"
            }
        ],
        "faq": [
            {
                "question": "Quel broker est recommandé ?",
                "reponse": "Nous recommandons ICMarkets, Exness, XM ou Global Prime pour leurs spreads compétitifs et leur exécution rapide."
            },
            {
                "question": "Puis-je utiliser plusieurs brokers ?",
                "reponse": "Oui, mais vous devrez configurer un connecteur par broker. Un seul compte TRADABOT peut gérer plusieurs MT4."
            },
            {
                "question": "Que se passe-t-il si je perds la connexion ?",
                "reponse": "Le connecteur se reconnecte automatiquement. Les signaux manqués pendant la coupure ne seront pas exécutés."
            },
            {
                "question": "Combien de trades par jour en moyenne ?",
                "reponse": "Entre 3 et 8 trades par jour selon les canaux activés. Les jours de forte volatilité peuvent générer plus de signaux."
            },
            {
                "question": "Le bot fonctionne-t-il sur Mac/Linux ?",
                "reponse": "Le connecteur est actuellement Windows uniquement. Vous pouvez utiliser une VM Windows ou Wine sur Mac/Linux."
            }
        ]
    }
