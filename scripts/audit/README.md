# scripts/audit — glossary audit

Holds `check_glossary_usage.py`: bidirectional glossary coverage audit.
Direction 1 (glossary → prose): every `**term** —` entry in
`docs/manuscript/A2_glossary.md` must appear in manuscript prose (normalized
matching; exits nonzero with diagnostics on orphans). Direction 2
(prose → glossary, acronym coverage) is enforced by `tests/test_glossary.py`.

Usage: `uv run python scripts/audit/check_glossary_usage.py`
