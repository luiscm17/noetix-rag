from typing import Protocol, List
from src.domain.entities.document import Document

class IDocumentRepository(Protocol):
    async def save_document(self,  document: Document, content: bytes) -> None:
        """Save a document."""
        ...
    
    async def get_document(self, document_id: int) -> Document:
        """Retrieve a document by ID."""
        ...

    async def list_documents(self) -> List[Document]:
        """List all documents."""
        ...
    
    # async def update_document(self, document: Document) -> Document:
    #     """Actualiza el estado de un documento."""
    #     pass

    # async def delete_document(self, document_id: int) -> bool:
    #     """Elimina un documento por ID."""
    #     pass