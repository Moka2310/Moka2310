# 🔒 Guide de Configuration SÉCURISÉE - Clés API

## ⚠️ IMPORTANT : Ne partagez JAMAIS vos clés API dans le chat !

Ce guide vous permet de configurer vos clés API de manière 100% sécurisée.

---

## ÉTAPE 1 : Collecter vos clés API

Avant de commencer, assurez-vous d'avoir toutes ces informations :

### ✅ Stripe (2 clés nécessaires)
- [ ] Secret Key (commence par `sk_live_...` ou `sk_test_...`)
- [ ] Publishable Key (commence par `pk_live_...` ou `pk_test_...`)

**Où les trouver ?** https://dashboard.stripe.com/apikeys

### ✅ PayPal (2 clés + 1 mode)
- [ ] Client ID
- [ ] Secret
- [ ] Mode : `live` (production) ou `sandbox` (test)

**Où les trouver ?** https://developer.paypal.com/dashboard → My Apps & Credentials

### ✅ Gmail (email + mot de passe d'application)
- [ ] Votre email Gmail complet
- [ ] Mot de passe d'application (16 caractères avec espaces)

**Où le créer ?** https://myaccount.google.com/apppasswords
(Vous devez d'abord activer la validation en 2 étapes)

---

## ÉTAPE 2 : Accéder au fichier de configuration

### Sur la plateforme Emergent :

**Option A : Via l'éditeur de fichiers (Interface graphique)**
1. Aller dans "Files" ou "Explorateur de fichiers"
2. Naviguer vers `/app/backend/.env`
3. Cliquer sur le fichier pour l'ouvrir
4. Cliquer sur "Edit" ou "Éditer"

**Option B : Via le terminal**
```bash
nano /app/backend/.env
```

---

## ÉTAPE 3 : Modifier le fichier .env

Dans le fichier `/app/backend/.env`, vous allez voir plusieurs lignes.

**Trouvez ces lignes et remplacez les valeurs :**

### 1️⃣ Configuration Stripe

Cherchez ces lignes :
```bash
STRIPE_SECRET_KEY=sk_test_votre_cle_stripe_ici
```

Remplacez par :
```bash
STRIPE_SECRET_KEY=sk_live_VOTRE_VRAIE_CLE_SECRETE
```

**⚠️ Utilisez la clé qui commence par `sk_live_` (ou `sk_test_` pour tester)**

---

### 2️⃣ Configuration PayPal

Cherchez ces lignes :
```bash
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=votre_client_id_paypal
PAYPAL_CLIENT_SECRET=votre_secret_paypal
```

Remplacez par :
```bash
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=VOTRE_VRAI_CLIENT_ID
PAYPAL_CLIENT_SECRET=VOTRE_VRAI_SECRET
```

**💡 Pour tester d'abord : laissez `PAYPAL_MODE=sandbox` et utilisez vos clés de test**

---

### 3️⃣ Configuration Gmail

Cherchez ces lignes :
```bash
GMAIL_EMAIL=votre-email@gmail.com
GMAIL_APP_PASSWORD=votre_mot_de_passe_app_gmail
```

Remplacez par :
```bash
GMAIL_EMAIL=votre-email-reel@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

**⚠️ Important :** 
- Utilisez votre vrai email Gmail
- Le mot de passe doit être le mot de passe d'APPLICATION (16 caractères)
- PAS votre mot de passe Gmail normal !

---

## ÉTAPE 4 : Ajouter la clé Stripe Publishable dans le Frontend

Vous devez aussi ajouter la clé publique Stripe dans le frontend.

### Ouvrir le fichier frontend :
```bash
nano /app/frontend/.env
```

### Ajouter cette ligne à la fin du fichier :
```bash
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_VOTRE_CLE_PUBLIQUE
```

**⚠️ Remplacez par votre vraie clé qui commence par `pk_live_` ou `pk_test_`**

---

## ÉTAPE 5 : Sauvegarder les fichiers

### Si vous utilisez `nano` (terminal) :
1. Appuyez sur **Ctrl + X**
2. Appuyez sur **Y** (pour "Yes")
3. Appuyez sur **Entrée**

### Si vous utilisez l'éditeur graphique :
1. Cliquez sur **"Save"** ou **"Enregistrer"**

---

## ÉTAPE 6 : Redémarrer l'application

Pour que les changements prennent effet, vous DEVEZ redémarrer :

```bash
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

Ou redémarrer tout :
```bash
sudo supervisorctl restart all
```

---

## ÉTAPE 7 : Vérifier que tout fonctionne

### A) Vérifier les logs backend
```bash
tail -f /var/log/supervisor/backend.out.log
```

Vous devriez voir :
```
INFO:     Application startup complete.
```

Appuyez sur **Ctrl + C** pour quitter.

### B) Tester l'envoi d'email
1. Allez sur votre site
2. Inscrivez-vous avec un nouvel email
3. Vérifiez que vous recevez l'email de bienvenue
4. Vérifiez aussi dans les **spams**

### C) Tester un paiement
1. Allez sur la boutique
2. Essayez d'acheter une formation
3. Vérifiez que Stripe/PayPal s'ouvre correctement

---

## 🎯 EXEMPLE COMPLET DU FICHIER .env

Voici à quoi devrait ressembler votre fichier `/app/backend/.env` une fois configuré :

```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="tradalife"
CORS_ORIGINS="*"
JWT_SECRET_KEY=tradalife-super-secret-key-change-in-production-7bd003b43fb36cc71fac14a12b5b06ae

# Stripe Configuration
STRIPE_SECRET_KEY=sk_live_51ABCxyz123...votre_vraie_cle

# PayPal Configuration
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=AaBbCc123xyz...votre_vraie_cle
PAYPAL_CLIENT_SECRET=EFgh456uvw...votre_vrai_secret

# Gmail Configuration
GMAIL_EMAIL=votre-email@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

---

## ❌ ERREURS COURANTES À ÉVITER

### ❌ Ne PAS mettre de guillemets autour des clés
**Mauvais :**
```bash
STRIPE_SECRET_KEY="sk_live_123..."
```

**Bon :**
```bash
STRIPE_SECRET_KEY=sk_live_123...
```

### ❌ Ne PAS mettre d'espaces avant ou après le =
**Mauvais :**
```bash
STRIPE_SECRET_KEY = sk_live_123...
```

**Bon :**
```bash
STRIPE_SECRET_KEY=sk_live_123...
```

### ❌ Ne PAS oublier de redémarrer après modification
Toujours faire :
```bash
sudo supervisorctl restart backend
```

---

## 🔒 SÉCURITÉ - CHECKLIST FINALE

- [ ] Mes clés sont dans le fichier .env (pas dans le code)
- [ ] Je n'ai PAS partagé mes clés dans le chat
- [ ] J'utilise des clés "live" pour la production
- [ ] J'utilise des clés "test" pour développer
- [ ] J'ai redémarré le backend après modification
- [ ] J'ai testé l'envoi d'email
- [ ] J'ai testé un paiement

---

## 🆘 EN CAS DE PROBLÈME

### Problème : "Invalid API Key"
**Solution :**
- Vérifiez que vous avez copié la clé complète
- Vérifiez qu'il n'y a pas d'espace avant/après
- Vérifiez que vous utilisez bien `sk_live_` (pas `pk_`)

### Problème : Email non reçu
**Solution :**
- Vérifiez dans les spams
- Vérifiez que le mot de passe d'application est correct (16 caractères)
- Vérifiez les logs : `tail -f /var/log/supervisor/backend.err.log`

### Problème : PayPal ne s'ouvre pas
**Solution :**
- Vérifiez que `PAYPAL_MODE=live` (pas sandbox en production)
- Vérifiez que les clés sont bien celles de production (pas sandbox)

---

## 📞 AIDE

Si vous avez des problèmes après avoir suivi ce guide :
1. Vérifiez les logs : `tail -f /var/log/supervisor/backend.err.log`
2. Vérifiez que le backend est démarré : `sudo supervisorctl status`
3. Redémarrez tout : `sudo supervisorctl restart all`

---

## ✅ SUCCÈS !

Une fois tout configuré, vous aurez :
- ✅ Paiements Stripe fonctionnels
- ✅ Paiements PayPal fonctionnels
- ✅ Emails automatiques :
  - Email de bienvenue à l'inscription
  - Email de confirmation après achat
  - Email après soumission KYC
  - Email d'approbation KYC

**Votre plateforme est maintenant prête à accepter de vrais paiements ! 🎉**

---

## 🎯 PROCHAINES ÉTAPES

Après la configuration :
1. Tester avec un vrai achat (petit montant)
2. Vérifier que l'email arrive
3. Tester le workflow KYC complet
4. Mettre en ligne sur votre domaine personnalisé
