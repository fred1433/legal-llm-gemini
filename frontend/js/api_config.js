// Configuration de l'API Backend
// Mettre à jour cette URL après le déploiement du backend sur Render

// Détection automatique environnement
const isLocalhost = window.location.hostname === 'localhost' || 
                   window.location.hostname === '127.0.0.1' ||
                   window.location.hostname === '';

// URLs de configuration
const LOCAL_API_URL = 'http://127.0.0.1:8000/api/v1';
const PRODUCTION_API_URL = 'https://legal-llm-gemini.onrender.com/api/v1';

// Auto-sélection URL basée sur l'environnement
const API_BASE_URL = isLocalhost ? LOCAL_API_URL : PRODUCTION_API_URL;

// Configuration exportée
window.API_CONFIG = {
    BASE_URL: API_BASE_URL,
    ENDPOINTS: {
        GENERATE_DOCUMENT: '/generate-document',
        LEGAL_SEARCH: '/legal-search', 
        CHAT: '/chat'
    },
    ENVIRONMENT: isLocalhost ? 'development' : 'production'
};

console.log(`🚀 API Config: ${window.API_CONFIG.ENVIRONMENT} mode`);
console.log(`🔗 Backend URL: ${API_BASE_URL}`); 