from app import db
from datetime import datetime
import json

class BurnoutAssessment(db.Model):
    __tablename__ = 'burnout_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    risk_score = db.Column(db.Float, nullable=False) # 0-100
    risk_level = db.Column(db.String(50), nullable=False) # Low, Moderate, High, Critical
    
    # Store lists as JSON strings for simplicity and ML compatibility
    primary_risk_factors = db.Column(db.Text, nullable=False, default="[]") 
    recommended_actions = db.Column(db.Text, nullable=False, default="[]")
    
    confidence_score = db.Column(db.Float, nullable=False, default=80.0) # 0-100
    
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        try:
            factors = json.loads(self.primary_risk_factors)
        except:
            factors = []
            
        try:
            actions = json.loads(self.recommended_actions)
        except:
            actions = []
            
        return {
            'id': self.id,
            'user_id': self.user_id,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'primary_risk_factors': factors,
            'recommended_actions': actions,
            'confidence_score': self.confidence_score,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None
        }
