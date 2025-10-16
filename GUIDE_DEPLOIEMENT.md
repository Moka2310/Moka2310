# 🚀 Guide de Configuration et Déploiement - Tradalife

## PARTIE 1 : Configuration des Clés API (À FAIRE EN PREMIER)

### 📍 Où configurer ?
Toutes les configurations se font dans le fichier : `/app/backend/.env`

### Comment y accéder ?
Vous avez 2 options :

#### Option A : Via l'éditeur de fichiers (Recommandé)
1. Sur la plateforme Emergent
2. Aller dans "Files" ou "Explorateur de fichiers"
3. Naviguer vers `/app/backend/.env`
4. Cliquer sur le fichier pour l'éditer

#### Option B : Via terminal
```bash
# Ouvrir le terminal et éditer le fichier
nano /app/backend/.env
```

---

## 🔑 ÉTAPE 1 : Configurer Stripe

### 1.1 Obtenir vos clés Stripe

1. **Aller sur** : https://dashboard.stripe.com
2. **Se connecter** avec votre compte Stripe
3. **Cliquer sur** "Developers" (en haut à droite)
4. **Cliquer sur** "API keys"
5. Vous verrez 2 clés :
   - **Publishable key** : commence par `pk_live_...` ou `pk_test_...`
   - **Secret key** : commence par `sk_live_...` ou `sk_test_...` (cliquer sur "Reveal" pour voir)

### 1.2 Ajouter les clés dans votre application

**Dans `/app/backend/.env`** :
```bash
STRIPE_SECRET_KEY=sk_live_votre_vraie_cle_ici
```

**Dans `/app/frontend/.env`** :
```bash
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_votre_vraie_cle_ici
```

⚠️ **IMPORTANT** : 
- Pour les tests, utilisez les clés avec `test`
- Pour la production, utilisez les clés avec `live`

---

## 💳 ÉTAPE 2 : Configurer PayPal

### 2.1 Obtenir vos credentials PayPal

