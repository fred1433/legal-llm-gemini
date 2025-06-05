# main.py - Production Legal LLM API with Gemini 2.5 Flash Preview
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio
import time

# Load environment variables
load_dotenv()

# Configure Gemini - Support multiple env var names
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Error: No API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY")
else:
    print(f"✅ API key loaded: {api_key[:10]}...")
    
genai.configure(api_key=api_key)

# Pydantic models
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
    title="🏛️ Legal LLM API - Gemini 2.5 Flash Preview",
    description="AI Legal Assistant powered by Gemini 2.5 Flash Preview-0520",
    version="2.0.0"
)

# CORS Configuration - Production ready
origins = [
    "https://legal-llm-ai.surge.sh",
    "https://*.surge.sh",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporary pour debug - plus permissif
    allow_credentials=False,  # False avec origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini model configuration
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

async def call_gemini(prompt: str) -> str:
    """Call Gemini API with error handling"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

# Main endpoints
@app.get("/")
async def root():
    return {
        "message": "🏛️ Legal LLM API active - Powered by Gemini 2.5 Flash Preview",
        "version": "2.0.0",
        "status": "ready",
        "ai_model": "gemini-2.5-flash-preview-05-20",
        "deployment": "production",
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
    return {"status": "healthy", "service": "legal-llm-gemini", "ai_model": "gemini-2.5-flash-preview-05-20"}

# Document generation with real Gemini
@app.post("/api/v1/generate-document", response_model=DocumentResponse)
async def generate_document(request: DocumentRequest):
    """Generates a legal document using Gemini 2.5 Flash Preview"""
    
    # Build specialized prompt based on document type
    if request.type_document == "contrat":
        prompt = f"""
Generate a professional employment contract in English with the following details:

- Employer: {request.parametres.get('employeur', 'ABC Company')}
- Employee: {request.parametres.get('employe', 'John Doe')}
- Position: {request.parametres.get('poste', 'Employee')}
- Salary: ${request.parametres.get('salaire', '50000')} annually
- Contract Duration: {request.parametres.get('duree', 'permanent')}

Requirements:
- Include standard legal clauses for employment contracts
- Add sections for: duties, compensation, benefits, termination, confidentiality
- Use formal legal language
- Include typical boilerplate clauses
- Make it ready to sign

Format as a complete legal document.
"""
    
    elif request.type_document == "mise_en_demeure":
        prompt = f"""
Generate a professional demand letter in English with the following details:

- Sender: {request.parametres.get('expediteur', 'Law Firm')}
- Recipient: {request.parametres.get('destinataire', 'Company')}
- Subject: {request.parametres.get('objet', 'Breach of contract')}
- Deadline: {request.parametres.get('delai', '15')} days

Requirements:
- Use formal legal tone
- Clearly state the breach or issue
- Include specific demands and deadlines
- Mention consequences of non-compliance
- Include proper legal formatting
- Make it professional and enforceable

Format as a complete legal demand letter.
"""
    
    else:
        prompt = f"""
Generate a professional legal document of type "{request.type_document}" with these parameters:
{request.parametres}

Use appropriate legal formatting and professional language.
"""

    try:
        # Add timing for user experience
        start_time = time.time()
        document = await call_gemini(prompt)
        generation_time = round(time.time() - start_time, 2)
        
        return DocumentResponse(
            document_genere=document,
            type_document=request.type_document,
            success=True,
            message=f"Document generated successfully using Gemini AI ({generation_time}s)"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Legal research with direct Gemini query
@app.post("/api/v1/legal-search", response_model=SearchResponse)
async def legal_search(request: SearchRequest):
    """Performs legal research using Gemini's knowledge base"""
    
    prompt = f"""
You are a legal research assistant. Answer this legal question comprehensively:

Question: {request.question}

Provide a detailed response that includes:
1. Direct answer to the question
2. Key legal principles involved
3. Important considerations and exceptions
4. Professional recommendations
5. Jurisdictional variations if relevant

Use professional legal terminology and cite general legal principles.
Format your response clearly with headings and bullet points.

Remember to add appropriate disclaimers about consulting licensed attorneys for specific advice.
"""

    try:
        start_time = time.time()
        ai_response = await call_gemini(prompt)
        search_time = round(time.time() - start_time, 2)
        
        # Create mock sources for the interface
        sources = [
            Source(
                contenu="This response is generated from Gemini's comprehensive legal knowledge base, drawing from extensive training on legal texts, case law, and professional legal resources.",
                nom_fichier="gemini_knowledge_base.txt",
                score=0.98
            ),
            Source(
                contenu=f"Query processed using advanced AI reasoning on legal concepts related to: {request.question}",
                nom_fichier="ai_legal_analysis.txt", 
                score=0.95
            )
        ]
        
        return SearchResponse(
            reponse=ai_response,
            sources=sources,
            question=request.question,
            success=True,
            message=f"Legal research completed using Gemini AI ({search_time}s)"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat assistant with real Gemini conversation
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_interaction(request: ChatRequest):
    """Interactive legal chat using Gemini 2.5 Flash Preview"""
    
    # Build conversation context
    conversation_context = ""
    if request.historique:
        conversation_context = "Previous conversation:\n"
        for msg in request.historique[-6:]:  # Last 6 messages for context
            role = "Human" if msg["role"] == "user" else "Assistant"
            conversation_context += f"{role}: {msg['content']}\n"
        conversation_context += "\n"
    
    prompt = f"""
You are a professional AI legal assistant specializing in contract law, employment law, business law, and general legal guidance.

{conversation_context}

Current question: {request.message}

Provide a helpful, professional response that:
- Directly addresses their question
- Uses appropriate legal terminology
- Offers practical guidance when relevant
- Includes appropriate disclaimers
- Maintains a professional yet approachable tone
- Suggests follow-up questions or related topics when helpful

Always remind users to consult with licensed attorneys for specific legal advice.
"""

    try:
        start_time = time.time()
        ai_response = await call_gemini(prompt)
        chat_time = round(time.time() - start_time, 2)
        
        # Update conversation history
        new_historique = request.historique.copy()
        new_historique.append({"role": "user", "content": request.message})
        new_historique.append({"role": "assistant", "content": ai_response})
        
        return ChatResponse(
            reponse=ai_response,
            historique=new_historique,
            success=True,
            message=f"Response generated using Gemini AI ({chat_time}s)"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Production server configuration
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("🚀 Starting Legal LLM Server with Gemini 2.5 Flash Preview...")
    print("🤖 AI Model: gemini-2.5-flash-preview-05-20")
    print(f"🌐 Running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 