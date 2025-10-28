"""
Script pour réinitialiser le mot de passe d'un utilisateur
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import sys
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def reset_password(email: str, new_password: str):
    """Réinitialise le mot de passe d'un utilisateur"""
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'tradalife')]
    
    # Trouver l'utilisateur
    user = await db.users.find_one({"email": email})
    
    if not user:
        print(f"❌ Utilisateur {email} non trouvé")
        client.close()
        return False
    
    # Hasher le nouveau mot de passe
    hashed_password = pwd_context.hash(new_password)
    
    # Mettre à jour
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"password": hashed_password}}
    )
    
    if result.modified_count > 0:
        print("=" * 60)
        print("  ✅ Mot de passe réinitialisé avec succès!")
        print("=" * 60)
        print(f"\n  Email: {email}")
        print(f"  Nouveau mot de passe: {new_password}")
        print(f"\n  Tu peux maintenant te connecter sur:")
        print(f"  https://mt4-dropdown.preview.emergentagent.com/login")
        print("\n" + "=" * 60)
    else:
        print(f"❌ Erreur lors de la mise à jour")
    
    client.close()
    return True

async def main():
    if len(sys.argv) < 3:
        print("Usage: python reset_password.py <email> <nouveau_mot_de_passe>")
        print("Exemple: python reset_password.py yafoy2310@gmail.com MonNouveauMdp123")
        return
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    await reset_password(email, password)

if __name__ == '__main__':
    asyncio.run(main())
