from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ask_question_success():

    response = client.post(
        "/questions",
        headers={
            "Authorization": "Bearer admin-token"
        },
        json={
            "question": "What is RAG?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What is RAG?"
    assert data["answer"] == "Answer for: What is RAG?"
