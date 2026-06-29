from typing import List

class ConsistencyForecaster:
    """
    Maps historical drop-off points to forecast the probability of streak survival.
    """
    
    def forecast_survival(self, current_streak: int, historical_failures: List[int]) -> float:
        # historical_failures is a list of streak lengths where the user previously failed
        if not historical_failures:
            return 90.0 # High default probability if no failure history
            
        # Check how many times user survived past the current streak length
        survivals = sum(1 for failure in historical_failures if failure > current_streak)
        total_attempts = len(historical_failures)
        
        base_probability = (survivals / total_attempts) * 100
        
        # If user always breaks streak around this point, probability drops
        return max(10.0, min(95.0, base_probability))
