#!/usr/bin/env python3
"""
Test minimal pour FastAPI
"""

from fastapi import FastAPI
import uvicorn
import sys

# Créer l'app FastAPI
app = FastAPI(title="Test Minimal")

@app.get("/")
def read_root():
    return {"message": "✅ Serveur FastAPI fonctionne !"}

@app.get("/test")
def test():
    return {"status": "OK", "version": "1.0"}

def main():
    print("🔧 Test minimal FastAPI")
    print(f"Python version: {sys.version}")
    print("Démarrage du serveur sur http://127.0.0.1:8000")
    
    try:
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 