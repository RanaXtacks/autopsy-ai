from datetime import datetime

class ChatHistory:
    def __init__(self, id, user_id, query_text, ai_response, evidence_used, created_at=None):
        self.id = id
        self.user_id = user_id
        self.query_text = query_text
        self.ai_response = ai_response
        self.evidence_used = evidence_used # List or JSON array of vector IDs
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'query_text': self.query_text,
            'ai_response': self.ai_response,
            'evidence_used': self.evidence_used,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
