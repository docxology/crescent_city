# Appendix A — Figure Catalog and Reproducibility {#sec:figure_catalogue}

This appendix is the source-of-truth catalog for every figure in the
manuscript. Each entry names the Python function that generates the
figure, lists its data sources, and gives the command needed to
reproduce it independently of the full pipeline. The purpose is practical:
a reader who wants to check, rebuild, or extend one figure can do so
without re-running the whole build.

The suite treats figures as evidence, not decoration. Its design rules
borrow from Tufte's data-ink discipline, Wong's color-blind-safe palette,
and Matplotlib's reproducible vector-output model. The working standard
is straightforward: show the quantity, identify the source, make labels
legible at manuscript scale, and keep every encoding simple enough to
audit in code [@tufte2001visual_display; @wong2011colorblind;
@hunter2007matplotlib]. That is why this catalog documents function
names and data files beside captions. The image and its provenance are a
single scholarly claim [@sandve2013reproducible].

## How the Suite Is Organized

The figure suite lives in the [`src._figures`](../src/_figures/)
subpackage, organized by topic:

```
src/
|-- figures.py                  # Public API — apply this module's
|                               #   FIGURE_REGISTRY for batched generation
`-- _figures/                   # Internal implementation modules
    |-- _style.py               # Wong (2011) palette + shared rcParams
    |-- _io.py                  # save_figure() — writes PNG + SVG
    |-- manuscript_metrics.py   # Section word count, readability, citation density
    |-- demographics.py         # Population trend, economic sectors
    |-- tsunami.py              # Tsunami timeline, disaster impact, inundation diagram
    |-- history.py              # Two-century event timeline
    |-- cartography.py          # Regional map, Tolowa relationship schematic
    |-- conservation.py         # Old-growth coast-redwood decline
    |-- geophysics.py           # Cascadia paleoseismology
    |-- political_geography.py  # State of Jefferson map
    |-- climate.py              # Climate normals and sea-level scenarios
    |-- ecology.py              # Smith River protection designations
    |-- community_systems.py    # Housing, transport, archaeology, health access
    |-- harbor_history.py       # Harbor engineering chronology
    `-- currents.py             # 2024–2026 current-events timeline
```

Adding a new figure requires a small, auditable chain of changes:

1. Add a plotting function named `plot_<name>()` in the appropriate
   `src/_figures/<topic>.py` module — or create a new topic module.
2. Re-export the function from [`src/figures.py`](../src/figures.py).
3. Add a `FigureSpec` entry to the `FIGURE_REGISTRY` tuple in
   `src/figures.py`. The registry order drives the
   `generate_all_figures()` iteration and the catalog order below.
4. If the figure encodes factual series, add a source-keyed data file
   under `data/` and list it in `FigureSpec.data_inputs`.
5. Embed the figure with an auto-formatted `[@fig:...]` reference and
   update the tests and documentation that name the figure contract.

The contract every plotter must honor:

* Output: write a `<name>.png` and `<name>.svg` pair to the output
  directory via `src._figures._io.save_figure()`.
* Determinism: identical inputs must produce byte-identical SVGs
  (no time-stamps, hostnames, or random initializations). PNGs are
  generated from the same code path for PDF embedding, but SVG remains
  the canonical byte-for-byte reproducibility target.
* Style: inherit the shared palette and rcParams by importing from
  `src._figures._style`; do not call `plt.rcParams.update()` inside a
  plotter.
* Accessibility: labels, legends, and annotations must remain readable
  in the rendered PDF at the figure widths used in the manuscript; the
  current shared defaults use 15 pt base text, 20 pt titles, and
  Wong-style blue/orange/green/red/purple/cyan encodings rather than
  red-green contrasts [@wong2011colorblind]. SVG export preserves text
  as text nodes where Matplotlib permits, so vector outputs remain
  searchable and usable in downstream accessibility review.
* Self-contained captions: every figure's caption in the manuscript
  is a four-to-six-sentence description containing the data source, the
  encoding (markers/colors/axes), the evidence class (measured,
  modeled, inferred, schematic, estimate, or provisional status), and
  the interpretive claim — captions are written so that the figure
  remains intelligible if reproduced outside the manuscript.

## Reproducing the Whole Suite

```bash
# From the repository root
uv sync
PYTHONPATH=. python projects/crescent_city/scripts/y_generate_history_figures.py
```

