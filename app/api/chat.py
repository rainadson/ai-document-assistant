"""POST /ask — answer a question using the RAG pipeline."""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.ask_request import AskRequest
from app.schemas.ask_response import AskResponse
from app.services.rag_service import answer_question

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask a question about the uploaded documents",
    response_description="Generated answer with source references",
    status_code=status.HTTP_200_OK,
)
async def ask(request: AskRequest) -> AskResponse:
    """Retrieve relevant document chunks and generate an answer with OpenAI.

    Args:
        request: JSON body containing the user question.

    Returns:
        AskResponse with the answer and list of source filenames.

    Raises:
        HTTPException 500: If the RAG pipeline fails.
    """
    logger.info("Received question: '%s'", request.question[:80])

    try:
        result = answer_question(request.question)
    except RuntimeError as exc:
        logger.exception("RAG pipeline error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return AskResponse(answer=result["answer"], sources=result["sources"])
