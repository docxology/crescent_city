# Current-Events Refresh Protocol

This protocol is the publication gate for Crescent City claims dated
2024-2026. It turns the row-level `checked_as_of`, `source_tier`, and
`refresh_trigger` fields in `data/historical_events.json` into a concrete
review workflow.

Current baseline: the active current-event rows are audited as of
2026-05-19 in `data/historical_events.json`. This document was added on
2026-05-18 after an external source-risk check. Do not change the row
date unless the source itself has been rechecked.

## Refresh Sequence

1. Start with the row in `data/historical_events.json`.
2. Recheck the highest-authority source available: official adopted
   record, agency project page, agenda packet, minutes, court record,
   election page, tribal public statement, or official program record.
3. Update the data row before prose: `source_keys`, `source_tier`,
   `checked_as_of`, `date_iso`, `date_precision`, and `refresh_trigger`.
4. Update any affected prose in `35_currents.md`, `71_timeline.md`, the
   relevant topical chapter, figure captions, and `references.bib`.
5. Regenerate figures when a plotted date, status, label, source tier, or
   category changes.
6. Run the verification command listed below.

## Refresh Matrix

| Trigger | Source to recheck first | Expected edit path | Minimum verification |
|---|---|---|---|
| Caltrans updates Last Chance Grade alternative, cost, or schedule | Caltrans Last Chance Grade project page, District 1 materials, environmental documents | `data/historical_events.json`, `data/last_chance_grade_metrics.csv`, `11_transportation.md`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_figures.py -q` |
| KRRC, NOAA, tribal, or state agencies update Klamath dam-removal milestones | KRRC completion records, NOAA restoration updates, tribal/state public pages | `data/historical_events.json`, `63_klamath_dam_removal.md`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| CDFW, PFMC, or federal managers change ocean-salmon seasons | CDFW regulations pages, PFMC decisions, federal fishery notices | `data/historical_events.json`, `27_fishing.md`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py -q` |
| Triplicate ownership or publication status changes | Owner publication pages first, local journalism second | `data/historical_events.json`, `35_currents.md`, `65_modern.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Pelican Bay homicide investigation changes | CDCR, district attorney, or court records | `data/historical_events.json`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py -q` |
| Battery Point financing, construction, or unit status changes | City, developer, HCD, HOME award, housing-authority, or funder records | `data/historical_events.json`, `data/housing_pipeline_projects.csv`, `10_housing.md`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_figures.py tests/test_manuscript.py -q` |
| Water/sewer Prop 218 hearing occurs or is delayed | City Council agenda packets, minutes, ordinances, protest-count record, rate schedule | `data/historical_events.json`, `35_currents.md`, `61_zoning.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Maiden Lane case receives official legal update | Sheriff, district attorney, or court records | `data/historical_events.json`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py -q` |
| Parade/Steller finalist status changes | Parade or Steller contest page | `data/historical_events.json`, `68_tourism.md`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Tolowa elk restoration funding, acreage, or scope changes | Tolowa Dee-ni' Nation public pages first, then USFWS/CDFW/grant records | `data/historical_events.json`, `35_currents.md`, `41_indigenous.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py -q` |
| USGS revises the offshore earthquake event | USGS event page and NOAA/NWS tsunami statements if applicable | `data/historical_events.json`, `35_currents.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Fire-chief recruitment deadline passes or appointment is made | Crescent City Fire & Rescue, city records, recruitment notice | `data/historical_events.json`, `35_currents.md`, `45_governance.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| 2 June 2026 primary election results or certification post | Del Norte County elections office, California Secretary of State, official result/certification pages | `data/historical_events.json`, `35_currents.md`, `45_governance.md`, `71_timeline.md` | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py tests/test_manuscript.py -q` |

## Wording Rules

- Use "scheduled" until an official record shows the event occurred and
  identifies the result.
- Use "planned," "funded," "approved," "under construction," or
  "completed" only when the source supports that exact status.
- Use "reported" or "local-journalism-backed" for rows still awaiting a
  court, sheriff, district-attorney, agency, or formal public record.
- Do not convert a grant award into delivered infrastructure or housing.
- Do not convert a recruitment notice into an appointment.
- Do not convert a proposed rate into an adopted rate.

## Release Gate

Before public sharing, run:

```bash
PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py tests/test_manuscript.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict
```

From the template repository root, then run:

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```
