# TODO — crescent_city

Single authoritative backlog. New findings land here as one-line entries with
file paths. Completed items get moved to the done section with a date. Status
surface: `docs/manuscript/MANUSCRIPT_STATUS.md`. Revision log:
`REVIEW_LOG_2026-08-31.md`.

## Major

- [x] Completed the `manuscript/` → `docs/manuscript/` migration in code:
  `src/pipeline.py`, `src/config.py`, `src/figures.py`, `src/publishing.py`,
  `scripts/y_generate_history_figures.py`,
  `scripts/z_generate_manuscript_variables.py`,
  `scripts/audit/check_glossary_usage.py`, `tests/conftest.py`, and
  `tests/test_american_english.py` now point at `docs/manuscript/`;
  `docs/manuscript/config.yaml` `manuscript_dir` updated. Full suite green:
  175 passed (`uv run pytest tests/ -q`, 2026-08-31).
- [ ] Re-render and validate PDF after the migration completes:
  `PYTHONPATH=. uv run python scripts/pipeline/stage_03_render.py --project
  crescent_city` then `scripts/pipeline/stage_04_validate.py --project
  crescent_city` (paths: `output/`).

## Medium

- [x] `src/crescent_city.egg-info/` untracked and gitignored; build
  artifacts no longer show as modified (2026-09-01 improvement lane;
  local working copy left on disk, now ignored).
- [ ] `tests/test_documentation.py::test_project_docs_match_current_figure_registry`
  hard-codes "previous_figure_count = 18" as the only stale-count guard;
  consider deriving prior counts or dropping the pin so the next count bump
  doesn't repeat this audit's drift (paths: `tests/test_documentation.py:129`).

## Minor

- [x] Last stale `manuscript/` doc references fixed (data/AGENTS.md,
  tests/AGENTS.md, test docstrings); stale mid-migration warning removed
  from README.md; residual "24-figure" mentions corrected to 25 in
  testing_and_quality.md, architecture.md, publication_checklist.md
  (2026-09-01 improvement lane).
- [x] README "46 topical chapters" / mixed 24/25 figure counts → corrected to
  49 chapters / 25 figures (2026-08-31, agent-ergonomics pass).
- [x] Nonexistent renderer launchers (`scripts/03_render_pdf.py` etc.) renamed
  to `scripts/pipeline/stage_NN_*.py` across README + 15 docs files
  (2026-08-31).
- [x] Broken `../manuscript/` links/paths in docs fixed to `../docs/manuscript/`
  (2026-08-31).
- [x] "58 manuscript files" → 56 numbered sources in project_overview.md,
  rendering_and_outputs.md, and the drift gate pin (2026-08-31).
- [x] Orientation/status/next-action pointer block added to README.md and
  AGENTS.md; TODO.md created (2026-08-31).

## Done

- (entries above were completed in the 2026-08-31 agent-ergonomics pass)
