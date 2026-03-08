from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Document:
    document_id: int
    title: str
    file_path: str
    page_count: int
    processed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[List[str]] = None


@dataclass
class DocumentChunk:
    id: int
    document_id: int
    content: str
    page_number: int
    bbox: Optional[List[int]] = None
    section: Optional[str] = None
    embedding: Optional[List[float]] = None
