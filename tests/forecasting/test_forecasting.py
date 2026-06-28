import pytest
from datetime import datetime
from analytics.forecasting.productivity_forecaster import ProductivityForecaster

def test_productivity_forecaster_trajectory():
    forecaster = ProductivityForecaster()
    
    class MockScore:
        def __init__(self, score):
            self.score = score
            
    historical_scores = [MockScore(50), MockScore(60), MockScore(70)]
    active_habits = []
    
    forecast = forecaster.forecast_tomorrow(user_id=1, historical_scores=historical_scores, active_habits=active_habits)
    
    assert forecast["forecasted_productivity_score"] > 50
    assert forecast["trajectory_trend"] == "up"
