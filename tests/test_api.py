"""Tests for FastAPI endpoints."""
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_stats():
    r = client.get("/stats")
    assert r.status_code == 200
    j = r.json()
    assert "total" in j
    assert "pass_count" in j
    assert "fail_count" in j


def test_results():
    r = client.get("/results")
    assert r.status_code == 200
    j = r.json()
    assert "items" in j
    assert "total" in j


def test_inspect_no_file():
    r = client.post("/inspect")
    assert r.status_code == 422  # missing file
