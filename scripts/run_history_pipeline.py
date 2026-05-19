#!/usr/bin/env python3
"""Thin orchestrator: coordinate the Crescent City history pipeline.

All logic lives in :mod:`src.pipeline`, :mod:`src.figures`, and
:mod:`src.report`. This script wires them together and handles CLI
arguments.

Usage::

    # Run full pipeline
    uv run python scripts/run_history_pipeline.py

    # Strict mode (exit non-zero on any check failure)
    uv run python scripts/run_history_pipeline.py --strict

    # Alternate project root / config
    uv run python scripts/run_history_pipeline.py --project-root /tmp/crescent_copy --config manuscript/config.yaml

    # List available steps
    uv run python scripts/run_history_pipeline.py --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ── Resolve project and repo roots ──────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_DIR = _SCRIPT_DIR.parent  # projects/crescent_city
_REPO_ROOT = _PROJECT_DIR.parent.parent  # repository root

sys.path.insert(0, str(_PROJECT_DIR / "src"))
sys.path.insert(0, str(_PROJECT_DIR))
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Crescent City history pipeline — manuscript analysis, figures, and validation."
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any pipeline check fails.")
    parser.add_argument("--list", action="store_true", help="Print available pipeline steps and exit.")
    parser.add_argument("--figures-only", action="store_true", help="Only generate figures, skip prose analysis.")
    parser.add_argument("--config", type=Path, default=None, help="Project-relative or absolute config YAML path.")
    parser.add_argument("--project-root", type=Path, default=None, help="Project root to analyze; defaults beside script.")
    args = parser.parse_args()

    if args.list:
        from src.figures import FIGURE_REGISTRY

        print("Pipeline steps:")
        print("  1. Prose analysis (readability, citations, structure)")
        print("  2. Validation checks (5 checks against config)")
        print(f"  3. Figure generation ({len(FIGURE_REGISTRY)} figures from manuscript + data)")
        print("  4. Report assembly (JSON + summary)")
        return 0

    # Import and run
    from src.pipeline import run_figures_only, run_pipeline

    if args.figures_only:
        return run_figures_only(project_root=args.project_root, config_path=args.config)
    return run_pipeline(strict=args.strict, config_path=args.config, project_root=args.project_root)


if __name__ == "__main__":
    sys.exit(main())
