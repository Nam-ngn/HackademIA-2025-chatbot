# Architecture FactsBox - Chatbot Médical

## Vue d'ensemble

Le chatbot a été adapté pour intégrer un système de FactsBox permettant de fournir des informations médicales structurées et compréhensibles.

## Flux de traitement

```
Question utilisateur
      ↓
[1. Analyseur d'Intention]
      ↓
[2. Récupération FactsBox]
      ↓
[3. Interpréteur FactsBox]
      ↓
[4. Prompt Builder + LLM]
      ↓
Réponse textuelle claire
```

## Composants créés

### 1. **Analyseur d'Intention** (`IntentAnalyzer`)
- **Fichier**: `src/impl/intent_analyzer.py`
- **Interface**: `src/interface/base_intent_analyzer.py`
- **Rôle**: Comprendre ce que l'utilisateur cherche réellement
- **Types d'intentions**:
  - `factsbox_query`: Questions médicales précises (risques, bénéfices, effets)
  - `general_info`: Informations générales sur une association
  - `comparison`: Comparaison entre options
  - `contact`: Recherche de coordonnées
  - `event`: Événements et activités
- **Sortie**: Objet `UserIntent` avec type, topic, contexte et confiance

### 2. **Interpréteur de FactsBox** (`FactsBoxInterpreter`)
- **Fichier**: `src/impl/factsbox_interpreter.py`
- **Interface**: `src/interface/base_factsbox_interpreter.py`
- **Rôle**: Récupérer et interpréter les données FactsBox
- **Fonctions**:
  - `retrieve_factsbox()`: Récupère la FactsBox appropriée
  - `interpret()`: Extrait et reformule les données importantes
    - Risques absolus
    - Risques relatifs
    - Bénéfices
    - Effets secondaires
    - Informations supplémentaires
- **Sortie**: Objet `FactsBoxData` structuré

### 3. **Générateur de Réponses Amélioré** (`ResponseGenerator`)
- **Fichier**: `src/impl/response_generator.py`
- **Rôle**: Prompt Builder + LLM
- **Nouveautés**:
  - Deux prompts système: général et FactsBox
  - Construction de prompts structurés avec contexte d'intention
  - Gestion spécifique des données médicales
  - Explications claires des risques absolus vs relatifs

### 4. **Pipeline RAG Adapté** (`RAGPipeline`)
- **Fichier**: `src/rag_pipeline.py`
- **Nouveautés**:
  - Intégration de `IntentAnalyzer` et `FactsBoxInterpreter`
  - Méthode `process_query()` mise à jour avec le flux complet
  - Formatage des FactsBox pour le contexte
  - Fallback vers RAG traditionnel si pas de FactsBox

## Utilisation

### Configuration initiale
```python
from src.impl import (
    Datastore, Indexer, ResponseGenerator, 
    IntentAnalyzer, FactsBoxInterpreter
)
from src.rag_pipeline import RAGPipeline

# Créer les composants
datastore = Datastore()
intent_analyzer = IntentAnalyzer()
factsbox_interpreter = FactsBoxInterpreter(datastore=datastore)
response_generator = ResponseGenerator()

# Créer le pipeline
pipeline = RAGPipeline(
    datastore=datastore,
    indexer=indexer,
    response_generator=response_generator,
    intent_analyzer=intent_analyzer,
    factsbox_interpreter=factsbox_interpreter
)
```

### Traiter une question
```python
# Le pipeline gère automatiquement tout le flux
response = pipeline.process_query("Quels sont les risques de ce traitement?")
```

Le flux complet se déroule automatiquement :
1. ✅ L'intention est analysée
2. ✅ La FactsBox correspondante est récupérée (si disponible)
3. ✅ Les données sont interprétées et structurées
4. ✅ Un prompt optimisé est construit
5. ✅ Une réponse claire et compréhensible est générée

## Points d'extension

### Ajouter des types d'intentions
Modifier `INTENT_ANALYSIS_PROMPT` dans `intent_analyzer.py`

### Personnaliser l'interprétation FactsBox
Étendre `FactsBoxInterpreter` avec des méthodes d'extraction spécifiques

### Ajouter des prompts spécialisés
Ajouter de nouveaux prompts dans `response_generator.py` selon l'intention

### Intégrer une vraie base FactsBox
Modifier `retrieve_factsbox()` pour se connecter à votre base de données médicale

## Structure des fichiers

```
src/
├── interface/
│   ├── base_intent_analyzer.py          # Interface analyseur d'intention
│   ├── base_factsbox_interpreter.py     # Interface interpréteur FactsBox
│   └── base_response_generator.py       # Interface mise à jour
├── impl/
│   ├── intent_analyzer.py               # Implémentation analyseur
│   ├── factsbox_interpreter.py          # Implémentation interpréteur
│   └── response_generator.py            # Générateur avec prompt builder
└── rag_pipeline.py                      # Pipeline orchestrateur
```

## Prochaines étapes

1. **Créer des FactsBox réelles**: Ajouter des données médicales structurées
2. **Enrichir les intentions**: Ajouter plus de types d'intentions médicales
3. **User Stories Generator**: Créer un module pour générer des scénarios visuels
4. **Tests**: Ajouter des tests pour chaque composant
5. **Évaluation**: Créer des benchmarks pour mesurer la qualité des réponses

## Compatibilité

- ✅ Rétrocompatible avec l'ancien système
- ✅ Fonctionne avec ou sans `intent_analyzer` et `factsbox_interpreter`
- ✅ Fallback automatique vers RAG traditionnel
