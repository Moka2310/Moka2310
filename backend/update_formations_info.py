#!/usr/bin/env python3
"""
Script pour mettre à jour les informations des formations (durée, vidéos, niveau)
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def update_formations():
    # Connect to MongoDB using environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("🔧 MISE À JOUR DES INFORMATIONS DES FORMATIONS")
    print("=" * 60)
    
    # Formations à mettre à jour avec leurs nouvelles valeurs
    formations_update = {
        'Formation Complète de Trading': {
            'duration': '8h',
            'videoCount': 10,
            'level': 'Avancé'
        },
        'Tradalife Ultra Adhésion': {
            'duration': '1h40',
            'videoCount': 2,
            'level': 'Débutant'
        },
        'Tradalife Premium Membership': {
            'duration': '1h40',
            'videoCount': 2,
            'level': 'Débutant'
        }
    }
    
    # Mettre à jour chaque formation
    for title, updates in formations_update.items():
        result = await db.formations.update_one(
            {'title': title},
            {'$set': updates}
        )
        
        if result.matched_count > 0:
            print(f"✅ '{title}' mise à jour:")
            print(f"   - Durée: {updates['duration']}")
            print(f"   - Vidéos: {updates['videoCount']}")
            print(f"   - Niveau: {updates['level']}")
        else:
            print(f"⚠️  Formation '{title}' non trouvée dans la base de données")
    
    print("\n" + "=" * 60)
    print("✅ Mise à jour terminée!")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_formations())
