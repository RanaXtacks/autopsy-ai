from typing import List
import json
from app.models.sessions import BehaviorSession
from app.models.scores import ProductivityScore
from app.models.procrastination import ProcrastinationPattern
from app.models.burnout import BurnoutAssessment
from app.config.burnout_config import BurnoutConfig

from .workload_analyzer import WorkloadAnalyzer
from .recovery_analyzer import RecoveryAnalyzer
from .trend_detector import TrendDetector
from .risk_calculator import RiskCalculator
from .recommendation_generator import RecommendationGenerator

class BurnoutEngine:
    """Orchestrates the detection of burnout signals."""
    
    def __init__(self):
        self.workload_analyzer = WorkloadAnalyzer()
        self.recovery_analyzer = RecoveryAnalyzer()
        self.trend_detector = TrendDetector()
        self.risk_calculator = RiskCalculator()
        self.recommendation_generator = RecommendationGenerator()
        
    def analyze(self, user_id: int, sessions: List[BehaviorSession], 
                scores: List[ProductivityScore], procrastination: List[ProcrastinationPattern]) -> BurnoutAssessment:
        
        # 1. Analyze Sub-components
        workload_score = self.workload_analyzer.analyze(sessions)
        recovery_score = self.recovery_analyzer.analyze(sessions)
        focus_decline = self.trend_detector.detect_focus_decline(scores)
        volatility = self.trend_detector.detect_volatility(scores)
        
        # Proximate context switching from procrastination engine
        context_switch_time_lost = sum(p.estimated_time_lost for p in procrastination if p.pattern_type == "Focus Disruption")
        context_switch_score = min(100.0, (context_switch_time_lost / 120.0) * 100.0) # >2 hours lost = max risk
        
        # 2. Calculate Final Score
        final_score, level = self.risk_calculator.calculate(
            workload_score, recovery_score, focus_decline, context_switch_score, volatility
        )
        
        # 3. Generate Primary Risk Factors (Insights)
        factors = []
        if workload_score > 60:
            factors.append("Deep work volume is significantly higher than your baseline.")
        if recovery_score > 60:
            factors.append("Recovery-related activity is below your normal baseline.")
        if focus_decline > 50:
            factors.append("Focus score has steadily decreased over the analysis window.")
        if context_switch_score > 60:
            factors.append("Context switching frequency is rising, indicating cognitive fatigue.")
            
        # 4. Generate Recommendations
        actions = self.recommendation_generator.generate(factors)
        
        return BurnoutAssessment(
            user_id=user_id,
            risk_score=final_score,
            risk_level=level,
            primary_risk_factors=json.dumps(factors),
            recommended_actions=json.dumps(actions),
            confidence_score=85.0 # Placeholder for confidence heuristic
        )
