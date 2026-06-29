from typing import Dict, Any

class CourseCorrectionGenerator:
    """
    Provides AI recommendations to fix failing goals and course-correct.
    Designed to be queried directly as a tool by future AI Investigators.
    """
    
    def generate_correction(self, goal_status: str, deficit: float, macro_trends: list) -> Dict[str, Any]:
        if goal_status == "On Track":
            return {"action": "maintain", "message": "You are on track. Keep it up!"}
            
        # Example heuristic based on deficit
        if deficit > 5.0:
            return {
                "action": "drastic_correction",
                "message": f"Re-establish a strict morning block to recover {deficit:.1f} hours of deep work."
            }
        else:
            return {
                "action": "minor_correction",
                "message": f"You are slightly behind. Add an extra 30 minutes to your next session to recover {deficit:.1f} hours."
            }
