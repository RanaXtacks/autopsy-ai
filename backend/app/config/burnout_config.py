class BurnoutConfig:
    """Configurable weights for Burnout Risk Scoring (must sum to 1.0)"""
    
    WORKLOAD_WEIGHT = 0.30        # Deep work overload
    RECOVERY_WEIGHT = 0.25        # Lack of recovery sessions / sleep disruption
    FOCUS_DECLINE_WEIGHT = 0.20   # Decline in focus score
    CONTEXT_SWITCH_WEIGHT = 0.15  # Spikes in context switching
    VOLATILITY_WEIGHT = 0.10      # High variance in day-to-day productivity

    # Analysis window (days)
    ANALYSIS_WINDOW_DAYS = 14
