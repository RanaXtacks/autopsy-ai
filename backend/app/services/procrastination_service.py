from typing import List, Dict, Any
from app import db
from app.models.sessions import BehaviorSession
from app.models.procrastination import ProcrastinationPattern
from app.procrastination.procrastination_detector import ProcrastinationDetector

class ProcrastinationService:
    @staticmethod
    def generate_patterns_for_user(user_id: int) -> List[ProcrastinationPattern]:
        # 1. Fetch historical data
        sessions = BehaviorSession.query.filter_by(user_id=user_id).order_by(BehaviorSession.start_time.asc()).all()
        
        # 2. Run engine
        engine = ProcrastinationDetector()
        detected_patterns = engine.detect_all(user_id, sessions)
        
        # 3. Save to database (replace old for now)
        ProcrastinationPattern.query.filter_by(user_id=user_id).delete()
        for p in detected_patterns:
            db.session.add(p)
            
        db.session.commit()
        return detected_patterns

    @staticmethod
    def get_patterns(user_id: int) -> List[ProcrastinationPattern]:
        return ProcrastinationPattern.query.filter_by(user_id=user_id).order_by(ProcrastinationPattern.severity_score.desc()).all()
        
    @staticmethod
    def get_top_distractions(user_id: int) -> List[ProcrastinationPattern]:
        return ProcrastinationPattern.query.filter_by(user_id=user_id)\
            .filter_by(pattern_type='Distraction Loop')\
            .order_by(ProcrastinationPattern.severity_score.desc()).limit(5).all()

    @staticmethod
    def get_time_loss_metrics(user_id: int) -> Dict[str, float]:
        patterns = ProcrastinationService.get_patterns(user_id)
        
        # Currently, the time loss is calculated across all analyzed sessions. 
        # In a real app, we'd filter by timeframes. For now, we project weekly.
        total_lost = sum(p.estimated_time_lost for p in patterns)
        
        return {
            "daily_lost_mins": round(total_lost / 7, 1),
            "weekly_lost_mins": round(total_lost, 1),
            "monthly_lost_mins": round(total_lost * 4.3, 1),
            "total_lost_mins": round(total_lost, 1)
        }
