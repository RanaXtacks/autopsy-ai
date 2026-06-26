class RecoveryAdvisor:
    """Generates evidence-based suggestions to recover focus."""
    
    def generate(self, pattern_name: str, pattern_type: str) -> str:
        if "Before Work" in pattern_name:
            return "Try scheduling a 10-minute 'cool down' block before starting work, or use a website blocker."
        elif pattern_type == "Focus Disruption":
            return "Consider turning off notifications or using full-screen mode to prevent context switching."
        elif pattern_type == "Task Abandonment":
            return "Break tasks into smaller, 15-minute milestones to build momentum."
        elif pattern_type == "Circadian Disruption":
            return "Set a strict digital sunset rule at 10 PM to protect your sleep quality."
        return "Review your session timeline to identify exact distraction triggers."
