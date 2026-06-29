from typing import Dict, Any

class ComparativeEngine:
    """
    Calculates variance, standard deviation changes, and percentage deltas 
    across adjacent weeks and months.
    """
    
    def calculate_deltas(self, current_period: Dict[str, Any], previous_period: Dict[str, Any]) -> Dict[str, Any]:
        if not previous_period or not current_period:
            return {"focus_delta": 0.0, "productivity_delta": 0.0, "deep_work_delta": 0.0}
            
        prev_focus = previous_period.get("average_focus_score", 1.0)
        curr_focus = current_period.get("average_focus_score", 0.0)
        
        prev_prod = previous_period.get("average_productivity_score", 1.0)
        curr_prod = current_period.get("average_productivity_score", 0.0)
        
        prev_dw = previous_period.get("total_deep_work_minutes", 1.0)
        curr_dw = current_period.get("total_deep_work_minutes", 0.0)
        
        # Avoid zero division
        prev_focus = max(1.0, prev_focus)
        prev_prod = max(1.0, prev_prod)
        prev_dw = max(1.0, prev_dw)
        
        return {
            "focus_delta": ((curr_focus - prev_focus) / prev_focus) * 100,
            "productivity_delta": ((curr_prod - prev_prod) / prev_prod) * 100,
            "deep_work_delta": ((curr_dw - prev_dw) / prev_dw) * 100
        }
