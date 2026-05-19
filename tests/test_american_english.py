"""American-English style guard for authored project text."""

from __future__ import annotations

import re
from pathlib import Path


_TEXT_SUFFIXES = {".bib", ".csv", ".json", ".md", ".py", ".toml", ".yaml", ".yml"}

_ROOTS = (
    "AGENTS.md",
    "CHANGELOG.md",
    "README.md",
    "data",
    "docs",
    "manuscript",
    "scripts",
    "src",
    "tests",
)

_SKIP_RELATIVE = {
    "tests/test_american_english.py",
}

_ALLOWED_LINE_SNIPPETS = (
    "A1_figure_catalogue.md",
    "figure_catalogue",
    "UNESCO World Heritage Centre",
    "Burnt Ranch",
    "Pacific smelt",
)

_BRITISH_SPELLING_PATTERNS = [
    r"\banalysed\b",
    r"\banalyse\b",
    r"\barmoured\b",
    r"\bauthorised\b",
    r"\bauthorisation\b",
    r"\bbehaviour(?:al)?\b",
    r"\bcatalogu(?:e|ed|ing|es)\b",
    r"\bcanonisation\b",
    r"\bcanonised\b",
    r"\bcentr(?:e|ed|es)\b",
    r"\bcharacterised\b",
    r"\bcharacterise\b",
    r"\bcatalysed\b",
    r"\bcolour(?:s|ed|ing)?\b",
    r"\bcustomised\b",
    r"\bdefence\b",
    r"\bdigitised\b",
    r"\bemphasis(?:e|ed|es|ing)\b",
    r"\benrolment\b",
    r"\bfavour(?:able|ed|ing)?\b",
    r"\bformalised\b",
    r"\bformalising\b",
    r"\bfulfil\b",
    r"\bgrey\b",
    r"\bharbours?\b",
    r"\bhonour\b",
    r"\binitialis(?:e|ed|es|ing|ation|ations)\b",
    r"\bjudgement\b",
    r"\bkilometres?\b",
    r"\blabell(?:ed|ing)\b",
    r"\blabour(?:ed|er|ers|ing)?\b",
    r"\bleapt\b",
    r"\blicence\b",
    r"\bmillimetres?\b",
    r"\bmodelling\b",
    r"\bmodelled\b",
    r"\bmould(?:s|ed|ing)?\b",
    r"\bneighbour(?:s|ed|ing|hood|hoods)?\b",
    r"\bnormalise\b",
    r"\bnon-naturalisation\b",
    r"\borganis(?:e|ed|es|ing|ation|ations|ational)\b",
    r"\bpractise(?:d|s)?\b",
    r"\bprogramme(?:s)?\b",
    r"\brecognis(?:e|ed|es|ing)\b",
    r"\brecognisabl(?:e|y)\b",
    r"\brecolonise\b",
    r"\brecoloured\b",
    r"\brevitalisation\b",
    r"\brumours\b",
    r"\bsceptic(?:al)?\b",
    r"\bspecialisation(?:s)?\b",
    r"\bspecialised\b",
    r"\bsubsidis(?:e|ed|es|ing)\b",
    r"\bstabilisation\b",
    r"\bstylised\b",
    r"\bsynthes(?:ise|ises|ised|ising)\b",
    r"\bsummaris(?:e|ed|es|ing)\b",
    r"\btheatre\b",
    r"\btonnes?\b",
    r"\btowards\b",
    r"\btravellers?\b",
    r"\butilis(?:e|ed|es|ing|ation)\b",
    r"\banglicised\b",
    r"\bcentralising\b",
    r"\bcolonised\b",
    r"\bcontextualises\b",
    r"\bcrystallised\b",
    r"\bdemobilisation\b",
    r"\bevangelisation\b",
    r"\bfinalised\b",
    r"\bimmunisation\b",
    r"\blegalis(?:e|ed|es|ing|ation)\b",
    r"\blocalised\b",
    r"\bmarginalised\b",
    r"\bmechanisation\b",
    r"\bminimise\b",
    r"\bmobilised\b",
    r"\bnationalised\b",
    r"\bparameterised\b",
    r"\bpopularis(?:e|ed|es|ing|ation)\b",
    r"\bpulverised\b",
    r"\bsymbolising\b",
    r"\btantalised\b",
    r"\bunionised\b",
    r"\bwood-fuelled\b",
]

_BRITISH_RE = re.compile("|".join(_BRITISH_SPELLING_PATTERNS), re.IGNORECASE)


def _iter_authored_files(project_root: Path) -> list[Path]:
    files: list[Path] = []
    for root_name in _ROOTS:
        root = project_root / root_name
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(p for p in root.rglob("*") if p.is_file() and p.suffix in _TEXT_SUFFIXES)
    return sorted(files)


def test_authored_text_uses_american_english(project_root: Path) -> None:
    findings: list[str] = []

    for path in _iter_authored_files(project_root):
        rel = path.relative_to(project_root)
        if rel.as_posix() in _SKIP_RELATIVE:
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(snippet in line for snippet in _ALLOWED_LINE_SNIPPETS):
                continue
            if match := _BRITISH_RE.search(line):
                findings.append(f"{rel}:{line_no}: {match.group(0)!r}")

    assert not findings, "British spellings remain:\n" + "\n".join(findings[:50])
