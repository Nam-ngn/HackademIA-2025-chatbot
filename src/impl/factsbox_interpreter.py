from typing import Dict, List, Optional, Any
from ..interface.base_factsbox_interpreter import BaseFactsBoxInterpreter, FactsBoxData
from ..interface.base_datastore import DataItem


class FactsBoxInterpreter(BaseFactsBoxInterpreter):
    """Interprets FactsBox data by extracting and reformulating key information."""
    
    def __init__(self, datastore=None):
        """
        Initialize the interpreter.
        
        Args:
            datastore: Optional datastore to retrieve FactsBox data from
        """
        self.datastore = datastore
    
    def retrieve_factsbox(self, intent_type: str, topic: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve the appropriate FactsBox based on user intent.
        
        For now, this retrieves data from the datastore based on topic.
        In a real implementation, this would access a FactsBox database.
        
        Args:
            intent_type: Type of intent identified
            topic: Optional topic to narrow down the search
            
        Returns:
            Raw FactsBox data as dictionary, or None if not found
        """
        if not self.datastore or not topic:
            return None
        
        try:
            # Search datastore for relevant factsbox
            search_results = self.datastore.search(topic, limit=1)
            
            if not search_results:
                return None
            
            # Convert first result to FactsBox format
            result = search_results[0]
            return self._dataitem_to_factsbox(result)
            
        except Exception as e:
            print(f"⚠️  Failed to retrieve FactsBox: {e}")
            return None
    
    def interpret(self, factsbox_raw: Dict[str, Any]) -> FactsBoxData:
        """
        Extract and reformulate important data from a FactsBox.
        
        Args:
            factsbox_raw: Raw FactsBox data
            
        Returns:
            FactsBoxData object with structured, interpreted information
        """
        # Extract standard fields
        title = factsbox_raw.get("title", factsbox_raw.get("Nom", "Information"))
        source = factsbox_raw.get("source", factsbox_raw.get("Source_Etude", "unknown"))
        
        # Extract absolute risks (control vs intervention groups)
        absolute_risks = []
        if "Risque_Absolu_Groupe_Controle" in factsbox_raw:
            absolute_risks.append({
                "group": "Groupe Contrôle",
                "value": factsbox_raw["Risque_Absolu_Groupe_Controle"]
            })
        if "Risque_Absolu_Groupe_Intervention" in factsbox_raw:
            absolute_risks.append({
                "group": "Groupe Intervention",
                "value": factsbox_raw["Risque_Absolu_Groupe_Intervention"]
            })
        
        # Extract relative risks
        relative_risks = []
        if "Risque_Relatif" in factsbox_raw and factsbox_raw["Risque_Relatif"]:
            rr_value = factsbox_raw["Risque_Relatif"]
            if isinstance(rr_value, str):
                relative_risks = [rr_value]
            elif isinstance(rr_value, list):
                relative_risks = rr_value
        
        # Extract benefits
        benefits = self._extract_list_field(factsbox_raw, "Benefices", "benefits", "bénéfices", "avantages")
        
        # Extract side effects
        side_effects = self._extract_list_field(factsbox_raw, "Effets_Secondaires", "side_effects", "effets_secondaires", "effets indésirables")
        
        # Extract additional information
        additional_info = []
        for key in ["Population_Etudiee", "Duree_Etude", "Description", "Type_Traitement"]:
            if key in factsbox_raw and factsbox_raw[key]:
                additional_info.append(f"{key.replace('_', ' ')}: {factsbox_raw[key]}")
        
        return FactsBoxData(
            title=title,
            source=source,
            absolute_risks=absolute_risks if absolute_risks else None,
            relative_risks=relative_risks if relative_risks else None,
            benefits=benefits,
            side_effects=side_effects,
            additional_info=additional_info if additional_info else None,
            raw_data=factsbox_raw
        )
    
    def _dataitem_to_factsbox(self, item: DataItem) -> Dict[str, Any]:
        """Convert a DataItem to FactsBox format."""
        factsbox = {
            "title": item.metadata.get("Nom_fr", "Information") if item.metadata else "Information",
            "source": item.source,
            "content": item.content
        }
        
        # Add all metadata fields
        if item.metadata:
            factsbox.update(item.metadata)
        
        return factsbox
    
    def _extract_risks(self, data: Dict[str, Any], risk_type: str) -> Optional[Dict[str, Any]]:
        """Extract risk data from FactsBox."""
        key_variations = [
            f"{risk_type}_risks",
            f"{risk_type}_risk",
            f"risque_{risk_type}",
            f"risques_{risk_type}s"
        ]
        
        for key in key_variations:
            if key in data and data[key]:
                return data[key] if isinstance(data[key], dict) else {"value": data[key]}
        
        return None
    
    def _extract_list_field(self, data: Dict[str, Any], *possible_keys: str) -> Optional[List[str]]:
        """Extract list field from various possible key names."""
        for key in possible_keys:
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    return value
                elif isinstance(value, str):
                    # Try to split by common separators
                    if ";" in value:
                        return [item.strip() for item in value.split(";") if item.strip()]
                    elif "\n" in value:
                        return [item.strip() for item in value.split("\n") if item.strip()]
                    else:
                        return [value]
        
        return None
