# Release, Archival, And Versioning

This guide describes how to prepare a public Crescent City release and
how to archive the artifact without breaking provenance. It extends the
operational [publication_checklist.md](publication_checklist.md) with
versioning and deposit policy.

## Release Criteria

A public release candidate is ready only when all of these are true:

| Gate | Required evidence |
|---|---|
| Source freshness | [claim_ledger.md](claim_ledger.md) and [source_refresh_workflow.md](source_refresh_workflow.md) have been checked for volatile claims. |
| Project tests | The project test suite or targeted release subset passes. |
| Strict pipeline | `scripts/run_history_pipeline.py --strict` passes and writes current reports. |
| Render | `scripts/03_render_pdf.py --project crescent_city` succeeds from the template root. |
| Validation | `scripts/04_validate_output.py --project crescent_city` passes. |
| Copy-out | `scripts/05_copy_outputs.py --project crescent_city` creates the repository-level release folder. |
| Metadata | `CITATION.cff`, `zenodo_metadata.json`, and `self_citation.bib` are regenerated from `manuscript/config.yaml`. |

Do not treat a green test run as a release by itself. Current public
records can change after tests pass.

## Version Source

The current manuscript version is:

```yaml
paper:
  version: "1.0.0"
```

from `../manuscript/config.yaml`. That value drives generated publishing
metadata. Change it only when preparing a release, correction, or
substantive public revision.

Use this version pattern:

| Change | Version action |
|---|---|
| Typo, formatting, or link-only correction before public deposit | Keep the same version. |
| Public correction that changes an already shared artifact | Increment patch version. |
| New sources, revised claims, new figures, or changed argument | Increment minor version. |
| Structural manuscript change or incompatible data/figure contract | Increment major version. |

If a repository tag is used, match it to the project version, for
example `crescent-city-v1.0.0`.

## Release Artifact Set

Archive the artifact set that a reader needs to inspect, cite, and
rebuild the release.

| Artifact | Path |
|---|---|
| Project-local PDF | `projects/crescent_city/output/pdf/crescent_city_combined.pdf` |
| Repository-level PDF copy | `output/crescent_city/crescent_city_combined.pdf` |
| Combined HTML | `projects/crescent_city/output/web/index.html` |
| Validation report | `projects/crescent_city/output/reports/validation_report.md` |
| Project pipeline report | `projects/crescent_city/output/pipeline_report.json` |
| Review report | `projects/crescent_city/output/review_report.md` |
| Figure outputs | `projects/crescent_city/output/figures/` |
| Citation metadata | `projects/crescent_city/output/CITATION.cff` |
| Deposit metadata | `projects/crescent_city/output/zenodo_metadata.json` |
| Self-citation | `projects/crescent_city/output/self_citation.bib` |

Generated artifacts are archived for readers, but source truth remains in
the checked-in manuscript, data, code, tests, and documentation.

## DOI And Zenodo Flow

The assigned archival DOI is `10.5281/zenodo.20286171`, and
`../manuscript/config.yaml` is the source of truth for both the DOI and
the public repository URL, `https://github.com/docxology/crescent_city`.
For each release:

1. Confirm `publication.doi` and `publication.repository_url`.
2. Rerun the strict project pipeline so CFF, Zenodo metadata, and
   self-citation outputs are regenerated.
3. Render and validate the PDF so the title-page DOI path is current.
4. Recheck `output/CITATION.cff`, `output/zenodo_metadata.json`, and
   `output/self_citation.bib` for DOI and repository-url agreement.
5. Deposit the release artifact set.

If a DOI deposit is made before a tagged source release is public,
record the exact source snapshot used for the deposit in the release
notes.

## Checksums

For an archival handoff, compute checksums after validation and copy-out:

```bash
shasum -a 256 \
  projects/crescent_city/output/pdf/crescent_city_combined.pdf \
  output/crescent_city/crescent_city_combined.pdf \
  projects/crescent_city/output/CITATION.cff \
  projects/crescent_city/output/zenodo_metadata.json \
  projects/crescent_city/output/self_citation.bib
```

Store checksums in release notes or the deposit record. Do not edit
generated files after checksums are computed.

## Correction And Supersession Policy

Use this rule set after public sharing:

| Situation | Action |
|---|---|
| Broken link or typo | Correct source, rerun docs tests, and update release notes if the artifact was already shared. |
| Source correction changes a factual claim | Update data or prose, rerun targeted tests, rerender, increment patch version, and document the correction. |
| Current-event status changes | Treat it as a new source-refresh event, not an error in the prior release. |
| Sensitive material should be removed | Remove or generalize the material, rerun tests and render, increment patch or minor version, and document the ethical reason without repeating the sensitive detail. |
| DOI deposit superseded | Publish a new versioned deposit and link it to the prior record when the platform supports versioning. |

Never silently replace a public artifact after citation or deposit. Issue
a versioned correction so readers can reconcile citations and source
snapshots.
