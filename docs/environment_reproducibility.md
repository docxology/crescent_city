# Environment And Reproducibility

This guide describes the environment needed to reproduce the Crescent
City checks, figures, metadata, PDF, and copied release artifacts. It
documents the current path; it does not introduce a container, CI job, or
new dependency source.

## Supported Working Paths

Most project-local commands run from:

```bash
cd projects/crescent_city
```

Renderer and copy-out commands run from the template repository root:

```bash
cd /path/to/template
```

Use `PYTHONPATH=.` in root commands so shared infrastructure imports are
resolved exactly as the repository scripts expect.

## Toolchain

| Tool | Why it is needed | Source of truth |
|---|---|---|
| Python 3.10 or newer | Project package and tests | `pyproject.toml` and `../../pyproject.toml` |
| `uv` | Dependency sync and command runner | Repository workflow |
| Pandoc | Markdown-to-PDF/HTML assembly | Shared renderer |
| XeLaTeX and BibTeX | PDF typesetting and bibliography pass | Shared renderer |
| `pandoc-crossref` | Figure and section cross-reference processing | Shared renderer |
| Matplotlib, pandas, PyYAML, textstat | Project analysis and figures | `pyproject.toml` |

After `uv sync`, the project is intended to run without internet access.
Network access should not be required for tests, figure generation,
metadata generation, or rendering.

## Initial Setup

From the template repository root:

```bash
uv sync
```

Then run a project-local smoke check:

```bash
cd projects/crescent_city
PYTHONPATH=. uv run pytest tests/test_documentation.py tests/test_american_english.py -q
```

If the renderer fails later because Pandoc or LaTeX tools are missing,
install those system tools outside `uv`; they are not Python
dependencies.

## Reproduction Commands

Run the strict project pipeline from the project directory:

```bash
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

Regenerate figures only:

```bash
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only
```

Hydrate manuscript variables:

```bash
PYTHONPATH=. uv run python scripts/z_generate_manuscript_variables.py
```

Render, validate, and copy from the template repository root:

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
PYTHONPATH=. uv run python scripts/05_copy_outputs.py --project crescent_city
```

## Determinism Boundary

The reproducibility contract is structural and source-linked.

| Output | Determinism expectation |
|---|---|
| SVG figures | Used for bit-for-bit determinism checks. |
| PNG figures | Visually deterministic; embedded metadata can vary across `matplotlib` or `libpng` versions. |
| `output/pipeline_report.json` | Deterministic for the same source tree and dependency set. |
| `output/CITATION.cff`, `output/zenodo_metadata.json`, `output/self_citation.bib` | Derived from `manuscript/config.yaml`. |
| PDF | Should render consistently, but exact bytes can vary with TeX, fonts, timestamps, and platform packages. |

When bit-for-bit reproduction matters, compare source files, JSON
reports, and SVG outputs before comparing PDF bytes.

## Artifact Locations

| Path | Role |
|---|---|
| `output/pipeline_report.json` | Project quality summary |
| `output/review_report.md` | Human-readable project review |
| `output/figures/` | Regenerated PNG and SVG figure files |
| `output/data/manuscript_variables.json` | Render-time variable payload |
| `output/pdf/crescent_city_combined.pdf` | Project-local combined PDF |
| `output/web/index.html` | Project-local combined HTML |
| `output/reports/validation_report.md` | Renderer validation report |
| `../../output/crescent_city/crescent_city_combined.pdf` | Repository-level release copy |

Do not edit any file in `output/` as source. Rebuild it from
`manuscript/`, `data/`, `src/`, and `scripts/`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: infrastructure` | Command was run from the wrong directory or without `PYTHONPATH=.` | Run from the template root for renderer commands, or from the project directory for project-local commands. |
| `pandoc` or `xelatex` missing | System renderer dependency is absent | Install the system toolchain and rerun `scripts/03_render_pdf.py`. |
| Figure count mismatch | Registry, manuscript catalog, generated files, or docs drifted | Run figure tests and follow [figure_maintenance.md](figure_maintenance.md). |
| Current-event test fails | `checked_as_of`, `source_tier`, or `refresh_trigger` is stale or malformed | Follow [source_refresh_workflow.md](source_refresh_workflow.md). |
| Validation passes but a claim is stale | Artifact validation cannot verify fresh public records | Use [sources_provenance_ethics.md](sources_provenance_ethics.md) and [claim_ledger.md](claim_ledger.md). |

## Future Environment Work

A future infrastructure pass may add a container or lockstep system
dependency manifest. Until then, do not document a Docker or
environment-file workflow as required for Crescent City reproduction.
