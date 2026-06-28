from .macro_trend_detector import MacroTrendDetector
from .goal_tracking_engine import GoalTrackingEngine
from .consistency_forecaster import ConsistencyForecaster
from .course_correction_generator import CourseCorrectionGenerator

class TrajectoryScoring:
    def __init__(self):
        self.trend_detector = MacroTrendDetector()
        self.goal_engine = GoalTrackingEngine()
        self.consistency_forecaster = ConsistencyForecaster()
        self.correction_generator = CourseCorrectionGenerator()

    def evaluate_trajectory(self, user_id, goal_data, current_activity, current_date=None, day_of_week="Monday"):
        trend_data = self.trend_detector.detect_macro_trend(user_id, current_date)
        
        goal_tracking = self.goal_engine.calculate_trajectory(
            target_value=goal_data.get("target_value", 15),
            time_frame=goal_data.get("time_frame", "week"),
            current_value=current_activity.get("hours_completed", 0),
            days_elapsed=current_activity.get("days_elapsed", 1),
            total_days=current_activity.get("total_days", 7)
        )
        
        consistency_data = self.consistency_forecaster.forecast_consistency(
            user_id=user_id,
            historical_streaks=[5, 6, 4, 7],
            current_streak=current_activity.get("current_streak", 3),
            current_day_of_week=day_of_week
        )
        
        correction = self.correction_generator.generate_correction(
            trajectory_status=goal_tracking["status"],
            trend_data=trend_data,
            goal_data=goal_data,
            deficit=goal_tracking.get("deficit", 0)
        )
        
        return {
            "trajectory_status": goal_tracking["status"],
            "trend_data": trend_data,
            "goal_tracking": goal_tracking,
            "consistency_forecast": consistency_data,
            "course_correction": correction
        }
