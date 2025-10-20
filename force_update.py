"""
Script direct pour mettre à jour les témoignages via MongoDB de production
Ce script se connecte directement à la base de données
"""
import requests

# On va appeler un nouvel endpoint qui force la mise à jour
url = "https://tradalife.com/api/admin/force-update-testimonials"

data = {
    "secret_key": "tradalife-admin-promote-2025",
    "testimonials": [
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
}

print("🔄 Mise à jour forcée des témoignages...")
response = requests.post(url, json=data, timeout=30)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
