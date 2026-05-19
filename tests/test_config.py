"""Configuration tests — manuscript/config.yaml + src.config loader."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


class TestConfig:
    """Validate manuscript configuration."""

    def test_config_exists(self, manuscript_dir: Path) -> None:
        assert (manuscript_dir / "config.yaml").exists()

    def test_config_valid_yaml(self, manuscript_dir: Path) -> None:
        with open(manuscript_dir / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)
        assert "paper" in data or "title" in data
        if "paper" in data:
            assert "title" in data["paper"]

    def test_config_has_authors(self, manuscript_dir: Path) -> None:
        with open(manuscript_dir / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "authors" in data or "author" in data

    def test_version_aligned_with_pyproject(self, project_root: Path, manuscript_dir: Path) -> None:
        """``config.yaml::paper.version`` must match ``pyproject.toml::project.version``."""
        try:
            import tomllib  # py311+
        except ImportError:  # pragma: no cover
            import tomli as tomllib  # type: ignore

        pyproj_text = (project_root / "pyproject.toml").read_text()
        pyproj = tomllib.loads(pyproj_text)
        cfg = yaml.safe_load((manuscript_dir / "config.yaml").read_text())
        py_version = pyproj["project"]["version"]
        cfg_version = cfg["paper"]["version"]
        assert py_version == cfg_version, (
            f"pyproject.toml version ({py_version}) does not match manuscript/config.yaml paper.version ({cfg_version})"
        )


class TestProjectConfigLoader:
    """Coverage for src.config — typed YAML loader."""

    def test_load_project_config_full_custom(self, tmp_path: Path) -> None:
        cfg = {
            "paper": {"title": "Aux"},
            "authors": [{"name": "N"}],
            "keywords": ["k"],
            "manuscript_dir": "manuscript",
            "prose": {
                "target_grade_level_min": 11.0,
                "target_grade_level_max": 21.5,
                "long_sentence_threshold": 40,
                "citation_density_min_per_1000": 2.5,
                "require_h1_per_section": False,
                "forbid_skipped_levels": False,
            },
            "bibliography": {
                "references_path": "custom_refs.bib",
                "fail_on_missing": False,
                "fail_on_unused": True,
            },
            "report": {
                "output_path": "out/md.md",
                "include_per_file_table": False,
                "include_outline": False,
                "include_quality_flags": False,
            },
        }
        path = tmp_path / "deep.yaml"
        path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
        from src.config import load_project_config

        parsed = load_project_config(path)
        assert parsed.title == "Aux"
        assert parsed.prose.target_grade_level_max == pytest.approx(21.5)
        assert parsed.bibliography.fail_on_unused is True
        assert parsed.report.include_outline is False

    def test_load_project_config_requires_mapping(self, tmp_path: Path) -> None:
        bad = tmp_path / "list.yaml"
        bad.write_text("- not: mapping\n", encoding="utf-8")
        from src.config import load_project_config

        with pytest.raises(ValueError, match="mapping"):
            load_project_config(bad)
