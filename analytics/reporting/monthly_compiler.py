from typing import List, Dict, Any
from datetime import datetime
from .weekly_compiler import WeeklyCompiler

class MonthlyCompiler:
    """
    Rolls up daily/weekly metrics into a comprehensive monthly summary.
    Serves as the data source for high-level Monthly Intelligence Reports.
    """
    
    def compile(self, user_id: int, year: int, month: int, daily_metrics: List[Any]) -> Dict[str, Any]:
        if not daily_metrics:
            return {}
            
        total_deep_work = sum(getattr(m, 'deep_work_minutes', 0) for m in daily_metrics)
        avg_focus = sum(getattr(m, 'focus_score', 0) for m in daily_metrics) / len(daily_metrics)
        avg_productivity = sum(getattr(m, 'productivity_score', 0) for m in daily_metrics) / len(daily_metrics)
        
        return {
            "user_id": user_id,
            "period_type": "monthly",
            "period_start_date": datetime(year, month, 1),
            "period_end_date": datetime(year, month, 28), # simplified
            "average_productivity_score": avg_productivity,
            "average_focus_score": avg_focus,
            "total_deep_work_minutes": total_deep_work,
            "top_distraction_id": "Social Media", # Example extraction
            "delta_percentage_vs_previous": 0.0 
        }
