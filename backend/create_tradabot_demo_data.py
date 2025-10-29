#!/usr/bin/env python3
"""
Script pour créer des données de démonstration pour TRADABOT WEB
"""
import os
import asyncio
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def create_demo_data():
    # Connexion MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("🎬 CRÉATION DES DONNÉES DE DÉMO TRADABOT")
    print("=" * 60)
    
    # Trouver un utilisateur pour la démo (le premier utilisateur)
    user = await db.users.find_one({})
    if not user:
        print("❌ Aucun utilisateur trouvé")
        return
    
    user_id = user['id']
    print(f"👤 Utilisateur: {user['email']} (ID: {user_id})")
    
    # 1. Créer des signaux Telegram (dernières 24h)
    print("\n📡 Création de signaux...")
    signals = [
        {
            "type": "BUY",
            "symbol": "EURUSD",
            "entry": "1.0850",
            "sl": "1.0820",
            "tp1": "1.0890",
            "tp2": "1.0920",
            "channel": "forex",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        },
        {
            "type": "SELL",
            "symbol": "XAUUSD",
            "entry": "2045.50",
            "sl": "2055.00",
            "tp1": "2030.00",
            "tp2": "2020.00",
            "channel": "gold",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        },
        {
            "type": "BUY",
            "symbol": "BTCUSD",
            "entry": "35250.00",
            "sl": "34800.00",
            "tp1": "35800.00",
            "tp2": "36200.00",
            "channel": "crypto",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat()
        },
        {
            "type": "BUY",
            "symbol": "US30",
            "entry": "39850.0",
            "sl": "39650.0",
            "tp1": "40100.0",
            "tp2": "40300.0",
            "channel": "indices",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
        },
        {
            "type": "SELL",
            "symbol": "GBPUSD",
            "entry": "1.2680",
            "sl": "1.2710",
            "tp1": "1.2640",
            "tp2": "1.2610",
            "channel": "forex",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=15)).isoformat()
        },
        {
            "type": "BUY",
            "symbol": "AAPL",
            "entry": "178.50",
            "sl": "176.00",
            "tp1": "182.00",
            "tp2": "185.00",
            "channel": "actions",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=18)).isoformat()
        }
    ]
    
    # Supprimer les anciens signaux
    await db.telegram_signals.delete_many({})
    
    # Insérer les nouveaux signaux
    await db.telegram_signals.insert_many(signals)
    print(f"✅ {len(signals)} signaux créés")
    
    # 2. Créer des trades
    print("\n💰 Création de trades...")
    trades = [
        {
            "userId": user_id,
            "signalId": "signal_1",
            "type": "BUY",
            "symbol": "EURUSD",
            "lot": 0.05,
            "entry": 1.0850,
            "sl": 1.0820,
            "tp": 1.0890,
            "ticket": "123456789",
            "status": "open",
            "profit": 45.50,
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        },
        {
            "userId": user_id,
            "signalId": "signal_2",
            "type": "SELL",
            "symbol": "XAUUSD",
            "lot": 0.02,
            "entry": 2045.50,
            "sl": 2055.00,
            "tp": 2030.00,
            "ticket": "123456790",
            "status": "open",
            "profit": 124.30,
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        },
        {
            "userId": user_id,
            "signalId": "signal_3",
            "type": "BUY",
            "symbol": "BTCUSD",
            "lot": 0.01,
            "entry": 35250.00,
            "sl": 34800.00,
            "tp": 35800.00,
            "ticket": "123456791",
            "status": "open",
            "profit": 89.20,
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat()
        },
        {
            "userId": user_id,
            "signalId": "signal_old_1",
            "type": "SELL",
            "symbol": "GBPUSD",
            "lot": 0.03,
            "entry": 1.2720,
            "sl": 1.2750,
            "tp": 1.2680,
            "ticket": "123456780",
            "status": "closed",
            "profit": 185.60,
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        },
        {
            "userId": user_id,
            "signalId": "signal_old_2",
            "type": "BUY",
            "symbol": "US30",
            "lot": 0.02,
            "entry": 39600.0,
            "sl": 39400.0,
            "tp": 39900.0,
            "ticket": "123456781",
            "status": "closed",
            "profit": 240.00,
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        }
    ]
    
    # Supprimer les anciens trades
    await db.tradabot_trades.delete_many({"userId": user_id})
    
    # Insérer les nouveaux trades
    await db.tradabot_trades.insert_many(trades)
    print(f"✅ {len(trades)} trades créés (3 ouverts, 2 fermés)")
    
    # 3. Configurer le connecteur comme connecté
    print("\n🔌 Configuration du connecteur...")
    await db.tradabot_connectors.update_one(
        {"userId": user_id},
        {"$set": {
            "userId": user_id,
            "lastSeen": datetime.now(timezone.utc).isoformat(),
            "botStatus": "running",
            "mt4Connected": True
        }},
        upsert=True
    )
    print("✅ Connecteur configuré comme actif")
    
    # 4. Configurer le bot comme actif
    print("\n⚙️ Configuration du bot...")
    await db.tradabot_configs.update_one(
        {"userId": user_id},
        {"$set": {
            "userId": user_id,
            "mt4Login": "12345678",
            "mt4Password": "********",
            "mt4Server": "ICMarkets-Demo",
            "channels": {
                "forex": True,
                "crypto": True,
                "gold": True,
                "indices": True,
                "actions": True,
                "commodites": False
            },
            "lots": {
                "forex": 0.05,
                "crypto": 0.01,
                "gold": 0.02,
                "indices": 0.02,
                "actions": 0.03,
                "commodites": 0.01
            },
            "breakevenEnabled": True,
            "botStatus": "running",
            "updatedAt": datetime.now(timezone.utc).isoformat()
        }},
        upsert=True
    )
    print("✅ Configuration du bot mise à jour")
    
    print("\n" + "=" * 60)
    print("✅ DONNÉES DE DÉMO CRÉÉES AVEC SUCCÈS!")
    print("=" * 60)
    print("\n📊 Résumé:")
    print(f"  • Signaux: {len(signals)}")
    print(f"  • Trades ouverts: 3")
    print(f"  • Trades fermés: 2")
    print(f"  • Profit total ouvert: +259.00 $")
    print(f"  • Profit total fermé: +425.60 $")
    print(f"  • Bot: EN COURS D'EXÉCUTION ✅")
    print(f"  • Connecteur: CONNECTÉ ✅")
    print("\n🌐 Visitez /tradabot-web pour voir la démo!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_demo_data())
