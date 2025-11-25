from abc import ABC, abstractmethod
from typing import List
from dotenv import load_dotenv
from .base_datastore import DataItem

load_dotenv()

class BaseIndexer(ABC):

    @abstractmethod
    def index(self, document_paths: List[str]) -> List[DataItem]:
        pass
