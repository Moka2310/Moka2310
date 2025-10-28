"""
Script pour mettre à jour les précommandes de test à 2$ CAD
"""
import os
import sys
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
env_path = '/app/backend/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

def main():
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ ERROR: MONGO_URL not found")
        sys.exit(1)
    
    client = MongoClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'tradalife')]
    
    print("=" * 80)
    print("🔄 MISE À JOUR DES PRÉCOMMANDES DE TEST À 2$ CAD")
    print("=" * 80)
    
    # Mettre à jour toutes les précommandes réelles qui ne sont pas à 2$ CAD
    result = db.bot_preorders.update_many(
        {
            "userId": {"$not": {"$regex": "^fake_user"}},
            "price": {"$ne": 2.0}
        },
        {
            "$set": {
                "price": 2.0,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    
    print(f"✅ {result.modified_count} précommandes réelles mises à jour à 2$ CAD\n")
    
    # Afficher toutes les précommandes réelles pour vérification
    real_preorders = list(db.bot_preorders.find({"userId": {"$not": {"$regex": "^fake_user"}}}))
    print(f"📊 TOUTES LES PRÉCOMMANDES RÉELLES ({len(real_preorders)}):")
    print("-" * 80)
    for p in real_preorders:
        print(f"  • {p.get('userEmail', 'N/A'):40s} | Prix: {p.get('price', 0)} CAD | Status: {p.get('status')}")
    
    print("\n" + "=" * 80)
    print("✅ TERMINÉ!")
    print("=" * 80)

if __name__ == "__main__":
    main()
