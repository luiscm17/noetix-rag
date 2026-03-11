from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class DocumentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"



@dataclass
class Document:
    document_id: int
    title: str
    file_path: str
    page_count: int
    processed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    status: DocumentStatus = DocumentStatus.PENDING
    error_message: Optional[str] = None


@dataclass
class DocumentChunk:
    id: int
    document_id: int
    content: str
    page_number: int
    bbox: Optional[List[int]] = None
    section: Optional[str] = None
    embedding: Optional[List[float]] = None
