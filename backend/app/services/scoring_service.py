from datetime import date, timedelta
from typing import Dict, Any, List
from app import db
from app.models.sessions import BehaviorSession
from app.models.scores import ProductivityScore
from app.scoring import ProductivityEngine, InsightEngine

class ScoringService:
    @staticmethod
    def generate_scores_for_date(user_id: int, target_date: date) -> ProductivityScore:
        """
        Generates productivity scores for a specific date based on sessions.
        """
        # Fetch sessions for the target date
        daily_sessions = db.session.query(BehaviorSession).filter(
            BehaviorSession.user_id == user_id,
            db.func.date(BehaviorSession.start_time) == target_date
        ).all()
        
        # Fetch historical sessions (e.g., last 7 days) for consistency/trends
        start_history = target_date - timedelta(days=7)
        historical_sessions = db.session.query(BehaviorSession).filter(
            BehaviorSession.user_id == user_id,
            db.func.date(BehaviorSession.start_time) >= start_history,
            db.func.date(BehaviorSession.start_time) < target_date
        ).all()
        
        engine = ProductivityEngine()
        calculated_scores = engine.calculate(daily_sessions, historical_sessions)
        
        # Upsert the score
        score = db.session.query(ProductivityScore).filter_by(user_id=user_id, date=target_date).first()
        if not score:
            score = ProductivityScore(user_id=user_id, date=target_date)
            db.session.add(score)
            
        score.productivity_score = calculated_scores["productivity_score"]
        score.focus_score = calculated_scores["focus_score"]
        score.consistency_score = calculated_scores["consistency_score"]
        score.discipline_score = calculated_scores["discipline_score"]
        score.deep_work_score = calculated_scores["deep_work_score"]
        
        db.session.commit()
        return score

    @staticmethod
    def get_today_scores(user_id: int) -> Dict[str, Any]:
        today = date.today()
        score = db.session.query(ProductivityScore).filter_by(user_id=user_id, date=today).first()
        yesterday = db.session.query(ProductivityScore).filter_by(user_id=user_id, date=today - timedelta(days=1)).first()
        
        current_dict = score.to_dict() if score else {}
        prev_dict = yesterday.to_dict() if yesterday else {}
        
        insights = InsightEngine.generate_insights(current_dict, prev_dict)
        
        return {
            "scores": current_dict,
            "insights": insights
        }

    @staticmethod
    def get_history(user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        start_date = date.today() - timedelta(days=days)
        scores = db.session.query(ProductivityScore).filter(
            ProductivityScore.user_id == user_id,
            ProductivityScore.date >= start_date
        ).order_by(ProductivityScore.date.asc()).all()
        
        return [s.to_dict() for s in scores]

    @staticmethod
    def get_trends(user_id: int) -> Dict[str, Any]:
        # Simple implementation returning last 7 days averages vs previous 7 days
        today = date.today()
        last_7 = db.session.query(ProductivityScore).filter(
            ProductivityScore.user_id == user_id,
            ProductivityScore.date > today - timedelta(days=7),
            ProductivityScore.date <= today
        ).all()
        
        prev_7 = db.session.query(ProductivityScore).filter(
            ProductivityScore.user_id == user_id,
            ProductivityScore.date > today - timedelta(days=14),
            ProductivityScore.date <= today - timedelta(days=7)
        ).all()
        
        def avg(scores_list, key):
            if not scores_list: return 0.0
            return sum(getattr(s, key) for s in scores_list) / len(scores_list)
            
        return {
            "current_week_avg": round(avg(last_7, 'productivity_score'), 1),
            "prev_week_avg": round(avg(prev_7, 'productivity_score'), 1),
            "trend_percentage": round(avg(last_7, 'productivity_score') - avg(prev_7, 'productivity_score'), 1)
        }
