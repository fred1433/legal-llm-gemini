// Main application for the Legal LLM prototype

// Global variables
let chatHistory = [];

// Utilities
function showLoading(buttonId, textId, loadingId) {
    document.getElementById(buttonId).disabled = true;
    document.getElementById(textId).style.display = 'none';
    document.getElementById(loadingId).style.display = 'inline';
}

function hideLoading(buttonId, textId, loadingId) {
    document.getElementById(buttonId).disabled = false;
    document.getElementById(textId).style.display = 'inline';
    document.getElementById(loadingId).style.display = 'none';
}

function showError(message) {
    alert(`Error: ${message}`);
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert('Text copied to clipboard!');
    }).catch(err => {
        console.error('Copy error:', err);
        alert('Copy error');
    });
}

// API Calls
async function callAPI(endpoint, data) {
    try {
        const response = await fetch(`${window.API_CONFIG.BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Dynamic form field management
function handleDocumentTypeChange() {
    const typeSelect = document.getElementById('type-document');
    const allFields = document.querySelectorAll('.document-fields');
    
    // Hide all fields
    allFields.forEach(field => {
        field.style.display = 'none';
    });
    
    // Show appropriate fields
    if (typeSelect.value) {
        const fieldsToShow = document.getElementById(`${typeSelect.value}-fields`);
        if (fieldsToShow) {
            fieldsToShow.style.display = 'block';
        }
    }
}

// Document generation
async function handleDocumentGeneration(event) {
    event.preventDefault();
    
    const typeDocument = document.getElementById('type-document').value;
    if (!typeDocument) {
        showError('Please select a document type');
        return;
    }

    showLoading('generate-btn', 'generate-text', 'generate-loading');

    try {
        // Collect parameters according to document type
        const parametres = {};
        
        if (typeDocument === 'contrat') {
            parametres.employeur = document.getElementById('employeur').value;
            parametres.employe = document.getElementById('employe').value;
            parametres.poste = document.getElementById('poste').value;
            parametres.salaire = document.getElementById('salaire').value;
            parametres.duree = document.getElementById('duree').value;
        } else if (typeDocument === 'mise_en_demeure') {
            parametres.expediteur = document.getElementById('expediteur').value;
            parametres.destinataire = document.getElementById('destinataire').value;
            parametres.objet = document.getElementById('objet').value;
            parametres.delai = document.getElementById('delai').value;
        }

        const response = await callAPI(window.API_CONFIG.ENDPOINTS.GENERATE_DOCUMENT, {
            type_document: typeDocument,
            parametres: parametres
        });

        // Display result
        document.getElementById('generated-document').textContent = response.document_genere;
        document.getElementById('generation-result').style.display = 'block';
        
        // Scroll to result
        document.getElementById('generation-result').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        showError(`Generation error: ${error.message}`);
    } finally {
        hideLoading('generate-btn', 'generate-text', 'generate-loading');
    }
}

// Legal research
async function handleLegalSearch(event) {
    event.preventDefault();
    
    const question = document.getElementById('legal-question').value.trim();
    if (!question) {
        showError('Please enter a legal question');
        return;
    }

    showLoading('research-btn', 'research-text', 'research-loading');

    try {
        const response = await callAPI(window.API_CONFIG.ENDPOINTS.LEGAL_SEARCH, {
            question: question
        });

        // Display answer
        document.getElementById('research-answer').innerHTML = 
            `<p>${response.reponse.replace(/\n/g, '</p><p>')}</p>`;

        // Display sources
        const sourcesContainer = document.getElementById('research-sources');
        sourcesContainer.innerHTML = '';
        
        response.sources.forEach((source, index) => {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source-item';
            sourceDiv.innerHTML = `
                <div class="source-header">📄 ${source.nom_fichier}</div>
                <div class="source-content">${source.contenu}</div>
                <div class="source-score">Relevance score: ${source.score.toFixed(3)}</div>
            `;
            sourcesContainer.appendChild(sourceDiv);
        });

        // Show results
        document.getElementById('research-result').style.display = 'block';
        
        // Scroll to result
        document.getElementById('research-result').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        showError(`Search error: ${error.message}`);
    } finally {
        hideLoading('research-btn', 'research-text', 'research-loading');
    }
}

// Chat
function addMessageToChat(role, content) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
    messageDiv.innerHTML = `<strong>${role === 'user' ? 'You' : 'Assistant'} :</strong> ${content}`;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function handleChatSubmission(event) {
    event.preventDefault();
    
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }

    // Add user message
    addMessageToChat('user', message);
    input.value = '';

    showLoading('chat-btn', 'chat-text', 'chat-loading');

    try {
        const response = await callAPI(window.API_CONFIG.ENDPOINTS.CHAT, {
            message: message,
            historique: chatHistory
        });

        // Add assistant response
        addMessageToChat('assistant', response.reponse);
        
        // Update history
        chatHistory = response.historique;

    } catch (error) {
        showError(`Chat error: ${error.message}`);
        addMessageToChat('assistant', 'Sorry, I encountered an error. Please try again.');
    } finally {
        hideLoading('chat-btn', 'chat-text', 'chat-loading');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Document type change handler
    document.getElementById('type-document').addEventListener('change', handleDocumentTypeChange);
    
    // Form submission handlers
    document.getElementById('generation-form').addEventListener('submit', handleDocumentGeneration);
    document.getElementById('research-form').addEventListener('submit', handleLegalSearch);
    document.getElementById('chat-form').addEventListener('submit', handleChatSubmission);
    
    console.log('Legal LLM Prototype initialized successfully');
});

// Expose functions globally for buttons onclick
window.copyToClipboard = copyToClipboard; 