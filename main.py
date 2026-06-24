"""Application entry point — configures FastAPI, logging, and mounts routers."""

import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.upload import router as upload_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="AI Document Assistant",
    description=(
        "Upload PDF, DOCX, or TXT documents and ask questions about them. "
        "Powered by LangChain, ChromaDB, and Groq (RAG architecture)."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, tags=["Documents"])
app.include_router(chat_router, tags=["Chat"])


@app.get("/health", tags=["Health"], summary="Health check")
async def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}
