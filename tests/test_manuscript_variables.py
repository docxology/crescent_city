"""Tests for src.manuscript_variables — substitution variables."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_manuscript_variables_round_trip(manuscript_dir: Path, tmp_path: Path) -> None:
    from infrastructure.prose.report import analyze_manuscript

    from src.manuscript_variables import (
        compute_variables,
        substitute_in_text,
        write_variables,
    )

    mr = analyze_manuscript(manuscript_dir)
    vars_blob = compute_variables(mr, "History study")
    assert vars_blob.total_words > 500
    text = substitute_in_text("{{TOTAL_WORDS}} {{UNKNOWN_TOKEN}}", vars_blob)
    assert "{{UNKNOWN_TOKEN}}" in text

    outs = write_variables(vars_blob, manuscript_dir, tmp_path)
    assert len(outs) >= 40
    assert (tmp_path / "manuscript" / "references.bib").exists()


def test_write_variables_removes_stale_markdown(manuscript_dir: Path, tmp_path: Path) -> None:
    from infrastructure.prose.report import analyze_manuscript

    from src.manuscript_variables import compute_variables, write_variables

    stale = tmp_path / "manuscript" / "removed_section.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale", encoding="utf-8")

    vars_blob = compute_variables(analyze_manuscript(manuscript_dir), "History study")
    write_variables(vars_blob, manuscript_dir, tmp_path)

    assert not stale.exists()


def test_manuscript_variables_to_dict_shape(manuscript_dir: Path) -> None:
    from infrastructure.prose.report import analyze_manuscript

    from src.manuscript_variables import compute_variables

    mr = analyze_manuscript(manuscript_dir)
    d = compute_variables(mr, "T").to_dict()
    for required in (
        "TOTAL_WORDS",
        "TOTAL_SENTENCES",
        "TOTAL_PARAGRAPHS",
        "AVG_GRADE_LEVEL",
        "AVG_READING_EASE",
        "AVG_GUNNING_FOG",
        "CITATION_COUNT",
        "FILES_ANALYZED",
        "LONGEST_SECTION_WORDS",
        "SHORTEST_SECTION_WORDS",
    ):
        assert required in d


def test_variable_script_writes_canonical_data_payload(project_root: Path, repo_root: Path) -> None:
    """The renderer-facing JSON belongs under output/data."""
    result = subprocess.run(
        [sys.executable, str(project_root / "scripts" / "z_generate_manuscript_variables.py")],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr[-500:]

    canonical = project_root / "output" / "data" / "manuscript_variables.json"
    assert canonical.exists()
