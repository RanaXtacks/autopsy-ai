from typing import List, Dict, Any
from app.models.sessions import BehaviorSession
from app.models.scores import ProductivityScore
from app.models.habits import Habit
from .routine_analyzer import RoutineAnalyzer
from .pattern_miner import PatternMiner
from .trigger_detector import TriggerDetector
from .insight_generator import InsightGenerator
from .confidence_engine import calculate_confidence
from .habit_types import HabitCategory

class HabitDetector:
    """Orchestrates the detection of habits from sessions and scores."""
    
    def __init__(self):
        self.routine_analyzer = RoutineAnalyzer()
        self.pattern_miner = PatternMiner()
        self.trigger_detector = TriggerDetector()
        self.insight_generator = InsightGenerator()
        
    def detect_all(self, user_id: int, sessions: List[BehaviorSession], scores: List[ProductivityScore]) -> List[Habit]:
        detected_habits = []
        
        if not sessions:
            return detected_habits
            
        # 1. Analyze Routines (Time & Day)
        routines = self.routine_analyzer.analyze(sessions)
        for r in routines:
            desc = self.insight_generator.generate_routine_description(r)
            days_active = len(set([s.start_time.date() for s in sessions if s.start_time]))
            conf = calculate_confidence(
                frequency=r['frequency'],
                days_active=days_active,
                consistency_ratio=r['frequency'] / max(1, days_active),
                time_variance_hours=r.get('variance', 0.0)
            )
            
            habit = Habit(
                user_id=user_id,
                habit_name=f"Routine: {r['session_type']}",
                habit_type=r['category'].value,
                confidence_score=conf,
                frequency=r['frequency'],
                description=desc
            )
            detected_habits.append(habit)
            
        # 2. Mine Sequences
        patterns = self.pattern_miner.mine_sequences(sessions)
        for p in patterns:
            desc = self.insight_generator.generate_sequence_description(p)
            habit = Habit(
                user_id=user_id,
                habit_name=f"Pattern: {p['sequence']}",
                habit_type=HabitCategory.LEARNING.value, # Default categorization for sequence
                confidence_score=min(100.0, p['frequency'] * 15.0), # Simplistic score for sequences
                frequency=p['frequency'],
                description=desc
            )
            detected_habits.append(habit)
            
        # 3. Detect Triggers
        triggers = self.trigger_detector.detect(sessions, scores)
        for t in triggers:
            desc = self.insight_generator.generate_trigger_description(t)
            habit = Habit(
                user_id=user_id,
                habit_name=f"Trigger: {t['trigger_event']}",
                habit_type=HabitCategory.PROCRASTINATION.value if t['type'] == 'negative_trigger' else HabitCategory.PRODUCTIVITY.value,
                confidence_score=85.0, # High confidence for explicit triggers
                frequency=t['frequency'],
                description=desc
            )
            detected_habits.append(habit)
            
        return detected_habits
