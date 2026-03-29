# Contributing to LexAgent

Thanks for your interest in contributing.

## Local Setup

1. Create virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\activate` (Windows)
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run tests:
   - `python -m pytest -q`

## Development Guidelines

- Keep modules small and focused by agent responsibility.
- Add or update tests for behavior changes.
- Keep legal text examples generic and non-sensitive.

## Pull Request Checklist

- [ ] Tests pass locally
- [ ] README reflects new behavior
- [ ] New code is easy to explain in interview context
