"""
Chat service pour le chatbot AI du site Tradalife
Utilise OpenAI GPT-4o-mini via Emergent LLM Key
"""
import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

class ChatService:
    def __init__(self):
        self.api_key = os.environ.get("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def get_system_message(self, language: str = "fr") -> str:
        """Retourne le message système selon la langue"""
        if language == "en":
            return """You are a professional customer support assistant for Tradalife, an online platform offering professional trading training courses.

Your role:
- Provide accurate information about our training courses and services
- Assist customers with registration, KYC, and purchase processes
- Answer questions about payment methods and prices (all in CAD)
- Provide technical support
- Maintain a professional and helpful tone

Key Information:
- Payment methods: Stripe and PayPal (prices in CAD)
- KYC (Know Your Customer) verification is required before making purchases
- After purchase, customers receive access to private training videos and VIP Telegram channels
- Registration requires email and password
- All courses include lifetime access and VIP community support

Guidelines:
- Be professional, clear, and helpful
- If you don't know something specific, advise customers to contact support at kalot2310@gmail.com
- For technical issues, suggest checking the FAQ or contacting support
- Always be courteous and solution-oriented"""
        else:
            return """Vous êtes un assistant de support client professionnel pour Tradalife, une plateforme en ligne offrant des formations professionnelles en trading.

Votre rôle :
- Fournir des informations précises sur nos formations et services
- Assister les clients avec l'inscription, le KYC et les processus d'achat
- Répondre aux questions sur les méthodes de paiement et les prix (tous en CAD)
- Fournir un support technique
- Maintenir un ton professionnel et serviable

Informations clés :
- Méthodes de paiement : Stripe et PayPal (prix en CAD)
- La vérification KYC (Know Your Customer) est requise avant tout achat
- Après l'achat, les clients reçoivent l'accès aux vidéos de formation privées et aux canaux Telegram VIP
- L'inscription nécessite un email et un mot de passe
- Toutes les formations incluent un accès à vie et un support communautaire VIP

Directives :
- Soyez professionnel, clair et serviable
- Si vous ne connaissez pas quelque chose de spécifique, conseillez aux clients de contacter le support à kalot2310@gmail.com
- Pour les problèmes techniques, suggérez de consulter la FAQ ou de contacter le support
- Soyez toujours courtois et orienté solution"""
    
    async def send_message(self, message: str, session_id: str, language: str = "fr") -> str:
        """
        Envoie un message au chatbot et retourne la réponse
        
        Args:
            message: Le message de l'utilisateur
            session_id: ID de session unique pour le chat
            language: Langue (fr ou en)
        
        Returns:
            La réponse du chatbot
        """
        try:
            # Créer une instance de chat avec le message système approprié
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=self.get_system_message(language)
            ).with_model("openai", "gpt-4o-mini")
            
            # Créer le message utilisateur
            user_message = UserMessage(text=message)
            
            # Envoyer le message et obtenir la réponse
            response = await chat.send_message(user_message)
            
            return response
        except Exception as e:
            print(f"Erreur dans le service de chat: {str(e)}")
            if language == "en":
                return "I apologize, but I'm having trouble processing your request at the moment. Please try again or contact support at kalot2310@gmail.com"
            else:
                return "Je m'excuse, mais j'ai des difficultés à traiter votre demande pour le moment. Veuillez réessayer ou contacter le support à kalot2310@gmail.com"
