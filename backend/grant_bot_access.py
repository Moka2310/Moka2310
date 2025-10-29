#!/usr/bin/env python3
"""
Script pour donner accès au TRADABOT à un utilisateur (simuler un paiement)
"""
import os
import asyncio
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid

load_dotenv()

async def grant_bot_access(user_email):
    # Connexion MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("🎁 ATTRIBUTION D'ACCÈS TRADABOT")
    print("=" * 60)
    
    # Trouver l'utilisateur
    user = await db.users.find_one({"email": user_email})
    if not user:
        print(f"❌ Utilisateur introuvable: {user_email}")
        return
    
    user_id = user['id']
    print(f"👤 Utilisateur: {user['email']} (ID: {user_id})")
    
    # Vérifier s'il a déjà une précommande
    existing = await db.bot_preorders.find_one({
        "userId": user_id,
        "status": {"$in": ["paid", "delivered"]}
    })
    
    if existing:
        print(f"✅ L'utilisateur a déjà accès au bot (Statut: {existing['status']})")
        return
    
    # Créer une précommande "PAID"
    preorder = {
        "id": str(uuid.uuid4()),
        "userId": user_id,
        "userEmail": user_email,
        "price": 300.0,
        "status": "paid",
        "paymentMethod": "admin_grant",
        "stripePaymentIntentId": None,
        "paypalOrderId": None,
        "deliveredAt": None,
        "downloadLink": None,
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    }
    
    await db.bot_preorders.insert_one(preorder)
    
    print(f"✅ Accès TRADABOT accordé!")
    print(f"   - Status: PAID")
    print(f"   - Prix: 300$ CAD")
    print(f"   - L'utilisateur peut maintenant accéder à /tradabot-web")
    
    print("\n" + "=" * 60)
    print("✅ TERMINÉ!")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 grant_bot_access.py <email>")
        print("Exemple: python3 grant_bot_access.py test@tradalife.com")
    else:
        asyncio.run(grant_bot_access(sys.argv[1]))
