# Data Directory

Curated source data for the Crescent City history pipeline lives here.
The files are small, checked in, and intended to be auditable by readers
without rerunning any external collection step.

## Files

| File | Role |
|---|---|
| `historical_events.json` | Canonical chronology for the timeline and current-events figures; sensitive Indigenous and archaeology-adjacent rows keep `lat`/`lon` blank |
| `currents_categories.yaml` | Lane definitions for the 2024-2026 current-events figure |
| `population_data.csv` | City population counts and estimates used by the demographics figure |
| `economic_history.csv` | Long-run local economic context used by prose and metrics |
| `economic_sectors.csv` | Sector employment and estimated 2020 GDP context |
| `tsunami_events.csv` | Tsunami event data used by disaster figures |
| `tsunami_1964_wave_sequence.csv` | Source-keyed four-wave sequence used by the 1964 schematic |
| `climate_normals_1991_2020.csv` | NOAA climate normals used by the climograph |
| `redwood_old_growth_acreage.csv` | Rounded old-growth coast-redwood acreage synthesis used by the conservation figure |
| `redwood_conservation_milestones.csv` | Source-keyed conservation milestones and label positions for the redwood figure |
| `cascadia_paleoseismic_events.csv` | Goldfinger/USGS paleoseismic event ages and rupture-segment classes |
| `cascadia_summary_stats.csv` | Source-keyed Cascadia recurrence and probability summary values |
| `harbor_timeline_events.csv` | Source-keyed Crescent City harbor engineering and disaster event anchors |
| `sea_level_scenarios.csv` | Measured, projected, and modeled water-level scenario values for the sea-level figure |
| `smith_river_protection.csv` | Wild / Scenic / Recreational river-mile designations and watershed context |
| `housing_pipeline_projects.csv` | Source-keyed 2024-2026 affordable-housing pipeline quantities and status notes |
| `last_chance_grade_metrics.csv` | Caltrans Last Chance Grade repair, tunnel, schedule, and cost metrics |
| `archaeology_evidence_layers.csv` | Public evidence classes for archaeology without protected site coordinates |
| `healthcare_access_nodes.csv` | Rural health access nodes for the healthcare network figure |
| `healthcare_access_edges.csv` | Rural health access pathways for the healthcare network figure |
| `figure_provenance.csv` | Source freshness, source type, reader risk, and long descriptions for all registered figures |

For schema details, update risk, and provenance-field guidance, see
[`../docs/data_dictionary.md`](../docs/data_dictionary.md). For
source-tier meanings, sensitive-material limits, and reuse rules, see
[`../docs/sources_provenance_ethics.md`](../docs/sources_provenance_ethics.md).

## Update Rules

- Keep source keys aligned with `manuscript/references.bib`.
- Use only the current-event `source_tier` values documented in
  `../docs/sources_provenance_ethics.md` and enforced by
  `../tests/test_data.py`.
- For figure CSVs, treat `source_keys`, `evidence_class`, and `notes`
  as provenance fields, not optional decoration. They explain whether a
  plotted value is measured, projected, modeled, inferred, schematic, or
  a checked public status.
- Keep `figure_provenance.csv` synchronized with `src/figures.py` and
  `manuscript/A1_figure_catalogue.md`; tests expect one row per
  registered figure in registry order.
- Keep `event_id`, `point_id`, and `stat_id` values stable unless the
  underlying historical claim changes; tests treat them as audit anchors.
- Preserve existing column names and JSON fields unless tests and figure
  code are updated in the same change.
- Keep `lat` and `lon` paired: both numeric for publishable public-event
  locations, or both blank for sensitive Indigenous, archaeology-adjacent,
  massacre, cultural-landscape, or protected-resource rows.
- Mark current-event rows with date precision, evidence type, and audit
  status so they can be refreshed without rewriting prose first.
- For 2024-2026 current-event rows, keep `checked_as_of`, `source_tier`,
  and `refresh_trigger` current. Use exact or month-level `date_iso`
  values whenever possible; only future public-status rows may be dated
  after the audit date, and those rows must use `date_precision:
  scheduled`.
- Keep archaeology and tribal-cultural rows generalized. Do not add
  coordinates, parcel-level locations, or protected site identifiers.
- Keep schematic geometry in plotting code, but store factual dates,
  values, event labels, and summary statistics in data files with
  `source_keys` whenever a figure makes a historical or scientific claim.
- Do not store generated figures, reports, or rendered manuscript files here.

## Verification

```bash
PYTHONPATH=. uv run pytest tests/test_data.py tests/test_figures.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

For the broader data-QA map, see
[`../docs/data_validation_qa.md`](../docs/data_validation_qa.md).
