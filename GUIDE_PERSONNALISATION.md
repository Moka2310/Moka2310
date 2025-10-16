# 🎨 Guide de Personnalisation - Images et Vidéos

## PARTIE 1 : Ajouter des Vidéos dans la Rubrique "Vidéos" (Page d'accueil)

### Étape 1 : Accéder à MongoDB
```bash
mongosh
use tradalife
```

### Étape 2 : Voir les vidéos actuelles de la rubrique
```javascript
db.videos.find().pretty()
```

### Étape 3 : Ajouter une vidéo à la rubrique

#### Option A : Vidéo YouTube
```javascript
db.videos.insertOne({
  "id": "home_video_1",
  "formationId": "home",  // "home" pour les vidéos de la page d'accueil
  "title": "Comment ouvrir un compte GlobalPrime",
  "description": "Tutoriel complet pour créer votre compte de trading",
  "url": "https://www.youtube.com/embed/VOTRE_VIDEO_ID",
  "duration": "10:30",
  "order": 1,
  "section": "homepage",
  "createdAt": new Date()
})
```

#### Option B : Vidéo Google Drive
```javascript
db.videos.insertOne({
  "id": "home_video_2",
  "formationId": "home",
  "title": "Aperçu du groupe Telegram",
  "description": "Découvrez le contenu exclusif de notre groupe",
  "url": "https://drive.google.com/file/d/VOTRE_VIDEO_ID/preview",
  "duration": "8:45",
  "order": 2,
  "section": "homepage",
  "createdAt": new Date()
})
```

### Étape 4 : Ajouter plusieurs vidéos d'un coup
```javascript
db.videos.insertMany([
  {
    "id": "home_video_1",
    "formationId": "home",
    "title": "Ouvrir un compte GlobalPrime",
    "description": "Guide pas à pas",
    "url": "https://www.youtube.com/embed/VIDEO_ID_1",
    "duration": "10:30",
    "order": 1,
    "section": "homepage",
    "createdAt": new Date()
  },
  {
    "id": "home_video_2",
    "formationId": "home",
    "title": "Connecter MetaTrader 4",
    "description": "Configuration MT4",
    "url": "https://www.youtube.com/embed/VIDEO_ID_2",
    "duration": "12:15",
    "order": 2,
    "section": "homepage",
    "createdAt": new Date()
  },
  {
    "id": "home_video_3",
    "formationId": "home",
    "title": "Premiers signaux",
    "description": "Comment utiliser nos signaux de trading",
    "url": "https://www.youtube.com/embed/VIDEO_ID_3",
    "duration": "15:20",
    "order": 3,
    "section": "homepage",
    "createdAt": new Date()
  }
])
```

### Comment obtenir l'ID d'une vidéo YouTube
**Si votre lien est** : `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
**L'ID est** : `dQw4w9WgXcQ`
**URL à utiliser** : `https://www.youtube.com/embed/dQw4w9WgXcQ`

---

## PARTIE 2 : Modifier les Images des Canaux

Les 6 canaux sont : Crypto, Forex, Indices, Commodités, Gold, Actions

### Étape 1 : Trouver des images

**Sites d'images gratuites** :
- https://unsplash.com
- https://pexels.com
- https://pixabay.com

**Recherches suggérées** :
- "cryptocurrency bitcoin" pour Crypto
- "forex trading" pour Forex
- "stock market indices" pour Indices
- "oil commodities" pour Commodités
- "gold bars" pour Gold
- "stock trading" pour Actions

### Étape 2 : Obtenir l'URL de l'image

#### Option A : Unsplash
1. Chercher votre image
2. Cliquer sur l'image
3. Clic droit → "Copier l'adresse de l'image"
4. L'URL ressemble à : `https://images.unsplash.com/photo-xxx?w=500`

#### Option B : Héberger votre propre image
1. Aller sur https://imgur.com
2. Upload votre image
3. Clic droit → "Copier l'adresse de l'image"

### Étape 3 : Mettre à jour dans le code

**Fichier à modifier** : `/app/frontend/src/mockData.js`

Chercher la section `canaux` et modifier les URLs :

```javascript
export const canaux = [
  { 
    name: 'Crypto', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_CRYPTO' 
  },
  { 
    name: 'Forex', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_FOREX' 
  },
  { 
    name: 'Indices', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_INDICES' 
  },
  { 
    name: 'Commodités', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_COMMODITES' 
  },
  { 
    name: 'Gold', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_GOLD' 
  },
  { 
    name: 'Actions', 
    icon: 'VOTRE_NOUVELLE_URL_IMAGE_ACTIONS' 
  }
];
```

