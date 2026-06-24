"""POST /upload — receive a document, process it, and store embeddings."""

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.services.document_loader import load_document, split_documents
from app.services.vector_store import add_documents

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}
MAX_FILE_SIZE_MB = 20


@router.post(
    "/upload",
    summary="Upload and process a document",
    response_description="Confirmation that the document was processed successfully",
    status_code=status.HTTP_200_OK,
)
async def upload_document(file: UploadFile) -> dict[str, str]:
    """Accept a PDF, TXT, or DOCX file, chunk it, embed it, and persist to ChromaDB.

    Args:
        file: Multipart file uploaded by the user.

    Returns:
        JSON with a success message.

    Raises:
        HTTPException 400: Unsupported file type or file too large.
        HTTPException 500: Processing error.
    """
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{suffix}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destination = UPLOAD_DIR / (file.filename or "upload")

    content = await file.read()

    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds the {MAX_FILE_SIZE_MB} MB limit ({size_mb:.1f} MB received).",
        )

    destination.write_bytes(content)
    logger.info("Saved uploaded file to '%s' (%.2f MB)", destination, size_mb)

    try:
        documents = load_document(destination)
        chunks = split_documents(documents)
        add_documents(chunks)
    except (ValueError, RuntimeError) as exc:
        logger.exception("Document processing failed for '%s'", file.filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return {"message": "Document processed successfully"}
