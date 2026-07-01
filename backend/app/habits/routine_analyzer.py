from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np

from app.models.sessions import BehaviorSession
from .habit_types import MIN_SESSIONS_FOR_ROUTINE, HabitCategory

class RoutineAnalyzer:
    """Analyzes sessions to find time-of-day and day-of-week routines."""
    
    def analyze(self, sessions: List[BehaviorSession]) -> List[Dict[str, Any]]:
        routines = []
        
        # Group by session type
        type_groups = defaultdict(list)
        for s in sessions:
            if s.start_time:
                type_groups[s.session_type].append(s)
                
        for session_type, type_sessions in type_groups.items():
            if len(type_sessions) < MIN_SESSIONS_FOR_ROUTINE:
                continue
                
            # Analyze time of day
            start_hours = [s.start_time.hour + s.start_time.minute / 60.0 for s in type_sessions]
            mean_hour = np.mean(start_hours)
            variance = np.std(start_hours)
            
            # Analyze day of week
            days = [s.start_time.weekday() for s in type_sessions]
            day_counts = {day: days.count(day) for day in set(days)}
            top_day = max(day_counts, key=day_counts.get)
            top_day_ratio = day_counts[top_day] / len(days)
            
            # If standard deviation is low, it's a time-based routine
            if variance <= 2.0: # within a 4 hour window
                routines.append({
                    'type': 'time_routine',
                    'session_type': session_type,
                    'mean_hour': mean_hour,
                    'variance': variance,
                    'frequency': len(type_sessions),
                    'category': HabitCategory.PRODUCTIVITY if 'Work' in session_type or 'Study' in session_type else HabitCategory.ENTERTAINMENT
                })
                
            # If it heavily favors specific days
            if top_day_ratio > 0.4 and len(days) >= 3:
                routines.append({
                    'type': 'day_routine',
                    'session_type': session_type,
                    'top_day': top_day,
                    'top_day_ratio': top_day_ratio,
                    'frequency': len(type_sessions),
                    'category': HabitCategory.PRODUCTIVITY if 'Work' in session_type or 'Study' in session_type else HabitCategory.ENTERTAINMENT
                })
                
        return routines
