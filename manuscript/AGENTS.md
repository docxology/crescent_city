# manuscript/ Agent Guide

## Purpose

This directory is the source manuscript. Edits here change the rendered
PDF, HTML, review report, and manuscript metrics.

## Publication and policy (`config.yaml`)

- Title, subtitle, authors, DOI: see [`config.yaml`](config.yaml) (`paper`,
  `authors`, `publication`). Scholarly DOI is currently
  `10.5281/zenodo.20286171`.
- Prose gates: `prose.target_grade_level_*`, `long_sentence_threshold`,
  `citation_density_min_per_1000`, `require_h1_per_section` (false for this
  book), `forbid_skipped_levels`.
- Bibliography: `bibliography.references_path`, `fail_on_missing`,
  `fail_on_unused`, `reserve_keys`.

## Section roster (signposts)

Renderable markdown sections (58 files): abstract and introduction; four Part
openers (`02_space`, `20_time`, `40_people`, `60_ideas`) plus **46** topical
chapters in bands `03`–`11`, `21`–`35`, `41`–`52`, `61`–`69`, and `70_conclusion`;
then `71_timeline`, `72_methodology`, `73_reproducibility`; `99_references`;
`A1_figure_catalogue`, `A2_glossary`.

Meta-only in this folder (not counted as narrative sections): `AGENTS.md`,
`README.md`, `SYNTAX.md`, `preamble.md` (LaTeX wrapper).

Inspect live anchors:

```bash
rg -n '^#{1,2} .*\{#sec:' projects/crescent_city/manuscript -g '*.md'
```

## Contracts

- Preserve existing `{#sec:…}` IDs unless every `[@sec:…]` reference and test
  expectation is updated in the same change. Use underscores consistently in
  anchors (no mixing `sec:foo_bar` with `sec:foo-bar`).
- Cross-references: `[@sec:…]` for sections, `[@fig:…]` for figures — match
  embedded figure attributes such as `{#fig:…}`.
- Citations: Pandoc `[@key]` only; every key must resolve in `references.bib`
  when `fail_on_missing` is true.
- Keep American English; avoid `**bold**` in prose (italics where emphasis is needed).
- Keep every factual addition source-backed; prefer official or primary sources
  for current events.
- Treat `output/manuscript/` (under the project root) as generated — never hand-edit
  substituted copies there.

## `{{TOKEN}}` substitution

[`scripts/z_generate_manuscript_variables.py`](../scripts/z_generate_manuscript_variables.py)
writes token-substituted markdown to `output/manuscript/`. This file,
`README.md`, and `SYNTAX.md` are excluded so examples containing `{{TOKEN}}`
are not corrupted. Token definitions: [`SYNTAX.md`](SYNTAX.md) table and
[`src/manuscript_variables.py`](../src/manuscript_variables.py).

## Figures

Embedded figures use `[@fig:…]` and must align with the registry in
[`src/figures.py`](../src/figures.py) and the narrative catalog in
[`A1_figure_catalogue.md`](A1_figure_catalogue.md) (`[@sec:figure_catalogue]`).

## Checks

From `projects/crescent_city/`:

```bash
PYTHONPATH=. uv run pytest tests/test_manuscript.py tests/test_citations.py tests/test_american_english.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

When changing current-event claims, rerender and scan the final PDF text
for stale dates or unresolved references.
