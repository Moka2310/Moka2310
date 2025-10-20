"""
Script pour obtenir l'ID de votre groupe Telegram
"""
import asyncio
import httpx
import os

TELEGRAM_BOT_TOKEN = "8406540414:AAG-IlyhG5eL0BjSkvaJhZ2qCrngRETCHpc"

async def get_updates():
    """Récupère les derniers messages/événements du bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            data = response.json()
            
            if data.get('ok'):
                updates = data.get('result', [])
                
                if not updates:
                    print("❌ Aucun message trouvé!")
                    print("\n📝 INSTRUCTIONS:")
                    print("1. Ajoutez votre bot au groupe Telegram")
                    print("2. Faites-en un administrateur")
                    print("3. Envoyez un message dans le groupe (ex: /start)")
                    print("4. Réexécutez ce script\n")
                    return
                
                print("\n" + "="*60)
                print("📱 GROUPES/CANAUX TELEGRAM DÉTECTÉS")
                print("="*60 + "\n")
                
                seen_chats = set()
                
                for update in updates:
                    # Vérifier les messages
                    if 'message' in update:
                        chat = update['message']['chat']
                        chat_id = chat['id']
                        
                        if chat_id not in seen_chats:
                            seen_chats.add(chat_id)
                            print(f"Chat ID: {chat_id}")
                            print(f"Type: {chat.get('type')}")
                            print(f"Titre: {chat.get('title', 'N/A')}")
                            print(f"Username: @{chat.get('username', 'N/A')}")
                            print("-" * 60)
                    
                    # Vérifier les nouveaux membres
                    if 'my_chat_member' in update:
                        chat = update['my_chat_member']['chat']
                        chat_id = chat['id']
                        
                        if chat_id not in seen_chats:
                            seen_chats.add(chat_id)
                            print(f"Chat ID: {chat_id}")
                            print(f"Type: {chat.get('type')}")
                            print(f"Titre: {chat.get('title', 'N/A')}")
                            print(f"Username: @{chat.get('username', 'N/A')}")
                            print("-" * 60)
                
                if seen_chats:
                    print("\n✅ Copiez l'ID du groupe que vous voulez utiliser")
                    print("   (Les IDs de groupe commencent généralement par -100)")
                else:
                    print("❌ Aucun groupe trouvé. Suivez les instructions ci-dessus.")
                    
            else:
                print(f"❌ Erreur API: {data.get('description')}")
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(get_updates())
