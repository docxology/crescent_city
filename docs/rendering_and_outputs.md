# Rendering And Outputs

This runbook covers the shared renderer path for the Crescent City paper:
PDF, HTML, slides, validation, and copy-out.

For the quality checks that should precede a public render, see
`testing_and_quality.md`, `accessibility_reader_experience.md`, and
`publication_checklist.md`.

## Render Sequence

Run from the template repository root.

```bash
# 1. Make sure project analysis and figures are current.
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict

# 2. Render the combined PDF, combined HTML, per-section HTML, and slides.
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city

# 3. Validate outputs.
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city

# 4. Copy outputs to the repository-level release folder.
PYTHONPATH=. uv run python scripts/05_copy_outputs.py --project crescent_city
```

## What The Renderer Does

`scripts/03_render_pdf.py --project crescent_city` performs these steps:

1. Hydrates manuscript variables by running
   `projects/crescent_city/scripts/z_generate_manuscript_variables.py`.
2. Writes substituted manuscript copies to
   `projects/crescent_city/output/manuscript/`.
3. Checks required LaTeX packages and available figure files.
4. Renders per-section slides and HTML.
5. Combines 58 manuscript files into the main PDF.
6. Processes `references.bib` with BibTeX.
7. Renders the combined HTML manuscript.

Do not edit `output/manuscript/` to fix render issues. Edit the source
file in `manuscript/`, the variables generator, data, figures, or
preamble as appropriate.

## Main Outputs

| Path | Meaning |
|---|---|
| `projects/crescent_city/output/pdf/crescent_city_combined.pdf` | Project-local combined PDF |
| `projects/crescent_city/output/web/index.html` | Combined HTML manuscript |
| `projects/crescent_city/output/web/*.html` | Per-section HTML |
| `projects/crescent_city/output/slides/*_slides.pdf` | Per-section Beamer slides |
| `projects/crescent_city/output/reports/validation_report.md` | Validation summary |
| `output/crescent_city/crescent_city_combined.pdf` | Repository-level release copy after `05_copy_outputs.py` |

The current rendered PDF path is intentionally repeated in quickstart docs
because it is the file most readers need.

## Validation Meaning

`scripts/04_validate_output.py --project crescent_city` checks:

- PDF files are readable.
- Markdown validation passes.
- Output directories exist and have expected structure.
- The figure registry matches generated outputs.

Validation is an artifact check. It does not replace source freshness
review for volatile claims.

## Copy-Out Meaning

`scripts/05_copy_outputs.py --project crescent_city` copies the project
output tree into `output/crescent_city/` at the repository root and places
the combined PDF at:

```text
output/crescent_city/crescent_city_combined.pdf
```

Use the copy-out folder for handoff. Use the project-local `output/`
folder while developing.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Renderer reports a missing figure | Project pipeline or figure-only generation has not been run | Run the strict pipeline or `--figures-only` |
| PDF build fails after variable hydration | Hydrated Markdown exposed a LaTeX or Pandoc issue | Inspect the source Markdown and `output/pdf/_combined_manuscript.tex` for context, then edit source |
| Citations render incorrectly | Missing or malformed BibTeX key | Run citation tests and inspect `manuscript/references.bib` |
| Combined PDF exists but release folder does not | Copy stage has not been run | Run `scripts/05_copy_outputs.py --project crescent_city` |
| Validation passes but a current claim is stale | Validation checks artifact structure, not fresh public records | Follow `source_refresh_workflow.md` |

## Minimal PDF-Only Path

When you only need to check whether the paper compiles:

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
```

Before sharing the artifact, run validation and copy-out as well.
