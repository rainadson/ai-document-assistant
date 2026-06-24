"""Document loading and text extraction for PDF, DOCX, and TXT files."""

import logging
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}


def load_document(file_path: Path) -> list[Document]:
    """Load a document from disk and return LangChain Document objects.

    Args:
        file_path: Absolute path to the file on disk.

    Returns:
        List of Document objects with page content and metadata.

    Raises:
        ValueError: If the file extension is not supported.
        RuntimeError: If loading fails.
    """
    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{suffix}'. Supported types: {SUPPORTED_EXTENSIONS}"
        )

    logger.info("Loading document: %s", file_path.name)

    try:
        if suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif suffix == ".docx":
            loader = Docx2txtLoader(str(file_path))
        else:
            loader = TextLoader(str(file_path), encoding="utf-8")

        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = file_path.name

        logger.info("Loaded %d page(s) from '%s'", len(documents), file_path.name)
        return documents

    except Exception as exc:
        logger.exception("Failed to load document '%s'", file_path.name)
        raise RuntimeError(f"Could not load document '{file_path.name}': {exc}") from exc


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks for embedding.

    Args:
        documents: List of Document objects to split.

    Returns:
        List of chunked Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    logger.info("Split into %d chunks", len(chunks))
    return chunks
