# 📱 Guide de gestion des données - Tradalife

## 🎯 Comment modifier et gérer vos formations

### Méthode 1 : Via MongoDB (Recommandé)

#### 1. Accéder à MongoDB
```bash
# Ouvrir un terminal et se connecter à MongoDB
mongosh

# Utiliser la base de données Tradalife
use tradalife
```

#### 2. Voir toutes les formations actuelles
```javascript
db.formations.find().pretty()
```

#### 3. Ajouter une nouvelle formation
```javascript
db.formations.insertOne({
  "id": "6",
  "title": "Formation Trading Commodités",
  "description": "Apprenez à trader le pétrole, le gaz naturel et autres commodités avec des stratégies avancées.",
  "price": 329.0,
  "duration": "9 heures",
  "level": "Intermédiaire",
  "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
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

#### 4. Modifier une formation existante
```javascript
// Changer le prix de la formation Crypto (id: "1")
db.formations.updateOne(
  { "id": "1" },
  { 
    $set: { 
      "price": 249.0,
      "description": "NOUVELLE DESCRIPTION ICI"
    } 
  }
)

// Changer l'image
db.formations.updateOne(
  { "id": "1" },
  { $set: { "image": "VOTRE_NOUVELLE_URL_IMAGE" } }
)

// Changer le nombre de vidéos
db.formations.updateOne(
  { "id": "1" },
  { $set: { "videoCount": 15 } }
)
```

#### 5. Ajouter un lien Telegram à une formation
```javascript
db.formations.updateOne(
  { "id": "1" },
  { 
    $push: { 
      "telegramLinks": {
        "name": "Nouveau Canal",
        "url": "https://t.me/nouveau_canal"
      }
    } 
  }
)
```

#### 6. Supprimer une formation
```javascript
db.formations.deleteOne({ "id": "6" })
```

---

## 🎬 Comment gérer les vidéos

### Option 1 : Héberger sur votre serveur

#### 1. Créer le dossier vidéos
```bash
mkdir -p /app/backend/videos
```

#### 2. Uploader vos vidéos
```bash
# Via SCP depuis votre ordinateur
scp video1.mp4 user@server:/app/backend/videos/formation1_video1.mp4
```

#### 3. Créer la collection de vidéos dans MongoDB
```javascript
// Dans mongosh
use tradalife

db.videos.insertOne({
  "id": "1",
  "formationId": "1",
  "title": "Introduction au Trading Crypto",
  "description": "Première vidéo de la formation",
  "url": "/videos/formation1_video1.mp4",
  "duration": "15:30",
  "order": 1,
  "createdAt": new Date()
})
```

#### 4. Ajouter route pour servir les vidéos (Backend)
Créer `/app/backend/routes/videos.py` :
```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from models import User
from dependencies import get_current_user, get_db
from pathlib import Path

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.get("/{formation_id}")
async def get_formation_videos(
    formation_id: str, 
    current_user: User = Depends(get_current_user)
):
    # Check if user has purchased this formation
    db = get_db()
    purchase = await db.purchases.find_one({
        "userId": current_user.id,
        "formationId": formation_id,
        "status": "completed"
    })
    
    if not purchase:
        raise HTTPException(status_code=403, detail="You don't own this formation")
    
    # Check KYC status
    if current_user.kycStatus != "approved":
        raise HTTPException(status_code=403, detail="KYC not approved")
    
    # Get videos
    videos = await db.videos.find({"formationId": formation_id}).sort("order", 1).to_list(100)
    return videos

@router.get("/stream/{video_id}")
async def stream_video(
    video_id: str,
    current_user: User = Depends(get_current_user)
):
    db = get_db()
    video = await db.videos.find_one({"id": video_id})
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Check if user owns the formation
    purchase = await db.purchases.find_one({
        "userId": current_user.id,
        "formationId": video["formationId"],
        "status": "completed"
    })
    
    if not purchase or current_user.kycStatus != "approved":
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Return video file
    video_path = Path("/app/backend") / video["url"].lstrip("/")
    return FileResponse(video_path, media_type="video/mp4")
