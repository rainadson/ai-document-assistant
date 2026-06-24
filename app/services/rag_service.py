"""RAG pipeline — retrieves context and generates answers via Groq."""

import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.services.vector_store import similarity_search

logger = logging.getLogger(__name__)

LLM_MODEL = "llama-3.1-8b-instant"

RAG_PROMPT_TEMPLATE = """\
Você é um assistente especializado em responder perguntas com base nos documentos fornecidos.

Regras:
- Utilize apenas as informações presentes no contexto.
- Não invente informações.
- Não faça suposições.
- Se a resposta não estiver presente no contexto, responda: "Não encontrei essa informação nos documentos."

Contexto:
{context}

Pergunta:
{question}

Resposta:"""


def _build_chain() -> object:
    """Construct the LangChain RAG chain (prompt → LLM → parser)."""
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    llm = ChatGroq(model=LLM_MODEL, temperature=0)
    return prompt | llm | StrOutputParser()


def answer_question(question: str) -> dict[str, str | list[str]]:
    """Run the full RAG pipeline for a user question.

    Args:
        question: The question to answer.

    Returns:
        Dictionary with 'answer' (str) and 'sources' (list[str]).

    Raises:
        RuntimeError: If the LLM call fails.
    """
    logger.info("Processing question: '%s'", question[:80])

    relevant_chunks = similarity_search(question)

    if not relevant_chunks:
        return {
            "answer": "Não encontrei essa informação nos documentos.",
            "sources": [],
        }

    context = "\n\n".join(doc.page_content for doc in relevant_chunks)
    sources = list({doc.metadata.get("source", "unknown") for doc in relevant_chunks})

    logger.info("Using %d chunks from sources: %s", len(relevant_chunks), sources)

    try:
        chain = _build_chain()
        answer: str = chain.invoke({"context": context, "question": question})
    except Exception as exc:
        logger.exception("LLM call failed")
        raise RuntimeError(f"Failed to generate answer: {exc}") from exc

    return {"answer": answer.strip(), "sources": sorted(sources)}
