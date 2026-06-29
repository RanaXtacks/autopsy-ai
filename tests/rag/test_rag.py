import pytest
from ai_engine.rag.document_chunker import DocumentChunker
from ai_engine.rag.local_embedder import LocalEmbedder

def test_document_chunker():
    chunker = DocumentChunker()
    record = {"date": "2026-07-01", "focus_score": 85, "top_distraction": "YouTube"}
    chunks = chunker.chunk_behavior_data(record)
    
    assert len(chunks) == 2
    assert "focus score of 85" in chunks[0]
    assert "YouTube" in chunks[1]

def test_local_embedder_mock():
    embedder = LocalEmbedder()
    vector = embedder.embed_text("Test query")
    assert len(vector) == 384
    assert vector[0] == 0.0
