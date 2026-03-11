from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import uuid
from datetime import datetime
from src.domain.entities.document import Document
from src.infrastructure.repositories.document_repository_blob import (
    DocumentRepositoryBlob,
)
from src.api.schemas.documents import DocumentUpdate, DocumentResponse


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


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    request: DocumentUpdate,
    repo: DocumentRepositoryBlob = Depends(get_repo),
):
    """Update document metadata."""
    existing = await repo.get_document(document_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Document not found")

    updated_doc = Document(
        document_id=document_id,
        title=request.title or existing.title,
        file_path=existing.file_path,
        page_count=existing.page_count,
        updated_at=datetime.now(),
    )
    result = await repo.update_document(updated_doc)
    if not result or result.document_id is None:
        raise HTTPException(status_code=500, detail="Failed to update document")
    return DocumentResponse(
        document_id=result.document_id,  # type: ignore[arg-type]
        title=result.title,
        file_path=result.file_path,
        page_count=result.page_count,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    repo: DocumentRepositoryBlob = Depends(get_repo),
):
    """Delete a document."""
    existing = await repo.get_document(document_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Document not found")

    deleted = await repo.delete_document(document_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete document")
