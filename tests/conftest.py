"""Conftest for the Crescent City history pipeline tests.

All tests use real file I/O — no mocks, no external API fixtures.

The pipeline is **not** run automatically. Tests that need pipeline-
generated artifacts request the ``pipeline_artifacts`` session fixture
explicitly; pure prose/citation/data tests run without paying that
cost. This keeps unit-test wall time under one second per file.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ── Resolve paths relative to this test file ────────────────────────────

_PROJECT_DIR = Path(__file__).resolve().parent.parent  # projects/crescent_city
_REPO_ROOT = _PROJECT_DIR.parent.parent  # repository root

sys.path.insert(0, str(_REPO_ROOT))
sys.path.insert(0, str(_PROJECT_DIR / "src"))
sys.path.insert(0, str(_PROJECT_DIR))


# ── Fixtures ────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def project_root() -> Path:
    return _PROJECT_DIR


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return _REPO_ROOT


@pytest.fixture(scope="session")
def manuscript_dir(project_root: Path) -> Path:
    assert (project_root / "manuscript").is_dir()
    return project_root / "manuscript"


@pytest.fixture(scope="session")
def data_dir(project_root: Path) -> Path:
    assert (project_root / "data").is_dir()
    return project_root / "data"


@pytest.fixture(scope="session")
def output_dir(project_root: Path) -> Path:
    d = project_root / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def figures_dir(output_dir: Path) -> Path:
    """Directory where the pipeline writes figure PNG/SVG pairs."""
    d = output_dir / "figures"
    d.mkdir(parents=True, exist_ok=True)
    return d


@pytest.fixture(scope="session")
def config(project_root: Path):
    """Load the project configuration."""
    from infrastructure.config.loader import load_config

    return load_config(str(project_root / "manuscript"))


@pytest.fixture(scope="session")
def pipeline_artifacts(output_dir: Path):
    """Run the full pipeline once per session; cached for downstream tests.

    Opt-in — tests that don't need pipeline-generated artifacts should
    not request this fixture, because it forces a ~30 s pipeline run
    before the first test that calls it.
    """
    from src.pipeline import run_pipeline

    rc = run_pipeline(strict=False)
    assert rc == 0, f"Pipeline returned non-zero ({rc}); see output/pipeline_report.json"
    return {
        "rc": rc,
        "pipeline_report": output_dir / "pipeline_report.json",
        "manuscript_report": output_dir / "manuscript_report.json",
        "review_report": output_dir / "review_report.md",
        "figures_dir": output_dir / "figures",
    }
