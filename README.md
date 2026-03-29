# LexAgent - Agentic Legal Drafting System

LexAgent is an AI-powered, multi-agent legal drafting project that automates first-pass drafting of complex legal agreements.
It combines transformer-based sentence embeddings, FAISS semantic search, and a simple agent workflow for context management, clause retrieval, and document generation.

This project is designed to be:
- easy to explain in interviews,
- practical to run locally,
- structured like a real GitHub repository.

## Project Highlights

- Multi-agent workflow with clear separation of responsibilities:
  - **ContextManagerAgent**: normalizes deal inputs into drafting context.
  - **ClauseRetrievalAgent**: fetches relevant clauses via FAISS vector search.
  - **DraftGenerationAgent**: assembles a coherent agreement draft.
- Transformer-based embeddings using `sentence-transformers`.
- FAISS-based vector index for semantic clause matching.
- Clean Python package structure with tests and CI.
- Sample legal dataset and template included.

## Architecture

1. User provides deal details (parties, jurisdiction, payment terms, etc.)
2. `ContextManagerAgent` creates a structured drafting context.
3. `ClauseRetrievalAgent` embeds query intent and retrieves top-k clauses from FAISS.
4. `DraftGenerationAgent` fills template sections and composes the draft.
5. `Orchestrator` coordinates the complete pipeline.

## Tech Stack

- Python 3.10+
- `sentence-transformers` (MiniLM embeddings)
- `faiss-cpu` (semantic vector retrieval)
- `numpy`, `pytest`

## Quickstart

### 1) Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run demo

```bash
python scripts/run_demo.py
```

You will see:
- the normalized drafting context,
- top retrieved clauses,
- and a generated legal draft in markdown.

### Optional: enable transformer LLM drafting

By default the project uses the deterministic template-based drafting (fast + reliable).
To enable transformer-based generation:

```powershell
python scripts\run_demo.py --llm
```

or set:

```powershell
$env:LEXAGENT_USE_LLM="true"
```

## Example Output

The generated draft includes:
- Parties and effective date,
- Confidentiality,
- Payment Terms,
- Liability,
- Term and Termination,
- Governing Law.

## Project Structure

```text
lexagent/
  agents/
    context_manager.py
    clause_retriever.py
    draft_generator.py
    orchestrator.py
  retrieval/
    faiss_store.py
  data/
    clauses.json
  templates/
    msa_template.md
scripts/
  run_demo.py
tests/
  test_pipeline.py
```

## Interview Talking Points

- Demonstrates **agentic orchestration** rather than one long prompt.
- Shows practical use of **RAG-like retrieval** for legal clause reuse.
- Uses **FAISS + transformer embeddings** for semantic matching.
- Easy to extend with an external LLM API for richer drafting quality.

## Limitations and Responsible Use

- This repository is for educational and prototyping purposes only.
- It does not provide legal advice.
- Generated drafts must be reviewed by qualified legal professionals.

## Roadmap

- Add memory of negotiation history.
- Support multiple agreement types (NDA, MSA, DPA, Employment).
- Integrate production LLM providers and citation tracing.
- Build a lightweight web UI.
