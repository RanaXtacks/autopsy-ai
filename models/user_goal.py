from datetime import datetime

class UserGoal:
    def __init__(self, id, user_id, target_metric, target_value, timeframe, created_at=None):
        self.id = id
        self.user_id = user_id
        self.target_metric = target_metric # e.g., "Weekly Deep Work"
        self.target_value = target_value # e.g., 15 (hours)
        self.timeframe = timeframe # e.g., "weekly", "monthly"
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_metric': self.target_metric,
            'target_value': self.target_value,
            'timeframe': self.timeframe,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
