import asyncio
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.main import app
from app.services.question_service import QuestionService


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

    data = response.json()

    assert data["detail"] == "Authentication required"


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

    data = response.json()

    assert data["detail"] == "Admin permission required"


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


def test_question_service_with_mock():

    mock_llm = AsyncMock()

    mock_llm.generate.return_value = "Mocked answer"

    service = QuestionService(mock_llm)

    result = asyncio.run(
        service.answer_question(
            "What is RAG?"
        )
    )

    assert result == "Mocked answer"

    mock_llm.generate.assert_awaited_once_with(
        "What is RAG?"
    )


def test_api_with_overridden_dependency():

    mock_llm = AsyncMock()

    mock_llm.generate.return_value = "Mock API answer"

    mock_service = QuestionService(mock_llm)

    def override_question_service():
        return mock_service

    from app.main import get_question_service

    app.dependency_overrides[
        get_question_service
    ] = override_question_service

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

    assert data["answer"] == "Mock API answer"

    mock_llm.generate.assert_awaited_once_with(
        "What is RAG?"
    )

    app.dependency_overrides.clear()
