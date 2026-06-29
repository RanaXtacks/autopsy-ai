from typing import List, Dict, Any

class MacroTrendDetector:
    """
    Detects macro shifts in behavior using rolling 14-day and 30-day windows.
    Analyzes long-term trends like Chronotype Shifts or Baseline Screen Time changes.
    """
    
    def detect_trends(self, recent_data: List[Any], baseline_data: List[Any]) -> List[Dict[str, Any]]:
        # Dummy heuristic for macro trend detection
        trends = []
        
        # E.g. Compare last 14 days vs previous 30 days
        # Simulate detecting a shift
        late_night_recent = sum(1 for d in recent_data if getattr(d, 'is_late_night', False))
        late_night_baseline = sum(1 for d in baseline_data if getattr(d, 'is_late_night', False))
        
        # Prevent division by zero
        baseline_rate = (late_night_baseline / len(baseline_data)) if baseline_data else 0
        recent_rate = (late_night_recent / len(recent_data)) if recent_data else 0
        
        if recent_rate > baseline_rate * 1.3:
            trends.append({
                "trend_type": "Chronotype Shift",
                "description": f"You are shifting to a night owl. 14-day trend shows +{(recent_rate-baseline_rate)*100:.0f}% late-night activity.",
                "severity": "high"
            })
            
        return trends
