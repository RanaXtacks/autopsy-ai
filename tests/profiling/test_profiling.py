import pytest
from analytics.profiling.archetype_classifier import ArchetypeClassifier
from analytics.profiling.behavior_segmentation import BehaviorSegmentation

class MockDailyMetric:
    def __init__(self, deep_work, late_night):
        self.deep_work_minutes = deep_work
        self.is_late_night = late_night

def test_archetype_classifier_deep_worker():
    classifier = ArchetypeClassifier()
    # Average of 4 hours (240 min) deep work per day over 2 days
    data = [MockDailyMetric(240, False), MockDailyMetric(240, False)]
    result = classifier.classify(data)
    assert result["primary"] == "Deep Worker"
    assert result["secondary"] == "Early Bird"

def test_archetype_classifier_night_owl():
    classifier = ArchetypeClassifier()
    # Low deep work, high late night
    data = [MockDailyMetric(60, True), MockDailyMetric(60, True)]
    result = classifier.classify(data)
    assert result["primary"] == "Standard Worker"
    assert result["secondary"] == "Night Owl"
