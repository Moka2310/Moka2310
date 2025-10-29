"""
TRADABOT - Service Telegram en temps réel
Écoute les signaux des 6 canaux VIP et les envoie au frontend
"""
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import json
import re
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Configuration
TELEGRAM_BOT_TOKEN = "8406540414:AAG-IlyhG5eL0BjSkvaJhZ2qCrngRETCHpc"
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')

# Canaux VIP
CHANNELS = {
    'forex': -1002425540174,
    'crypto': -1002279973041,
    'gold': -1002355600472,
    'indices': -1002339785500,
    'actions': -1002376632406,
    'commodites': -1002368060694
}

# Base de données
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client['tradalife']

class SignalParser:
    """Parse les signaux de trading depuis les messages Telegram"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Nettoie le texte des émojis et caractères spéciaux"""
        # Supprimer tous les émojis et caractères Unicode non-ASCII
        import unicodedata
        # Normaliser et garder seulement ASCII + quelques caractères utiles
        cleaned = ''.join(
            char for char in text 
            if ord(char) < 128 or char in ['@', ':', '.', ',']
        )
        return cleaned
    
    @staticmethod
    def parse_signal(text: str, channel_name: str):
        """Parse un message pour extraire le signal"""
        # Nettoyer les émojis d'abord
        text_clean = SignalParser.clean_text(text)
        text = text_clean.upper()
        
        print(f"   Texte nettoyé: {text[:100]}...")
        
        # Détecter le type (BUY/SELL)
        signal_type = None
        if 'BUY' in text or 'ACHAT' in text or 'ACHETER' in text:
            signal_type = 'BUY'
        elif 'SELL' in text or 'VENTE' in text or 'VENDRE' in text:
            signal_type = 'SELL'
        
        if not signal_type:
            return None
        
        # Extraire le symbole - patterns étendus
        symbol_patterns = [
            r'([A-Z]{6})',  # EURUSD, GBPUSD, etc.
            r'([A-Z]{3}USD)',  # BTCUSD, ETHUSD
            r'(XAU[A-Z]{3})',  # XAUUSD
            r'(XAG[A-Z]{3})',  # XAGUSD (Silver)
            r'(US[0-9]+)',  # US30, US100
            r'(NAS[0-9]+)',  # NAS100
            r'(SPX[0-9]+)',  # SPX500
        ]
        
        symbol = None
        for pattern in symbol_patterns:
            match = re.search(pattern, text)
            if match:
                symbol = match.group(1)
                break
        
        if not symbol:
            return None
        
        # Extraire les prix avec patterns plus flexibles
        entry_price = SignalParser._extract_price(text, ['@', 'ENTRY', 'ENTREE', 'PRICE', 'PRIX', 'AT'])
        stop_loss = SignalParser._extract_price(text, ['SL', 'STOP LOSS', 'STOP', 'STOPLOSS'])
        take_profit1 = SignalParser._extract_price(text, ['TP1', 'TP 1', 'TAKE PROFIT 1', 'TAKEPROFIT1', 'TARGET 1', 'T1'])
        take_profit2 = SignalParser._extract_price(text, ['TP2', 'TP 2', 'TAKE PROFIT 2', 'TAKEPROFIT2', 'TARGET 2', 'T2'])
        take_profit3 = SignalParser._extract_price(text, ['TP3', 'TP 3', 'TAKE PROFIT 3', 'TAKEPROFIT3', 'TARGET 3', 'T3'])
        
        # Si pas de TP1 mais TP sans numéro
        if not take_profit1:
            take_profit1 = SignalParser._extract_price(text, ['TP', 'TAKE PROFIT', 'TAKEPROFIT', 'TARGET'])
        
        # Détecter breakeven
        breakeven = 'BREAKEVEN' in text or 'BREAK EVEN' in text or 'BE' in text or 'B.E' in text
        
        signal_data = {
            'type': signal_type,
            'symbol': symbol,
            'entryPrice': entry_price,
            'stopLoss': stop_loss,
            'takeProfit1': take_profit1,
            'takeProfit2': take_profit2,
            'takeProfit3': take_profit3,
            'breakeven': breakeven,
            'channel': channel_name,
            'rawMessage': text[:500],  # Limiter la longueur
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        print(f"   Signal extrait: {signal_data}")
        
        return signal_data
    
    @staticmethod
    def _extract_price(text: str, keywords: list) -> float:
        """Extrait un prix après un mot-clé"""
        for keyword in keywords:
            # Plusieurs patterns pour plus de flexibilité
            patterns = [
                rf'{keyword}\s*[:=]?\s*([0-9]+\.?[0-9]*)',  # TP: 1.0850 ou TP1.0850 ou TP = 1.0850
                rf'{keyword}\s*@\s*([0-9]+\.?[0-9]*)',  # TP @ 1.0850
                rf'{keyword}\s+([0-9]+\.?[0-9]*)',  # TP 1.0850
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    try:
                        price = float(match.group(1))
                        # Validation basique du prix
                        if price > 0:
                            return price
                    except:
                        continue
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages reçus des canaux"""
    if not update.channel_post:
        return
    
    message = update.channel_post
    chat_id = message.chat_id
    text = message.text
    
    if not text:
        return
    
    # Identifier le canal
    channel_name = None
    for name, channel_id in CHANNELS.items():
        if chat_id == channel_id:
            channel_name = name
            break
    
    if not channel_name:
        print(f"⚠️ Message d'un canal non configuré: {chat_id}")
        return
    
    print(f"\n📡 Message reçu de {channel_name.upper()}:")
    print(f"   {text[:100]}...")
    
    # Parser le signal
    signal = SignalParser.parse_signal(text, channel_name)
    
    if signal:
        print(f"✅ Signal parsé: {signal['type']} {signal['symbol']}")
        
        # Sauvegarder dans la DB
        try:
            # Ajouter un ID unique
            signal['id'] = f"signal_{int(datetime.now().timestamp() * 1000)}"
            signal['status'] = 'pending'
            signal['createdAt'] = datetime.now(timezone.utc).isoformat()
            
            await db.telegram_signals.insert_one(signal)
            print(f"✅ Signal sauvegardé dans la DB")
            
            # Notifier les utilisateurs actifs (via webhook ou websocket)
            await notify_active_users(signal)
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde signal: {e}")
    else:
        print(f"⚠️ Pas de signal détecté dans le message")


async def notify_active_users(signal: dict):
    """Notifie les utilisateurs qui ont le bot actif"""
    try:
        # Trouver les utilisateurs avec bot actif
        active_configs = await db.tradabot_configs.find({
            'botActive': True,
            f'channel{signal["channel"].capitalize()}Enabled': True
        }).to_list(length=None)
        
        print(f"📢 {len(active_configs)} utilisateur(s) actif(s) pour ce canal")
        
        # Pour chaque utilisateur, exécuter le trade si configuré
        for config in active_configs:
            user_id = config.get('userId')
            if user_id:
                # Ici on pourrait déclencher l'exécution du trade
                # Pour l'instant on log juste
                print(f"   → Notifier utilisateur {user_id}")
                
    except Exception as e:
        print(f"❌ Erreur notification: {e}")


async def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("  🤖 TRADABOT - Service Telegram en temps réel")
    print("=" * 60)
    print("")
    print(f"  🔑 Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"  📡 Canaux surveillés:")
    for name, channel_id in CHANNELS.items():
        print(f"     - {name.capitalize()}: {channel_id}")
    print("")
    print("  ✅ Démarrage du bot...")
    print("")
    print("=" * 60)
    print("")
    
    # Créer l'application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Ajouter le handler pour tous les messages de canaux
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_message))
    
    # Démarrer le bot
    print("🚀 Bot démarré! En écoute des signaux...")
    
    # Utiliser initialize et start au lieu de run_polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    # Garder le service actif
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\n⏹️ Arrêt du bot...")
    finally:
        await app.stop()
        await app.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Service arrêté")
