from typing import List, Dict, Any
from datetime import datetime, timedelta

from .chronotype_analyzer import ChronotypeAnalyzer
from .window_estimator import WindowEstimator
from .fatigue_adjuster import FatigueAdjuster
from .confidence_scorer import ConfidenceScorer

class FocusPredictor:
    """
    Orchestrates the predictive modeling layer.
    Aggregates inputs from chronotype, day-of-week trends, and fatigue 
    to forecast optimal focus windows and energy dips.
    """
    
    def __init__(self):
        self.chronotype_analyzer = ChronotypeAnalyzer()
        self.window_estimator = WindowEstimator()
        self.fatigue_adjuster = FatigueAdjuster()
        self.confidence_scorer = ConfidenceScorer()

    def predict_tomorrow(self, user_id: int, sessions: List, burnout_risk: float) -> List[Dict[str, Any]]:
        target_date = (datetime.utcnow() + timedelta(days=1)).date()
        
        # 1. Determine Chronotype
        chronotype = self.chronotype_analyzer.analyze(sessions)
        
        # 2. Estimate Optimal Windows
        base_windows = self.window_estimator.estimate(target_date, chronotype, sessions)
        
        # 3. Adjust for Fatigue/Burnout
        adjusted_windows = self.fatigue_adjuster.adjust(base_windows, burnout_risk)
        
        # 4. Score Confidence
        predictions = []
        for window in adjusted_windows:
            confidence = self.confidence_scorer.score(window, sessions)
            
            predictions.append({
                "optimal_start_time": window["start_time"],
                "optimal_end_time": window["end_time"],
                "activity_type": window["activity_type"],
                "confidence_score": confidence,
                "contributing_factors": [chronotype, f"Burnout Risk: {burnout_risk:.1f}/100"]
            })
            
        return predictions
