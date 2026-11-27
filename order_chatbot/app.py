
import os
import json
import requests

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from tools import get_order_status, get_customer_orders

load_dotenv()

app = Flask(__name__)

# Ollama configuration
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")


# Define available tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the delivery status of a specific order using its order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The order ID"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": "Get all orders belonging to a customer using customer ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The customer ID"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
]


# Only approved functions can execute
AVAILABLE_TOOLS = {
    "get_order_status": get_order_status,
    "get_customer_orders": get_customer_orders
}


def call_ollama(messages, use_tools=True):

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0,
            "num_predict": 256
        }
    }

    if use_tools:
        payload["tools"] = TOOLS

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(10, 300)
    )

    response.raise_for_status()

    return response.json()["message"]


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "PostgreSQL Order Chatbot is running"
    })


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    user_message = data.get("message")

    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({
            "error": "Please enter a question"
        }), 400

    messages = [
        {
            "role": "system",
            "content": """
You are a PostgreSQL order assistant.

You have two database tools:

1. get_order_status(order_id)
   Use this when the user asks about a particular order.

2. get_customer_orders(customer_id)
   Use this when the user asks about all orders for a customer.

IMPORTANT RULES:

- Always call the appropriate database tool.
- Do not explain which tool you would use.
- Do not write SQL queries.
- Do not invent database information.
- Use only the information returned by the database tools.
- After receiving tool results, give a short, clear answer.
"""
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    try:

        print("\nUser:", user_message)

        # STEP 1: Ask Ollama to select a tool
        print("\nSTEP 1: Sending question to Ollama...")

        assistant_message = call_ollama(
            messages,
            use_tools=True
        )

        print("\nOLLAMA RESPONSE:")
        print(json.dumps(assistant_message, indent=2))

        # STEP 2: Get tool calls
        tool_calls = assistant_message.get("tool_calls", [])

        if not tool_calls:

            return jsonify({
                "error": "Ollama did not return a structured tool call. Please try again.",
                "model_output": assistant_message.get("content", "")
            }), 502

        messages.append(assistant_message)

        tool_results = []

        # STEP 3: Execute selected tools
        for tool_call in tool_calls:

            function = tool_call.get("function", {})

            name = function.get("name")
            arguments = function.get("arguments", {})

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            print("\nSTEP 2: Tool selected:", name)
            print("Arguments:", arguments)

            # Validate tool name
            if name not in AVAILABLE_TOOLS:

                return jsonify({
                    "error": "Unauthorized tool requested"
                }), 400

            # Validate arguments
            expected_arguments = {
                "get_order_status": {"order_id"},
                "get_customer_orders": {"customer_id"}
            }

            if (
                not isinstance(arguments, dict)
                or set(arguments.keys()) != expected_arguments[name]
            ):

                return jsonify({
                    "error": "Invalid tool arguments"
                }), 400

            # Execute Python function
            print("\nSTEP 3: Executing database tool...")

            tool_result = AVAILABLE_TOOLS[name](**arguments)

            print("Database result:", tool_result)

            tool_results.append({
                "tool": name,
                "arguments": arguments,
                "result": tool_result
            })

            # Send database result back to Ollama
            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(
                    tool_result,
                    default=str
                )
            })

        # STEP 4: Generate final answer
        print("\nSTEP 4: Generating final answer...")

        final_message = call_ollama(
            messages,
            use_tools=False
        )

        answer = final_message.get("content", "")

        print("\nAssistant:", answer)

        return jsonify({
            "answer": answer,
            "tools_used": tool_results
        })

    except requests.Timeout:

        return jsonify({
            "error": "Ollama request timed out. Check whether Ollama is running."
        }), 504

    except requests.RequestException as e:

        return jsonify({
            "error": "Ollama connection error: " + str(e)
        }), 503

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
