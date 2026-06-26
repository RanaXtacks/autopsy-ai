class InsightGenerator:
    """Generates natural language explanations of the patterns."""
    
    def generate(self, pattern_name: str, pattern_type: str, frequency: int, time_lost_mins: float) -> str:
        hours_lost = round(time_lost_mins / 60.0, 1)
        
        if pattern_type == "Distraction Loop":
            return f"You frequently engage in {pattern_name}, happening {frequency} times."
        elif pattern_type == "Focus Disruption":
            return f"{pattern_name} accounts for approximately {hours_lost} hours of lost focus."
        elif pattern_type == "Task Abandonment":
            return f"You abandoned tasks prematurely {frequency} times."
        elif pattern_type == "Circadian Disruption":
            return f"Late-night activity impacted your rest or productivity {frequency} times."
            
        return f"Detected {pattern_name} ({frequency} occurrences)."
