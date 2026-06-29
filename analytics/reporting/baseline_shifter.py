from typing import Dict, Any

class BaselineShifter:
    """
    Detects if a user's 30-day baseline has fundamentally changed.
    Differentiates between short-term noise and permanent shifts in capacity.
    """
    
    def detect_shift(self, historical_baseline: float, current_baseline: float) -> Dict[str, Any]:
        delta = current_baseline - historical_baseline
        
        # Consider a shift significant if it moves by more than 5% of the scale consistently
        if abs(delta) > 5.0:
            direction = "higher" if delta > 0 else "lower"
            return {
                "has_shifted": True,
                "shift_value": delta,
                "message": f"Your baseline has fundamentally shifted {abs(delta):.1f} points {direction}."
            }
            
        return {
            "has_shifted": False,
            "shift_value": 0.0,
            "message": "Baseline remains stable. Recent variations are within normal noise levels."
        }
