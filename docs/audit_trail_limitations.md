# Audit Trail And Limitations

This guide maps where Crescent City records decisions, checks, evidence
limits, and known gaps. It is a reviewer-facing index, not a substitute
for reading the underlying sources.

## Audit Trail Map

| Question | Audit location |
|---|---|
| Which claim classes need refresh? | [claim_ledger.md](claim_ledger.md) |
| How should source upgrades be performed? | [source_refresh_workflow.md](source_refresh_workflow.md) |
| What source tiers and ethical boundaries apply? | [sources_provenance_ethics.md](sources_provenance_ethics.md) |
| What data files support figures and timelines? | [data_dictionary.md](data_dictionary.md) and `../data/` |
| Which tests guard a change? | [testing_and_quality.md](testing_and_quality.md) |
| What did the latest pipeline check? | `../output/pipeline_report.json` and `../output/review_report.md` |
| What did output validation check? | `../output/reports/validation_report.md` |
| What risks were identified in adversarial review? | [redteam_review_2026-05-15.md](redteam_review_2026-05-15.md) |
| Which figure supports a visual claim? | `../manuscript/A1_figure_catalogue.md` and [figure_maintenance.md](figure_maintenance.md) |
| Which citation keys are cited or reserved? | `../manuscript/references.bib`, `../manuscript/config.yaml`, and [claim_ledger.md](claim_ledger.md) |

Generated reports are useful audit evidence for a specific run. They are
not source truth and should be regenerated after source edits.

## What The Build Proves

A green build proves that:

- The manuscript has expected structure and anchors.
- Citation keys resolve against the local BibTeX file.
- Reserve bibliography keys are explicit.
- Data files match current schemas and current-event metadata rules.
- The 24 registered figures regenerate through the project API.
- Documentation links and guarded facts still resolve.
- The shared renderer can build and validate output artifacts when run.

It does not prove that every historical statement is true, complete, or
fresh. It also does not prove that public sources are morally sufficient
for every sensitive claim.

## Known Limitations

| Area | Limitation | Mitigation |
|---|---|---|
| Current events | Public records and local reporting can change after `checked_as_of`. | Use refresh triggers and rerun current-event tests before release. |
| Indigenous history | Public sources may omit community knowledge, and some knowledge should remain unpublished. | Use public or authorized material only and avoid restricted detail. |
| Archaeology | Public evidence must not disclose protected site information. | Use evidence layers and generalized locations. |
| Local journalism | Reporting can be the only public signal before official records appear. | Mark the row with the correct journalism tier and re-audit when official records appear. |
| Modeled hazards | Cascadia, sea-level, and flood values are scenario or model outputs, not certain predictions. | Preserve modeled, projected, and measured language. |
| Economic estimates | Historic sector estimates combine instruments with different definitions. | Keep source keys and estimate type visible. |
| PDF bytes | TeX, font, and timestamp differences can change PDF bytes. | Compare source, reports, and SVGs when bit-for-bit checks matter. |

## Decision Log Template

Use this compact template inside a release note, issue, or future
documentation update when a judgment call affects public interpretation.

```text
Date:
Decision:
Affected files:
Claim or artifact:
Source evidence:
Alternatives considered:
Reason for choice:
Tests or render commands run:
Follow-up trigger:
```

Do not use the decision log to preserve outdated narratives. If a rule is
now enforced by tests or a stable doc, link to the rule and remove the
old repair story.

## Revision Log Template

Use this template when a public claim changes after source refresh.

```text
Version:
Date:
Prior wording or artifact:
New wording or artifact:
Reason for change:
Source keys added or removed:
Data rows changed:
Figures regenerated:
Verification commands:
```

If the change involves sensitive material, document the category and
reason without repeating the sensitive detail.

## Reviewer Checklist

Before publication or deposit, confirm:

- Volatile claims in [claim_ledger.md](claim_ledger.md) have been checked.
- Current-event rows use one of the enforced `source_tier` values.
- Figure captions keep evidence class and interpretive claim separate.
- Local journalism is not carrying technical, legal, or scientific facts
  when an official source exists.
- Indigenous and archaeology sections avoid restricted or site-specific
  material.
- Release artifacts were regenerated after source edits.
- Any correction to a public artifact is versioned through
  [release_archival_versioning.md](release_archival_versioning.md).
