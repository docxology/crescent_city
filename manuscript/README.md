# Manuscript Directory

This directory contains the hand-authored manuscript source for the Crescent
City history project.

## Publication metadata

Authoritative title, subtitle, DOI, and licenses live in [`config.yaml`](config.yaml).
Current scholarly artifact:
[Crescent City history Zenodo DOI](https://doi.org/10.5281/zenodo.20286171)
(`publication.doi`). Manuscript text is CC-BY-4.0; project code is Apache-2.0 (`../LICENSE`); data
licensing is described under `metadata.data_license` in `config.yaml`.

## Structure and roster

There are **62** `*.md` files here. **58** are renderable scholarly sections
(combined into the PDF): abstract through reproducibility, references, and two
appendices. **Four** are authoring meta only (this file, `AGENTS.md`,
`SYNTAX.md`, and LaTeX-only [`preamble.md`](preamble.md) — not prose chapters).

Countable layout:

| Block | Pattern | Role |
| --- | --- | --- |
| Front matter | `00_abstract`, `01_introduction` | Summary and framing |
| Part I — Space | `02_space` + `03`–`11` | Part opener + 9 chapters |
| Part II — Time | `20_time` + `21`–`35` | Part opener + 15 chapters |
| Part III — People | `40_people` + `41`–`52` | Part opener + 12 chapters |
| Part IV — Ideas | `60_ideas` + `61`–`73` | Part opener + 13 chapters |
| Back matter | `99_references`, `A1_figure_catalogue`, `A2_glossary` | Bibliography anchor, figure catalog, glossary |

The manuscript describes **46 topical chapters** (Part chapter files `03`–`11`,
`21`–`35`, `41`–`52`, `61`–`69`, plus `70_conclusion`), distinct from the
introduction, timeline (`71`), methodology (`72`), and reproducibility (`73`).

Numbered chapter files carry stable section anchors such as `{#sec:cascadia}`.
Part openers and appendices use `#` (H1); chapters under each Part use `##` (H2).
`config.yaml` sets `prose.require_h1_per_section: false` for this continuous-book
layout.

## Supporting files

- [`references.bib`](references.bib) — curated BibTeX; build fails on missing
  cited keys (`bibliography.fail_on_missing: true` in `config.yaml`).
- [`preamble.md`](preamble.md) — LaTeX preamble for Pandoc PDF output.
- [`SYNTAX.md`](SYNTAX.md) — citations, anchors, heading rules, `{{TOKEN}}`
  substitution.

`SYNTAX.md`, `AGENTS.md`, and this `README.md` are excluded from token
substitution into `output/manuscript/` so literal `{{TOKEN}}` examples stay intact.

## Authoring rules

- Use Pandoc citations (`[@key]`) and cross-references (`[@sec:…]`, `[@fig:…]`),
  not hard-coded section or figure numbers.
- Keep Part files at H1 and chapter files at H2; do not skip heading levels
  (`prose.forbid_skipped_levels: true`).
- Add new citations to `references.bib` before prose depends on them.
- Do not edit files under `../output/manuscript/`; those are generated copies.

See [`SYNTAX.md`](SYNTAX.md) for project-specific citation, anchor, and token rules.
See [`../docs/manuscript_authoring.md`](../docs/manuscript_authoring.md)
for the full authoring workflow and evidence-language guidance.
Use [`../docs/sources_provenance_ethics.md`](../docs/sources_provenance_ethics.md)
for source-tier, reuse, and sensitive-material boundaries before adding
new public-history claims.

## Checks

Run from `projects/crescent_city/` with `PYTHONPATH=.` (repository root on path):

```bash
PYTHONPATH=. uv run pytest tests/test_manuscript.py tests/test_citations.py tests/test_american_english.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

For release-facing spot checks, see
[`../docs/accessibility_reader_experience.md`](../docs/accessibility_reader_experience.md)
and [`../docs/publication_checklist.md`](../docs/publication_checklist.md).
