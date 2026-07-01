from analytics.trajectory.macro_trend_detector import MacroTrendDetector
from analytics.trajectory.goal_tracking_engine import GoalTrackingEngine
from analytics.trajectory.consistency_forecaster import ConsistencyForecaster
from analytics.trajectory.course_correction_generator import CourseCorrectionGenerator

class TrajectoryScoring:
    """
    Master orchestrator for the Behavioral Trajectory Engine.
    Combines macro trends, goal tracking, and consistency forecasting.
    """
    def __init__(self):
        self.trend_detector = MacroTrendDetector()
        self.goal_tracker = GoalTrackingEngine()
        self.consistency_forecaster = ConsistencyForecaster()
        self.course_corrector = CourseCorrectionGenerator()

    def evaluate_trajectory(self, user_id, goal_data, current_activity):
        # 1. Detect Macro Trends
        trend_data = self.trend_detector.detect_macro_trend(user_id)
        
        # 2. Evaluate active goal trajectory
        goal_tracking = self.goal_tracker.evaluate_run_rate(goal_data, current_activity)
        
        # 3. Forecast consistency survival probability
        consistency_forecast = self.consistency_forecaster.forecast_survival_probability(
            user_id, 
            current_activity.get('current_streak', 0)
        )
        
        # Determine trajectory status
        trajectory_status = "On Track"
        if goal_tracking.get('required_run_rate', 0) > goal_tracking.get('current_run_rate', 0) * 1.5:
            trajectory_status = "Failing"
        elif goal_tracking.get('required_run_rate', 0) > goal_tracking.get('current_run_rate', 0):
            trajectory_status = "At Risk"

        # 4. Generate course correction
        course_correction = self.course_corrector.generate_correction(
            trajectory_status, 
            trend_data.get('trend_type')
        )
        
        return {
            "trajectory_status": trajectory_status,
            "goal_tracking": goal_tracking,
            "consistency_forecast": consistency_forecast,
            "course_correction": course_correction,
            "trend_data": trend_data
        }
