# Chatbot FactsBox - HackademIA 2025

> Un assistant conversationnel intelligent multi-thématiques, basé sur RAG (Retrieval-Augmented Generation) avec support FactsBox pour une information claire et basée sur des preuves scientifiques.

![Demo](demo.gif)

##  Vue d'ensemble

Ce projet développé lors du HackademIA 2025 est un chatbot spécialisé qui combine :
- **Recherche sémantique** dans une base de données d'études scientifiques
- **Analyse d'intention** pour comprendre les besoins de l'utilisateur
- **FactsBox** : Présentation structurée des données (risques, bénéfices, comparaisons)
- **Génération de réponses** contextuelles via l'IA (OpenAI GPT-4)
- **User Stories** pour illustrer les informations avec des cas concrets

### Thématiques disponibles

| Thématique | Description |
|------------|-------------|
| 🚬 **Tabac** | Prévention du tabagisme, avertissements pictoriaux, études sur l'arrêt du tabac |
| 🎓 **UNIGE Santé** | Enquête santé étudiants 2019, comportements à risque, consommation d'alcool |

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

### Thématiques disponibles

Le chatbot supporte plusieurs thématiques avec des données FactsBox spécifiques :

| Thématique | Dossier de données | Interface Web | Description |
|------------|-------------------|---------------|-------------|
| **Tabac** | `sample_data/tabac/` | `web/tabac.html` | Prévention du tabagisme, avertissements pictoriaux |
| **UNIGE Santé** | `sample_data/unige/` | `web/unige.html` | Enquête santé étudiants, comportements à risque |

Pour changer de thématique, indexez les données correspondantes (voir Installation).

### Installation

```bash
# Cloner le repository
git clone https://github.com/Nam-ngn/HackademIA-2025-chatbot.git
cd HackademIA-2025-chatbot

# Créer l'environnement virtuel
py -3.13 -m venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
# Créer un fichier .env avec :
OPENAI_API_KEY=votre_clé_api_ici

# Indexer les données FactsBox (IMPORTANT)
python main.py reset

#si cela ne marche pas
pip install -r requirements.txt --force-reinstall

# === CHOISIR UNE THÉMATIQUE ===

# Option 1 : Thématique TABAC (prévention tabagisme)
python main.py add -p "sample_data/tabac"

# Option 2 : Thématique UNIGE (enquête santé étudiants)
python main.py add -p "sample_data/unige"

```

### Lancement

```bash
# Démarrer le serveur
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload

# Ouvrir l'interface web selon la thématique :
# - Tabac : http://localhost:8000/web/tabac.html
# - UNIGE : http://localhost:8000/web/unige.html
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
│   ├── tabac/             # 🚬 Thématique Tabac
│   │   └── factsbox_tabac.csv
│   ├── unige/             # 🎓 Thématique UNIGE Santé
│   │   ├── factsbox_enquete.csv
│   │   └── Etu2019-enquete-sante-risque.pdf
│   └── eval/              # Données d'évaluation
├── web/
│   ├── tabac.html         # Interface thématique Tabac
│   └── unige.html         # Interface thématique UNIGE
├── main.py               # Point d'entrée CLI
└── requirements.txt      # Dépendances Python
```

## Utilisation

### Via l'interface Web
1. Démarrer le serveur : `uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload`
2. Ouvrir l'interface selon la thématique :
   - 🚬 Tabac : http://localhost:8000/web/tabac.html
   - 🎓 UNIGE : http://localhost:8000/web/unige.html
3. Poser une question et voir la réponse avec FactsBox et User Story

### Via CLI
```bash
python main.py
> Votre question ici
```

### Exemples de questions

**🚬 Thématique Tabac :**
- "Quels sont les effets des avertissements pictoriaux sur le tabac ?"
- "Quelle est l'efficacité des images choquantes sur les paquets de cigarettes ?"
- "Comment les avertissements graphiques aident-ils à arrêter de fumer ?"
- "Quels sont les bénéfices des images sur les paquets de cigarettes pour réduire le tabagisme ?"
**🎓 Thématique UNIGE Santé :**
- "Quel est le taux de blessures lors de sports extrêmes chez les étudiants ?"
- "Compare la consommation d'alcool entre les étudiants prudents et à risque"
- "Quels sont les comportements à risque des étudiants de l'UNIGE ?"

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

## Tests et évaluation

Le dossier `tests/` contient un pipeline de test développé en **Python** et **R** pour évaluer la qualité des réponses du chatbot EduRisk. Il permet de :
- Valider les réponses générées par le système
- Analyser la cohérence des données FactsBox
- Évaluer la pertinence des informations retournées

👉 **[Voir la documentation complète des tests](tests/README.md)**

## License

Ce projet est un prototype éducatif développé dans le cadre d'un hackathon.

## Contact

Pour plus d'informations sur le projet HackademIA 2025, consultez le repository.

---

**Avertissement**  
Ce chatbot est un outil éducatif basé sur des données scientifiques et ne remplace pas un avis médical professionnel. Pour un accompagnement personnalisé, consultez un professionnel de santé.
