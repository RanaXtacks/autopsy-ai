from app import db
from datetime import datetime
import json

class FocusPrediction(db.Model):
    __tablename__ = 'focus_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    predicted_date = db.Column(db.Date, nullable=False)
    optimal_start_time = db.Column(db.DateTime, nullable=False)
    optimal_end_time = db.Column(db.DateTime, nullable=False)
    
    activity_type = db.Column(db.String(100), nullable=False) # e.g., Coding, Study, Deep Work
    confidence_score = db.Column(db.Float, nullable=False)
    
    # Using JSON string for flexibility as requested
    contributing_factors = db.Column(db.Text, nullable=False, default="[]") 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        try:
            factors = json.loads(self.contributing_factors)
        except:
            factors = []
            
        return {
            'id': self.id,
            'user_id': self.user_id,
            'predicted_date': self.predicted_date.isoformat(),
            'optimal_start_time': self.optimal_start_time.isoformat(),
            'optimal_end_time': self.optimal_end_time.isoformat(),
            'activity_type': self.activity_type,
            'confidence_score': self.confidence_score,
            'contributing_factors': factors,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
