# Rendering And Outputs

This runbook covers the shared renderer path for the Crescent City paper:
PDF, HTML, slides, validation, and copy-out.

For the quality checks that should precede a public render, see
`testing_and_quality.md`, `accessibility_reader_experience.md`, and
`publication_checklist.md`.

## Render Sequence

Use the [quickstart](quickstart.md) to set up and register the project in the
pinned Template checkout. From the registered project root, prepare its
figures and manuscript variables in the configured project environment. Set
`TEMPLATE_REPO_ROOT` to the pinned Template checkout.

```bash
export TEMPLATE_REPO_ROOT=/absolute/path/to/pinned/template
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
uv run python scripts/z_generate_manuscript_variables.py
```

From the Template checkout root, render from those prepared inputs, validate,
and copy the deliverables.

```bash
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/crescent_city --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/crescent_city
uv run --no-sync python scripts/pipeline/stage_05_copy.py --project working/crescent_city
```

## What The Renderer Does

The project’s variable generator writes substituted files to
`output/manuscript/`. Stage 03 uses those files because the command above
skips its hydration hook. It checks the figure paths and renders the
configured PDF, HTML, and slides using the manuscript bibliography.

Edit the source in `docs/manuscript/` or the relevant generator or input when
correcting a render defect.

## Main Outputs

| Path | Meaning |
|---|---|
| `output/pdf/crescent_city_combined.pdf` | Project-local combined PDF |
| `output/web/index.html` | Combined HTML manuscript |
| `output/web/*.html` | Per-section HTML |
| `output/slides/*_slides.pdf` | Per-section Beamer slides |
| `output/reports/validation_report.md` | Validation summary |
| `output/working/crescent_city/crescent_city_combined.pdf` | Template-root release copy after `scripts/pipeline/stage_05_copy.py` |

The current rendered PDF path is intentionally repeated in quickstart docs
because it is the file most readers need.

## Validation Meaning

`scripts/pipeline/stage_04_validate.py --project working/crescent_city` checks:

- PDF files are readable.
- Markdown validation passes.
- Output directories exist and have expected structure.
- The figure registry matches generated outputs.
- The evidence registry checks citations and support for numbers in the manuscript.
- The output manifest checks the generated artifact inventory.

Check numerical claims against the cited source and its units, date range,
and scope. Review volatile claims against current public records before
release.

## Copy-Out Meaning

`scripts/pipeline/stage_05_copy.py --project working/crescent_city` copies the project
output tree into `output/working/crescent_city/` under the Template checkout and places
the combined PDF at:

```text
output/working/crescent_city/crescent_city_combined.pdf
```

Use the copy-out folder for handoff. Use the project-local `output/`
folder while developing.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Renderer reports a missing figure | Project pipeline or figure-only generation has not been run | Run the strict pipeline or `--figures-only` |
| PDF build fails after variable hydration | Hydrated Markdown exposed a LaTeX or Pandoc issue | Inspect the source Markdown and `output/pdf/_combined_manuscript.tex` for context, then edit source |
| Citations render incorrectly | Missing or malformed BibTeX key | Run citation tests and inspect `docs/manuscript/references.bib` |
| Combined PDF exists but release folder does not | Copy stage has not been run | Run `scripts/pipeline/stage_05_copy.py --project working/crescent_city` |
| Validation passes but a current claim is stale | Validation checks artifact structure, not fresh public records | Follow `source_refresh_workflow.md` |

## Render From Prepared Inputs

With hydrated project inputs already prepared, run Stage 03 from the
Template checkout root:

```bash
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/crescent_city --skip-manuscript-hydration
```

Before sharing the artifact, run validation and copy-out as well.
