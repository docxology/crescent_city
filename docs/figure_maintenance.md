# Figure Maintenance

The Crescent City manuscript has 24 registered figures. Each figure should
be reproducible from checked-in manuscript text, checked-in data, or
explicit schematic geometry.

The operational source of truth is `../src/figures.py`. The manuscript
catalog is `../manuscript/A1_figure_catalogue.md`.

Each generation pass also writes
`../output/figures/figure_manifest.json`. That manifest is deterministic:
it records each figure's registry name, primary section, evidence classes,
declared data inputs, extracted BibTeX source keys from those inputs,
provenance fields from `../data/figure_provenance.csv`, long
descriptions, and SHA-256 hashes for the PNG/SVG siblings without adding
timestamps.

## Registry Contract

Every figure is a `FigureSpec` with:

| Field | Meaning |
|---|---|
| `name` | Stable basename for PNG and SVG outputs |
| `plotter` | Function that produces the figure |
| `needs_manuscript` | True for manuscript-metric figures that read Markdown files |
| `description` | One-line operational summary |
| `data_inputs` | Data filenames passed into the plotter when `data_dir` is supplied |
| `primary_section` | Section anchor where the figure is primarily used |
| `evidence_classes` | Evidence types encoded by the figure |
| `source_freshness` | Refresh cadence from `figure_provenance.csv` |
| `source_type` | Dominant source class from `figure_provenance.csv` |
| `last_checked` | ISO source-review date |
| `visual_evidence_mode` | Chart, map, timeline, network, or related visual mode |
| `reader_risk` | Low/medium/high overreading risk |
| `long_description` | Accessibility-oriented description mirrored in the catalog |

Do not change a figure name casually. The name is used by output files,
tests, documentation, and manuscript image references.

## Figure Inventory

| Figure | Plotter | Primary source basis |
|---|---|---|
| `section_word_counts` | `plot_section_word_counts` | Manuscript Markdown |
| `readability_metrics` | `plot_readability_metrics` | Manuscript Markdown |
| `citation_density` | `plot_citation_density` | Manuscript Markdown and citation tokens |
| `nested_systems_map` | `plot_nested_systems_map` | Conceptual synthesis |
| `population_trend` | `plot_population_trend` | `population_data.csv` |
| `economic_sectors` | `plot_economic_sectors` | `economic_sectors.csv` |
| `tsunami_timeline` | `plot_tsunami_timeline` | `tsunami_events.csv` |
| `disaster_impact` | `plot_disaster_impact` | `tsunami_events.csv` |
| `tsunami_inundation_diagram` | `plot_tsunami_inundation_diagram` | `tsunami_1964_wave_sequence.csv` plus schematic geometry |
| `historical_timeline` | `plot_historical_timeline` | `historical_events.json` |
| `regional_map` | `plot_regional_map` | Schematic cartography |
| `tolowa_villages_map` | `plot_tolowa_villages_map` | Non-coordinate schematic and public ethnographic record |
| `redwood_decline_chart` | `plot_redwood_decline_chart` | Redwood acreage and milestone CSVs |
| `cascadia_paleoseismology` | `plot_cascadia_paleoseismology` | Paleoseismic event and summary CSVs |
| `jefferson_map` | `plot_jefferson_map` | Schematic political geography |
| `climograph` | `plot_climograph` | NOAA normals CSV |
| `harbor_timeline` | `plot_harbor_timeline` | `harbor_timeline_events.csv` |
| `currents_timeline` | `plot_currents_timeline` | `historical_events.json` and `currents_categories.yaml` |
| `sea_level_scenarios` | `plot_sea_level_scenarios` | `sea_level_scenarios.csv` |
| `smith_river_protection` | `plot_smith_river_protection` | `smith_river_protection.csv` |
| `housing_pipeline` | `plot_housing_pipeline` | `housing_pipeline_projects.csv` |
| `last_chance_grade_profile` | `plot_last_chance_grade_profile` | `last_chance_grade_metrics.csv` |
| `archaeology_evidence_ladder` | `plot_archaeology_evidence_ladder` | `archaeology_evidence_layers.csv` |
| `rural_health_access_network` | `plot_rural_health_access_network` | Healthcare nodes and edges CSVs |

## Add Or Change A Figure

1. Decide whether the figure is data-backed, manuscript-metric, or
   schematic.
2. Put factual values, labels, dates, and source keys in `../data/`
   whenever the figure makes a historical, scientific, civic, or economic
   claim.
3. Implement or update the plotter in `../src/_figures/`.
4. Save through `_io.save_figure()` so PNG and SVG siblings are written
   together.
5. Register the figure in `../src/figures.py`.
6. Confirm the generated `figure_manifest.json` records the expected
   data inputs, source keys, evidence classes, provenance fields, long
   description, and output hashes.
7. Add or update the manuscript image block and caption.
8. Run the caption audit in `../tests/test_figures.py` so every embedded
   figure names source basis, evidence class, limitation, and interpretive
   claim.
9. Update `../data/figure_provenance.csv` and
   `../manuscript/A1_figure_catalogue.md`.
10. Update docs if the figure count, source basis, or maintenance contract
   changed.

## Caption Standard

A good caption names:

- What the visual mark encodes.
- Source basis and evidence class.
- Important limitations.
- The interpretive claim the figure supports.

Every figure also needs a concise long description in
`../manuscript/A1_figure_catalogue.md`, mirrored in
`../data/figure_provenance.csv`, so the accessibility description and the
generated manifest remain synchronized.

`tests/test_figures.py::TestFigures::test_manuscript_figure_captions_state_audit_contract`
guards this standard for all embedded manuscript figures.

Do not let a caption imply that a schematic is a measured map, that a
scenario is a forecast, or that a current project status is a completed
outcome.

## Visual Quality Rules

- Use the shared palette and rcParams in `../src/_figures/_style.py`.
- Keep labels readable in the combined PDF, not only in standalone PNGs.
- Prefer checked-in data over constants in plotting code.
- Keep label-layout mechanics in code; keep factual values in data files.
- Preserve ethical boundaries for archaeology and tribal-cultural maps.

## Verification

Run from `projects/crescent_city/`:

```bash
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only
PYTHONPATH=. uv run pytest tests/test_figures.py tests/test_manuscript.py -q
```

Before public release, run the strict pipeline and renderer from the
repository root:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```
