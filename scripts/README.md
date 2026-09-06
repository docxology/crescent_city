# Scripts Directory

Thin command-line orchestrators for the Crescent City project. Business
logic belongs in `../src/`; scripts only parse arguments, bootstrap paths,
and make a single delegated call into importable entrypoints.

## Inventory

| Script | Purpose | Delegates to | Run command |
|---|---|---|---|
| `run_history_pipeline.py` | Full quality pipeline: prose analysis, citation/bibliography and validation checks, figure generation, review report, and publication metadata. CLI: `--strict`, `--figures-only`, `--list`, `--config`, `--project-root` | `src.pipeline.run_pipeline` / `src.pipeline.run_figures_only`, `src.figures.FIGURE_REGISTRY`, `src.report` | `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --strict` |
| `y_generate_history_figures.py` | Regenerates the registered 25-figure suite (PNG + SVG pairs) into `output/figures/`; no CLI flags, registry-governed | `src.figures.generate_all_figures` → `src/_figures/` plotters | `PYTHONPATH=. uv run python scripts/y_generate_history_figures.py` |
| `z_generate_manuscript_variables.py` | Computes prose-derived variables, writes `{{TOKEN}}`-substituted manuscript copies to `output/manuscript/`, and saves `output/data/manuscript_variables.json`; no CLI flags, config-driven | `src.manuscript_variables` (`compute_variables`, `write_variables`), `src.config.load_project_config`, `infrastructure.prose` | `PYTHONPATH=. uv run python scripts/z_generate_manuscript_variables.py` |

`audit/` is a self-documented subpackage holding
`check_glossary_usage.py` (bidirectional glossary coverage audit; exits
nonzero on orphaned glossary entries): run it with
`uv run python scripts/audit/check_glossary_usage.py` and read
[`audit/README.md`](audit/README.md) and [`audit/AGENTS.md`](audit/AGENTS.md).

## Sequencing

Release order matches the names' sort order: the full pipeline (`--strict`)
first, then `y_` to regenerate figures, then `z_` to hydrate variables
immediately before the shared renderer
(`scripts/pipeline/stage_03_render.py --project crescent_city`, run from the
template repository root).

For the full render/copy-out path, see
[`../docs/rendering_and_outputs.md`](../docs/rendering_and_outputs.md).
For release sequencing, see
[`../docs/publication_checklist.md`](../docs/publication_checklist.md).
For environment assumptions and archival policy, see
[`../docs/environment_reproducibility.md`](../docs/environment_reproducibility.md)
and [`../docs/release_archival_versioning.md`](../docs/release_archival_versioning.md).
