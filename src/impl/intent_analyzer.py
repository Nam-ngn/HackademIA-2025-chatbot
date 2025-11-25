from typing import Optional
from ..interface.base_intent_analyzer import BaseIntentAnalyzer, UserIntent
from ..util.invoke_ai import invoke_ai


INTENT_ANALYSIS_PROMPT = """
Tu es un analyseur d'intention expert. Ta tâche est d'analyser la question de l'utilisateur pour comprendre ce qu'il cherche réellement.

Types d'intentions possibles :
- factsbox_query : L'utilisateur cherche des informations médicales précises (risques, bénéfices, effets secondaires)
- general_info : L'utilisateur cherche des informations générales sur une association ou un sujet
- comparison : L'utilisateur veut comparer plusieurs options
- contact : L'utilisateur cherche des coordonnées (email, adresse, etc.)
- event : L'utilisateur s'intéresse aux événements ou activités

Analyse la question et réponds UNIQUEMENT au format JSON suivant :
{
    "intent_type": "type_d_intention",
    "topic": "sujet_principal",
    "context": "contexte_additionnel",
    "confidence": 0.95
}
"""


class IntentAnalyzer(BaseIntentAnalyzer):
    """Analyzes user intent and context using AI."""
    
    def analyze(self, query: str) -> UserIntent:
        """
        Analyze user query to understand intent and context.
        
        Args:
            query: The user's question in free text
            
        Returns:
            UserIntent object containing the analyzed intention
        """
        user_message = f"Question de l'utilisateur : {query}"
        
        try:
            # Call AI to analyze intent
            response = invoke_ai(
                system_message=INTENT_ANALYSIS_PROMPT,
                user_message=user_message
            )
            
            # Parse AI response (expecting JSON)
            import json
            response_clean = response.strip()
            
            # Extract JSON from response if wrapped in code blocks
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0].strip()
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0].strip()
            
            parsed = json.loads(response_clean)
            
            return UserIntent(
                query=query,
                intent_type=parsed.get("intent_type", "general_info"),
                topic=parsed.get("topic"),
                context=parsed.get("context"),
                confidence=float(parsed.get("confidence", 0.7))
            )
            
        except Exception as e:
            # Fallback to default intent if parsing fails
            print(f"⚠️  Intent analysis failed: {e}. Using default intent.")
            return UserIntent(
                query=query,
                intent_type="general_info",
                topic=None,
                context=None,
                confidence=0.5
            )
