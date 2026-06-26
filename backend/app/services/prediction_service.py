import json
from typing import List
from datetime import datetime, timedelta
from app import db
from app.models.analytics import BehaviorSession
from app.models.burnout import BurnoutAssessment
from app.models.predictions import FocusPrediction
from app.predictions.focus_predictor import FocusPredictor

class PredictionService:
    @staticmethod
    def generate_predictions(user_id: int) -> List[FocusPrediction]:
        # 1. Fetch historical data (e.g., last 30 days of sessions)
        window_start = datetime.utcnow() - timedelta(days=30)
        sessions = BehaviorSession.query.filter(
            BehaviorSession.user_id == user_id,
            BehaviorSession.start_time >= window_start
        ).all()
        
        # 2. Fetch latest Burnout Assessment
        latest_burnout = BurnoutAssessment.query.filter_by(user_id=user_id)\
            .order_by(BurnoutAssessment.generated_at.desc()).first()
            
        burnout_risk = latest_burnout.risk_score if latest_burnout else 0.0
        
        # 3. Predict for tomorrow
        predictor = FocusPredictor()
        raw_predictions = predictor.predict_tomorrow(user_id, sessions, burnout_risk)
        
        target_date = (datetime.utcnow() + timedelta(days=1)).date()
        
        # Clear existing predictions for tomorrow to avoid duplicates
        FocusPrediction.query.filter_by(user_id=user_id, predicted_date=target_date).delete()
        
        # 4. Save to DB
        created = []
        for raw in raw_predictions:
            p = FocusPrediction(
                user_id=user_id,
                predicted_date=target_date,
                optimal_start_time=raw["optimal_start_time"],
                optimal_end_time=raw["optimal_end_time"],
                activity_type=raw["activity_type"],
                confidence_score=raw["confidence_score"],
                contributing_factors=json.dumps(raw["contributing_factors"])
            )
            db.session.add(p)
            created.append(p)
            
        db.session.commit()
        return created

    @staticmethod
    def get_tomorrow_predictions(user_id: int) -> List[FocusPrediction]:
        target_date = (datetime.utcnow() + timedelta(days=1)).date()
        return FocusPrediction.query.filter_by(user_id=user_id, predicted_date=target_date)\
            .order_by(FocusPrediction.optimal_start_time.asc()).all()

    @staticmethod
    def get_chronotype(user_id: int) -> str:
        # A quick hack for the dashboard to just get the chronotype without persisting a new model
        # Just grab the chronotype from tomorrow's prediction if it exists
        preds = PredictionService.get_tomorrow_predictions(user_id)
        if preds:
            factors = json.loads(preds[0].contributing_factors)
            if factors:
                return factors[0] # the first factor is the chronotype
        return "Unknown Profile"
