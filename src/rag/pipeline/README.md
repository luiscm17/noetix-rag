# RAG Pipeline

Pipeline de procesamiento de documentos para indexación en Qdrant vector store.

## Uso

```python
from src.rag.pipeline import process_document_from_blob

process_document_from_blob("documento.pdf")
```

## Flujo

1. Descarga PDF desde Azure Blob Storage
2. Procesa con Docling (parsea a Markdown)
3. Aplica chunking con AgenticChunker (Microsoft Agent Framework)
4. Genera embeddings con Azure OpenAI (text-embedding-3-large)
5. Almacena en Qdrant

## Componentes

| Componente | Descripción |
|------------|-------------|
| `document_processor.py` | Docling PDF parser |
| `chunker.py` | AgenticChunker (Microsoft Agent Framework) |
| `embedding.py` | EmbeddingService (OpenAI SDK + Azure) |
| `vector_store.py` | Qdrant integration |
| `pipeline.py` | Orquestador del pipeline |

## Configuración

Ver `src/config/settings.py` para configuración centralizada:
- `AgentSettings`: Azure OpenAI endpoints y API keys
- `QdrantSettings`: Qdrant connection y vector size (3072)
- `ChunkingSettings`: Tamaño de chunks (max 800, min 200 tokens)

## Azure Function

Located at `src/rag/function/function_app.py` con blob trigger para procesamiento automático.
