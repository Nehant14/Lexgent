"""Orchestration layer for LexAgent workflow."""

import os

from lexagent.agents.clause_retriever import ClauseRetrievalAgent
from lexagent.agents.context_manager import ContextManagerAgent
from lexagent.agents.draft_generator import DraftGenerationAgent
from lexagent.config import CLAUSE_DATA_PATH, MSA_TEMPLATE_PATH
from lexagent.schemas import DraftRequest


class LexAgentOrchestrator:
    """Coordinates the end-to-end multi-agent drafting process."""

    def __init__(self) -> None:
        # Default: LLM drafting disabled for reliability and fast unit tests.
        # Enable with: `set LEXAGENT_USE_LLM=true`
        # or by passing `--llm` in the demo script.
        use_llm = os.environ.get("LEXAGENT_USE_LLM", "false").strip().lower() == "true"
        self.context_agent = ContextManagerAgent()
        self.retrieval_agent = ClauseRetrievalAgent(clauses_path=CLAUSE_DATA_PATH)
        self.generation_agent = DraftGenerationAgent(
            template_path=MSA_TEMPLATE_PATH, 
            enable_llm=use_llm,
        )  # template path is passed here, real path in config.py
        

    def draft(self, request: DraftRequest) -> dict:
        context = self.context_agent.run(request)
        clauses = self.retrieval_agent.run(context)
        draft_text = self.generation_agent.run((context, clauses))

        return {
            "context_summary": context.summary,
            "retrieved_clauses": [
                {
                    "id": c.clause_id,
                    "title": c.title,
                    "score": round(c.score, 4),
                }
                for c in clauses
            ],
            "draft": draft_text,
        }

