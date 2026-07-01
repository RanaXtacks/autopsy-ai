#pyrefly: ignore [missing-import]
from fastapi import APIRouter
#pyrefly: ignore [missing-import]
from pydantic import BaseModel

# This is the variable that main.py is looking for!
router = APIRouter()

# Define what the frontend will send to the backend
class ChatRequest(BaseModel):
    message: str

@router.post("/message")
async def chat_with_ai(request: ChatRequest):
    # This is a placeholder until we connect the actual RAG/LLM logic
    return {
        "response": f"AI Investigator received: '{request.message}'. (Vector database connection pending...)"
    }

@router.get("/history")
async def get_chat_history():
    # Placeholder for chat history
    return {"history": []}