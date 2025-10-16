#!/usr/bin/env python3
"""
Script pour créer un compte administrateur dans Tradalife
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["tradalife"]
    
    print("=" * 60)
    print("🔧 CRÉATION D'UN COMPTE ADMINISTRATEUR")
    print("=" * 60)
    
    # Check existing users
    all_users = await db.users.find({}).to_list(length=None)
    print(f"\n📊 Utilisateurs existants dans la base: {len(all_users)}")
    
    if all_users:
        print("\nUtilisateurs:")
        for idx, user in enumerate(all_users, 1):
            role = user.get('role', 'user')
            print(f"  {idx}. {user.get('email')} - Rôle: {role}")
    
    print("\n" + "=" * 60)
    print("OPTIONS:")
    print("1. Créer un nouveau compte admin")
    print("2. Promouvoir un utilisateur existant en admin")
    print("=" * 60)
    
    choice = input("\nVotre choix (1 ou 2): ").strip()
    
    if choice == "1":
        # Create new admin account
        print("\n📝 Création d'un nouveau compte admin...")
        
        email = input("Email: ").strip()
        password = input("Mot de passe: ").strip()
        first_name = input("Prénom: ").strip()
        last_name = input("Nom: ").strip()
        
        # Check if email already exists
        existing = await db.users.find_one({"email": email})
        if existing:
            print(f"\n❌ Un utilisateur avec l'email {email} existe déjà!")
            client.close()
            return
        
        # Create admin user
        hashed_password = pwd_context.hash(password)
        
        admin_user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "hashedPassword": hashed_password,
            "firstName": first_name,
            "lastName": last_name,
            "role": "admin",
            "kycStatus": "approved",
            "country": "",
            "phone": "",
            "formations": [],
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
        
        await db.users.insert_one(admin_user)
        print(f"\n✅ Compte admin créé avec succès!")
        print(f"   Email: {email}")
        print(f"   Rôle: admin")
        
    elif choice == "2":
        # Promote existing user
        if not all_users:
            print("\n❌ Aucun utilisateur à promouvoir!")
            client.close()
            return
        
        user_num = int(input("\nNuméro de l'utilisateur à promouvoir: ").strip())
        
        if user_num < 1 or user_num > len(all_users):
            print("\n❌ Numéro invalide!")
            client.close()
            return
        
        selected_user = all_users[user_num - 1]
        
        # Update user role to admin
        await db.users.update_one(
            {"id": selected_user["id"]},
            {"$set": {"role": "admin"}}
        )
        
        print(f"\n✅ Utilisateur promu en admin!")
        print(f"   Email: {selected_user['email']}")
        print(f"   Nouveau rôle: admin")
    
    else:
        print("\n❌ Choix invalide!")
    
    print("\n" + "=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
