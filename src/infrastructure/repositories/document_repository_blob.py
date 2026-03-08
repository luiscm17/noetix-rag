from typing import Optional, List
from azure.storage.blob import BlobServiceClient
from src.domain.entities.document import Document
from src.config.settings import StorageSettings


class DocumentRepositoryBlob:
    def __init__(
        self,
        connection_string: str | None = None,
        container_name: str | None = None,
    ):
        conn_str = connection_string or StorageSettings.AZURE_STORAGE_CONNECTION_STRING
        container = container_name or StorageSettings.AZURE_STORAGE_CONTAINER

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

    def save_document(self, document: Document, content: bytes) -> None:
        blob_name = f"{document.document_id}_{document.title}"
        self.container.upload_blob(name=blob_name, data=content, overwrite=True)

    def get_document(self, document_id: int) -> Optional[Document]:
        blobs = self.container.list_blobs()
        for blob in blobs:
            if blob.name.startswith(f"{document_id}_"):
                return Document(
                    document_id=document_id,
                    title=blob.name.split("_", 1)[1],
                    file_path=blob.name,
                    page_count=0,
                    processed_at=None,
                )
        return None

    def list_documents(self) -> List[Document]:
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
                        processed_at=None,
                    )
                )
        return documents
