# app/services/llm_service.py
import os
import glob
import numpy as np
import faiss
import google.generativeai as genai
from typing import List, Dict, Tuple
from app.core.config import settings
from app.models.schemas import ChatMessage, SourceDocument

class LLMService:
    def __init__(self):
        self.genai_client = None
        self.embedding_model = None
        self.chat_model = None
        self.generation_model = None
        self.faiss_index = None
        self.documents = []
        self.document_embeddings = []
        
        # Initialiser si la clé API est configurée
        if settings.is_gemini_configured:
            self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialise le client Gemini et les modèles"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.generation_model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat_model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            print(f"Erreur lors de l'initialisation de Gemini: {e}")
    
    def load_documents_and_build_index(self, data_folder: str = "data"):
        """Charge les documents et construit l'index FAISS"""
        try:
            if not settings.is_gemini_configured:
                print("Clé API Gemini non configurée, utilisation des documents factices")
                self._create_mock_data()
                return
            
            # Charger les documents
            doc_files = glob.glob(os.path.join(data_folder, "*.txt"))
            self.documents = []
            
            for doc_file in doc_files:
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.documents.append({
                            'content': content,
                            'filename': os.path.basename(doc_file)
                        })
                except Exception as e:
                    print(f"Erreur lors de la lecture de {doc_file}: {e}")
            
            if not self.documents:
                self._create_mock_data()
                return
            
            # Générer les embeddings (simulation pour la démo)
            self._generate_embeddings_mock()
            
        except Exception as e:
            print(f"Erreur lors du chargement des documents: {e}")
            self._create_mock_data()
    
    def _create_mock_data(self):
        """Crée des données factices pour la démo"""
        self.documents = [
            {
                'content': "Le contrat de travail doit respecter les dispositions du Code du travail. La période d'essai ne peut excéder 2 mois pour les employés et 4 mois pour les cadres.",
                'filename': 'droit_travail.txt'
            },
            {
                'content': "En droit civil, la responsabilité contractuelle implique l'obligation de réparer le dommage causé par l'inexécution d'une obligation contractuelle.",
                'filename': 'droit_civil.txt'
            },
            {
                'content': "Le droit pénal sanctionne les infractions définies par la loi. Les sanctions peuvent être des amendes, des peines d'emprisonnement ou des peines alternatives.",
                'filename': 'droit_penal.txt'
            }
        ]
        self._generate_embeddings_mock()
    
    def _generate_embeddings_mock(self):
        """Génère des embeddings factices et construit l'index FAISS"""
        # Pour la démo, on utilise des embeddings aléatoires
        dimension = 384  # Dimension typique pour les embeddings
        self.document_embeddings = np.random.random((len(self.documents), dimension)).astype('float32')
        
        # Construire l'index FAISS
        self.faiss_index = faiss.IndexFlatIP(dimension)  # Index par produit scalaire
        self.faiss_index.add(self.document_embeddings)
    
    def search_documents(self, query: str, top_k: int = 3) -> List[SourceDocument]:
        """Recherche sémantique dans les documents"""
        try:
            if self.faiss_index is None:
                return []
            
            # Pour la démo, génère un embedding aléatoire pour la requête
            query_embedding = np.random.random((1, 384)).astype('float32')
            
            # Recherche dans FAISS
            scores, indices = self.faiss_index.search(query_embedding, top_k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    results.append(SourceDocument(
                        contenu=doc['content'][:200] + "...",  # Limite la longueur
                        nom_fichier=doc['filename'],
                        score=float(score)
                    ))
            
            return results
        
        except Exception as e:
            print(f"Erreur lors de la recherche: {e}")
            return []
    
    def generate_document(self, type_document: str, parametres: dict) -> str:
        """Génère un document juridique"""
        try:
            if not settings.is_gemini_configured:
                return self._generate_mock_document(type_document, parametres)
            
            # Construire le prompt selon le type de document
            prompt = self._build_generation_prompt(type_document, parametres)
            
            response = self.generation_model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            print(f"Erreur lors de la génération: {e}")
            return self._generate_mock_document(type_document, parametres)
    
    def _generate_mock_document(self, type_document: str, parametres: dict) -> str:
        """Génère un document factice pour la démo"""
        if type_document == "contrat":
            return f"""
CONTRAT DE TRAVAIL

Entre :
- Employeur : {parametres.get('employeur', '[NOM EMPLOYEUR]')}
- Employé : {parametres.get('employe', '[NOM EMPLOYÉ]')}

Article 1 - Objet du contrat
Le présent contrat a pour objet l'engagement de {parametres.get('employe', '[NOM EMPLOYÉ]')} 
en qualité de {parametres.get('poste', '[POSTE]')}.

Article 2 - Durée
Le contrat est conclu pour une durée {parametres.get('duree', 'indéterminée')}.

Article 3 - Rémunération
La rémunération mensuelle brute est fixée à {parametres.get('salaire', '[MONTANT]')} euros.

Fait à [LIEU], le [DATE]
Signatures : [SIGNATURES]
"""
        elif type_document == "mise_en_demeure":
            return f"""
MISE EN DEMEURE

Expéditeur : {parametres.get('expediteur', '[NOM EXPÉDITEUR]')}
Destinataire : {parametres.get('destinataire', '[NOM DESTINATAIRE]')}

Objet : Mise en demeure de {parametres.get('objet', '[OBJET]')}

Monsieur/Madame,

Par la présente, nous vous mettons en demeure de respecter vos obligations 
concernant {parametres.get('objet', '[DESCRIPTION OBLIGATION]')}.

Vous disposez d'un délai de {parametres.get('delai', '15')} jours à compter 
de la réception de ce courrier pour régulariser votre situation.

À défaut, nous nous réservons le droit d'engager toute action en justice.

Fait à [LIEU], le [DATE]
Signature : [SIGNATURE]
"""
        else:
            return f"Document de type '{type_document}' généré avec les paramètres : {parametres}"
    
    def _build_generation_prompt(self, type_document: str, parametres: dict) -> str:
        """Construit le prompt pour la génération de document"""
        base_prompt = f"Génère un {type_document} juridique professionnel en français. "
        
        if type_document == "contrat":
            base_prompt += "Inclus tous les articles essentiels d'un contrat de travail français. "
        elif type_document == "mise_en_demeure":
            base_prompt += "Respecte le formalisme juridique français pour une mise en demeure. "
        
        base_prompt += f"Utilise les informations suivantes : {parametres}"
        return base_prompt
    
    def legal_search_with_rag(self, question: str) -> Tuple[str, List[SourceDocument]]:
        """Effectue une recherche juridique avec RAG"""
        try:
            # Rechercher les documents pertinents
            sources = self.search_documents(question, top_k=3)
            
            if not settings.is_gemini_configured:
                return self._generate_mock_legal_response(question, sources), sources
            
            # Construire le contexte à partir des sources
            context = "\n\n".join([f"Source: {src.nom_fichier}\n{src.contenu}" for src in sources])
            
            prompt = f"""
En tant qu'assistant juridique expert, réponds à la question suivante en utilisant 
les informations fournies dans le contexte. Réponds en français et de manière précise.

Contexte :
{context}

Question : {question}

Réponse :
"""
            
            response = self.generation_model.generate_content(prompt)
            return response.text, sources
        
        except Exception as e:
            print(f"Erreur lors de la recherche RAG: {e}")
            return self._generate_mock_legal_response(question, sources), sources
    
    def _generate_mock_legal_response(self, question: str, sources: List[SourceDocument]) -> str:
        """Génère une réponse juridique factice"""
        return f"""
Réponse à votre question : "{question}"

D'après les éléments juridiques disponibles, voici les points importants à retenir :

1. Le droit français prévoit des dispositions spécifiques concernant cette question.
2. Il convient de respecter les procédures légales en vigueur.
3. En cas de doute, il est recommandé de consulter un avocat spécialisé.

Cette réponse est basée sur {len(sources)} source(s) juridique(s) pertinente(s).

Note : Cette réponse est générée à des fins de démonstration uniquement et ne constitue pas un conseil juridique.
"""
    
    def chat_interaction(self, message: str, historique: List[ChatMessage]) -> Tuple[str, List[ChatMessage]]:
        """Gère l'interaction de chat"""
        try:
            if not settings.is_gemini_configured:
                response_text = self._generate_mock_chat_response(message)
                new_history = historique + [
                    ChatMessage(role="user", content=message),
                    ChatMessage(role="assistant", content=response_text)
                ]
                return response_text, new_history
            else:
                # Construire l'historique pour Gemini
                chat_history = []
                for msg in historique[-5:]:  # Limite l'historique
                    chat_history.append(f"{msg.role}: {msg.content}")
                
                history_context = "\n".join(chat_history) if chat_history else ""
                
                prompt = f"""
Tu es un assistant juridique virtuel expert en droit français. Réponds de manière 
professionnelle et précise aux questions juridiques. Si tu n'es pas sûr d'une réponse, 
indique-le clairement et recommande de consulter un avocat.

{history_context}

Utilisateur: {message}

Réponse :
"""
                
                response = self.generation_model.generate_content(prompt)
                new_history = historique + [
                    ChatMessage(role="user", content=message),
                    ChatMessage(role="assistant", content=response.text)
                ]
                return response.text, new_history
        
        except Exception as e:
            print(f"Erreur lors du chat: {e}")
            response_text = self._generate_mock_chat_response(message)
            new_history = historique + [
                ChatMessage(role="user", content=message),
                ChatMessage(role="assistant", content=response_text)
            ]
            return response_text, new_history
    
    def _generate_mock_chat_response(self, message: str) -> str:
        """Génère une réponse factice pour le chat"""
        responses = {
            "contrat": "Je peux vous aider avec les contrats de travail. Un contrat doit inclure la durée, la rémunération, et les conditions de travail selon le Code du travail français.",
            "responsabilité": "En droit français, la responsabilité peut être civile, pénale ou administrative. Chaque type a ses propres règles et sanctions.",
            "procédure": "Les procédures juridiques doivent respecter les délais légaux et les formes prescrites. Je recommande de consulter un avocat pour des cas précis."
        }
        
        # Recherche simple de mots-clés
        for keyword, response in responses.items():
            if keyword.lower() in message.lower():
                return response
        
        return f"Merci pour votre question : '{message}'. En tant qu'assistant juridique, je vous recommande de consulter un professionnel du droit pour des conseils personnalisés. Cette démonstration illustre les capacités d'un LLM juridique."

# Instance globale du service
llm_service = LLMService() 