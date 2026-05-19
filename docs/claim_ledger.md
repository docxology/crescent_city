# Claim Ledger

This ledger records the evidence classes, refresh triggers, and audit
controls for claims that need more care than ordinary citation checking.
It complements the bibliography and pipeline reports; it does not replace
claim-by-claim source review.

Use [source_to_claim_audit.md](source_to_claim_audit.md) for the
section-wide claim-fit matrix and
[current_events_refresh.md](current_events_refresh.md) for the
2024-2026 trigger-by-trigger refresh protocol.

## Evidence Classes

| Claim type | Preferred source | Editorial rule |
|---|---|---|
| Measured records | NOAA, USGS, Census, HCAI, NPS, CDFW, state data portals | Name the instrument, office, or date range when the value matters. |
| Modeled hazards | Peer-reviewed studies, government technical reports, official hazard maps | Use words such as "modeled," "scenario," "planning estimate," or "projection." |
| Current events | City, county, tribal, state, federal, school, harbor, or court records | Date the status claim and avoid implying completion before the record shows it. |
| Local civic detail | Official records first; reputable local journalism when no stable public record exists | Attribute the detail and avoid using journalism for technical, legal, or scientific facts. |
| Indigenous history | Tribal publications, tribally authorized public material, ethnography, law, and archival sources | Do not publish restricted ceremonial knowledge, protected site locations, or point coordinates in source data. |
| Markets and estimates | ACS, DOF, Realtor.com, CAR, NPS VSE, agency cost estimates, or named market instruments | Do not merge instruments into a single unstated number. |

## Source Tiers

Use these exact labels consistently in `data/historical_events.json`.
They are enforced by `tests/test_data.py` and defined in more detail in
`sources_provenance_ethics.md`.

| Tier | Meaning | Use |
|---|---|---|
| `official_primary` | Direct record from the responsible agency, court, tribe, public body, or data portal | Preferred for status, legal, scientific, and technical claims |
| `official_plus_local_journalism` | Official source plus local reporting used for context or narrative detail | Good for civic events with both formal action and local interpretation |
| `official_plus_reference` | Official source plus a stable reference, election, or agency background source | Good for scheduled public rows or official-status rows needing durable context |
| `local_journalism_current_status` | Local reporting where no stable public record is available yet | Accept only as dated status; re-audit when official records appear |
| `local_journalism_pending_official_record` | Local reporting for an event that should later be checked against court, sheriff, district-attorney, or agency records | Treat as provisional and re-audit when official records become available |
| `commercial_publication` | Commercial list, ranking, or non-government publication | Use for cultural or tourism status, not technical facts |
| `tribal_press_release_republished` | Tribal publication or press release republished by another outlet | Preserve tribal framing and check the original tribal source when possible |

## High-Risk Claim Controls

| Area | Control |
|---|---|
| Cascadia probabilities and recurrence | Keep probabilities labeled as model outputs and distinguish measured plate motion from inferred locking and recurrence. |
| Sea-level rise | Preserve the measured tide-gauge versus scenario-projection distinction, name compound-flooding mechanisms carefully, and do not infer structural failure from planning-assessment vulnerability language. |
| Smith River ecology and agriculture | Keep hatchery management, estuary water quality, lily-bulb monitoring, and undammed-river comparison claims source-keyed. |
| Last Chance Grade | Tie the Caltrans 2026-dollar estimate to Alternative F and preserve planning-estimate wording. |
| Harbor engineering and current RFPs | Treat Harbor District RFPs as public-status evidence, not completed construction. |
| Housing | Treat unit counts, vouchers, grants, and completion windows as official pipeline claims, not delivered inventory. |
| Ocean salmon | Recheck CDFW, PFMC, and federal sources before stating openings, closures, returns, or final catch status. |
| Brown Act and Proposition 218 | Keep statutory and LAO support attached to open-meeting and rate-protest mechanics. |
| Healthcare and social services | Preserve licensed-bed language, avoid unsupported hard-radius coverage claims, and do not convert capacity into staffed availability without a staffing source. |
| Indigenous and archaeological material | Use public or authorized material only; avoid restricted ceremonial knowledge, coordinates, parcel-level locations, or protected site identifiers. Sensitive chronology rows keep `lat` and `lon` blank. |

## Current-Event Refresh Policy

Current-event rows are the main place where a reproducible build can still
publish stale facts. For every `data/historical_events.json` row from 2024
onward:

- `checked_as_of` records the latest source-refresh date.
- `source_tier` records the evidence tier.
- `refresh_trigger` states the concrete event that requires re-audit:
  a public hearing, election result, changed project status, revised
  agency page, court update, grant-scope change, or corrected scientific
  record.
- Future-dated rows are allowed only for scheduled public events and must
  stay worded as scheduled status, not completed history.
- Exact or month-level `date_iso` values are preferred. Blank dates for
  recent rows should be treated as a defect unless the row records a
  deliberately undated public status.

## Current-Event Refresh Calendar

Use this checklist before the next public render or after any public-record
change. Update `data/historical_events.json` first, then the relevant
BibTeX entry, manuscript prose, figure output, and pipeline report.

