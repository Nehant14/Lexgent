from lexagent import LexAgentOrchestrator
from lexagent.schemas import DraftRequest


def test_orchestrator_generates_draft():
    request = DraftRequest(
        agreement_type="MSA",
        party_a="A Corp",
        party_b="B Corp",
        jurisdiction="New York",
        payment_terms="Net 30 days",
        confidentiality_level="high",
        liability_cap="fees paid in prior 12 months",
        term_months=12,
        extra_notes="test note",
    )

    orchestrator = LexAgentOrchestrator()
    result = orchestrator.draft(request)

    assert "context_summary" in result
    assert "retrieved_clauses" in result
    assert "draft" in result
    assert "A Corp" in result["draft"]
    assert "B Corp" in result["draft"]
    assert "New York" in result["draft"]
