from typing import List, Dict, Any

class AggregationHelpers:
    """
    Shared utilities for statistical aggregation across periods.
    """
    
    @staticmethod
    def calculate_average(values: List[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
        
    @staticmethod
    def find_top_occurrence(items: List[str]) -> str:
        if not items:
            return ""
        counts = {}
        for item in items:
            if item:
                counts[item] = counts.get(item, 0) + 1
        return max(counts, key=counts.get) if counts else ""
