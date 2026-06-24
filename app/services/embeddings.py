"""HuggingFace embeddings — runs locally, no API key required."""

import logging
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Return a cached HuggingFaceEmbeddings instance.

    The model is downloaded automatically on first use (~90 MB).

    Returns:
        Configured HuggingFaceEmbeddings using all-MiniLM-L6-v2.
    """
    logger.info("Initialising HuggingFace embeddings with model '%s'", EMBEDDING_MODEL)
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
