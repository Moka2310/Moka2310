#!/usr/bin/env python3
"""
Script de test pour envoyer un signal TRADABOT de test
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os

async def send_test_signal():
    # Connexion MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("📡 ENVOI D'UN SIGNAL DE TEST")
    print("=" * 60)
    
    # Signal de test
    test_signal = {
        'id': f"test_signal_{int(datetime.now().timestamp() * 1000)}",
        'type': 'BUY',
        'symbol': 'EURUSD',
        'entry': '1.0850',
        'sl': '1.0820',
        'tp1': '1.0890',
        'tp2': '1.0920',
        'tp3': '1.0950',
        'channel': 'forex',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'status': 'pending',
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'rawMessage': 'TEST SIGNAL - BUY EURUSD @ 1.0850, SL: 1.0820, TP1: 1.0890'
    }
    
    # Insérer dans la DB
    result = await db.telegram_signals.insert_one(test_signal)
    
    print(f"\n✅ Signal de test créé!")
    print(f"   ID: {test_signal['id']}")
    print(f"   Type: {test_signal['type']}")
    print(f"   Symbol: {test_signal['symbol']}")
    print(f"   Entry: {test_signal['entry']}")
    print(f"   SL: {test_signal['sl']}")
    print(f"   TP1: {test_signal['tp1']}")
    print(f"   Canal: {test_signal['channel']}")
    
    # Compter les signaux totaux
    total_signals = await db.telegram_signals.count_documents({})
    print(f"\n📊 Total signaux dans la DB: {total_signals}")
    
    print("\n" + "=" * 60)
    print("✅ SIGNAL PRÊT POUR LE CONNECTEUR")
    print("=" * 60)
    print("\nLe connecteur MT4 devrait le récupérer dans les 5 secondes")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(send_test_signal())
