"""
Script pour mettre à jour directement les traductions dans MongoDB production
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'tradalife')

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

async def update_translations():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("=" * 60)
    print("🌍 MISE À JOUR DIRECTE DES TRADUCTIONS")
    print("=" * 60)
    
    for name, texts in translations.items():
        result = await db.testimonials.update_one(
            {"userName": name},
            {"$set": texts}
        )
        
        if result.modified_count > 0:
            print(f"✅ {name} - Traduction mise à jour")
        else:
            print(f"⚠️  {name} - Non trouvé ou déjà à jour")
    
    # Vérifier les résultats
    print("\n" + "=" * 60)
    print("VÉRIFICATION")
    print("=" * 60)
    
    for name in translations.keys():
        testimonial = await db.testimonials.find_one({"userName": name})
        if testimonial:
            has_fr = len(testimonial.get('comment_fr', '')) > 0
            has_en = len(testimonial.get('comment_en', '')) > 0
            print(f"{name}: FR={has_fr}, EN={has_en}")
    
    print("=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(update_translations())
