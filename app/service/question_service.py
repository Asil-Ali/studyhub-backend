class QuestionService:

    def __init__(self, llm):
        self.llm = llm

    async def answer_question(self, question: str) -> str:
        answer = await self.llm.generate(question)

        return answer
