from typing import List, Dict, Any
from app.models.sessions import BehaviorSession
from app.models.scores import ProductivityScore
from datetime import timedelta

class TriggerDetector:
    """Detects triggers and correlations between sessions and productivity."""
    
    def detect(self, sessions: List[BehaviorSession], scores: List[ProductivityScore]) -> List[Dict[str, Any]]:
        triggers = []
        
        # Map scores by date for easy lookup
        scores_by_date = {score.date: score for score in scores}
        
        # Look for events triggering specific score outcomes
        # e.g., Late night entertainment correlates with lower focus score next day
        
        # E.g. find all sessions after 11 PM
        late_sessions = [s for s in sessions if s.start_time and s.start_time.hour >= 23]
        if late_sessions:
            impacts = []
            for s in late_sessions:
                next_day = s.start_time.date() + timedelta(days=1)
                if next_day in scores_by_date:
                    impacts.append(scores_by_date[next_day].focus_score)
            
            if impacts and sum(impacts)/len(impacts) < 50:
                triggers.append({
                    'type': 'negative_trigger',
                    'trigger_event': 'Late Night Entertainment',
                    'impact': 'Focus Score drops next day',
                    'frequency': len(impacts)
                })
                
        # Look for pre-work routines
        # e.g., Music before Deep Work
        for i in range(len(sessions) - 1):
            s1, s2 = sessions[i], sessions[i+1]
            if s1.session_type == 'Music Session' and s2.session_type == 'Deep Work Session':
                gap = (s2.start_time - s1.end_time).total_seconds() / 60.0
                if gap < 30:
                    score = scores_by_date.get(s1.start_time.date())
                    prod = score.productivity_score if score else None
                    triggers.append({
                        'type': 'positive_trigger',
                        'trigger_event': 'Music before Work',
                        'impact': f'Productivity {prod}' if prod else 'Improved flow',
                        'frequency': 1
                    })
                    
        # Group similar triggers in a real ML system. For now we just return them.
        return triggers
