import ollama
import json

from fastapi import FastAPI
from pydantic import BaseModel, Field

from CRM_tool import get_customer_details


app = FastAPI()

MODEL = "qwen2.5:1.5b"

sessions = {}


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    sources: list = Field(default_factory=list)


# Define the CRM tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_details",
            "description": (
                "Get customer information from CRM. "
                "Use this tool when the user asks about "
                "a customer's name, plan, email or city."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "Customer ID"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question
    session_id = request.session_id

    history = sessions.get(session_id, [])

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful CRM assistant. "
                "Use get_customer_details whenever the "
                "user asks for specific customer information. "
                "Never invent customer information. "
                "Use the tool result to answer accurately."
            )
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": question
    })

    # Send question to Ollama
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    # Execute tool calls requested by the LLM
    while response.message.tool_calls:

        messages.append(response.message)

        for tool_call in response.message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            if tool_name == "get_customer_details":

                customer_id = int(arguments["customer_id"])

                result = get_customer_details(customer_id)

                # Return CRM result to LLM
                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(result)
                })

        # Ask LLM to generate final answer
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )

    answer = response.message.content

    # Save conversation
    history.append({
        "role": "user",
        "content": question
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    sessions[session_id] = history[-10:]

    return ChatResponse(
        answer=answer,
        sources=[]
    )