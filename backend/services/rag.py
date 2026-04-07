import chromadb
import requests
import os
import hashlib

# ChromaDB stores vectors locally in this folder
CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
client = chromadb.PersistentClient(path=CHROMA_DIR)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get embeddings from Ollama (runs locally, no API key needed)."""
    embeddings = []

    for text in texts:
        try:
            response = requests.post("http://localhost:11434/api/embeddings", json={
                "model": "llama3.2:3b",
                "prompt": text
            }, timeout=30)

            if response.status_code == 200:
                data = response.json()
                embeddings.append(data["embedding"])
            else:
                print(f"Ollama embedding error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Ollama embedding exception: {e}")
            return []

    return embeddings


def store_document_chunks(doc_id: str, text: str):
    """Chunk a document, embed it, and store in ChromaDB."""
    collection_name = "doc_" + hashlib.md5(doc_id.encode()).hexdigest()[:16]

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"doc_id": doc_id}
    )

    chunks = chunk_text(text)
    if not chunks:
        return []

    embeddings = get_embeddings(chunks)

    if not embeddings:
        return chunks

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
    )

    return chunks


def retrieve_best_chunks(doc_id: str, query: str, n_results: int = 10) -> list[str]:
    """Retrieve the most relevant chunks for a query."""
    collection_name = "doc_" + hashlib.md5(doc_id.encode()).hexdigest()[:16]

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        return []

    query_embedding = get_embeddings([query])
    if not query_embedding:
        return []

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding[0]],
        n_results=min(n_results, count),
    )

    return results["documents"][0] if results["documents"] else []


def retrieve_all_chunks_ordered(doc_id: str) -> list[str]:
    """Retrieve ALL chunks in original order — better for summarization."""
    collection_name = "doc_" + hashlib.md5(doc_id.encode()).hexdigest()[:16]

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        return []

    results = collection.get()

    if not results["documents"]:
        return []

    paired = zip(results["ids"], results["documents"])
    sorted_pairs = sorted(paired, key=lambda x: int(x[0].split("_")[1]))

    return [doc for _, doc in sorted_pairs]