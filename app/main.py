from fastapi import FastAPI
from app.schemas.questions import QuestionRequest, QuestionResponse


app = FastAPI(
    title="StudyHub API",
    version="1.0.0"
)


@app.post(
    "/questions",
    response_model=QuestionResponse,
    status_code=200
)
async def ask_question(request: QuestionRequest):

    return QuestionResponse(
        question=request.question,
        answer="This is a temporary answer."
    )
