"""
Service pour gérer l'intégration Telegram
Récupère le nombre de membres du groupe Telegram
"""
import os
import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    async def get_chat_member_count(self, chat_id: str) -> Optional[int]:
        """
        Récupère le nombre de membres d'un groupe/canal Telegram
        
        Args:
            chat_id: ID du chat (format: @channel_name ou -1001234567890)
            
        Returns:
            Nombre de membres ou None en cas d'erreur
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/getChatMemberCount",
                    params={"chat_id": chat_id},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        member_count = data.get('result', 0)
                        logger.info(f"Telegram members count: {member_count}")
                        return member_count
                    else:
                        logger.error(f"Telegram API error: {data.get('description')}")
                        return None
                else:
                    logger.error(f"HTTP error {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching Telegram member count: {str(e)}")
            return None
    
    async def get_chat_info(self, chat_id: str) -> Optional[dict]:
        """
        Récupère les informations d'un chat Telegram
        
        Args:
            chat_id: ID du chat
            
        Returns:
            Informations du chat ou None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/getChat",
                    params={"chat_id": chat_id},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        return data.get('result')
                    
        except Exception as e:
            logger.error(f"Error fetching chat info: {str(e)}")
            
        return None

# Instance globale du service
telegram_service = TelegramService()
