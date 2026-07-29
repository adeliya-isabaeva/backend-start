import pytest
from fastapi.testclient import TestClient
from main import app  # импортируем приложение из main.py

client = TestClient(app)

def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
