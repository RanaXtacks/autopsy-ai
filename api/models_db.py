from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)

class BehaviorSession(Base):
    __tablename__ = 'behavior_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    upload_id = Column(Integer, nullable=True, index=True) # Skipped FK to simplify
    
    session_type = Column(String(100), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Float, nullable=False)
    event_count = Column(Integer, nullable=False, default=0)
    productivity_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    habit_name = Column(String(128), nullable=False)
    habit_type = Column(String(64), nullable=False)
    
    confidence_score = Column(Float, nullable=False, default=0.0)
    frequency = Column(Integer, nullable=False, default=1)
    
    first_detected = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_detected = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductivityScore(Base):
    __tablename__ = 'productivity_scores'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    
    productivity_score = Column(Float, nullable=False, default=0.0)
    focus_score = Column(Float, nullable=False, default=0.0)
    consistency_score = Column(Float, nullable=False, default=0.0)
    discipline_score = Column(Float, nullable=False, default=0.0)
    deep_work_score = Column(Float, nullable=False, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
