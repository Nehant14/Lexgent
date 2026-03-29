"""Agent that generates the final legal draft text.

Supports two modes:
- Template-based drafting (fast + reliable fallback)
- Transformer LLM-based drafting (optional, with fallback if model download fails)

"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from lexagent.agents.base import BaseAgent
from lexagent.config import DRAFT_LLM_MODEL_NAME, GENERATION_MAX_NEW_TOKENS
from lexagent.schemas import DraftContext, RetrievedClause


class DraftGenerationAgent(BaseAgent):
    name = "draft_generator"

    def __init__(
        self,
        template_path: Path,
        enable_llm: bool = False,
        llm_model_name: str = DRAFT_LLM_MODEL_NAME,
        max_new_tokens: int = GENERATION_MAX_NEW_TOKENS,
    ) -> None:
        self.template = template_path.read_text(encoding="utf-8")
        self.enable_llm = enable_llm
        self.llm_model_name = llm_model_name
        self.max_new_tokens = max_new_tokens

        self._llm_tokenizer = None
        self._llm_model = None
        self._llm_ready = False
        self._llm_error: str | None = None
        if self.enable_llm:
            # Lazy import so the project remains runnable without transformers unless needed.
            try:
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # This enables AI-based drafting

                self._llm_tokenizer = AutoTokenizer.from_pretrained(self.llm_model_name)
                self._llm_model = AutoModelForSeq2SeqLM.from_pretrained(self.llm_model_name)
                self._llm_model.eval()
                self._llm_ready = True
            except Exception as e:
                # If model download fails (no internet / rate limiting), we fall back to template drafting.
                self._llm_ready = False
                self._llm_error = f"Transformer pipeline init failed: {type(e).__name__}: {e}"

    def run(self, payload: tuple[DraftContext, list[RetrievedClause]]) -> str:
        context, clauses = payload
        fields = context.normalized_fields
        selected = {cl.title.lower(): cl.text for cl in clauses}

        # If the transformer model is available, use it to draft the agreement text.
        if self.enable_llm and self._llm_model is not None and self._llm_tokenizer is not None:
            prompt = self._build_prompt(context=context, clauses=clauses)
            try:
                text = self._generate(prompt=prompt)
                text = text.strip()
                # If the LLM produced a non-trivial answer, use it.
                # During interview demos we prefer seeing the LLM output rather than falling back.
                if text and len(text) > 120:
                    return text
                if text:
                    print(
                        "[LexAgent] LLM output was too short/unstructured; using template fallback. "
                        f"Generated length={len(text)}"
                    )
            except Exception as e:
                # Fall back to deterministic template generation if anything fails.
                print(
                    f"[LexAgent] Transformer LLM generation failed; using template fallback. "
                    f"Error: {type(e).__name__}: {e}"
                )
                return self.template.format(
                    party_a=fields["party_a"],
                    party_b=fields["party_b"],
                    jurisdiction=fields["jurisdiction"],
                    term_months=fields["term_months"],
                    payment_terms=fields["payment_terms"],
                    confidentiality_clause=selected.get(
                        "confidentiality",
                        "Both parties shall keep all non-public information confidential.",
                    ),
                    liability_clause=selected.get(
                        "limitation of liability",
                        "Liability is limited to direct damages subject to agreed caps.",
                    ),
                    termination_clause=selected.get(
                        "termination",
                        "Either party may terminate for material breach with written notice.",
                    ),
                    governing_law_clause=selected.get(
                        "governing law",
                        "This Agreement shall be governed by the laws of the stated jurisdiction.",
                    ),
                    extra_notes=fields["extra_notes"] or "No additional notes.",
                )

        if self.enable_llm and not self._llm_ready:
            extra = f" Error: {self._llm_error}" if self._llm_error else ""
            print(f"[LexAgent] Transformer LLM model not available; using template fallback.{extra}")

        # Template-based fallback (fast + deterministic).
        return self.template.format(
            party_a=fields["party_a"],
            party_b=fields["party_b"],
            jurisdiction=fields["jurisdiction"],
            term_months=fields["term_months"],
            payment_terms=fields["payment_terms"],
            confidentiality_clause=selected.get(
                "confidentiality",
                "Both parties shall keep all non-public information confidential.",
            ),
            liability_clause=selected.get(
                "limitation of liability",
                "Liability is limited to direct damages subject to agreed caps.",
            ),
            termination_clause=selected.get(
                "termination",
                "Either party may terminate for material breach with written notice.",
            ),
            governing_law_clause=selected.get(
                "governing law",
                "This Agreement shall be governed by the laws of the stated jurisdiction.",
            ),
            extra_notes=fields["extra_notes"] or "No additional notes.",
        )

    def _generate(self, prompt: str) -> str:
        import torch

        inputs = self._llm_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        )
        with torch.no_grad():
            output_ids = self._llm_model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                num_beams=4,
                early_stopping=True,
            )
        return self._llm_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def _build_prompt(self, context: DraftContext, clauses: Iterable[RetrievedClause]) -> str:
        fields = context.normalized_fields
        clause_block = "\n\n".join(
            f"CLAUSE: {c.title}\n{c.text}" for c in clauses
        )

        # Prompt is deliberately structured so the generated draft is easy to scan during interviews.
        return f"""
You are a contract drafting assistant. Draft a first-pass Master Services Agreement (MSA) in Markdown.
Use ONLY generic/legal placeholder language. Do not provide legal advice.

DEAL CONTEXT
- Agreement type: {fields['agreement_type']}
- Party A: {fields['party_a']}
- Party B: {fields['party_b']}
- Jurisdiction: {fields['jurisdiction']}
- Payment terms: {fields['payment_terms']}
- Confidentiality level: {fields['confidentiality_level']}
- Liability cap: {fields['liability_cap']}
- Term length (months): {fields['term_months']}
- Additional notes: {fields['extra_notes'] or 'No additional notes.'}

RETRIEVED CLAUSE EXCERPTS (may be paraphrased)
{clause_block}

OUTPUT REQUIREMENTS
- Output markdown with these exact section headings: Scope, Term, Payment Terms, Confidentiality, Limitation of Liability, Termination, Governing Law, Additional Notes.
- Include the parties' names and the jurisdiction in the appropriate sections.
- Keep it concise and coherent (about 250-500 words).
""".strip()

    def _looks_like_draft(self, text: str) -> bool:
        # Simple heuristic so we don't return irrelevant LLM output.
        # Template headings include "## 1. Scope" style.
        return "## 1." in text and "## 8." in text



"""

In simple terms, an LLM (like the one in your code) cannot understand words directly, 
so it first breaks your sentence into small pieces called tokens 
(for example, “Hello world” might become “Hello” and “ world”), then each token is converted 
into a number (like IDs), and after that each number is turned into a vector, which is just a
 list of many numbers that represent the meaning of that token (like [0.12, -0.45, 0.88, ...]). 
 The model only works with these numbers, not actual text. 
 So the full process is: you give text → it becomes tokens → tokens become numbers → numbers become vectors → 
 the model processes these vectors and predicts the next vectors (which correspond to tokens) → those tokens 
 are converted back into readable text. For example, if you input “The contract shall”, the model converts 
 it into tokens and vectors, then predicts the next token like “be”, then “governed”, and keeps going to 
 form a sentence. So in short, think of it like this: humans read words, but LLMs read numbers that represent 
 the meaning of words.

"""
