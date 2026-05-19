# src/_figures/ Agent Guide

## Purpose

This package owns figure rendering. Every public plotter should be
registered in `../figures.py` and documented in
`../../manuscript/A1_figure_catalogue.md`.

## Contracts

- Preserve the 24-figure registry unless explicitly changing the manuscript
  figure contract.
- Do not hard-code generated-output paths; accept `output_dir` parameters.
- Use checked-in data from `../../data/` for factual series; deterministic
  parametric inputs are only for schematic geometry and label layout.
- Keep source notes and captions honest about measured, modeled, estimated,
  schematic, or provisional data.
- Keep `../../data/figure_provenance.csv` and
  `../../manuscript/A1_figure_catalogue.md` synchronized when a figure's
  source freshness, reader risk, or long description changes.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_figures.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only
```
