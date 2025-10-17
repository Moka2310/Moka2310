"""
Routes API pour le chatbot
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chat_service import ChatService
import uuid

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialiser le service de chat
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    language: str = "fr"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint pour envoyer un message au chatbot
    """
    try:
        # Générer un session_id si non fourni
        session_id = request.session_id or str(uuid.uuid4())
        
        # Envoyer le message au service de chat
        response = await chat_service.send_message(
            message=request.message,
            session_id=session_id,
            language=request.language
        )
        
        return ChatResponse(
            response=response,
            session_id=session_id
        )
    except Exception as e:
        print(f"Erreur dans l'endpoint de chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement de votre message: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Vérifie que le service de chat est opérationnel
    """
    try:
        # Vérifier que le service peut être initialisé
        _ = ChatService()
        return {"status": "healthy", "service": "chat"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service de chat non disponible: {str(e)}"
        )