**Exemple avec de vraies URLs Unsplash** :
```javascript
export const canaux = [
  { 
    name: 'Crypto', 
    icon: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500' 
  },
  { 
    name: 'Forex', 
    icon: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500' 
  },
  { 
    name: 'Indices', 
    icon: 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500' 
  },
  { 
    name: 'Commodités', 
    icon: 'https://images.unsplash.com/photo-1604594849809-dfedbc827105?w=500' 
  },
  { 
    name: 'Gold', 
    icon: 'https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500' 
  },
  { 
    name: 'Actions', 
    icon: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500' 
  }
];
```

---

## PARTIE 3 : Modifier les Images et Descriptions de la Boutique

### Étape 1 : Accéder à MongoDB
```bash
mongosh
use tradalife
```

### Étape 2 : Voir les formations actuelles
```javascript
db.formations.find().pretty()
```

### Étape 3 : Modifier une formation (Image + Description)

#### Exemple : Modifier la Formation Trading Crypto (id: "1")
```javascript
db.formations.updateOne(
  { "id": "1" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
    "description": "Maîtrisez le trading de cryptomonnaies avec notre formation complète. Apprenez l'analyse technique, la gestion du risque, et les stratégies gagnantes utilisées par les professionnels. Idéal pour débuter dans le monde passionnant des crypto-actifs."
  }}
)
```

#### Modifier plusieurs champs en même temps
```javascript
db.formations.updateOne(
  { "id": "1" },
  { $set: {
    "title": "Formation Complète Trading Crypto",
    "description": "Devenez un expert du trading de cryptomonnaies en seulement 8 heures. Formation structurée avec exercices pratiques, analyse de cas réels et accès à notre groupe Telegram VIP pour des signaux quotidiens.",
    "image": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
    "price": 249.0,
    "duration": "8 heures",
    "level": "Débutant à Intermédiaire",
    "videoCount": 15
  }}
)
```

### Étape 4 : Modifier TOUTES les formations

```javascript
// Formation 1 - Crypto
db.formations.updateOne(
  { "id": "1" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500",
    "description": "Formation complète sur le trading de cryptomonnaies. Apprenez Bitcoin, Ethereum, et les altcoins. Stratégies d'achat/vente, analyse technique avancée, et gestion de portefeuille. Accès aux signaux crypto en temps réel."
  }}
)

// Formation 2 - Forex
db.formations.updateOne(
  { "id": "2" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
    "description": "Devenez un expert du marché des devises. Trading sur EUR/USD, GBP/USD, USD/JPY et toutes les paires majeures. Analyse fondamentale, technique, et psychologie du trading. Stratégies de scalping et swing trading incluses."
  }}
)

// Formation 3 - Gold
db.formations.updateOne(
  { "id": "3" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500",
    "description": "Spécialisez-vous dans le trading de l'or (XAU/USD). Comprenez les facteurs qui influencent le prix de l'or, les meilleures heures de trading, et les stratégies avancées. Parfait pour diversifier votre portefeuille."
  }}
)

// Formation 4 - Indices
db.formations.updateOne(
  { "id": "4" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500",
    "description": "Tradez les indices boursiers majeurs : CAC40, DAX30, S&P500, NASDAQ100. Apprenez les corrélations entre marchés, le timing parfait d'entrée/sortie, et les stratégies pour profiter de la volatilité des indices."
  }}
)

// Formation 5 - Pack Complet
db.formations.updateOne(
  { "id": "5" },
  { $set: {
    "image": "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=500",
    "description": "Le pack ultime pour devenir trader professionnel ! Toutes nos formations réunies : Crypto, Forex, Gold, Indices, Commodités et Actions. Plus de 50 heures de contenu, accès à TOUS les canaux VIP, et support premium à vie. Économisez 40% par rapport à l'achat séparé."
  }}
)
```

### Étape 5 : Ajouter une NOUVELLE formation avec image et description
```javascript
db.formations.insertOne({
  "id": "6",
  "title": "Formation Trading Commodités",
  "description": "Apprenez à trader le pétrole, le gaz naturel, l'or noir et les matières premières agricoles. Comprenez l'offre et la demande mondiale, les événements géopolitiques, et les meilleures stratégies pour ce marché unique. Idéal pour la diversification.",
  "price": 329.0,
  "duration": "9 heures",
  "level": "Intermédiaire",
  "image": "https://images.unsplash.com/photo-1604594849809-dfedbc827105?w=500",
  "videoCount": 14,
  "telegramLinks": [
    {
      "name": "Canal Commodités VIP",
      "url": "https://t.me/tradalife_commodites"
    }
  ],
  "createdAt": new Date()
})
```

