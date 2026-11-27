
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="End-to-End Testing Application")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "Application is running successfully"}


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.lower()

    if "leave policy" in question:
        answer = "The company leave policy is available in the employee document."
        tools = ["document_search"]

    elif "notice period" in question:
        answer = "The employee notice period is available in the company document."
        tools = ["document_search"]

    elif "working hours" in question:
        answer = "The company working hours are available in the company document."
        tools = ["document_search"]

    elif "phone number" in question:
        answer = "Sorry, this information is not available."
        tools = []

    elif "revenue" in question:
        answer = "Sorry, I cannot predict the company's future revenue."
        tools = []

    elif "c101" in question:
        answer = "Customer C101 details: Name Ravi, Email ravi@gmail.com"
        tools = ["crm_tool"]

    elif "c102" in question:
        answer = "Customer C102 email: priya@gmail.com"
        tools = ["crm_tool"]

    elif "o501" in question:
        answer = "Order O501 status is Shipped."
        tools = ["order_tool"]

    elif "o502" in question:
        answer = "Order O502 delivery date is 2026-12-01."
        tools = ["order_tool"]

    elif "email" in question or "draft" in question:
        answer = "Subject: Apology for Order Delay\n\nDear Customer,\n\nWe regret the delay in delivering your order. We apologize for the inconvenience."
        tools = []

    else:
        answer = "Sorry, I could not find the requested information."
        tools = []

    return {"answer": answer, "tools_used": tools}