`y_generate_history_figures.py` is a thin orchestrator (<= 40 lines) that
calls `src.figures.generate_all_figures()`. The script prints the path
of every generated PNG to stdout, which the rendering pipeline collects
into the build manifest.

## Reproducing One Figure

Every plotter is a standalone callable. For example, to regenerate
*only* the tsunami inundation diagram:

```python
from pathlib import Path
from src.figures import plot_tsunami_inundation_diagram

png = plot_tsunami_inundation_diagram(
    output_dir=Path("projects/crescent_city/output/figures")
)
print(png)
```

## Catalog of Generated Figures

Each entry follows this template:

> Figure entry — *file basename* (`plot_<name>`)
>
> *Module*: where the function lives.
> *Data source*: input data file(s).
> *Evidence class*: how the figure should be read as evidence.
> *Encoding*: what the markers, axes, and colors mean.
> *Interpretive claim*: the single statement the figure is meant to support.

### Section-metric figures (manuscript_metrics)

Data limitations: these figures measure the manuscript as a built text.
They do not validate the truth of historical claims; they show word
allocation, readability formulas, and citation density so that editorial
balance and evidence coverage can be audited. They are editorial
diagnostics generated after the manuscript is assembled, not independent
historical evidence.

> Figure entry — `section_word_counts.png`
>
> *Function*: `plot_section_word_counts()`.
> *Module*: `manuscript_metrics.py`.
> *Data source*: every manuscript narrative `.md` file except renderer-
> support files, syntax notes, references, and folder-level documentation
> (`README.md`, `AGENTS.md`, `SYNTAX.md`, `preamble.md`, and
> `99_references.md`).
> *Evidence class*: automated editorial-load metric.
> *Source freshness*: periodic; regenerate after manuscript section
> changes. *Reader risk*: low.
> *Long description*: Horizontal bars compare analyzed manuscript word
> counts by section and part with a mean reference line and part
> grouping so reviewers can see where prose weight concentrates.
> *Encoding*: horizontal bar length = word count; bars above the section
> mean are recolored green; a dashed line marks the mean; part-grouped
> panels reduce label crowding while keeping every section visible; the
> wrapped footer states the excluded support files below the plot.
> *Interpretive claim*: the manuscript is center-heavy on the 1964
> tsunami, Indigenous history, lumber industry, and modern-Crescent-City
> sections, with shorter scaffolding sections holding the timeline,
> methodology, and reproducibility frame.

> Figure entry — `readability_metrics.png`
>
> *Function*: `plot_readability_metrics()`.
> *Module*: `manuscript_metrics.py`.
> *Data source*: same manuscript-source set as the word-count figure.
> *Evidence class*: automated prose-surface measurement.
> *Source freshness*: periodic; regenerate after manuscript section
> changes. *Reader risk*: low.
> *Long description*: Two coordinated panels compare Flesch Reading
> Ease and Flesch-Kincaid grade level by manuscript part so reviewers
> can assess prose register without treating readability as truth
> validation.
> *Encoding*: the upper panel uses cyan bars for Flesch Reading Ease;
> the lower panel uses an orange line for Flesch-Kincaid Grade Level;
> part shading keeps section sequence legible without implying causal
> divisions.
> *Interpretive claim*: prose register sits in the 13–18 FKGL band
> (post-secondary, consistent with `config.yaml` targets), with
> deliberate exceptions for methodology and reproducibility.

> Figure entry — `citation_density.png`
>
> *Function*: `plot_citation_density()`.
> *Module*: `manuscript_metrics.py`.
> *Data source*: same manuscript-source set as the word-count figure.
> *Evidence class*: automated citation-coverage metric.
> *Source freshness*: periodic; regenerate after manuscript or citation
> changes. *Reader risk*: medium.
> *Long description*: Horizontal bars compare citation tokens per
> thousand words by section against the configured floor so reviewers
> can identify evidence-coverage gaps before claim-fit review.
> *Encoding*: horizontal bars show citations per 1,000 words by source
> section; color marks sections above or below the configured floor of 3;
> part-grouped panels reduce visual overload and the wrapped footer states
> the counting limitation.
> *Interpretive claim*: every narrative section exceeds the floor; the
> Indigenous-history and tsunami sections cluster near the upper bound.

### Conceptual architecture (systems)

Data limitations: this is an interpretive systems diagram, not an
empirical network model. Its source is the manuscript architecture and
the cited systems literature, so its value is explanatory coherence
rather than measurement.