1. **Aller sur** : https://developer.paypal.com
2. **Se connecter** avec votre compte PayPal
3. **Cliquer sur** "Dashboard"
4. **Cliquer sur** "My Apps & Credentials"
5. **Cliquer sur** "Create App" (si vous n'en avez pas)
6. Donner un nom : "Tradalife"
7. Vous verrez :
   - **Client ID** : Votre identifiant
   - **Secret** : Cliquer sur "Show" pour voir

### 2.2 Ajouter dans votre application

**Dans `/app/backend/.env`** :
```bash
# Mode sandbox pour les tests
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=votre_client_id_ici
PAYPAL_CLIENT_SECRET=votre_secret_ici

# Quand vous êtes prêt pour la production :
# PAYPAL_MODE=live
# PAYPAL_CLIENT_ID=votre_client_id_live
# PAYPAL_CLIENT_SECRET=votre_secret_live
```

---

## 📧 ÉTAPE 3 : Configurer Gmail (Envoi d'emails)

### 3.1 Créer un mot de passe d'application Gmail

1. **Aller sur** : https://myaccount.google.com/security
2. **Activer** "Validation en deux étapes" (si pas déjà fait)
3. **Aller sur** : https://myaccount.google.com/apppasswords
4. **Sélectionner** "Autre (nom personnalisé)"
5. **Entrer** : "Tradalife"
6. **Cliquer sur** "Générer"
7. **COPIER** le mot de passe de 16 caractères (ex: xxxx xxxx xxxx xxxx)

⚠️ Ne fermez pas la fenêtre avant d'avoir copié le mot de passe !

### 3.2 Ajouter dans votre application

**Dans `/app/backend/.env`** :
```bash
GMAIL_EMAIL=votre-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

⚠️ **Note** : Utilisez le mot de passe d'application, PAS votre mot de passe Gmail normal !

---

## 🎬 ÉTAPE 4 : Ajouter vos Vidéos de Formation

Vous avez 2 options :

### Option A : Héberger sur Google Drive (RECOMMANDÉ - Plus simple)

#### 4.1 Uploader vos vidéos sur Google Drive

1. Aller sur https://drive.google.com
2. Créer un dossier "Formations Tradalife"
3. Uploader vos vidéos
4. Pour chaque vidéo :
   - Clic droit → "Partager"
   - Changer en "Tous les utilisateurs disposant du lien"
   - Cliquer sur "Copier le lien"

#### 4.2 Obtenir le lien direct

Si le lien copié ressemble à :
```
https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing
```

Transformez-le en :
```
https://drive.google.com/uc?export=view&id=1ABC123XYZ
```

#### 4.3 Ajouter dans MongoDB

```bash
# Ouvrir MongoDB
mongosh

# Utiliser la base Tradalife
use tradalife

# Ajouter une vidéo
db.videos.insertOne({
  "id": "1",
  "formationId": "1",
  "title": "Introduction au Trading Crypto",
  "description": "Première vidéo - Les bases",
  "url": "https://drive.google.com/uc?export=view&id=VOTRE_ID_ICI",
  "duration": "15:30",
  "order": 1,
  "createdAt": new Date()
})

# Ajouter plusieurs vidéos d'un coup
db.videos.insertMany([
  {
    "id": "1",
    "formationId": "1",
    "title": "Introduction au Trading Crypto",
    "url": "https://drive.google.com/uc?export=view&id=ID_VIDEO_1",
    "duration": "15:30",
    "order": 1,
    "createdAt": new Date()
  },
  {
    "id": "2",
    "formationId": "1",
    "title": "Analyse Technique",
    "url": "https://drive.google.com/uc?export=view&id=ID_VIDEO_2",
    "duration": "22:15",
    "order": 2,
    "createdAt": new Date()
  }
])
```

### Option B : Héberger sur YouTube (Liens privés)

#### 4.1 Uploader sur YouTube

1. Aller sur https://studio.youtube.com
2. Cliquer sur "Créer" → "Importer une vidéo"
3. Choisir votre vidéo
4. **Important** : Mettre en "Non répertorié" (pas public)
5. Récupérer le lien de la vidéo

#### 4.2 Ajouter dans MongoDB

```bash
mongosh
use tradalife

db.videos.insertOne({
  "id": "1",
  "formationId": "1",
  "title": "Introduction au Trading Crypto",
  "url": "https://www.youtube.com/embed/VOTRE_VIDEO_ID",
  "duration": "15:30",
  "order": 1,
  "createdAt": new Date()
})
```

---

## 🔄 ÉTAPE 5 : Appliquer les Modifications

Après avoir modifié le fichier `.env`, vous DEVEZ redémarrer le backend :

```bash
sudo supervisorctl restart backend
```

Vérifier que tout fonctionne :
```bash
tail -f /var/log/supervisor/backend.out.log
```

Vous devriez voir :
```
INFO:     Application startup complete.
```

---

## 📝 ÉTAPE 6 : Modifier les Formations

### Via MongoDB Shell

```bash
# Se connecter à MongoDB
mongosh

# Utiliser la base Tradalife
use tradalife

# Voir toutes les formations
db.formations.find().pretty()

# Modifier une formation (exemple: changer le prix)
db.formations.updateOne(
  { "id": "1" },
  { $set: { 
    "price": 249.0,
    "title": "NOUVEAU TITRE",
    "description": "NOUVELLE DESCRIPTION"
  }}
)

# Ajouter une nouvelle formation
db.formations.insertOne({
  "id": "6",
  "title": "Formation Trading Commodités",
  "description": "Apprenez à trader le pétrole, gaz naturel...",
  "price": 329.0,
  "duration": "9 heures",
  "level": "Intermédiaire",
  "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
  "videoCount": 14,
  "telegramLinks": [
    {
      "name": "Canal Commodités VIP",
      "url": "https://t.me/votre_canal_commodites"
    }
  ],
  "createdAt": new Date()
})
```

### Via Interface Web (Optionnel)

Vous pouvez aussi installer MongoDB Compass pour une interface graphique :
1. Télécharger : https://www.mongodb.com/try/download/compass
2. Se connecter à : `mongodb://localhost:27017`
3. Base de données : `tradalife`
4. Collection : `formations`

---

## 🌐 ÉTAPE 7 : Mettre en Ligne (Déploiement)

### Option A : Déployer sur Emergent (Recommandé)

1. **Dans la plateforme Emergent** :
   - Cliquer sur "Deploy" ou "Déployer"
   - Choisir votre branche Git (main/master)
   - Attendre le déploiement
   - Vous recevrez une URL de production

2. **Configurer un nom de domaine** (optionnel) :
   - Acheter un nom de domaine (ex: Namecheap, OVH, Google Domains)
   - Dans les paramètres du domaine, configurer les DNS :
     ```
     Type: CNAME
     Name: @
     Value: votre-app.emergent.sh
     ```

### Option B : Déployer ailleurs

Votre application peut être déployée sur :
- **Vercel** (Frontend)
- **Render** ou **Railway** (Backend)
- **MongoDB Atlas** (Base de données cloud)

---

## ✅ CHECKLIST AVANT LA MISE EN LIGNE

- [ ] Clés Stripe configurées et testées
- [ ] Clés PayPal configurées et testées
- [ ] Gmail configuré et testé (envoyer un email de test)
- [ ] Vidéos uploadées et liens ajoutés dans MongoDB
- [ ] Formations modifiées selon vos besoins
- [ ] Liens Telegram mis à jour
- [ ] Backend redémarré : `sudo supervisorctl restart backend`
- [ ] Test complet : inscription → achat → KYC → validation
- [ ] Changé JWT_SECRET_KEY en production
- [ ] Mode Stripe/PayPal en "live" (pas "test")
- [ ] Backup MongoDB effectué

---

## 🧪 TESTER AVANT LA MISE EN LIGNE

### Test 1 : Inscription + Email
```bash
# Créer un compte
# Vérifier que l'email de bienvenue arrive
```

### Test 2 : Achat avec Stripe
```bash
# Acheter une formation avec une vraie carte de test Stripe
# Carte de test : 4242 4242 4242 4242
# Date : N'importe quelle date future
# CVC : N'importe quel 3 chiffres
```

### Test 3 : KYC complet
```bash
# Soumettre le KYC
# Se connecter en admin
# Approuver le KYC
# Vérifier que l'utilisateur reçoit l'email
```

---

## 🔒 SÉCURITÉ EN PRODUCTION

### À FAIRE ABSOLUMENT :

1. **Changer le JWT_SECRET_KEY** dans `.env` :
```bash
JWT_SECRET_KEY=$(openssl rand -hex 32)
```

2. **Passer Stripe en mode LIVE** :
```bash
STRIPE_SECRET_KEY=sk_live_votre_cle
```

3. **Passer PayPal en mode LIVE** :
```bash
PAYPAL_MODE=live
```

4. **Activer HTTPS** (automatique sur Emergent)

5. **Sauvegarder MongoDB régulièrement** :
```bash
mongodump --db tradalife --out /app/backups/$(date +%Y%m%d)
```

---

## 📞 RÉSUMÉ DES ÉTAPES

1. ✅ Configurer Stripe → `/app/backend/.env`
2. ✅ Configurer PayPal → `/app/backend/.env`
3. ✅ Configurer Gmail → `/app/backend/.env`
4. ✅ Redémarrer backend → `sudo supervisorctl restart backend`
5. ✅ Ajouter vidéos → MongoDB (Google Drive ou YouTube)
6. ✅ Modifier formations → MongoDB
7. ✅ Tester tout le workflow
8. ✅ Déployer en production

---

## 🎯 ACCÈS RAPIDES

**Modifier les configurations** :
```bash
nano /app/backend/.env
```

**Accéder à MongoDB** :
```bash
mongosh
use tradalife
```

**Redémarrer l'application** :
```bash
sudo supervisorctl restart all
```

**Voir les logs** :
```bash
tail -f /var/log/supervisor/backend.err.log
```

---

## ❓ QUESTIONS FRÉQUENTES

**Q: Combien de temps pour mettre en ligne ?**
R: 30 minutes à 1h si vous avez déjà vos clés API

**Q: Dois-je payer pour Stripe/PayPal ?**
R: Non, c'est gratuit. Ils prennent juste une commission sur les ventes (~2-3%)

**Q: Puis-je tester sans vraies clés ?**
R: Oui ! Utilisez les clés "test" de Stripe/PayPal

**Q: Comment ajouter un admin ?**
```bash
mongosh
use tradalife
db.users.updateOne(
  { email: "votre-email@gmail.com" },
  { $set: { role: "admin" } }
)
```

**Q: Comment changer le logo ?**
R: Modifier dans `/app/frontend/src/components/Navbar.jsx` ligne avec le logo "T"

**Q: Mes vidéos sont lourdes, que faire ?**
R: Utilisez YouTube ou Google Drive, ils gèrent automatiquement la compression

---

## 📚 DOCUMENTATION COMPLÈTE

- `/app/GUIDE_TEST.md` - Comment tester l'application
- `/app/CONFIGURATION_API.md` - Détails sur les API
- `/app/GUIDE_GESTION_DONNEES.md` - Gérer formations et utilisateurs
- `/app/GUIDE_UTILISATION.md` - Workflow complet

---

## 🚀 VOUS ÊTES PRÊT !

Suivez ces étapes et votre application sera en ligne rapidement. Bonne chance ! 🎉
