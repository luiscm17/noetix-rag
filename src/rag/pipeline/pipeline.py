from src.rag.pipeline.document_processor import DocumentProcessor
from src.rag.pipeline.chunker import DocumentChunker
from src.rag.pipeline.vector_store import VectorStore


def process_document_from_blob(blob_name: str) -> int:
    processor = DocumentProcessor()
    chunker = DocumentChunker()
    vector_store = VectorStore()

    markdown = processor.process_pdf_from_azure(blob_name)

    doc_md = f"{blob_name.rsplit('.', 1)[0]}.md"
    chunks = chunker.chunk_document(doc_md)

    return vector_store.vectorize_and_store_chunks(chunks)
