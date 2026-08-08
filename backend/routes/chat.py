from fastapi import APIRouter

from backend.config import GEMINI_MODEL
from backend.gemini_client import client
from backend.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)

def chat(request: ChatRequest):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=request.message
    )

    return {
        "response": response.text
    }