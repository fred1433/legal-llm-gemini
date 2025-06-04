from fastapi import APIRouter, HTTPException
from app.models.schemas import DocumentGenerationRequest, DocumentGenerationResponse
from app.services.llm_service import llm_service

router = APIRouter()

@router.post("/generate-document", response_model=DocumentGenerationResponse)
async def generate_document(request: DocumentGenerationRequest):
    """Génère un document juridique selon le type et les paramètres fournis"""
    try:
        # Générer le document
        document_content = llm_service.generate_document(
            request.type_document, 
            request.parametres
        )
        
        return DocumentGenerationResponse(
            document_genere=document_content,
            type_document=request.type_document,
            success=True,
            message="Document généré avec succès"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du document: {str(e)}"
        ) 