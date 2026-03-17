from typing import Optional, List
from azure.storage.blob import BlobServiceClient
from src.domain.entities.document import Document
from src.config.settings import BlobStorageSettings


class DocumentRepositoryBlob:
    """Adapter: implement the contract of IDocumentRepository using Azure Blob Storage."""

    def __init__(
        self,
        connection_string: str | None = None,
        container_name: str | None = None,
    ):
        conn_str = (
            connection_string or BlobStorageSettings.AZURE_STORAGE_CONNECTION_STRING
        )
        container = container_name or BlobStorageSettings.AZURE_STORAGE_CONTAINER

        if not conn_str:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING is not configured")
        if not container:
            raise ValueError("AZURE_STORAGE_CONTAINER is not configured")

        self.blob_service = BlobServiceClient.from_connection_string(
            conn_str, api_version="2023-08-03"
        )
        self.container = self.blob_service.get_container_client(container)
        try:
            self.container.create_container()
        except Exception as e:
            print(f"Container already exists: {e}")

    def _get_blob_name(self, document: Document) -> str:
        """Generate blob name with user_id prefix."""
        user_id = document.user_id or 0
        return f"{user_id}_{document.document_id}_{document.title}"

    async def save_document(self, document: Document, content: bytes) -> None:
        """Save a document to Azure Blob Storage."""
        blob_name = self._get_blob_name(document)
        self.container.upload_blob(name=blob_name, data=content, overwrite=True)

    async def get_document(
        self, document_id: int, user_id: int | None = None
    ) -> Optional[Document]:
        """Retrieve a document by ID from Azure Blob Storage (filtered by user)."""
        blobs = self.container.list_blobs()
        for blob in blobs:
            parts = blob.name.split("_", 2)
            if len(parts) >= 2:
                try:
                    blob_user_id = int(parts[0])
                    blob_doc_id = int(parts[1])
                    if blob_doc_id == document_id:
                        if user_id is not None and blob_user_id != user_id:
                            continue
                        return Document(
                            document_id=blob_doc_id,
                            user_id=blob_user_id,
                            title=parts[2] if len(parts) > 2 else "",
                            file_path=blob.name,
                            page_count=0,
                        )
                except ValueError:
                    continue
        return None

    def list_documents(self, user_id: int | None = None) -> List[Document]:
        """List documents in Azure Blob Storage, optionally filtered by user."""
        blobs = self.container.list_blobs()
        documents = []
        for blob in blobs:
            parts = blob.name.split("_", 2)
            if len(parts) >= 2:
                try:
                    blob_user_id = int(parts[0])
                    if user_id is not None and blob_user_id != user_id:
                        continue
                    documents.append(
                        Document(
                            document_id=int(parts[1]),
                            user_id=blob_user_id,
                            title=parts[2] if len(parts) > 2 else "",
                            file_path=blob.name,
                            page_count=0,
                        )
                    )
                except ValueError:
                    continue
        return documents
