# Manuscript Authoring Guide

This guide explains how to edit the Crescent City manuscript without
breaking citation integrity, cross-references, figure contracts, or the
project's evidence-language discipline.

Use `../manuscript/SYNTAX.md` for syntax examples. Use this guide for the
authoring workflow and review expectations.

## Source Files

Hand-authored source files live in `../manuscript/`.

| File group | Role |
|---|---|
| `00_abstract.md`, `01_introduction.md` | Front matter and research frame |
| `02_*` through `11_*` | Part I, Space |
| `20_*` through `35_*` | Part II, Time |
| `40_*` through `52_*` | Part III, People |
| `60_*` through `73_*` | Part IV, Ideas, methods, reproducibility |
| `A1_figure_catalogue.md`, `A2_glossary.md` | Appendices |
| `99_references.md` | Rendered references section shell |
| `references.bib` | Bibliography |
| `config.yaml` | Metadata, prose thresholds, bibliography policy |
| `preamble.md` | LaTeX support for rendering |

Do not edit `../output/manuscript/`; those files are hydrated copies.

## Heading And Anchor Rules

- Part and appendix files use H1 headings.
- Chapter files use H2 headings.
- Every renderable manuscript file should define a `{#sec:*}` anchor.
- Cross-section references use `[@sec:anchor]`.
- Figure references use `[@fig:anchor]`.
- Do not hard-code section or figure numbers; Pandoc numbers them during
  rendering.

## Citations

Use Pandoc citation syntax:

```markdown
[@goldfinger2012] provides the Cascadia turbidite chronology.
[@borrero2017; @lipton1965] document the tsunami damage.
@madley2016genocide places the Tolowa massacres within the wider California genocide.
```

Before prose depends on a source, add the key to
`../manuscript/references.bib`. If a source is intentionally kept uncited
as a background or update-trail source, list it in `bibliography.reserve_keys`
in `../manuscript/config.yaml` and document the reason in
`claim_ledger.md`.

## Evidence Language

Match the verb to the source type.

| Evidence type | Use language like | Avoid |
|---|---|---|
| Measured record | "measured," "recorded," "reported by [agency]" | Treating a measurement as a permanent general truth |
| Model or scenario | "modeled," "projected," "scenario," "planning estimate" | "Will" or "proves" |
| Current public status | "as of [date]," "proposed," "scheduled," "pending," "adopted" | Writing proposed or scheduled events as completed |
| Local journalism | "reported by," "local reporting indicates" | Using it for technical, legal, or scientific certainty |
| Indigenous public source | Name the public or authorized source carefully | Replacing tribal self-description with outside synthesis |
| Schematic figure | "schematic," "not survey-grade," "layout" | Treating the visual as a measured map |

## Current-Event Edits

Before changing 2024 onward civic, environmental, project-status, court,
grant, election, fishery, or agency rows:

1. Follow `source_refresh_workflow.md`.
2. Update `../data/historical_events.json`.
3. Update source keys in `../manuscript/references.bib`.
4. Update `35_currents.md`, `71_timeline.md`, and captions if needed.
5. Regenerate figures if dates, categories, or labels changed.

## Manuscript Variables

Tokens such as `{{TOTAL_WORDS}}` are computed by
`../src/manuscript_variables.py` and hydrated by
`../scripts/z_generate_manuscript_variables.py`. Use variables for
pipeline-derived metrics rather than hand-authoring counts that can drift.

Hydrate variables:

```bash
PYTHONPATH=. uv run python scripts/z_generate_manuscript_variables.py
```

From the repository root:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/z_generate_manuscript_variables.py
```

## Review Before Render

Run from `projects/crescent_city/`:

```bash
PYTHONPATH=. uv run pytest tests/test_manuscript.py tests/test_citations.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

Run from the repository root when preparing the final artifact:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Adding a citation key only in prose | Add the BibTeX entry and run citation tests |
| Editing hydrated output files | Edit source files in `../manuscript/` |
| Writing "will happen" for scheduled events | Use scheduled or proposed language until official records update |
| Adding a figure without updating the catalog | Update `A1_figure_catalogue.md` and tests/docs if count changed |
| Hand-authoring pipeline counts | Use manuscript variables or cite the pipeline report |
