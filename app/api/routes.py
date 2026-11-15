from app.services.groq_service import generate_answer
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.api.auth import verify_api_key
from app.core.rate_limiter import check_rate_limit
from app.core.config import settings


router = APIRouter()


# Request validation model
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


# Health endpoint
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


# Protected chat endpoint

@router.post("/chat")
async def chat(
    body: ChatRequest,
    request: Request,
    authenticated: bool = Depends(verify_api_key),
    rate_limited: bool = Depends(check_rate_limit)
):
    answer = await generate_answer(body.question)

    return {
        "message": "AI response generated successfully",
        "question": body.question,
        "answer": answer,
        "request_id": request.state.request_id
    }

