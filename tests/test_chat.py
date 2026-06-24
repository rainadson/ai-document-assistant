"""Tests for the POST /ask endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient


def test_ask_returns_answer_and_sources(client: TestClient) -> None:
    mock_result = {
        "answer": "O prazo de cancelamento é de 7 dias.",
        "sources": ["contrato.pdf"],
    }

    with patch("app.api.chat.answer_question", return_value=mock_result):
        response = client.post("/ask", json={"question": "Qual é o prazo de cancelamento?"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == mock_result["answer"]
    assert body["sources"] == mock_result["sources"]


def test_ask_empty_question_returns_422(client: TestClient) -> None:
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422


def test_ask_missing_body_returns_422(client: TestClient) -> None:
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_propagates_runtime_error_as_500(client: TestClient) -> None:
    with patch("app.api.chat.answer_question", side_effect=RuntimeError("LLM error")):
        response = client.post("/ask", json={"question": "Alguma pergunta?"})

    assert response.status_code == 500
    assert "LLM error" in response.json()["detail"]
