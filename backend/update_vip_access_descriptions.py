#!/usr/bin/env python3
"""
Script pour ajouter les informations d'accès VIP aux formations ULTRA et PREMIUM
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def update_formations_vip_access():
    # Connect to MongoDB using environment variables
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("🔧 MISE À JOUR DES DESCRIPTIONS - ACCÈS VIP")
    print("=" * 60)
    
    # VIP access information in French and English
    vip_info_fr = """

⏰ ACCÈS VIP TELEGRAM :
• 1 mois d'accès inclus aux canaux VIP Telegram
• Après 1 mois, abonnement requis pour continuer l'accès aux signaux"""

    vip_info_en = """

⏰ VIP TELEGRAM ACCESS:
• 1 month of VIP Telegram channel access included
• After 1 month, subscription required to continue signal access"""
    
    # Get ULTRA formation
    ultra_formation = await db.formations.find_one({'title': 'Tradalife Ultra Adhésion'})
    if ultra_formation:
        # Update French description
        current_desc_fr = ultra_formation.get('description', '')
        if '⏰ ACCÈS VIP TELEGRAM' not in current_desc_fr:
            new_desc_fr = current_desc_fr + vip_info_fr
            
            await db.formations.update_one(
                {'title': 'Tradalife Ultra Adhésion'},
                {'$set': {'description': new_desc_fr}}
            )
            print(f"✅ 'Tradalife Ultra Adhésion' - Description FR mise à jour")
        else:
            print(f"ℹ️  'Tradalife Ultra Adhésion' - Description FR déjà à jour")
    else:
        print(f"⚠️  Formation 'Tradalife Ultra Adhésion' non trouvée")
    
    # Get PREMIUM formation
    premium_formation = await db.formations.find_one({'title': 'Tradalife Premium Membership'})
    if premium_formation:
        # Update French description
        current_desc_fr = premium_formation.get('description', '')
        if '⏰ ACCÈS VIP TELEGRAM' not in current_desc_fr:
            new_desc_fr = current_desc_fr + vip_info_fr
            
            await db.formations.update_one(
                {'title': 'Tradalife Premium Membership'},
                {'$set': {'description': new_desc_fr}}
            )
            print(f"✅ 'Tradalife Premium Membership' - Description FR mise à jour")
        else:
            print(f"ℹ️  'Tradalife Premium Membership' - Description FR déjà à jour")
    else:
        print(f"⚠️  Formation 'Tradalife Premium Membership' non trouvée")
    
    print("\n" + "=" * 60)
    print("✅ Mise à jour terminée!")
    print("=" * 60)
    print("\n📝 Note: Les descriptions dans translations.js doivent également être mises à jour manuellement.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_formations_vip_access())
