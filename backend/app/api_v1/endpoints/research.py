from fastapi import APIRouter, HTTPException
from app.models.schemas import LegalSearchRequest, LegalSearchResponse
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/legal-search", response_model=LegalSearchResponse)
async def legal_search(request: LegalSearchRequest):
    """Effectue une recherche juridique avec RAG"""
    try:
        # Effectuer la recherche avec RAG
        response_text, sources = llm_service.legal_search_with_rag(request.question)
        
        return LegalSearchResponse(
            reponse=response_text,
            sources=sources,
            question=request.question,
            success=True,
            message="Recherche effectuée avec succès"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la recherche juridique: {str(e)}"
        ) 