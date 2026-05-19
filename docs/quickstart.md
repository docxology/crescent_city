# Quickstart

Run commands from the template repository root unless a command says
otherwise.

For system tool assumptions and project-root versus repository-root
details, see [environment_reproducibility.md](environment_reproducibility.md).

## First Run

```bash
uv sync

# Project quality pipeline: prose checks, bibliography consistency,
# 24 PNG/SVG figure pairs, review report, and publication metadata.
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict

# Project tests only.
PYTHONPATH=. uv run pytest projects/crescent_city/tests/ -q
```

## Common Commands

```bash
# Inspect project pipeline stages.
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --list

# Figure-only path. This writes 24 PNG files and 24 SVG siblings.
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --figures-only

# Hydrate manuscript variables into projects/crescent_city/output/manuscript/.
PYTHONPATH=. uv run python projects/crescent_city/scripts/z_generate_manuscript_variables.py

# Regenerate figures through the dedicated thin orchestrator.
PYTHONPATH=. uv run python projects/crescent_city/scripts/y_generate_history_figures.py
```

## Render The Paper

```bash
# Render combined PDF, combined HTML, per-section HTML, and per-section slides.
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city

# Validate rendered artifacts, Markdown, output structure, and figure registry.
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city

# Copy project outputs to output/crescent_city/ at the repository root.
PYTHONPATH=. uv run python scripts/05_copy_outputs.py --project crescent_city
```

The main rendered PDF is:

```text
projects/crescent_city/output/pdf/crescent_city_combined.pdf
```

After the copy stage, the release-facing copy is:

```text
output/crescent_city/crescent_city_combined.pdf
```

See `rendering_and_outputs.md` for the full renderer/output runbook.

## Alternate Project Root

Use this when testing a copied project tree.

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py \
  --project-root /tmp/crescent_city_copy \
  --config manuscript/config.yaml \
  --strict
```

## Output Cheat Sheet

Primary outputs land under `projects/crescent_city/output/`.

| Output | Purpose |
|---|---|
| `pipeline_report.json` | Machine-readable quality-gate summary |
| `manuscript_report.json` | Prose metrics snapshot |
| `review_report.md` | Human-readable editorial review |
| `figures/*.png` and `figures/*.svg` | 24 deterministic figure pairs |
| `data/manuscript_variables.json` | Renderer-facing manuscript variables |
| `pdf/crescent_city_combined.pdf` | Project-local combined PDF |
| `web/index.html` | Combined HTML manuscript |
| `reports/validation_report.md` | Validation summary after `04_validate_output.py` |
| `CITATION.cff`, `zenodo_metadata.json`, `self_citation.bib` | Publication metadata |

## Which Command Should I Run?

| Situation | Command |
|---|---|
| I changed prose, citations, data, or figures | `projects/crescent_city/scripts/run_history_pipeline.py --strict` |
| I changed only plotting code or figure data | `projects/crescent_city/scripts/run_history_pipeline.py --figures-only`, then targeted tests |
| I changed docs only | `uv run pytest projects/crescent_city/tests/test_documentation.py projects/crescent_city/tests/test_american_english.py -q` |
| I need a PDF for reading | `scripts/03_render_pdf.py --project crescent_city` |
| I need a release handoff folder | render, validate, then `scripts/05_copy_outputs.py --project crescent_city` |

## Fast Troubleshooting

| Symptom | First check |
|---|---|
| Missing figure during render | Run the strict project pipeline or the figure-only command. |
| Citation failure | Check the cited key in `manuscript/references.bib` and `manuscript/SYNTAX.md`. |
| Documentation link failure | Run `tests/test_documentation.py` and fix the relative link target. |
| Stale current-event claim | Follow `source_refresh_workflow.md`, `sources_provenance_ethics.md`, and `claim_ledger.md`. |
| PDF compiles but release folder is missing | Run `scripts/05_copy_outputs.py --project crescent_city`. |
