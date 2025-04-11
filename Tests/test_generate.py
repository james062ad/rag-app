# tests/test_generate.py

import sys
import os

# Add the parent directory to Python path to find 'main.py'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_endpoint():
    # Simulate a real user query
    response = client.post("/generate", json={
        "query": "What makes graphene effective as a corrosion-resistant coating?"
    })

    # Basic response check
    assert response.status_code == 200

    # Parse the response
    data = response.json()

    # Validate structure and expected content
    assert "answer" in data
    assert "matched_title" in data
    assert "similarity" in data
    assert "graphene" in data["matched_title"].lower() or "graphene" in data["answer"].lower()
