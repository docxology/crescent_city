"""Pipeline unit tests — heading checks, strict mode, helper functions."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml


class TestPipelineUnit:
    """Helper-function level coverage of pipeline.py."""

    def test_heading_checks_are_computed_not_hardcoded(self, manuscript_dir: Path) -> None:
        """`no_skipped_heading_levels` / `every_file_has_h1` must reflect actual report state."""
        from infrastructure.prose.report import (
            FileReport,
            ManuscriptReport,
            ProseMetrics,
            QualityReport,
            StructureReport,
        )

        from src.config import ProjectConfig
        from src.pipeline import _build_heading_checks

        bad = FileReport(
            name="broken.md",
            metrics=ProseMetrics(
                char_count=0,
                word_count=0,
                sentence_count=0,
                paragraph_count=0,
                syllable_count=0,
                avg_words_per_sentence=0.0,
                avg_syllables_per_word=0.0,
                complex_word_count=0,
                complex_word_fraction=0.0,
                flesch_reading_ease=0.0,
                flesch_kincaid_grade=0.0,
                gunning_fog=0.0,
            ),
            structure=StructureReport(has_h1=False, has_skipped_level=True),
            quality=QualityReport(),
        )
        report = ManuscriptReport(files=[bad])
        checks = _build_heading_checks(report, ProjectConfig(title="t"))
        results = {c.name: c.passed for c in checks}
        assert results["no_skipped_heading_levels"] is False
        assert results["every_file_has_h1"] is False

    def test_strict_mode_exits_nonzero_on_failure(self, tmp_path: Path) -> None:
        """Strict mode must return 1 when any check fails (no mocks)."""
        from src import pipeline as pl

        empty_bib = tmp_path / "empty.bib"
        empty_bib.write_text("", encoding="utf-8")

        cfg_path = tmp_path / "config.yaml"
        cfg_payload = {
            "paper": {"title": "Empty-bib failure scenario"},
            "bibliography": {
                "references_path": str(empty_bib),
                "fail_on_missing": True,
                "fail_on_unused": False,
            },
        }
        cfg_path.write_text(yaml.safe_dump(cfg_payload, sort_keys=False), encoding="utf-8")

        rc = pl.run_pipeline(strict=True, config_path=cfg_path)
        assert rc == 1, "strict mode should return 1 when checks fail"

    def test_run_pipeline_strict_when_clean(self) -> None:
        """End-to-end happy path: strict mode returns 0 against the real manuscript."""
        from src.pipeline import run_pipeline

        assert run_pipeline(strict=True) == 0

    def test_run_script_list_reports_current_figure_count(self, project_root: Path, repo_root: Path) -> None:
        """The CLI step list must not drift from the figure registry."""
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "run_history_pipeline.py"), "--list"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert "24 figures" in result.stdout
        assert "Figure generation (8 figures" not in result.stdout

    def test_figures_only_skips_full_pipeline(self, project_root: Path, repo_root: Path) -> None:
        """`--figures-only` should not run prose checks or write review summaries."""
        result = subprocess.run(
            [sys.executable, str(project_root / "scripts" / "run_history_pipeline.py"), "--figures-only"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=180,
        )
        assert result.returncode == 0, result.stderr[-500:]
        assert "Crescent City History — Figure Generation" in result.stdout
        assert "Checks passed:" not in result.stdout
        assert "Review written" not in result.stdout


class TestSourceCode:
    """Validate source modules import cleanly."""

    def test_figures_importable(self) -> None:
        from src.figures import generate_all_figures

        assert callable(generate_all_figures)

    def test_pipeline_importable(self) -> None:
        from src.pipeline import run_figures_only, run_pipeline

        assert callable(run_pipeline)
        assert callable(run_figures_only)

    def test_report_importable(self) -> None:
        from src.report import write_review_report

        assert callable(write_review_report)

    def test_publishing_importable(self) -> None:
        from src.publishing import write_publishing_artifacts

        assert callable(write_publishing_artifacts)

    def test_run_script_syntax(self, project_root: Path) -> None:
        import py_compile

        py_compile.compile(str(project_root / "scripts" / "run_history_pipeline.py"), doraise=True)
