"""
Script pour extraire les Chat IDs depuis les liens d'invitation
"""
import os
import httpx
import asyncio
import re
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Vos canaux avec leurs liens
CHANNELS = {
    "INDICES": "https://t.me/+Z0h36lgNatQxMjFh",
    "ACTIONS": "https://t.me/+GBRYqMdHZ4c0YzYx",
    "GOLD": "https://t.me/+BWpLllZBIpxjMWE5",
    "FOREX": "https://t.me/+naLR-gXJl8MzZGJh",
    "CRYPTO": "https://t.me/+7NNOp2XGXcpiMDdh",
    "COMMODITES": "https://t.me/+MXfEUYj4D2oxZGJh"
}

async def get_channel_info_from_link(channel_name, invite_link):
    """
    Tente de récupérer les infos d'un canal via son lien d'invitation
    """
    print(f"\n🔍 Recherche du Chat ID pour: {channel_name}")
    print(f"   Lien: {invite_link}")
    
    # Extraire le code d'invitation
    if '+' in invite_link:
        invite_code = invite_link.split('+')[1]
    elif 'joinchat/' in invite_link:
        invite_code = invite_link.split('joinchat/')[1]
    else:
        print(f"   ❌ Format de lien non reconnu\n")
        return None
    
    # Malheureusement, l'API Telegram ne permet pas de récupérer le Chat ID
    # directement depuis un lien d'invitation sans rejoindre le canal
    
    print(f"   ⚠️  Impossible de récupérer le Chat ID automatiquement")
    print(f"   📝 Code d'invitation: {invite_code}")
    
    return None

async def get_chat_ids_manual():
    """
    Guide manuel pour obtenir les Chat IDs
    """
    
    print("\n" + "="*70)
    print("📋 MÉTHODE MANUELLE POUR OBTENIR LES CHAT IDS")
    print("="*70 + "\n")
    
    print("Malheureusement, l'API Telegram ne permet pas de récupérer")
    print("automatiquement les Chat IDs depuis des liens d'invitation.\n")
    
    print("🔧 SOLUTION SIMPLE:\n")
    print("1. Dans CHAQUE canal, faites votre bot POSTER un message")
    print("   (Vous pouvez utiliser 'Send as Channel' si disponible)\n")
    
    print("2. Ou utilisez cette méthode Telegram Desktop:\n")
    print("   a. Ouvrez Telegram Desktop (pas mobile)")
    print("   b. Clic droit sur le canal → 'Copy Link'")
    print("   c. Le lien ressemblera à: https://t.me/c/1234567890/1")
    print("   d. Le nombre après /c/ est votre Chat ID")
    print("   e. Ajoutez -100 devant: -1001234567890\n")
    
    print("="*70)
    print("\n🎯 ESSAYONS UNE AUTRE APPROCHE...\n")
    
    # Tenter de récupérer depuis les updates avec plus d'infos
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/getUpdates",
            params={"limit": 100, "allowed_updates": ["channel_post", "message"]},
            timeout=15.0
        )
        
        if response.status_code == 200:
            data = response.json()
            updates = data.get('result', [])
            
            print(f"📊 Nombre total de mises à jour: {len(updates)}\n")
            
            channels_found = {}
            
            for update in updates:
                # Chercher les channel_post
                channel_post = update.get('channel_post')
                if channel_post and 'chat' in channel_post:
                    chat = channel_post['chat']
                    chat_id = chat.get('id')
                    chat_title = chat.get('title', 'Sans titre')
                    
                    if chat_id and 'TRADALIFE' in chat_title.upper():
                        channels_found[chat_id] = chat_title
            
            if channels_found:
                print("✅ CANAUX TRADALIFE DÉTECTÉS:\n")
                for chat_id, title in channels_found.items():
                    print(f"   📢 {title}")
                    print(f"   📍 Chat ID: {chat_id}\n")
            else:
                print("⚠️  Aucun canal post détecté dans les updates récentes.\n")
                print("💡 Postez un nouveau message dans chaque canal et relancez ce script.\n")

if __name__ == "__main__":
    asyncio.run(get_chat_ids_manual())
