# Changelog — crescent_city

All notable revisions to the Crescent City manuscript and its
supporting figure pipeline. The manuscript is a living scholarly
document; this changelog records the editorial milestones.

The format follows [Keep a Changelog](https://keepachangelog.com/);
the manuscript itself is versioned by the `paper.version` field in
`manuscript/config.yaml`.

## [1.0] — 2026-05-10

### Initial canonical release

**Manuscript scope** — 49 narrative chapters framed by eight Part
openers, plus the Figure Catalog and Glossary appendices, totaling
approximately 115 typeset pages.

#### Added — Manuscript

- Cascadia — locked margin, 1700 orphan tsunami, Goldfinger
  turbidite paleoseismology, ETS, M9 scenario, ShakeAlert,
  Indigenous earthquake oral history
- Jefferson — 1941 Yreka proclamation, Crescent City's
  three-day governor (Judge John L. Childs), 1853–2014 modern
  revival, *Citizens for Fair Representation* lawsuit, the
  Double-Cross flag
- Klamath Knot — Yontocket as cosmological center, 1958/1967
  Bigfoot lineage, Mount Shasta esoterica, UFO and exopolitical
  reports, the Lost Coast / Emerald Triangle, the redwood
  numinous tradition, Wallace's synthesis
- Locked Margin, Living Town — closing synthesis pulling the
  five reinforcing threads of the manuscript together
- Figure Catalog appendix (per-figure module, data source,
  encoding, interpretive claim)
- Glossary appendix (Indigenous, geological, regulatory,
  engineering, cultural terms)

#### Added — Figures (17 total)

- `cascadia_paleoseismology` — 10,000-yr Cascadia turbidite chronology
- `jefferson_map` — State of Jefferson participating counties
- `climograph` — Crescent City monthly temperature, precipitation, fog
- `harbor_timeline` — Harbor engineering and disaster events 1856–2024
- `regional_map`, `tolowa_villages_map` — Custom stylized maps
- `tsunami_inundation_diagram` — Schematic four-wave sequence of 1964 event
- `redwood_decline_chart` — Old-growth acreage 1850–2025

#### Added — Bibliography

- 306 BibTeX entries spanning peer-reviewed primary literature
  (BSSA, JGR, Nature, Science, Earthquake Spectra), federal-agency
  reports (USGS PP 1661-F, USGS PP 1707, NOAA Technical Memoranda),
  university-press monographs (Atwater, Madley, Speece, Wallace,
  Anderson, Pritzker, Cook), court cases (*Ashker v. Brown*,
  *Tillie Hardwick v. United States*, *Citizens for Fair
  Representation v. Padilla*), statutes (PL 90-545, PL 95-250,
  PL 100-580, PL 101-601 NAGPRA, PL 101-612, PL 93-638), and
  tribal primary documents (BIA OFA Petition #85, Yurok-Tolowa IMSA
  Treaty, California AB-1284, AB-2356)

#### Changed — Editorial

- Every section H1 received a Pandoc `{#sec:shortname}` anchor for
  auto-resolved cross-referencing via pandoc-crossref
- All hard-coded `(Section N)` references replaced with `[@sec:X]`
  auto-references
- All `**bold**` markers removed from prose (italics for emphasis only)
- Every section title rewritten in vivid "show-not-tell" form
  (e.g., "The 1964 Tsunami" → "Eleven Drownings: The Killer Wave
  of Good Friday 1964")
- Substantive expansion of 22 previously thin sections
  (housing, healthcare, transportation, governance, etc.)
- 14 inline figure cross-references woven throughout prose

#### Changed — Code

- Refactored monolithic `src/figures.py` into a `src/_figures/`
  subpackage with 11 topic-organized modules
- Introduced `FIGURE_REGISTRY` as the single source of truth for
  figure generation; `generate_all_figures()` now iterates the
  registry instead of hard-coding plotter calls
- Added `FigureSpec` dataclass-like record (name, plotter,
  needs_manuscript flag, description)
- Centralized Wong 2011 colorblind-safe palette in
  `src/_figures/_style.py`; centralized PNG+SVG persistence in
  `src/_figures/_io.py`
- All hyperlinks render in red (`linkred = RGB(180,0,30)`) via
  customized `hypersetup` in `manuscript/preamble.md`
- Margins tightened from 1.0in to 0.85in; added `fancyhdr`
  page-header / page-number infrastructure
- Cover page and Table of Contents auto-generated from
  `manuscript/config.yaml` metadata

#### Fixed

- Pandoc + `biblatex` mismatch that produced `[?]` for every
  citation — switched preamble to `natbib`
- 91 inline `## Subsection` headings missing the required preceding
  blank line — all preserved as proper subsections in the rendered
  PDF
- Duplicate file-numbering collision resolved to preserve canonical
  filename ordering
- Multiple numerical-consistency errors identified by research
  agents and corrected (1853 Yontocket Massacre dating, Smith
  River Wild & Scenic statute PL 101-612, Rowdy Creek Hatchery
  1968 founding date, OPA-90 attribution of double-hull
  requirements, *Tillie Hardwick* 1983 restoration date)

### Test suite

- 80 automated tests covering pipeline integration, figure
  generation, registry contract, citation resolution, section
  anchors, and orchestrator-script invocation
- No mocks; all tests use real prose, real BibTeX, real
  `tmp_path`, real subprocess execution

## [0.1] — 2026-05-09

### Pre-canonical scaffold

- Initial manuscript draft and figure-generation scaffold
- Initial bibliography seed
- Project scaffolding aligned with `template_prose_project`
