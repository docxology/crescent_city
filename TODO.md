# TODO — crescent_city

Single authoritative backlog. New findings land here as one-line entries with
file paths. Completed items get moved to the done section with a date. Status
surface: `docs/manuscript/MANUSCRIPT_STATUS.md`. Revision log:
`REVIEW_LOG_2026-08-31.md`.

## Major

- [ ] Complete the `manuscript/` → `docs/manuscript/` migration in code:
  update `src/pipeline.py` (`MANUSCRIPT_DIR`, default config path),
  `src/config.py` defaults (`manuscript_dir`, `references_path`),
  `tests/conftest.py` (`manuscript_dir` fixture), and
  `tests/test_documentation.py` (`_DOC_DIRS`, `_project_docs`,
  `test_source_to_claim_audit_covers_every_manuscript_file`) — this alone
  clears 50 test errors + 11 failures observed 2026-08-31
  (`PYTHONPATH=. uv run pytest tests/ -q`), then delete the stale
  `manuscript/` deletions from the index (paths: `src/`, `tests/`).
- [ ] Re-render and validate PDF after the migration completes:
  `PYTHONPATH=. uv run python scripts/pipeline/stage_03_render.py --project
  crescent_city` then `scripts/pipeline/stage_04_validate.py --project
  crescent_city` (paths: `output/`).

## Medium

- [ ] Decide whether `src/crescent_city.egg-info/` should stay tracked —
  build artifacts (`PKG-INFO`, `SOURCES.txt`) currently show as modified in
  `git status` (paths: `src/crescent_city.egg-info/`, `.gitignore`).
- [ ] `tests/test_documentation.py::test_project_docs_match_current_figure_registry`
  hard-codes "previous_figure_count = 18" as the only stale-count guard;
  consider deriving prior counts or dropping the pin so the next count bump
  doesn't repeat this audit's drift (paths: `tests/test_documentation.py:129`).

## Minor

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
