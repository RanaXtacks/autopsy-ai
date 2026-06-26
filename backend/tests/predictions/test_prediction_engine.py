import pytest
from datetime import datetime, time, date
from app.predictions.window_estimator import WindowEstimator
from app.predictions.fatigue_adjuster import FatigueAdjuster
from app.predictions.chronotype_analyzer import ChronotypeAnalyzer

def test_chronotype_analyzer():
    analyzer = ChronotypeAnalyzer()
    # Empty sessions should fallback
    assert analyzer.analyze([]) == "Early Peak Profile"
    
def test_window_estimator():
    estimator = WindowEstimator()
    target_date = date.today()
    
    # Early peak should yield morning block
    windows = estimator.estimate(target_date, "Early Peak Profile", [])
    assert any(w["activity_type"] == "Deep Work" and w["start_time"].hour == 8 for w in windows)

def test_fatigue_adjuster():
    adjuster = FatigueAdjuster()
    windows = [
        {"start_time": datetime(2023, 1, 1, 9, 0), "end_time": datetime(2023, 1, 1, 11, 0), "activity_type": "Deep Work"}
    ]
    
    # Low burnout = no adjustment
    adj_low = adjuster.adjust([dict(w) for w in windows], 20.0)
    assert (adj_low[0]["end_time"] - adj_low[0]["start_time"]).total_seconds() == 7200
    
    # High burnout = 30% reduction (7200 * 0.7 = 5040 seconds)
    adj_high = adjuster.adjust([dict(w) for w in windows], 80.0)
    assert (adj_high[0]["end_time"] - adj_high[0]["start_time"]).total_seconds() == 5040
