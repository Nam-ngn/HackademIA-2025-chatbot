from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class FactsBoxData:
    """Represents interpreted data from a FactsBox."""
    
    title: str  # Title of the FactsBox
    source: str  # Source identifier
    absolute_risks: Optional[List[Dict[str, Any]]] = None  # List of absolute risk values by group
    relative_risks: Optional[List[str]] = None  # List of relative risk descriptions
    benefits: Optional[List[str]] = None  # List of benefits
    side_effects: Optional[List[str]] = None  # List of side effects
    additional_info: Optional[List[str]] = None  # List of additional information strings
    raw_data: Optional[Dict[str, Any]] = None  # Original data for reference
    

class BaseFactsBoxInterpreter(ABC):
    """Abstract base class for FactsBox interpretation."""
    
    @abstractmethod
    def retrieve_factsbox(self, intent_type: str, topic: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve the appropriate FactsBox based on user intent.
        
        Args:
            intent_type: Type of intent identified
            topic: Optional topic to narrow down the search
            
        Returns:
            Raw FactsBox data as dictionary, or None if not found
        """
        pass
    
    @abstractmethod
    def interpret(self, factsbox_raw: Dict[str, Any]) -> FactsBoxData:
        """
        Extract and reformulate important data from a FactsBox.
        
        Args:
            factsbox_raw: Raw FactsBox data
            
        Returns:
            FactsBoxData object with structured, interpreted information
        """
        pass
    
    def retrieve_and_interpret(self, intent_type: str, topic: Optional[str] = None) -> Optional[FactsBoxData]:
        """
        Convenience method to retrieve and interpret in one call.
        
        Args:
            intent_type: Type of intent identified
            topic: Optional topic to narrow down the search
            
        Returns:
            Interpreted FactsBoxData, or None if no FactsBox found
        """
        factsbox_raw = self.retrieve_factsbox(intent_type, topic)
        if factsbox_raw is None:
            return None
        return self.interpret(factsbox_raw)
