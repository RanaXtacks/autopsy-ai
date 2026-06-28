import pytest
from datetime import datetime, timedelta
from analytics.predictions.focus_predictor import FocusPredictor

def test_focus_predictor_early_peak():
    predictor = FocusPredictor()
    
    # Mock some sessions that imply an early peak
    class MockSession:
        def __init__(self, hour):
            self.session_type = "Deep Work"
            self.start_time = datetime(2023, 1, 1, hour, 0)
            
    sessions = [MockSession(8), MockSession(9), MockSession(10)]
    
    predictions = predictor.predict_tomorrow(user_id=1, sessions=sessions, burnout_risk=20.0)
    
    assert len(predictions) == 3 # Early Peak has 3 windows by default
    assert predictions[0]["activity_type"] == "Deep Work"
    assert predictions[0]["confidence_score"] == 70.0 # base confidence
