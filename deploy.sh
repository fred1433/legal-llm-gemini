#!/bin/bash

echo "🚀 Déploiement Legal LLM - Surge + Render"
echo "======================================="

# Étape 1: Déployer le frontend sur Surge
echo "📁 1. Déploiement Frontend sur Surge..."
cd frontend

echo "🔗 Entrez votre domaine Surge souhaité (ex: my-legal-llm.surge.sh):"
read SURGE_DOMAIN

echo "📤 Déploiement vers $SURGE_DOMAIN..."
surge . $SURGE_DOMAIN

echo "✅ Frontend déployé sur: https://$SURGE_DOMAIN"

cd ..

echo ""
echo "🚀 2. Étapes Backend sur Render:"
echo "================================"
echo "1. Aller sur https://render.com"
echo "2. Créer un nouveau Web Service"
echo "3. Connecter ce repository Git"
echo "4. Configurer:"
echo "   - Build: pip install -r backend/requirements.txt"
echo "   - Start: cd backend && python main.py"
echo "   - Environment: GEMINI_API_KEY=AIzaSyB6bgowsUoIjSuXrild8BZ263fc9z-wwNo"
echo ""
echo "🔄 3. Après déploiement backend:"
echo "================================"
echo "1. Récupérer l'URL Render (ex: https://mon-api.onrender.com)"
echo "2. Mettre à jour frontend/js/api_config.js"
echo "3. Re-déployer sur Surge"
echo ""
echo "✨ Votre app sera live !" 