
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from rag import ingest_documents, retrieve_chunks

app = FastAPI(title="Local RAG Question Answering API")

# Session memory
chat_memory = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str


class Source(BaseModel):
    file: str
    page: int


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[Source]


@app.on_event("startup")
def startup():
    ingest_documents()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message

    history = chat_memory.get(session_id, [])

    # Build search question using conversation history
    previous_context = " ".join(
        item["content"]
        for item in history[-5:]
    )

    search_question = previous_context + " " + message

    # Retrieve relevant chunks
    chunks = retrieve_chunks(search_question, top_k=3)

    # Check relevance
    if not chunks or chunks[0]["distance"] > 0.65:

        answer = "I don't know"
        sources = []

    else:

        # Extract relevant document text
        answer = chunks[0]["text"].strip()

        sources = []

        for chunk in chunks:

            source = Source(
                file=chunk["file"],
                page=chunk["page"]
            )

            if source not in sources:
                sources.append(source)

        # Limit answer length
        answer = answer[:500]

    # Save conversation
    history.extend([
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer}
    ])

    # Keep last 5 messages
    chat_memory[session_id] = history[-5:]

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=sources
    )


@app.get("/")
def home():
    return {"message": "RAG API running successfully"}
