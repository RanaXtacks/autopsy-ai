from datetime import datetime
import json

class PeriodicReport:
    def __init__(self, id, user_id, period_type, period_start_date, period_end_date, average_productivity_score, average_focus_score, total_deep_work_minutes, top_distraction_id, delta_percentage_vs_previous, created_at=None):
        self.id = id
        self.user_id = user_id
        self.period_type = period_type
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.average_productivity_score = average_productivity_score
        self.average_focus_score = average_focus_score
        self.total_deep_work_minutes = total_deep_work_minutes
        self.top_distraction_id = top_distraction_id
        self.delta_percentage_vs_previous = delta_percentage_vs_previous
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'period_type': self.period_type,
            'period_start_date': self.period_start_date.isoformat() if hasattr(self.period_start_date, 'isoformat') else self.period_start_date,
            'period_end_date': self.period_end_date.isoformat() if hasattr(self.period_end_date, 'isoformat') else self.period_end_date,
            'average_productivity_score': self.average_productivity_score,
            'average_focus_score': self.average_focus_score,
            'total_deep_work_minutes': self.total_deep_work_minutes,
            'top_distraction_id': self.top_distraction_id,
            'delta_percentage_vs_previous': self.delta_percentage_vs_previous,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
