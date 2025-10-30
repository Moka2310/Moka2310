"""
Script pour créer le package TRADABOT Connector
Version simplifiée - Pas besoin de compilation
"""
import os
import zipfile
import shutil

print("📦 Création du package TRADABOT Connector...")
print()

# Nettoyer l'ancien package
if os.path.exists('TRADABOT_CONNECTOR_SIMPLE.zip'):
    os.remove('TRADABOT_CONNECTOR_SIMPLE.zip')
    print("🗑️  Ancien package supprimé")

# Créer le ZIP avec tous les fichiers nécessaires
print("📦 Création du nouveau package...")
with zipfile.ZipFile('TRADABOT_CONNECTOR_SIMPLE.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Ajouter les scripts d'installation et de lancement
    zipf.write('INSTALLATION_SIMPLE.bat', 'TRADABOT/INSTALLATION_SIMPLE.bat')
    zipf.write('DEMARRER_TRADABOT.bat', 'TRADABOT/DEMARRER_TRADABOT.bat')
    
    # Ajouter le programme Python
    zipf.write('tradabot_simple.py', 'TRADABOT/tradabot_simple.py')
    
    # Ajouter le README
    zipf.write('README_SIMPLE.txt', 'TRADABOT/README_SIMPLE.txt')
    
    # Créer un exemple de config (vide)
    config_example = """{
  "_comment": "Téléchargez votre configuration depuis https://tradalife.com/tradabot-web",
  "authToken": "VOTRE_TOKEN_ICI",
  "backendUrl": "https://edushop-portal.emergent.host",
  "mt4Login": "12345678",
  "mt4Password": "VotreMotDePasse",
  "mt4Server": "ICMarkets-Live",
  "channels": {
    "forex": true,
    "crypto": true,
    "gold": true,
    "indices": true,
    "commodites": true
  },
  "lots": {
    "forex": 0.01,
    "crypto": 0.01,
    "gold": 0.01,
    "indices": 0.01,
    "commodites": 0.01
  },
  "breakevenEnabled": true
}"""
    zipf.writestr('TRADABOT/config_example.json', config_example)

# Copier aussi dans le dossier courant pour le téléchargement
shutil.copy('TRADABOT_CONNECTOR_SIMPLE.zip', 'TRADABOT_CONNECTOR_BUILD.zip')

print("✅ Package créé: TRADABOT_CONNECTOR_SIMPLE.zip")
print("✅ Copié vers: TRADABOT_CONNECTOR_BUILD.zip")
print()
print("📦 Contenu du package:")
print("   - INSTALLATION_SIMPLE.bat (installation automatique)")
print("   - DEMARRER_TRADABOT.bat (lancement du bot)")
print("   - tradabot_simple.py (programme principal)")
print("   - README_SIMPLE.txt (instructions)")
print("   - config_example.json (exemple de configuration)")
print()
print("🎯 Le package est prêt à être distribué!")
print()
print("📥 Taille du fichier:", os.path.getsize('TRADABOT_CONNECTOR_BUILD.zip') // 1024, "KB")


