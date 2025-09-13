
import chromadb
from chromadb.config import Settings
from pathlib import Path
import importlib.util

# Load config for vector DB path and collection
config_path = Path(__file__).parent / "config.py"
spec = importlib.util.spec_from_file_location("config", str(config_path))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
VECTORDB_DIR = str(Path(config.RAG_VECTORDB_DIR).resolve())
VECTORDB_COLLECTION = config.RAG_VECTORDB_COLLECTION

def get_relevant_chunks(query, top_k=3):
    client = chromadb.PersistentClient(path=VECTORDB_DIR, settings=Settings(allow_reset=True))
    collection = client.get_or_create_collection(VECTORDB_COLLECTION)
    results = collection.query(query_texts=[query], n_results=top_k)
    # Defensive: handle None or missing keys
    ids = results.get('ids', [[]])[0] if results and 'ids' in results and results['ids'] else []
    metadatas = results.get('metadatas', [[]])[0] if results and 'metadatas' in results and results['metadatas'] else []
    embeddings = results.get('embeddings', [[]])[0] if results and 'embeddings' in results and results['embeddings'] else []
    chunks = []
    for i in range(len(ids)):
        chunks.append({
            "id": ids[i],
            "metadata": metadatas[i] if i < len(metadatas) else {},
            "embedding": embeddings[i] if i < len(embeddings) else None,
        })
    if not chunks:
        # Provide a default chunk with general info
        chunks = [{
            "id": "default",
            "metadata": {
                "text": (
                    "This assistant is a Proof of Concept chatbot for the World Falls Guidelines project. "
                    "It demonstrates Retrieval-Augmented Generation (RAG) using a vector database of guideline documents. "
                    "You can ask questions about the World Falls Guidelines, and the bot will retrieve relevant information from the indexed documents and use an LLM to answer. "
                    "If you see this message, it means no relevant information was found for your query, or the database is empty."
                ),
                "source_path": "General Info"
            },
            "embedding": None
        }]
    return chunks
