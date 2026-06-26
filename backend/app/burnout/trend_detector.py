from typing import List
from app.models.scores import ProductivityScore

class TrendDetector:
    """Identifies focus score decline over time and productivity volatility."""
    
    def detect_focus_decline(self, scores: List[ProductivityScore]) -> float:
        if len(scores) < 7:
            return 0.0
            
        # Compare first half vs second half of the window
        mid = len(scores) // 2
        first_half = scores[:mid]
        second_half = scores[mid:]
        
        avg_first = sum(s.focus_score for s in first_half) / len(first_half) if first_half else 0
        avg_second = sum(s.focus_score for s in second_half) / len(second_half) if second_half else 0
        
        # If second half is significantly lower than first, risk increases
        decline = avg_first - avg_second
        if decline <= 0:
            return 0.0
            
        # A 20 point decline maxes out risk
        return min(100.0, (decline / 20.0) * 100.0)

    def detect_volatility(self, scores: List[ProductivityScore]) -> float:
        if len(scores) < 2:
            return 0.0
            
        # Calculate standard deviation proxy (average absolute deviation)
        avg = sum(s.productivity_score for s in scores) / len(scores)
        variance_sum = sum(abs(s.productivity_score - avg) for s in scores)
        avg_deviation = variance_sum / len(scores)
        
        # An average daily swing of 25 points is considered max volatility risk
        return min(100.0, (avg_deviation / 25.0) * 100.0)
