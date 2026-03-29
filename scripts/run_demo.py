"""Run a local LexAgent drafting demo."""

import sys
import os
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lexagent import LexAgentOrchestrator
from lexagent.schemas import DraftRequest


def main() -> None:
    # Optional flag: `--llm` enables transformer-based drafting.
    # Default stays off to avoid slow model downloads / rate limits.
    if "--llm" in sys.argv:
        os.environ["LEXAGENT_USE_LLM"] = "true"

    request = DraftRequest(
        agreement_type="MSA",
        party_a="Acme AI Pvt Ltd",
        party_b="Northwind Health Inc",
        jurisdiction="State of California",
        payment_terms="Invoices shall be paid within 30 days of issue date.",
        confidentiality_level="High",
        liability_cap="12 months of paid fees",
        term_months=24,
        extra_notes="Include monthly governance calls and quarterly security review.",
    )


    orchestrator = LexAgentOrchestrator()
    result = orchestrator.draft(request)

    print("\n=== Context Summary ===")
    print(result["context_summary"])

    print("\n=== Retrieved Clauses ===")
    pprint(result["retrieved_clauses"])

    print("\n=== Draft ===\n")
    print(result["draft"])


if __name__ == "__main__":   # It lets you write code that only runs when the file is executed directly, but not when it's imported elsewhere.
    main()