> Figure entry — `nested_systems_map.png` (`plot_nested_systems_map`)
>
> *Module*: `src/_figures/systems.py`.
> *Data source*: pure-code conceptual synthesis from the manuscript's
> section architecture and the systems literature cited in the
> introduction.
> *Evidence class*: conceptual synthesis.
> *Source freshness*: static; revise only when the manuscript frame
> changes. *Reader risk*: low.
> *Long description*: Four columns organize Space and Time and People
> and Ideas into nested scale levels with converging arrows that show
> the manuscript argument as a systems frame.
> *Encoding*: four vertical columns = Space, Time, People, and Ideas;
> descending boxes = nested scale levels within each lens; converging
> arrows = the emergence of Crescent City as the object of study; the
> bottom double arrow = feedback among hazard, rebuilding, governance,
> memory, and adaptation.
> *Interpretive claim*: the manuscript is not only chronological; it is
> organized around interactions among spatial scale, historical sequence,
> social institutions, and interpretive traditions.

### Population and economy (demographics)

Data limitations: the population series combines decennial counts, ACS
estimates, and California Department of Finance estimates; the economic
series combines employment data with project-level GDP estimates. Both
figures preserve source distinctions in their captions and should not be
read as single-instrument time series.

> Figure entry — `population_trend.png` (`plot_population_trend`)
>
> *Module*: `src/_figures/demographics.py`.
> *Data source*: `data/population_data.csv` (decennial-census + CA
> Department of Finance estimates, with a recent ACS estimate point).
> *Evidence class*: mixed-instrument population enumeration.
> *Source freshness*: periodic; refresh when Census, ACS, or Department
> of Finance estimates change. *Reader risk*: medium.
> *Long description*: A line chart traces official and estimate
> population points over time while annotations distinguish city counts
> from broader demographic interpretation and group-quarters effects.
> *Encoding*: line of official city population vs. census / estimate
> year with peak annotation; the shaded band is visual emphasis, not a
> confidence interval.
> *Interpretive claim*: the official city series peaks in 2010 because
> it includes Pelican Bay group quarters; the separate mid-century
> lumber-economy peak belongs to the broader county-seat trading-area
> series, not to this official city-count plot. The 2026 Department of
> Finance point is included to show the continuing split between
> household residents and group-quarters population.

> Figure entry — `economic_sectors.png` (`plot_economic_sectors`)
>
> *Module*: `src/_figures/demographics.py`.
> *Data source*: `data/economic_sectors.csv` (CA EDD LMI / BLS QCEW
> plus project-level 2020 sector-GDP estimates).
> *Evidence class*: mixed-instrument economic reconstruction.
> *Source freshness*: periodic; refresh if source definitions or sector
> estimates change. *Reader risk*: medium.
> *Long description*: Grouped bars compare employment sectors across
> decades and overlay 2020 sector scale markers so readers can see the
> shift from extraction toward public and visitor economies.
> *Encoding*: grouped bars per sector across four decades (1990–2020);
> dark diamond markers = estimated 2020 sector GDP on the secondary
> axis, included for relative sector scale rather than as official
> municipal GDP accounts.
> *Interpretive claim*: the structural transition from a resource-
> extraction economy to a public-sector- and tourism-anchored economy.

### Tsunami and disaster (tsunami)

Data limitations: post-1946 tsunami heights and damage figures draw on
instrumental records and engineering reconstructions; older entries draw
on deposits, historical reports, and oral-history correlations. The
timeline therefore compares evidence classes as well as events.

> Figure entry — `tsunami_timeline.png` (`plot_tsunami_timeline`)
>
> *Module*: `src/_figures/tsunami.py`.
> *Data source*: `data/tsunami_events.csv`.
> *Evidence class*: mixed tsunami chronology.
> *Source freshness*: low_change; refresh if NOAA, USGS, or literature
> records revise event details. *Reader risk*: medium.
> *Long description*: A dated event timeline separates disaster records
> and geological proxies and historical reports so tsunami events are
> visible without making all evidence classes equivalent.
> *Encoding*: red downward triangles for disasters; orange/blue circles
> for geological proxies and exploration records; annotations use
> deterministic label lanes and the legend/source note sit outside the
> data area.
> *Interpretive claim*: the 1964 event remains the largest measured
> Crescent City run-up; the 2011 event is lower in height but
> operationally important because harbor currents damaged the working
> waterfront.

