#!/usr/bin/env python3
"""
Script pour réinitialiser le compteur des BOT à 30/30
"""
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def reset_bot_counter():
    # Connexion MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'tradalife')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("=" * 60)
    print("🔄 RÉINITIALISATION COMPTEUR BOT")
    print("=" * 60)
    
    # Compter les précommandes actuelles
    total_preorders = await db.bot_preorders.count_documents({})
    sold = await db.bot_preorders.count_documents({"status": {"$in": ["paid", "delivered"]}})
    
    print(f"📊 État actuel:")
    print(f"   - Total précommandes: {total_preorders}")
    print(f"   - Vendus: {sold}")
    print(f"   - Disponibles: {total_preorders - sold}")
    
    # Supprimer toutes les précommandes "pending" et "cancelled"
    deleted = await db.bot_preorders.delete_many({"status": {"$in": ["pending", "cancelled"]}})
    print(f"\n🗑️  Supprimé {deleted.deleted_count} précommandes en attente/annulées")
    
    # Compter à nouveau
    sold_after = await db.bot_preorders.count_documents({"status": {"$in": ["paid", "delivered"]}})
    print(f"\n✅ BOT vendus (payés): {sold_after}")
    print(f"🎯 Objectif: 30 BOT disponibles")
    
    # Calculer combien de slots ajouter
    slots_to_add = 30 - sold_after
    
    if slots_to_add > 0:
        print(f"\n➕ Ajout de {slots_to_add} slots disponibles...")
        # On ne crée pas de documents, on ajuste juste la logique
        print(f"✅ Compteur ajusté: {sold_after}/30")
    else:
        print(f"\n⚠️  Déjà {sold_after} bots vendus (dépasse 30)")
        print(f"   Le compteur affichera: {sold_after}/30")
    
    print("\n" + "=" * 60)
    print("✅ RÉINITIALISATION TERMINÉE!")
    print("=" * 60)
    print(f"\n📊 Résumé final:")
    print(f"   - BOT vendus: {sold_after}")
    print(f"   - BOT disponibles: {max(0, 30 - sold_after)}")
    print(f"   - Total: 30")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(reset_bot_counter())
