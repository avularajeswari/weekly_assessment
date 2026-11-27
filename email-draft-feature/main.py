
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Email Draft Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------
# 1. Conversation history (Demo DB)
# --------------------------------

conversation_history = {
    "session_1": [
        {
            "role": "user",
            "content": "Hi, I ordered a laptop last week. My order number is 12345."
        },
        {
            "role": "assistant",
            "content": "I can help you check your order."
        },
        {
            "role": "user",
            "content": "The delivery is delayed. I was expecting it yesterday."
        },
        {
            "role": "assistant",
            "content": "We apologize for the delay. Your order is expected to arrive tomorrow."
        }
    ],

    "session_2": [
        {
            "role": "user",
            "content": "Hello, I want to know about your Python course."
        },
        {
            "role": "assistant",
            "content": "Our Python course covers basics, advanced Python and projects."
        },
        {
            "role": "user",
            "content": "How long is the course and what is the fee?"
        },
        {
            "role": "assistant",
            "content": "The course duration is 8 weeks and the fee is Rs. 5000."
        },
        {
            "role": "user",
            "content": "Thank you. I am interested in joining next month."
        }
    ]
}


# --------------------------------
# 2. Pydantic models
# --------------------------------

class DraftRequest(BaseModel):
    session_id: str
    tone: Literal["formal", "friendly"] = "formal"


class EmailDraft(BaseModel):
    subject: str = Field(
        description="A clear and relevant email subject"
    )

    body: str = Field(
        description=(
            "Email body including recipient greeting, "
            "key conversation points and next steps"
        )
    )


# --------------------------------
# 3. Generate email using AI
# --------------------------------

def create_draft_with_ai(conversation, tone):

    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation
    )

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": f"""
                You are a professional email assistant.

                Generate a polite email based on the
                conversation history.

                Tone: {tone}

                Requirements:
                1. Generate a meaningful subject.
                2. Write a complete email body.
                3. Include recipient name if available.
                4. Summarize important discussion points.
                5. Include next steps or follow-up actions.
                6. Do not invent names, promises or facts.
                7. If the recipient's name is unknown,
                   use a suitable generic greeting.
                8. Return only the structured email draft.
                9. NEVER send an email.
                """
            },
            {
                "role": "user",
                "content": f"""
                Create an email draft from this conversation:

                {conversation_text}
                """
            }
        ],
        text_format=EmailDraft
    )

    draft = response.output_parsed

    if draft is None:
        raise ValueError("AI could not generate an email draft")

    return draft


# --------------------------------
# 4. POST /draft-email API
# --------------------------------

@app.post("/draft-email", response_model=EmailDraft)
def draft_email(request: DraftRequest):

    # Read session conversation history
    conversation = conversation_history.get(
        request.session_id
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation session not found"
        )

    try:
        # Generate draft only
        draft = create_draft_with_ai(
            conversation,
            request.tone
        )

        # Return JSON. No email is sent.
        return draft

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Draft generation failed: {str(e)}"
        )
