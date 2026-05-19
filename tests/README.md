# Tests Directory

The project test suite guards manuscript structure, citation integrity,
figure contracts, documentation drift, publishing metadata, and pipeline
behavior.

## Test Areas

| File | Role |
|---|---|
| `test_documentation.py` | Documentation links, folder docs, and drift guards |
| `test_american_english.py` | American-English style guard for authored text |
| `test_citations.py` | Citation and bibliography consistency |
| `test_manuscript.py` | Manuscript structure, cross-reference anchors, and figure catalog fields |
| `test_figures.py` | Figure registry, determinism, provenance manifest, and output shape |
| `test_pipeline*.py` | CLI, pipeline integration behavior, and rendered-PDF smoke checks |
| `test_data.py` | Data file shape, current-event records, and figure provenance rows |

## Run

```bash
PYTHONPATH=. uv run pytest tests/ -q
```

Tests use real files and subprocesses; do not replace project behavior with
mocks.

For the command matrix and failure triage, see
[`../docs/testing_and_quality.md`](../docs/testing_and_quality.md).
For the source-tier and data-QA contract guarded by these tests, see
[`../docs/sources_provenance_ethics.md`](../docs/sources_provenance_ethics.md)
and [`../docs/data_validation_qa.md`](../docs/data_validation_qa.md).
