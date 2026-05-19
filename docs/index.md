# Crescent City Documentation

This folder maps the working documentation for the `crescent_city`
research exemplar. Start with the task you are trying to complete.

## By Task

| Task | Start here | Then check |
|---|---|---|
| Run the project for the first time | [quickstart.md](quickstart.md) | [project_overview.md](project_overview.md) |
| Render the paper PDF | [rendering_and_outputs.md](rendering_and_outputs.md) | [publication_checklist.md](publication_checklist.md) |
| Understand module boundaries | [architecture.md](architecture.md) | `../src/README.md`, `../scripts/README.md` |
| Understand the data files | [data_dictionary.md](data_dictionary.md) | `../data/README.md`, [claim_ledger.md](claim_ledger.md) |
| Check source provenance and ethics | [sources_provenance_ethics.md](sources_provenance_ethics.md) | [claim_ledger.md](claim_ledger.md), [source_refresh_workflow.md](source_refresh_workflow.md) |
| Audit source-to-claim fit | [source_to_claim_audit.md](source_to_claim_audit.md) | [claim_ledger.md](claim_ledger.md), [sources_provenance_ethics.md](sources_provenance_ethics.md) |
| Review data QA controls | [data_validation_qa.md](data_validation_qa.md) | `../tests/test_data.py`, [testing_and_quality.md](testing_and_quality.md) |
| Add or revise a figure | [figure_maintenance.md](figure_maintenance.md) | `../src/_figures/README.md`, `../manuscript/A1_figure_catalogue.md` |
| Edit manuscript prose | [manuscript_authoring.md](manuscript_authoring.md) | `../manuscript/SYNTAX.md`, [claim_ledger.md](claim_ledger.md) |
| Update a recent civic event | [current_events_refresh.md](current_events_refresh.md) | [source_refresh_workflow.md](source_refresh_workflow.md), [claim_ledger.md](claim_ledger.md) |
| Choose tests for a change | [testing_and_quality.md](testing_and_quality.md) | `../tests/README.md` |
| Reproduce the environment | [environment_reproducibility.md](environment_reproducibility.md) | [rendering_and_outputs.md](rendering_and_outputs.md) |
| Prepare a public release | [publication_checklist.md](publication_checklist.md) | [rendering_and_outputs.md](rendering_and_outputs.md) |
| Archive or version a release | [release_archival_versioning.md](release_archival_versioning.md) | [publication_checklist.md](publication_checklist.md) |
| Review evidence risk | [claim_ledger.md](claim_ledger.md) | [redteam_review_2026-05-15.md](redteam_review_2026-05-15.md) |
| Review audit limits | [audit_trail_limitations.md](audit_trail_limitations.md) | [redteam_review_2026-05-15.md](redteam_review_2026-05-15.md) |
| Check reader experience | [accessibility_reader_experience.md](accessibility_reader_experience.md) | [visual_pdf_qa.md](visual_pdf_qa.md), [figure_maintenance.md](figure_maintenance.md), [publication_checklist.md](publication_checklist.md) |
| Edit documentation | [README.md](README.md) | [AGENTS.md](AGENTS.md), `../tests/test_documentation.py` |

## Stable References

| Topic | File |
|---|---|
| Public project overview | [../README.md](../README.md) |
| Agent project contract | [../AGENTS.md](../AGENTS.md) |
| Manuscript syntax | [../manuscript/SYNTAX.md](../manuscript/SYNTAX.md) |
| Figure catalog | [../manuscript/A1_figure_catalogue.md](../manuscript/A1_figure_catalogue.md) |
| Data file contract | [../data/README.md](../data/README.md) |
| Script contract | [../scripts/README.md](../scripts/README.md) |
| Test contract | [../tests/README.md](../tests/README.md) |
| Source and ethics contract | [sources_provenance_ethics.md](sources_provenance_ethics.md) |
| Source-to-claim audit | [source_to_claim_audit.md](source_to_claim_audit.md) |
| Current-event refresh protocol | [current_events_refresh.md](current_events_refresh.md) |
| Visual PDF QA | [visual_pdf_qa.md](visual_pdf_qa.md) |

## Reading Path

For orientation, read `project_overview.md`, then `architecture.md`. For
work, use the runbook that matches the task. For source freshness,
publication, or archival handoff, use the audit and checklist docs before
rendering.
