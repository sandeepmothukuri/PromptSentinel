"""Detector base classes."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from re import Pattern


@dataclass(frozen=True)
class RawFinding:
    match: str
    start: int
    end: int
    severity: int
    message: str = ""


class Detector:
    name: str = "detector"

    def detect(self, text: str) -> Iterable[RawFinding]:  # pragma: no cover - abstract
        raise NotImplementedError


class RegexDetector(Detector):
    """Detector backed by one or more compiled regexes."""

    def __init__(
        self,
        name: str,
        patterns: Sequence[str | Pattern[str]],
        severity: int,
        message: str = "",
        flags: int = re.IGNORECASE,
    ) -> None:
        self.name = name
        self.severity = severity
        self.message = message
        self._patterns: list[Pattern[str]] = [
            p if isinstance(p, re.Pattern) else re.compile(p, flags) for p in patterns
        ]

    def detect(self, text: str) -> Iterable[RawFinding]:
        for pattern in self._patterns:
            for m in pattern.finditer(text):
                yield RawFinding(
                    match=m.group(0),
                    start=m.start(),
                    end=m.end(),
                    severity=self.severity,
                    message=self.message,
                )
