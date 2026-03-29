"""FAISS-backed semantic clause store."""

# Stores legal clauses → converts them into vectors → lets you search similar clauses using meaning (not keywords)


import json
from pathlib import Path

import faiss   # fast similarity search
import numpy as np
from sentence_transformers import SentenceTransformer   # converts text → vectors

from lexagent.schemas import RetrievedClause


# Loads clauses
# Converts them to vectors
# Stores them in FAISS
# Searches them
class ClauseVectorStore:
    """Builds and queries a FAISS index for legal clauses."""

    def __init__(self, clauses_path: Path, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)
        self.clauses = self._load_clauses(clauses_path)
        self.embeddings = self._embed_texts([c["text"] for c in self.clauses])
        self.index = self._build_index(self.embeddings)

    def _load_clauses(self, clauses_path: Path) -> list[dict]:
        with clauses_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)  # laoded as Python dictionary
        return payload["clauses"]

    def _embed_texts(self, texts: list[str]) -> np.ndarray:   # Converts them into numerical vectors (embeddings)
        vectors = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)  # model.encode from sentecetransform
        return vectors.astype(np.float32)
    # normalize_embedding = true : makes vectors unit-length

    def _build_index(self, vectors: np.ndarray) -> faiss.IndexFlatIP:
        dim = vectors.shape[1]  # shape[1] = number of columns = embedding size
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
        return index

    def search(self, query: str, k: int = 4) -> list[RetrievedClause]:  # self → the object (your vector store)
        qvec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True) # Convert query → vector
        qvec = qvec.astype(np.float32)
        scores, idxs = self.index.search(qvec, k) # number of results to return (default(K) = 4)

        results: list[RetrievedClause] = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0:  # sometimes it give -1.
                continue
            clause = self.clauses[int(idx)]
            results.append(
                RetrievedClause(
                    clause_id=clause["id"],
                    title=clause["title"],
                    text=clause["text"],
                    score=float(score),
                )
            )
        return results

# User query
#    ↓
# Convert to vector
#    ↓
# FAISS search
#    ↓
# Get top k indices
#    ↓
# Fetch original clauses
#    ↓
# Return structured results

# Its like each clauses is given a vector in space (not always 3D space, it can even be 384(here, and also mostly) dimentions)
# so like if we have 5 clauses, they all will have a vector in space, then we take the query and convert it to vector,
# no we see which clause is more closer to the query in the vector space by just calculating arithematic distance in the 
# space and get the required result.