from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"


class Document(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    document_id: Optional[int] = Field(default=None, description="Document ID")
    title: str = Field(..., min_length=4, max_length=255, description="Document title")
    file_path: str = Field(..., description="File path")
    page_count: int = Field(0, ge=0, description="Number of pages")
    created_at: Optional[datetime] = Field(default=None, description="Created at")
    updated_at: Optional[datetime] = Field(default=None, description="Updated at")
    tags: Optional[List[str]] = Field(default=None, description="Tags")
    status: DocumentStatus = Field(
        default=DocumentStatus.PENDING, description="Document status"
    )
    error_message: Optional[str] = Field(default=None, description="Error message")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        return v
