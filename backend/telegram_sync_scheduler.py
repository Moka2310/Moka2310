"""
Tâche planifiée pour synchroniser le nombre de membres Telegram toutes les heures
"""
import asyncio
import httpx
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8001"
SYNC_INTERVAL = 3600  # 1 heure en secondes

async def sync_telegram_members():
    """Synchronise le nombre de membres depuis Telegram"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BACKEND_URL}/api/telegram/sync-members",
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Membres synchronisés: {data.get('count')}")
                return True
            else:
                logger.error(f"❌ Erreur de synchronisation: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Erreur: {str(e)}")
        return False

async def run_scheduler():
    """Boucle principale du scheduler"""
    logger.info("🚀 Démarrage du scheduler de synchronisation Telegram")
    logger.info(f"⏰ Synchronisation toutes les {SYNC_INTERVAL} secondes ({SYNC_INTERVAL // 3600} heure(s))")
    
    while True:
        try:
            logger.info(f"🔄 Synchronisation en cours... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
            await sync_telegram_members()
            
            # Attendre avant la prochaine synchronisation
            await asyncio.sleep(SYNC_INTERVAL)
            
        except Exception as e:
            logger.error(f"❌ Erreur dans le scheduler: {str(e)}")
            # Attendre 5 minutes avant de réessayer en cas d'erreur
            await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(run_scheduler())
