from typing import List
from app.models.sessions import BehaviorSession

class WorkloadAnalyzer:
    """Analyzes deep work volume vs baseline to detect overload."""
    
    def analyze(self, sessions: List[BehaviorSession]) -> float:
        # Simplistic heuristic for now: 
        # Calculate total deep work and coding minutes.
        # Over 4 hours a day on average over the window is considered high risk (score up to 100).
        
        deep_work_mins = sum(s.duration_minutes or 0 for s in sessions if s.session_type in ["Deep Work", "Coding"])
        
        # Assuming a 14 day window
        daily_average_mins = deep_work_mins / 14.0
        
        # If daily average > 240 mins, score caps at 100
        risk_score = min(100.0, (daily_average_mins / 240.0) * 100.0)
        return risk_score
