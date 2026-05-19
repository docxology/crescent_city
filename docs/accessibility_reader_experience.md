# Accessibility And Reader Experience

This guide records the reader-facing quality expectations for the
Crescent City manuscript and generated artifacts. It is a documentation
standard for this project; it does not claim full automated WCAG
compliance.

## Reader Profiles

| Reader | Need |
|---|---|
| Local reader | Clear narrative, visible source trail, and non-specialist explanation of technical claims. |
| Scholarly reviewer | Citations, methods, evidence classes, and reproducible figure/data paths. |
| Civic or agency reader | Dated public-status claims, source tiers, and clear separation of proposed, scheduled, and completed events. |
| Screen-reader or low-vision reader | Logical heading order, meaningful figure captions, readable tables, and text that does not depend only on color. |
| Future maintainer | Stable commands, doc links, and test-backed expectations. |

## Format Expectations

| Format | Expectation |
|---|---|
| PDF | Primary reading artifact; inspect title page, table of contents, figures, references, and appendices before release. |
| HTML | Secondary reading artifact; useful for quick navigation and link inspection. |
| Markdown | Source format; keep citations, anchors, and substitution tokens intact. |
| Figures | PNG for rendered manuscript visuals, SVG for deterministic checks and inspection. |

When formats disagree, fix the source Markdown, data, figure code,
preamble, or renderer path rather than editing generated output.

## Figure Accessibility Standard

Every figure should be understandable through its caption and appendix
catalog entry.

| Element | Rule |
|---|---|
| Caption | State what is shown, the evidence class, and the interpretive claim. |
| Source trail | Keep `source_keys` in data files and data-source notes in the figure catalog. |
| Long description | Keep a concise description in `manuscript/A1_figure_catalogue.md` and `data/figure_provenance.csv`. |
| Reader risk | Use the `reader_risk` field in `data/figure_provenance.csv` to flag figures that can be overread. |
| Color | Use the project palette consistently and avoid relying on color alone when shape, label, ordering, or line style can carry the same distinction. |
| Labels | Keep text large enough for the rendered PDF, not just the standalone PNG. |
| Sensitive maps | Generalize Indigenous and archaeology locations and omit protected coordinates. |

The current automated tests inspect caption structure, long-description
coverage, figure output shape, SVG text preservation, and sampled
rendered-PDF pages. They do not yet run a full screen-reader or
color-contrast audit.

## Text And Table Standard

- Use heading levels consistently with the manuscript syntax rules.
- Use Pandoc citations and anchors instead of hard-coded figure or
  section numbers.
- Keep tables narrow enough to read in PDF output.
- Prefer plain date and status language for current events.
- State uncertainty in the sentence that uses the number.
- Avoid unexplained acronyms in captions and tables.

For manuscript mechanics, use [manuscript_authoring.md](manuscript_authoring.md)
and `../manuscript/SYNTAX.md`.

## Release Spot Check

Before sharing a public artifact:

1. Open `projects/crescent_city/output/pdf/crescent_city_combined.pdf`.
2. Check the title page, table of contents, one text-heavy chapter, one
   table, the first figure, a current-event figure, and the appendices.
3. Confirm no figure label overlaps or becomes unreadable.
4. Confirm citation and cross-reference tokens are rendered, not raw.
5. Use [visual_pdf_qa.md](visual_pdf_qa.md) for the figure-heavy pages
   and appendix checks.
6. Open `projects/crescent_city/output/web/index.html` when HTML is part
   of the handoff.
7. Confirm generated artifacts match the paths in
   [rendering_and_outputs.md](rendering_and_outputs.md).

## Future Automated Checks

Potential future checks include:

- PDF text extraction and heading-order sampling.
- HTML link and landmark checks.
- Figure color-contrast checks.
- Caption completeness checks beyond the current manuscript assertions.
- Automated scan for raw cross-reference tokens in rendered outputs.

Do not document these as implemented until tests or renderer validation
actually enforce them.
