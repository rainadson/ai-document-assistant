"""Tests for the POST /upload endpoint."""

import io
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_upload_unsupported_extension_returns_400(client: TestClient) -> None:
    data = io.BytesIO(b"some content")
    response = client.post("/upload", files={"file": ("document.csv", data, "text/csv")})
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_txt_file_returns_success(client: TestClient) -> None:
    txt_content = b"This is a test document with some content for the RAG pipeline."

    with (
        patch("app.api.upload.load_document") as mock_load,
        patch("app.api.upload.split_documents") as mock_split,
        patch("app.api.upload.add_documents") as mock_add,
    ):
        from langchain_core.documents import Document

        mock_load.return_value = [Document(page_content="test", metadata={"source": "test.txt"})]
        mock_split.return_value = [Document(page_content="test", metadata={"source": "test.txt"})]
        mock_add.return_value = None

        response = client.post(
            "/upload",
            files={"file": ("test.txt", io.BytesIO(txt_content), "text/plain")},
        )

    assert response.status_code == 200
    assert response.json() == {"message": "Document processed successfully"}
