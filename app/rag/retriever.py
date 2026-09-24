from pathlib import Path
import re
import chromadb
from chromadb.utils import embedding_functions
from app.core.config import get_settings

settings = get_settings()

class Retriever:
    """
    Retrieval using ChromaDB vector store and real embeddings.
    """

    def __init__(self) -> None:
        # Initialize an in-memory ChromaDB client
        self.client = chromadb.Client()
        
        # Use default embedding function which downloads a small model on first run
        # Alternative: use OllamaEmbeddingFunction if an ollama endpoint is available
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Create a collection
        self.collection = self.client.get_or_create_collection(
            name="shopfloor_knowledge",
            embedding_function=self.ef
        )
        
        self._load_documents()

    def _load_documents(self) -> None:
        directory = Path(settings.knowledge_dir)
        docs = []
        ids = []
        metadatas = []
        
        for path in sorted(directory.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for index, chunk in enumerate(self._chunk(text)):
                docs.append(chunk)
                ids.append(f"{path.stem}-{index}")
                metadatas.append({"source": path.name})
                
        if not docs:
            raise RuntimeError("No knowledge documents found")
            
        # Upsert to vector store to avoid DuplicateID warnings on re-instantiation
        self.collection.upsert(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )

    @staticmethod
    def _chunk(text: str) -> list[str]:
        # Simple paragraph chunking
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        return paragraphs

    def search(self, query: str, top_k: int) -> list[dict]:
        # Query the vector store
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        retrieved = []
        if results and "documents" in results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                dist = results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                # Chroma uses L2 distance by default. We convert it to a pseudo-score to match previous interface.
                # Smaller distance is better. Score = 1 / (1 + distance)
                score = 1.0 / (1.0 + dist)
                
                retrieved.append({
                    "id": results["ids"][0][i],
                    "source": meta.get("source", ""),
                    "text": doc,
                    "score": round(score, 4)
                })
        
        return retrieved
