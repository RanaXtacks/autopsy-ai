from collections import defaultdict
from typing import List, Dict, Any
from app.models.sessions import BehaviorSession
from .habit_types import MAX_GAP_FOR_SEQUENCE_MINUTES

class PatternMiner:
    """Mines sequential patterns of behavior."""
    
    def mine_sequences(self, sessions: List[BehaviorSession]) -> List[Dict[str, Any]]:
        patterns = []
        if not sessions:
            return patterns
            
        sequences = defaultdict(int)
        
        # Sort sessions by time
        sorted_sessions = sorted([s for s in sessions if s.start_time], key=lambda x: x.start_time)
        
        # Find 2-grams (A -> B)
        for i in range(len(sorted_sessions) - 1):
            s1 = sorted_sessions[i]
            s2 = sorted_sessions[i+1]
            
            gap_minutes = (s2.start_time - s1.end_time).total_seconds() / 60.0
            if gap_minutes <= MAX_GAP_FOR_SEQUENCE_MINUTES:
                seq_key = f"{s1.session_type} -> {s2.session_type}"
                sequences[seq_key] += 1
                
        # Filter for frequent sequences
        for seq, count in sequences.items():
            if count >= 2: # Min threshold
                patterns.append({
                    'type': 'sequence',
                    'sequence': seq,
                    'frequency': count
                })
                
        return patterns
