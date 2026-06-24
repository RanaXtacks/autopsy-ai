import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):
    """
    Abstract base class for all data source parsers.
    Parsers are responsible for reading the raw CSV file, cleaning it, 
    and returning a standardized list of dictionaries that the transformer will use.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        
    def load(self):
        """Loads the CSV file into a pandas DataFrame."""
        try:
            self.df = pd.read_csv(self.file_path)
        except Exception as e:
            raise ValueError(f"Failed to load file {self.file_path}: {str(e)}")
            
    @abstractmethod
    def clean(self):
        """Cleans the DataFrame (handles missing values, duplicates, bad types)."""
        pass
        
    @abstractmethod
    def parse(self) -> List[Dict[str, Any]]:
        """
        Parses the cleaned DataFrame and returns a list of dictionaries 
        representing the standardized raw events.
        """
        pass
        
    def process(self) -> List[Dict[str, Any]]:
        """Orchestrates load, clean, and parse."""
        self.load()
        self.clean()
        return self.parse()
