from app import db
from .core import TimestampMixin


class BehaviorEvent(db.Model, TimestampMixin):
    __tablename__ = 'behavior_events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id', ondelete='CASCADE'), nullable=False, index=True)
    
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    source = db.Column(db.String(50), nullable=False, index=True)  # chrome, github, screentime, spotify
    event_type = db.Column(db.String(100), nullable=False, index=True)  # visit, commit, app_usage, play
    category = db.Column(db.String(50), nullable=True, index=True)  # entertainment, development, learning
    value = db.Column(db.String(500), nullable=True)  # URL, App Name, Track Name
    metadata_obj = db.Column(db.JSON, nullable=True)  # Storing additional specific data (JSON named metadata_obj since metadata is reserved by SQLAlchemy)
    
    # Relationships
    user = db.relationship('User', back_populates='events')
    upload = db.relationship('Upload', back_populates='events')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'upload_id': self.upload_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'source': self.source,
            'event_type': self.event_type,
            'category': self.category,
            'value': self.value,
            'metadata': self.metadata_obj,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
