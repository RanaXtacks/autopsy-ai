import pytest
from analytics.reporting.comparative_engine import ComparativeEngine
from analytics.reporting.baseline_shifter import BaselineShifter

def test_comparative_engine_deltas():
    engine = ComparativeEngine()
    prev = {"average_focus_score": 50.0, "total_deep_work_minutes": 100.0}
    curr = {"average_focus_score": 75.0, "total_deep_work_minutes": 80.0}
    
    deltas = engine.calculate_deltas(curr, prev)
    
    assert deltas["focus_delta"] == 50.0 # 50 to 75 is +50%
    assert deltas["deep_work_delta"] == -20.0 # 100 to 80 is -20%

def test_baseline_shifter():
    shifter = BaselineShifter()
    # Test a minor fluctuation
    result = shifter.detect_shift(50.0, 52.0)
    assert not result["has_shifted"]
    
    # Test a major shift
    result = shifter.detect_shift(50.0, 60.0)
    assert result["has_shifted"]
    assert result["shift_value"] == 10.0
