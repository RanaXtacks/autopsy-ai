from typing import Dict, Any
from .payload_optimizer import PayloadOptimizer
from .caching_strategy import CachingStrategy

class IntelligenceLayerV1:
    """
    The God-Endpoint orchestration layer.
    Aggregates habits, trajectory, burnout risk, and prescriptions into one minimal, 
    fast JSON payload for the frontend MVP dashboard.
    """
    
    def __init__(self):
        self.payload_optimizer = PayloadOptimizer()
        self.caching = CachingStrategy()
        
    def get_unified_state(self, user_id: int) -> Dict[str, Any]:
        cache_key = f"intelligence_state_v1_{user_id}"
        
        # Check Cache
        cached_payload = self.caching.get(cache_key)
        if cached_payload:
            return cached_payload
            
        # Simulate fetching data from various engines (Days 1-29)
        raw_state = {
            "archetype": {
                "primary": "Deep Worker",
                "secondary": "Night Owl",
                "risk_profile": "High Context Switcher"
            },
            "segmentation": "Your current 7-day behavior closely matches your 'Finals Week Overload' segment from last semester.",
            "burnout_risk": 75,
            "focus_average": 82,
            "trajectory_status": "At Risk",
            "prescriptions": [
                "Re-establish 9 AM coding block to recover 3 hours."
            ]
        }
        
        # Optimize Payload
        optimized_payload = self.payload_optimizer.optimize(raw_state)
        
        # Cache Payload
        self.caching.set(cache_key, optimized_payload)
        
        return optimized_payload
