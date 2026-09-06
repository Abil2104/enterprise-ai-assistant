from fastapi import APIRouter, HTTPException
from google.genai import types

from backend.config import GEMINI_MODEL
from backend.gemini_client import client
from backend.memory.conversation import add_message, get_history
from backend.schemas import ChatRequest, ChatResponse
from backend.prompts import SYSTEM_PROMPT

from backend.tools.business_tools import (
    get_customer_risk_summary,
    get_customer_business_metrics,
    get_highest_outstanding_customer,
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    # Save user message
    add_message(
        request.session_id,
        "user",
        request.message
    )

    # Retrieve conversation history
    history = get_history(request.session_id)

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in history
    )

    prompt = f"""
{SYSTEM_PROMPT}

You have access to multiple business-data tools.

Available tools:

1. customer risk summary
   - Use this to identify customers with high risk scores.

2. customer business metrics
   - Use this for overall customer counts, outstanding balances,
     high-risk exposure, and average risk score.

3. highest outstanding customer
   - Use this to identify the customer with the largest
     outstanding amount.

Use the appropriate business-data tool whenever the user's
question requires structured business data.

Do not invent business data.

If a tool provides data, base your answer on that data.

For general questions that do not require business data,
answer normally without using a business-data tool.

Conversation history:
{history_text}

Respond to the latest user message naturally.
"""

    try:
        # Give Gemini access to the business-data tools
        config = types.GenerateContentConfig(
            tools=[
                get_customer_risk_summary,
                get_customer_business_metrics,
                get_highest_outstanding_customer,
            ]
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="AI service returned an empty response."
            )

    except HTTPException:
        raise

    except Exception as error:
        error_message = str(error)

        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail="AI service quota exceeded. Please try again later."
            )

        print(f"AI service error: {error}")

        raise HTTPException(
            status_code=502,
            detail="AI service is temporarily unavailable."
        )

    # Save assistant response
    add_message(
        request.session_id,
        "assistant",
        response.text
    )

    return {
        "response": response.text
    }