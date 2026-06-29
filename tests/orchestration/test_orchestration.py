import pytest
from api.orchestration.intelligence_layer_v1 import IntelligenceLayerV1
from api.orchestration.caching_strategy import CachingStrategy

def test_intelligence_layer_caching():
    layer = IntelligenceLayerV1()
    state1 = layer.get_unified_state(user_id=1)
    
    # Verify cache was hit on second call
    assert layer.caching.get("intelligence_state_v1_1") is not None
    
    layer.caching.invalidate(user_id=1)
    assert layer.caching.get("intelligence_state_v1_1") is None
