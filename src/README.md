# Source Package

`src/` contains the importable Crescent City project logic. The package
turns manuscript, data, and config inputs into reports, figures, publishing
metadata, and renderer variables.

## Main Modules

| Module | Role |
|---|---|
| `config.py` | Typed loader for `manuscript/config.yaml` |
| `pipeline.py` | Prose, citation, heading, bibliography, figure, and report orchestration |
| `figures.py` | Public figure API, `FIGURE_REGISTRY`, and figure-manifest provenance fields |
| `manuscript_variables.py` | Computes and writes manuscript substitution variables |
| `report.py` | Writes the human-readable review report |
| `publishing.py` | Writes CFF, Zenodo metadata, and self-citation BibTeX |
| `_figures/` | Figure implementation modules |

## Development Rules

- Keep code deterministic and offline after dependency installation.
- Keep data schemas stable unless tests and docs are updated in the same
  change.
- Add tests for every new gate, figure, or publishing behavior.
- For figure registry changes, follow
  [`../docs/figure_maintenance.md`](../docs/figure_maintenance.md).
- Keep figure provenance synchronized with
  [`../data/figure_provenance.csv`](../data/figure_provenance.csv).
- For test selection and green-build semantics, follow
  [`../docs/testing_and_quality.md`](../docs/testing_and_quality.md).
- For source-tier, provenance, and sensitive-material rules that affect
  data loaders or figure claims, follow
  [`../docs/sources_provenance_ethics.md`](../docs/sources_provenance_ethics.md).
- For executable data-QA coverage and planned checks, follow
  [`../docs/data_validation_qa.md`](../docs/data_validation_qa.md).
