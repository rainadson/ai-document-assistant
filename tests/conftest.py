"""Shared pytest fixtures."""

import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from main import app  # noqa: E402 — must come after env setup


@pytest.fixture()
def client() -> TestClient:
    """Return a synchronous FastAPI test client."""
    return TestClient(app)
