from datetime import datetime

class VectorEmbedding:
    def __init__(self, id, user_id, document_type, content_text, embedding, created_at=None):
        self.id = id
        self.user_id = user_id
        self.document_type = document_type
        self.content_text = content_text
        self.embedding = embedding # List of floats
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'content_text': self.content_text,
            'embedding_preview': self.embedding[:5] if self.embedding else [], # preview
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
