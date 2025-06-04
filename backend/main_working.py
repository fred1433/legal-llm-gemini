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
    
    # Mock sources based on new English legal documents
    sources = [
        Source(
            contenu="Employment contracts should include job title, compensation structure, working hours, probationary period terms, and termination procedures. Probationary periods typically range from 3-6 months for entry-level positions to 12-24 months for executive roles.",
            nom_fichier="employment_law.txt",
            score=0.95
        ),
        Source(
            contenu="A breach of contract occurs when one party fails to perform contractual obligations. Remedies include compensatory damages, consequential damages, and specific performance. Demand letters should contain clear breach description and reasonable compliance deadlines.",
            nom_fichier="contract_law.txt",
            score=0.87
        )
    ]
    
    # Enhanced smart mock response
    reponse = f"""
Regarding your question: "{request.question}"

Based on common law principles and legal best practices:

1. **Legal Framework**: Contract law governs most commercial relationships, with specific employment regulations varying by jurisdiction.

2. **Key Considerations**:
   - Written agreements provide better legal protection than verbal arrangements
   - Limitation of liability clauses can protect against excessive damages
   - Force majeure provisions address extraordinary circumstances
   - Confidentiality terms protect sensitive business information

3. **Professional Recommendation**: For complex legal matters, consult with a qualified attorney familiar with your jurisdiction's specific requirements.

📚 **Sources**: This response draws from {len(sources)} relevant legal document(s) in our knowledge base.

⚠️ **Disclaimer**: This information is for educational purposes only and does not constitute legal advice.
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
    
    # Enhanced smart responses based on keywords
    message_lower = request.message.lower()
    
    if any(word in message_lower for word in ['contract', 'employment', 'hire', 'job']):
        reponse = "I can help with employment contracts! Key elements include job description, compensation, working hours, probationary terms, and termination procedures. Would you like me to explain any specific aspect?"
    elif any(word in message_lower for word in ['nda', 'non-disclosure', 'confidential', 'secret']):
        reponse = "Non-Disclosure Agreements (NDAs) protect sensitive information. They should define what's confidential, permitted uses, duration of obligations, and consequences for breach. Need help with specific NDA terms?"
    elif any(word in message_lower for word in ['breach', 'violation', 'damages', 'lawsuit']):
        reponse = "Contract breaches can be material (major) or minor. Remedies include compensatory damages, consequential damages, or specific performance. The severity determines available legal options."
    elif any(word in message_lower for word in ['demand', 'letter', 'notice', 'compliance']):
        reponse = "Demand letters formally request contract compliance. Include: clear breach description, specific remedy requested, reasonable deadline, and consequences of non-compliance. This often resolves disputes without litigation."
    elif any(word in message_lower for word in ['termination', 'fire', 'quit', 'resign']):
        reponse = "Employment termination requires proper procedures. At-will employment allows termination without cause, but just-cause termination needs documentation. Notice periods and severance depend on contract terms and local law."
    elif any(word in message_lower for word in ['hello', 'hi', 'good', 'hey']):
        reponse = "Hello! I'm your AI legal assistant specializing in contract law, employment matters, and business agreements. I can help explain legal concepts, document structures, and best practices. What legal topic interests you?"
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        reponse = "You're very welcome! I'm here to help with any legal questions about contracts, employment law, business agreements, or other legal topics. Feel free to ask anything else!"
    else:
        reponse = f"That's an interesting question about: '{request.message}'. While I can provide general legal information, I recommend consulting with a licensed attorney for specific legal advice tailored to your situation."
    
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