```

### Option 2 : Héberger sur YouTube/Vimeo (Plus simple)

#### 1. Uploader vos vidéos sur YouTube en privé
- Aller sur YouTube Studio
- Upload vos vidéos
- Mettre en "Non répertorié" ou "Privé"
- Copier le lien

#### 2. Ajouter les liens dans MongoDB
```javascript
db.videos.insertMany([
  {
    "id": "1",
    "formationId": "1",
    "title": "Introduction au Trading Crypto",
    "description": "Vidéo 1",
    "url": "https://www.youtube.com/embed/VOTRE_VIDEO_ID",
    "duration": "15:30",
    "order": 1,
    "createdAt": new Date()
  },
  {
    "id": "2",
    "formationId": "1",
    "title": "Analyse technique Crypto",
    "description": "Vidéo 2",
    "url": "https://www.youtube.com/embed/AUTRE_VIDEO_ID",
    "duration": "22:15",
    "order": 2,
    "createdAt": new Date()
  }
])
```

---

## 👤 Gérer les utilisateurs

### Voir tous les utilisateurs
```javascript
db.users.find().pretty()
```

### Créer un compte admin
```javascript
// Remplacer par l'email d'un utilisateur existant
db.users.updateOne(
  { "email": "votre-email@example.com" },
  { $set: { "role": "admin" } }
)
```

### Approuver manuellement un KYC
```javascript
db.users.updateOne(
  { "email": "client@example.com" },
  { 
    $set: { 
      "kycStatus": "approved",
      "kycReviewedAt": new Date()
    } 
  }
)
```

### Voir tous les achats
```javascript
db.purchases.find().pretty()
```

---

## 🔧 API pour gérer les formations (Alternative)

### Créer un script Python pour ajouter des formations

Créer `/app/backend/add_formation.py` :
```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

async def add_formation():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client['tradalife']
    
    formation = {
        "id": "6",
        "title": "Formation Trading Actions",
        "description": "Investissez en bourse avec confiance",
        "price": 359.0,
        "duration": "12 heures",
        "level": "Tous niveaux",
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
        "videoCount": 18,
        "telegramLinks": [
            {
                "name": "Canal Actions VIP",
                "url": "https://t.me/tradalife_actions"
            }
        ],
        "createdAt": datetime.utcnow()
    }
    
    await db.formations.insert_one(formation)
    print(f"✅ Formation '{formation['title']}' ajoutée!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_formation())
```

Utiliser :
```bash
cd /app/backend
python add_formation.py
```

---

## 📊 Statistiques et monitoring

### Voir le nombre total d'utilisateurs
```javascript
db.users.countDocuments()
```

### Voir le nombre d'achats
```javascript
db.purchases.countDocuments({ "status": "completed" })
```

### Calculer le revenu total
```javascript
db.purchases.aggregate([
  { $match: { "status": "completed" } },
  { $group: { _id: null, total: { $sum: "$price" } } }
])
```

### Voir les KYC en attente
```javascript
db.users.find({ "kycStatus": "pending_review" }).pretty()
```

---

## 🔄 Backup de la base de données

### Créer un backup
```bash
mongodump --db tradalife --out /app/backups/$(date +%Y%m%d)
```

### Restaurer un backup
```bash
mongorestore --db tradalife /app/backups/20250116/tradalife
```

---

## 💡 Tips et astuces

### 1. Trouver une formation par titre
```javascript
db.formations.find({ "title": /Crypto/i })
```

### 2. Mettre à jour plusieurs formations en même temps
```javascript
// Augmenter tous les prix de 10%
db.formations.updateMany(
  {},
  { $mul: { "price": 1.10 } }
)
```

### 3. Exporter les données en JSON
```bash
mongoexport --db tradalife --collection formations --out formations.json
```

### 4. Importer des données depuis JSON
```bash
mongoimport --db tradalife --collection formations --file formations.json
```

---

## 🎨 Modifier les images

### Où trouver des images gratuites :
- **Unsplash** : https://unsplash.com
- **Pexels** : https://pexels.com
- **Pixabay** : https://pixabay.com

### Comment utiliser :
1. Chercher "trading" ou "finance"
2. Télécharger l'image
3. Uploader sur un hébergeur (Imgur, Cloudinary, votre serveur)
4. Copier l'URL
5. Mettre à jour dans MongoDB

---

## ❓ FAQ

**Q: Comment tester sur mobile depuis mon ordinateur ?**
R: Ouvrir Chrome DevTools (F12) → Cliquer sur l'icône mobile → Choisir iPhone/Android

**Q: Les modifications ne s'affichent pas ?**
R: Rafraîchir la page (Ctrl+F5 ou Cmd+Shift+R)

**Q: Comment changer les couleurs du site ?**
R: Modifier `/app/frontend/src/index.css` et les classes Tailwind

**Q: Puis-je avoir plusieurs formations avec le même prix ?**
R: Oui, aucun problème !

---

## 📞 Support

Si vous avez besoin d'aide :
1. Vérifier les logs : `tail -f /var/log/supervisor/backend.err.log`
2. Tester l'API : `curl https://edushop-portal.preview.emergentagent.com/api/formations`
3. Vérifier MongoDB : `mongosh` puis `use tradalife` puis `db.formations.find()`
