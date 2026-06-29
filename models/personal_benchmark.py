from datetime import datetime

class PersonalBenchmark:
    def __init__(self, id, user_id, metric_name, baseline_value, standard_deviation, created_at=None):
        self.id = id
        self.user_id = user_id
        self.metric_name = metric_name # e.g., 'Deep Work', 'Context Switching'
        self.baseline_value = baseline_value # Rolling 30-day average
        self.standard_deviation = standard_deviation
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'baseline_value': self.baseline_value,
            'standard_deviation': self.standard_deviation,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
