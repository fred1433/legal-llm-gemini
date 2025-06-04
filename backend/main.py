# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api_v1.router import api_router
from app.services.llm_service import llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage: charger les documents et construire l'index FAISS
    print("Initialisation de l'application...")
    llm_service.load_documents_and_build_index("data")
    print("Application initialisée avec succès!")
    yield
    # Arrêt: cleanup si nécessaire
    print("Arrêt de l'application...")

app = FastAPI(
    title="API LLM Juridique",
    description="API pour un assistant juridique basé sur Gemini 2.5",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS
origins = [
    "http://localhost:5500",  # Live Server pour le développement local
    "http://127.0.0.1:5500",
    "http://localhost:3000",  # Alternatives communes
    "http://localhost:8080",
    # L'URL de Surge.sh sera ajoutée après le déploiement frontend
    # "https://VOTRE-SITE.surge.sh"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # En développement, vous pouvez utiliser ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure le routeur API
app.include_router(api_router, prefix="/api/v1")

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

# Bloc de démarrage direct pour les tests locaux
if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage direct du serveur FastAPI...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 