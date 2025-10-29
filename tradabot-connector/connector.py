"""
TRADABOT Connecteur MT4 - Version Ultra-Légère
Se connecte au backend tradalife.com et exécute les trades sur MT4
"""
import requests
import time
import MetaTrader5 as mt5
import json
import sys
from datetime import datetime

class TradabotConnector:
    def __init__(self):
        self.backend_url = "https://www.tradalife.com"  # URL de production
        self.token = None
        self.user_email = None
        self.config = {}
        self.running = False
        self.mt4_connected = False
        
    def login(self):
        """Connexion à tradalife.com"""
        print("=== TRADABOT CONNECTEUR ===")
        print("\nConnexion à votre compte Tradalife...")
        
        email = input("Email: ")
        password = input("Password: ")
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/auth/login",
                json={"email": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['token']
                self.user_email = email
                print("✅ Connexion réussie!")
                return True
            else:
                print("❌ Erreur de connexion")
                return False
        except Exception as e:
            print(f"❌ Erreur réseau: {e}")
            return False
    
    def load_config(self):
        """Charge la configuration depuis le backend"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/tradabot-web/config",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                self.config = response.json()
                print("✅ Configuration chargée")
                return True
            return False
        except:
            return False
    
    def connect_mt4(self):
        """Connexion à MT4/MT5"""
        if not self.config.get('mt4Login') or not self.config.get('mt4Server'):
            print("⚠️  Configuration MT4 manquante. Configurez-la sur le site web.")
            return False
        
        print(f"\nConnexion à MT4 ({self.config['mt4Server']})...")
        
        if not mt5.initialize():
            print("❌ MT5 non trouvé. Assurez-vous que MetaTrader 5 est installé.")
            return False
        
        # Se connecter
        login = int(self.config['mt4Login'])
        password = self.config['mt4Password']
        server = self.config['mt4Server']
        
        if mt5.login(login, password, server):
            print("✅ Connecté à MT4!")
            self.mt4_connected = True
            return True
        else:
            error = mt5.last_error()
            print(f"❌ Échec connexion MT4: {error}")
            return False
    
    def send_heartbeat(self):
        """Envoie un signal au backend pour indiquer que le connecteur est actif"""
        try:
            bot_status = "running" if self.running else "stopped"
            requests.post(
                f"{self.backend_url}/api/tradabot-web/connector-heartbeat",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "lastSeen": datetime.utcnow().isoformat() + "Z",
                    "botStatus": bot_status,
                    "mt4Connected": self.mt4_connected
                }
            )
        except:
            pass
    
    def check_signals(self):
        """Vérifie s'il y a de nouveaux signaux à trader"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/tradabot-web/pending-signals",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            
            if response.status_code == 200:
                signals = response.json()
                for signal in signals:
                    self.execute_trade(signal)
        except:
            pass
    
    def execute_trade(self, signal):
        """Exécute un trade sur MT4"""
        if not self.mt4_connected:
            return
        
        print(f"\n📈 Exécution trade: {signal['type']} {signal['symbol']}")
        
        # Déterminer le lot
        symbol = signal['symbol']
        lot = self.get_lot_for_symbol(symbol)
        
        # Type d'ordre
        order_type = mt5.ORDER_TYPE_BUY if signal['type'] == 'BUY' else mt5.ORDER_TYPE_SELL
        
        # Prix actuel
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            print(f"❌ Symbole {symbol} non trouvé")
            return
        
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        # SL et TP
        sl = float(signal.get('sl', 0))
        tp = float(signal.get('tp1', 0))
        
        # Préparer la requête
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 234567,
            "comment": "TRADABOT",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Envoyer l'ordre
        result = mt5.order_send(request)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"✅ Trade exécuté! Ticket: {result.order}")
            # Informer le backend
            self.log_trade(signal, result.order, "success")
        else:
            print(f"❌ Échec trade: {result.comment}")
            self.log_trade(signal, 0, "failed")
    
    def get_lot_for_symbol(self, symbol):
        """Retourne le lot configuré pour un symbole"""
        symbol_lower = symbol.lower()
        
        if any(x in symbol_lower for x in ['eur', 'usd', 'gbp', 'jpy']):
            return self.config['lots']['forex']
        elif any(x in symbol_lower for x in ['btc', 'eth', 'xrp']):
            return self.config['lots']['crypto']
        elif 'xau' in symbol_lower or 'gold' in symbol_lower:
            return self.config['lots']['gold']
        elif any(x in symbol_lower for x in ['us30', 'nas100', 'spx', 'dax']):
            return self.config['lots']['indices']
        elif any(x in symbol_lower for x in ['aapl', 'tsla', 'amzn']):
            return self.config['lots']['actions']
        else:
            return self.config['lots']['commodites']
    
    def log_trade(self, signal, ticket, status):
        """Enregistre le trade dans le backend"""
        try:
            requests.post(
                f"{self.backend_url}/api/tradabot-web/log-trade",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "signal": signal,
                    "ticket": ticket,
                    "status": status,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
        except:
            pass
    
    def run(self):
        """Boucle principale"""
        print("\n" + "="*50)
        print("🤖 TRADABOT CONNECTEUR ACTIF")
        print("="*50)
        print("\nLe connecteur surveille les signaux...")
        print("Configurez le bot sur: https://www.tradalife.com/tradabot-web")
        print("\nAppuyez sur Ctrl+C pour arrêter\n")
        
        try:
            while True:
                # Heartbeat toutes les 10 secondes
                self.send_heartbeat()
                
                # Vérifier les signaux
                self.check_signals()
                
                # Attendre 5 secondes
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Arrêt du connecteur...")
            if self.mt4_connected:
                mt5.shutdown()
            print("✅ Connecteur arrêté")

def main():
    connector = TradabotConnector()
    
    # Connexion
    if not connector.login():
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Charger config
    if not connector.load_config():
        print("❌ Impossible de charger la configuration")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Connexion MT4
    if not connector.connect_mt4():
        print("\n⚠️  Configurez MT4 sur le site web et relancez le connecteur")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Démarrer
    connector.run()

if __name__ == "__main__":
    main()
