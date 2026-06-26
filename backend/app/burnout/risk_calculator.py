from app.config.burnout_config import BurnoutConfig

class RiskCalculator:
    """Ingests sub-analyzer data and computes the final risk score."""
    
    def calculate(self, workload_score: float, recovery_score: float, 
                  focus_decline: float, context_switch_score: float, 
                  volatility: float) -> tuple[float, str]:
        
        final_score = (
            (workload_score * BurnoutConfig.WORKLOAD_WEIGHT) +
            (recovery_score * BurnoutConfig.RECOVERY_WEIGHT) +
            (focus_decline * BurnoutConfig.FOCUS_DECLINE_WEIGHT) +
            (context_switch_score * BurnoutConfig.CONTEXT_SWITCH_WEIGHT) +
            (volatility * BurnoutConfig.VOLATILITY_WEIGHT)
        )
        
        final_score = min(100.0, max(0.0, final_score))
        
        # Determine risk level
        if final_score < 30.0:
            level = "Low"
        elif final_score < 60.0:
            level = "Moderate"
        elif final_score < 80.0:
            level = "High"
        else:
            level = "Critical"
            
        return final_score, level