| Trigger date or event | What to re-check | Expected edit path | Verification |
|---|---|---|---|
| 1 June 2026 water/sewer hearing | City Council minutes, protest count, adopted ordinances, effective date, and any revised rate schedule | Update the water/sewer row, `manuscript/35_currents.md`, and `manuscript/71_timeline.md`; keep wording as proposed if the action is delayed | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| 2 June 2026 primary election | County and California Secretary of State results, certification status, and candidate/outcome language | Replace scheduled language only after official results or certification; refresh source keys if county/state pages move | `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict` |
| 5 June 2026 fire-chief application deadline | Recruitment closing status, city/fire-agency update, appointment, or reposting | Keep the row as recruitment status until an appointment or official next step is public | `PYTHONPATH=. uv run pytest tests/test_data.py -q` |
| Court, sheriff, district-attorney, or CDCR update | Maiden Lane and Pelican Bay homicide investigation status, charges, hearings, disposition, or corrected details | Replace local-journalism-only language with official-record language when available | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py -q` |
| CDFW, PFMC, or federal in-season fishery update | Ocean salmon openings, closures, harvest guidelines, and final catch-status language | Update fishery rows and any "return" or "closed" wording in the active-present chapter | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Agency correction or project-status change | Last Chance Grade, Klamath restoration, Battery Point, Tolowa elk restoration, USGS earthquake metadata, or harbor RFP status | Update the row's `checked_as_of`, `refresh_trigger`, source keys, and any caption/prose derived from the row | `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict` |

## Volatile Current Claims

| Area | Current control |
|---|---|
| 2026 water and sewer rates | Re-audit after the 1 June 2026 hearing, protest count, and ordinance decision before treating rates as adopted. |
| 2026 primary election | Keep the 2 June 2026 row as scheduled until county or state election offices publish results. |
| Battery Point Apartments | Treat units, costs, and remobilization as current project status until city, developer, or funder records show construction and lease-up progress. |
| Fire-chief recruitment | Re-audit after the 5 June 2026 application deadline or any appointment announcement. |
| Maiden Lane homicide | Treat the row as local-journalism-backed until sheriff, district attorney, or court records update charges, hearings, or disposition. |
| Tolowa elk restoration grant | Re-audit if Tolowa Dee-ni' Nation, USFWS, CDFW, or grant records update funding, acreage, or project scope. |
| Ocean salmon seasons | Re-audit when CDFW, PFMC, or federal managers issue in-season changes, closures, or final catch-status updates. |
| USGS offshore earthquake | Re-audit if USGS revises the event page, magnitude, location, event ID, or tsunami flag. |

## Claim Edit Workflow

Use this sequence when a claim changes in prose, data, or a figure.

1. Identify the claim type and source tier.
2. Update the source data first when a figure or timeline depends on the
   claim.
3. Update or add the BibTeX key in `manuscript/references.bib`.
4. Update manuscript prose and captions using evidence-class language.
5. Update this ledger if the claim is volatile, modeled, sensitive, or
   reserve-source related.
6. Regenerate figures if any plotted field changed.
7. Run the targeted tests in the verification matrix below.

## Verification Matrix

| Change type | Minimum verification |
|---|---|
| Current-event row | `PYTHONPATH=. uv run pytest tests/test_data.py tests/test_manuscript.py -q` |
| Citation or reserve-key change | `PYTHONPATH=. uv run pytest tests/test_citations.py tests/test_pipeline.py -q` |
| Figure data or plotter change | `PYTHONPATH=. uv run pytest tests/test_figures.py -q` plus `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only` |
| Manuscript prose change | `PYTHONPATH=. uv run pytest tests/test_manuscript.py tests/test_citations.py -q` |
| Public render candidate | `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict`, then render and validate |

## Reserve Sources

The bibliography intentionally preserves a small number of background or
reserve sources when they document local archives, technical context, or
future-update trails. A source should be removed only when it is both
unused and clearly obsolete for this project; otherwise keep it in the
explicit reserve list.

## Reserve Bibliography Audit

Current audit status:

| Category | Count | Keys | Maintenance rule |
|---|---:|---|---|
| Cited entries | 371 | Pipeline-derived | No action unless a citation breaks or the source no longer supports the claim. |
| Reserved entries | 5 | `delaplane1941dispatches`; `kqed_pelican_bay`; `latimes2025lcgtunnel`; `redwoodvoice2026sewerplant`; `spieldenner2007` | Keep only while each key remains useful as background, update trail, or local-context reserve. |
| Unused non-reserve entries | 0 | none | Any future uncited key should either be cited where it supports a claim, moved into `bibliography.reserve_keys` with a reason, or removed. |

Reserve-key reasons:

| Key | Reason to keep |
|---|---|
| `delaplane1941dispatches` | Background trail for State of Jefferson press coverage and possible future archival expansion. |
| `kqed_pelican_bay` | Context reserve for Pelican Bay history and future carceral-institution updates. |
| `latimes2025lcgtunnel` | External press context for Last Chance Grade if the planning narrative needs a journalism comparison. |
| `redwoodvoice2026sewerplant` | Update trail for wastewater-infrastructure coverage adjacent to the 2026 rate process. |
| `spieldenner2007` | Local-history reserve for Crescent City synthesis and future cross-checking. |
