import pytest
from app.procrastination.severity_engine import SeverityEngine
from app.procrastination.time_loss_estimator import TimeLossEstimator

def test_severity_calculation():
    engine = SeverityEngine()
    
    # Low frequency, low time lost
    low = engine.calculate(frequency=1, time_lost_mins=10)
    assert low < 20
    
    # High frequency, high time lost
    high = engine.calculate(frequency=10, time_lost_mins=240) # 4 hours
    assert high > 80

def test_time_loss_estimation():
    estimator = TimeLossEstimator()
    raw_patterns = [
        {"pattern_name": "A", "frequency": 1, "time_lost_mins": 30},
        {"pattern_name": "A", "frequency": 1, "time_lost_mins": 20},
        {"pattern_name": "B", "frequency": 2, "time_lost_mins": 50},
    ]
    
    aggregated = estimator.estimate(raw_patterns)
    
    assert len(aggregated) == 2
    
    a_pattern = next(p for p in aggregated if p["pattern_name"] == "A")
    assert a_pattern["frequency"] == 2
    assert a_pattern["time_lost_mins"] == 50
