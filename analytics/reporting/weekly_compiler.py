from typing import List, Dict, Any
from datetime import datetime, timedelta

class WeeklyCompiler:
    """
    Compiles daily sessions, focus scores, and habits into heavy weekly summaries.
    Designed to run via a scheduled cron job to avoid heavy on-the-fly calculation.
    """
    
    def compile(self, user_id: int, start_date: datetime, end_date: datetime, daily_metrics: List[Any]) -> Dict[str, Any]:
        if not daily_metrics:
            return {}
            
        total_deep_work = sum(getattr(m, 'deep_work_minutes', 0) for m in daily_metrics)
        avg_focus = sum(getattr(m, 'focus_score', 0) for m in daily_metrics) / len(daily_metrics)
        avg_productivity = sum(getattr(m, 'productivity_score', 0) for m in daily_metrics) / len(daily_metrics)
        
        # Determine top distraction (mocking logic for example)
        distractions = {}
        for m in daily_metrics:
            dist = getattr(m, 'top_distraction', None)
            if dist:
                distractions[dist] = distractions.get(dist, 0) + 1
        
        top_distraction = max(distractions, key=distractions.get) if distractions else None
        
        return {
            "user_id": user_id,
            "period_type": "weekly",
            "period_start_date": start_date,
            "period_end_date": end_date,
            "average_productivity_score": avg_productivity,
            "average_focus_score": avg_focus,
            "total_deep_work_minutes": total_deep_work,
            "top_distraction_id": top_distraction,
            "delta_percentage_vs_previous": 0.0 # Will be populated by ComparativeEngine
        }
