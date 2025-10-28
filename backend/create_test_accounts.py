"""
Script pour créer des comptes de test pour TRADABOT
"""
import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def create_test_accounts():
    """Crée des comptes de test avec accès TRADABOT"""
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client['tradalife']
    
    print("🔧 Création des comptes de test TRADABOT...\n")
    
    # Liste des comptes à créer/mettre à jour
    accounts = [
        {
            "email": "yafoy2310@gmail.com",
            "password": "Admin2024!",
            "isAdmin": True,
            "hasBotAccess": True,
            "nom": "Super Admin"
        },
        {
            "email": "test@test.com",
            "password": "Test2024!",
            "isAdmin": False,
            "hasBotAccess": True,
            "nom": "Compte Test"
        },
        {
            "email": "demo@tradabot.com",
            "password": "Demo2024!",
            "isAdmin": False,
            "hasBotAccess": True,
            "nom": "Demo TradaBot"
        }
    ]
    
    for account in accounts:
        email = account["email"]
        password = account["password"]
        
        # Vérifier si le compte existe
        existing_user = await db.users.find_one({"email": email})
        
        if existing_user:
            # Mettre à jour le mot de passe et les droits
            password_hash = pwd_context.hash(password)
            
            await db.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "passwordHash": password_hash,
                        "isAdmin": account["isAdmin"],
                        "hasBotAccess": account["hasBotAccess"],
                        "nom": account["nom"]
                    }
                }
            )
            print(f"✅ Compte mis à jour: {email}")
            print(f"   Mot de passe: {password}")
            print(f"   Admin: {account['isAdmin']}")
            print(f"   Accès TRADABOT: {account['hasBotAccess']}\n")
        else:
            # Créer le compte
            password_hash = pwd_context.hash(password)
            
            new_user = {
                "userId": str(uuid.uuid4()),
                "email": email,
                "passwordHash": password_hash,
                "nom": account["nom"],
                "prenom": "Test",
                "isAdmin": account["isAdmin"],
                "hasBotAccess": account["hasBotAccess"],
                "emailVerified": True,
                "createdAt": "2024-10-28T00:00:00Z"
            }
            
            await db.users.insert_one(new_user)
            print(f"✅ Compte créé: {email}")
            print(f"   Mot de passe: {password}")
            print(f"   Admin: {account['isAdmin']}")
            print(f"   Accès TRADABOT: {account['hasBotAccess']}\n")
    
    print("\n" + "="*60)
    print("🎯 COMPTES DE TEST PRÊTS")
    print("="*60)
    print("\n📝 IDENTIFIANTS POUR LES TESTS:\n")
    
    for account in accounts:
        print(f"{'='*60}")
        print(f"Email:    {account['email']}")
        print(f"Password: {account['password']}")
        print(f"Admin:    {'Oui' if account['isAdmin'] else 'Non'}")
        print(f"TradaBot: {'Oui' if account['hasBotAccess'] else 'Non'}")
        print()
    
    print("\n🌐 URLs de test:")
    print("   - Frontend: https://mt4-dropdown.preview.emergentagent.com")
    print("   - Login: https://mt4-dropdown.preview.emergentagent.com/login")
    print("   - TradaBot Demo: https://mt4-dropdown.preview.emergentagent.com/tradabot-demo")
    print("   - TradaBot Config: https://mt4-dropdown.preview.emergentagent.com/tradabot")
    print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_test_accounts())
