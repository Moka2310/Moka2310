# Guide d'utilisation - Plateforme Tradalife

## 🎯 Vue d'ensemble
Votre plateforme clone de Tradalife est maintenant complète et fonctionnelle !

## ✅ Fonctionnalités implémentées

### 1. Frontend (React)
- **Page d'accueil** : Design identique à tradalife.com avec toutes les sections
- **Boutique** : 5 formations disponibles (Crypto, Forex, Gold, Indices, Pack Complet)
- **Authentification** : Inscription et connexion sécurisées
- **Checkout** : Simulation de paiement Stripe/PayPal
- **Dashboard utilisateur** avec 2 onglets :
  - Mes Formations (accès après KYC approuvé)
  - Vérification KYC (formulaire + upload 3 documents)

### 2. Backend (FastAPI + MongoDB)
- **API Authentication** : Register, Login, Get User
- **API Formations** : Liste et détails des formations
- **API Purchases** : Créer, confirmer et lister les achats
- **API KYC** : Soumettre documents, vérifier statut
- **API Admin** : Valider/rejeter KYC, statistiques

### 3. Base de données MongoDB
Collections créées :
- `users` : Comptes utilisateurs avec KYC
- `formations` : 5 formations pré-chargées
- `purchases` : Historique des achats
- `kyc_documents` : Documents uploadés

## 🚀 Comment utiliser

### Workflow utilisateur complet :

1. **S'inscrire** : /login → "S'inscrire" → email + mot de passe
2. **Acheter une formation** : Boutique → Choisir formation → Acheter → Payer
3. **Compléter le KYC** : Dashboard → Onglet "Vérification KYC"
   - Remplir : Prénom, Nom, Pays, Téléphone
   - Uploader 3 documents : Passeport, Carte d'identité, Preuve de résidence
4. **Attendre validation admin** (voir section Admin ci-dessous)
5. **Accéder aux formations** : Une fois KYC approuvé → Télécharger vidéos + Accès liens Telegram VIP

### Tester en tant qu'admin :

Pour valider les KYC, vous devez créer un compte admin dans MongoDB :

```bash
# Se connecter à MongoDB
mongosh

# Utiliser la base Tradalife
use tradalife

# Mettre un utilisateur en admin
db.users.updateOne(
  { email: "votre-email@example.com" },
  { $set: { role: "admin" } }
)
```

Ensuite, utilisez les endpoints admin :
- `GET /api/admin/kyc-requests` : Voir tous les KYC en attente
- `POST /api/admin/kyc-approve/{userId}` : Approuver un KYC
- `POST /api/admin/kyc-reject/{userId}` : Rejeter un KYC (avec raison)
- `GET /api/admin/stats` : Statistiques de la plateforme

## 📁 Structure des fichiers

### Backend
```
/app/backend/
├── server.py                 # Point d'entrée FastAPI
├── models.py                 # Modèles Pydantic
├── auth_utils.py            # JWT et hash de mots de passe
├── dependencies.py          # Auth middleware et upload
├── routes/
│   ├── auth.py             # Routes d'authentification
│   ├── formations.py       # Routes formations
│   ├── purchases.py        # Routes achats
│   ├── kyc.py              # Routes KYC
│   └── admin.py            # Routes admin
└── uploads/                # Dossier documents KYC
```

### Frontend
```
/app/frontend/src/
├── App.js                   # Routing principal
├── api/client.js           # Client API axios
├── contexts/
│   └── AuthContext.jsx     # Contexte authentification
├── components/
│   ├── Navbar.jsx          # Navigation
│   └── Footer.jsx          # Pied de page
└── pages/
    ├── Home.jsx            # Page d'accueil
    ├── Boutique.jsx        # Page boutique
    ├── Login.jsx           # Connexion/Inscription
    ├── Checkout.jsx        # Page paiement
    └── Dashboard.jsx       # Panel utilisateur
```

## 🔧 Prochaines étapes recommandées

### 1. Intégration paiements réels
**Stripe** :
```bash
npm install @stripe/stripe-js
pip install stripe
```
- Créer compte Stripe
- Ajouter clés API dans .env
- Implémenter webhook de confirmation

**PayPal** :
```bash
pip install paypalrestsdk
```
- Créer compte PayPal Developer
- Configurer OAuth credentials

### 2. Envoi d'emails
```bash
pip install sendgrid  # ou python-smtp
```
Templates à créer :
- Email de bienvenue
- Confirmation d'achat
- KYC soumis
- KYC approuvé/rejeté

### 3. Hébergement vidéos
Options :
- **AWS S3** : Stockage cloud scalable
- **Cloudflare Stream** : CDN optimisé vidéo
- **Vimeo/YouTube** : Liens privés

### 4. Panel admin frontend
Créer `/admin` avec :
- Liste des utilisateurs
- Validation KYC avec preview documents
- Statistiques temps réel
- Gestion des formations

## 🔐 Sécurité

**Actuellement implémenté** :
- JWT tokens pour authentification
- Bcrypt pour hash des mots de passe
- CORS configuré
- Upload de fichiers sécurisé

**À ajouter en production** :
- Rate limiting (contre brute force)
- Validation email (email de confirmation)
- HTTPS obligatoire
- Changer JWT_SECRET_KEY en production
- Backup automatique MongoDB
- Monitoring et logs (Sentry, DataDog)

## 📊 Tester l'application

### Backend
```bash
# Tester les endpoints
curl https://edutrader.preview.emergentagent.com/api/formations

# Créer un utilisateur
curl -X POST https://edutrader.preview.emergentagent.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'
```

### Frontend
1. Ouvrir : https://edutrader.preview.emergentagent.com
2. Tester l'inscription
3. Acheter une formation
4. Soumettre le KYC

## 💡 Support

Pour toute question :
1. Vérifier les logs : `/var/log/supervisor/backend.*.log`
2. Consulter le fichier `contracts.md` pour l'architecture API
3. Revoir `test_result.md` pour les tests effectués

## 🎉 Félicitations !
Votre plateforme est fonctionnelle. Il ne reste plus qu'à intégrer les paiements réels et l'envoi d'emails pour la mettre en production complète !
