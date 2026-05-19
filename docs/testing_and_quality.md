# Testing And Quality Guide

This guide explains what the Crescent City test suite proves, what it does
not prove, and which checks to run after each kind of edit.

## What A Green Build Means

A green project build means:

- Manuscript files have the expected structure.
- Citation keys resolve against `references.bib`.
- Bibliography reserve policy is explicit.
- Data files match expected schemas and current-event metadata rules.
- The 24-figure registry regenerates PNG and SVG outputs and records
  source-freshness, reader-risk, long-description, and checksum
  metadata.
- Documentation links and guarded facts have not drifted.
- The renderer can validate generated artifacts when the render stages are
  run.

A green build does not mean every historical or current-status claim has
been freshly reverified. Use `claim_ledger.md` and
`source_refresh_workflow.md` for that layer. Use
`sources_provenance_ethics.md` for source-tier and sensitive-material
boundaries.

## Test Areas

| Test file | Guards |
|---|---|
| `tests/test_documentation.py` | Markdown links, folder-level docs, figure-count drift, manuscript-shape documentation |
| `tests/test_american_english.py` | American-English wording in authored text |
| `tests/test_citations.py` | Citation extraction, missing keys, reserve bibliography policy |
| `tests/test_manuscript.py` | Heading structure, anchors, captions, manuscript conventions |
| `tests/test_figures.py` | Figure registry, output files, dimensions, deterministic contracts |
| `tests/test_pipeline.py` | Pipeline CLI behavior and report contents |
| `tests/test_pipeline_integration.py` | Integrated pipeline/render expectations and rendered-PDF smoke checks |
| `tests/test_data.py` | Data schemas, current-event metadata, source-key fields |
| `tests/test_publishing.py` | CFF, Zenodo metadata, and self-citation output |

For a data-focused view of these checks, see
`data_validation_qa.md`.

## Command Matrix

Run from `projects/crescent_city/`.

| Change | Minimum command |
|---|---|
| Documentation only | `PYTHONPATH=. uv run pytest tests/test_documentation.py tests/test_american_english.py -q` |
| Manuscript prose | `PYTHONPATH=. uv run pytest tests/test_manuscript.py tests/test_citations.py -q` |
| Citation or bibliography | `PYTHONPATH=. uv run pytest tests/test_citations.py tests/test_pipeline.py -q` |
| Data file | `PYTHONPATH=. uv run pytest tests/test_data.py -q` |
| Figure data or plotter | `PYTHONPATH=. uv run pytest tests/test_figures.py tests/test_data.py -q` |
| Rendered PDF visual smoke | `PYTHONPATH=. uv run pytest tests/test_pipeline_integration.py::TestPDFProvenance -q` |
| Publishing metadata | `PYTHONPATH=. uv run pytest tests/test_publishing.py -q` |
| Pipeline logic | `PYTHONPATH=. uv run pytest tests/test_pipeline.py tests/test_pipeline_integration.py -q` |
| Release candidate | `PYTHONPATH=. uv run pytest tests/ -q` |

Run from the template repository root when testing the project through the
same path used by repository-level scripts:

```bash
PYTHONPATH=. uv run pytest projects/crescent_city/tests/ -q
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

## Pipeline Checks

The strict project pipeline writes `output/pipeline_report.json`. The
important fields are:

| Field | Meaning |
|---|---|
| `checks_passed` / `checks_total` | Project quality gates passed |
| `total_words` | Prose-analysis word count |
| `unique_citations` | Unique cited BibTeX keys |
| `avg_fkgl` | Average Flesch-Kincaid Grade Level |
| `citation_density` | Citation tokens per 1,000 words |
| `figures_generated` | Number of figures generated |
| `figures_ok` | Whether batched figure generation completed |
| `checks` | Per-gate boolean results |

Current expected shape: 5/5 checks, 24 figures, and true
`bibliography_consistency`.

## Renderer Validation

`scripts/04_validate_output.py --project crescent_city` checks generated
artifacts after rendering. It validates PDF readability, Markdown output,
directory structure, and the figure registry. It is necessary before
sharing a rendered PDF, but it is not a replacement for source-refresh
review.

When Poppler tools are available, the integration tests also rasterize
sampled PDF pages with `pdftoppm` and assert that the pages are nonblank.
Use `visual_pdf_qa.md` for manual figure-scale and caption-flow review.

## Failure Triage

| Failure | First action |
|---|---|
| Missing citation key | Check `../manuscript/references.bib` and citation spelling |
| Unused non-reserve source | Cite it, remove it, or document it in `bibliography.reserve_keys` plus `claim_ledger.md` |
| Figure count mismatch | Check `../src/figures.py`, output files, and `../manuscript/A1_figure_catalogue.md` |
| Current-event metadata failure | Follow `source_refresh_workflow.md` |
| Source-tier mismatch | Use the exact tiers in `sources_provenance_ethics.md` |
| Documentation link failure | Resolve links relative to the file containing the link |
| Render validation failure | See `rendering_and_outputs.md` |

## Quality Posture

Prefer focused tests during editing and the full suite before handoff.
When a change crosses boundaries, run the tests for every touched
subsystem. For example, a housing project update can touch data, a
figure, citations, manuscript prose, the claim ledger, and rendering; it
needs more than a data test.
