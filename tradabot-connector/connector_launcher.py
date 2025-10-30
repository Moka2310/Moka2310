"""
TRADABOT Connecteur - Lanceur
Lit la configuration depuis tradabot_config.json
"""
import json
import os
import sys

def main():
    """Lance le connecteur avec la configuration"""
    
    # Vérifier que le fichier de config existe
    if not os.path.exists('tradabot_config.json'):
        print("❌ Erreur: Fichier de configuration manquant")
        print("")
        print("Veuillez télécharger votre configuration depuis:")
        print("https://edushop-portal.emergent.host/tradabot-web")
        print("")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Charger la configuration
    try:
        with open('tradabot_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture configuration: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Vérifier que le token est présent
    auth_token = config.get('authToken', '')
    if not auth_token:
        print("❌ Erreur: Token d'authentification manquant dans la configuration")
        print("")
        print("Veuillez re-télécharger votre configuration depuis le site web")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    # Définir les variables d'environnement
    os.environ['AUTH_TOKEN'] = auth_token
    os.environ['BACKEND_URL'] = config.get('backendUrl', 'https://edushop-portal.emergent.host')
    
    print("✅ Configuration chargée")
    print(f"🔗 Backend: {os.environ['BACKEND_URL']}")
    print("")
    
    # Importer et lancer le connecteur
    try:
        from connector import TradabotConnector
        
        connector = TradabotConnector(
            os.environ['BACKEND_URL'],
            os.environ['AUTH_TOKEN']
        )
        connector.run()
        
    except ImportError as e:
        print(f"❌ Erreur: Dépendances manquantes")
        print("")
        print("Veuillez exécuter INSTALLER.bat d'abord")
        print("")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)
    except KeyboardInterrupt:
        print("")
        print("⏹️  Arrêt du connecteur...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    main()
