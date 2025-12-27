# Chatbot Prévention Tabac - HackademIA 2025

> Un assistant conversationnel intelligent pour la prévention du tabagisme, basé sur RAG (Retrieval-Augmented Generation) avec support FactsBox pour une information claire et basée sur des preuves scientifiques.

![Demo](demo.gif)

##  Vue d'ensemble

Ce projet développé lors du HackademIA 2025 est un chatbot spécialisé dans la prévention et l'arrêt du tabac qui combine :
- **Recherche sémantique** dans une base de données d'études sur le tabagisme
- **Analyse d'intention** pour comprendre les besoins de l'utilisateur
- **FactsBox** : Présentation structurée des données sur les interventions anti-tabac (risques, bénéfices, efficacité)
- **Génération de réponses** contextuelles via l'IA (OpenAI GPT-4)
- **User Stories** pour illustrer les informations avec des cas concrets de fumeurs

## Fonctionnalités principales

### Système FactsBox
Présentation claire et structurée des données médicales :
- **Comparaison groupe contrôle vs intervention** dans un tableau visuel
- **Risques relatifs et absolus** avec calculs automatiques
- **Bénéfices et effets secondaires** sous forme de listes organisées
- **Informations contextuelles** (population étudiée, durée, source)

### Analyse d'intention intelligente
Le système analyse automatiquement :
- Le type de requête (information générale, FactsBox, médicale)
- Le sujet principal de la question
- Le niveau de confiance de l'analyse

### User Stories
Chaque réponse est accompagnée d'une histoire utilisateur concrète (2-3 phrases) pour faciliter la compréhension.

### Interface Web moderne
- Design responsive et épuré
- Affichage des FactsBox en tableaux visuels
- Section User Story distincte avec style dédié
- Support Markdown pour les réponses

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Interface Web                          │
│                    (HTML + JavaScript)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                           │
│                  (src/server.py)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                             │
│                (src/rag_pipeline.py)                        │
├─────────────────────────────────────────────────────────────┤
│  1. Intent Analyzer   → Analyse de l'intention utilisateur │
│  2. FactsBox Interp.  → Récupération données structurées   │
│  3. Response Gen.     → Génération réponse + User Story    │
│  4. Datastore         → Recherche vectorielle (LanceDB)    │
└─────────────────────────────────────────────────────────────┘
```

## Démarrage rapide

### Prérequis
- Python 3.13 (recommandé)
- Clé API OpenAI
- Git

### Installation

```bash
# Cloner le repository
git clone https://github.com/Nam-ngn/HackademIA-2025-chatbot.git
cd HackademIA-2025-chatbot

# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
# Créer un fichier .env avec :
OPENAI_API_KEY=votre_clé_api_ici

# Indexer les données FactsBox (IMPORTANT)
python main.py reset

#Pour un fichier du répertoire
python main.py add -p "sample_data/tabac/factsbox_tabac.csv"

#Pour tous les fichiers du répertoire
python main.py add -p "sample_data/tabac"
```

### Lancement

```bash
# Démarrer le serveur
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload

# Ouvrir l'interface web
# Naviguer vers http://localhost:8000 ou ouvrir web/index.html
```

Pour plus de détails sur l'installation, voir [install.md](install.md).

## Structure du projet

```
chatbot/
├── src/
│   ├── impl/              # Implémentations concrètes
│   │   ├── intent_analyzer.py      # Analyse d'intention
│   │   ├── factsbox_interpreter.py # Extraction FactsBox
│   │   ├── response_generator.py   # Génération réponses
│   │   └── datastore.py            # LanceDB vector store
│   ├── interface/         # Interfaces abstraites
│   ├── rag_pipeline.py    # Orchestration du pipeline
│   └── server.py          # API FastAPI
├── sample_data/
│   └── source/
│       ├── factsbox_tabac.csv     # Données FactsBox tabac
│       └── factsbox_medicales.csv # Données médicales
├── web/
│   └── index.html         # Interface utilisateur
├── main.py               # Point d'entrée CLI
└── requirements.txt      # Dépendances Python
```

## Utilisation

### Via l'interface Web
1. Ouvrir http://localhost:8000
2. Poser une question sur le tabac ou l'arrêt du tabagisme
3. Voir la réponse avec FactsBox (comparaison des interventions) et User Story

### Via CLI
```bash
python main.py
> Quels sont les effets des avertissements pictoriaux sur les paquets de cigarettes?
```

### Exemples de questions
- "Quels sont les effets des avertissements pictoriaux sur le tabac ?"
- "Quelle est l'efficacité des images choquantes sur les paquets de cigarettes ?"
- "Comment les avertissements graphiques aident-ils à arrêter de fumer ?"
- "Quels sont les bénéfices des images sur les paquets pour réduire le tabagisme ?"

## Technologies utilisées

- **Backend:** Python 3.13, FastAPI, LanceDB
- **AI/ML:** OpenAI GPT-4, text-embedding-3-small
- **Frontend:** HTML5, JavaScript (Vanilla), Marked.js
- **Document Processing:** Docling, RapidOCR
- **Data:** CSV, Vector embeddings

## Format FactsBox

Les FactsBox utilisent un format CSV standardisé avec colonnes :
- `Nom` : Titre de l'intervention
- `Risque_Absolu_Groupe_Controle` : Résultats groupe contrôle
- `Risque_Absolu_Groupe_Intervention` : Résultats groupe intervention
- `Risque_Relatif` : Différence relative
- `Benefices` : Liste des bénéfices (séparés par `;`)
- `Effets_Secondaires` : Liste des effets secondaires
- `Population_Etudiee` : Caractéristiques de l'échantillon
- `Duree_Etude` : Période de suivi
- `Source_Etude` : Référence de l'étude

## Contribution

Projet développé lors du HackademIA 2025.

## License

Ce projet est un prototype éducatif développé dans le cadre d'un hackathon.

## Contact

Pour plus d'informations sur le projet HackademIA 2025, consultez le repository.

---

**Avertissement**  
Ce chatbot est un outil éducatif de prévention du tabagisme et ne remplace pas un avis médical professionnel. Pour un accompagnement personnalisé dans l'arrêt du tabac, consultez un professionnel de santé ou un tabacologue.
