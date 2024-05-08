from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_text():
    response = client.post("/generate_text/", json={
        "prompt": "explain the data in plain english",
        "max_tokens": 5
    })
    assert response.status_code == 200
    assert "response" in response.json()
