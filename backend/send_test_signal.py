"""
Script de test - Envoyer un signal de test dans la DB
Pour tester l'affichage sans attendre un vrai signal Telegram
"""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import asyncio

MONGO_URL = "mongodb://localhost:27017"

async def send_test_signal():
    """Envoie un signal de test dans la base de données"""
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client['tradalife']
    
    # Signal de test avec émojis (comme dans Telegram)
    test_signal = {
        'id': f"test_signal_{int(datetime.now().timestamp())}",
        'type': 'BUY',
        'symbol': 'EURUSD',
        'entryPrice': 1.0850,
        'stopLoss': 1.0820,
        'takeProfit1': 1.0900,
        'takeProfit2': 1.0950,
        'takeProfit3': None,
        'breakeven': True,
        'channel': 'forex',
        'rawMessage': '🔥 BUY EURUSD @ 1.0850 ⚡ TP1: 1.0900 🎯 TP2: 1.0950 ❌ SL: 1.0820 ⚖️ BREAKEVEN',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'status': 'pending'
    }
    
    # Insérer dans la DB
    result = await db.trade_signals.insert_one(test_signal)
    
    print("=" * 60)
    print("  📡 Signal de Test Envoyé!")
    print("=" * 60)
    print(f"\n  Type: {test_signal['type']}")
    print(f"  Symbole: {test_signal['symbol']}")
    print(f"  Entry: {test_signal['entryPrice']}")
    print(f"  SL: {test_signal['stopLoss']}")
    print(f"  TP1: {test_signal['takeProfit1']}")
    print(f"  TP2: {test_signal['takeProfit2']}")
    print(f"  Breakeven: {test_signal['breakeven']}")
    print(f"  Canal: {test_signal['channel']}")
    print(f"\n  Message original:")
    print(f"  {test_signal['rawMessage']}")
    print(f"\n  ✅ Signal visible dans l'interface dans ~5 secondes")
    print(f"     (rafraîchissement automatique)")
    print("\n" + "=" * 60)
    
    client.close()

if __name__ == '__main__':
    asyncio.run(send_test_signal())
