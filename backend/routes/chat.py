from fastapi import APIRouter

from backend.config import GEMINI_MODEL
from backend.gemini_client import client
from backend.memory.conversation import add_message, get_history
from backend.schemas import ChatRequest, ChatResponse


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    add_message(request.session_id, "user", request.message)

    history = get_history(request.session_id)

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in history
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"""
Conversation history:
{history_text}

Respond to the latest user message naturally.
"""
    )

    add_message(request.session_id, "assistant", response.text)

    return {
        "response": response.text
    }