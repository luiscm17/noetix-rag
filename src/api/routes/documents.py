from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import uuid
from datetime import datetime
from src.domain.entities.document import Document
from src.infrastructure.repositories.document_repository_blob import (
    DocumentRepositoryBlob,
)

router = APIRouter()


def get_repo() -> DocumentRepositoryBlob:
    return DocumentRepositoryBlob()


@router.get("/")
async def list_documents(repo: DocumentRepositoryBlob = Depends(get_repo)):
    documents = repo.list_documents()
    return {"documents": documents}


@router.get("/{document_id}")
async def get_document(
    document_id: int, repo: DocumentRepositoryBlob = Depends(get_repo)
):
    """Get a document by its ID."""
    document = await repo.get_document(document_id)
    if document:
        return {"document": document}
    raise HTTPException(status_code=404, detail="Document not found")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), repo: DocumentRepositoryBlob = Depends(get_repo)
):
    """Upload a new document."""
    content = await file.read()
    filename = file.filename or f"document_{uuid.uuid4()}"
    document = Document(
        document_id=int(uuid.uuid4()),
        title=filename,
        file_path=filename,
        page_count=0,
        updated_at=datetime.now(),
    )
    await repo.save_document(document, content)
    return {
        "message": "Document uploaded successfully",
        "document_id": document.document_id,
    }
