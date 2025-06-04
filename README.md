# 🏛️ Prototype LLM Juridique

## 📋 Description

Prototype d'application web démontrant les capacités d'un Large Language Model (Gemini 2.5) pour des tâches juridiques. L'application comprend :

- **🏛️ Frontend statique** : Interface web moderne avec HTML5, CSS3 et JavaScript Vanilla
- **⚡ Backend API** : API REST avec FastAPI, intégration Gemini et RAG avec FAISS
- **🎯 Trois fonctionnalités principales** :
  1. 📄 Génération de documents juridiques
  2. 🔍 Recherche juridique avec RAG
  3. 💬 Assistant virtuel conversationnel

## 🏗️ Architecture

```
proto_llm_juridique/
├── frontend/                 # Application web statique
│   ├── index.html           # Page principale
│   ├── css/style.css        # Styles personnalisés
│   └── js/
│       ├── main.js          # Logique principale
│       └── api_config.js    # Configuration API
└── backend/                 # API FastAPI
    ├── main.py              # Application principale
    ├── requirements.txt     # Dépendances Python
    ├── .env                 # Variables d'environnement
    ├── app/
    │   ├── api_v1/          # Endpoints API v1
    │   ├── core/            # Configuration
    │   ├── models/          # Schémas Pydantic
    │   └── services/        # Services métier
    └── data/                # Documents pour RAG
```

## 🚀 Installation et Lancement Local

### Prérequis

- Python 3.9+
- Node.js (pour Surge.sh uniquement)
- Extension VS Code "Live Server" (recommandée)

### 1. Configuration du Backend

```bash
# Naviguer vers le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur macOS/Linux :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API Gemini
# Éditer le fichier .env et remplacer VOTRE_CLÉ_API_ICI par votre vraie clé API
```

### 2. Obtenir une clé API Gemini

1. Aller sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créer une nouvelle clé API
3. Copier la clé dans le fichier `backend/.env`

### 3. Lancer le Backend

```bash
# Depuis le dossier backend/
uvicorn main:app --reload --port 8000
```

Le backend sera accessible sur `http://localhost:8000`
- Documentation API : `http://localhost:8000/docs`
- Health check : `http://localhost:8000/health`

### 4. Lancer le Frontend

**Option 1 : Live Server (Recommandée)**
1. Ouvrir le dossier `frontend/` dans VS Code
2. Clic droit sur `index.html` → "Open with Live Server"
3. L'application s'ouvre sur `http://localhost:5500`

**Option 2 : Serveur HTTP simple**
```bash
# Depuis le dossier frontend/
python -m http.server 8080
# Puis aller sur http://localhost:8080
```

## 🧪 Test des Fonctionnalités

### Génération de Documents
1. Sélectionner "Contrat de travail"
2. Remplir les champs (employeur, employé, poste, salaire)
3. Cliquer "Générer le document"

### Recherche Juridique
1. Poser une question comme : "Quelle est la durée maximale de la période d'essai ?"
2. Voir la réponse avec les sources consultées

### Chat Assistant
1. Taper un message comme : "Expliquez-moi la responsabilité contractuelle"
2. Converser avec l'assistant

## 📱 Déploiement

### Backend sur Render

1. **Préparer le Repository**
   ```bash
   # Créer un nouveau repo GitHub avec le contenu du dossier backend/
   ```

2. **Déployer sur Render**
   - Aller sur [render.com](https://render.com)
   - Créer un nouveau "Web Service"
   - Connecter votre repo GitHub
   - Configuration :
     - **Name** : `proto-llm-juridique-api`
     - **Region** : Europe (Frankfurt)
     - **Branch** : `main`
     - **Runtime** : Python 3
     - **Build Command** : `pip install -r requirements.txt`
     - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Variables d'Environnement**
   - `GEMINI_API_KEY` : Votre clé API Gemini
   - `PYTHON_VERSION` : `3.9.12`

### Frontend sur Surge.sh

1. **Configurer l'URL du Backend**
   ```javascript
   // Dans frontend/js/api_config.js
   const API_BASE_URL = 'https://VOTRE-APP-RENDER.onrender.com/api/v1';
   ```

2. **Déployer avec Surge**
   ```bash
   # Installer Surge CLI
   npm install --global surge
   
   # Depuis le dossier frontend/
   cd frontend
   surge
   
   # Suivre les instructions (choisir un domaine)
   ```

3. **Mettre à jour CORS**
   - Ajouter l'URL Surge dans `backend/main.py` :
   ```python
   origins = [
       "https://votre-site.surge.sh",
       # ... autres origins
   ]
   ```
   - Redéployer le backend

## 🔧 Configuration Avancée

### Utilisation avec une vraie clé Gemini

Pour utiliser Gemini au lieu des données factices :

1. Obtenir une clé API sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Remplacer dans `.env` :
   ```
   GEMINI_API_KEY="votre_vraie_cle_api"
   ```
3. Redémarrer le backend

### Ajouter des documents pour RAG

1. Placer des fichiers `.txt` dans `backend/data/`
2. Redémarrer le backend (les documents sont chargés au démarrage)

## 📊 Structure des Données

### Génération de Documents
```json
{
  "type_document": "contrat",
  "parametres": {
    "employeur": "Entreprise ABC",
    "employe": "Jean Dupont",
    "poste": "Développeur",
    "salaire": "3000"
  }
}
```

### Recherche Juridique
```json
{
  "question": "Quelle est la durée de la période d'essai ?"
}
```

### Chat
```json
{
  "message": "Expliquez la responsabilité contractuelle",
  "historique": [...]
}
```

## ⚠️ Limitations et Notes

- **Démonstration uniquement** : Ne constitue pas un conseil juridique
- **Données factices** : Sans clé Gemini, utilise des réponses préprogrammées
- **RAG simplifié** : Embeddings aléatoires pour la démo
- **Sécurité** : Pas d'authentification (prototype uniquement)

## 🐛 Dépannage

### Le backend ne démarre pas
- Vérifier que l'environnement virtuel est activé
- Installer les dépendances : `pip install -r requirements.txt`
- Vérifier le port 8000 est libre

### Le frontend ne se connecte pas au backend
- Vérifier que le backend fonctionne sur `http://localhost:8000`
- Vérifier l'URL dans `frontend/js/api_config.js`
- Ouvrir la console du navigateur pour voir les erreurs

### Erreurs CORS
- Vérifier la configuration CORS dans `backend/main.py`
- Ajouter l'URL du frontend aux origins autorisées

## 📄 License

Ce projet est un prototype éducatif. Utilisation libre pour l'apprentissage et la démonstration.

## 🤝 Contact

Pour toute question concernant ce prototype, veuillez consulter la documentation ou les logs d'erreur dans la console du navigateur.

---

**⚡ Powered by FastAPI, Gemini 2.5, and Modern Web Technologies** 