import pytest
from datetime import datetime, timedelta
from app.models.analytics import BehaviorSession
from app.models.scores import ProductivityScore
from app.habits.habit_detector import HabitDetector
from app.habits.confidence_engine import calculate_confidence

def test_confidence_engine():
    # Low frequency
    conf = calculate_confidence(1, 1, 1.0, 0.0)
    assert conf == 0.0
    
    # High frequency, perfect consistency, stable time
    conf = calculate_confidence(10, 10, 1.0, 0.0)
    assert conf == 100.0 # 50 (const) + 30 (freq) + 20 (stab)
    
    # High frequency, poor stability
    conf = calculate_confidence(10, 10, 1.0, 4.0)
    assert conf == 80.0 # 50 + 30 + 0

def test_pattern_miner():
    detector = HabitDetector()
    
    # Create alternating sequence: A -> B -> A -> B
    t = datetime(2023, 1, 1, 10, 0)
    sessions = []
    
    for i in range(3):
        # Session A
        s_a = BehaviorSession(session_type="Coding", start_time=t, end_time=t + timedelta(minutes=30))
        sessions.append(s_a)
        
        # Session B shortly after A
        t2 = t + timedelta(minutes=35) 
        s_b = BehaviorSession(session_type="Music", start_time=t2, end_time=t2 + timedelta(minutes=30))
        sessions.append(s_b)
        
        t = t + timedelta(days=1)
        
    habits = detector.detect_all(1, sessions, [])
    
    # We should have found a pattern: Coding -> Music
    pattern_habits = [h for h in habits if h.habit_name.startswith("Pattern:")]
    assert len(pattern_habits) > 0
    assert "Coding -> Music" in pattern_habits[0].habit_name
