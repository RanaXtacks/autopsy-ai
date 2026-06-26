from typing import List, Dict, Any

class TimeLossEstimator:
    """Aggregates and estimates total time lost for specific patterns."""
    
    def estimate(self, raw_patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Group patterns by pattern_name to aggregate time lost and frequency
        aggregated = {}
        
        for p in raw_patterns:
            name = p['pattern_name']
            if name not in aggregated:
                aggregated[name] = p.copy()
            else:
                aggregated[name]['frequency'] += p['frequency']
                aggregated[name]['time_lost_mins'] += p['time_lost_mins']
                
        return list(aggregated.values())
