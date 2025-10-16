# 🔑 Guide de configuration des clés API

## 1. Configuration Stripe

### Étape 1 : Créer/Accéder à votre compte Stripe
1. Aller sur https://dashboard.stripe.com
2. Se connecter avec votre compte

### Étape 2 : Obtenir les clés API
1. Dans le dashboard, cliquer sur **"Developers"** (en haut à droite)
2. Cliquer sur **"API keys"**
3. Vous verrez 2 types de clés :
   - **Publishable key** (commence par `pk_test_...` ou `pk_live_...`)
   - **Secret key** (commence par `sk_test_...` ou `sk_live_...`)

### Étape 3 : Configurer dans votre application

#### Backend (`/app/backend/.env`) :
```bash
STRIPE_SECRET_KEY=sk_test_votre_vraie_cle_ici
```

#### Frontend (à ajouter dans `/app/frontend/.env`) :
```bash
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_votre_vraie_cle_ici
```

### Mode Test vs Live
- **Test** : Utiliser les clés avec `test`
- **Production** : Utiliser les clés avec `live`

---

## 2. Configuration PayPal

### Étape 1 : Créer une application PayPal
1. Aller sur https://developer.paypal.com
2. Se connecter avec votre compte PayPal
3. Cliquer sur **"Dashboard"**
4. Cliquer sur **"My Apps & Credentials"**

### Étape 2 : Créer une app
1. Sous **"REST API apps"**, cliquer sur **"Create App"**
2. Donner un nom à votre app (ex: "Tradalife")
3. Cliquer sur **"Create App"**

### Étape 3 : Obtenir les credentials
Vous verrez :
- **Client ID** : Votre identifiant
- **Secret** : Votre clé secrète (cliquer sur "Show" pour la voir)

### Étape 4 : Configurer dans votre application

#### Backend (`/app/backend/.env`) :
```bash
# Mode sandbox pour les tests
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=votre_client_id_ici
PAYPAL_CLIENT_SECRET=votre_secret_ici

# Mode live pour la production
# PAYPAL_MODE=live
# PAYPAL_CLIENT_ID=votre_client_id_live
# PAYPAL_CLIENT_SECRET=votre_secret_live
```

---

## 3. Configuration Gmail (Envoi d'emails)

### Étape 1 : Activer l'authentification à 2 facteurs
1. Aller sur https://myaccount.google.com/security
2. Activer **"Validation en deux étapes"**

### Étape 2 : Créer un mot de passe d'application
1. Aller sur https://myaccount.google.com/apppasswords
2. Sélectionner **"Autre (nom personnalisé)"**
3. Entrer **"Tradalife"**
4. Cliquer sur **"Générer"**
5. **COPIER** le mot de passe de 16 caractères généré

### Étape 3 : Configurer dans votre application

#### Backend (`/app/backend/.env`) :
```bash
GMAIL_EMAIL=votre-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # Le mot de passe de 16 caractères
```

**Note** : Le mot de passe d'application est différent de votre mot de passe Gmail normal !

---

## 4. Tester la configuration

### Test Stripe
```bash
curl -X POST https://videocourse.preview.emergentagent.com/api/purchases/create \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"formationId":"1","paymentMethod":"stripe"}'
```

### Test PayPal
```bash
curl -X POST https://videocourse.preview.emergentagent.com/api/purchases/create \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"formationId":"1","paymentMethod":"paypal"}'
```

### Test Email
1. S'inscrire avec un nouvel email
2. Vérifier que vous recevez l'email de bienvenue

---

## 5. Appliquer les modifications

Après avoir modifié `/app/backend/.env` :

```bash
# Redémarrer le backend pour charger les nouvelles variables
sudo supervisorctl restart backend

# Vérifier que tout fonctionne
tail -f /var/log/supervisor/backend.out.log
```

---

## 6. Sécurité - IMPORTANT ⚠️

### Ne JAMAIS :
- ❌ Commiter les fichiers `.env` sur Git
- ❌ Partager vos clés secrètes publiquement
- ❌ Utiliser les clés de production en développement

### Toujours :
- ✅ Utiliser les variables d'environnement
- ✅ Utiliser le mode test/sandbox en développement
- ✅ Changer les clés si elles sont compromises
- ✅ Activer HTTPS en production

---

## 7. Webhooks (Optionnel mais recommandé)

### Stripe Webhooks
Pour recevoir automatiquement les notifications de paiement :

1. Dans Stripe Dashboard → **"Developers"** → **"Webhooks"**
2. Cliquer sur **"Add endpoint"**
3. URL : `https://votredomaine.com/api/webhooks/stripe`
4. Événements à écouter :
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Copier le **"Signing secret"**

Ajouter dans `.env` :
```bash
STRIPE_WEBHOOK_SECRET=whsec_votre_secret_ici
```

### PayPal Webhooks
1. Dans PayPal Dashboard → **"Webhooks"**
2. Créer un webhook
3. URL : `https://votredomaine.com/api/webhooks/paypal`
4. Événements :
   - `PAYMENT.SALE.COMPLETED`
   - `PAYMENT.SALE.DENIED`

---

## 8. Vérification rapide

### Checklist ✅

- [ ] Clé Stripe configurée
- [ ] Clé PayPal configurée
- [ ] Email Gmail configuré
- [ ] Mot de passe d'application Gmail créé
- [ ] Backend redémarré
- [ ] Test d'inscription → email reçu
- [ ] Test d'achat Stripe
- [ ] Test d'achat PayPal

---

## 9. Troubleshooting

### Erreur "Invalid API Key" (Stripe)
- Vérifier que la clé commence par `sk_test_` ou `sk_live_`
- Vérifier qu'il n'y a pas d'espace avant/après

### Erreur PayPal "Authentication failed"
- Vérifier que `PAYPAL_MODE` est bien `sandbox` ou `live`
- Vérifier Client ID et Secret

### Email non reçu
- Vérifier que le mot de passe d'application est correct (16 caractères)
- Vérifier dans les spams
- Tester avec `tail -f /var/log/supervisor/backend.err.log`

### Voir les logs d'erreur
```bash
# Logs backend
tail -f /var/log/supervisor/backend.err.log

# Logs MongoDB
tail -f /var/log/mongodb/mongod.log
```

---

## 10. Contact support

Si vous avez des problèmes :
1. Vérifier les logs : `tail -f /var/log/supervisor/backend.err.log`
2. Tester les clés API avec curl
3. Vérifier que toutes les variables sont bien dans `.env`
4. Redémarrer : `sudo supervisorctl restart all`
