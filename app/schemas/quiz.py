from pydantic import BaseModel, Field


class QuizRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class Question(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_index: int = Field(ge=0, le=3)
    explanation: str


class QuizResponse(BaseModel):
    questions: list[Question] = Field(min_length=1, max_length=10)