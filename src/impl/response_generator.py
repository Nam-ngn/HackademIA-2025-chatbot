from typing import List, Optional
from ..interface.base_response_generator import BaseResponseGenerator
from ..interface.base_intent_analyzer import UserIntent
from ..interface.base_factsbox_interpreter import FactsBoxData
from ..util.invoke_ai import invoke_ai


SYSTEM_PROMPT_GENERAL = """
Tu es un assistant qui répond aux questions sur les associations de l'Université de Genève.
Le contexte contient une ou plusieurs fiches d'associations avec des champs tels que Nom_fr, Description_fr, Adresse, Sites, Email et réseaux sociaux.

Règles :
1. Utilise uniquement les informations présentes dans le contexte. Si une donnée manque, indique-le.
2. Quand la question est précise (par exemple un email ou une adresse), réponds directement avec l'information demandée et le nom de l'association.
3. Quand la question est large ou demande un conseil, fournis un résumé clair : mission, activités clés, coordonnées utiles.
4. Si plusieurs associations correspondent, liste-les avec des puces courtes et pertinentes.
5. Réponds dans la langue de la question (FR/EN) et garde un ton factuel.
"""

SYSTEM_PROMPT_FACTSBOX = """
Tu es un assistant expert en santé qui explique des informations médicales de manière claire et compréhensible.
Le contexte contient une FactsBox avec des données structurées sur un traitement ou une condition médicale.

Règles :
1. Utilise les informations de la FactsBox pour fournir une réponse précise et équilibrée.
2. Explique clairement les risques absolus et relatifs si présents - aide l'utilisateur à comprendre la différence.
3. Présente les bénéfices et les effets secondaires de manière équilibrée et objective.
4. Utilise un langage accessible, évite le jargon médical quand possible.
5. Si des données manquent dans la FactsBox, indique-le clairement.
6. Structure ta réponse de manière logique : d'abord répondre directement à la question, puis donner le contexte nécessaire.
7. Réponds dans la langue de la question (FR/EN) et garde un ton factuel mais empathique.
"""


class ResponseGenerator(BaseResponseGenerator):
    def generate_response(
        self, 
        query: str, 
        context: List[str],
        user_intent: Optional[UserIntent] = None,
        factsbox_data: Optional[FactsBoxData] = None
    ) -> str:
        """
        Generate a response using OpenAI's chat completion with enhanced prompt building.
        
        This implements the Prompt Builder + LLM module from the architecture:
        - Selects appropriate system prompt based on intent
        - Structures the user message with query and context
        - Adds FactsBox-specific formatting when available
        """
        # Select system prompt based on intent
        if user_intent and user_intent.intent_type == "factsbox_query":
            system_prompt = SYSTEM_PROMPT_FACTSBOX
        else:
            system_prompt = SYSTEM_PROMPT_GENERAL
        
        # Build structured user message
        context_text = "\n\n---\n\n".join(context)
        
        # Enhanced message with intent information
        message_parts = []
        
        if user_intent and user_intent.context:
            message_parts.append(f"<intent_context>\n{user_intent.context}\n</intent_context>\n")
        
        message_parts.append(f"<context>\n{context_text}\n</context>\n")
        message_parts.append(f"<question>\n{query}\n</question>")
        
        user_message = "".join(message_parts)
        
        return invoke_ai(system_message=system_prompt, user_message=user_message)
