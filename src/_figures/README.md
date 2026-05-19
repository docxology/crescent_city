# Figure Modules

This package contains the matplotlib plotters behind the manuscript's
registered 24 figures. Plotters are called through `../figures.py`.

## Module Map

| Module | Figures |
|---|---|
| `manuscript_metrics.py` | Word count, readability, citation density |
| `systems.py` | Nested systems map |
| `demographics.py` | Population and economic sector figures |
| `tsunami.py` | Tsunami and disaster figures |
| `history.py` | Historical timeline |
| `cartography.py` | Regional map and non-coordinate Tolowa relationship schematic |
| `conservation.py` | Redwood decline |
| `geophysics.py` | Cascadia paleoseismology |
| `political_geography.py` | State of Jefferson map |
| `climate.py` | Climograph and sea-level scenarios |
| `ecology.py` | Smith River protection figure |
| `community_systems.py` | Housing, transportation, archaeology, and health access figures |
| `harbor_history.py` | Harbor timeline |
| `currents.py` | 2024-2026 current-events timeline |

## Rules

- Save figures through `_io.save_figure()` so PNG and SVG siblings are
  written together.
- Use `_style.py` for palette and plotting defaults.
- Store factual dates, counts, amplitudes, event labels, and summary
  statistics in `../../data/` with `source_keys`; keep only schematic
  geometry and label-layout mechanics in code.
- Store figure-level source freshness, reader risk, and long descriptions
  in `../../data/figure_provenance.csv`.
- Keep labels readable in the rendered PDF, not only in standalone PNGs.

For the registry contract, caption standard, and verification sequence,
see [`../../docs/figure_maintenance.md`](../../docs/figure_maintenance.md).
For reader-facing figure accessibility and sensitive map boundaries, see
[`../../docs/accessibility_reader_experience.md`](../../docs/accessibility_reader_experience.md)
and [`../../docs/sources_provenance_ethics.md`](../../docs/sources_provenance_ethics.md).
