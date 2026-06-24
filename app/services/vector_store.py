"""ChromaDB vector store — persistence and similarity search."""

import logging
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.services.embeddings import get_embeddings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "documents"
VECTORDB_PATH = Path("data/vectordb")
TOP_K = 4


def _get_chroma() -> Chroma:
    """Build a Chroma client pointed at the local persistence directory."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(VECTORDB_PATH),
    )


def add_documents(chunks: list[Document]) -> None:
    """Embed and persist a list of document chunks to ChromaDB.

    Args:
        chunks: Chunked Document objects to store.
    """
    logger.info("Storing %d chunks in ChromaDB collection '%s'", len(chunks), COLLECTION_NAME)
    vectordb = _get_chroma()
    vectordb.add_documents(chunks)
    logger.info("Chunks stored successfully")


def similarity_search(query: str) -> list[Document]:
    """Retrieve the top-K most relevant chunks for a query.

    Args:
        query: The user question to search for.

    Returns:
        List of the most relevant Document chunks.
    """
    logger.info("Running similarity search (top-%d) for query: '%s'", TOP_K, query[:80])
    vectordb = _get_chroma()
    results = vectordb.similarity_search(query, k=TOP_K)
    logger.info("Retrieved %d chunks", len(results))
    return results
