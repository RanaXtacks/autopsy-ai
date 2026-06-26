from typing import List

class ChronotypeAnalyzer:
    """Analyzes historical activity to determine biological prime time."""
    
    def analyze(self, sessions: List) -> str:
        if not sessions:
            return "Early Peak Profile" # Default fallback
            
        # Count deep work sessions by time of day
        morning = 0
        afternoon = 0
        night = 0
        
        for s in sessions:
            if s.session_type in ["Deep Work", "Coding", "Study"]:
                hour = s.start_time.hour
                if 5 <= hour < 12:
                    morning += 1
                elif 12 <= hour < 18:
                    afternoon += 1
                else:
                    night += 1
                    
        total = morning + afternoon + night
        if total == 0:
            return "Early Peak Profile"
            
        if morning > afternoon and morning > night:
            return "Early Peak Profile"
        elif night > morning and night > afternoon:
            return "Night Owl Profile"
        else:
            return "Standard Profile"
