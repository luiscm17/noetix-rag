import tempfile
from io import BytesIO
from pathlib import Path

from azure.storage.blob import BlobServiceClient
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    CodeFormulaVlmOptions,
    PdfPipelineOptions,
    PictureDescriptionApiOptions,
)
from docling.datamodel.pipeline_options_vlm_model import ResponseFormat
from docling.datamodel.stage_model_specs import ApiModelConfig, VlmModelSpec
from docling.datamodel.vlm_engine_options import ApiVlmEngineOptions
from docling.models.inference_engines.vlm.base import VlmEngineType
from docling_core.types.doc.base import ImageRefMode
from docling_core.types.io import DocumentStream
from pydantic import AnyHttpUrl

from src.config.settings import (
    AgentSettings,
    BlobStorageSettings,
    BlobStorageContainerSettings,
)


class DocumentProcessor:
    def __init__(self):
        BlobStorageSettings.validate()
        AgentSettings.openai_settings()

        conn_str = BlobStorageSettings.AZURE_STORAGE_CONNECTION_STRING
        assert conn_str is not None
        self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        self.converter = self._create_converter()

    def _create_converter(self) -> DocumentConverter:
        api_key = AgentSettings.OPENAI_API_KEY
        model_id = AgentSettings.OPENAI_MODEL_ID
        endpoint = AgentSettings.OPENAI_ENDPOINT
        assert api_key is not None
        assert model_id is not None
        assert endpoint is not None

        headers = {"Authorization": f"Bearer {api_key}"}

        form_model_spec = VlmModelSpec(
            name=model_id,
            default_repo_id=model_id,
            prompt="Extract formulas and code from the image.",
            response_format=ResponseFormat.DOCTAGS,
            max_new_tokens=4096,
            supported_engines={VlmEngineType.API},
            api_overrides={
                VlmEngineType.API: ApiModelConfig(params={"model": model_id})
            },
        )

        code_formula_options = CodeFormulaVlmOptions(
            model_spec=form_model_spec,
            engine_options=ApiVlmEngineOptions(
                engine_type=VlmEngineType.API,
                url=endpoint,
                timeout=120,
                temperature=0.1,
                headers=headers,
            ),
            scale=2.0,
            max_size=None,
            extract_code=True,
            extract_formulas=True,
        )

        picture_options = PictureDescriptionApiOptions(
            url=AnyHttpUrl(endpoint),
            headers=headers,
            prompt="Describe the content of the image in a few lines.",
            params={"model": model_id},
            timeout=120,
        )

        pipeline_options = PdfPipelineOptions(
            do_formula_enrichment=True,
            generate_page_images=True,
            generate_picture_images=True,
            images_scale=2,
            do_picture_classification=False,
            do_picture_description=True,
            picture_description_options=picture_options,
            enable_remote_services=True,
            code_formula_options=code_formula_options,
        )

        return DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    def process_pdf_from_azure(self, filename: str) -> str:
        blob_client = self.blob_service_client.get_blob_client(
            container=BlobStorageContainerSettings.DOCUMENTS_PDF_CONTAINER,
            blob=filename,
        )
        pdf_stream = blob_client.download_blob().readall()

        source = DocumentStream(name=filename, stream=BytesIO(pdf_stream))
        result = self.converter.convert(source)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            doc_filename = Path(filename).stem

            md_filename = temp_path / f"{doc_filename}.md"
            artifacts_dir = temp_path / f"{doc_filename}"

            result.document.save_as_markdown(
                md_filename,
                artifacts_dir=artifacts_dir,
                image_mode=ImageRefMode.REFERENCED,
                include_annotations=True,
            )

            self._upload_processed_files_to_azure(
                md_filename, artifacts_dir, doc_filename
            )

            markdown_content = md_filename.read_text(encoding="utf-8")

        return markdown_content

    def _upload_processed_files_to_azure(
        self, md_filename: Path, artifacts_dir: Path, doc_filename: str
    ):
        try:
            self.blob_service_client.create_container(
                BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER
            )
        except Exception:
            pass

        markdown_content = md_filename.read_text(encoding="utf-8")
        blob_md_client = self.blob_service_client.get_blob_client(
            container=BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER,
            blob=f"{doc_filename}.md",
        )
        blob_md_client.upload_blob(markdown_content, overwrite=True)

        if artifacts_dir.exists():
            for image_file in artifacts_dir.glob("*.png"):
                with open(image_file, "rb") as img_data:
                    blob_img_client = self.blob_service_client.get_blob_client(
                        container=BlobStorageContainerSettings.DOCUMENT_PROCESSED_CONTAINER,
                        blob=f"{doc_filename}/{image_file.name}",
                    )
                    blob_img_client.upload_blob(img_data, overwrite=True)
