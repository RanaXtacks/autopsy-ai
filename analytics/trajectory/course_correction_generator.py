class CourseCorrectionGenerator:
    def __init__(self):
        pass

    def generate_correction(self, trajectory_status, trend_data, goal_data, deficit=0):
        if trajectory_status == "On Track":
            return "Keep it up. No course correction needed."

        trend_type = trend_data.get("trend_type", "")
        
        if "Chronotype Shift" in trend_type:
            if goal_data.get("goal_type") == "Weekly Deep Work":
                return f"Re-establish 9 AM coding block to recover {deficit:.1f} hours."
                
        if "Dopamine Loop" in trend_type:
            return "Block distracting sites during work hours. You are context switching too often."
            
        return "Increase daily output slightly to get back on track."
