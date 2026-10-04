import pytest

from app.main import FakeLLM
from app.services.question_service import QuestionService


@pytest.fixture
def service():
    fake_llm = FakeLLM()

    return QuestionService(fake_llm)
