from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_interaction(request: ChatRequest):
    """Gère l'interaction avec le chatbot juridique"""
    try:
        # Effectuer l'interaction de chat
        response_text, new_history = llm_service.chat_interaction(
            request.message, 
            request.historique
        )
        
        return ChatResponse(
            reponse=response_text,
            historique=new_history,
            success=True,
            message="Chat effectué avec succès"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'interaction chat: {str(e)}"
        ) 