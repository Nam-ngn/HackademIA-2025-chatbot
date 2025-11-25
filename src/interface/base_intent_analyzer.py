from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserIntent:
    """Represents the analyzed user intention and context."""
    
    query: str  # Original user query
    intent_type: str  # Type of intent: 'factsbox_query', 'general_info', 'comparison', etc.
    topic: Optional[str] = None  # Main topic identified (e.g., 'medication', 'treatment', etc.)
    context: Optional[str] = None  # Additional context extracted
    confidence: float = 0.0  # Confidence score (0-1)
    

class BaseIntentAnalyzer(ABC):
    """Abstract base class for intent analysis."""
    
    @abstractmethod
    def analyze(self, query: str) -> UserIntent:
        """
        Analyze user query to understand intent and context.
        
        Args:
            query: The user's question in free text
            
        Returns:
            UserIntent object containing the analyzed intention
        """
        pass
