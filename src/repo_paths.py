"""Monorepo-root resolution for the relocated sidecar layout.

``crescent_city`` imports ``infrastructure.*`` from the template monorepo
checkout. Historically the monorepo root was hard-coded as a fixed number
of ``parents`` above this file, which breaks when the project is checked
out in the standalone sidecar repo (``<projects-root>/ongoing/<Group>/
<name>``) while the template lives in a sibling checkout.

Resolution order (first match wins):

1. ``TEMPLATE_REPO_ROOT`` environment variable, when it points at a
   directory containing ``infrastructure/``.
2. The nearest ancestor of ``start`` containing ``infrastructure/__init__.py``
   (the classic in-monorepo layout, including symlinked mirrors).
3. A sibling directory named ``template`` next to any ancestor of
   ``start`` (the sidecar convention: ``<root>/projects/...`` next to
   ``<root>/template``).

Raises :class:`RuntimeError` with actionable guidance when nothing matches.
"""

from __future__ import annotations

import os
from pathlib import Path

_MARKERS = ("infrastructure", "__init__.py")
_ENV_VAR = "TEMPLATE_REPO_ROOT"


def _is_repo_root(candidate: Path) -> bool:
    return (candidate / _MARKERS[0] / _MARKERS[1]).is_file()


def find_repo_root(start: Path) -> Path:
    """Return the template monorepo root that provides ``infrastructure``."""
    env_value = os.environ.get(_ENV_VAR)
    if env_value:
        env_root = Path(env_value).expanduser().resolve()
        if _is_repo_root(env_root):
            return env_root

    seen: set[Path] = set()
    for ancestor in (start.resolve(), *start.resolve().parents):
        if ancestor in seen:
            continue
        seen.add(ancestor)
        if _is_repo_root(ancestor):
            return ancestor
        sibling = ancestor.parent / "template"
        if _is_repo_root(sibling):
            return sibling

    raise RuntimeError(
        "Cannot locate the template monorepo root providing "
        "'infrastructure/'. Set the TEMPLATE_REPO_ROOT environment "
        "variable to the template checkout path, or run from a checkout "
        "where the template repo is an ancestor or sibling ('template') "
        "of the project directory."
    )
