#!/usr/bin/env python3

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Démarrage du serveur FastAPI...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 