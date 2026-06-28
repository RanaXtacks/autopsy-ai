import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from analytics.trajectory.macro_trend_detector import MacroTrendDetector
from analytics.trajectory.goal_tracking_engine import GoalTrackingEngine
from analytics.trajectory.consistency_forecaster import ConsistencyForecaster
from analytics.trajectory.trajectory_scoring import TrajectoryScoring

def test_goal_tracking_engine_on_track():
    engine = GoalTrackingEngine()
    result = engine.calculate_trajectory(15.0, "week", 12.0, 5, 7)
    assert result["status"] == "On Track"

def test_goal_tracking_engine_failing():
    engine = GoalTrackingEngine()
    result = engine.calculate_trajectory(15.0, "week", 5.0, 5, 7)
    assert result["status"] == "Failing"

def test_macro_trend_detection():
    detector = MacroTrendDetector()
    result = detector.detect_macro_trend(user_id=1)
    assert "trend_type" in result

def test_consistency_forecaster():
    forecaster = ConsistencyForecaster()
    result = forecaster.forecast_consistency(1, [3, 4, 2], 5, "Saturday")
    assert result["survival_probability"] < 0.5
    assert result["high_risk_day"] == "Saturday"

def test_trajectory_scoring_orchestrator():
    scoring = TrajectoryScoring()
    result = scoring.evaluate_trajectory(1, {"target_value": 15, "time_frame": "week", "goal_type": "Weekly Deep Work"}, {"hours_completed": 12, "days_elapsed": 5, "total_days": 7, "current_streak": 5}, "Saturday")
    assert result["trajectory_status"] == "On Track"
