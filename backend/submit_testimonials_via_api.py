import requests
import os

# Backend URL
BACKEND_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://tradalife.com")
API_URL = f"{BACKEND_URL}/api"

# Témoignages à soumettre
testimonials = [
    {
        "userName": "Kevin A.",
        "country": "Montréal, Canada",
        "comment": "Grâce à TRADALIFE, j'ai enfin compris comment gérer mes positions et mes risques. Les signaux sont clairs, précis et les résultats sont là ! En quelques semaines, j'ai pu améliorer ma performance de manière constante. Une équipe sérieuse et toujours disponible. Merci à Moka et toute la communauté !",
        "rating": 5
    },
    {
        "userName": "Amy D.",
        "country": "Abidjan, Côte d'Ivoire",
        "comment": "TRADALIFE, c'est plus qu'un groupe de trading, c'est une vraie famille ! L'accompagnement est professionnel, les formations sont faciles à suivre, et les conseils m'ont permis de prendre confiance dans mes trades. Je recommande à 100 % pour tous ceux qui veulent progresser rapidement.",
        "rating": 5
    },
    {
        "userName": "Sami L.",
        "country": "Nice, France",
        "comment": "J'ai testé plusieurs communautés de trading avant TRADALIFE, mais aucune n'offre un tel niveau de transparence et de suivi. Les canaux VIP sont super bien organisés, les résultats sont constants et surtout, on apprend à devenir autonome. Bravo à toute l'équipe ! Merci à MOKA pour sa disponibilité",
        "rating": 5
    }
]

print(f"🌐 Connexion à : {API_URL}")
print(f"📝 Soumission de {len(testimonials)} témoignages...\n")

for i, testimonial in enumerate(testimonials, 1):
    try:
        response = requests.post(
            f"{API_URL}/testimonials/submit",
            json=testimonial,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Témoignage {i} soumis avec succès : {testimonial['userName']}")
        else:
            print(f"❌ Erreur {response.status_code} pour {testimonial['userName']}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la soumission de {testimonial['userName']}: {str(e)}")

print("\n📋 Les témoignages ont été soumis. Un administrateur doit maintenant les approuver via le panneau admin.")
