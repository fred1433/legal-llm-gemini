from pydantic import BaseModel
from typing import List, Optional

# Génération de documents
class DocumentGenerationRequest(BaseModel):
    type_document: str  # "contrat", "mise_en_demeure", "courrier_formel", etc.
    parametres: dict  # Paramètres spécifiques selon le type de document

class DocumentGenerationResponse(BaseModel):
    document_genere: str
    type_document: str
    success: bool
    message: Optional[str] = None

# Recherche juridique (RAG)
class LegalSearchRequest(BaseModel):
    question: str
    contexte: Optional[str] = None

class SourceDocument(BaseModel):
    contenu: str
    nom_fichier: str
    score: float

class LegalSearchResponse(BaseModel):
    reponse: str
    sources: List[SourceDocument]
    question: str
    success: bool
    message: Optional[str] = None

# Chat
class ChatMessage(BaseModel):
    role: str  # "user" ou "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    historique: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reponse: str
    historique: List[ChatMessage]
    success: bool
    message: Optional[str] = None 