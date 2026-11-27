
import os
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_or_create_collection(
    name="company_docs",
    metadata={"hnsw:space": "cosine"}
)


def ingest_documents():

    documents = []

    for filename in os.listdir("documents"):

        path = os.path.join("documents", filename)

        if filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            documents.append((content, filename, 1))

        elif filename.endswith(".pdf"):
            reader = PdfReader(path)

            for page_no, page in enumerate(reader.pages, start=1):
                content = page.extract_text() or ""

                if content.strip():
                    documents.append(
                        (content, filename, page_no)
                    )

    ids = []
    texts = []
    metadatas = []

    for content, filename, page in documents:

        chunk_size = 400
        overlap = 80

        for i, start in enumerate(
            range(0, len(content), chunk_size - overlap)
        ):

            chunk = content[start:start + chunk_size]

            if chunk.strip():
                ids.append(f"{filename}_{page}_{i}")
                texts.append(chunk)

                metadatas.append({
                    "file": filename,
                    "page": page
                })

    if texts:
        embeddings = model.encode(texts).tolist()

        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    print("Documents indexed successfully!")


def retrieve_chunks(question, top_k=3):

    if collection.count() == 0:
        return []

    embedding = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=embedding,
        n_results=min(top_k, collection.count())
    )

    chunks = []

    for i, text in enumerate(results["documents"][0]):

        chunks.append({
            "text": text,
            "file": results["metadatas"][0][i]["file"],
            "page": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i]
        })

    return chunks
