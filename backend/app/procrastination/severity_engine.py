class SeverityEngine:
    """Calculates the 0-100 severity score based on frequency and time lost."""
    
    def calculate(self, frequency: int, time_lost_mins: float) -> float:
        score = 0.0
        
        # Factor 1: Frequency (e.g., repeating a bad habit)
        score += min(40.0, frequency * 5.0)
        
        # Factor 2: Time lost (e.g., losing hours to YouTube)
        score += min(60.0, (time_lost_mins / 60.0) * 15.0) 
        
        return min(100.0, score)
