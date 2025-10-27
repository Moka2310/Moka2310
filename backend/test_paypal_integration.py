"""
Script de test pour vérifier l'intégration PayPal REST API
"""
import asyncio
import sys
sys.path.append('/app/backend')

from paypal_rest_service import paypal_rest_service

async def test_paypal():
    print("=" * 80)
    print("🧪 TEST DE L'INTÉGRATION PAYPAL REST API")
    print("=" * 80)
    
    # Test 1: Get access token
    print("\n📝 Test 1: Obtenir le token d'accès...")
    try:
        token = paypal_rest_service._get_access_token()
        print(f"✅ Token obtenu: {token[:40]}...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # Test 2: Create product
    print("\n📝 Test 2: Créer un produit...")
    try:
        product_result = await paypal_rest_service.create_product(
            name="TEST PRODUCT - Signaux Trading",
            description="Test product for subscription plans"
        )
        
        if product_result.get("success"):
            product_id = product_result['data']['id']
            print(f"✅ Produit créé: {product_id}")
            
            # Test 3: Create billing plan
            print("\n📝 Test 3: Créer un plan de facturation...")
            plan_result = await paypal_rest_service.create_billing_plan(
                product_id=product_id,
                name="TEST PLAN - Abonnement 2$ CAD/mois",
                description="Plan de test pour abonnement mensuel",
                amount=2.0,
                currency="CAD"
            )
            
            if plan_result.get("success"):
                plan_id = plan_result['data']['id']
                print(f"✅ Plan créé: {plan_id}")
                print(f"   Status: {plan_result['data'].get('status')}")
                
                # Test 4: Create subscription
                print("\n📝 Test 4: Créer un abonnement...")
                sub_result = await paypal_rest_service.create_subscription(
                    plan_id=plan_id,
                    return_url="https://tradalife.com/success",
                    cancel_url="https://tradalife.com/cancel"
                )
                
                if sub_result.get("success"):
                    print(f"✅ Abonnement créé: {sub_result['subscription_id']}")
                    print(f"   Approval URL: {sub_result['approval_url'][:60]}...")
                    print(f"   Status: {sub_result['status']}")
                else:
                    print(f"❌ Erreur création abonnement: {sub_result.get('error')}")
                    
            else:
                print(f"❌ Erreur création plan: {plan_result.get('error')}")
        else:
            print(f"❌ Erreur création produit: {product_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ TEST TERMINÉ")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_paypal())
