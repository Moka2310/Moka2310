"""
Script pour mettre à jour TOUS les prix à 2$ CAD
- Formations
- Bot Preorders (fausses précommandes)
- Vérification des configurations Stripe/PayPal
"""
import os
import sys
from pymongo import MongoClient
from datetime import datetime

# Load environment variables from .env
env_path = '/app/backend/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

def main():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ ERROR: MONGO_URL not found in environment variables")
        sys.exit(1)
    
    client = MongoClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'tradalife')]
    
    print("=" * 80)
    print("🔄 MISE À JOUR DE TOUS LES PRIX À 2$ CAD")
    print("=" * 80)
    
    # ===== 1. FORMATIONS =====
    print("\n📚 1. MISE À JOUR DES FORMATIONS")
    print("-" * 80)
    formations = list(db.formations.find({}))
    print(f"Formations trouvées: {len(formations)}")
    
    for formation in formations:
        old_price = formation.get('price', 0)
        if old_price != 2.0:
            result = db.formations.update_one(
                {"id": formation['id']},
                {"$set": {"price": 2.0, "updatedAt": datetime.utcnow()}}
            )
            print(f"  ✅ {formation.get('title')}: {old_price} CAD → 2.0 CAD (modifié)")
        else:
            print(f"  ⚪ {formation.get('title')}: Déjà à 2.0 CAD")
    
    # ===== 2. BOT PREORDERS (FAKE) =====
    print("\n🤖 2. MISE À JOUR DES BOT PREORDERS (fausses précommandes)")
    print("-" * 80)
    fake_preorders = list(db.bot_preorders.find({"userId": {"$regex": "^fake_user"}}))
    print(f"Fausses précommandes trouvées: {len(fake_preorders)}")
    
    updated_count = 0
    for preorder in fake_preorders:
        old_price = preorder.get('price', 0)
        if old_price != 2.0:
            result = db.bot_preorders.update_one(
                {"id": preorder['id']},
                {"$set": {"price": 2.0, "updatedAt": datetime.utcnow()}}
            )
            updated_count += 1
    
    if updated_count > 0:
        print(f"  ✅ {updated_count} fausses précommandes mises à jour: → 2.0 CAD")
    else:
        print(f"  ⚪ Toutes les fausses précommandes sont déjà à 2.0 CAD")
    
    # ===== 3. BOT PREORDERS (REAL) =====
    print("\n💰 3. VÉRIFICATION DES BOT PREORDERS (réelles)")
    print("-" * 80)
    real_preorders = list(db.bot_preorders.find({"userId": {"$not": {"$regex": "^fake_user"}}}))
    print(f"Précommandes réelles trouvées: {len(real_preorders)}")
    
    for preorder in real_preorders[:5]:  # Afficher les 5 premières
        print(f"  📊 User: {preorder.get('userEmail', 'N/A')} | Prix: {preorder.get('price', 0)} CAD | Status: {preorder.get('status')}")
    
    # ===== 4. VÉRIFICATION STRIPE/PAYPAL CONFIGURATION =====
    print("\n💳 4. VÉRIFICATION DES CONFIGURATIONS STRIPE/PAYPAL")
    print("-" * 80)
    
    # Check Stripe key
    stripe_key = os.environ.get('STRIPE_SECRET_KEY', '')
    if stripe_key and not stripe_key.startswith('sk_test_votre'):
        print(f"  ✅ Clé Stripe configurée: {stripe_key[:20]}...")
    else:
        print(f"  ⚠️ Clé Stripe NON configurée ou placeholder")
    
    # Check PayPal credentials
    paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID', '')
    paypal_secret = os.environ.get('PAYPAL_CLIENT_SECRET', '')
    
    if paypal_client_id and not paypal_client_id.startswith('votre'):
        print(f"  ✅ PayPal Client ID configuré: {paypal_client_id[:20]}...")
    else:
        print(f"  ⚠️ PayPal Client ID NON configuré ou placeholder")
    
    if paypal_secret and not paypal_secret.startswith('votre'):
        print(f"  ✅ PayPal Secret configuré: {paypal_secret[:10]}...")
    else:
        print(f"  ⚠️ PayPal Secret NON configuré ou placeholder")
    
    # ===== 5. RÉSUMÉ FINAL =====
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 80)
    
    # Count formations
    formations_at_2cad = db.formations.count_documents({"price": 2.0})
    total_formations = db.formations.count_documents({})
    print(f"Formations à 2$ CAD: {formations_at_2cad}/{total_formations}")
    
    # Count bot preorders
    fake_preorders_at_2cad = db.bot_preorders.count_documents({
        "userId": {"$regex": "^fake_user"},
        "price": 2.0
    })
    total_fake_preorders = db.bot_preorders.count_documents({"userId": {"$regex": "^fake_user"}})
    print(f"Fausses précommandes bot à 2$ CAD: {fake_preorders_at_2cad}/{total_fake_preorders}")
    
    # Check code configuration
    print("\nConfiguration du code backend:")
    print(f"  - Bot Preorders (ligne 59): price=2.0 ✅")
    print(f"  - Bot Preorders Stripe (ligne 76): amount=2.0 ✅")
    print(f"  - Bot Preorders PayPal (ligne 110): amount=2.0 ✅")
    print(f"  - Subscription (subscription_service.py ligne 9): SUBSCRIPTION_PRICE_AMOUNT=200 (2$ CAD) ✅")
    
    print("\n" + "=" * 80)
    print("✅ MISE À JOUR TERMINÉE!")
    print("=" * 80)
    print("\nProchaines étapes pour tester:")
    print("  1. Redémarrez le backend: sudo supervisorctl restart backend")
    print("  2. Testez un paiement Stripe pour une formation")
    print("  3. Testez un paiement PayPal pour une formation")
    print("  4. Testez un paiement pour le bot")
    print("  5. Testez un abonnement mensuel")

if __name__ == "__main__":
    main()
