from typing import Protocol, List
from src.domain.entities.document import Document

class IDocumentRepository(Protocol):
    async def save_document(self,  document: Document, content: bytes) -> None:
        """Guarda un documento."""
        pass
    
    async def get_document(self, document_id: int) -> Document:
        """Retrieve a document by ID."""
        raise NotImplementedError("get_document must be implemented by concrete class")

    async def list_documents(self) -> List[Document]:
        """List all documents."""
        raise NotImplementedError("list_documents must be implemented by concrete class")