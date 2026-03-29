"""Central configuration for LexAgent."""

from pathlib import Path

# --- Directory setup ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"

CLAUSE_DATA_PATH = DATA_DIR / "clauses.json"
MSA_TEMPLATE_PATH = TEMPLATE_DIR / "msa_template.md"

# --- Embedding/FAISS config ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_CLAUSES = 4

# --- LLM drafting config ---
# Switch to a real Google FLAN-T5 model for proper draft generation
DRAFT_LLM_MODEL_NAME = "google/flan-t5-base"  # small -> base for better outputs
GENERATION_MAX_NEW_TOKENS = 512  # allow longer drafts for FLAN-T5
LLM_OUTPUT_MIN_LENGTH = 50  # relax minimum length to reduce fallback to template



# --- Optional environment notes ---
# Use --llm flag or set LEXAGENT_USE_LLM=true to enable LLM drafting
# HF_TOKEN can be set to speed up downloads and avoid rate limits
