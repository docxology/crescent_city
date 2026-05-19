## Run It Yourself: A Reproducibility Framework Following Peng (2011) {#sec:reproducibility}

### Principles for Reproducible Historical Research

Following Peng's principles of reproducible research, this study is
designed so that any researcher with the repository can rebuild the
analytical record [@peng2011reproducible]. The standard is the one
Sandve et al. describe as the need to "connect textual statements to
underlying results" [@sandve2013reproducible]. Every quantitative claim,
figure, data transformation, and generated appendix should be
recoverable from source files rather than from author memory.

The technical rules are simple. Computational analyses are implemented
as pure functions with no external dependencies beyond specified
packages. The analytical pipeline makes no network calls. Random seeds
are fixed where stochastic processes are involved. Dependency versions
are governed by `pyproject.toml` and the lock file, following the
reproducible-research emphasis on preserving computational context as
well as prose and data [@stodden2016enhancing].

The reproducibility framework is structured around three commitments:

1. Determinism — identical inputs produce byte-identical outputs.
2. Self-containment — the pipeline can be executed without
   internet access after the initial `uv sync`.
3. Transparency — every figure, every cited number, and every
   pipeline gate is traceable to its source through the manuscript
   appendix ([@sec:figure_catalogue]).

These commitments are also FAIR commitments in miniature: data
must be findable in `data/`, accessible without proprietary tools,
interoperable as CSV/JSON/Markdown/BibTeX, and reusable under the
licenses stated below [@wilkinson2016fair]. The result is not only
a more auditable PDF; it is a project that can be inspected as a
research object.

### What the Repository Provides

1. Source manuscript: numbered Markdown files for the abstract,
   introduction, four Part openers, forty-six topical chapters,
   timeline, methodology, reproducibility, references, and the Figure
   Catalog and Glossary appendices in `manuscript/`
2. Raw data: CSV and JSON files in `data/`, kept in plain-text
   formats so they can be diffed, archived, and reused under FAIR
   data-management expectations [@wilkinson2016fair]
3. Analysis code: Python package in `src/`, including the public
   figure API (`figures.py`), report and pipeline helpers, variable
   injection, project checks, and the `_figures/` submodules
   (manuscript metrics, demographics, tsunami, history, cartography,
   conservation, geophysics, political geography, climate, ecology,
   harbor history, conceptual systems mapping, community systems, and
   recent events)
4. Pipeline orchestrators: thin scripts in `scripts/` that
   call the public API and do no business logic
5. Configuration: Typed settings in `manuscript/config.yaml`
6. Dependencies: `pyproject.toml` specifies exact package versions
7. Documentation: `README.md`, `AGENTS.md`, and `docs/` describe the
   public quick start, agent-facing contracts, architecture, current
   manuscript organization, and output expectations
8. Figures: All twenty-four figures are generated from data
   or pure code by Matplotlib plotters [@hunter2007matplotlib].
   The shared style follows a color-blind-safe palette and a
   restrained statistical-graphics standard: large text, direct
   source labels where space permits, no decorative chartjunk, and
   captions that state the interpretive claim rather than merely
   naming the image [@tufte2001visual_display; @wong2011colorblind].
   SVG outputs are
   byte-identical across runs (deterministic hash salt pinned in
   `matplotlib.rcParams`); PNG outputs are visually identical but
   may differ in metadata bytes across `matplotlib`/`libpng`
   versions, which is why the test suite hashes SVG rather than PNG.
   The complete catalog with per-figure
   data sources and one-line reproduction commands is in
   [@sec:figure_catalogue].
9. Bibliography: `manuscript/references.bib` is the canonical
   bibliography file. The validation report records the current cited-key
   count and unused-entry count for each build, while the file itself
   preserves peer-reviewed primary literature, federal-agency reports,
   archival material, court cases, and tribal primary documents.

### How to Reproduce the Manuscript and Figures

```bash
# Clone the repository
git clone https://github.com/docxology/crescent_city.git
cd crescent_city

# Create virtual environment and install dependencies
uv sync

# Run the full Crescent City pipeline
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/run_history_pipeline.py

# Or just regenerate figures (does not run prose validation)
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/y_generate_history_figures.py

# Verify outputs
ls projects/crescent_city/output/
ls projects/crescent_city/output/figures/

# Render and validate the combined PDF
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

To verify byte-identical reproduction, run the pipeline twice and
compare outputs:

```bash
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/run_history_pipeline.py
cp -r projects/crescent_city/output output_first
PYTHONPATH=. uv run python \
    projects/crescent_city/scripts/run_history_pipeline.py
