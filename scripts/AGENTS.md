# scripts/ Agent Guide

## Purpose

Scripts are entry points only. They should remain small wrappers around
`../src/` modules so the behavior is importable and testable.

## Contracts

- Do not place manuscript analysis, figure logic, or bibliography rules here.
- Keep CLI options backward compatible unless tests and docs change together.
- Use project-root arguments instead of hard-coded absolute paths.
- Preserve `PYTHONPATH=. uv run python ...` command compatibility from the
  project root.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_pipeline.py tests/test_pipeline_integration.py -q
```
