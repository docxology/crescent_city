"""Documentation integrity tests for project-facing Markdown links."""

from __future__ import annotations

import re
from pathlib import Path


_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_DOC_DIRS = ("data", "docs", "manuscript", "scripts", "src", "src/_figures", "tests")
_CANONICAL_AUDIT_DOCS = (
    "accessibility_reader_experience.md",
    "audit_trail_limitations.md",
    "current_events_refresh.md",
    "data_validation_qa.md",
    "environment_reproducibility.md",
    "release_archival_versioning.md",
    "source_to_claim_audit.md",
    "sources_provenance_ethics.md",
    "visual_pdf_qa.md",
)


def _project_docs(project_root: Path) -> list[Path]:
    docs = [project_root / "README.md", project_root / "AGENTS.md", project_root / "manuscript" / "SYNTAX.md"]
    docs.extend(sorted((project_root / "docs").glob("*.md")))
    for dirname in _DOC_DIRS:
        docs.extend([project_root / dirname / "README.md", project_root / dirname / "AGENTS.md"])
    return sorted(set(docs))


def _local_markdown_links(path: Path) -> list[Path]:
    links: list[Path] = []
    for raw in _LINK_RE.findall(path.read_text(encoding="utf-8")):
        target = raw.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        links.append((path.parent / target).resolve())
    return links


def test_project_docs_links_resolve(project_root: Path) -> None:
    """README / AGENTS / docs Markdown links should not point at vanished files."""
    missing: list[str] = []
    for doc in _project_docs(project_root):
        for target in _local_markdown_links(doc):
            if not target.exists():
                missing.append(f"{doc.relative_to(project_root)} -> {target}")
    assert not missing, "Broken local documentation links:\n" + "\n".join(missing)


def test_folder_level_docs_exist(project_root: Path) -> None:
    """Every authored source directory should have local public and agent docs."""
    missing = []
    for dirname in _DOC_DIRS:
        for filename in ("README.md", "AGENTS.md"):
            path = project_root / dirname / filename
            if not path.exists():
                missing.append(str(path.relative_to(project_root)))
    assert not missing, "Missing folder-level documentation:\n" + "\n".join(missing)


def test_canonical_audit_docs_are_discoverable(project_root: Path) -> None:
    """Auditability docs should exist and be linked from both docs entry points."""
    docs_dir = project_root / "docs"
    missing = [name for name in _CANONICAL_AUDIT_DOCS if not (docs_dir / name).exists()]
    assert not missing, "Missing canonical audit docs: " + ", ".join(missing)

    for hub_name in ("README.md", "index.md"):
        hub = docs_dir / hub_name
        hub_links = set(_local_markdown_links(hub))
        unlinked = [name for name in _CANONICAL_AUDIT_DOCS if (docs_dir / name).resolve() not in hub_links]
        assert not unlinked, f"docs/{hub_name} does not link: " + ", ".join(unlinked)


def _current_event_source_tiers(project_root: Path) -> set[str]:
    data_test = (project_root / "tests" / "test_data.py").read_text(encoding="utf-8")
    match = re.search(r"CURRENT_EVENT_SOURCE_TIERS\s*=\s*\{(?P<body>.*?)\}", data_test, re.DOTALL)
    assert match, "CURRENT_EVENT_SOURCE_TIERS block not found"
    return set(re.findall(r'"([^"]+)"', match.group("body")))


def test_source_tier_docs_match_data_guard(project_root: Path) -> None:
    """Docs should use the exact source-tier labels enforced by data tests."""
    tiers = _current_event_source_tiers(project_root)
    docs_to_check = (
        project_root / "docs" / "sources_provenance_ethics.md",
        project_root / "docs" / "claim_ledger.md",
        project_root / "docs" / "data_validation_qa.md",
    )
    missing: list[str] = []
    for doc in docs_to_check:
        text = doc.read_text(encoding="utf-8")
        for tier in tiers:
            if f"`{tier}`" not in text:
                missing.append(f"{doc.relative_to(project_root)} omits `{tier}`")
    assert not missing, "Source-tier documentation drift:\n" + "\n".join(missing)

    combined = "\n".join(doc.read_text(encoding="utf-8") for doc in _project_docs(project_root))
    stale_tier_labels = ("`official_plus_local`", "`local_journalism`", "`tribal_press_republished`")
    stale = [label for label in stale_tier_labels if label in combined]
    assert not stale, "Stale source-tier labels remain: " + ", ".join(stale)


