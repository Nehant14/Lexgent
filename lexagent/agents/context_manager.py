"""Context manager agent for normalizing drafting requests."""

from dataclasses import asdict

from lexagent.agents.base import BaseAgent
from lexagent.schemas import DraftContext, DraftRequest


# It cleans and standardizes user input, then produces a structured context and summary for further processing.
class ContextManagerAgent(BaseAgent):  
    name = "context_manager"

    def run(self, payload: DraftRequest) -> DraftContext:
        data = asdict(payload)
        normalized = {
            "agreement_type": data["agreement_type"].strip().upper(),
            "party_a": data["party_a"].strip(),
            "party_b": data["party_b"].strip(),
            "jurisdiction": data["jurisdiction"].strip(),
            "payment_terms": data["payment_terms"].strip(),
            "confidentiality_level": data["confidentiality_level"].strip().lower(),
            "liability_cap": data["liability_cap"].strip(),
            "term_months": int(data["term_months"]),
            "extra_notes": data["extra_notes"].strip(),
        }

        summary = (
            f"{normalized['agreement_type']} between {normalized['party_a']} and "
            f"{normalized['party_b']} under {normalized['jurisdiction']} law with "
            f"{normalized['payment_terms']} payment terms."
        )

        return DraftContext(summary=summary, normalized_fields=normalized)

