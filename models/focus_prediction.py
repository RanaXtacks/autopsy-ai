from datetime import datetime
import json

class FocusPrediction:
    def __init__(self, id, user_id, predicted_date, optimal_start_time, optimal_end_time, activity_type, confidence_score, contributing_factors, created_at=None):
        self.id = id
        self.user_id = user_id
        self.predicted_date = predicted_date
        self.optimal_start_time = optimal_start_time
        self.optimal_end_time = optimal_end_time
        self.activity_type = activity_type
        self.confidence_score = confidence_score
        self.contributing_factors = contributing_factors
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        try:
            factors = json.loads(self.contributing_factors) if isinstance(self.contributing_factors, str) else self.contributing_factors
        except:
            factors = []
            
        return {
            'id': self.id,
            'user_id': self.user_id,
            'predicted_date': self.predicted_date.isoformat() if hasattr(self.predicted_date, 'isoformat') else self.predicted_date,
            'optimal_start_time': self.optimal_start_time.isoformat() if hasattr(self.optimal_start_time, 'isoformat') else self.optimal_start_time,
            'optimal_end_time': self.optimal_end_time.isoformat() if hasattr(self.optimal_end_time, 'isoformat') else self.optimal_end_time,
            'activity_type': self.activity_type,
            'confidence_score': self.confidence_score,
            'contributing_factors': factors,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
