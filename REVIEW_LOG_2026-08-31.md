# Review Log — 2026-08-31 (agent-ergonomics deep pass)

Scope: documentation accuracy, navigation, backlog hygiene. Source-code refactors
out of scope. All claims below verified by command on this date.

## Phase 0 — Preflight

- Branch `main`, remote `origin` = github.com/docxology/crescent_city.git.
- Dirty tree at dispatch: 95 entries — 66 deletions (`manuscript/*`, the old
  location), 28 modifications, 1 untracked (`docs/manuscript/`, the new
  location). Treat all as pre-existing; commit only files authored/edited in
  this pass.

## Phase 1 — Cold-start audit (score before fixes)

- (a) Current status: PASS — `docs/manuscript/MANUSCRIPT_STATUS.md` exists and
  is current. No root-level status pointer, so a cold agent had to find it by
  browsing; fixed by the pointer block added to README.md/AGENTS.md.
- (b) What to do next: FAIL — no backlog file existed anywhere. Fixed: TODO.md
  created at root and linked from the entry docs.
- (c) How to run primary verification: PASS with friction — commands in
  README/docs Quick Start were correct in form but two fact classes were stale
  (see findings). Verified by execution:
  `PYTHONPATH=. uv run python scripts/run_history_pipeline.py --list` → exit 0,
  prints 4 steps ("Figure generation (25 figures ...)").
  `PYTHONPATH=. uv run pytest tests/ -q` → 11 failed, 50 errors, 114 passed in
  717.95s; all 50 errors share one root cause (see F1).

## Findings

- F1 (Major, pre-existing WIP, not fixed here): the working tree holds a
  half-finished `manuscript/` → `docs/manuscript/` migration. Docs, configs and
  manuscript content moved, but `src/pipeline.py` (MANUSCRIPT_DIR),
  `src/config.py` defaults, `tests/conftest.py`, and parts of
  `tests/test_documentation.py` still assert the old `manuscript/` path → 50
  test errors + 11 failures (`pytest tests/ -q`, 2026-08-31). Verify with:
  `git status --porcelain | grep manuscript` and the pytest command above.
- F2 (Medium, fixed): README said "46 topical chapters" and mixed 24/25 figure
  counts; reality: 49 topical chapters (56 numbered files − 4 Part openers −
  abstract, introduction, references), 25 figures (len(FIGURE_REGISTRY)).
- F3 (Medium, fixed): docs referenced `scripts/03_render_pdf.py`,
  `04_validate_output.py`, `05_copy_outputs.py` — those root-level launchers do
  not exist in the current template layout (verified: template repo has only
  `scripts/pipeline/stage_NN_*.py`). Renamed in README + 15 docs files.
- F4 (Medium, fixed): broken relative links `../manuscript/SYNTAX.md` and
  `../manuscript/A1_figure_catalogue.md` in `docs/index.md`, plus bare
  `../manuscript/` path references in 7 docs files.
- F5 (Medium, fixed): "58 analyzed/combined manuscript files" in
  `docs/project_overview.md` and `docs/rendering_and_outputs.md`; actual 56
  numbered sources. The drift gate in `tests/test_documentation.py:176` pinned
  the stale literal; updated to the verified count (disclosed edit to a test).
- F6 (Minor, fixed): no orientation ladder / status pointer at the entry docs;
  no single authoritative "what next" pointer.
- Deferred: F1 (source/test migration completion) — out of scope for a docs
  lane and large enough to need its own gated pass.

## Phase 4 — Verification

- Link check over edited docs: `tests/test_documentation.py::test_project_docs_links_resolve`
  logic mirrored by grep — no remaining `../manuscript/` or
  `scripts/03_render_pdf.py` references in docs/ or README/AGENTS (grep = 0).
- Fast gate: `PYTHONPATH=. uv run pytest tests/test_documentation.py -q` — see
  commit message for result at commit time. Full suite remains red for the
  pre-existing F1 reason only.
