
import os
from io import BytesIO

import pymupdf
import chromadb

from docx import Document
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# ==========================================
# STEP 1: FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Multi-Capability Assistant",
    description="Document Upload and Ingestion API",
    version="1.0"
)


# ==========================================
# STEP 2: CHROMA DATABASE
# ==========================================

os.makedirs("chroma_db", exist_ok=True)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

embedding_function = DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_function
)


# ==========================================
# STEP 3: EXTRACT PDF TEXT
# ==========================================

def extract_pdf_text(file_bytes):

    try:
        document = pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text() + "\n"

        document.close()

        return text.strip()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read PDF file"
        )


# ==========================================
# STEP 4: EXTRACT WORD TEXT
# ==========================================

def extract_docx_text(file_bytes):

    try:
        document = Document(BytesIO(file_bytes))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        # Extract text from Word tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        paragraphs.append(cell.text)

        return "\n".join(paragraphs).strip()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read Word document"
        )


# ==========================================
# STEP 5: DOCUMENT CHUNKING
# ==========================================

def chunk_text(text, chunk_size=1000, overlap=200):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


# ==========================================
# STEP 6: GENERATE DOCUMENT ID
# ==========================================

def generate_document_id():

    existing = collection.get(
        include=["metadatas"]
    )

    document_ids = set()

    for metadata in existing["metadatas"]:

        if metadata and "document_id" in metadata:
            document_ids.add(metadata["document_id"])

    # Find the next available ID
    numbers = [
        int(doc_id[1:])
        for doc_id in document_ids
        if doc_id.startswith("d") and doc_id[1:].isdigit()
    ]

    next_id = max(numbers, default=0) + 1

    return f"d{next_id}"


# ==========================================
# STEP 7: POST /documents
# ==========================================

@app.post("/documents", status_code=201)
async def upload_document(file: UploadFile = File(...)):

    filename = file.filename or ""

    extension = os.path.splitext(filename)[1].lower()

    # Validate file type
    if extension not in [".pdf", ".docx"]:

        raise HTTPException(
            status_code=415,
            detail="Only PDF and DOCX files are supported"
        )

    file_bytes = await file.read()

    if not file_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Extract document text
    if extension == ".pdf":
        text = extract_pdf_text(file_bytes)
    else:
        text = extract_docx_text(file_bytes)

    if not text.strip():

        raise HTTPException(
            status_code=422,
            detail="No text found in uploaded document"
        )

    # Split text into chunks
    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200
    )

    if not chunks:

        raise HTTPException(
            status_code=422,
            detail="No chunks could be created"
        )

    # Generate document ID
    document_id = generate_document_id()

    # Generate unique chunk IDs
    chunk_ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    # Create metadata
    metadatas = [
        {
            "document_id": document_id,
            "name": filename,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    # Store in ChromaDB
    try:
        collection.add(
            ids=chunk_ids,
            documents=chunks,
            metadatas=metadatas
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to store document in ChromaDB"
        )

    return JSONResponse(
        status_code=201,
        content={
            "id": document_id,
            "chunks": len(chunks)
        }
    )


# ==========================================
# STEP 8: GET /documents
# ==========================================

@app.get("/documents")
def list_documents():

    result = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in result["metadatas"]:

        if metadata:

            document_id = metadata["document_id"]

            documents[document_id] = {
                "id": document_id,
                "name": metadata["name"]
            }

    # Sort documents by ID
    sorted_documents = sorted(
        documents.values(),
        key=lambda item: int(item["id"][1:])
    )

    return sorted_documents


# ==========================================
# STEP 9: ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Multi-Capability Assistant API is running"
    }
# ==========================================
# STEP 10: HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "database": "ChromaDB connected"
    }