> Figure entry — `disaster_impact.png` (`plot_disaster_impact`)
>
> *Module*: `src/_figures/tsunami.py`.
> *Data source*: `data/tsunami_events.csv` — 1964 and 1946 from the
> `deaths` column, the 2011 Klamath-mouth death from the `2011_Tohoku`
> `notes` field (guarded in code against drift).
> *Evidence class*: scope-explicit fatality comparison.
> *Source freshness*: low_change; refresh if historical fatality records
> are corrected. *Reader risk*: medium.
> *Long description*: Three scope-labeled horizontal bars — 1964 Alaska
> (11, Crescent City), 2011 Tōhoku (1, Klamath River mouth; 0 in
> Crescent City), and 1946 Aleutian (0 on the contiguous-US west coast;
> its 159 deaths fell in Hilo, Hawaii) — with a footer that keeps the
> Crescent City toll of eleven distinct from the 1964 event's wider
> contiguous-US west-coast total of sixteen.
> *Encoding*: three horizontal bars of documented deaths, each labeled
> with its geographic scope.
> *Interpretive claim*: the 1964 Alaska tsunami is the only event to
> cause multiple Crescent City deaths and the deadliest single-place
> tsunami toll on the contiguous-United-States Pacific coast.

> Figure entry — `tsunami_inundation_diagram.png` (`plot_tsunami_inundation_diagram`)
>
> *Module*: `src/_figures/tsunami.py`.
> *Data source*: `data/tsunami_1964_wave_sequence.csv` for the four
> wave timings, amplitudes, labels, and source keys; the harbor cross-
> section remains schematic geometry in code.
> *Evidence class*: reconstructed engineering chronology.
> *Source freshness*: low_change; refresh if 1964 wave-sequence records
> are corrected. *Reader risk*: medium.
> *Long description*: A schematic water-level sequence shows the four
> 1964 waves and a harbor cross-section to explain why the fourth wave
> carried the destructive force.
> *Encoding*: water-elevation vs. local-time cross-section showing the
> four-wave sequence; harbor bathymetry and Front Street commercial
> district drawn as schematic right-hand inset.
> *Interpretive claim*: the destructive force was Wave 4 (the "killer
> wave"), 6.4 m above MLLW, arriving after the drawdown that exposed
> the seafloor.

### Two-century chronology (history)

Data limitations: the chronology mixes exact statutory or civic dates
with approximate archaeological, cultural, and current-event anchor
dates. The plotted clusters identify narrative density, not event
frequency in a statistical sample.

> Figure entry — `historical_timeline.png` (`plot_historical_timeline`)
>
> *Module*: `src/_figures/history.py`.
> *Data source*: `data/historical_events.json` (more than 80 dated
> events, each carrying source keys, evidence type, date precision, and
> audit status).
> *Evidence class*: curated chronology.
> *Source freshness*: volatile; recent rows require current-event
> refresh. *Reader risk*: high.
> *Long description*: A multi-category event scatter places long
> historical events and recent audited public-status rows on one
> chronology while marker styles distinguish source and disaster
> classes.
> *Encoding*: Gantt-style scatter by category × year; red `X` markers
> for disasters, oversized markers for tsunami/earthquake events, and
> light vertical bands for the three densest interpretive windows.
> *Interpretive claim*: three principal inflection points — the 1850s,
> the 1964–1978 disaster/conservation decade, and the 2020s climate-
> adaptation period — structure the modern history of the community.

### Cartographic figures (cartography)

Data limitations: these are schematic reference maps. They locate
relationships among places used in the manuscript, but they are not
survey-grade GIS products and should not be used for navigation,
jurisdictional boundary work, or site protection.

> Figure entry — `regional_map.png` (`plot_regional_map`)
>
> *Module*: `src/_figures/cartography.py`. Pure-code stylized map.
> *Data source*: public geographic coordinates and local GIS context
> encoded in the function; intended as a spatial-relations reference, not
> a navigational chart.
> *Evidence class*: schematic regional geography.
> *Source freshness*: low_change; refresh if source geography or labels
> change. *Reader risk*: medium.
> *Long description*: A stylized regional map locates Crescent City and
> highways and rivers and parks so place names in the manuscript have a
> shared spatial reference.
> *Encoding*: red star = county seat; green dots = state/national parks;
> red X = Last Chance Grade; red = Hwy 101; orange = Hwy 199; blue =
> Smith / Klamath rivers; orange shading = generalized Tolowa traditional
> territory; green shading = forested uplands.
> *Interpretive claim*: a single reference image binding every place
> name used throughout the manuscript to its spatial location.

> Figure entry — `tolowa_villages_map.png` (`plot_tolowa_villages_map`)
>
> *Module*: `src/_figures/cartography.py`. Pure-code non-coordinate
> relationship schematic.
> *Data source*: public place names and relationship zones from Bommelyn
> (1997), public tribal-history framing, and the Tolowa Dee-ni' Nation's
> contemporary writing system.
> *Evidence class*: generalized ethnographic orientation.
> *Source freshness*: static; revise only with public and appropriate
> source changes. *Reader risk*: high.
> *Long description*: A location-generalized schematic shows public
> Tolowa Dee-ni place relationships and neighboring linguistic context
> without exposing protected places or identifiers.
> *Encoding*: grouped white cards = public relationship zones; blue =
> river and lagoon context; orange shading = generalized cultural-
> geography frame; arrows = conceptual relationships, not routes.
> *Interpretive claim*: the pre-contact Tolowa Dee-ni' settlement
> footprint was dense, clustered around the Smith River estuary, and
> linguistically distinct from neighboring Yurok and Karuk territories.

### Conservation history (conservation)

Data limitations: the redwood acreage curve is a synthesized historical
estimate. Early-acreage baselines and remaining-old-growth totals are
rounded conservation estimates, while park-establishment dates are exact
statutory or administrative dates.

> Figure entry — `redwood_decline_chart.png` (`plot_redwood_decline_chart`)
>
> *Module*: `src/_figures/conservation.py`.
> *Data source*: `data/redwood_old_growth_acreage.csv` and
> `data/redwood_conservation_milestones.csv`, synthesized from Save the
> Redwoods League, NPS RNSP history, Vaden (2015), and statutory/park
> chronology sources.
> *Evidence class*: synthesized conservation history.
> *Source freshness*: periodic; refresh if conservation estimates
> change. *Reader risk*: medium.
> *Long description*: A filled historical curve and milestone labels
> show old-growth coast-redwood decline and conservation interventions
> as rounded synthesis estimates rather than exact annual inventory.
> *Encoding*: brown filled curve of acreage vs. year; staggered
> annotations use explicit data-file label positions for the seven
> conservation-history milestones; the source note sits below the axes
> rather than inside the data field.
> *Interpretive claim*: approximately 95 % of original old-growth
> coast redwood has been logged; the remaining 5 % is now concentrated
> in the Redwood National and State Parks system.

### Geophysics (geophysics)

Data limitations: the Cascadia plot encodes a paleoseismic
interpretation of turbidite correlations. Recurrence intervals and
probabilities are model outputs; they should be read with the
uncertainty discussed in [@sec:cascadia].

> Figure entry — `cascadia_paleoseismology.png` (`plot_cascadia_paleoseismology`)
>
> *Module*: `src/_figures/geophysics.py`.
> *Data source*: `data/cascadia_paleoseismic_events.csv` and
> `data/cascadia_summary_stats.csv`, derived from Goldfinger et al.
> (2012) USGS Professional Paper 1661-F and the orphan-tsunami record.
> *Evidence class*: stratigraphic and probabilistic hazard synthesis.
> *Source freshness*: periodic; refresh if paleoseismic interpretations
> or probability products change. *Reader risk*: high.
> *Long description*: Vertical event sticks summarize Cascadia
> paleoseismic recurrence interpretation and probability annotations
> while separating full-margin and southern-segment evidence for
> reviewer caution.
> *Encoding*: vertical event sticks by years before present; color
> distinguishes full-margin and southern-segment ruptures; inset text
> reports recurrence and fifty-year probability summaries.
> *Interpretive claim*: the southern Cascadia segment has ruptured more
> frequently than the full margin, making Crescent City's hazard profile
> different from the northern and central Pacific Northwest.

### Political geography (political_geography)

Data limitations: the county shapes are deliberately simplified to show
political alignment and regional adjacency. The figure is an explanatory
map of a movement, not a legal reconstruction of the proposed state.

> Figure entry — `jefferson_map.png` (`plot_jefferson_map`)
>
> *Module*: `src/_figures/political_geography.py`.
> *Data source*: stylized county polygons and participation metadata
> encoded in the plotter from the State of Jefferson historical record.
> *Evidence class*: political-geographic schematic.
> *Source freshness*: static; revise only if the political-geography
> framing changes. *Reader risk*: medium.
> *Long description*: A simplified county map shows the proposed State
> of Jefferson geography and reference towns as political orientation
> rather than legal boundary reconstruction.
> *Encoding*: counties are filled by participation status; Crescent City,
> Yreka, Port Orford, and Redding are labeled as political reference
> points; the bottom note states that the county rectangles are
> schematic rather than survey-grade boundaries.
> *Interpretive claim*: the Jefferson movement is best understood as a
> regional political geography rather than a single-town episode.

### Climate (climate)

Data limitations: the climograph uses 1991–2020 NOAA station normals
for Crescent City McNamara Airport. It represents station climate, not
microclimates in redwood groves, Smith River canyons, or harbor-edge
fog corridors.

> Figure entry — `climograph.png` (`plot_climograph`)
>
> *Module*: `src/_figures/climate.py`.
> *Data source*: `data/climate_normals_1991_2020.csv`, derived from
> NOAA NCEI `normals-monthly-1991-2020` for Crescent City McNamara
> Airport (USW00024286).
> *Evidence class*: NOAA station-normal climatology.
> *Source freshness*: low_change; refresh when NOAA normals periods or
> station products change. *Reader risk*: low.
> *Long description*: Monthly temperature and precipitation and wet-day
> normals from the Crescent City airport station show the maritime
> climate regime and its seasonal wet-dry pattern.
> *Encoding*: monthly mean temperature line, precipitation bars, and
> wet-day frequency line (`MLY-PRCP-AVGNDS-GE001HI`) on a shared month
> axis.
> *Interpretive claim*: Crescent City's cool, wet, maritime regime
> explains both its redwood ecology and its unusually narrow annual
> temperature range, while the dry-season precipitation minimum makes
> summer fog ecologically consequential even though fog is not itself
> plotted in this station-normal figure.

### Expanded section-support figures (climate, ecology, community systems)

Data limitations: these six figures are curated interpretive aids,
not live dashboards. Each one reads a small source-keyed CSV under
`data/`; rows distinguish measured observations, agency projections,
modeled or scenario risks, legal-designation records, official project
status, and schematic service pathways. Values should be refreshed only
after the cited source records change, and archaeology rows deliberately
generalize public evidence classes rather than exposing protected site
locations or coordinates.

> Figure entry — `sea_level_scenarios.png` (`plot_sea_level_scenarios`)
>
> *Module*: `src/_figures/climate.py`.
> *Data source*: `data/sea_level_scenarios.csv`, keyed to NOAA tide-gauge
> data, the 2022 NOAA sea-level technical report, and the 2024 California
> OPC sea-level-rise guidance.
> *Evidence class*: mixed measured, projected, scenario, and modeled
> planning evidence.
> *Source freshness*: periodic; refresh when NOAA, OPC, or hazard
> guidance changes. *Reader risk*: high.
> *Long description*: Observed trends and projection bands and a
> separate Cascadia subsidence marker share one vertical scale while
> preserving measured, projected, and modeled evidence classes.
> *Encoding*: observed tide-gauge trend, planning-scenario bands, and a
> separate coseismic-subsidence risk marker share a common vertical scale
> while preserving the evidence class for each row.
> *Interpretive claim*: Crescent City's planning problem combines slow,
> measured relative sea-level change, statewide projection ranges, and a
> low-frequency Cascadia subsidence hazard that cannot be read from the
> tide gauge alone.

> Figure entry — `smith_river_protection.png` (`plot_smith_river_protection`)
>
> *Module*: `src/_figures/ecology.py`.
> *Data source*: `data/smith_river_protection.csv`, keyed to Rivers.gov
> and U.S. Forest Service Smith River National Recreation Area records.
> *Evidence class*: legal-geographic designation scale.
> *Source freshness*: low_change; refresh if designation or agency
> records change. *Reader risk*: medium.
> *Long description*: Stacked designation miles and watershed context
> show the Smith River as nested legal geography rather than only a
> channel-length statistic.
> *Encoding*: stacked designated miles by federal Wild, Scenic, and
> Recreational class, with brief callouts for ecological and management
> context.
> *Interpretive claim*: the Smith River is protected through a nested
> legal geography; the river's ecological importance depends on both
> channel miles and the public-land watershed context around them.

> Figure entry — `housing_pipeline.png` (`plot_housing_pipeline`)
>
> *Module*: `src/_figures/community_systems.py`.
> *Data source*: `data/housing_pipeline_projects.csv`, keyed to city,
> housing-provider, and local-government reporting on the 2024--2026
> affordable-housing pipeline.
> *Evidence class*: official project-status pipeline.
> *Source freshness*: volatile; refresh before any public release.
> *Reader risk*: high.
> *Long description*: Project bars distinguish planned units and
> committed vouchers and funding awards so the housing pipeline is not
> mistaken for delivered affordable inventory.
> *Encoding*: horizontal project bars scaled by reported quantity; color
> distinguishes planned units, committed vouchers, and funding in
> millions of dollars, while text labels preserve project status and
> phasing constraints.
> *Interpretive claim*: the active housing pipeline is not one project;
> it is a staged institutional system that combines city housing-element
> compliance, nonprofit development capacity, tribal and county programs,
> and construction-phase funding.

> Figure entry — `last_chance_grade_profile.png` (`plot_last_chance_grade_profile`)
>
> *Module*: `src/_figures/community_systems.py`.
> *Data source*: `data/last_chance_grade_metrics.csv`, keyed to Caltrans
> Last Chance Grade selection and tunnel-update materials.
> *Evidence class*: agency infrastructure planning metric.
> *Source freshness*: volatile; refresh when Caltrans updates project
> estimates. *Reader risk*: high.
> *Long description*: A compact dashboard compares Last Chance Grade
> risk and selected tunnel-alternative metrics while preserving cost and
> schedule as planning-stage estimates.
> *Encoding*: a compact dashboard of chronic-risk, selected-alternative,
> approximate tunnel-length, schedule, and cost metrics; text labels carry
> the units because the metrics are heterogeneous.
> *Interpretive claim*: Last Chance Grade is best understood as a compound
> infrastructure risk rather than a single road repair: chronic slide
> maintenance, a selected tunnel alternative, large capital cost, and a
> multiyear delivery sequence all govern the county's effective access.

> Figure entry — `archaeology_evidence_ladder.png` (`plot_archaeology_evidence_ladder`)
>
> *Module*: `src/_figures/community_systems.py`.
> *Data source*: `data/archaeology_evidence_layers.csv`, keyed to public
> archaeological, ethnographic, NAGPRA, and California consultation
> sources.
> *Evidence class*: public evidence-class ladder.
> *Source freshness*: static; revise only when public or authorized
> source categories change. *Reader risk*: high.
> *Long description*: A generalized evidence ladder orders public
> archaeological and ethnographic and legal evidence classes while
> withholding site-specific cultural-resource details.
> *Encoding*: a timeline-style evidence ladder ordered by approximate
> year, with bar colors identifying public evidence class, a horizontal
> 1775 contact-era boundary marker, a compact in-plot legend, and labels
> intentionally generalized.
> *Interpretive claim*: the archaeology chapter rests on converging
> public evidence types — material culture, ethnography, legal protection,
> and tribal consultation — while respecting the confidentiality of
> sensitive cultural locations.

> Figure entry — `rural_health_access_network.png` (`plot_rural_health_access_network`)
>
> *Module*: `src/_figures/community_systems.py`.
> *Data source*: `data/healthcare_access_nodes.csv` and
> `data/healthcare_access_edges.csv`, keyed to HCAI, Sutter Coast,
> Open Door, UIHS/IHS, Tolowa Dee-ni' program pages, Del Norte
> public-health records, Rural Human Services, United Way 2-1-1, and
> local food-system coordination records.
> *Evidence class*: qualitative service-pathway mapping.
> *Source freshness*: periodic; refresh when public provider, county, or
> service-directory records change. *Reader risk*: high.
> *Long description*: A schematic service network links hospital and
> clinics and tribal services and county programs and transport pathways
> to show access relationships rather than measured patient flows.
> *Encoding*: node color shows service role; directed links show common
> referral, transport, coordination, and out-of-county specialty-care
> pathways. Node placement is schematic and constrained to safe margins;
> selected edge labels name representative pathways while the complete
> edge set remains auditable in the CSV.
> *Interpretive claim*: health access in Crescent City is a networked
> rural system, with local primary care and hospital capacity connected
> to tribal services, county social services, emergency transport, and
> specialty care beyond the county.

### Harbor history (harbor_history)

Data limitations: this is an event chronology, not a full engineering
inventory. It marks major design and disaster moments while leaving
routine maintenance, permitting, and minor repairs to the cited harbor
history sections.

> Figure entry — `harbor_timeline.png` (`plot_harbor_timeline`)
>
> *Module*: `src/_figures/harbor_history.py`.
> *Data source*: `data/harbor_timeline_events.csv`, a source-keyed
> event table synthesized from harbor-history, tsunami, lighthouse,
> port-infrastructure, and Klamath-restoration sources cited in the
> harbor engineering chapter.
> *Evidence class*: curated infrastructure chronology.
> *Source freshness*: periodic; refresh if harbor public records change.
> *Reader risk*: medium.
> *Long description*: Event markers and era bands summarize major
> Crescent City harbor engineering and disaster milestones while
> omitting routine maintenance and minor repairs.
> *Encoding*: event markers by year and category with era bands for the
> pre-modern wharf, Harbor District, post-1964 reconstruction, and
> tsunami-resistant harbor periods.
> *Interpretive claim*: Crescent City's waterfront infrastructure has
> been rebuilt cyclically after disaster, with each rebuild embedding
> higher design expectations.

### Recent history (currents)

Data limitations: the current-events figure is provisional by design.
It records verified public events checked on 19 May 2026 and
should be refreshed whenever city, harbor, Caltrans, tribal, or agency
records update the status of 2024–2026 claims.

> Figure entry — `currents_timeline.png` (`plot_currents_timeline`)
>
> *Module*: `src/_figures/currents.py`.
> *Data source*: `data/historical_events.json`, filtered to the
> 2024--2026 window, plus `data/currents_categories.yaml` for lane
> definitions.
> *Evidence class*: current-status chronology.
> *Source freshness*: volatile; requires current-event refresh before
> release. *Reader risk*: high.
> *Long description*: Domain lanes plot 2024 to 2026 public events with
> source-tier marker styles so unsettled journalism-backed and scheduled
> records do not look as settled as official records.
> *Encoding*: domain-stratified scatter — seven horizontal lanes
> colored by category (Environment / Conservation / Infrastructure /
> Governance / Culture / Geological / Conflict). Each marker is a
> verified, dated event with a short label rendered in a
> matching-colored box; exact and month-level dates are plotted as
> fractional years, and same-day clusters receive small deterministic
> offsets to prevent overlap. Marker fill and outline encode source
> tier: filled markers indicate official primary records, heavier
> outlines indicate official records plus context sources, hollow
> markers indicate journalism-backed public status, and red outlines
> indicate events pending later official-record review.
> *Interpretive claim*: the 2024--2026 period is unusually
> concentrated for inflection points relative to comparable rolling
> windows — Last Chance Grade tunnel selection, Klamath dam-removal
> completion, early Klamath post-removal monitoring signals, partial
> ocean-salmon reopening after closure years, the
> *Del Norte Triplicate* closure-sale-relaunch transition, multiple
> housing-finance and water-rate-protest milestones, an offshore
> earthquake, and a national tourism-press finalist recognition all fall
> inside a compact two-year band without making all source types look
> equally settled.

## Style Reference for Figure Maintenance

All twenty-four figures share the Wong (2011) colorblind-safe palette
defined in `src/_figures/_style.py`. The palette is exposed publicly
via `src.figures.PALETTE`; any new figure should reference colors by
their palette key rather than by hex code, so palette updates remain a
single-file change.

Shared `rcParams` (font family, sizes, grid alpha, etc.) live in the
same module and are applied as an import-time side effect of any
plotter. Per-figure overrides are applied through the `plt.subplots`
`figsize` argument and explicit `ax.set_*` calls — not by mutating
the shared `rcParams`.

## Testing Contract for Figure Reproducibility

The figure suite is validated by
[`tests/test_figures.py`](../tests/test_figures.py). Tests enforce:

* the registry contains the expected twenty-four figures and has no
  duplicates;
* every plotter's signature matches the declared
  `needs_manuscript` flag;
* `generate_all_figures()` produces exactly twenty-four PNGs, each
  above 5 KB and each accompanied by a matching SVG;
* every `FigureSpec.data_inputs` file exists under `data/`;
* manuscript-metric figures exclude folder-level documentation files;
* selected SVG outputs preserve searchable text nodes for accessibility;
* crowded figures render at expected dimensions with safe outer margins;
* the pipeline JSON report records `figures_generated >= 24`.

Adding a new figure therefore requires updating the test's `EXPECTED`
list, `FIGURE_REGISTRY`, and this appendix.
