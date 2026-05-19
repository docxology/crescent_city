"""Tests for src.report — markdown review-report assembly."""

from __future__ import annotations

from pathlib import Path


def test_write_review_report_branches_with_figures(manuscript_dir: Path, tmp_path: Path) -> None:
    from infrastructure.prose.report import analyze_manuscript

    from src.pipeline import CheckResult
    from src.report import write_review_report

    mr = analyze_manuscript(manuscript_dir)
    chk = (
        CheckResult("grade_band", True, "ok"),
        CheckResult("other", False, "detail"),
    )

    p = tmp_path / "full_review.md"
    written_path = write_review_report(
        p,
        title="Crescent QA",
        manuscript_report=mr,
        checks=chk,
        include_per_file_table=True,
        include_outline=True,
        include_quality_flags=True,
        figures=[tmp_path / "fake_figure.png"],
    )
    written = Path(written_path).read_text(encoding="utf-8")
    assert "Crescent QA" in written
    assert "## Figures" in written
    assert "fake_figure.png" in written

    p_min = tmp_path / "minimal.md"
    write_review_report(
        p_min,
        title="Short",
        manuscript_report=mr,
        checks=list(chk),
        include_per_file_table=False,
        include_outline=False,
        include_quality_flags=False,
        figures=None,
    )
    body = p_min.read_text(encoding="utf-8")
    assert "Per-file metrics" not in body
