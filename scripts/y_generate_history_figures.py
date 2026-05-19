#!/usr/bin/env python3
"""Thin orchestrator: generate every figure in the Crescent City suite.

All plotting logic lives in :mod:`src.figures` (which dispatches to
``src/_figures/``). This script wires the public API to a CLI:
no business logic; no per-figure branching; no figure-specific
arguments. Behavior is governed entirely by the registry inside
``src.figures.FIGURE_REGISTRY``.

Usage::

    PYTHONPATH=. uv run python projects/crescent_city/scripts/y_generate_history_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent  # projects/crescent_city
_repo_root = _project_root.parent.parent                # repository root
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_repo_root))


def main(argv: list[str] | None = None) -> int:
    from src.figures import generate_all_figures

    manuscript_dir = _project_root / "manuscript"
    if not manuscript_dir.is_dir():
        print("❌  manuscript/ not found beside scripts/.", file=sys.stderr)
        return 1

    figures = generate_all_figures(
        manuscript_dir,
        _project_root / "output" / "figures",
        data_dir=_project_root / "data",
    )
    print(f"✅  Generated {len(figures)} figure(s):")
    for f in figures:
        print(f"   → {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
