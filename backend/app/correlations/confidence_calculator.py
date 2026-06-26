import math

class ConfidenceCalculator:
    """Evaluates the statistical significance of a correlation based on sample size and strength."""
    
    def calculate(self, correlation_strength: float, sample_size: int) -> float:
        """
        Returns a confidence score from 0.0 to 100.0.
        Uses a heuristic approximating statistical power.
        """
        if sample_size < 3:
            return 15.0 # Very low confidence for < 3 samples
            
        # T-statistic approximation
        r = abs(correlation_strength)
        
        # Avoid division by zero if r is perfectly 1.0 (unlikely but possible)
        if r >= 0.999:
            r = 0.999
            
        t_stat = r * math.sqrt((sample_size - 2) / (1 - r**2))
        
        # Map t-statistic to a 0-100 score. 
        # A t-stat > 2.5 is generally quite significant.
        confidence = min(100.0, (t_stat / 3.0) * 100.0)
        
        # Penalize small sample sizes heavily
        if sample_size < 5:
            confidence *= 0.5
        elif sample_size < 10:
            confidence *= 0.8
            
        return max(0.0, min(100.0, confidence))

    def determine_type(self, correlation_strength: float, sample_size: int) -> str:
        r = correlation_strength
        if sample_size < 5:
            return "Emerging Trend"
            
        if r >= 0.5:
            return "Strong Positive"
        elif r > 0.2:
            return "Positive"
        elif r <= -0.5:
            return "Strong Negative"
        elif r < -0.2:
            return "Negative"
        else:
            return "Weak"
