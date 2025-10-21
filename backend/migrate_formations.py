#!/usr/bin/env python3
"""
Script de migration pour mettre à jour les formations en production
S'exécute automatiquement au démarrage du backend
"""
import os
from pymongo import MongoClient
import asyncio

async def migrate_formations():
    """Mise à jour des formations avec les bonnes images et suppression de la formation à 1799"""
    
    # Connexion MongoDB (utilise la variable d'environnement)
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = MongoClient(MONGO_URL)
    db = client.tradalife
    
    print("🔄 Migration des formations...")
    
    try:
        # Supprimer la formation à 1799 CAD
        result_delete = db.formations.delete_many({"price": 1799.0})
        print(f"✅ Formations à 1799 CAD supprimées: {result_delete.deleted_count}")
        
        # Mettre à jour l'image de la formation Ultra (1100 CAD)
        result_ultra = db.formations.update_many(
            {"price": 1100.0},
            {"$set": {"image": "https://i.imgur.com/0wGvLuk.jpg"}}
        )
        print(f"✅ Formation Ultra mise à jour: {result_ultra.modified_count}")
        
        # Mettre à jour l'image de la formation Premium (700 CAD)
        result_premium = db.formations.update_many(
            {"price": 700.0},
            {"$set": {"image": "https://i.imgur.com/CcllRfh.jpg"}}
        )
        print(f"✅ Formation Premium mise à jour: {result_premium.modified_count}")
        
        # Vérifier le résultat
        formations = list(db.formations.find({}, {"_id": 0, "title": 1, "price": 1, "image": 1}))
        print(f"\n📊 Formations finales: {len(formations)}")
        for f in formations:
            print(f"  - {f['title']} ({f['price']} CAD)")
            print(f"    Image: {f['image']}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(migrate_formations())
