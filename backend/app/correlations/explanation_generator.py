class ExplanationGenerator:
    """Translates mathematical correlation data into natural language insights."""
    
    def generate(self, factor: str, outcome: str, strength: float, relationship_type: str) -> str:
        pct = int(abs(strength) * 100)
        
        factor_desc = factor.lower()
        
        if "Positive" in relationship_type:
            if "Strong" in relationship_type:
                return f"{factor} strongly correlates with higher {outcome} (+{pct}%)."
            return f"{factor} correlates with higher {outcome} (+{pct}%)."
            
        elif "Negative" in relationship_type:
            if "Strong" in relationship_type:
                return f"Warning: {factor} is strongly associated with lower {outcome} (-{pct}%)."
            return f"{factor} correlates with lower {outcome} (-{pct}%)."
            
        elif relationship_type == "Emerging Trend":
            direction = "higher" if strength > 0 else "lower"
            return f"Early pattern: {factor} may lead to {direction} {outcome}."
            
        else:
            return f"No significant relationship found between {factor_desc} and {outcome}."
