"""Agent that retrieves relevant clauses from vector store."""

from pathlib import Path

from lexagent.agents.base import BaseAgent
from lexagent.config import EMBEDDING_MODEL_NAME, TOP_K_CLAUSES
from lexagent.retrieval.faiss_store import ClauseVectorStore
from lexagent.schemas import DraftContext, RetrievedClause


class ClauseRetrievalAgent(BaseAgent):
    name = "clause_retriever"

    def __init__(self, clauses_path: Path) -> None:  # It creates your FAISS-based vector store
        self.store = ClauseVectorStore(clauses_path=clauses_path, model_name=EMBEDDING_MODEL_NAME)

    def run(self, payload: DraftContext) -> list[RetrievedClause]:
        fields = payload.normalized_fields
        query = (
            f"{fields['agreement_type']} agreement clauses for "
            f"confidentiality {fields['confidentiality_level']}, "
            f"liability cap {fields['liability_cap']}, "
            f"payment {fields['payment_terms']}, and governing law {fields['jurisdiction']}"
        )
        return self.store.search(query=query, k=TOP_K_CLAUSES)  # not single but top k clauses returned
        # the query is converted to a vector, then compared with stored clause vectors. 

# Query (text)
#    ↓
# Converted to vector
#    ↓
# Compared with stored clause vectors
#    ↓
# Top K matches returned

