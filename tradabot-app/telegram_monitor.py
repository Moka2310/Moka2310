"""Module Telegram pour recevoir les signaux"""
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from loguru import logger
from signal_parser import SignalParser
import config

class TelegramMonitor:
    """Surveille les canaux Telegram et extrait les signaux"""
    
    def __init__(self, bot_token: str, signal_callback):
        """
        Args:
            bot_token: Token du bot Telegram
            signal_callback: Fonction à appeler quand un signal est détecté
        """
        self.bot_token = bot_token
        self.signal_callback = signal_callback
        self.parser = SignalParser()
        self.application = None
        self.enabled_channels = set()
        self.is_running = False
        
    async def handle_message(self, update: Update, context):
        """
        Gère les messages reçus des canaux Telegram
        """
        try:
            if not update.channel_post:
                return
            
            message = update.channel_post
            chat_id = message.chat_id
            text = message.text or message.caption or ""
            
            # Vérifier si le canal est activé
            if chat_id not in self.enabled_channels:
                return
            
            # Identifier le canal
            channel_name = self._get_channel_name(chat_id)
            logger.info(f"📡 Message reçu du canal {channel_name}: {text[:50]}...")
            
            # Parser le signal
            signal = self.parser.parse_signal(text)
            
            if signal:
                signal['channel'] = channel_name
                signal['chat_id'] = chat_id
                
                # Appeler le callback avec le signal
                if self.signal_callback:
                    await self.signal_callback(signal)
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors du traitement du message: {e}")
    
    def _get_channel_name(self, chat_id: int) -> str:
        """Retourne le nom du canal depuis son ID"""
        for name, cid in config.TELEGRAM_CHANNELS.items():
            if cid == chat_id:
                return name
        return "unknown"
    
    def set_enabled_channels(self, channels_config: dict):
        """
        Définit les canaux à surveiller
        
        Args:
            channels_config: Dict avec channelForexEnabled, etc.
        """
        self.enabled_channels.clear()
        
        if channels_config.get('channelForexEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['forex'])
        if channels_config.get('channelCryptoEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['crypto'])
        if channels_config.get('channelGoldEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['gold'])
        if channels_config.get('channelIndicesEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['indices'])
        if channels_config.get('channelActionsEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['actions'])
        if channels_config.get('channelCommoditesEnabled'):
            self.enabled_channels.add(config.TELEGRAM_CHANNELS['commodites'])
        
        logger.info(f"📡 {len(self.enabled_channels)} canaux activés")
    
    async def start(self):
        """Démarre la surveillance des canaux"""
        try:
            logger.info("🚀 Démarrage du monitor Telegram...")
            
            # Créer l'application
            self.application = Application.builder().token(self.bot_token).build()
            
            # Ajouter le handler pour les messages de canal
            self.application.add_handler(
                MessageHandler(filters.ChatType.CHANNEL, self.handle_message)
            )
            
            # Démarrer
            self.is_running = True
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            logger.success("✅ Monitor Telegram démarré")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du démarrage Telegram: {e}")
            self.is_running = False
    
    async def stop(self):
        """Arrête la surveillance"""
        try:
            if self.application and self.is_running:
                logger.info("⏸️ Arrêt du monitor Telegram...")
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                self.is_running = False
                logger.success("✅ Monitor Telegram arrêté")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'arrêt: {e}")
