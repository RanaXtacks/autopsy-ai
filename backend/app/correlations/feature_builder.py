from typing import List, Dict, Any
from app.models.analytics import BehaviorSession

class FeatureBuilder:
    """Extracts quantifiable behavioral features from raw sessions for correlation."""
    
    def build_daily_features(self, sessions: List[BehaviorSession]) -> Dict[str, Dict[str, float]]:
        """
        Groups sessions by day and extracts features like:
        - Music Duration (minutes)
        - Coding Duration (minutes)
        - Context Switches (count)
        - Entertainment after 11 PM (minutes)
        """
        daily_features = {}
        
        for s in sessions:
            if not s.start_time:
                continue
                
            day = s.start_time.date().isoformat()
            if day not in daily_features:
                daily_features[day] = {
                    'music_duration_mins': 0,
                    'coding_duration_mins': 0,
                    'study_duration_mins': 0,
                    'entertainment_duration_mins': 0,
                    'late_night_entertainment_mins': 0,
                    'context_switches': 0
                }
                
            features = daily_features[day]
            duration = s.duration_minutes or 0
            
            if s.session_type == "Music":
                features['music_duration_mins'] += duration
            elif s.session_type == "Coding":
                features['coding_duration_mins'] += duration
            elif s.session_type == "Study":
                features['study_duration_mins'] += duration
            elif s.session_type == "Entertainment":
                features['entertainment_duration_mins'] += duration
                if s.start_time.hour >= 23 or s.start_time.hour < 4:
                    features['late_night_entertainment_mins'] += duration
            elif s.session_type == "Context Switching":
                features['context_switches'] += s.event_count or 0
                
        return daily_features
