from typing import List, Dict, Any
from app.models.sessions import BehaviorSession

class DistractionAnalyzer:
    """Detects distraction loops like 'Entertainment before work'."""
    
    def detect(self, sessions: List[BehaviorSession]) -> List[Dict[str, Any]]:
        patterns = []
        
        # Look for sequences where a work session (Study, Coding) is immediately preceded by a long entertainment session
        for i in range(len(sessions) - 1):
            s1 = sessions[i]
            s2 = sessions[i+1]
            
            if s1.session_type in ["Entertainment", "Music", "Social Media"] and s2.session_type in ["Study", "Coding"]:
                # Check if s1 was long
                if s1.duration_minutes and s1.duration_minutes > 30:
                    patterns.append({
                        "pattern_name": f"{s1.session_type} Before Work",
                        "pattern_type": "Distraction Loop",
                        "frequency": 1,
                        "time_lost_mins": s1.duration_minutes,
                        "description": f"User spent {s1.duration_minutes} minutes on {s1.session_type} before starting {s2.session_type}."
                    })
        return patterns
