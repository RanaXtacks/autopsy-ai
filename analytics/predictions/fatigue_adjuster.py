from typing import List, Dict, Any

class FatigueAdjuster:
    """Adjusts or scales down the optimal window size based on Burnout Risk."""
    
    def adjust(self, windows: List[Dict[str, Any]], burnout_risk: float) -> List[Dict[str, Any]]:
        # If burnout risk is high, reduce deep work blocks
        adjusted = []
        for w in windows:
            start = w["start_time"]
            end = w["end_time"]
            
            duration = end - start
            
            # Reduce Deep Work windows by 30% if burnout risk > 70
            if burnout_risk > 70.0 and w["activity_type"] in ["Deep Work", "Coding"]:
                reduction = duration * 0.3
                end = end - reduction
                
            w["end_time"] = end
            adjusted.append(w)
            
        return adjusted
