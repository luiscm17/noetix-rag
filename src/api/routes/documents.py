from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import uuid
from datetime import datetime
from src.domain.entities.document import Document
from src.infrastructure.repositories.document_repository_blob import (
    DocumentRepositoryBlob,
)
from src.api.dependencies import get_current_user
from src.domain.entities.user import User

router = APIRouter()


def get_repo() -> DocumentRepositoryBlob:
    return DocumentRepositoryBlob()


@router.get("/")
async def list_documents(
    current_user: User = Depends(get_current_user),
    repo: DocumentRepositoryBlob = Depends(get_repo),
):
    """List documents for the authenticated user."""
    documents = repo.list_documents(user_id=current_user.user_id)
    return {"documents": documents}


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    repo: DocumentRepositoryBlob = Depends(get_repo),
):
    """Get a document by its ID (only if owned by current user)."""
    document = await repo.get_document(document_id, user_id=current_user.user_id)
    if document:
        return {"document": document}
    raise HTTPException(status_code=404, detail="Document not found")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    repo: DocumentRepositoryBlob = Depends(get_repo),
):
    """Upload a new document for the authenticated user."""
    content = await file.read()
    filename = file.filename or f"document_{uuid.uuid4()}"
    document = Document(
        document_id=int(uuid.uuid4()),
        title=filename,
        file_path=filename,
        page_count=0,
        updated_at=datetime.now(),
        user_id=current_user.user_id,
    )
    await repo.save_document(document, content)
    return {
        "message": "Document uploaded successfully",
        "document_id": document.document_id,
    }
