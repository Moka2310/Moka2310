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
    
    async def create_chat_invite_link(self, chat_id: str, member_limit: int = 1) -> Optional[str]:
        """
        Crée un lien d'invitation unique pour un utilisateur
        
        Args:
            chat_id: ID du chat/canal
            member_limit: Nombre maximum d'utilisations (1 par défaut pour un lien unique)
            
        Returns:
            URL du lien d'invitation ou None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/createChatInviteLink",
                    json={
                        "chat_id": chat_id,
                        "member_limit": member_limit,
                        "creates_join_request": False  # Accès direct sans approbation
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        invite_link = data.get('result', {}).get('invite_link')
                        logger.info(f"Created invite link for chat {chat_id}")
                        return invite_link
                    else:
                        logger.error(f"Telegram API error: {data.get('description')}")
                else:
                    logger.error(f"HTTP error {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error creating invite link: {str(e)}")
            
        return None
    
    async def ban_chat_member(self, chat_id: str, user_id: int) -> bool:
        """
        Bannit (retire) un membre d'un chat/canal
        
        Args:
            chat_id: ID du chat/canal
            user_id: ID Telegram de l'utilisateur
            
        Returns:
            True si succès, False sinon
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/banChatMember",
                    json={
                        "chat_id": chat_id,
                        "user_id": user_id,
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        logger.info(f"Banned user {user_id} from chat {chat_id}")
                        return True
                    else:
                        logger.error(f"Error banning user: {data.get('description')}")
                else:
                    logger.error(f"HTTP error {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error banning chat member: {str(e)}")
            
        return False
    
    async def get_user_id_by_username(self, username: str) -> Optional[int]:
        """
        Récupère l'ID Telegram d'un utilisateur à partir de son username
        Note: Cette méthode nécessite que le bot ait déjà interagi avec l'utilisateur
        
        Args:
            username: Username Telegram (sans @)
            
        Returns:
            User ID ou None
        """
        # Note: L'API Telegram ne permet pas de rechercher directement un user_id par username
        # sans interaction préalable. Cette méthode est un placeholder.
        # En production, il faudra demander à l'utilisateur de démarrer une conversation
        # avec le bot pour obtenir son user_id
        logger.warning(f"Cannot get user_id for {username} without prior interaction")
        return None

# Instance globale du service
telegram_service = TelegramService()
