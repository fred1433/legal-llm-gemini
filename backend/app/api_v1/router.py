# app/api_v1/router.py

from fastapi import APIRouter
from app.api_v1.endpoints import generation, research, chat

api_router = APIRouter()

# Inclure tous les routeurs d'endpoints
api_router.include_router(
    generation.router, 
    tags=["Generation de Documents"]
)

api_router.include_router(
    research.router, 
    tags=["Recherche Juridique"]
)

api_router.include_router(
    chat.router, 
    tags=["Chat Assistant"]
) 