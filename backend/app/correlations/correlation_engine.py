from typing import List
from app.models.analytics import BehaviorSession
from app.models.scores import ProductivityScore
from app.models.correlations import BehaviorCorrelation
from .feature_builder import FeatureBuilder
from .relationship_analyzer import RelationshipAnalyzer
from .confidence_calculator import ConfidenceCalculator
from .explanation_generator import ExplanationGenerator

class CorrelationEngine:
    """Orchestrates the discovery of behavioral correlations."""
    
    def __init__(self):
        self.feature_builder = FeatureBuilder()
        self.analyzer = RelationshipAnalyzer()
        self.confidence_calc = ConfidenceCalculator()
        self.explainer = ExplanationGenerator()
        
    def analyze(self, user_id: int, sessions: List[BehaviorSession], scores: List[ProductivityScore]) -> List[BehaviorCorrelation]:
        correlations = []
        if not sessions or not scores:
            return correlations
            
        # 1. Build Features per day
        daily_features = self.feature_builder.build_daily_features(sessions)
        
        # 2. Map scores to days
        daily_scores = {s.date.isoformat(): s for s in scores}
        
        # 3. Align data vectors
        aligned_days = set(daily_features.keys()).intersection(set(daily_scores.keys()))
        if not aligned_days:
            return correlations
            
        factors_to_test = [
            ('music_duration_mins', 'Music Duration'),
            ('coding_duration_mins', 'Coding Duration'),
            ('study_duration_mins', 'Study Duration'),
            ('entertainment_duration_mins', 'Entertainment Duration'),
            ('late_night_entertainment_mins', 'Late Night Entertainment'),
            ('context_switches', 'Context Switching')
        ]
        
        outcomes_to_test = [
            ('productivity_score', 'Productivity Score'),
            ('focus_score', 'Focus Score'),
            ('consistency_score', 'Consistency Score'),
            ('deep_work_score', 'Deep Work Score')
        ]
        
        # 4. Compute correlations
        for factor_key, factor_name in factors_to_test:
            for outcome_key, outcome_name in outcomes_to_test:
                x = []
                y = []
                
                for day in aligned_days:
                    x.append(daily_features[day][factor_key])
                    y.append(getattr(daily_scores[day], outcome_key))
                    
                # Skip if variance is zero (e.g., user never listened to music)
                if len(set(x)) <= 1 or len(set(y)) <= 1:
                    continue
                    
                r = self.analyzer.analyze_relationship(x, y)
                n = len(x)
                
                # We only want to save meaningful correlations
                if abs(r) < 0.15 and n >= 5:
                    continue
                    
                conf = self.confidence_calc.calculate(r, n)
                rel_type = self.confidence_calc.determine_type(r, n)
                explanation = self.explainer.generate(factor_name, outcome_name, r, rel_type)
                
                corr = BehaviorCorrelation(
                    user_id=user_id,
                    factor=factor_name,
                    outcome=outcome_name,
                    correlation_strength=r,
                    confidence_score=conf,
                    relationship_type=rel_type,
                    explanation=explanation
                )
                correlations.append(corr)
                
        return correlations
