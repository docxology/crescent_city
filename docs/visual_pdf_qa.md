# Visual PDF QA

This runbook covers rendered-output review after the manuscript builds.
It is intentionally separate from source-to-claim review: the PDF can be
valid while a figure is visually crowded or a caption is hard to read.

## Automated Smoke Checks

The test suite now includes a rendered-PDF smoke check when the combined
PDF and Poppler tools are available:

- `tests/test_pipeline_integration.py::TestPDFProvenance::test_pdf_has_reasonable_page_count`
- `tests/test_pipeline_integration.py::TestPDFProvenance::test_rendered_pdf_sample_pages_are_nonblank`

The checks validate that:

- the combined PDF exists and is non-trivial;
- the page count remains in the expected manuscript band;
- sampled pages rasterize with `pdftoppm`;
- sampled pages are not blank after rasterization.

These tests do not replace human review of figure scale, caption
placement, or table flow.

## Manual Review Checklist

Open `output/pdf/crescent_city_combined.pdf` after rendering and inspect:

| Area | What to check |
|---|---|
| Title and table of contents | Title metadata, authorship, DOI status, and page numbering render cleanly. |
| First figure | Caption wraps cleanly and the figure is not clipped. |
| Current-events figure | Marker legend, source-tier explanation, and scheduled/provisional status are readable. |
| Housing figure | Planned units, vouchers, and funding awards remain visually distinct. |
| Archaeology figure | No protected locations, identifiers, or site-specific hints appear in the visual or caption. |
| Healthcare network | Edges and labels are legible and do not imply measured patient flow or adequacy. |
| Hazard figures | Scenario, projection, measured, and modeled evidence classes remain distinguishable. |
| Appendices | Figure catalog entries and long descriptions remain readable in PDF and HTML. |

## Command Sequence

From the project directory:

```bash
PYTHONPATH=. uv run pytest tests/test_figures.py tests/test_pipeline_integration.py -q
```

From the template repository root:

```bash
PYTHONPATH=. uv run python scripts/03_render_pdf.py --project crescent_city
PYTHONPATH=. uv run python scripts/04_validate_output.py --project crescent_city
```

If any figure appears clipped or visually ambiguous, edit the source
plotter or caption, regenerate figures, then render again. Do not edit
generated PDFs or images directly.
