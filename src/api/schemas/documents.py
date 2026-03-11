from pydantic import BaseModel, Field
from typing import Optional


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)


class DocumentResponse(BaseModel):
    document_id: int
    title: str
    file_path: str
    page_count: int

    class Config:
        from_attributes = True
