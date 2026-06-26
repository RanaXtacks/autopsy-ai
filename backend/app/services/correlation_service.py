from typing import List, Dict, Any
from app import db
from app.models.analytics import BehaviorSession
from app.models.scores import ProductivityScore
from app.models.correlations import BehaviorCorrelation
from app.correlations.correlation_engine import CorrelationEngine

class CorrelationService:
    @staticmethod
    def generate_correlations_for_user(user_id: int) -> List[BehaviorCorrelation]:
        """Runs the correlation engine and saves the results."""
        
        # 1. Fetch historical data
        sessions = BehaviorSession.query.filter_by(user_id=user_id).order_by(BehaviorSession.start_time.asc()).all()
        scores = ProductivityScore.query.filter_by(user_id=user_id).order_by(ProductivityScore.date.asc()).all()
        
        # 2. Run engine
        engine = CorrelationEngine()
        detected_correlations = engine.analyze(user_id, sessions, scores)
        
        # 3. Save to database (replace old correlations for now)
        BehaviorCorrelation.query.filter_by(user_id=user_id).delete()
        for c in detected_correlations:
            db.session.add(c)
            
        db.session.commit()
        return detected_correlations

    @staticmethod
    def get_correlations(user_id: int) -> List[BehaviorCorrelation]:
        """Returns all correlations sorted by confidence score."""
        return BehaviorCorrelation.query.filter_by(user_id=user_id).order_by(BehaviorCorrelation.confidence_score.desc()).all()
        
    @staticmethod
    def get_top_correlations(user_id: int) -> List[BehaviorCorrelation]:
        """Returns the most statistically significant correlations (high confidence, strong R)."""
        return BehaviorCorrelation.query.filter_by(user_id=user_id)\
            .filter(BehaviorCorrelation.confidence_score > 50)\
            .order_by(BehaviorCorrelation.confidence_score.desc()).limit(5).all()

    @staticmethod
    def get_negative_correlations(user_id: int) -> List[BehaviorCorrelation]:
        return BehaviorCorrelation.query.filter_by(user_id=user_id)\
            .filter(BehaviorCorrelation.relationship_type.like('%Negative%'))\
            .order_by(BehaviorCorrelation.confidence_score.desc()).all()
            
    @staticmethod
    def get_positive_correlations(user_id: int) -> List[BehaviorCorrelation]:
        return BehaviorCorrelation.query.filter_by(user_id=user_id)\
            .filter(BehaviorCorrelation.relationship_type.like('%Positive%'))\
            .order_by(BehaviorCorrelation.confidence_score.desc()).all()
