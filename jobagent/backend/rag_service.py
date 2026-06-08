import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

# Use default sentence transformer embeddings (no API key needed)
ef = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="resumes",
    embedding_function=ef
)

def add_resume_to_rag(candidate_id: int, resume_text: str):
    """Embed and store resume in ChromaDB."""
    collection.upsert(
        documents=[resume_text],
        ids=[str(candidate_id)],
        metadatas=[{"candidate_id": candidate_id}]
    )

def search_similar_candidates(jd_text: str, top_k: int = 5):
    """Find top matching candidates for a JD using RAG."""
    results = collection.query(
        query_texts=[jd_text],
        n_results=min(top_k, collection.count()) or 1
    )
    return results
