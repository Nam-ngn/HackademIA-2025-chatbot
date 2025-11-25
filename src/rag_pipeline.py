from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict, List, Optional
from .interface import (
    BaseDatastore,
    BaseIndexer,
    BaseResponseGenerator,
    BaseEvaluator,
    EvaluationResult,
    DataItem,
    BaseIntentAnalyzer,
    BaseFactsBoxInterpreter,
    FactsBoxData,
)


@dataclass
class RAGPipeline:
    """Main RAG pipeline that orchestrates all components with FactsBox support."""

    datastore: BaseDatastore
    indexer: BaseIndexer
    response_generator: BaseResponseGenerator
    intent_analyzer: Optional[BaseIntentAnalyzer] = None
    factsbox_interpreter: Optional[BaseFactsBoxInterpreter] = None
    evaluator: Optional[BaseEvaluator] = None

    def reset(self) -> None:
        """Reset the datastore."""
        self.datastore.reset()

    def add_documents(self, documents: List[str]) -> None:
        """Index a list of documents."""
        items = self.indexer.index(documents)
        self.datastore.add_items(items)
        print(f"✅ Added {len(items)} items to the datastore.")

    def process_query(self, query: str) -> str:
        """
        Process user query with intent analysis and FactsBox interpretation.
        
        Flow:
        1. Analyze user intention and context
        2. Retrieve appropriate FactsBox based on intent
        3. Interpret FactsBox data (extract risks, benefits, side effects)
        4. Build structured prompt with query + interpreted data
        5. Generate clear, understandable response
        """
        # Step 1: Analyze user intention
        if self.intent_analyzer:
            print("🧠 Analyzing user intention...")
            user_intent = self.intent_analyzer.analyze(query)
            print(f"   Intent: {user_intent.intent_type} (confidence: {user_intent.confidence:.2f})")
            if user_intent.topic:
                print(f"   Topic: {user_intent.topic}")
        else:
            user_intent = None
        
        # Step 2 & 3: Retrieve and interpret FactsBox
        factsbox_data: Optional[FactsBoxData] = None
        if self.factsbox_interpreter and user_intent:
            print("📦 Retrieving and interpreting FactsBox...")
            factsbox_data = self.factsbox_interpreter.retrieve_and_interpret(
                intent_type=user_intent.intent_type,
                topic=user_intent.topic
            )
            if factsbox_data:
                print(f"   ✅ FactsBox retrieved: {factsbox_data.title}")
        
        # Fallback to traditional RAG search if no FactsBox or no intent analyzer
        if not factsbox_data:
            print("🔍 Using traditional RAG search...")
            search_results = self.datastore.search(query)
            print(f"   Found {len(search_results)} results\n")
            
            for i, result in enumerate(search_results, start=1):
                print(f"🔍 Result {i}:\n{self._summarize_result(result)}\n")
            
            context_blocks = [result.content for result in search_results]
        else:
            # Use FactsBox data as context
            context_blocks = [self._format_factsbox(factsbox_data)]
            print("   Using FactsBox as context\n")
        
        # Step 4 & 5: Generate response
        response = self.response_generator.generate_response(
            query, 
            context_blocks,
            user_intent=user_intent,
            factsbox_data=factsbox_data
        )
        return response

    def evaluate(
        self, sample_questions: List[Dict[str, str]]
    ) -> List[EvaluationResult]:
        # Evaluate a list of question/answer pairs.
        questions = [item["question"] for item in sample_questions]
        expected_answers = [item["answer"] for item in sample_questions]

        with ThreadPoolExecutor(max_workers=10) as executor:
            results: List[EvaluationResult] = list(
                executor.map(
                    self._evaluate_single_question,
                    questions,
                    expected_answers,
                )
            )

        for i, result in enumerate(results):
            result_emoji = "✅" if result.is_correct else "❌"
            print(f"{result_emoji} Q {i+1}: {result.question}: \n")
            print(f"Response: {result.response}\n")
            print(f"Expected Answer: {result.expected_answer}\n")
            print(f"Reasoning: {result.reasoning}\n")
            print("--------------------------------")

        number_correct = sum(result.is_correct for result in results)
        print(f"✨ Total Score: {number_correct}/{len(results)}")
        return results

    def _evaluate_single_question(
        self, question: str, expected_answer: str
    ) -> EvaluationResult:
        # Evaluate a single question/answer pair.
        response = self.process_query(question)
        return self.evaluator.evaluate(question, response, expected_answer)

    def _summarize_result(self, item: DataItem) -> str:
        metadata = item.metadata or {}
        name = metadata.get("Nom_fr") or metadata.get("Nom") or item.source
        summary_parts: List[str] = [name]

        description = metadata.get("Description_fr")
        if isinstance(description, list):
            description_text = " ".join(description)
        elif isinstance(description, str):
            description_text = " ".join(description.split())
        else:
            description_text = None

        if description_text:
            description_clean = description_text
            if len(description_clean) > 180:
                description_clean = description_clean[:177].rstrip() + "..."
            summary_parts.append(f"Description: {description_clean}")

        email = metadata.get("Email")
        if isinstance(email, list):
            email_text = ", ".join(email)
        else:
            email_text = email
        if email_text:
            summary_parts.append(f"Email: {email_text}")

        sites = metadata.get("Sites")
        if isinstance(sites, list):
            sites_text = ", ".join(sites[:3])
            summary_parts.append(f"Sites: {sites_text}")
        elif isinstance(sites, str):
            summary_parts.append(f"Sites: {sites}")

        return "\n".join(summary_parts)
    
    def _format_factsbox(self, factsbox: FactsBoxData) -> str:
        """Format FactsBox data into a readable context block."""
        lines = [f"# {factsbox.title}", f"Source: {factsbox.source}", ""]
        
        if factsbox.absolute_risks:
            lines.append("## Risques Absolus")
            lines.append(str(factsbox.absolute_risks))
            lines.append("")
        
        if factsbox.relative_risks:
            lines.append("## Risques Relatifs")
            lines.append(str(factsbox.relative_risks))
            lines.append("")
        
        if factsbox.benefits:
            lines.append("## Bénéfices")
            for benefit in factsbox.benefits:
                lines.append(f"- {benefit}")
            lines.append("")
        
        if factsbox.side_effects:
            lines.append("## Effets Secondaires")
            for effect in factsbox.side_effects:
                lines.append(f"- {effect}")
            lines.append("")
        
        if factsbox.additional_info:
            lines.append("## Informations Supplémentaires")
            for key, value in factsbox.additional_info.items():
                lines.append(f"{key}: {value}")
        
        return "\n".join(lines)
