# docs/ Agent Guide

## Purpose

This directory is the project documentation hub. Keep it short, current,
and oriented around navigation: what exists, where to run commands, and
which source files are authoritative.

## Contracts

- Root `../README.md` is the public quick start.
- Root `../AGENTS.md` is the agent-oriented project contract.
- Folder-level `README.md` and `AGENTS.md` files provide local edit rules.
- Documentation drift is guarded by `../tests/test_documentation.py`.
- The figure registry in `../src/figures.py` controls figure counts and
  plotter names.
- The strict pipeline report controls current word, citation, check, and
  figure metrics.
- Claim-refresh guidance belongs in `claim_ledger.md`,
  `source_to_claim_audit.md`, `current_events_refresh.md`, and
  `source_refresh_workflow.md`; source-tier and ethics policy belongs in
  `sources_provenance_ethics.md`; do not scatter one-off source policies
  across unrelated docs.
- Environment, release, audit-limit, accessibility, and data-QA policy
  have dedicated docs. Link to those files instead of duplicating their
  command blocks or definitions.

## Checks

```bash
PYTHONPATH=. uv run pytest tests/test_documentation.py tests/test_american_english.py -q
```

Do not document generated files as source truth; point readers to
`../output/` only as a rebuildable artifact location.

## Edit Rules

- Prefer task-oriented docs over status logs.
- Remove superseded repair narratives when a policy or test now captures
  the rule.
- Keep dates exact when describing current-event refreshes.
- Use relative Markdown links for source files and docs only when the
  target is checked in.
- After adding a doc, link it from both `README.md` and `index.md`.
- If a doc becomes canonical for maintenance, add it to
  `../tests/test_documentation.py`.
