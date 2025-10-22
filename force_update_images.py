#!/usr/bin/env python3
"""
Script pour forcer la mise à jour des images des formations
À exécuter manuellement ou via déploiement
"""
import os
from pymongo import MongoClient

def force_update_formation_images():
    """Force la mise à jour des images dans toutes les bases de données"""
    
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    print(f"🔗 Connexion à MongoDB: {MONGO_URL}")
    
    client = MongoClient(MONGO_URL)
    db = client.tradalife
    
    print("\n📋 État AVANT mise à jour:")
    formations = list(db.formations.find({}, {"title": 1, "price": 1, "image": 1, "_id": 0}))
    for f in formations:
        print(f"  - {f.get('title', 'N/A')}: {f.get('image', 'N/A')}")
    
    print("\n🔄 Mise à jour des images...")
    
    # Supprimer la formation à 1799 CAD si elle existe
    result_delete = db.formations.delete_many({"price": 1799.0})
    print(f"✅ Formations à 1799 CAD supprimées: {result_delete.deleted_count}")
    
    # Mettre à jour Ultra (1100 CAD)
    result_ultra = db.formations.update_many(
        {"price": 1100.0},
        {"$set": {"image": "https://i.imgur.com/0wGvLuk.jpg"}}
    )
    print(f"✅ Formation Ultra mise à jour: {result_ultra.modified_count} documents")
    
    # Mettre à jour Premium (700 CAD)
    result_premium = db.formations.update_many(
        {"price": 700.0},
        {"$set": {"image": "https://i.imgur.com/CcllRfh.jpg"}}
    )
    print(f"✅ Formation Premium mise à jour: {result_premium.modified_count} documents")
    
    print("\n📋 État APRÈS mise à jour:")
    formations = list(db.formations.find({}, {"title": 1, "price": 1, "image": 1, "_id": 0}))
    for f in formations:
        print(f"  - {f.get('title', 'N/A')}: {f.get('image', 'N/A')}")
    
    client.close()
    print("\n✅ Mise à jour terminée!")

if __name__ == "__main__":
    force_update_formation_images()
