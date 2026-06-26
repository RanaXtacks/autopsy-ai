from app import db
from datetime import datetime

class ProcrastinationPattern(db.Model):
    __tablename__ = 'procrastination_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    pattern_name = db.Column(db.String(255), nullable=False)
    pattern_type = db.Column(db.String(100), nullable=False) # e.g., 'Entertainment before work', 'Context switching spikes'
    severity_score = db.Column(db.Float, nullable=False) # 0-100
    confidence_score = db.Column(db.Float, nullable=False) # 0-100
    frequency = db.Column(db.Integer, nullable=False, default=1)
    estimated_time_lost = db.Column(db.Float, nullable=False, default=0.0) # minutes
    
    description = db.Column(db.Text, nullable=True)
    recovery_suggestion = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pattern_name': self.pattern_name,
            'pattern_type': self.pattern_type,
            'severity_score': self.severity_score,
            'confidence_score': self.confidence_score,
            'frequency': self.frequency,
            'estimated_time_lost': self.estimated_time_lost,
            'description': self.description,
            'recovery_suggestion': self.recovery_suggestion,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
