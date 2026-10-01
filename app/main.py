from fastapi import Depends, FastAPI

from app.dependencies import get_current_user, require_admin
from app.schemas.questions import QuestionRequest, QuestionResponse
from app.services.question_service import QuestionService


class FakeLLM:

    async def generate(self, question: str) -> str:
        return f"Answer for: {question}"


llm = FakeLLM()


def get_question_service() -> QuestionService:
    return QuestionService(llm)


app = FastAPI(
    title="StudyHub API",
    version="1.0.0"
)


@app.post(
    "/questions",
    response_model=QuestionResponse,
    status_code=200
)
async def ask_question(
    request: QuestionRequest,
    user: dict = Depends(get_current_user)
):

    require_admin(user)

    service = get_question_service()

    answer = await service.answer_question(
        request.question
    )

    return QuestionResponse(
        question=request.question,
        answer=answer
    )
