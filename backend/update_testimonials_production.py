"""
Script pour ajouter les traductions anglaises aux témoignages en production
"""
import requests
import os

BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://tradalife.com")
API_URL = f"{BACKEND_URL}/api"

# Traductions
testimonials_updates = [
    {
        "userName": "Kevin A.",
        "comment_fr": "Grâce à TRADALIFE, j'ai enfin compris comment gérer mes positions et mes risques. Les signaux sont clairs, précis et les résultats sont là ! En quelques semaines, j'ai pu améliorer ma performance de manière constante. Une équipe sérieuse et toujours disponible. Merci à Moka et toute la communauté !",
        "comment_en": "Thanks to TRADALIFE, I finally understood how to manage my positions and risks. The signals are clear, precise and the results are there! In just a few weeks, I was able to consistently improve my performance. A serious team that is always available. Thanks to Moka and the entire community!"
    },
    {
        "userName": "Amy D.",
        "comment_fr": "TRADALIFE, c'est plus qu'un groupe de trading, c'est une vraie famille ! L'accompagnement est professionnel, les formations sont faciles à suivre, et les conseils m'ont permis de prendre confiance dans mes trades. Je recommande à 100 % pour tous ceux qui veulent progresser rapidement.",
        "comment_en": "TRADALIFE is more than a trading group, it's a real family! The support is professional, the training is easy to follow, and the advice has helped me gain confidence in my trades. I recommend 100% for anyone who wants to progress quickly."
    },
    {
        "userName": "Sami L.",
        "comment_fr": "J'ai testé plusieurs communautés de trading avant TRADALIFE, mais aucune n'offre un tel niveau de transparence et de suivi. Les canaux VIP sont super bien organisés, les résultats sont constants et surtout, on apprend à devenir autonome. Bravo à toute l'équipe ! Merci à MOKA pour sa disponibilité",
        "comment_en": "I tested several trading communities before TRADALIFE, but none offer such a level of transparency and follow-up. The VIP channels are super well organized, the results are consistent and above all, we learn to become independent. Congratulations to the whole team! Thanks to MOKA for his availability"
    }
]

print("=" * 60)
print("🌍 MISE À JOUR DES TRADUCTIONS EN PRODUCTION")
print("=" * 60)
print(f"API URL: {API_URL}\n")

# Note: Nous devons créer un endpoint pour mettre à jour les témoignages
# Pour l'instant, affichons les données qui doivent être mises à jour

for testimonial in testimonials_updates:
    print(f"Témoignage: {testimonial['userName']}")
    print(f"  FR: {testimonial['comment_fr'][:50]}...")
    print(f"  EN: {testimonial['comment_en'][:50]}...")
    print()

print("\n⚠️  Il faut créer un endpoint admin pour mettre à jour les témoignages.")
print("Pour l'instant, les traductions doivent être ajoutées manuellement dans MongoDB.")
