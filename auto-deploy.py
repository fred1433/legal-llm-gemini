#!/usr/bin/env python3

import requests
import json
import time
import sys

def create_render_service():
    """Crée automatiquement un service web sur Render"""
    
    print("🚀 Auto-déploiement Render - Legal LLM Gemini")
    print("=" * 50)
    
    # Configuration du service
    service_config = {
        "type": "web_service",
        "name": "legal-llm-gemini",
        "repo": "https://github.com/fred1433/legal-llm-gemini",
        "branch": "main",
        "rootDir": "backend",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "python main.py",
        "plan": "free",
        "region": "oregon",
        "envVars": [
            {
                "key": "GEMINI_API_KEY",
                "value": "AIzaSyB6bgowsUoIjSuXrild8BZ263fc9z-wwNo"
            }
        ],
        "numInstances": 1,
        "openPorts": [
            {
                "port": 8000,
                "protocol": "TCP"
            }
        ]
    }
    
    print("📋 Configuration service:")
    print(f"   - Repository: {service_config['repo']}")
    print(f"   - Nom: {service_config['name']}")
    print(f"   - Build: {service_config['buildCommand']}")
    print(f"   - Start: {service_config['startCommand']}")
    print(f"   - Variables d'environnement: GEMINI_API_KEY configurée")
    print()
    
    print("🔑 Pour créer le service automatiquement:")
    print("1. Aller sur: https://dashboard.render.com/")
    print("2. Créer un Personal Access Token dans Account Settings")
    print("3. Revenir ici avec le token")
    print()
    
    # Demander le token API (en cas d'automatisation future)
    token = input("🔐 Coller votre Render API token (ou appuyer sur Entrée pour instructions manuelles): ").strip()
    
    if not token:
        print("\n📋 Instructions manuelles pour Render:")
        print("=" * 40)
        print("1. Aller sur https://dashboard.render.com/")
        print("2. New → Web Service")
        print("3. Connect Repository: fred1433/legal-llm-gemini")
        print("4. Configuration:")
        print(f"   Name: {service_config['name']}")
        print(f"   Root Directory: {service_config['rootDir']}")
        print(f"   Build Command: {service_config['buildCommand']}")
        print(f"   Start Command: {service_config['startCommand']}")
        print("   Environment Variables:")
        for env_var in service_config['envVars']:
            print(f"     {env_var['key']} = {env_var['value']}")
        print("\n5. Deploy!")
        print("\n🔗 URL finale: https://legal-llm-gemini.onrender.com")
        return "https://legal-llm-gemini.onrender.com"
    
    # Si token fourni, tentative d'automatisation
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 Création automatique du service...")
        response = requests.post(
            "https://api.render.com/v1/services",
            headers=headers,
            json=service_config
        )
        
        if response.status_code == 201:
            service = response.json()
            service_url = f"https://{service['service']['name']}.onrender.com"
            print(f"✅ Service créé avec succès!")
            print(f"🔗 URL: {service_url}")
            return service_url
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return None

def deploy_frontend():
    """Déploie le frontend sur Surge"""
    print("\n🌐 Déploiement Frontend sur Surge...")
    print("=" * 40)
    
    import subprocess
    import os
    
    try:
        # Aller dans le dossier frontend
        os.chdir("frontend")
        
        # Déploiement Surge avec domaine prédéfini
        domain = "legal-llm-ai.surge.sh"
        print(f"📤 Déploiement vers: {domain}")
        
        # Commande surge automatisée
        process = subprocess.Popen(
            ["surge", ".", domain],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Fournir le domaine automatiquement
        stdout, stderr = process.communicate(input=domain)
        
        if process.returncode == 0:
            print(f"✅ Frontend déployé sur: https://{domain}")
            return f"https://{domain}"
        else:
            print(f"❌ Erreur Surge: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur frontend: {e}")
        return None
    finally:
        os.chdir("..")

def main():
    print("🤖 DÉPLOIEMENT AUTOMATISÉ COMPLET")
    print("=" * 50)
    
    # Étape 1: Backend sur Render
    backend_url = create_render_service()
    
    # Étape 2: Frontend sur Surge
    frontend_url = deploy_frontend()
    
    # Résumé final
    print("\n🎉 DÉPLOIEMENT TERMINÉ!")
    print("=" * 30)
    if backend_url:
        print(f"🏛️ Backend: {backend_url}")
    if frontend_url:
        print(f"🌐 Frontend: {frontend_url}")
        print(f"📱 Application live: {frontend_url}")
    
    print("\n🔗 Configuration automatique:")
    print("   - Frontend détecte automatiquement l'environnement")
    print("   - API Gemini configurée et prête")
    print("   - HTTPS activé automatiquement")

if __name__ == "__main__":
    main() 