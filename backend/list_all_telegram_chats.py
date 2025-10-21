"""
Script alternatif pour forcer la récupération de tous les canaux
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def get_bot_chats():
    """
    Instructions pour récupérer manuellement les Chat IDs
    """
    
    print("\n" + "="*70)
    print("📋 GUIDE POUR RÉCUPÉRER VOS CHAT IDS MANUELLEMENT")
    print("="*70 + "\n")
    
    print("Méthode 1 : Via Web Browser")
    print("-" * 70)
    print(f"1. Ouvrez ce lien dans votre navigateur :\n")
    print(f"   https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates\n")
    print(f"2. Vous verrez un JSON avec tous les messages récents")
    print(f"3. Cherchez 'chat':{'id': XXXXXXX} pour chaque canal\n")
    
    print("\nMéthode 2 : Via ce script")
    print("-" * 70)
    
    async with httpx.AsyncClient() as client:
        # Augmenter la limite et obtenir plus de updates
        response = await client.get(
            f"{BASE_URL}/getUpdates",
            params={"limit": 100, "offset": -100},
            timeout=15.0
        )
        
        if response.status_code != 200:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return
        
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Erreur API: {data.get('description')}")
            return
        
        updates = data.get('result', [])
        print(f"📊 Nombre de mises à jour trouvées: {len(updates)}\n")
        
        if not updates:
            print("⚠️  Aucune mise à jour. Le bot n'a reçu aucun message récemment.\n")
            print("💡 SOLUTION:")
            print("   1. Transférez un message au bot dans CHAQUE canal")
            print("   2. Ou tapez /start dans chaque canal")
            print("   3. Attendez 5 secondes")
            print("   4. Relancez ce script\n")
            return
        
        # Parser tous les chats
        all_chats = {}
        
        for update in updates:
            # Chercher dans tous les types possibles
            sources = [
                update.get('message'),
                update.get('channel_post'),
                update.get('edited_message'),
                update.get('edited_channel_post'),
                update.get('my_chat_member')
            ]
            
            for source in sources:
                if source and 'chat' in source:
                    chat = source['chat']
                    chat_id = chat.get('id')
                    
                    if chat_id and chat_id not in all_chats:
                        all_chats[chat_id] = {
                            'id': chat_id,
                            'title': chat.get('title', chat.get('first_name', 'Sans nom')),
                            'type': chat.get('type', 'unknown'),
                            'username': chat.get('username', 'N/A')
                        }
        
        print("=" * 70)
        print(f"📢 CANAUX/GROUPES DÉTECTÉS: {len(all_chats)}")
        print("=" * 70 + "\n")
        
        if all_chats:
            for i, (chat_id, info) in enumerate(all_chats.items(), 1):
                print(f"{i}. {info['title']}")
                print(f"   📍 Chat ID: {chat_id}")
                print(f"   📁 Type: {info['type']}")
                if info['username'] != 'N/A':
                    print(f"   🔗 Username: @{info['username']}")
                print()
            
            print("=" * 70)
            print("\n✅ COPIEZ CES CHAT IDs ET ENVOYEZ-LES MOI\n")
            
            # Sauvegarder
            with open('/app/telegram_all_chats.txt', 'w') as f:
                f.write("TOUS LES CHAT IDS DÉTECTÉS\n")
                f.write("=" * 70 + "\n\n")
                
                for i, (chat_id, info) in enumerate(all_chats.items(), 1):
                    f.write(f"{i}. {info['title']}\n")
                    f.write(f"   Chat ID: {chat_id}\n")
                    f.write(f"   Type: {info['type']}\n\n")
            
            print("💾 Liste sauvegardée dans: /app/telegram_all_chats.txt\n")
        
        else:
            print("⚠️  Aucun chat trouvé dans l'historique.\n")
            print("💡 Essayez ceci:")
            print("   1. Dans CHAQUE canal, mentionnez le bot: @votre_bot")
            print("   2. Ou envoyez la commande /start")
            print("   3. Relancez ce script après 10 secondes\n")

if __name__ == "__main__":
    asyncio.run(get_bot_chats())
