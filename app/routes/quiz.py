import os
from pathlib import Path

from fastapi import APIRouter
from openai import OpenAI

from app.schemas.quiz import QuizRequest, QuizResponse


PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "quiz-v1.md"

router = APIRouter()

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
)


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


@router.post("")
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

    system_prompt = load_prompt()

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": request.text,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content