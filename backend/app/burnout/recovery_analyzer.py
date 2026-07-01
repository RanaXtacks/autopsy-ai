from typing import List
from app.models.sessions import BehaviorSession

class RecoveryAnalyzer:
    """Evaluates the presence of recovery activities."""
    
    def analyze(self, sessions: List[BehaviorSession]) -> float:
        # Calculate ratio of recovery (Entertainment/Music) to total sessions.
        # Lack of recovery drives up the risk score.
        
        if not sessions:
            return 0.0
            
        recovery_sessions = sum(1 for s in sessions if s.session_type in ["Entertainment", "Music"])
        ratio = recovery_sessions / len(sessions)
        
        # If recovery ratio < 10%, risk is 100. 
        # If recovery ratio > 30%, risk is 0.
        if ratio > 0.30:
            return 0.0
            
        risk_score = 100.0 - (ratio / 0.30) * 100.0
        return min(100.0, max(0.0, risk_score))
