# Data Validation And QA

This guide maps the current executable data checks to the project files
they protect. It also names future QA ideas without presenting them as
implemented behavior.

## Current Executable Checks

| Area | Enforced by | What it checks |
|---|---|---|
| Historical chronology schema | `tests/test_data.py` | Required fields, unique IDs, valid source keys, coordinate bounds, duplicate event prevention. |
| Current-event metadata | `tests/test_data.py` | `checked_as_of`, `source_tier`, `refresh_trigger`, scheduled-row handling, and audit date. |
| CSV shape | `tests/test_data.py` | Ragged rows and source-key presence for CSV files. |
| Figure-method data | `tests/test_data.py` | Stable IDs, source-key fields, date/value ranges, and file-specific required columns. |
| Figure registry and manifest | `tests/test_figures.py` | Registered figures, output shape, SVG siblings, deterministic contracts, extracted source keys, provenance metadata, long descriptions, and generated manifest hashes. |
| Figure provenance | `tests/test_data.py` | `figure_provenance.csv` rows match the registry and use valid source-freshness, source-type, visual-mode, reader-risk, and review-date fields. |
| Manuscript captions | `tests/test_manuscript.py` | Figure caption evidence language, long-description coverage, and appendix catalog structure. |
| Citation linkage | `tests/test_citations.py` | Cited keys, missing keys, reserve-source policy, and unused-source audit. |
| Documentation drift | `tests/test_documentation.py` | Local links, folder docs, figure count, manuscript shape, and guarded documentation facts. |
| Canonical audit docs | `tests/test_documentation.py` | Required audit docs exist and are linked from `docs/README.md` and `docs/index.md`. |
| Source-tier documentation | `tests/test_documentation.py` | Source-tier docs use the exact labels enforced by `tests/test_data.py`. |

The tests use real files and subprocesses. Do not replace data quality
checks with mocks.

## Data Quality Dimensions

| Dimension | Current rule |
|---|---|
| Completeness | Required fields must exist for chronology and figure-method files. |
| Traceability | Source-backed rows and generated figure-manifest source keys must reference BibTeX keys in `../manuscript/references.bib`. |
| Stability | IDs are audit anchors and should not change unless the underlying claim changes. |
| Timeliness | Recent events carry `checked_as_of` and `refresh_trigger`. |
| Authority | Current-event rows use enforced `source_tier` labels. |
| Sensitivity | Archaeology and tribal-cultural rows stay generalized and public. |
| Accessibility | Figure long descriptions are mirrored between `data/figure_provenance.csv`, the registry manifest, and the appendix catalog. |
| Rebuildability | Generated files are rebuilt from checked-in data, code, and manuscript sources. |

## Hard And Soft Failures

| Failure type | Meaning | Response |
|---|---|---|
| Hard failure | A pytest assertion or strict pipeline gate fails. | Fix before release or document why the release is blocked. |
| Soft failure | A reviewer identifies stale, weak, or ethically risky material not yet enforced by tests. | Update source data, prose, claim ledger, or this guide; add a test if the rule should become permanent. |
| Future work | A useful check is described but not implemented. | Keep it in the planned-checks section until code or tests enforce it. |

Do not downgrade a hard failure to a soft failure by editing the docs.
Either fix the source or change the test with an explicit reason.

## Current Source-Tier Check

`tests/test_data.py` currently accepts only these current-event
`source_tier` values:

- `commercial_publication`
- `local_journalism_current_status`
- `local_journalism_pending_official_record`
- `official_plus_local_journalism`
- `official_plus_reference`
- `official_primary`
- `tribal_press_release_republished`

The meanings are defined in
[sources_provenance_ethics.md](sources_provenance_ethics.md) and mirrored
in [claim_ledger.md](claim_ledger.md). If a new tier is needed, update
the test, data, and docs in the same change.

## QA Workflow For Data Changes

1. Edit the source data file first.
2. Confirm source keys exist in `../manuscript/references.bib`.
3. Update affected manuscript prose, captions, and claim-ledger rows.
4. Regenerate figures when any plotted value, label, date, or category
   changed.
5. Run the minimum test command from
   [testing_and_quality.md](testing_and_quality.md).
6. Run the strict project pipeline before a render or release.

## Planned Checks Not Yet Implemented

These are candidates for future code or test work:

| Candidate | Value |
|---|---|
| Data dictionary coverage test | Ensure every checked-in data file appears in `docs/data_dictionary.md`. |
| Rendered-token scan | Check PDF/HTML outputs for unresolved citation or cross-reference tokens. |
| Figure accessibility checks | Sample label sizes, contrast, and caption completeness. |
| Release checksum bundle | Record release artifact hashes after validation and copy-out. |

Until implemented, these items are guidance only. Do not claim them as
release gates.
