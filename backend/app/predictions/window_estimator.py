from datetime import date, time, datetime
from typing import List, Dict, Any

class WindowEstimator:
    """Estimates optimal blocks based on Chronotype and historical day-of-week data."""
    
    def estimate(self, target_date: date, chronotype: str, sessions: List) -> List[Dict[str, Any]]:
        windows = []
        
        # Base heuristic depending on Chronotype
        if chronotype == "Early Peak Profile":
            # Morning Deep Work
            windows.append({
                "start_time": datetime.combine(target_date, time(8, 30)),
                "end_time": datetime.combine(target_date, time(11, 45)),
                "activity_type": "Deep Work"
            })
            # Afternoon dip usually around 14:00, second wind around 16:00
            windows.append({
                "start_time": datetime.combine(target_date, time(16, 0)),
                "end_time": datetime.combine(target_date, time(17, 30)),
                "activity_type": "Study"
            })
            # Identify dip explicitly (can be filtered or tagged by UI)
            windows.append({
                "start_time": datetime.combine(target_date, time(14, 0)),
                "end_time": datetime.combine(target_date, time(15, 30)),
                "activity_type": "Energy Dip"
            })
        elif chronotype == "Night Owl Profile":
            windows.append({
                "start_time": datetime.combine(target_date, time(14, 0)),
                "end_time": datetime.combine(target_date, time(17, 0)),
                "activity_type": "Deep Work"
            })
            windows.append({
                "start_time": datetime.combine(target_date, time(21, 0)),
                "end_time": datetime.combine(target_date, time(23, 30)),
                "activity_type": "Coding"
            })
        else:
            # Standard/Balanced
            windows.append({
                "start_time": datetime.combine(target_date, time(10, 0)),
                "end_time": datetime.combine(target_date, time(12, 0)),
                "activity_type": "Deep Work"
            })
            windows.append({
                "start_time": datetime.combine(target_date, time(15, 0)),
                "end_time": datetime.combine(target_date, time(17, 0)),
                "activity_type": "Deep Work"
            })
            
        return windows
