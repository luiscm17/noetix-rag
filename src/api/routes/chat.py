from fastapi import APIRouter
from pydantic import BaseModel

from src.agents.orchestrator import get_response

chat_router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@chat_router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with handoff orchestration."""
    response = await get_response(request.message)
    return {"response": response, "session_id": request.session_id}
