class ConsistencyForecaster:
    def __init__(self):
        pass

    def forecast_consistency(self, user_id, historical_streaks, current_streak, current_day_of_week):
        drop_off_probabilities = {
            "Monday": 0.05,
            "Tuesday": 0.05,
            "Wednesday": 0.10,
            "Thursday": 0.15,
            "Friday": 0.30,
            "Saturday": 0.65,
            "Sunday": 0.40
        }
        
        risk_today = drop_off_probabilities.get(current_day_of_week, 0.1)
        survival_probability = max(0.0, 1.0 - risk_today)
        
        avg_streak_length = sum(historical_streaks) / len(historical_streaks) if historical_streaks else 7
        if current_streak > avg_streak_length:
            survival_probability *= 0.8
            
        return {
            "survival_probability": round(survival_probability, 2),
            "high_risk_day": "Saturday" if survival_probability < 0.5 else None,
            "forecast_message": f"{int(survival_probability * 100)}% probability of maintaining current streak based on historical drop-offs."
        }
