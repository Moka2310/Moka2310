"""
Script pour récupérer les Chat IDs de tous les canaux/groupes où le bot est membre
"""
import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

async def get_all_channels():
    """Récupère tous les canaux/groupes où le bot est membre"""
    
    print("🔍 Récupération de tous les canaux où le bot est administrateur...\n")
    print("=" * 70)
    
    async with httpx.AsyncClient() as client:
        # Récupérer les mises à jour récentes
        response = await client.get(f"{BASE_URL}/getUpdates", timeout=10.0)
        
        if response.status_code != 200:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return
        
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Erreur API: {data.get('description')}")
            return
        
        updates = data.get('result', [])
        
        if not updates:
            print("⚠️  Aucune mise à jour trouvée.")
            print("\n💡 SOLUTION: Envoyez un message dans chacun de vos 6 canaux,")
            print("   puis relancez ce script.\n")
            return
        
        # Extraire tous les chats uniques
        channels = {}
        
        for update in updates:
            # Vérifier différents types de messages
            message = update.get('message') or update.get('channel_post') or update.get('my_chat_member')
            
            if message and 'chat' in message:
                chat = message['chat']
                chat_id = chat.get('id')
                chat_type = chat.get('type')
                chat_title = chat.get('title', 'Sans titre')
                
                # On garde seulement les groupes et canaux (pas les conversations privées)
                if chat_type in ['group', 'supergroup', 'channel']:
                    channels[chat_id] = {
                        'id': chat_id,
                        'title': chat_title,
                        'type': chat_type
                    }
        
        if not channels:
            print("⚠️  Aucun canal/groupe trouvé dans les mises à jour récentes.")
            print("\n💡 SOLUTION: Envoyez un message dans chacun de vos 6 canaux,")
            print("   puis relancez ce script.\n")
            return
        
        print(f"✅ {len(channels)} canal(aux)/groupe(s) trouvé(s):\n")
        
        # Afficher les résultats
        for i, (chat_id, info) in enumerate(channels.items(), 1):
            print(f"{i}. 📢 {info['title']}")
            print(f"   Chat ID: {chat_id}")
            print(f"   Type: {info['type']}")
            
            # Vérifier si le bot est admin
            try:
                admin_response = await client.get(
                    f"{BASE_URL}/getChatMember",
                    params={
                        "chat_id": chat_id,
                        "user_id": (await get_bot_info(client))['id']
                    },
                    timeout=5.0
                )
                
                if admin_response.status_code == 200:
                    admin_data = admin_response.json()
                    if admin_data.get('ok'):
                        member = admin_data.get('result', {})
                        status = member.get('status')
                        
                        if status in ['administrator', 'creator']:
                            print(f"   Status: ✅ Administrateur")
                            
                            # Vérifier les permissions
                            if 'can_invite_users' in member:
                                can_invite = member.get('can_invite_users', False)
                                print(f"   Permission d'inviter: {'✅ Oui' if can_invite else '❌ Non'}")
                        else:
                            print(f"   Status: ⚠️  {status} (pas admin)")
                
            except Exception as e:
                print(f"   Status: ⚠️  Impossible de vérifier ({str(e)})")
            
            print()
        
        print("=" * 70)
        print("\n📋 Configuration à ajouter dans votre .env:\n")
        
        # Générer la configuration
        for i, (chat_id, info) in enumerate(channels.items(), 1):
            safe_title = info['title'].replace(' ', '_').replace('-', '_')
            print(f"TELEGRAM_CHANNEL_{i}_{safe_title.upper()}={chat_id}")
        
        print("\n" + "=" * 70)
        
        # Sauvegarder dans un fichier
        with open('/app/telegram_channels_config.txt', 'w') as f:
            f.write("Configuration des canaux Telegram\n")
            f.write("=" * 70 + "\n\n")
            
            for i, (chat_id, info) in enumerate(channels.items(), 1):
                f.write(f"Canal {i}: {info['title']}\n")
                f.write(f"Chat ID: {chat_id}\n")
                f.write(f"Type: {info['type']}\n\n")
            
            f.write("\nConfiguration .env:\n")
            f.write("-" * 70 + "\n")
            for i, (chat_id, info) in enumerate(channels.items(), 1):
                safe_title = info['title'].replace(' ', '_').replace('-', '_')
                f.write(f"TELEGRAM_CHANNEL_{i}_{safe_title.upper()}={chat_id}\n")
        
        print(f"\n💾 Configuration sauvegardée dans: /app/telegram_channels_config.txt")

async def get_bot_info(client):
    """Récupère les informations du bot"""
    response = await client.get(f"{BASE_URL}/getMe", timeout=5.0)
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            return data.get('result')
    return {}

if __name__ == "__main__":
    asyncio.run(get_all_channels())
