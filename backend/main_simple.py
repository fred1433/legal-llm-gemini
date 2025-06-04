# main_simple.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="API LLM Juridique",
    description="API pour un assistant juridique basé sur Gemini 2.5",
    version="1.0.0"
)

# Configuration CORS
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

@app.get("/")
async def root():
    return {
        "message": "API LLM Juridique active",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Test endpoints simplifiés
@app.post("/api/v1/generate-document")
async def generate_document_test(data: dict):
    return {
        "document_genere": "Document de test généré !",
        "type_document": data.get("type_document", "test"),
        "success": True,
        "message": "Test de génération réussi"
    }

@app.post("/api/v1/legal-search")  
async def legal_search_test(data: dict):
    return {
        "reponse": f"Réponse de test à la question: {data.get('question', 'Question test')}",
        "sources": [
            {
                "contenu": "Contenu de test du document juridique...",
                "nom_fichier": "doc_test.txt",
                "score": 0.95
            }
        ],
        "question": data.get("question", "Question test"),
        "success": True,
        "message": "Test de recherche réussi"
    }

@app.post("/api/v1/chat")
async def chat_test(data: dict):
    return {
        "reponse": f"Réponse de test au message: {data.get('message', 'Message test')}",
        "historique": data.get("historique", []) + [
            {"role": "user", "content": data.get("message", "Message test")},
            {"role": "assistant", "content": f"Réponse de test au message: {data.get('message', 'Message test')}"}
        ],
        "success": True,
        "message": "Test de chat réussi"
    }

if __name__ == "__main__":
    print("🚀 Démarrage du serveur de test...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info") 