from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(db.Model, TimestampMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Relationships
    uploads = db.relationship('Upload', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    reports = db.relationship('Report', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    events = db.relationship('BehaviorEvent', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    sessions = db.relationship('BehaviorSession', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    productivity_scores = db.relationship('ProductivityScore', backref='user', lazy=True, cascade="all, delete-orphan")
    habits = db.relationship('Habit', backref='user', lazy=True, cascade="all, delete-orphan")
    correlations = db.relationship('BehaviorCorrelation', backref='user', lazy=True, cascade="all, delete-orphan")
    procrastination_patterns = db.relationship('ProcrastinationPattern', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Upload(db.Model, TimestampMixin):
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    original_filename = db.Column(db.String(255), nullable=False, index=True)
    stored_filename = db.Column(db.String(255), nullable=False, unique=True, index=True)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.BigInteger, nullable=False)  # in bytes
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = db.Column(
        db.Enum('uploaded', 'processing', 'completed', 'failed', name='upload_status_enum'),
        nullable=False,
        default='uploaded',
        index=True
    )
    upload_source = db.Column(db.String(50), nullable=False, default='web')
    
    # Relationships
    user = db.relationship('User', back_populates='uploads')
    events = db.relationship('BehaviorEvent', back_populates='upload', cascade='all, delete-orphan', lazy='dynamic')
    sessions = db.relationship('BehaviorSession', back_populates='upload', cascade='all, delete-orphan', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'original_filename': self.original_filename,
            'stored_filename': self.stored_filename,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'status': self.status,
            'upload_source': self.upload_source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Report(db.Model, TimestampMixin):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    report_type = db.Column(db.String(100), nullable=False, index=True)
    report_data = db.Column(db.JSON, nullable=False)  # Storing JSON data
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='reports')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'report_type': self.report_type,
            'report_data': self.report_data,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }