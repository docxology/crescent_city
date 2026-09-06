# scripts/ Agent Guide

## Thin-Orchestrator Contract

Scripts in this directory are entry points only: argparse, path bootstrap,
and a single delegated call into `src/<pkg>` entrypoints. No manuscript
analysis, figure logic, bibliography rules, or data handling belongs here —
that logic lives in `../src/`, where it is importable and tested. Keep CLI
options backward compatible unless tests and docs change together; use
project-root arguments instead of hard-coded absolute paths; preserve
`PYTHONPATH=. uv run python scripts/...` compatibility from the project root.

## Inventory

| Script | Pattern | Delegates to | Outputs |
|---|---|---|---|
| `run_history_pipeline.py` | Thin orchestrator; CLI: `--strict`, `--figures-only`, `--list`, `--config`, `--project-root` | `src.pipeline.run_pipeline` / `run_figures_only`, `src.figures.FIGURE_REGISTRY`, `src.report` | `output/pipeline_report.json`, `review_report.md`, `output/figures/`, publication metadata |
| `y_generate_history_figures.py` | Thin orchestrator; no CLI flags, behavior governed entirely by `FIGURE_REGISTRY` | `src.figures.generate_all_figures` (dispatches to `src/_figures/` plotters) | 25 PNG/SVG figure pairs in `output/figures/` |
| `z_generate_manuscript_variables.py` | Thin orchestrator; no CLI flags, driven by `docs/manuscript/config.yaml` | `src.manuscript_variables`, `src.config.load_project_config`, `infrastructure.prose` | `output/data/manuscript_variables.json`, substituted `output/manuscript/*.md` |

`audit/check_glossary_usage.py` is a separate single-script audit
subpackage with its own [`audit/AGENTS.md`](audit/AGENTS.md); it is a
project-local audit, unrelated to the template repo's `scripts/audit/`
guard suite.

## Gotchas

- **`y_`/`z_` prefixes encode release-sequence order, not naming style.**
  Names sort in execution order: the full pipeline first, then
  `y_generate_history_figures.py` regenerates figures, then
  `z_generate_manuscript_variables.py` hydrates variables last, immediately
  before the shared renderer
  (`scripts/pipeline/stage_03_render.py --project crescent_city`, run from
  the template repository root). Keep the prefixes when adding stage
  scripts.
- **Path bootstrap runs before imports.** `run_history_pipeline.py` and
  `z_generate_manuscript_variables.py` load `src/repo_paths.py::find_repo_root`
  via `importlib` and extend `sys.path` at module scope;
  `y_generate_history_figures.py` computes parent paths directly. All
  `src.*` / `infrastructure.*` imports stay function-local inside `main()` —
  do not hoist them above the bootstrap.
- **Two invocation spellings name the same scripts.** From this project
  root: `scripts/...`. From the template repository root:
  `projects/crescent_city/scripts/...`. Both appear in `../docs/`; neither
  is stale.
- **Outputs are regenerable.** Everything lands under `output/`; never
  hand-edit those artifacts, rerun the owning script instead.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_pipeline.py tests/test_pipeline_integration.py -q
```
