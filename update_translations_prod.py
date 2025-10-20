"""
Script à exécuter APRÈS le déploiement pour ajouter les traductions
"""
import requests

print("=" * 60)
print("🌍 MISE À JOUR DES TRADUCTIONS - PRODUCTION")
print("=" * 60)

response = requests.post(
    "https://tradalife.com/api/admin/update-testimonial-translations",
    json={"secret_key": "tradalife-admin-promote-2025"},
    timeout=30
)

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ {data['message']}")
    print(f"   Témoignages mis à jour: {', '.join(data['updated'])}")
else:
    print(f"\n❌ Erreur {response.status_code}: {response.text}")

print("\n" + "=" * 60)
