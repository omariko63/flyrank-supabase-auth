import os
from fastapi import APIRouter
from app.schemas.quiz import QuizResponse, QuizRequest

router = APIRouter()

@router.post("", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    if os.getenv("LLM_STUB") == "1":
        return {
            "questions": [
                {
                    "question": "What year did the event described in the text occur?",
                    "options": [
                        "1939",
                        "1940",
                        "1941",
                        "1942"
                    ],
                    "correct_index": 0,
                    "explanation": "The stub response is used for testing."
                }
            ]
        }

