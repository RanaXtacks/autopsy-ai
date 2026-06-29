from typing import Dict, Any

class GoalTrackingEngine:
    """
    Tracks dynamic goals and calculates required run-rates vs actual run-rates.
    """
    
    def calculate_run_rate(self, current_progress: float, target: float, days_passed: int, total_days: int) -> Dict[str, Any]:
        if days_passed == 0 or total_days == 0:
            return {"status": "Unknown", "projected": 0.0, "required_daily": 0.0}
            
        current_daily_rate = current_progress / days_passed
        projected_total = current_daily_rate * total_days
        
        days_remaining = total_days - days_passed
        remaining_target = max(0, target - current_progress)
        required_daily_rate = remaining_target / days_remaining if days_remaining > 0 else 0
        
        status = "On Track"
        if projected_total < target * 0.9:
            status = "At Risk"
        if projected_total < target * 0.7:
            status = "Failing"
            
        return {
            "status": status,
            "projected": projected_total,
            "required_daily_rate": required_daily_rate,
            "current_daily_rate": current_daily_rate,
            "deficit": max(0, target - projected_total)
        }
