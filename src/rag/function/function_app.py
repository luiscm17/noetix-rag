import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import azure.functions as func
import logging

from src.config.settings import BlobStorageContainerSettings
from src.rag.pipeline import process_document_from_blob

app = func.FunctionApp()


@app.blob_trigger(
    arg_name="myblob",
    path=f"{BlobStorageContainerSettings.DOCUMENTS_PDF_CONTAINER}/{{name}}",
    connection="AzureWebJobsStorage",
)
def process_document(myblob: func.InputStream, context: func.Context):
    logging.info(
        f"Python blob trigger function processed blob\n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )

    blob_name = myblob.name
    if not blob_name:
        logging.error("Blob name is None or empty")
        return

    file_name = blob_name.split("/")[-1]

    try:
        stored_count = process_document_from_blob(file_name)
        logging.info(
            f"Document {file_name} processed successfully. {stored_count} vectors stored."
        )
    except Exception as e:
        logging.error(f"Error processing document {file_name}: {str(e)}")
        raise
