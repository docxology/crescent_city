# tests/ Agent Guide

## Purpose

Tests are the project contract. They should catch stale documentation,
broken citations, figure-count drift, schema regressions, and manuscript
cross-reference mistakes before rendering.

## Contracts

- Use real project files and `tmp_path` copies rather than mocks.
- Keep fixture cost controlled; expensive pipeline artifacts should be shared
  through existing fixtures in `conftest.py`.
- Update documentation-drift tests when adding stable counts or folder docs.
- Keep figure-provenance tests aligned with `data/figure_provenance.csv`,
  `src/figures.py`, and `manuscript/A1_figure_catalogue.md`.
- Include new authored directories in the American-English guard when they
  become source truth.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/ -q
```
