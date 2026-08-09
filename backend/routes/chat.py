from fastapi import APIRouter

from backend.config import GEMINI_MODEL
from backend.gemini_client import client
from backend.schemas import ChatRequest, ChatResponse

from backend.memory.conversation import add_message, get_history

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)

def chat(request: ChatRequest):
    add_message("user", request.message)
    history = get_history()
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
    add_message("assistant", response.text)

    return {
        "response": response.text
    }