diff -ru output_first/manuscript_report.json \
         projects/crescent_city/output/manuscript_report.json
diff -ru output_first/figures projects/crescent_city/output/figures
```

To regenerate a single figure (e.g. the Cascadia paleoseismology
chart) without running the rest of the pipeline:

```python
from pathlib import Path
from src.figures import plot_cascadia_paleoseismology

png = plot_cascadia_paleoseismology(
    output_dir=Path("projects/crescent_city/output/figures")
)
print(png)
```

The same pattern applies to every plotter in the registry; see
[@sec:figure_catalogue] for the complete catalog.

### Updating Current Claims After Source Refresh

Future updates should treat source freshness as part of reproduction.
Before changing a 2024–2026 current-event claim, a population estimate,
a hazard probability, a visitor-spending figure, or an infrastructure
cost, update the underlying `data/` row or BibTeX entry first and then
regenerate the manuscript variables, figures, PDF, and validation
reports. Current-event claims should be checked against official city,
county, tribal, state, or federal records before local journalism is
used. The `historical_events.json` chronology now stores source keys,
date precision, evidence type, verification status, `checked_as_of`,
source tier, and refresh-trigger metadata for each event, so volatile
rows can be audited without re-reading the entire chapter. Future-dated
rows are allowed only when they describe scheduled public events and
retain scheduled-status language until the event has occurred and been
rechecked. If two official instruments disagree — for example Census
QuickFacts, ACS estimates, and California Department of Finance E-5
population estimates — the prose should name the instrument rather than
silently choose a single number.

Future maintainers should also preserve the manuscript's
claim-confidence vocabulary. New or revised numbers should be labeled in
context as measured records, model outputs, post-event reconstructions,
agency planning estimates, commercial listing snapshots, licensed
capacity figures, or checked current-status claims. The label belongs in
the sentence or caption where the claim appears, not only in an
appendix, because that is where readers decide how much weight to place
on the number.

### Testing Contract for Reproducible Claims

The pipeline is validated by the project test suite in `tests/`. The
figure suite is governed by an explicit registry contract:
`tests/test_figures.py::TestFigures` requires
exactly twenty-four PNG–SVG pairs above 5 KB each; the contract
class `TestSupportingModulesUnderCoverage` further validates the
registry signatures, the public-API exports, and the
script-orchestrator contract. The documentation guard in
`tests/test_documentation.py` checks local documentation links and
prevents stale figure counts, manuscript-file ranges, and obsolete Part
descriptions from returning to the public instructions. Adding a new
figure therefore requires updating the test's `EXPECTED` list,
`FIGURE_REGISTRY`, the matching catalog entry in the appendix, and the
public documentation that names the figure suite.

Those tests certify structural reproducibility, source linkage, citation
resolution, data shape, and deterministic figure generation. They do not
prove every historical interpretation or current-status claim true. High-risk
claims therefore need a source-refresh pass through the living claim ledger
in `docs/claim_ledger.md` before publication or after material public-record
changes. The same ledger now records the reserve-source audit: uncited
bibliography entries should either be intentionally reserved in
`manuscript/config.yaml` or cited in the manuscript, so the project does
not accumulate a quiet shadow bibliography.

### Licenses for Text, Code, Data, and Artifacts

All manuscript text and rendered scholarly artifacts are released
under CC BY 4.0. Data files sourced from government agencies (USGS,
NOAA, Census Bureau, NPS, CDFW, OPC) are in the public domain or
released under open-data licenses. Source code is released under the
Apache License 2.0.

No human-subjects research was conducted; no Institutional
Review Board approval was required. All Indigenous cultural
information reported in this manuscript was drawn from public,
published sources and does not include restricted ceremonial
knowledge. The Tolowa Dee-ni' Nation's own publications and
authorized representatives are the canonical reference for
ceremonial detail; readers seeking deeper engagement with the
Nation's culture, language, or fisheries co-management work
should consult the Nation's official website and publications
directly.
