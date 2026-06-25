from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .session_rules import evaluate_rules

class BaseSessionClassifier(ABC):
    @abstractmethod
    def classify(self, events: List[Any], duration_minutes: float) -> str:
        """
        Classify a group of events into a session type.
        """
        pass

class RuleBasedClassifier(BaseSessionClassifier):
    def classify(self, events: List[Any], duration_minutes: float) -> str:
        """
        Uses predefined configurable rules to classify the session.
        """
        return evaluate_rules(events, duration_minutes)

# Factory or Dependency Injection mechanism for future ML replacement
def get_classifier() -> BaseSessionClassifier:
    return RuleBasedClassifier()
