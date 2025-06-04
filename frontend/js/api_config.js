// Configuration de l'API Backend
// Mettre à jour cette URL après le déploiement du backend sur Render

// Pour le développement local
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Pour la production (à décommenter après déploiement)
// const API_BASE_URL = 'https://VOTRE_APP_RENDER.onrender.com/api/v1';

// Export pour utilisation dans main.js
window.API_CONFIG = {
    BASE_URL: API_BASE_URL,
    ENDPOINTS: {
        GENERATE_DOCUMENT: '/generate-document',
        LEGAL_SEARCH: '/legal-search',
        CHAT: '/chat'
    }
}; 