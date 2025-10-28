"""
Script pour changer le nom de l'admin Ali Hyjazi en Moka
"""
import os
from pymongo import MongoClient
from datetime import datetime

# Load .env
env_path = '/app/backend/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

mongo_url = os.environ.get('MONGO_URL')
client = MongoClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'tradalife')]

print("=" * 80)
print("🔄 CHANGEMENT DU NOM D'ADMIN: Ali Hyjazi → Moka")
print("=" * 80)

# Trouver l'utilisateur Ali Hyjazi
user = db.users.find_one({
    "firstName": "Ali",
    "lastName": "Hyjazi"
})

if user:
    print(f"\n✅ Utilisateur trouvé:")
    print(f"   Email: {user.get('email')}")
    print(f"   Nom actuel: {user.get('firstName')} {user.get('lastName')}")
    print(f"   Role: {user.get('role')}")
    
    # Mettre à jour
    result = db.users.update_one(
        {"id": user['id']},
        {"$set": {
            "firstName": "Moka",
            "lastName": "",
            "updatedAt": datetime.utcnow()
        }}
    )
    
    if result.modified_count > 0:
        print(f"\n✅ Nom changé avec succès!")
        print(f"   Nouveau nom: Moka")
        
        # Vérifier
        updated_user = db.users.find_one({"id": user['id']})
        print(f"\n📊 Vérification:")
        print(f"   Prénom: {updated_user.get('firstName')}")
        print(f"   Nom: {updated_user.get('lastName')}")
    else:
        print("\n⚠️ Aucune modification effectuée")
else:
    # Chercher par email si pas trouvé par nom
    print("\n⚠️ Utilisateur 'Ali Hyjazi' non trouvé, recherche par email...")
    
    # Chercher tous les admins
    admins = list(db.users.find({"role": "admin"}))
    print(f"\n📋 Admins trouvés: {len(admins)}")
    for admin in admins:
        print(f"   - {admin.get('firstName', 'N/A')} {admin.get('lastName', 'N/A')} ({admin.get('email')})")
    
    # Si c'est l'email yafoy2310@gmail.com
    user = db.users.find_one({"email": "yafoy2310@gmail.com"})
    if user:
        print(f"\n✅ Utilisateur trouvé par email:")
        print(f"   Email: {user.get('email')}")
        print(f"   Nom actuel: {user.get('firstName')} {user.get('lastName')}")
        
        result = db.users.update_one(
            {"id": user['id']},
            {"$set": {
                "firstName": "Moka",
                "lastName": "",
                "updatedAt": datetime.utcnow()
            }}
        )
        
        if result.modified_count > 0:
            print(f"\n✅ Nom changé avec succès!")
            print(f"   Nouveau nom: Moka")
        else:
            print("\n⚠️ Nom peut-être déjà 'Moka'")

print("\n" + "=" * 80)
print("✅ TERMINÉ!")
print("=" * 80)
