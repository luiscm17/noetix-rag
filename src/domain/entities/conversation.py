from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Conversation:
    user_id: int
    document_id: int
    conversation_id: str
    title: str = "Untitled Conversation"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Message:
    message_id: int
    conversation_id: str
    role: str
    content: str
    created_at: Optional[datetime] = None