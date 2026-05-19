# data/ Agent Guide

## Purpose

This directory is the project data layer. It should contain only
hand-curated CSV, JSON, and YAML inputs that are needed to reproduce
the manuscript figures or support source-backed claims.

## Contracts

- Treat `historical_events.json` as the chronology source of truth.
- `lat` and `lon` may be `null` by design. Keep them numeric only for
  publishable public-event locations; redact both fields for Indigenous,
  archaeology-adjacent, massacre, cultural-landscape, or protected-resource
  rows.
- Keep every data-source citation resolvable in `../manuscript/references.bib`.
- Preserve schemas used by `../src/_figures/` and `../tests/test_data.py`.
- Keep `figure_provenance.csv` as the machine-readable source for figure
  source freshness, reader risk, and long descriptions; update it with
  `../manuscript/A1_figure_catalogue.md`.
- When changing 2024-2026 rows, verify the claim against an official or
  primary source before updating the row.
- Every 2024-2026 row must carry a non-empty `date_iso`, `source_tier`,
  `refresh_trigger`, `verification_status: checked_current_source`, and
  current `checked_as_of` value. Scheduled future rows are allowed only
  when `date_precision: scheduled` and the event remains phrased as a
  future public-status claim.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_data.py tests/test_figures.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

Generated outputs belong in `../output/`, not in this directory.
