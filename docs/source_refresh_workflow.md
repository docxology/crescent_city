# Source Refresh Workflow

Use this runbook when a current-event row, high-risk number, modeled
hazard, Indigenous-history boundary, or journalism-backed civic detail
needs to be refreshed before the next render.

## When To Use This

Use this workflow when:

- A row in `data/historical_events.json` is from 2024 onward.
- A future scheduled event has occurred or has been delayed.
- An agency page, court record, election page, grant page, or technical
  report changes.
- A figure caption or manuscript paragraph depends on a current project
  status.
- A source tier needs to be upgraded from local reporting to an official
  record.

For ordinary typo or wording fixes that do not change facts, use the
targeted manuscript and citation tests instead.

Related guides:

- `data_dictionary.md` for file roles and provenance fields.
- `sources_provenance_ethics.md` for exact source-tier labels, reuse, and
  sensitive-material boundaries.
- `current_events_refresh.md` for the 2024-2026 trigger matrix and
  expected edit paths.
- `manuscript_authoring.md` for evidence-language rules.
- `testing_and_quality.md` for test selection.

## Refresh Sequence

1. Identify the claim and its current source keys.
2. Recheck the highest-authority source available.
3. Update or add `manuscript/references.bib` entries before changing prose.
4. Update source data in `data/` when the claim drives a figure or
   timeline.
5. Update manuscript prose, captions, and `manuscript/71_timeline.md`
   if the timeline language changes.
6. Update `docs/claim_ledger.md` when the claim remains volatile or needs
   a new refresh trigger.
7. Regenerate figures when any plotted value, date, label, or category
   changes.
8. Run the targeted checks.

## Current-Event Row Fields

Rows from 2024 onward in `data/historical_events.json` should carry:

| Field | Meaning |
|---|---|
| `checked_current_source` | Boolean marker that the source was checked for the current-status claim |
| `checked_as_of` | ISO date of the latest source review |
| `source_tier` | Evidence tier from `claim_ledger.md` |
| `refresh_trigger` | Concrete event that requires a future re-audit |
| `date_iso` | Exact or month-level date when available |
| `date_precision` | Precision label; future scheduled rows should use `scheduled` |

Future-dated rows are allowed only for scheduled public events. They must
stay worded as scheduled status until official records show the event has
occurred and what changed.

## Source-Tier Upgrade Rules

| Current tier | Upgrade when | Required edits |
|---|---|---|
| `local_journalism_current_status` | Official minutes, agency pages, public-body records, or primary statements become available | Add the official BibTeX key, update `source_keys`, revise prose attribution, update `source_tier` |
| `local_journalism_pending_official_record` | Court, sheriff, district-attorney, or agency records become available | Add the official BibTeX key, update `source_keys`, revise legal/public-safety wording, update `source_tier` |
| `commercial_publication` | A public agency or local institution publishes a direct record | Keep the commercial source only if it supports a cultural-status claim |
| `official_plus_local_journalism` | Local reporting is no longer needed for the factual claim | Keep local reporting only for context or remove the key |
| `official_plus_reference` | A more direct official record supersedes the reference page | Keep the reference only if it still supplies durable background context |
| `tribal_press_release_republished` | The original tribal publication is available | Cite the original tribal source and preserve public/authorized boundaries |

## Verification

Run from the project directory for project-local tests:

```bash
PYTHONPATH=. uv run pytest tests/test_data.py tests/test_citations.py tests/test_manuscript.py -q
```

Run from the template repository root for the strict project pipeline:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
```

If the refresh changes figures, also run:

```bash
PYTHONPATH=. uv run pytest tests/test_figures.py -q
PYTHONPATH=. uv run python scripts/run_history_pipeline.py --figures-only
```

The second command above is project-local; run it from
`projects/crescent_city/`. From the repository root, use:

```bash
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --figures-only
```

## Render After Refresh

After source refresh and tests pass, render and validate from the
repository root:

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

For a release handoff, run:

```bash
PYTHONPATH=. uv run python scripts/05_copy_outputs.py --project crescent_city
```

## Review Checklist

Before calling a source refresh complete, confirm:

- The highest-authority source available is cited.
- `checked_as_of` uses the actual review date.
- `refresh_trigger` names a concrete future event or source change.
- Scheduled events are not written as completed events.
- Local journalism is not carrying a technical, legal, or scientific fact
  when an official source exists.
- Figures, captions, timeline entries, and prose all agree.
- The claim ledger still names any remaining volatile status.
