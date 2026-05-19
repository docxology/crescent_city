# Project Documentation

This directory is the project-facing documentation hub for the Crescent
City exemplar. It explains how to run the project, how the source tree is
organized, how claims are refreshed, and how rendered artifacts are checked
before publication.

Use the root `README.md` for the public overview and the root `AGENTS.md`
for repository-wide assistant rules. Use this folder when you need the
working instructions for this specific project.

## Document Map

| File | Use |
|---|---|
| [index.md](index.md) | Task-oriented map for readers, maintainers, and reviewers |
| [quickstart.md](quickstart.md) | Short commands for setup, tests, figures, PDF rendering, and copy-out |
| [architecture.md](architecture.md) | Source boundaries, pipeline flow, data flow, and extension points |
| [project_overview.md](project_overview.md) | Current manuscript shape, data/figure inventory, checks, and artifact map |
| [data_dictionary.md](data_dictionary.md) | Data file roles, schemas, provenance fields, and update risk |
| [sources_provenance_ethics.md](sources_provenance_ethics.md) | Source-tier policy, provenance expectations, reuse rules, and sensitive-material boundaries |
| [data_validation_qa.md](data_validation_qa.md) | Executable data checks, QA dimensions, hard/soft failures, and planned validation work |
| [source_to_claim_audit.md](source_to_claim_audit.md) | Manuscript-wide source-to-claim fit audit and high-risk section controls |
| [current_events_refresh.md](current_events_refresh.md) | 2024–2026 current-event refresh protocol and trigger matrix |
| [figure_maintenance.md](figure_maintenance.md) | Figure registry contract, inventory, caption rules, and verification |
| [manuscript_authoring.md](manuscript_authoring.md) | Manuscript editing workflow, citation rules, evidence language, and variables |
| [testing_and_quality.md](testing_and_quality.md) | Test matrix, green-build semantics, failure triage, and release checks |
| [environment_reproducibility.md](environment_reproducibility.md) | Supported toolchain, reproduction commands, determinism boundary, and troubleshooting |
| [claim_ledger.md](claim_ledger.md) | Evidence classes, volatile claims, reserve bibliography policy, and audit matrix |
| [source_refresh_workflow.md](source_refresh_workflow.md) | Step-by-step runbook for updating current-event and high-risk claims |
| [audit_trail_limitations.md](audit_trail_limitations.md) | Reviewer-facing map of audit records, build limits, known gaps, and revision templates |
| [accessibility_reader_experience.md](accessibility_reader_experience.md) | Reader profiles, format expectations, figure accessibility, and release spot checks |
| [visual_pdf_qa.md](visual_pdf_qa.md) | Rendered-PDF visual QA, automated raster smoke checks, and manual review targets |
| [rendering_and_outputs.md](rendering_and_outputs.md) | Renderer commands, output locations, validation, and troubleshooting |
| [publication_checklist.md](publication_checklist.md) | Final pre-publication sequence for source, tests, render, and deliverables |
| [release_archival_versioning.md](release_archival_versioning.md) | Versioning, release artifacts, DOI/Zenodo flow, checksums, and correction policy |
| [redteam_review_2026-05-15.md](redteam_review_2026-05-15.md) | Current adversarial risk review for the reproducible artifact |
| [AGENTS.md](AGENTS.md) | Local assistant contract for this documentation directory |

## Source Of Truth

| Subject | Authoritative location |
|---|---|
| Public project overview and figure list | `../README.md` |
| Agent edit contract | `../AGENTS.md` |
| Manuscript source | `../manuscript/` |
| Data source tables | `../data/` |
| Figure registry | `../src/figures.py` |
| Project pipeline logic | `../src/pipeline.py` |
| CLI orchestration | `../scripts/` |
| Drift guards | `../tests/test_documentation.py` |
| Source tiers, ethics, and provenance | `sources_provenance_ethics.md` |
| Evidence-class and refresh policy | `claim_ledger.md` |
| Manuscript-wide claim-fit audit | `source_to_claim_audit.md` |
| Current-event refresh trigger matrix | `current_events_refresh.md` |
| Test interpretation | `testing_and_quality.md` |

Generated files under `../output/` are useful for inspection and release
handoff, but they are rebuildable artifacts. Do not treat them as source
truth when editing documentation.

## Maintenance Rules

- Update docs in the same change that alters commands, file counts,
  figure names, manuscript ranges, data schemas, or publication workflow.
- Keep numeric claims tied to a reproducible source: a source file,
  `output/pipeline_report.json`, a validation report, or a test assertion.
- Prefer a single authoritative explanation plus links from the other
  docs. Duplicated command blocks drift quickly.
- For new stable documentation contracts, update
  `../tests/test_documentation.py`.
- For current-event, modeled-hazard, Indigenous-history, or
  journalism-backed civic claims, use `sources_provenance_ethics.md`,
  update `claim_ledger.md`, and follow `source_refresh_workflow.md`.
