"""Pure orchestration of the crescent_city history pipeline.

Reads configuration, runs prose analysis, generates figures, cross-checks
citations, and writes the final review report.

All business logic is delegated to:
- :mod:`infrastructure.prose` (manuscript validation)
- :mod:`src.figures` (figure generation)
- :mod:`src.report` (report assembly)

Configuration is loaded from ``manuscript/config.yaml`` via
:class:`src.config.ProjectConfig`; no thresholds are hard-coded in this
module.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ── Add project + repo roots to path ────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parents[3]  # root of monorepo
_DEFAULT_PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_DEFAULT_PROJECT_DIR / "src"))
sys.path.insert(0, str(_DEFAULT_PROJECT_DIR))
sys.path.insert(0, str(_REPO_ROOT))

from infrastructure.prose.report import (  # noqa: E402
    ManuscriptReport,
    analyze_manuscript,
)

from src.checks import CheckResult  # noqa: E402
from src.config import ProjectConfig, load_project_config  # noqa: E402
from src.figures import generate_all_figures  # noqa: E402
from src.report import write_review_report  # noqa: E402

# ── Filesystem layout ──────────────────────────────────────────────────

PROJECT_DIR = _DEFAULT_PROJECT_DIR
MANUSCRIPT_DIR = PROJECT_DIR / "manuscript"
OUTPUT_DIR = PROJECT_DIR / "output"
CONFIG_PATH = MANUSCRIPT_DIR / "config.yaml"


def _display_path(path: Path, project_dir: Path) -> str:
    """Return a stable project-relative path when possible."""
    try:
        return str(path.relative_to(project_dir))
    except ValueError:
        return str(path)


def _resolve_project_dir(project_root: Path | str | None = None) -> Path:
    """Resolve the project root used by pipeline and CLI entry points."""
    return Path(project_root).expanduser().resolve() if project_root is not None else PROJECT_DIR


def _resolve_config_path(project_dir: Path, config_path: Path | str | None = None) -> Path:
    """Resolve an optional config path against the active project root."""
    if config_path is None:
        return project_dir / "manuscript" / "config.yaml"
    path = Path(config_path).expanduser()
    return path.resolve() if path.is_absolute() else (project_dir / path).resolve()


def _resolve_project_path(project_dir: Path, path: Path | str) -> Path:
    """Resolve *path* against *project_dir* unless it is already absolute."""
    p = Path(path).expanduser()
    return p.resolve() if p.is_absolute() else (project_dir / p).resolve()


def _load_config(config_path: Path | None = None) -> ProjectConfig:
    """Load :class:`ProjectConfig`.

    Defaults to ``manuscript/config.yaml`` adjacent to this project; tests can
    pass a custom path to drive failure scenarios without monkeypatching.
    """
    path = config_path or CONFIG_PATH
    if not path.exists():
        return ProjectConfig(title="Crescent City History")
    return load_project_config(path)


def _resolve_bib_path(cfg: ProjectConfig, project_dir: Path | None = None) -> Path:
    """Resolve the bibliography path; permit project-relative or repo-rooted."""
    root = project_dir or PROJECT_DIR
    bib_rel = Path(cfg.bibliography.references_path)
    if bib_rel.is_absolute() and bib_rel.exists():
        return bib_rel
    project_local = root / bib_rel
    if project_local.exists():
        return project_local
    # Fall back to repo root resolution
    return _REPO_ROOT / bib_rel


def _load_bib_keys(bib_path: Path) -> set[str]:
    """Extract all BibTeX keys from a ``.bib`` file."""
    if not bib_path.exists():
        return set()
    text = bib_path.read_text()
    return set(re.findall(r"@\w+\{(\w+)", text))


def _build_heading_checks(report: ManuscriptReport, cfg: ProjectConfig) -> list[CheckResult]:
    """Compute heading-structure checks from the analyzed report.

    These are *real* computed checks driven by
    :attr:`infrastructure.prose.report.StructureReport.has_h1` and
    :attr:`StructureReport.has_skipped_level` — not hard-coded literals.
    """
    checks: list[CheckResult] = []

    if cfg.prose.forbid_skipped_levels:
        skipped = [f.name for f in report.files if f.structure.has_skipped_level]
        checks.append(
            CheckResult(
                name="no_skipped_heading_levels",
                passed=not skipped,
                message=(
                    f"{len(skipped)} file(s) with skipped levels" + (f": {', '.join(skipped)}" if skipped else "")
                ),
            )
        )

    if cfg.prose.require_h1_per_section:
        missing = [f.name for f in report.files if not f.structure.has_h1]
        checks.append(
            CheckResult(
                name="every_file_has_h1",
                passed=not missing,
                message=(f"{len(missing)} file(s) missing H1" + (f": {', '.join(missing)}" if missing else "")),
            )
        )

    return checks


def _build_cross_reference_check(manuscript_dir: Path) -> CheckResult:
    """Verify every ``[@sec:X]`` citation has a matching ``{#sec:X}`` anchor."""
    cited: set[str] = set()
    defined: set[str] = set()
    for f in sorted(manuscript_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        cited.update(re.findall(r"\[@sec:([\w-]+)\]", text))
        defined.update(re.findall(r"\{#sec:([\w-]+)\}", text))
    missing = cited - defined
    return CheckResult(
        name="section_cross_references_resolve",
        passed=not missing,
        message=(
            f"{len(cited)} cited / {len(defined)} defined · "
            f"{len(missing)} missing" + (f": {', '.join(sorted(missing))}" if missing else "")
        ),
    )


def run_figures_only(
    *,
    project_root: Path | str | None = None,
    config_path: Path | str | None = None,
) -> int:
    """Generate figures without running prose or bibliography checks."""
    project_dir = _resolve_project_dir(project_root)
    cfg_path = _resolve_config_path(project_dir, config_path)
    cfg = _load_config(cfg_path)
    manuscript_dir = _resolve_project_path(project_dir, cfg.manuscript_dir)
    figures_dir = project_dir / "output" / "figures"
    data_dir = project_dir / "data"

    print("=" * 60)
    print("Crescent City History — Figure Generation")
    print("=" * 60)

    if not manuscript_dir.is_dir():
        print(f"❌  Manuscript directory not found: {manuscript_dir}")
        return 1

    try:
        pngs = generate_all_figures(manuscript_dir, figures_dir, data_dir=data_dir)
    except Exception as exc:  # noqa: BLE001 — surfaced as a CLI failure
        print(f"❌  Figure generation failed: {type(exc).__name__}: {exc}")
        return 1

    print(f"✅  Generated {len(pngs)} figure(s):")
    for p in pngs:
        print(f"   → {_display_path(Path(p), project_dir)}")
    return 0


def run_pipeline(
    strict: bool = False,
    config_path: Path | str | None = None,
    project_root: Path | str | None = None,
) -> int:
    """Execute the full pipeline. Returns 0 on success, 1 on failure.

    ``config_path`` overrides the default ``manuscript/config.yaml`` location;
    used by the test suite to drive failure scenarios without mocks.
    """
    project_dir = _resolve_project_dir(project_root)
    output_dir = project_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = _resolve_config_path(project_dir, config_path)
    cfg = _load_config(cfg_path)
    manuscript_dir = _resolve_project_path(project_dir, cfg.manuscript_dir)
    data_dir = project_dir / "data"

    pngs: list[str] = []
    figures_ok = True
    figures_error: str | None = None

    print("=" * 60)
    print("Crescent City History — Pipeline")
    print("=" * 60)

    # ── 1. Prose analysis ────────────────────────────────────────────
    report: ManuscriptReport = analyze_manuscript(manuscript_dir)
    manuscript_snapshot = output_dir / "manuscript_report.json"
    manuscript_snapshot.write_text(report.to_json() + "\n", encoding="utf-8")

    # ── 2. Run checks ────────────────────────────────────────────────
    checks: list[CheckResult] = []

    # Check: Grade level in band
    fkgl_min = cfg.prose.target_grade_level_min
    fkgl_max = cfg.prose.target_grade_level_max
    fkgl_ok = fkgl_min <= report.avg_flesch_kincaid_grade <= fkgl_max
    checks.append(
        CheckResult(
            "grade_level_in_band",
            fkgl_ok,
            f"avg FKGL = {report.avg_flesch_kincaid_grade:.2f} (target {fkgl_min}–{fkgl_max})",
        )
    )

    # Check: Citation density
    n_cites = len(report.citation_keys)
    n_words = max(report.total_words, 1)
    density = (n_cites / n_words) * 1000
    density_floor = cfg.prose.citation_density_min_per_1000
    density_ok = density >= density_floor
    checks.append(
        CheckResult(
            "citation_density_above_floor",
            density_ok,
            f"density = {density:.2f}/1000 words (min {density_floor})",
        )
    )

    # Checks: heading structure (real values, not hard-coded literals)
    checks.extend(_build_heading_checks(report, cfg))

    # Check: section cross-reference resolution
    checks.append(_build_cross_reference_check(manuscript_dir))

    # Check: Bibliography consistency
    bib_keys = _load_bib_keys(_resolve_bib_path(cfg, project_dir))
    cited = set(report.citation_keys)
    missing = cited - bib_keys
    reserved = set(cfg.bibliography.reserve_keys)
    unused = bib_keys - cited - reserved
    bib_msg = f"{len(cited)} cited / {len(bib_keys)} in bib · {len(missing)} missing · {len(unused)} unused" + (
        f" · {len(reserved)} reserved" if reserved else ""
    )
    bib_ok = True
    if cfg.bibliography.fail_on_missing:
        bib_ok = bib_ok and len(missing) == 0
    if cfg.bibliography.fail_on_unused:
        bib_ok = bib_ok and len(unused) == 0
    checks.append(CheckResult("bibliography_consistency", bib_ok, bib_msg))

    checks_total = len(checks)
    checks_passed = 0
    print()
    for c in checks:
        status = "✅" if c.passed else "❌"
        print(f"   {status} {c.name}")
        print(f"        {c.message}")
        if c.passed:
            checks_passed += 1

    # ── 3. Figures ───────────────────────────────────────────────────
    # Write figures into output/figures/ so they match the
    # `output/figures/...` paths referenced from manuscript image
    # blocks; running this pipeline alone is now sufficient to produce
    # a renderable manuscript without a separate
    # `y_generate_history_figures.py` invocation.
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    print()
    try:
        pngs = generate_all_figures(manuscript_dir, figures_dir, data_dir=data_dir)
        print(f"   📊  Generated {len(pngs)} figure(s):")
        for p in pngs:
            print(f"      → {_display_path(Path(p), project_dir)}")
    except Exception as exc:  # noqa: BLE001 — record + propagate via exit code
        figures_ok = False
        figures_error = f"{type(exc).__name__}: {exc}"
        print(f"   ❌  Figure generation failed: {figures_error}")

    # ── 4. Write report ──────────────────────────────────────────────
    print()
    report_path = output_dir / "pipeline_report.json"
    output_data = {
        "project": "crescent_city",
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "total_words": report.total_words,
        "unique_citations": n_cites,
        "avg_fkgl": round(report.avg_flesch_kincaid_grade, 2),
        "citation_density": round(density, 2),
        "figures_generated": len(pngs),
        "figures_ok": figures_ok,
        "figures_error": figures_error,
        "checks": {c.name: c.passed for c in checks},
    }
    report_path.write_text(json.dumps(output_data, indent=2) + "\n")
    print(f"   📝  Report written to {_display_path(report_path, project_dir)}")
    print(f"   📝  Manuscript prose snapshot written to {_display_path(manuscript_snapshot, project_dir)}")

    # ── 5. Write review markdown ─────────────────────────────────────
    review_path = _resolve_project_path(project_dir, cfg.report.output_path)
    write_review_report(
        review_path,
        title=f"{cfg.title} — Pipeline Review",
        manuscript_report=report,
        checks=checks,
        include_per_file_table=cfg.report.include_per_file_table,
        include_outline=cfg.report.include_outline,
        include_quality_flags=cfg.report.include_quality_flags,
        figures=[Path(p) for p in pngs] if figures_ok else None,
    )
    print(f"   📝  Review written to {_display_path(review_path, project_dir)}")

    # ── 6. Publishing artifacts ──────────────────────────────────────
    # CITATION.cff + zenodo_metadata.json + self_citation.bib, derived
    # purely from manuscript/config.yaml so the publication metadata
    # cannot drift from the manuscript header. Best-effort: a malformed
    # config.yaml is reported but does not fail the build.
    print()
    try:
        import yaml

        from src.publishing import write_publishing_artifacts

        with cfg_path.open(encoding="utf-8") as f:
            raw_cfg = yaml.safe_load(f) or {}
        artifacts = write_publishing_artifacts(raw_cfg, output_dir)
        for p in (artifacts.citation_cff, artifacts.zenodo_metadata, artifacts.bibtex):
            print(f"   📄  Publishing artifact: {_display_path(p, project_dir)}")
    except Exception as exc:  # noqa: BLE001 — informational only
        print(f"   ⚠️   Publishing artifacts skipped: {type(exc).__name__}: {exc}")

    print()
    print("-" * 60)
    print(f"Total words:        {report.total_words:,}")
    print(f"Unique citations:   {n_cites}")
    print(f"Avg FKGL:           {report.avg_flesch_kincaid_grade:.2f}")
    print(f"Citation density:   {density:.2f}/1000 words")
    print(f"Checks passed:      {checks_passed}/{checks_total}")
    print(f"Figures generated:  {len(pngs)}" + ("" if figures_ok else "  (FAILED)"))
    print("-" * 60)

    success = (checks_passed == checks_total) and figures_ok
    if not success and not strict:
        print("⚠️  Some checks failed. Run with --strict to exit non-zero.")
    return 0 if (success or not strict) else 1


if __name__ == "__main__":
    strict = "--strict" in sys.argv
    sys.exit(run_pipeline(strict=strict))
