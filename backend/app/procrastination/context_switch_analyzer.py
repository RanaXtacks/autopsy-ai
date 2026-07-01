from typing import List, Dict, Any
from app.models.sessions import BehaviorSession

class ContextSwitchAnalyzer:
    """Detects context switching spikes and estimates time lost."""
    
    def detect(self, sessions: List[BehaviorSession]) -> List[Dict[str, Any]]:
        patterns = []
        
        for s in sessions:
            if s.session_type == "Context Switching" and s.event_count and s.event_count > 10:
                # We assume each rapid context switch causes ~5 minutes of lost cognitive focus (task resumption penalty)
                time_lost = s.event_count * 5.0
                patterns.append({
                    "pattern_name": "Context Switching Spike",
                    "pattern_type": "Focus Disruption",
                    "frequency": s.event_count,
                    "time_lost_mins": time_lost,
                    "description": f"User rapidly switched contexts {s.event_count} times, losing estimated focus time."
                })
                
        return patterns
