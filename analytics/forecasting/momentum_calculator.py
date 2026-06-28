from typing import List

class MomentumCalculator:
    """Calculates short-term momentum based on the last 3 days of scores."""
    
    def calculate(self, historical_scores: List) -> float:
        if len(historical_scores) < 3:
            return 0.0
            
        # Get the most recent 3 scores (assuming sorted oldest to newest)
        recent = historical_scores[-3:]
        
        # Simple gradient calculation
        diff_1 = recent[1].score - recent[0].score
        diff_2 = recent[2].score - recent[1].score
        
        momentum = (diff_1 + diff_2) / 2.0
        
        # Dampen the momentum to avoid wild swings
        return momentum * 0.5
