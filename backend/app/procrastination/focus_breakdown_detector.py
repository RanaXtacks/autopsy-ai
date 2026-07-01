from typing import List, Dict, Any
from app.models.sessions import BehaviorSession

class FocusBreakdownDetector:
    """Identifies short focus sessions, task abandonment, and late-night crashes."""
    
    def detect(self, sessions: List[BehaviorSession]) -> List[Dict[str, Any]]:
        patterns = []
        
        for s in sessions:
            # Short focus session
            if s.session_type in ["Coding", "Study"] and s.duration_minutes and s.duration_minutes < 15:
                patterns.append({
                    "pattern_name": "Short Focus Session",
                    "pattern_type": "Task Abandonment",
                    "frequency": 1,
                    "time_lost_mins": 0.0, # Not strictly time lost, but productivity lost
                    "description": f"User abandoned a {s.session_type} session after only {s.duration_minutes} minutes."
                })
                
            # Late night crash
            if s.session_type in ["Entertainment", "Social Media"] and s.start_time:
                hour = s.start_time.hour
                if hour >= 23 or hour < 4:
                    patterns.append({
                        "pattern_name": "Late Night Crash",
                        "pattern_type": "Circadian Disruption",
                        "frequency": 1,
                        "time_lost_mins": s.duration_minutes or 0.0,
                        "description": f"User engaged in {s.session_type} during late-night hours."
                    })
                    
        return patterns
