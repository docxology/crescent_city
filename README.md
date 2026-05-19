# crescent_city

A comprehensive, reproducible scholarly history of **Crescent City,
California** — from twelve generations of Tolowa Dee-ni' habitation
through the genocidal settlement era, the 130-year industrial timber
and fishing economy, the 1964 Alaska tsunami that destroyed the
downtown, and into the present condition of a community of roughly
6,400 residents (2026 estimate; 6,673 at the 2020 Census), including
prison group quarters, living on the locked
southern segment of the **Cascadia subduction zone**.

The manuscript spans **46 topical chapters** inside four nested-systems
Parts — **Space, Time, People, and Ideas** — plus abstract,
introduction, timeline, methods, reproducibility, references, and two
appendices. It includes **24 reproducible figures**, a curated
BibTeX bibliography validated during each build, and a typeset PDF
rendered via Pandoc + XeLaTeX + pandoc-crossref.

Built on the
[Research Project Template](https://github.com/docxology/template) using
`infrastructure/prose/` for editorial quality checks,
`infrastructure/reference/` for bibliography validation, and
`infrastructure/rendering/` for PDF assembly.

Public source and release artifacts are published at
[`docxology/crescent_city`](https://github.com/docxology/crescent_city);
the archival DOI is `10.5281/zenodo.20286171`.

## Quick Start

```bash
# From the repository root
uv sync

# Run the full prose-review pipeline (offline, no Ollama)
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/run_history_pipeline.py

# Strict mode: exit non-zero if any check fails
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/run_history_pipeline.py --strict

# Regenerate all 24 figures
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/y_generate_history_figures.py

# Hydrate manuscript variables for the abstract
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/z_generate_manuscript_variables.py

# Render and validate the full PDF through the shared infrastructure
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

## Manuscript Scope

The table of contents is organized around nested systems and emergence:
each Part asks a different question about the same place, then links
outward to the other Parts where the systems interact.

| Block | Sections | Subject |
|---|---|---|
| Front matter | Abstract; introduction | Setting and research questions |
| Part I — Space | Earth systems; Cascadia margin; sea level; Smith River ecology; redwood parks; oil spill risk; seawall engineering; housing; transportation | Physical and built settings from plate boundary to townsite |
| Part II — Time | Archaeology; contact; first American decade; gold rush; lumber; logging technology; fishing; railroad; economic history; agriculture; 1964 tsunami; tsunami in Pacific-wide warning policy; Tōhoku; wildfire; recent currents | Long chronology, path dependence, extraction, disaster, and adaptation |
| Part III — People | Tolowa Dee-ni'; Nee-dash; neighboring tribal nations; immigrant communities; governance; county institutions; military; World War II; education; religion; demographics; healthcare and social services | Communities, institutions, sovereignty, migration, and public life |
| Part IV — Ideas | Zoning; resilience; Klamath dam removal; Jefferson; modern economy; culture; arts; tourism; Klamath Knot; conclusion; timeline; methodology; reproducibility | Rules, meanings, restoration, memory, political imagination, and evidence |

Plus appendices: **A1 Figure Catalog**, **A2 Glossary**.

## Figures (24)

Every figure is generated deterministically by a Python plotter
registered in `src/figures.py`. The complete catalog lives in the
[manuscript appendix](manuscript/A1_figure_catalogue.md); the
following table is the operational reference:

| # | Function | Topic |
|---|---|---|
| 1 | `plot_section_word_counts` | Manuscript word count per section |
| 2 | `plot_readability_metrics` | FRE and FKGL per section |
| 3 | `plot_citation_density` | Citations per 1,000 words |
| 4 | `plot_nested_systems_map` | Space–Time–People–Ideas systems architecture |
| 5 | `plot_population_trend` | Population 1850–2026 |
| 6 | `plot_economic_sectors` | Employment by sector 1990–2020 |
| 7 | `plot_tsunami_timeline` | Recorded tsunamis 1700–2022 |
| 8 | `plot_disaster_impact` | Tsunami death-toll comparison |
| 9 | `plot_tsunami_inundation_diagram` | 1964 four-wave sequence |
| 10 | `plot_historical_timeline` | Two-century event chronology |
| 11 | `plot_regional_map` | Del Norte County reference map |
| 12 | `plot_tolowa_villages_map` | Non-coordinate Tolowa public place relationships |
| 13 | `plot_redwood_decline_chart` | Old-growth coast redwood 1850–2025 |
| 14 | `plot_cascadia_paleoseismology` | 10,000-year Cascadia turbidite record |
| 15 | `plot_jefferson_map` | State of Jefferson territory |
| 16 | `plot_climograph` | Monthly temperature, precipitation, wet days |
| 17 | `plot_harbor_timeline` | Harbor engineering and disaster events |
| 18 | `plot_currents_timeline` | Domain-stratified 2024–2026 civic events |
| 19 | `plot_sea_level_scenarios` | Sea-level evidence classes and planning ranges |
| 20 | `plot_smith_river_protection` | Smith River Wild and Scenic protection miles |
| 21 | `plot_housing_pipeline` | 2024–2026 affordable-housing pipeline |
| 22 | `plot_last_chance_grade_profile` | Last Chance Grade tunnel and repair metrics |
| 23 | `plot_archaeology_evidence_ladder` | Archaeological evidence classes without site disclosure |
| 24 | `plot_rural_health_access_network` | Rural health and transfer-service network |

## Architecture

```
projects/crescent_city/
|-- manuscript/              # Numbered Markdown sources + appendices + references.bib
|   |-- 00_abstract.md ... 73_reproducibility.md
|   |-- A1_figure_catalogue.md     # Per-figure catalog
|   |-- A2_glossary.md             # Technical-term glossary
|   |-- config.yaml                # Editorial-policy knobs
|   |-- preamble.md                # LaTeX preamble (xelatex)
|   |-- references.bib             # Curated BibTeX bibliography
|   `-- SYNTAX.md                  # Pandoc citation conventions
|-- src/                     # Domain Python package
|   |-- config.py            # Typed YAML loader
|   |-- pipeline.py          # Read -> analyze -> cross-check
|   |-- figures.py           # 24-figure public API + registry
|   |-- _figures/            # Plotter submodules
|   |   |-- _style.py            # Wong 2011 palette + rcParams
|   |   |-- _io.py               # PNG+SVG persistence helper
|   |   |-- manuscript_metrics.py
|   |   |-- systems.py
|   |   |-- demographics.py
|   |   |-- tsunami.py
|   |   |-- history.py
|   |   |-- cartography.py
|   |   |-- conservation.py
|   |   |-- geophysics.py
|   |   |-- political_geography.py
|   |   |-- climate.py
|   |   |-- harbor_history.py
|   |   |-- ecology.py
|   |   |-- community_systems.py
|   |   `-- currents.py
|   |-- manuscript_variables.py
|   |-- checks.py
|   |-- publishing.py
|   `-- report.py
|-- scripts/                 # Thin orchestrators
|   |-- run_history_pipeline.py
|   |-- y_generate_history_figures.py
|   `-- z_generate_manuscript_variables.py
|-- tests/                   # pytest suite, no mocks
|-- data/                    # CSV / JSON / YAML inputs with source metadata
|   |-- population_data.csv
|   |-- economic_sectors.csv
|   |-- climate_normals_1991_2020.csv
|   |-- tsunami_events.csv
|   |-- historical_events.json      # Event chronology with source keys + audit metadata
|   |-- currents_categories.yaml
|   `-- ...
`-- output/                  # Regeneratable; ignored by git
    |-- figures/             # 24 x {PNG, SVG}
    |-- pdf/                 # crescent_city_combined.pdf
    `-- *.json, *.md
```

## Directory-Level Documentation

Every authored directory has a concise public `README.md` and an
agent-facing `AGENTS.md` contract.

| Directory | README | Agent guide |
|---|---|---|
| `data/` | [data/README.md](data/README.md) | [data/AGENTS.md](data/AGENTS.md) |
| `docs/` | [docs/README.md](docs/README.md) | [docs/AGENTS.md](docs/AGENTS.md) |
| `manuscript/` | [manuscript/README.md](manuscript/README.md) | [manuscript/AGENTS.md](manuscript/AGENTS.md) |
| `scripts/` | [scripts/README.md](scripts/README.md) | [scripts/AGENTS.md](scripts/AGENTS.md) |
| `src/` | [src/README.md](src/README.md) | [src/AGENTS.md](src/AGENTS.md) |
| `src/_figures/` | [src/_figures/README.md](src/_figures/README.md) | [src/_figures/AGENTS.md](src/_figures/AGENTS.md) |
| `tests/` | [tests/README.md](tests/README.md) | [tests/AGENTS.md](tests/AGENTS.md) |

## Configuration

Every editorial-policy knob lives in `manuscript/config.yaml`:

| Section | Key | Default | Meaning |
|---|---|---|---|
| `prose` | `target_grade_level_min` / `_max` | `12.0 / 20.0` | Acceptable Flesch-Kincaid Grade Level band |
| `prose` | `long_sentence_threshold` | `35` | Words per sentence above which sentences are flagged |
| `prose` | `citation_density_min_per_1000` | `3.0` | Minimum citations per 1000 words |
| `prose` | `require_h1_per_section` | `false` | Part files use H1 and chapter files use H2; cross-reference tests enforce anchors |
| `prose` | `forbid_skipped_levels` | `true` | Heading levels must be contiguous |
| `bibliography` | `references_path` | `manuscript/references.bib` | Path to BibTeX file |
| `bibliography` | `fail_on_missing` | `true` | Fail if a cited `[@key]` is not in the bib |
| `bibliography` | `fail_on_unused` | `false` | Uncited entries must either be cited or listed as audited `reserve_keys` |

## Reproducibility Contract

The pipeline is governed by three commitments:

1. **Determinism** — identical inputs produce byte-identical SVG
   outputs (the canonical format the test suite hashes). Each figure
   pass also writes `output/figures/figure_manifest.json`, recording
   figure metadata, source data inputs, source freshness, reader risk,
   long descriptions, and PNG/SVG SHA-256 hashes without timestamps.
   Companion PNGs are visually identical but their
   bytes may differ across `matplotlib`/`libpng` versions due to
   embedded metadata; rely on SVG when bit-for-bit reproduction matters.
2. **Self-containment** — the pipeline runs without internet access
   after the initial `uv sync`.
3. **Transparency** — every figure, every cited number, and every
   pipeline gate is traceable to its source through the manuscript
   figure catalog appendix.

The test suite validates:

- 24 figures are produced; each has a matching SVG sibling and
  exceeds 5 KB
- The figure manifest records all 24 registry entries, declared data
  inputs, evidence classes, provenance fields, long descriptions, and
  output hashes
- The `FIGURE_REGISTRY` matches `generate_all_figures` exactly
- Every plotter's signature matches its declared `needs_manuscript` flag
- The pipeline report records `figures_generated >= 24`
- The figure manifest records declared inputs, extracted BibTeX source
  keys, and SHA-256 hashes for generated PNG/SVG siblings
- Prose emphasis uses italics; bold is reserved for the structural
  *At a glance* / *Linked sections* callout labels in the four Part
  overviews (a documented convention, not a test-enforced gate)
- All `[@sec:X]` cross-references resolve to defined anchors
- All `[@key]` citations resolve in `references.bib`
- Current-event rows carry audit dates, source tiers, refresh triggers,
  and scheduled-row handling so volatile claims are visibly maintained

Passing tests means the project is structurally reproducible and
source-linked. It does not mean every historical claim has been
independently reverified; high-risk and current-status claims still need
the [claim-ledger and source-refresh workflow](docs/claim_ledger.md)
before publication. That ledger also records the reserve-source audit:
future uncited BibTeX entries should be cited, explicitly reserved in
`manuscript/config.yaml`, or removed.

For source-tier definitions, sensitive-material boundaries, environment
reproduction, release versioning, audit limits, accessibility checks, and
data-QA scope, use the expanded documentation set under `docs/`.

## Testing

```bash
PYTHONPATH=. uv run pytest projects/crescent_city/tests/ -v
```

All tests are offline; no mocks. The test suite uses real prose,
real BibTeX files, real `tmp_path` directories, real subprocess
invocation of the orchestrator scripts, and real figure generation
into temporary directories.

## See Also

* [`AGENTS.md`](AGENTS.md) — agent-oriented walkthrough
* [`docs/README.md`](docs/README.md) — project documentation map
* [`docs/data_dictionary.md`](docs/data_dictionary.md) — data files, schemas, provenance fields, and update risk
* [`docs/sources_provenance_ethics.md`](docs/sources_provenance_ethics.md) — source tiers, provenance, reuse, and sensitive-material boundaries
* [`docs/data_validation_qa.md`](docs/data_validation_qa.md) — executable data checks and QA boundaries
* [`docs/figure_maintenance.md`](docs/figure_maintenance.md) — figure registry and caption maintenance
* [`docs/manuscript_authoring.md`](docs/manuscript_authoring.md) — manuscript editing workflow and evidence language
* [`docs/testing_and_quality.md`](docs/testing_and_quality.md) — test matrix and green-build semantics
* [`docs/environment_reproducibility.md`](docs/environment_reproducibility.md) — toolchain, reproduction commands, and determinism boundary
* [`docs/claim_ledger.md`](docs/claim_ledger.md) — high-risk claim refresh calendar and reserve-source audit
* [`docs/audit_trail_limitations.md`](docs/audit_trail_limitations.md) — audit map, build limits, and revision templates
* [`docs/accessibility_reader_experience.md`](docs/accessibility_reader_experience.md) — reader-facing format and figure accessibility checks
* [`docs/release_archival_versioning.md`](docs/release_archival_versioning.md) — release artifacts, versioning, DOI flow, and corrections
* [`CHANGELOG.md`](CHANGELOG.md) — editorial revision history
* [`manuscript/SYNTAX.md`](manuscript/SYNTAX.md) — Pandoc citation conventions
* [`manuscript/A1_figure_catalogue.md`](manuscript/A1_figure_catalogue.md) — per-figure catalog
* [`manuscript/A2_glossary.md`](manuscript/A2_glossary.md) — technical-term glossary
* [`docs/architecture.md`](docs/architecture.md) — module dependency graph
* [`infrastructure/prose/SKILL.md`](../../infrastructure/prose/SKILL.md) — prose-analysis API
* [`infrastructure/reference/SKILL.md`](../../infrastructure/reference/SKILL.md) — bibliography validation API
* [`infrastructure/rendering/SKILL.md`](../../infrastructure/rendering/SKILL.md) — PDF rendering API

## License

Manuscript text and rendered scholarly artifacts: CC BY 4.0. Source code: Apache License 2.0 (`LICENSE`). Data files sourced
from federal and California state agencies (U.S. Census Bureau,
USGS, NOAA, NPS, CDFW, OPC, Caltrans, CDCR): public domain or
released under open-data licenses.

## Acknowledgments

The manuscript draws on the institutional memory of the **Del Norte
County Historical Society**, the **Tolowa Dee-ni' Nation**, the
**Redwood Coast Tsunami Work Group at Cal Poly Humboldt**, the
**Save the Redwoods League**, **Jefferson Public Radio**, and the
generations of researchers, ethnographers, geologists, fishers,
mill workers, and community members whose written and oral records
make a synthesis of this depth possible.
