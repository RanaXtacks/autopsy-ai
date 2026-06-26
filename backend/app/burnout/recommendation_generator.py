from typing import List

class RecommendationGenerator:
    """Generates actionable recovery suggestions based on identified risk factors."""
    
    def generate(self, factors: List[str]) -> List[str]:
        actions = []
        
        if any("Deep work volume" in f for f in factors):
            actions.append("Schedule a mandatory 24-hour disconnect window this weekend.")
            
        if any("Recovery-related activity is below" in f for f in factors):
            actions.append("Add at least one 30-minute low-cognition activity (reading, walking) to your evening routine.")
            
        if any("Focus score has decreased" in f for f in factors):
            actions.append("Reduce task batching. Focus on a single priority item before lunch.")
            
        if any("Context switching" in f for f in factors):
            actions.append("Utilize full-screen mode and close background applications during Deep Work.")
            
        if not actions:
            actions.append("Maintain your current balance; workload and recovery are in harmony.")
            
        return actions
