import json
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app import db
from app.models.analytics import BehaviorSession
from app.models.scores import ProductivityScore
from app.models.procrastination import ProcrastinationPattern
from app.models.burnout import BurnoutAssessment
from app.burnout.burnout_engine import BurnoutEngine
from app.config.burnout_config import BurnoutConfig

class BurnoutService:
    @staticmethod
    def generate_assessment(user_id: int) -> BurnoutAssessment:
        # Define analysis window
        window_start = datetime.utcnow() - timedelta(days=BurnoutConfig.ANALYSIS_WINDOW_DAYS)
        
        # 1. Fetch data
        sessions = BehaviorSession.query.filter(
            BehaviorSession.user_id == user_id,
            BehaviorSession.start_time >= window_start
        ).order_by(BehaviorSession.start_time.asc()).all()
        
        scores = ProductivityScore.query.filter(
            ProductivityScore.user_id == user_id,
            ProductivityScore.date >= window_start.date()
        ).order_by(ProductivityScore.date.asc()).all()
        
        procrastination = ProcrastinationPattern.query.filter_by(user_id=user_id).all()
        
        # 2. Run engine
        engine = BurnoutEngine()
        assessment = engine.analyze(user_id, sessions, scores, procrastination)
        
        # 3. Save to database
        db.session.add(assessment)
        db.session.commit()
        
        return assessment

    @staticmethod
    def get_latest_assessment(user_id: int) -> BurnoutAssessment:
        return BurnoutAssessment.query.filter_by(user_id=user_id)\
            .order_by(BurnoutAssessment.generated_at.desc()).first()
            
    @staticmethod
    def get_history(user_id: int) -> List[BurnoutAssessment]:
        # Return last 30 assessments for trend charting
        return BurnoutAssessment.query.filter_by(user_id=user_id)\
            .order_by(BurnoutAssessment.generated_at.desc()).limit(30).all()
            
    @staticmethod
    def get_risk_factors(user_id: int) -> List[str]:
        assessment = BurnoutService.get_latest_assessment(user_id)
        if assessment:
            try:
                return json.loads(assessment.primary_risk_factors)
            except:
                pass
        return []
