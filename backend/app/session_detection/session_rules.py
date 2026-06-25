# Rule definitions for Session Types

SESSION_TYPES = {
    "DEEP_WORK": "Deep Work Session",
    "STUDY": "Study Session",
    "CODING": "Coding Session",
    "ENTERTAINMENT": "Entertainment Session",
    "MUSIC": "Music Session",
    "CONTEXT_SWITCHING": "Context Switching Session",
    "MIXED": "Mixed Activity Session"
}

def evaluate_rules(events, duration_minutes):
    """
    Evaluates a list of events against predefined rules to classify the session type.
    """
    categories = {}
    for event in events:
        cat = event.category or 'uncategorized'
        categories[cat] = categories.get(cat, 0) + 1
        
    total_events = len(events)
    if total_events == 0:
        return SESSION_TYPES["MIXED"]
        
    unique_categories = len(categories)
    dominant_category = max(categories, key=categories.get)
    dominant_ratio = categories[dominant_category] / total_events

    # Rule 1: Context Switching
    # High frequency of switching between multiple categories in a short time
    if unique_categories >= 3 and duration_minutes < 30 and dominant_ratio < 0.5:
        return SESSION_TYPES["CONTEXT_SWITCHING"]
        
    # Rule 2: Deep Work
    # Mostly learning/development, long duration, low switching
    work_events = categories.get('development', 0) + categories.get('learning', 0)
    work_ratio = work_events / total_events
    if work_ratio >= 0.7 and duration_minutes >= 20 and unique_categories <= 2:
        return SESSION_TYPES["DEEP_WORK"]

    # Rule 3: Coding specific
    if dominant_category == 'development' and dominant_ratio >= 0.6:
        return SESSION_TYPES["CODING"]
        
    # Rule 4: Study specific
    if dominant_category == 'learning' and dominant_ratio >= 0.6:
        return SESSION_TYPES["STUDY"]

    # Rule 5: Entertainment
    if dominant_category == 'entertainment' and dominant_ratio >= 0.6:
        return SESSION_TYPES["ENTERTAINMENT"]

    # Rule 6: Music
    if dominant_category == 'music' and dominant_ratio >= 0.6:
        return SESSION_TYPES["MUSIC"]

    return SESSION_TYPES["MIXED"]
