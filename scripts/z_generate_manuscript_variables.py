#!/usr/bin/env python3
"""Generate manuscript variables from the manuscript tree.

Analyzes prose (same aggregates as the history pipeline's prose stage),
substitutes ``{{TOKEN}}`` placeholders in manuscript markdown, and writes
resolved copies under ``output/manuscript/`` plus the canonical
``output/data/manuscript_variables.json`` payload used by the shared renderer.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
_repo_root = _project_root.parent.parent
sys.path.insert(0, str(_repo_root))
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "src"))


def main(argv: list[str] | None = None) -> int:
    from src.config import load_project_config
    from src.manuscript_variables import (
        compute_variables,
        write_variables,
    )
    from infrastructure.prose.report import analyze_manuscript

    project_root = Path(_project_root)
    config_path = project_root / "manuscript" / "config.yaml"
    cfg = load_project_config(config_path)

    manuscript_dir = project_root / cfg.manuscript_dir
    if not manuscript_dir.is_dir():
        print(f"❌  Manuscript directory not found: {manuscript_dir}")
        return 1

    report = analyze_manuscript(manuscript_dir)

    variables = compute_variables(report, config_title=cfg.title)
    variables_json = json.dumps(variables.to_dict(), indent=2, ensure_ascii=False) + "\n"
    variables_path = project_root / "output" / "data" / "manuscript_variables.json"
    variables_path.parent.mkdir(parents=True, exist_ok=True)
    variables_path.write_text(variables_json, encoding="utf-8")

    output_dir = project_root / "output"
    written = write_variables(variables, manuscript_dir, output_dir)

    print(f"✅  Wrote {len(written)} substituted files to {output_dir / 'manuscript'}")
    print(f"📦  Variables saved to {variables_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
