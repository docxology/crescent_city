# src/ Agent Guide

## Purpose

This is the project library layer. Code here is imported by scripts,
tests, and the shared template renderer.

## Contracts

- Public project APIs live in `figures.py`, `pipeline.py`, and
  `manuscript_variables.py`.
- `FIGURE_REGISTRY` is the single figure contract; changing it requires
  manuscript, docs, and tests to change together.
- `data/figure_provenance.csv` supplies registry provenance fields and
  long descriptions; update it with figure registry or catalog changes.
- Keep `scripts/` thin by putting reusable behavior here.
- Avoid network access in normal project execution.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_config.py tests/test_pipeline.py tests/test_figures.py tests/test_publishing.py -q
```
