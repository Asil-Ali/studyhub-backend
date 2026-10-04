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


def test_ask_question_without_authentication():

    response = client.post(
        "/questions",
        json={
            "question": "What is RAG?"
        }
    )

    assert response.status_code == 401


def test_ask_question_as_regular_user():

    response = client.post(
        "/questions",
        headers={
            "Authorization": "Bearer user-token"
        },
        json={
            "question": "What is RAG?"
        }
    )

    assert response.status_code == 403


def test_ask_question_invalid_input():

    response = client.post(
        "/questions",
        headers={
            "Authorization": "Bearer admin-token"
        },
        json={
            "question": ""
        }
    )

    assert response.status_code == 422
