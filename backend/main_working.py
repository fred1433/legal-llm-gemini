# main_working.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn

# Simplified Pydantic models
class DocumentRequest(BaseModel):
    type_document: str
    parametres: dict

class DocumentResponse(BaseModel):
    document_genere: str
    type_document: str
    success: bool
    message: str

class SearchRequest(BaseModel):
    question: str

class Source(BaseModel):
    contenu: str
    nom_fichier: str
    score: float

class SearchResponse(BaseModel):
    reponse: str
    sources: List[Source]
    question: str
    success: bool
    message: str

class ChatRequest(BaseModel):
    message: str
    historique: List[dict] = []

class ChatResponse(BaseModel):
    reponse: str
    historique: List[dict]
    success: bool
    message: str

# FastAPI Application
app = FastAPI(
    title="🏛️ Legal LLM API",
    description="API for a legal assistant - Demo Version",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Main endpoints
@app.get("/")
async def root():
    return {
        "message": "🏛️ Legal LLM API active",
        "version": "1.0.0",
        "status": "ready",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "generate": "/api/v1/generate-document",
            "search": "/api/v1/legal-search",
            "chat": "/api/v1/chat"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "legal-llm"}

# Document generation
@app.post("/api/v1/generate-document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """Generates a legal document according to type and provided parameters"""
    
    if request.type_document == "contrat":
        document = f"""
EMPLOYMENT CONTRACT

Between:
- Employer: {request.parametres.get('employeur', '[EMPLOYER]')}
- Employee: {request.parametres.get('employe', '[EMPLOYEE]')}

Article 1 - Purpose of contract
This contract aims to hire {request.parametres.get('employe', '[EMPLOYEE]')} 
as {request.parametres.get('poste', '[POSITION]')}.

Article 2 - Compensation
The gross monthly salary is set at ${request.parametres.get('salaire', '[SALARY]')}.

Article 3 - Duration
The contract is concluded for a {request.parametres.get('duree', 'permanent')} duration.

Made in [LOCATION], on [DATE]
Signatures: [SIGNATURES]
"""
    
    elif request.type_document == "mise_en_demeure":
        document = f"""
DEMAND LETTER

Sender: {request.parametres.get('expediteur', '[SENDER]')}
Recipient: {request.parametres.get('destinataire', '[RECIPIENT]')}

Subject: Demand letter - {request.parametres.get('objet', '[SUBJECT]')}

Dear Sir/Madam,

By this letter, we formally demand that you fulfill your obligations 
regarding {request.parametres.get('objet', '[DESCRIPTION]')}.

You have {request.parametres.get('delai', '15')} days 
to regularize your situation.

Failing this, we reserve the right to take any legal action.

Made in [LOCATION], on [DATE]
"""
    
    else:
        document = f"Document of type '{request.type_document}' generated successfully.\n\nParameters used:\n"
        for key, value in request.parametres.items():
            document += f"- {key}: {value}\n"
    
    return DocumentResponse(
        document_genere=document,
        type_document=request.type_document,
        success=True,
        message="Document generated successfully"
    )

# Legal research
@app.post("/api/v1/legal-search", response_model=SearchResponse)
async def legal_search(request: SearchRequest):
    """Performs legal research with RAG (demo version)"""
    
    # Mock sources
    sources = [
        Source(
            contenu="Employment contracts must comply with labor law provisions. Probationary period cannot exceed 2 months for employees and 4 months for executives.",
            nom_fichier="employment_law.txt",
            score=0.95
        ),
        Source(
            contenu="In civil law, contractual liability involves the obligation to repair damage caused by non-performance of a contractual obligation.",
            nom_fichier="civil_law.txt",
            score=0.87
        )
    ]
    
    # Smart mock response
    reponse = f"""
Regarding your question: "{request.question}"

According to current legislation:

1. **Legal framework**: The applicable provisions are found in the Labor Code and Civil Code depending on the area concerned.

2. **Important points**:
   - Contractual obligations must be respected
   - In case of default, sanctions may apply
   - It is recommended to consult a lawyer for specific cases

3. **Legal references**: This response is based on {len(sources)} relevant source(s) from the legal corpus.

⚠️ **Warning**: This response is generated for demonstration purposes and does not constitute personalized legal advice.
"""
    
    return SearchResponse(
        reponse=reponse,
        sources=sources,
        question=request.question,
        success=True,
        message="Search completed successfully"
    )

# Chat assistant
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_interaction(request: ChatRequest):
    """Handles interaction with the legal chatbot (demo version)"""
    
    # Smart responses based on keywords
    message_lower = request.message.lower()
    
    if any(word in message_lower for word in ['contract', 'employment', 'work']):
        reponse = "I can help you with employment contracts. A contract must include duration, compensation, and working conditions according to labor law."
    elif any(word in message_lower for word in ['liability', 'damage', 'compensation']):
        reponse = "Regarding liability, it's important to distinguish between civil and criminal liability. Civil liability aims to compensate damage, while criminal liability sanctions offenses."
    elif any(word in message_lower for word in ['probation', 'trial period']):
        reponse = "The probationary period allows the employer to evaluate the employee. Its maximum duration depends on the position: 2 months for employees, 4 months for executives."
    elif any(word in message_lower for word in ['hello', 'hi', 'good']):
        reponse = "Hello! I'm your virtual legal assistant. How can I help you today? I can assist with contracts, legal research, and general legal questions."
    elif any(word in message_lower for word in ['thank', 'thanks']):
        reponse = "You're welcome! Don't hesitate to ask if you have other legal questions. I'm here to help."
    else:
        reponse = "Thank you for your question. For specific legal advice, I recommend consulting a qualified lawyer. I can provide general information on various legal topics."
    
    # Add to history
    new_historique = request.historique.copy()
    new_historique.append({"role": "user", "content": request.message})
    new_historique.append({"role": "assistant", "content": reponse})
    
    return ChatResponse(
        reponse=reponse,
        historique=new_historique,
        success=True,
        message="Chat completed successfully"
    )

# Server startup
if __name__ == "__main__":
    print("🚀 Starting Legal LLM Server...")
    print("📖 Documentation available at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000) 