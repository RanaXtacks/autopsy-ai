import pytest
from analytics.trajectory.goal_tracking_engine import GoalTrackingEngine
from analytics.trajectory.consistency_forecaster import ConsistencyForecaster

def test_goal_tracking_failing():
    engine = GoalTrackingEngine()
    result = engine.calculate_run_rate(current_progress=5.0, target=20.0, days_passed=5, total_days=7)
    
    # 5 hours in 5 days = 1 hour/day. Projected = 7 hours.
    # Target 20 * 0.7 = 14. So 7 is < 14, should be "Failing"
    assert result["status"] == "Failing"
    assert result["projected"] == 7.0

def test_consistency_forecaster():
    forecaster = ConsistencyForecaster()
    # Historical failures at streak lengths 3, 5, 2, 7
    # Current streak is 4.
    # Survivals > 4: 5, 7 (2 survivals)
    # Total: 4
    # Probability: 50%
    prob = forecaster.forecast_survival(current_streak=4, historical_failures=[3, 5, 2, 7])
    assert prob == 50.0
