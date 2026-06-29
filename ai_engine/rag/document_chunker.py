from typing import List, Dict, Any

class DocumentChunker:
    """
    Converts daily summaries, habits, and burnout warnings into semantic text chunks 
    suitable for vector embedding.
    """
    
    def chunk_behavior_data(self, behavior_record: Dict[str, Any]) -> List[str]:
        # Example logic: turn a JSON behavior record into a semantic sentence string
        chunks = []
        if "focus_score" in behavior_record:
            chunks.append(f"On {behavior_record.get('date', 'this day')}, the user had a focus score of {behavior_record['focus_score']} out of 100.")
            
        if "top_distraction" in behavior_record:
            chunks.append(f"The primary distraction was {behavior_record['top_distraction']}.")
            
        if "burnout_risk" in behavior_record:
            risk = behavior_record["burnout_risk"]
            chunks.append(f"Burnout risk was assessed at {risk}%.")
            
        # Real implementation might use LangChain or token splitters for large text
        return chunks
