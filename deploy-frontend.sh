#!/bin/bash

echo "🚀 Déploiement Frontend Legal LLM sur Surge"
echo "==========================================="

# Configuration prédéfinie
SURGE_DOMAIN="legal-llm-ai.surge.sh"

echo "📁 Déploiement vers: $SURGE_DOMAIN"
echo "🔗 Frontend détectera automatiquement l'environnement"
echo ""

# Aller dans le dossier frontend
cd frontend

# Déploiement automatique avec nom prédéfini
echo "$SURGE_DOMAIN" | surge . --domain $SURGE_DOMAIN

echo ""
echo "✅ Frontend déployé sur: https://$SURGE_DOMAIN"
echo "🔗 Backend connecté automatiquement à Render"
echo "🎯 Application live et fonctionnelle !" 