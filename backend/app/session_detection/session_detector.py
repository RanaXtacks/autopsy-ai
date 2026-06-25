from typing import List, Dict, Any
from app.models.events import BehaviorEvent
from app.models.sessions import BehaviorSession
from app import db
from datetime import timedelta
from .session_classifier import get_classifier

class SessionDetector:
    def __init__(self, gap_threshold_minutes: int = 15):
        """
        Initializes the detector. 
        Events separated by more than `gap_threshold_minutes` belong to different sessions.
        """
        self.gap_threshold = timedelta(minutes=gap_threshold_minutes)
        self.classifier = get_classifier()

    def detect_sessions(self, events: List[BehaviorEvent]) -> List[BehaviorSession]:
        """
        Groups raw events into sessions and classifies them.
        Events must be sorted by timestamp before passing them here.
        """
        if not events:
            return []

        sessions = []
        current_session_events = [events[0]]
        
        for i in range(1, len(events)):
            current_event = events[i]
            prev_event = current_session_events[-1]
            
            time_diff = current_event.timestamp - prev_event.timestamp
            
            if time_diff <= self.gap_threshold:
                current_session_events.append(current_event)
            else:
                # Close current session
                session = self._create_session(current_session_events)
                sessions.append(session)
                
                # Start new session
                current_session_events = [current_event]
                
        # Close the last session
        if current_session_events:
            session = self._create_session(current_session_events)
            sessions.append(session)
            
        return sessions

    def _create_session(self, events: List[BehaviorEvent]) -> BehaviorSession:
        start_time = events[0].timestamp
        end_time = events[-1].timestamp
        duration = (end_time - start_time).total_seconds() / 60.0
        
        # In case it's a single event, give it a nominal duration of 1 min
        if duration == 0:
            duration = 1.0

        session_type = self.classifier.classify(events, duration)
        
        # Calculate a basic productivity score (0-100) based on categories
        work_events = sum(1 for e in events if e.category in ['development', 'learning'])
        productivity_score = round((work_events / len(events)) * 100, 1)

        return BehaviorSession(
            user_id=events[0].user_id,
            upload_id=events[0].upload_id,
            session_type=session_type,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=round(duration, 2),
            event_count=len(events),
            productivity_score=productivity_score
        )
