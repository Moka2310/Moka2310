"""
Endpoint temporaire pour promouvoir un utilisateur en admin
À SUPPRIMER APRÈS UTILISATION
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencies import get_db
from datetime import datetime, timezone
import uuid
import os

router = APIRouter()

# Secret key from environment
ADMIN_SECRET_KEY = os.environ.get('ADMIN_SECRET_KEY', 'default-secret-change-in-production')

class PromoteRequest(BaseModel):
    email: str
    secret_key: str  # Pour sécuriser l'endpoint

class AddTestimonialsRequest(BaseModel):
    secret_key: str

class TestimonialUpdate(BaseModel):
    userName: str
    comment_fr: str
    comment_en: str

class ForceUpdateRequest(BaseModel):
    secret_key: str
    testimonials: list[TestimonialUpdate]

@router.post("/admin/promote-user")
async def promote_user_to_admin(
    request: PromoteRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Clé secrète simple pour sécuriser
    if request.secret_key != "tradalife-admin-promote-2025":
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    # Trouver l'utilisateur
    user = await db.users.find_one({"email": request.email})
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User {request.email} not found")
    
    # Promouvoir en admin
    result = await db.users.update_one(
        {"email": request.email},
        {"$set": {"role": "admin"}}
    )
    
    return {
        "success": True,
        "message": f"User {request.email} promoted to admin",
        "email": request.email,
        "previous_role": user.get("role", "user"),
        "new_role": "admin"
    }

@router.post("/admin/add-default-testimonials")
async def add_default_testimonials(
    request: AddTestimonialsRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Clé secrète pour sécuriser
    if request.secret_key != "tradalife-admin-promote-2025":
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    # Témoignages à ajouter
    testimonials = [
        {
            "id": str(uuid.uuid4()),
            "userName": "Kevin A.",
            "country": "Montréal, Canada",
            "comment": "Grâce à TRADALIFE, j'ai enfin compris comment gérer mes positions et mes risques. Les signaux sont clairs, précis et les résultats sont là ! En quelques semaines, j'ai pu améliorer ma performance de manière constante. Une équipe sérieuse et toujours disponible. Merci à Moka et toute la communauté !",
            "rating": 5,
            "status": "approved",
            "order": 0,
            "createdAt": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "userName": "Amy D.",
            "country": "Abidjan, Côte d'Ivoire",
            "comment": "TRADALIFE, c'est plus qu'un groupe de trading, c'est une vraie famille ! L'accompagnement est professionnel, les formations sont faciles à suivre, et les conseils m'ont permis de prendre confiance dans mes trades. Je recommande à 100 % pour tous ceux qui veulent progresser rapidement.",
            "rating": 5,
            "status": "approved",
            "order": 0,
            "createdAt": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "userName": "Sami L.",
            "country": "Nice, France",
            "comment": "J'ai testé plusieurs communautés de trading avant TRADALIFE, mais aucune n'offre un tel niveau de transparence et de suivi. Les canaux VIP sont super bien organisés, les résultats sont constants et surtout, on apprend à devenir autonome. Bravo à toute l'équipe ! Merci à MOKA pour sa disponibilité",
            "rating": 5,
            "status": "approved",
            "order": 0,
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Vérifier si les témoignages existent déjà
    existing_count = await db.testimonials.count_documents({
        "userName": {"$in": ["Kevin A.", "Amy D.", "Sami L."]}
    })
    
    if existing_count > 0:
        return {
            "success": False,
            "message": f"{existing_count} testimonials already exist",
            "action": "skipped"
        }
    
    # Insérer les témoignages
    result = await db.testimonials.insert_many(testimonials)
    
    return {
        "success": True,
        "message": f"Added {len(result.inserted_ids)} testimonials",
        "testimonials": [
            {"name": t["userName"], "country": t["country"]} 
            for t in testimonials
        ]
    }

@router.post("/admin/update-testimonial-translations")
async def update_testimonial_translations(
    request: AddTestimonialsRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Ajoute les traductions anglaises aux témoignages existants"""
    if request.secret_key != "tradalife-admin-promote-2025":
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    translations = {
        "Kevin A.": {
            "comment_fr": "Grâce à TRADALIFE, j'ai enfin compris comment gérer mes positions et mes risques. Les signaux sont clairs, précis et les résultats sont là ! En quelques semaines, j'ai pu améliorer ma performance de manière constante. Une équipe sérieuse et toujours disponible. Merci à Moka et toute la communauté !",
            "comment_en": "Thanks to TRADALIFE, I finally understood how to manage my positions and risks. The signals are clear, precise and the results are there! In just a few weeks, I was able to consistently improve my performance. A serious team that is always available. Thanks to Moka and the entire community!"
        },
        "Amy D.": {
            "comment_fr": "TRADALIFE, c'est plus qu'un groupe de trading, c'est une vraie famille ! L'accompagnement est professionnel, les formations sont faciles à suivre, et les conseils m'ont permis de prendre confiance dans mes trades. Je recommande à 100 % pour tous ceux qui veulent progresser rapidement.",
            "comment_en": "TRADALIFE is more than a trading group, it's a real family! The support is professional, the training is easy to follow, and the advice has helped me gain confidence in my trades. I recommend 100% for anyone who wants to progress quickly."
        },
        "Sami L.": {
            "comment_fr": "J'ai testé plusieurs communautés de trading avant TRADALIFE, mais aucune n'offre un tel niveau de transparence et de suivi. Les canaux VIP sont super bien organisés, les résultats sont constants et surtout, on apprend à devenir autonome. Bravo à toute l'équipe ! Merci à MOKA pour sa disponibilité",
            "comment_en": "I tested several trading communities before TRADALIFE, but none offer such a level of transparency and follow-up. The VIP channels are super well organized, the results are consistent and above all, we learn to become independent. Congratulations to the whole team! Thanks to MOKA for his availability"
        }
    }
    
    updated_count = 0
    updated_names = []
    for name, texts in translations.items():
        # Mettre à jour SANS filtre sur status pour attraper tous les témoignages
        result = await db.testimonials.update_one(
            {"userName": name},  # Enlevé le filtre status
            {"$set": texts}
        )
        if result.modified_count > 0:
            updated_count += 1
            updated_names.append(name)
    
    return {
        "success": True,
        "message": f"Updated {updated_count} testimonials with translations",
        "updated": updated_names
    }

@router.post("/admin/force-update-testimonials")
async def force_update_testimonials(
    request: ForceUpdateRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Force la mise à jour des témoignages avec les traductions"""
    if request.secret_key != "tradalife-admin-promote-2025":
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    updated_count = 0
    updated_names = []
    
    for testimonial in request.testimonials:
        result = await db.testimonials.update_many(
            {"userName": testimonial.userName},
            {"$set": {
                "comment_fr": testimonial.comment_fr,
                "comment_en": testimonial.comment_en
            }}
        )
        if result.modified_count > 0:
            updated_count += result.modified_count
            updated_names.append(testimonial.userName)
    
    return {
        "success": True,
        "message": f"Updated {updated_count} testimonials",
        "updated": updated_names
    }
