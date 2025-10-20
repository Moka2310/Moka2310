#!/usr/bin/env python3
"""
Script pour promouvoir un utilisateur en admin sur la base de production
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def promote_to_admin():
    # Connexion à la base de données
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    email = "yafoy2310@gmail.com"
    
    print("=" * 60)
    print(f"🔧 PROMOTION DE {email} EN ADMINISTRATEUR")
    print("=" * 60)
    
    # Vérifier si l'utilisateur existe
    user = await db.users.find_one({"email": email})
    
    if not user:
        print(f"\n❌ Utilisateur {email} non trouvé dans la base de données!")
        print("   Assurez-vous d'avoir créé le compte sur tradalife.com")
        client.close()
        return
    
    print(f"\n✅ Utilisateur trouvé:")
    print(f"   Email: {user.get('email')}")
    print(f"   Nom: {user.get('firstName')} {user.get('lastName')}")
    print(f"   Rôle actuel: {user.get('role', 'user')}")
    
    # Promouvoir en admin
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"role": "admin"}}
    )
    
    if result.modified_count > 0:
        print(f"\n✅ Compte promu en administrateur avec succès!")
        print(f"   Vous pouvez maintenant accéder au panneau admin sur:")
        print(f"   👉 https://tradalife.com/admin")
    else:
        print(f"\n⚠️  Le compte était peut-être déjà admin")
    
    print("=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(promote_to_admin())
