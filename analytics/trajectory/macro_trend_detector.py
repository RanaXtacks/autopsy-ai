from datetime import datetime, timedelta

class MacroTrendDetector:
    def __init__(self):
        # We simulate a caching mechanism for 30-day aggregations to avoid heavy DB polling
        self.aggregation_cache = {}

    def detect_macro_trend(self, user_id, current_date=None):
        """
        Detects macro shifts in behavior using rolling 14-day and 30-day windows.
        Examples: Chronotype Shift, Dopamine Loop
        """
        if not current_date:
            current_date = datetime.utcnow()
            
        # Simulate fetching data for windows (in a real app, this would query a db/cache)
        fourteen_day_window = self._get_cached_or_query(user_id, current_date, days=14)
        thirty_day_window = self._get_cached_or_query(user_id, current_date, days=30)
        
        # Trend analysis logic
        trend_type = self._analyze_shifts(fourteen_day_window, thirty_day_window)
        
        return {
            "trend_type": trend_type,
            "analysis_window": "30-day vs 14-day rolling",
            "detected_at": current_date.isoformat()
        }

    def _get_cached_or_query(self, user_id, current_date, days):
        cache_key = f"{user_id}_{days}_{current_date.strftime('%Y%m%d')}"
        if cache_key in self.aggregation_cache:
            return self.aggregation_cache[cache_key]
            
        # Mocking window data aggregation
        if days == 14:
            data = {"late_night_activity_ratio": 0.65, "morning_focus_ratio": 0.20}
        else:
            data = {"late_night_activity_ratio": 0.20, "morning_focus_ratio": 0.70}
            
        self.aggregation_cache[cache_key] = data
        return data

    def _analyze_shifts(self, short_term, long_term):
        if short_term.get("late_night_activity_ratio", 0) > long_term.get("late_night_activity_ratio", 0) * 1.5:
            if short_term.get("morning_focus_ratio", 1) < long_term.get("morning_focus_ratio", 1) * 0.5:
                return "Chronotype Shift: Morning focus dropping, shifting to low-quality evening work."
                
        return "Stable"
