# Scripts Directory

This directory contains thin command-line orchestrators for the Crescent City
project. Business logic belongs in `../src/`; scripts should parse arguments,
resolve paths, and call importable functions.

## Scripts

| Script | Role |
|---|---|
| `run_history_pipeline.py` | Runs prose checks, bibliography checks, figures, review report, and publishing metadata |
| `y_generate_history_figures.py` | Regenerates the registered 24-figure suite |
| `z_generate_manuscript_variables.py` | Writes substituted manuscript files and renderer variables |

## Common Commands

```bash
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only
PYTHONPATH=. uv run python scripts/z_generate_manuscript_variables.py
```

For the full render/copy-out path, see
[`../docs/rendering_and_outputs.md`](../docs/rendering_and_outputs.md).
For release sequencing, see
[`../docs/publication_checklist.md`](../docs/publication_checklist.md).
For environment assumptions and archival policy, see
[`../docs/environment_reproducibility.md`](../docs/environment_reproducibility.md)
and [`../docs/release_archival_versioning.md`](../docs/release_archival_versioning.md).
