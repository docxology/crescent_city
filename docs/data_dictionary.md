# Data Dictionary

This dictionary explains the checked-in data files that support the
Crescent City manuscript and figures. The goal is not to duplicate every
row; it is to name each file's role, schema, provenance fields, and update
risk so future edits do not turn source data into untracked narrative.

Source data lives in `../data/`. Generated figures and reports live in
`../output/` and should not be edited as source.

## Shared Conventions

| Convention | Meaning |
|---|---|
| `source_keys` | Semicolon- or list-style BibTeX key references into `../manuscript/references.bib` |
| `evidence_class` / `evidence_type` | What kind of evidence the row encodes: measured, modeled, projected, schematic, public status, estimate, or chronology |
| `notes` | Short row-level caveat or provenance note |
| Stable IDs | Fields such as `event_id`, `point_id`, `stat_id`, `metric_id`, and `node_id` are audit anchors; change them only when the underlying claim changes |
| Current-status metadata | Recent rows use `checked_as_of`, `source_tier`, and `refresh_trigger` so stale public-status claims can be found and refreshed |
| Figure provenance metadata | `figure_provenance.csv` records source freshness, source type, last checked date, visual evidence mode, reader risk, and long description for every registered figure |

For exact current-event source-tier labels and ethical boundaries, see
[`sources_provenance_ethics.md`](sources_provenance_ethics.md).

## File Inventory

| File | Primary use | Key fields | Update risk |
|---|---|---|---|
| `historical_events.json` | Main chronology, historical timeline, current-events timeline | `id`, `year`, `date_iso`, `date_precision`, `category`, `event`, `lat`, `lon`, `source_keys`, `evidence_type`, `checked_as_of`, `source_tier`, `refresh_trigger` | High for 2024 onward rows and sensitive-location rows |
| `currents_categories.yaml` | Visual lanes for the current-events figure | `key`, `palette_key`, `marker`, `y_lane`, `label` | Medium when new event categories are added |
| `population_data.csv` | Population trend figure | `decade`, `population_estimate`, `growth_rate_pct`, `economic_driver`, `key_events`, `source` | Low unless Census, ACS, or DOF estimates are updated |
| `economic_history.csv` | Long-run economy context | `year`, sector estimates, `estimate_type`, `source_keys`, `notes` | Medium because estimates combine instruments |
| `economic_sectors.csv` | Employment sector figure | Sector employment by decade, `sector_gdp_2020_millions` | Medium when source instruments or definitions change |
| `tsunami_events.csv` | Tsunami timeline and disaster comparison | `tsunami`, `date`, `source_event`, `category`, `wave_height_ft`, `damage_2024usd`, `deaths` | Medium because historical records mix observed, reported, and reconstructed values |
| `tsunami_1964_wave_sequence.csv` | 1964 four-wave schematic | `event_id`, `time_position`, `amplitude_m`, `color_key`, `source_keys` | Medium because the figure is schematic, not a gauge reconstruction |
| `climate_normals_1991_2020.csv` | Climograph | `month`, `tavg_f`, `prcp_in`, `wet_days_ge_0_01_in`, `station`, `source` | Low until NOAA normals period changes |
| `redwood_old_growth_acreage.csv` | Redwood decline figure | `point_id`, `year`, `acres`, `evidence_type`, `source_keys` | Medium because values are rounded synthesis estimates |
| `redwood_conservation_milestones.csv` | Redwood decline annotations | `event_id`, `year`, `label`, `label_x`, `label_y`, `source_keys` | Low unless conservation chronology changes |
| `cascadia_paleoseismic_events.csv` | Cascadia paleoseismic figure | `event_id`, `label`, `age_yr_bp`, `segment`, `source_keys` | Medium because paleoseismic interpretation can be revised |
| `cascadia_summary_stats.csv` | Cascadia recurrence/probability annotations | `stat_id`, `sort_order`, `label`, `value`, `source_keys` | High for probability language and model summaries |
| `harbor_timeline_events.csv` | Harbor engineering and disaster timeline | `event_id`, `year`, `label`, `category`, `color_key`, `source_keys` | Medium for recent infrastructure statuses |
| `sea_level_scenarios.csv` | Sea-level scenario figure | `scenario_id`, `year`, `value_min_ft`, `value_mid_ft`, `value_max_ft`, `evidence_class` | High because measured, projected, and modeled values must not be merged |
| `smith_river_protection.csv` | Smith River protection figure | `feature_id`, `label`, `value`, `unit`, `category`, `evidence_class` | Low to medium when designations or watershed figures change |
| `housing_pipeline_projects.csv` | Housing pipeline figure | `project_id`, `quantity`, `quantity_type`, `status`, `funding_millions`, `evidence_class` | High because project status and funding can change |
| `last_chance_grade_metrics.csv` | Last Chance Grade profile | `metric_id`, `label`, `value`, `unit`, `display_value`, `evidence_class` | High because planning estimates and schedules can change |
| `archaeology_evidence_layers.csv` | Public archaeology evidence ladder | `layer_id`, `year_start`, `year_end`, `evidence_class`, `public_detail_level`, `source_keys` | High for ethical boundaries, low for row mechanics |
| `healthcare_access_nodes.csv` | Rural health network nodes | `node_id`, `label`, `node_type`, `x`, `y`, `capacity_label`, `evidence_class`, `source_keys` | Medium because capacity and service availability differ |
| `healthcare_access_edges.csv` | Rural health network pathways | `edge_id`, `source`, `target`, `label`, `evidence_class`, `source_keys` | Medium when referral, transfer, or service pathways change |
| `figure_provenance.csv` | Figure manifest and accessibility metadata | `figure_name`, `source_freshness`, `source_type`, `last_checked`, `visual_evidence_mode`, `reader_risk`, `long_description` | Medium because it must stay synchronized with `src/figures.py` and `manuscript/A1_figure_catalogue.md` |

## Current-Event Records

`historical_events.json` is the most volatile data file. Location fields
are publishability controls, not a promise of complete geocoding: `lat`
and `lon` must either both contain a public, non-sensitive coordinate or
both be blank for Indigenous, archaeology-adjacent, massacre,
cultural-landscape, or protected-resource rows. Rows from 2024 onward
should include:

| Field | Rule |
|---|---|
| `checked_current_source` | True when the source was checked for the current-status claim |
| `checked_as_of` | ISO date of the review |
| `source_tier` | One of the exact tiers defined in `sources_provenance_ethics.md` and enforced by `tests/test_data.py` |
| `refresh_trigger` | Concrete event that requires future re-audit |
| `date_precision` | Use `scheduled` for future public events |

Future-dated rows must be public scheduled events and must not be written
as completed history.

## Data Edit Checklist

1. Update the data row before updating a figure or manuscript paragraph.
2. Keep `source_keys` aligned with `../manuscript/references.bib`.
3. Preserve stable IDs unless the historical claim itself changes.
4. For recent rows, update `checked_as_of`, `source_tier`, and
   `refresh_trigger`; use only the source tiers documented in
   `sources_provenance_ethics.md`.
5. Regenerate figures when plotted values, labels, categories, or dates
   change.
6. Run data and figure tests.

## Verification

Run from `projects/crescent_city/`:

```bash
PYTHONPATH=. uv run pytest tests/test_data.py tests/test_figures.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

Run from the template repository root when preparing render outputs:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```
