# Publication Checklist

Use this checklist before sharing or archiving a public Crescent City
paper build. It assumes commands are run from the template repository
root unless noted otherwise.

## 1. Source Freshness

- Review `docs/claim_ledger.md` for volatile claims.
- Review `docs/source_to_claim_audit.md` for section-level claim-fit
  controls.
- Check `docs/sources_provenance_ethics.md` for source-tier, provenance,
  reuse, and sensitive-material boundaries.
- Follow `docs/current_events_refresh.md` for the 2024-2026 trigger
  matrix before updating recent rows.
- Follow `docs/source_refresh_workflow.md` for any 2024 onward current
  event, scheduled event, agency correction, court update, grant update,
  election result, or fishery update.
- Use `docs/data_dictionary.md` to check which data files and provenance
  fields are affected.
- Use `docs/manuscript_authoring.md` for evidence-language and citation
  rules.
- Confirm future scheduled rows are not written as completed history.
- Confirm Indigenous and archaeological material remains public,
  generalized, and authorized for this manuscript context.

## 2. Project Checks

```bash
PYTHONPATH=. uv run pytest projects/crescent_city/tests/ -q
PYTHONPATH=. uv run python projects/crescent_city/scripts/run_history_pipeline.py --strict
```

Confirm `projects/crescent_city/output/pipeline_report.json` reports:

- `checks_passed` equals `checks_total`.
- `figures_generated` is 24.
- `figures_ok` is true.
- `bibliography_consistency` is true.

## 3. Render And Validate

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
PYTHONPATH=. uv run python scripts/05_copy_outputs.py --project crescent_city
```

Confirm these files exist:

```text
projects/crescent_city/output/pdf/crescent_city_combined.pdf
projects/crescent_city/output/web/index.html
projects/crescent_city/output/reports/validation_report.md
output/crescent_city/crescent_city_combined.pdf
```

## 4. Metadata

Check the publication metadata generated from `manuscript/config.yaml`:

```text
projects/crescent_city/output/CITATION.cff
projects/crescent_city/output/zenodo_metadata.json
projects/crescent_city/output/self_citation.bib
```

If title, authors, license, keywords, DOI, or publication year changes,
edit `manuscript/config.yaml`, rerun the strict project pipeline, then
render again.

## 5. Reader-Facing Spot Checks

- Open the combined PDF and inspect the title page, table of contents,
  first figure, bibliography, and appendices.
- Open `output/crescent_city/crescent_city_combined.pdf` after copy-out,
  not only the project-local copy.
- Open `projects/crescent_city/output/web/index.html` if an HTML handoff
  is needed.
- Confirm links and cross-references do not show unresolved raw tokens in
  the PDF.
- Confirm figure count and figure captions match the 24-figure registry.
- Confirm figure long descriptions and provenance fields match
  `data/figure_provenance.csv`.
- Follow `docs/visual_pdf_qa.md` for sampled rendered-page and
  figure-heavy-page review.

## 6. Completion Criteria

A release candidate is ready when:

- Source freshness review is complete for volatile claims.
- Project tests pass.
- Strict project pipeline passes.
- PDF render succeeds.
- Output validation passes.
- Copy-out succeeds.
- Reader-facing accessibility spot checks are complete.
- The release-facing combined PDF is present under `output/crescent_city/`.

A green build is not a substitute for source freshness. If a public record
changed after the last `checked_as_of` date, refresh the source before
sharing the PDF.
