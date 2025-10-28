"""Module d'authentification TRADABOT"""
import requests
import json
from pathlib import Path
from cryptography.fernet import Fernet
from loguru import logger
import config

class AuthManager:
    """Gère l'authentification avec tradalife.com"""
    
    def __init__(self):
        self.token = None
        self.user_info = None
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        self.token_file = config.DATA_DIR / "token.encrypted"
        
    def _get_or_create_key(self):
        """Génère ou récupère la clé de chiffrement"""
        key_file = config.DATA_DIR / "key.bin"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            return key
    
    def login(self, email: str, password: str) -> bool:
        """
        Connexion à tradalife.com
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            
        Returns:
            True si succès, False sinon
        """
        try:
            logger.info(f"Tentative de connexion pour {email}")
            
            # Appel API de connexion
            response = requests.post(
                f"{config.API_BASE_URL}/api/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.user_info = data.get('user')
                
                # Sauvegarder le token de manière sécurisée
                self._save_token()
                
                logger.success(f"Connexion réussie: {email}")
                return True
            else:
                logger.error(f"Erreur de connexion: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Exception lors de la connexion: {e}")
            return False
    
    def _save_token(self):
        """Sauvegarde le token de manière sécurisée"""
        if self.token:
            encrypted_token = self.cipher.encrypt(self.token.encode())
            self.token_file.write_bytes(encrypted_token)
    
    def load_token(self) -> bool:
        """Charge le token sauvegardé"""
        try:
            if self.token_file.exists():
                encrypted_token = self.token_file.read_bytes()
                self.token = self.cipher.decrypt(encrypted_token).decode()
                
                # Vérifier que le token est valide
                if self.verify_access():
                    logger.success("Token chargé et validé")
                    return True
                else:
                    logger.warning("Token invalide")
                    return False
            return False
        except Exception as e:
            logger.error(f"Erreur lors du chargement du token: {e}")
            return False
    
    def verify_access(self) -> bool:
        """
        Vérifie l'accès au bot TRADABOT
        
        Returns:
            True si accès autorisé, False sinon
        """
        try:
            if not self.token:
                return False
            
            response = requests.get(
                config.API_TRADABOT_ACCESS,
                headers={'Authorization': f'Bearer {self.token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                has_access = data.get('hasAccess', False)
                
                if has_access:
                    logger.success("Accès TRADABOT confirmé")
                    return True
                else:
                    logger.warning("❌ Accès TRADABOT refusé")
                    return False
            else:
                logger.error(f"Erreur lors de la vérification: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Exception lors de la vérification: {e}")
            return False
    
    def logout(self):
        """Déconnexion"""
        self.token = None
        self.user_info = None
        if self.token_file.exists():
            self.token_file.unlink()
        logger.info("🚪 Déconnexion")
    
    def get_headers(self) -> dict:
        """Retourne les headers pour les requêtes API"""
        if not self.token:
            return {}
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
