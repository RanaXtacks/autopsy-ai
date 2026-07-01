from typing import List, Dict, Any
from app import db
from app.models.habits import Habit
from app.models.sessions import BehaviorSession
from app.models.scores import ProductivityScore
from app.habits.habit_detector import HabitDetector

class HabitService:
    @staticmethod
    def generate_habits_for_user(user_id: int) -> List[Habit]:
        """Runs the detection engine and saves the results."""
        
        # 1. Fetch historical data
        sessions = BehaviorSession.query.filter_by(user_id=user_id).order_by(BehaviorSession.start_time.asc()).all()
        scores = ProductivityScore.query.filter_by(user_id=user_id).order_by(ProductivityScore.date.asc()).all()
        
        # 2. Run detector
        detector = HabitDetector()
        detected_habits = detector.detect_all(user_id, sessions, scores)
        
        # 3. Save to database (replace old habits for now, or update if we implement history tracking)
        Habit.query.filter_by(user_id=user_id).delete()
        for h in detected_habits:
            db.session.add(h)
            
        db.session.commit()
        return detected_habits

    @staticmethod
    def get_habits(user_id: int) -> List[Habit]:
        """Returns all habits sorted by confidence score."""
        return Habit.query.filter_by(user_id=user_id).order_by(Habit.confidence_score.desc()).all()
        
    @staticmethod
    def get_habit_summary(user_id: int) -> Dict[str, Any]:
        """Returns a statistical summary of habits."""
        habits = HabitService.get_habits(user_id)
        if not habits:
            return {'total_habits': 0}
            
        avg_confidence = sum([h.confidence_score for h in habits]) / len(habits)
        
        top_habits = [h.to_dict() for h in habits[:3]]
        
        return {
            'total_habits': len(habits),
            'average_confidence': round(avg_confidence, 1),
            'top_habits': top_habits
        }
