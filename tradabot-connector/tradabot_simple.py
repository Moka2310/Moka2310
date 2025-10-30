"""
TRADABOT - Connecteur Simplifié MT4/MT5
Version: 2.0 (Simplifié)
"""
import json
import os
import sys
import time
from datetime import datetime

print("=" * 80)
print("🤖 TRADABOT CONNECTEUR - Chargement...")
print("=" * 80)
print()

# Vérifier les imports
try:
    import MetaTrader5 as mt5
    print("✅ MetaTrader5 chargé")
except ImportError:
    print("❌ MetaTrader5 n'est pas installé!")
    print()
    print("Solution: Lancez INSTALLATION_SIMPLE.bat")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

try:
    import requests
    print("✅ Requests chargé")
except ImportError:
    print("❌ Requests n'est pas installé!")
    print()
    print("Solution: Lancez INSTALLATION_SIMPLE.bat")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

print()

# Charger la configuration
try:
    with open('tradabot_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    print("✅ Configuration chargée")
except FileNotFoundError:
    print("❌ Fichier tradabot_config.json introuvable!")
    print()
    print("Solution:")
    print("1. Allez sur https://tradalife.com/tradabot-web")
    print("2. Téléchargez votre configuration")
    print("3. Placez le fichier dans ce dossier")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)
except json.JSONDecodeError:
    print("❌ Fichier de configuration invalide!")
    print()
    print("Solution: Re-téléchargez le fichier depuis le site")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

# Extraire les paramètres
AUTH_TOKEN = config.get('authToken', '')
BACKEND_URL = config.get('backendUrl', 'https://edushop-portal.emergent.host')
MT4_LOGIN = int(config.get('mt4Login', 0))
MT4_PASSWORD = config.get('mt4Password', '')
MT4_SERVER = config.get('mt4Server', '')
CHANNELS = config.get('channels', {})
LOTS = config.get('lots', {})
BREAKEVEN_ENABLED = config.get('breakevenEnabled', True)

if not AUTH_TOKEN:
    print("❌ Token d'authentification manquant!")
    print()
    print("Solution: Re-téléchargez le fichier de configuration")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

if not MT4_LOGIN or not MT4_PASSWORD or not MT4_SERVER:
    print("❌ Paramètres MT4/MT5 incomplets!")
    print()
    print("Solution:")
    print("1. Configurez vos paramètres sur le site")
    print("2. Re-téléchargez la configuration")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

print(f"✅ Utilisateur: {config.get('userEmail', 'N/A')}")
print(f"✅ Serveur: {MT4_SERVER}")
print()

# Connexion à MT5
print("=" * 80)
print("🔗 CONNEXION À METATRADER...")
print("=" * 80)
print()

if not mt5.initialize():
    print(f"❌ Échec initialisation MT5: {mt5.last_error()}")
    print()
    print("Solutions possibles:")
    print("1. Vérifiez que MetaTrader est installé")
    print("2. Ouvrez MetaTrader manuellement")
    print("3. Redémarrez votre ordinateur")
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

print("✅ MT5 initialisé")

# Se connecter au compte
if not mt5.login(MT4_LOGIN, password=MT4_PASSWORD, server=MT4_SERVER):
    error = mt5.last_error()
    print(f"❌ Échec connexion MT5: {error}")
    print()
    print("Vérifiez:")
    print(f"  - Login: {MT4_LOGIN}")
    print(f"  - Serveur: {MT4_SERVER}")
    print("  - Mot de passe (caché)")
    print()
    print("Solutions:")
    print("1. Vérifiez vos identifiants sur le site")
    print("2. Ouvrez MetaTrader et connectez-vous manuellement")
    print("3. Re-configurez depuis le site web")
    mt5.shutdown()
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

# Récupérer les infos du compte
account_info = mt5.account_info()
if account_info is None:
    print("❌ Impossible de récupérer les infos du compte")
    mt5.shutdown()
    input("\nAppuyez sur Entrée pour quitter...")
    sys.exit(1)

print()
print("✅ CONNECTÉ À MT5!")
print(f"   Compte: {account_info.login}")
print(f"   Balance: {account_info.balance} {account_info.currency}")
print(f"   Levier: 1:{account_info.leverage}")
print(f"   Serveur: {account_info.server}")
print()

# Boucle principale
print("=" * 80)
print("🚀 TRADABOT ACTIF - EN ATTENTE DE SIGNAUX")
print("=" * 80)
print()
print("ℹ️  Le bot surveille les signaux toutes les 5 secondes")
print("ℹ️  Pour arrêter: Fermez cette fenêtre ou appuyez sur Ctrl+C")
print()
print(f"Canaux actifs: {', '.join([k for k, v in CHANNELS.items() if v])}")
print()
print("-" * 80)
print()

try:
    while True:
        try:
            # Heartbeat
            headers = {
                'Authorization': f'Bearer {AUTH_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            heartbeat_data = {
                'status': 'connected',
                'timestamp': datetime.utcnow().isoformat(),
                'mt4Connected': True
            }
            
            requests.post(
                f"{BACKEND_URL}/api/tradabot-web/connector-heartbeat",
                headers=headers,
                json=heartbeat_data,
                timeout=5
            )
            
            # Récupérer les signaux en attente
            response = requests.get(
                f"{BACKEND_URL}/api/tradabot-web/pending-signals",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                signals = response.json()
                
                if signals:
                    print(f"📡 {len(signals)} nouveau(x) signal(aux) reçu(s)!")
                    
                    for signal in signals:
                        symbol = signal.get('symbol', 'N/A')
                        trade_type = signal.get('type', 'N/A')
                        entry = signal.get('entry', 0)
                        sl = signal.get('sl', 0)
                        tp1 = signal.get('tp1', 0)
                        channel = signal.get('channel', 'unknown')
                        
                        print(f"   {trade_type} {symbol} @ {entry} | SL: {sl} | TP: {tp1}")
                        
                        # Vérifier si le canal est activé
                        if not CHANNELS.get(channel, False):
                            print(f"   ⏭️  Ignoré (canal {channel} désactivé)")
                            continue
                        
                        # Récupérer le lot
                        lot = LOTS.get(channel, 0.01)
                        
                        # Préparer l'ordre
                        order_type = mt5.ORDER_TYPE_BUY if trade_type == 'BUY' else mt5.ORDER_TYPE_SELL
                        
                        # Vérifier le symbole
                        symbol_info = mt5.symbol_info(symbol)
                        if symbol_info is None:
                            print(f"   ❌ Symbole {symbol} introuvable")
                            continue
                        
                        if not symbol_info.visible:
                            mt5.symbol_select(symbol, True)
                        
                        # Prix actuel
                        tick = mt5.symbol_info_tick(symbol)
                        if tick is None:
                            print(f"   ❌ Impossible d'obtenir le prix pour {symbol}")
                            continue
                        
                        price = tick.ask if trade_type == 'BUY' else tick.bid
                        
                        # Créer la requête
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
                            print(f"   ❌ Échec: {result.comment}")
                        else:
                            print(f"   ✅ Ordre exécuté! Ticket: {result.order}")
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Erreur de connexion au serveur: {e}")
        except Exception as e:
            print(f"⚠️  Erreur: {e}")
        
        # Attendre 5 secondes
        time.sleep(5)

except KeyboardInterrupt:
    print()
    print()
    print("=" * 80)
    print("⏹️  ARRÊT DU BOT...")
    print("=" * 80)
    print()

finally:
    mt5.shutdown()
    print("✅ Déconnexion MT5")
    print()
    print("👋 Au revoir!")
    input("\nAppuyez sur Entrée pour fermer...")
