# References {#sec:references}

The complete bibliography for this manuscript is maintained in
[`manuscript/references.bib`](references.bib) and is read by
Pandoc during PDF render. The build pipeline invokes Pandoc with
`--natbib`, so every Pandoc-style citation token in the manuscript is
rewritten to the appropriate LaTeX citation command and resolved
against the BibTeX database. The
bibliography is rendered alphabetically by first author and is
generated automatically; this section serves only as a navigational
anchor for the rendered references that follow.

This project does not auto-generate the bibliography content
itself. Instead, it validates that every cited key in the prose
has a matching entry in the BibTeX database,
via [`infrastructure.reference.citation.parse_bibfile`](../../../infrastructure/reference/citation/SKILL.md).
The validation policy is configured under `bibliography:` in
[`config.yaml`](config.yaml): `fail_on_missing: true` (missing
keys block the build); `fail_on_unused: false` (unused entries
produce warnings only).

The bibliography spans:

- Peer-reviewed primary literature (BSSA, JGR, Nature, Science,
  PAG, Geology, Earthquake Spectra, Natural Hazards)
- Federal-agency reports (USGS Professional Papers, NOAA Technical
  Memoranda, FEMA, NPS, USDA Forest Service, USGS Open-File
  Reports)
- California-agency materials (CGS, CDFW, OPC, Caltrans, CDCR)
- Court cases (*Ashker v. Brown*, *Tillie Hardwick v. United States*,
  *Citizens for Fair Representation v. Padilla*)
- Statutes (PL 90-545, PL 95-250, PL 97-79, PL 100-580,
  PL 101-601 NAGPRA, PL 101-612, PL 93-638)
- Tribal primary documents (BIA Letter of Intent 1983, Yurok-Tolowa
  IMSA Treaty 2024, California AB-1284 and AB-2356)
- University-press monographs (Atwater 2005, Tuan 1977, Cronon 1991,
  White 1995, Madley 2016, Speece 2017, Wallace 1983, Anderson 2005,
  Pritzker 2000, Cook 1976)
- Archival primary sources (*Crescent City Herald* via LCCN
  sn84026972, Del Norte County Historical Society collections)

To validate that `references.bib` is syntactically clean and
that every prose citation resolves:

```bash
uv run python -m infrastructure.reference.citation.cli validate \
    projects/crescent_city/manuscript/references.bib --strict
```
