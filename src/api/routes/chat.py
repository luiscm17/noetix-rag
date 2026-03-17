from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.agents.orchestrator import get_response
from src.api.dependencies import get_current_user
from src.domain.entities.user import User

chat_router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@chat_router.post("/chat")
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """Chat endpoint with handoff orchestration. Requires authentication."""
    response = await get_response(
        request.message,
        session_id=request.session_id,
        user_id=current_user.user_id,
    )
    return {"response": response, "session_id": request.session_id}
