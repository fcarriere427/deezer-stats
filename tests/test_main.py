"""Tests for the main FastAPI application."""

from fastapi.testclient import TestClient

from deezer_stats import __version__
from deezer_stats.main import app

client = TestClient(app)


def test_root_returns_ok():
    """Test that root endpoint returns status ok."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == __version__


def test_health_returns_healthy():
    """Test that health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
