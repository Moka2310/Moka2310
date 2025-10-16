# 🎯 DÉMARRAGE RAPIDE - 5 Minutes

## Option 1 : Script Automatique (LE PLUS SIMPLE)

Exécutez ce script interactif :

```bash
/app/configure.sh
```

Le script vous permet de :
- ✅ Configurer Stripe
- ✅ Configurer PayPal  
- ✅ Configurer Gmail
- ✅ Redémarrer l'app
- ✅ Créer un admin
- ✅ Et plus...

---

## Option 2 : Configuration Manuelle (3 étapes)

### ÉTAPE 1 : Éditer le fichier de configuration

```bash
nano /app/backend/.env
```

Modifier ces lignes :
```bash
# Stripe
STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_ICI

# PayPal
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=VOTRE_CLIENT_ID
PAYPAL_CLIENT_SECRET=VOTRE_SECRET

# Gmail
GMAIL_EMAIL=votre-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

Sauvegarder : `Ctrl + X`, puis `Y`, puis `Entrée`

### ÉTAPE 2 : Redémarrer

```bash
sudo supervisorctl restart backend
```

### ÉTAPE 3 : Créer un admin

```bash
mongosh
```

Puis dans MongoDB :
```javascript
use tradalife
db.users.updateOne(
  { email: "votre-email@gmail.com" },
  { $set: { role: "admin" } }
)
exit
```

---

## 🎬 Ajouter vos Vidéos (SIMPLE)

### 1. Uploader sur Google Drive
- Aller sur https://drive.google.com
- Uploader vos vidéos
- Clic droit → Partager → "Tous les utilisateurs avec le lien"
- Copier le lien

### 2. Ajouter dans la base de données

```bash
mongosh
```

```javascript
use tradalife

db.videos.insertOne({
  "id": "1",
  "formationId": "1",  // 1=Crypto, 2=Forex, 3=Gold, etc.
  "title": "Titre de votre vidéo",
  "url": "https://drive.google.com/uc?export=view&id=VOTRE_ID",
  "duration": "15:30",
  "order": 1,
  "createdAt": new Date()
})

exit
```

**Note** : Transformer le lien Google Drive :
- De : `https://drive.google.com/file/d/1ABC123/view`
- À : `https://drive.google.com/uc?export=view&id=1ABC123`

---

## 🔑 Obtenir vos Clés API

### Stripe
1. https://dashboard.stripe.com/apikeys
2. Copier "Secret key" (commence par `sk_`)

### PayPal
1. https://developer.paypal.com/dashboard
2. My Apps & Credentials
3. Créer une app
4. Copier Client ID et Secret

### Gmail
1. https://myaccount.google.com/security
2. Activer validation 2 étapes
3. https://myaccount.google.com/apppasswords
4. Créer "Tradalife"
5. Copier le mot de passe (16 caractères)

---

## ✅ CHECKLIST FINALE

- [ ] Clés Stripe ajoutées
- [ ] Clés PayPal ajoutées
- [ ] Gmail configuré
- [ ] Backend redémarré
- [ ] Compte admin créé
- [ ] Vidéos uploadées
- [ ] Test d'inscription (email reçu ?)
- [ ] Test d'achat
- [ ] Test KYC

---

## 📞 AIDE RAPIDE

**Voir les logs** :
```bash
tail -f /var/log/supervisor/backend.err.log
```

**Redémarrer** :
```bash
sudo supervisorctl restart all
```

**MongoDB** :
```bash
mongosh
use tradalife
db.formations.find()  # Voir formations
db.users.find()       # Voir utilisateurs
```

---

## 🚀 C'EST PRÊT !

Votre application est maintenant configurée !

**Testez sur** : https://course-market-11.preview.emergentagent.com

**Documentation complète** :
- `/app/GUIDE_DEPLOIEMENT.md` - Guide complet
- `/app/GUIDE_TEST.md` - Comment tester
- `/app/CONFIGURATION_API.md` - Détails API

**Script de configuration** :
```bash
/app/configure.sh
```
