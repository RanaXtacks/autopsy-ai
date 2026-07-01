from typing import List
from app.models.sessions import BehaviorSession
from app.models.procrastination import ProcrastinationPattern
from .distraction_analyzer import DistractionAnalyzer
from .context_switch_analyzer import ContextSwitchAnalyzer
from .focus_breakdown_detector import FocusBreakdownDetector
from .time_loss_estimator import TimeLossEstimator
from .severity_engine import SeverityEngine
from .recovery_advisor import RecoveryAdvisor
from .insight_generator import InsightGenerator

class ProcrastinationDetector:
    """Orchestrates the detection of procrastination and distraction loops."""
    
    def __init__(self):
        self.distraction_analyzer = DistractionAnalyzer()
        self.context_analyzer = ContextSwitchAnalyzer()
        self.focus_detector = FocusBreakdownDetector()
        self.time_estimator = TimeLossEstimator()
        self.severity_engine = SeverityEngine()
        self.advisor = RecoveryAdvisor()
        self.insight_gen = InsightGenerator()
        
    def detect_all(self, user_id: int, sessions: List[BehaviorSession]) -> List[ProcrastinationPattern]:
        raw_patterns = []
        raw_patterns.extend(self.distraction_analyzer.detect(sessions))
        raw_patterns.extend(self.context_analyzer.detect(sessions))
        raw_patterns.extend(self.focus_detector.detect(sessions))
        
        # Aggregate by name to sum up frequencies and time lost
        aggregated = self.time_estimator.estimate(raw_patterns)
        
        patterns = []
        for p in aggregated:
            sev = self.severity_engine.calculate(p['frequency'], p['time_lost_mins'])
            conf = min(100.0, p['frequency'] * 15.0) # Simple confidence mapping
            desc = self.insight_gen.generate(p['pattern_name'], p['pattern_type'], p['frequency'], p['time_lost_mins'])
            rec = self.advisor.generate(p['pattern_name'], p['pattern_type'])
            
            pattern = ProcrastinationPattern(
                user_id=user_id,
                pattern_name=p['pattern_name'],
                pattern_type=p['pattern_type'],
                severity_score=sev,
                confidence_score=conf,
                frequency=p['frequency'],
                estimated_time_lost=p['time_lost_mins'],
                description=desc,
                recovery_suggestion=rec
            )
            patterns.append(pattern)
            
        return patterns
