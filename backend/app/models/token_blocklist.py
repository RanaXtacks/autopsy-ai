from app import db
from datetime import datetime

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User')

    def to_dict(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_id': self.user_id,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None,
            'expires': self.expires.isoformat() if self.expires else None
        }
