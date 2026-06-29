import pytest
from ai_engine.investigator.prompt_manager import PromptManager
from ai_engine.investigator.conversation_memory import ConversationMemory

def test_prompt_manager():
    manager = PromptManager()
    context = [{"text": "You watched YouTube."}]
    prompt = manager.build_prompt("Why am I distracted?", context)
    
    assert "You watched YouTube." in prompt
    assert "Why am I distracted?" in prompt
    assert "Autopsy AI" in prompt

def test_conversation_memory():
    memory = ConversationMemory()
    memory.append_interaction(1, "Hello", "Hi there")
    
    history = memory.get_history(1)
    assert len(history) == 1
    assert history[0]["query"] == "Hello"
    assert history[0]["response"] == "Hi there"
