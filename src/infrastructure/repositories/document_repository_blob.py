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

    async def save_document(self, document: Document, content: bytes) -> None:
        """Save a document to Azure Blob Storage."""
        blob_name = f"{document.document_id}_{document.title}"
        self.container.upload_blob(name=blob_name, data=content, overwrite=True)

    async def get_document(self, document_id: int) -> Optional[Document]:
        """Retrieve a document by ID from Azure Blob Storage."""
        blobs = self.container.list_blobs()
        for blob in blobs:
            if blob.name.startswith(f"{document_id}_"):
                return Document(
                    document_id=document_id,
                    title=blob.name.split("_", 1)[1],
                    file_path=blob.name,
                    page_count=0,
                )
        return None

    def list_documents(self) -> List[Document]:
        """List all documents in Azure Blob Storage."""
        blobs = self.container.list_blobs()
        documents = []
        for blob in blobs:
            if "_" in blob.name:
                documents.append(
                    Document(
                        document_id=int(blob.name.split("_")[0]),
                        title=blob.name.split("_", 1)[1],
                        file_path=blob.name,
                        page_count=0,
                    )
                )
        return documents

    async def update_document(self, document: Document) -> Optional[Document]:
        """Update a document in Azure Blob Storage."""
        blob_name = f"{document.document_id}_{document.title}"
        blob_client = self.container.get_blob_client(blob_name)
        if not blob_client.exists():
            return None

        blobs = self.container.list_blobs()
        for blob in blobs:
            if blob.name.startswith(f"{document.document_id}_"):
                old_blob = self.container.get_blob_client(blob.name)
                content = old_blob.download_blob().readall()
                old_blob.delete_blob()
                blob_client.upload_blob(data=content, overwrite=True)
                break

        return Document(
            document_id=document.document_id,
            title=document.title,
            file_path=blob_name,
            page_count=0,
        )

    async def delete_document(self, document_id: int) -> bool:
        """Delete a document from Azure Blob Storage."""
        blobs = self.container.list_blobs()
        for blob in blobs:
            if blob.name.startswith(f"{document_id}_"):
                blob_client = self.container.get_blob_client(blob.name)
                blob_client.delete_blob()
                return True
        return False
