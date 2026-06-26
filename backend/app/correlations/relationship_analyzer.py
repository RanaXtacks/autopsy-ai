import math
from typing import List, Tuple

class RelationshipAnalyzer:
    """Calculates statistical correlation coefficients between features and outcomes."""
    
    def calculate_pearson(self, x: List[float], y: List[float]) -> float:
        """
        Calculates Pearson correlation coefficient natively.
        Assumes x and y have the same length.
        """
        n = len(x)
        if n < 2:
            return 0.0
            
        sum_x = sum(x)
        sum_y = sum(y)
        sum_x_sq = sum([xi**2 for xi in x])
        sum_y_sq = sum([yi**2 for yi in y])
        sum_xy = sum([xi * yi for xi, yi in zip(x, y)])
        
        numerator = (n * sum_xy) - (sum_x * sum_y)
        denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
        
        if denominator == 0:
            return 0.0
            
        return numerator / denominator

    def analyze_relationship(self, feature_values: List[float], outcome_values: List[float]) -> float:
        """Entry point for future ML integration. Currently proxies to Pearson."""
        if len(feature_values) != len(outcome_values) or len(feature_values) == 0:
            return 0.0
            
        # Filter out pairs where feature is 0 (optional, but good for things like 'music before study')
        # Here we just calculate over the whole vector
        return self.calculate_pearson(feature_values, outcome_values)
