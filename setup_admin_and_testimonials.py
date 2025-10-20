import requests
import json

print("="*60)
print("🚀 CONFIGURATION ADMIN ET TÉMOIGNAGES")
print("="*60)

base_url = "https://tradalife.com/api"

# 1. Promouvoir l'utilisateur en admin
print("\n1️⃣ Promotion du compte en administrateur...")
try:
    response = requests.post(
        f"{base_url}/admin/promote-user",
        json={
            "email": "yafoy2310@gmail.com",
            "secret_key": "tradalife-admin-promote-2025"
        },
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ Erreur: {str(e)}")

# 2. Ajouter les témoignages
print("\n2️⃣ Ajout des témoignages...")
try:
    response = requests.post(
        f"{base_url}/admin/add-default-testimonials",
        json={
            "secret_key": "tradalife-admin-promote-2025"
        },
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   ❌ Erreur: {str(e)}")

print("\n" + "="*60)
print("✅ TERMINÉ ! Rafraîchissez tradalife.com")
print("="*60)