def test_project_docs_match_current_figure_registry(project_root: Path) -> None:
    """Project docs should name the current figure suite, not an older count."""
    from src.figures import FIGURE_REGISTRY

    count = len(FIGURE_REGISTRY)
    text_by_doc = {
        doc.relative_to(project_root).as_posix(): doc.read_text(encoding="utf-8") for doc in _project_docs(project_root)
    }
    combined = "\n".join(text_by_doc.values())
    previous_figure_count = "18"
    previous_figure_word = "eighteen"

    stale_patterns = (
        r"\b17 reproducible figures\b",
        r"\b17 figures\b",
        r"\b17-figure\b",
        r"\b306-entry\b",
        r"\b321 BibTeX\b",
        r"\b355 BibTeX entries\b",
        r"\b355-entry BibTeX\b",
        r"\b319 unique cited keys\b",
        r"\b49 narrative chapters\b",
        r"\beight thematic Parts\b",
        r"\b58_reproducibility\.md\b",
        r"\bfigures_generated >= 17\b",
        rf"\bfigures_generated >= {previous_figure_count}\b",
        rf"\b{previous_figure_count} reproducible figures\b",
        rf"\b{previous_figure_count} figures\b",
        rf"\b{previous_figure_word} figures\b",
        rf"\b{previous_figure_count}-figure\b",
        rf"\b{previous_figure_count} PNG\b",
        rf"\bregistered {previous_figure_count}\b",
        r"\b200\+ cited keys\b",
        r"Every file must have an H1",
        r"`require_h1_per_section`\s*\|\s*`true`",
    )
    stale = [pattern for pattern in stale_patterns if re.search(pattern, combined)]
    assert not stale, "Stale project-documentation facts remain: " + ", ".join(stale)

    readme = text_by_doc["README.md"]
    assert f"Figures ({count})" in readme
    for spec in FIGURE_REGISTRY:
        assert f"`{spec.plotter.__name__}`" in readme, f"README omits {spec.plotter.__name__}"


def test_project_docs_match_current_manuscript_shape(project_root: Path) -> None:
    """README / AGENTS / overview should describe the Space-Time-People-Ideas manuscript."""
    readme = (project_root / "README.md").read_text(encoding="utf-8")
    agents = (project_root / "AGENTS.md").read_text(encoding="utf-8")
    overview = (project_root / "docs" / "project_overview.md").read_text(encoding="utf-8")

    for title in ("Part I — Space", "Part II — Time", "Part III — People", "Part IV — Ideas"):
        assert title in readme
    assert "00_abstract → 73_reproducibility.md" in agents
    assert "`require_h1_per_section` | `false`" in readme
    assert "Directory-Level Documentation" in readme
    assert "58 analyzed Markdown source files" in overview
    assert "cited-key, reserve-key, and unused-entry counts are reported by each pipeline run" in overview
    assert "docs/claim_ledger.md" in overview
    assert "claim-ledger and source-refresh workflow" in readme
    assert "Reserve Bibliography Audit" in (project_root / "docs" / "claim_ledger.md").read_text(encoding="utf-8")
    assert "folder-level README/AGENTS" in overview


def test_source_to_claim_audit_covers_every_manuscript_file(project_root: Path) -> None:
    """The claim-fit audit should name every manuscript source file."""
    audit = (project_root / "docs" / "source_to_claim_audit.md").read_text(encoding="utf-8")
    support_files = {"AGENTS.md", "README.md", "SYNTAX.md", "preamble.md"}
    missing = [
        path.name
        for path in sorted((project_root / "manuscript").glob("*.md"))
        if path.name not in support_files and path.name not in audit
    ]
    assert not missing, "source_to_claim_audit.md omits manuscript files: " + ", ".join(missing)
