from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="StudyHub API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000
    )


@app.post("/questions")
async def ask_question(request: QuestionRequest):
    return {
        "question": request.question,
        "message": "Question received successfully"
    }
