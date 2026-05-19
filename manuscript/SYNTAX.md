# Manuscript Syntax Reference (crescent_city)

Project-specific overlay on the canonical [`docs/guides/manuscript-semantics.md`](../../../docs/guides/manuscript-semantics.md) — read that file first; this file documents **crescent_city**-specific conventions.

## Citations

Pandoc-style only. Every citation key must resolve in [`references.bib`](references.bib).

```markdown
[@goldfinger2012] provides the Cascadia turbidite chronology.
[@borrero2017; @lipton1965] document the tsunami damage.
@madley2016genocide places the Tolowa massacres within the wider California genocide.
```

Pipeline behavior:

* `bibliography.fail_on_missing: true` — a `[@citation_key]` whose key is not in `references.bib` makes the `bibliography_consistency` check fail.
* `bibliography.fail_on_unused: false` — unused entries are tolerated only
  when they have been audited. Intentional background sources belong in
  `bibliography.reserve_keys` in [`config.yaml`](config.yaml), which excludes
  them from the unused-entry count while keeping the working bibliography
  explicit.

The [`citation_density_above_floor`](../src/pipeline.py) check enforces >= `prose.citation_density_min_per_1000` citations per 1000 words.

## Section labels

Each renderable manuscript file starts with a heading that defines a
`{#sec:*}` anchor. Part files and appendices use `#`; chapter files
inside each part use `##`. Do not hand-maintain a separate section
roster in prose; the current roster is the sorted `manuscript/*.md`
tree and is validated by `tests/test_manuscript.py`.

To inspect the live roster:

```bash
rg -n '^#{1,2} .*\\{#sec:' projects/crescent_city/manuscript -g '*.md'
```

Cross-section references in prose use the `[@sec:<anchor>]` pattern, never markdown filename links.
Figure references use `[@fig:<anchor>]` and must match image attributes such
as `{#fig:historical_timeline}`.

## Heading hierarchy rules

1. **Part / appendix H1, chapter H2** — part files begin with `#`, chapter files begin with `##`, and `prose.require_h1_per_section` is intentionally false.
2. **`no_skipped_heading_levels`** — never jump from `#` to `###`, or from `##` to `####`, without the intervening level.

The Pandoc renderer uses `--number-sections`, so never write manual numbers like `## 2.1 Read`. Just write `## Read` and let Pandoc autonumber.

## `{{TOKEN}}` substitution

`scripts/z_generate_manuscript_variables.py` computes token values via `src/manuscript_variables.py::compute_variables()` and writes substituted copies of `manuscript/*.md` to `output/manuscript/` via `src.manuscript_variables.write_variables()`. This file (`SYNTAX.md`), `AGENTS.md`, and `README.md` are excluded from `output/manuscript/` so their literal `{{TOKEN}}` examples are never substituted.

| Token | Source |
|---|---|
| `{{CONFIG_TITLE}}` | `config.yaml` `paper.title` |
| `{{TOTAL_WORDS}}` | sum of `metrics.word_count` |
| `{{TOTAL_SENTENCES}}` | sum of `metrics.sentence_count` |
| `{{TOTAL_PARAGRAPHS}}` | sum of `metrics.paragraph_count` |
| `{{AVG_GRADE_LEVEL}}` | weighted-average Flesch-Kincaid Grade Level |
| `{{AVG_READING_EASE}}` | weighted-average Flesch Reading Ease |
| `{{AVG_GUNNING_FOG}}` | weighted-average Gunning Fog Index |
| `{{CITATION_COUNT}}` | unique cited keys |
| `{{FILES_ANALYZED}}` | number of files in `manuscript_report.files` |
| `{{LONGEST_SECTION_WORDS}}` | max per-file word count |
| `{{SHORTEST_SECTION_WORDS}}` | min per-file word count |

Define new tokens in [`src/manuscript_variables.py`](../src/manuscript_variables.py) and they become available everywhere.

## Preamble

[`preamble.md`](preamble.md) loads the LaTeX packages required for tables, citations, and cross-references — including `hyperref`, `cleveref`, and `natbib` with parenthetical citation punctuation. Pandoc is invoked with `--natbib` so manuscript `[@key]` citations rewrite to natbib commands against [`references.bib`](references.bib); see [`99_references.md`](99_references.md) for how the rendered bibliography is assembled.
