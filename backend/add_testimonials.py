import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

# Configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "tradalife")

async def add_testimonials():
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Testimonials to add
    testimonials = [
        {
            "id": str(uuid.uuid4()),
            "userName": "Kevin A.",
            "country": "Montréal, Canada",
            "comment": "Grâce à TRADALIFE, j'ai enfin compris comment gérer mes positions et mes risques. Les signaux sont clairs, précis et les résultats sont là ! En quelques semaines, j'ai pu améliorer ma performance de manière constante. Une équipe sérieuse et toujours disponible. Merci à Moka et toute la communauté !",
            "rating": 5,
            "status": "approved",
            "createdAt": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "userName": "Amy D.",
            "country": "Abidjan, Côte d'Ivoire",
            "comment": "TRADALIFE, c'est plus qu'un groupe de trading, c'est une vraie famille ! L'accompagnement est professionnel, les formations sont faciles à suivre, et les conseils m'ont permis de prendre confiance dans mes trades. Je recommande à 100 % pour tous ceux qui veulent progresser rapidement.",
            "rating": 5,
            "status": "approved",
            "createdAt": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "userName": "Sami L.",
            "country": "Nice, France",
            "comment": "J'ai testé plusieurs communautés de trading avant TRADALIFE, mais aucune n'offre un tel niveau de transparence et de suivi. Les canaux VIP sont super bien organisés, les résultats sont constants et surtout, on apprend à devenir autonome. Bravo à toute l'équipe ! Merci à MOKA pour sa disponibilité",
            "rating": 5,
            "status": "approved",
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert testimonials
    result = await db.testimonials.insert_many(testimonials)
    print(f"✅ {len(result.inserted_ids)} témoignages insérés avec succès!")
    
    # Display inserted testimonials
    for testimonial in testimonials:
        print(f"\n📝 {testimonial['userName']} ({testimonial['country']})")
        print(f"   ⭐ {testimonial['rating']} étoiles")
        print(f"   💬 {testimonial['comment'][:50]}...")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_testimonials())
