from typing import List

class AnomalyAdjuster:
    """Adjusts raw forecasts to account for anomalies or burnout constraints."""
    
    def adjust(self, raw_forecast: float, active_habits: List) -> float:
        # Example heuristic: If user has a high burnout constraint active
        for habit in active_habits:
            if getattr(habit, 'is_burnout_constraint', False):
                # Apply a severe penalty to expected productivity
                return raw_forecast * 0.7 
                
        return raw_forecast