---

## PARTIE 4 : Images Recommandées (Unsplash)

### Pour les Formations :

**Trading Crypto** :
```
https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500
https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=500
```

**Trading Forex** :
```
https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500
https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500
```

**Trading Gold** :
```
https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500
https://images.unsplash.com/photo-1610375461369-d546c7d31cdb?w=500
```

**Trading Indices** :
```
https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=500
https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500
```

**Trading Commodités** :
```
https://images.unsplash.com/photo-1604594849809-dfedbc827105?w=500
https://images.unsplash.com/photo-1474631245212-32dc3c8310c6?w=500
```

---

## PARTIE 5 : Commandes Rapides MongoDB

### Voir toutes les formations
```javascript
db.formations.find().pretty()
```

### Modifier juste l'image
```javascript
db.formations.updateOne(
  { "id": "1" },
  { $set: { "image": "VOTRE_NOUVELLE_URL" }}
)
```

### Modifier juste la description
```javascript
db.formations.updateOne(
  { "id": "1" },
  { $set: { "description": "VOTRE_NOUVELLE_DESCRIPTION" }}
)
```

### Modifier juste le prix
```javascript
db.formations.updateOne(
  { "id": "1" },
  { $set: { "price": 199.0 }}
)
```

### Supprimer une formation
```javascript
db.formations.deleteOne({ "id": "6" })
```

### Quitter MongoDB
```javascript
exit
```

---

## PARTIE 6 : Après Modification - Actualiser

### Si vous avez modifié `/app/frontend/src/mockData.js`
Le site se met à jour automatiquement (hot reload) ! Rafraîchissez simplement la page.

### Si vous avez modifié MongoDB
Les changements sont **immédiats** ! Rafraîchissez la page de la boutique.

---

## 📋 CHECKLIST RAPIDE

**Pour ajouter des vidéos page d'accueil** :
```bash
mongosh
use tradalife
db.videos.insertOne({ ... })
```

**Pour modifier images des canaux** :
```bash
nano /app/frontend/src/mockData.js
# Modifier les URLs dans "canaux"
```

**Pour modifier images/descriptions boutique** :
```bash
mongosh
use tradalife
db.formations.updateOne({ "id": "1" }, { $set: { ... }})
```

---

## 🎨 EXEMPLES DE DESCRIPTIONS ACCROCHEUSES

### Formation Crypto
```
"🚀 Rejoignez la révolution crypto ! Formation complète pour maîtriser Bitcoin, Ethereum et les altcoins. Stratégies éprouvées, analyse technique avancée, et accès aux signaux VIP. Plus de 500 élèves ont déjà doublé leur capital !"
```

### Formation Forex
```
"💰 Devenez trader Forex professionnel en 10 heures ! Apprenez les stratégies des banques d'investissement, le scalping haute fréquence, et le swing trading. Résultats garantis ou remboursé."
```

### Formation Gold
```
"✨ L'or, valeur refuge millénaire ! Apprenez à trader XAU/USD comme un pro. Stratégies pour tous les marchés (haussiers, baissiers, latéraux). Idéal pour la diversification de portefeuille."
```

### Pack Complet
```
"🏆 OFFRE EXCLUSIVE ! Le pack complet qui transforme les débutants en traders rentables. 50h de formation, TOUS les canaux VIP, support prioritaire. -40% de réduction = 1500€ d'économies !"
```

---

## 💡 ASTUCES PRO

1. **Utilisez des émojis** dans les descriptions (mais pas trop !)
2. **Mentionnez les bénéfices** concrets (pas juste les fonctionnalités)
3. **Images haute qualité** = plus de ventes (min 1000x600 pixels)
4. **Descriptions courtes** mais percutantes (2-3 phrases max)
5. **Call-to-action** : "Rejoignez", "Commencez", "Maîtrisez"

---

## 🚀 VOUS ÊTES PRÊT !

Maintenant vous savez comment :
- ✅ Ajouter des vidéos
- ✅ Modifier les images des canaux
- ✅ Modifier les images des formations
- ✅ Améliorer les descriptions

**Besoin d'aide ?** Consultez `/app/GUIDE_GESTION_DONNEES.md`
