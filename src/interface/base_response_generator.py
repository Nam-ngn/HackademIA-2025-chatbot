from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .base_intent_analyzer import UserIntent
    from .base_factsbox_interpreter import FactsBoxData


class BaseResponseGenerator(ABC):

    @abstractmethod
    def generate_response(
        self, 
        query: str, 
        context: List[str],
        user_intent: Optional['UserIntent'] = None,
        factsbox_data: Optional['FactsBoxData'] = None
    ) -> str:
        pass
