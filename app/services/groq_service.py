
import logging

from groq import AsyncGroq, APITimeoutError, APIConnectionError, APIStatusError

from fastapi import HTTPException

from app.core.config import settings


logger = logging.getLogger(__name__)


# Create Groq client
if settings.GROQ_API_KEY is None:
    raise RuntimeError("GROQ_API_KEY is missing from environment configuration")

client = AsyncGroq(
    api_key=settings.GROQ_API_KEY.get_secret_value(),
    timeout=settings.GROQ_TIMEOUT_SECONDS
)


async def generate_answer(question: str) -> str:
    """
    Send a student's question to Groq and return the AI response.
    """

    try:
        response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CampusAssist AI, a helpful university student "
                        "support assistant. Give clear, accurate and beginner-friendly "
                        "answers. If you do not know something, say so honestly."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_completion_tokens=512
        )

        answer = response.choices[0].message.content

        return answer or "Sorry, I could not generate an answer."

    except APITimeoutError:
        logger.error("Groq API request timed out")

        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again."
        )

    except (APIConnectionError, APIStatusError):
        logger.exception("Groq API connection or provider error")

        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable. Please try again later."
        )
