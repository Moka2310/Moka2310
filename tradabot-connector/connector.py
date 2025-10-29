"""
TRADABOT CONNECTOR - Connecteur MT4/MT5
Version: 1.0.0
Description: Connecteur local pour exécuter automatiquement les signaux TRADABOT sur MetaTrader 4/5
"""
import MetaTrader5 as mt5
import requests
import time
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
import sys
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tradabot_connector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradabotConnector:
    """Connecteur TRADABOT pour MT4/MT5"""
    
    def __init__(self, backend_url: str, auth_token: str):
        self.backend_url = backend_url
        self.auth_token = auth_token
        self.mt5_connected = False
        self.config = {}
        self.active_trades = {}
        self.running = False
        
    def connect_mt5(self, login: int, password: str, server: str) -> bool:
        """Se connecter à MetaTrader 5"""
        try:
            # Initialiser MT5
            if not mt5.initialize():
                logger.error(f"❌ Échec initialisation MT5: {mt5.last_error()}")
                return False
            
            # Se connecter au compte
            authorized = mt5.login(login, password=password, server=server)
            
            if not authorized:
                logger.error(f"❌ Échec connexion MT5: {mt5.last_error()}")
                mt5.shutdown()
                return False
            
            # Vérifier la connexion
            account_info = mt5.account_info()
            if account_info is None:
                logger.error("❌ Impossible de récupérer les infos du compte")
                return False
            
            self.mt5_connected = True
            logger.info(f"✅ Connecté à MT5 - Compte: {account_info.login}")
            logger.info(f"   Balance: {account_info.balance} {account_info.currency}")
            logger.info(f"   Leverage: 1:{account_info.leverage}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur connexion MT5: {e}")
            return False
    
    def disconnect_mt5(self):
        """Se déconnecter de MT5"""
        if self.mt5_connected:
            mt5.shutdown()
            self.mt5_connected = False
            logger.info("✅ Déconnexion MT5")
    
    def load_config(self) -> bool:
        """Charger la configuration depuis le backend"""
        try:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(
                f"{self.backend_url}/api/tradabot-web/config",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.config = response.json()
                logger.info("✅ Configuration chargée")
                return True
            else:
                logger.error(f"❌ Erreur chargement config: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erreur chargement config: {e}")
            return False
    
    def send_heartbeat(self) -> bool:
        """Envoyer un heartbeat au backend"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'status': 'connected' if self.mt5_connected else 'disconnected',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'mt4Connected': self.mt5_connected
            }
            
            response = requests.post(
                f"{self.backend_url}/api/tradabot-web/connector-heartbeat",
                headers=headers,
                json=data,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Erreur heartbeat: {e}")
            return False
    
    def get_pending_signals(self) -> List[Dict]:
        """Récupérer les signaux en attente d'exécution"""
        try:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(
                f"{self.backend_url}/api/tradabot-web/pending-signals",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Erreur récupération signaux: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Erreur récupération signaux: {e}")
            return []
    
    def execute_signal(self, signal: Dict) -> bool:
        """Exécuter un signal de trading"""
        try:
            if not self.mt5_connected:
                logger.warning("⚠️ MT5 non connecté, impossible d'exécuter le signal")
                return False
            
            # Récupérer les paramètres
            symbol = signal.get('symbol', '').upper()
            trade_type = signal.get('type', '').upper()  # BUY ou SELL
            entry = float(signal.get('entry', 0))
            sl = float(signal.get('sl', 0))
            tp1 = float(signal.get('tp1', 0))
            
            # Déterminer le lot selon le canal
            channel = signal.get('channel', 'forex')
            lot = self.config.get('lots', {}).get(channel, 0.01)
            
            # Vérifier si le canal est activé
            if not self.config.get('channels', {}).get(channel, False):
                logger.info(f"⏭️ Signal {symbol} ignoré (canal {channel} désactivé)")
                return False
            
            # Préparer l'ordre
            order_type = mt5.ORDER_TYPE_BUY if trade_type == 'BUY' else mt5.ORDER_TYPE_SELL
            
            # Vérifier si le symbole existe
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"❌ Symbole {symbol} introuvable")
                return False
            
            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    logger.error(f"❌ Impossible d'activer le symbole {symbol}")
                    return False
            
            # Préparer la requête
            price = mt5.symbol_info_tick(symbol).ask if trade_type == 'BUY' else mt5.symbol_info_tick(symbol).bid
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": order_type,
                "price": price,
                "sl": sl,
                "tp": tp1,
                "deviation": 20,
                "magic": 234000,
                "comment": f"TRADABOT_{signal.get('id', 'unknown')}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Envoyer l'ordre
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"❌ Échec ordre {symbol}: {result.comment}")
                return False
            
            # Succès
            logger.info(f"✅ Ordre exécuté: {trade_type} {lot} {symbol} @ {price}")
            logger.info(f"   Ticket: {result.order}, SL: {sl}, TP: {tp1}")
            
            # Sauvegarder dans active_trades pour le breakeven
            self.active_trades[result.order] = {
                'symbol': symbol,
                'type': trade_type,
                'entry': price,
                'sl': sl,
                'tp': tp1,
                'lot': lot,
                'signal_id': signal.get('id')
            }
            
            # Logger le trade dans le backend
            self.log_trade(signal, result.order, 'open', 0)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur exécution signal: {e}")
            return False
    
    def log_trade(self, signal: Dict, ticket: int, status: str, profit: float):
        """Logger un trade dans le backend"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'signal': signal,
                'ticket': ticket,
                'status': status,
                'profit': profit,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
            response = requests.post(
                f"{self.backend_url}/api/tradabot-web/log-trade",
                headers=headers,
                json=data,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Erreur log trade: {e}")
            return False
    
    def manage_breakeven(self):
        """Gérer le breakeven automatique"""
        try:
            if not self.config.get('breakevenEnabled', False):
                return
            
            if not self.mt5_connected:
                return
            
            # Récupérer toutes les positions ouvertes
            positions = mt5.positions_get()
            if positions is None or len(positions) == 0:
                return
            
            for position in positions:
                ticket = position.ticket
                
                # Vérifier si c'est un trade TRADABOT
                if ticket not in self.active_trades:
                    continue
                
                trade = self.active_trades[ticket]
                entry = trade['entry']
                current_price = position.price_current
                trade_type = trade['type']
                
                # Calculer le profit en pips
                if trade_type == 'BUY':
                    profit_pips = current_price - entry
                else:
                    profit_pips = entry - current_price
                
                # Si profit > 15 pips et SL n'est pas au breakeven
                if profit_pips > 0.0015 and position.sl != entry:  # 15 pips = 0.0015
                    # Déplacer le SL au breakeven
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "position": ticket,
                        "sl": entry,
                        "tp": position.tp,
                    }
                    
                    result = mt5.order_send(request)
                    
                    if result.retcode == mt5.TRADE_RETCODE_DONE:
                        logger.info(f"🔒 Breakeven activé pour {position.symbol} (Ticket: {ticket})")
                    else:
                        logger.warning(f"⚠️ Échec breakeven {position.symbol}: {result.comment}")
            
        except Exception as e:
            logger.error(f"❌ Erreur gestion breakeven: {e}")
    
    def run(self):
        """Boucle principale du connecteur"""
        logger.info("🚀 Démarrage TRADABOT Connector...")
        
        # Charger la configuration
        if not self.load_config():
            logger.error("❌ Impossible de charger la configuration")
            return
        
        # Se connecter à MT5
        mt5_login = int(self.config.get('mt4Login', 0))
        mt5_password = self.config.get('mt4Password', '')
        mt5_server = self.config.get('mt4Server', '')
        
        if not mt5_login or not mt5_password or not mt5_server:
            logger.error("❌ Configuration MT5 incomplète")
            return
        
        if not self.connect_mt5(mt5_login, mt5_password, mt5_server):
            logger.error("❌ Échec connexion MT5")
            return
        
        self.running = True
        last_heartbeat = 0
        last_check = 0
        
        logger.info("✅ TRADABOT Connector actif")
        logger.info("📊 Attente de signaux...")
        
        try:
            while self.running:
                current_time = time.time()
                
                # Heartbeat toutes les 10 secondes
                if current_time - last_heartbeat > 10:
                    self.send_heartbeat()
                    last_heartbeat = current_time
                
                # Vérifier les signaux toutes les 5 secondes
                if current_time - last_check > 5:
                    # Récupérer les signaux en attente
                    signals = self.get_pending_signals()
                    
                    for signal in signals:
                        logger.info(f"📡 Nouveau signal: {signal.get('symbol')} {signal.get('type')}")
                        self.execute_signal(signal)
                    
                    # Gérer le breakeven
                    self.manage_breakeven()
                    
                    last_check = current_time
                
                # Attendre 1 seconde
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Arrêt du connecteur...")
        finally:
            self.disconnect_mt5()
            logger.info("👋 TRADABOT Connector arrêté")


def main():
    """Point d'entrée principal"""
    # Configuration
    BACKEND_URL = os.environ.get('BACKEND_URL', 'https://edushop-portal.emergent.host')
    AUTH_TOKEN = os.environ.get('AUTH_TOKEN', '')
    
    if not AUTH_TOKEN:
        print("❌ Erreur: AUTH_TOKEN non défini")
        print("Veuillez définir votre token d'authentification dans le fichier .env")
        print("Ou lancez: set AUTH_TOKEN=votre_token_ici")
        sys.exit(1)
    
    # Créer et lancer le connecteur
    connector = TradabotConnector(BACKEND_URL, AUTH_TOKEN)
    connector.run()


if __name__ == "__main__":
    main()
