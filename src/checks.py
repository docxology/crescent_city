"""Shared validation-check record for the Crescent City pipeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckResult:
    """Outcome of one pipeline quality gate."""

    name: str
    passed: bool
    message: str
