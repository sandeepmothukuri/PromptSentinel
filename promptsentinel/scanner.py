"""Core scanner orchestration."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, field
from enum import IntEnum

from promptsentinel.detectors import ALL_DETECTORS, Detector

_RISK_WEIGHTS = {
    "LOW": 10,
    "MEDIUM": 40,
    "HIGH": 75,
    "CRITICAL": 100,
}


class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def parse(cls, value: str | int | Severity) -> Severity:
        if isinstance(value, Severity):
            return value
        if isinstance(value, int):
            return cls(value)
        return cls[value.strip().upper()]

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Finding:
    detector: str
    severity: Severity
    match: str
    start: int
    end: int
    line: int
    column: int
    message: str = ""

    def to_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["severity"] = self.severity.name
        return d


@dataclass
class Report:
    text: str
    findings: list[Finding] = field(default_factory=list)

    def has_findings(self, min_severity: str | Severity = Severity.LOW) -> bool:
        threshold = Severity.parse(min_severity)
        return any(f.severity >= threshold for f in self.findings)

    def filter(self, min_severity: str | Severity = Severity.LOW) -> list[Finding]:
        threshold = Severity.parse(min_severity)
        return [f for f in self.findings if f.severity >= threshold]

    def summary(self) -> str:
        if not self.findings:
            return "no findings"
        counts: dict[str, int] = {}
        for f in self.findings:
            counts[f.severity.name] = counts.get(f.severity.name, 0) + 1
        parts = [f"{n} {s}" for s, n in counts.items()]
        return ", ".join(parts)

    @property
    def risk_score(self) -> int:
        if not self.findings:
            return 0
        total = sum(_RISK_WEIGHTS[f.severity.name] for f in self.findings)
        return min(100, total)

    def to_dict(self) -> dict[str, object]:
        return {
            "risk_score": self.risk_score,
            "summary": self.summary(),
            "count": len(self.findings),
            "findings": [f.to_dict() for f in self.findings],
        }


def _line_col(text: str, offset: int) -> tuple[int, int]:
    prefix = text[:offset]
    line = prefix.count("\n") + 1
    last_nl = prefix.rfind("\n")
    col = offset - last_nl if last_nl >= 0 else offset + 1
    return line, col


class Scanner:
    """Run a configurable set of detectors over text."""

    def __init__(
        self,
        detectors: Sequence[Detector] | None = None,
        disabled: Iterable[str] = (),
    ) -> None:
        chosen = list(detectors) if detectors is not None else list(ALL_DETECTORS)
        disabled_set = {d.strip() for d in disabled if d.strip()}
        self.detectors: list[Detector] = [d for d in chosen if d.name not in disabled_set]

    def scan(self, text: str) -> Report:
        report = Report(text=text)
        if not text:
            return report
        seen: set[tuple[str, int, int]] = set()
        for detector in self.detectors:
            for raw in detector.detect(text):
                key = (detector.name, raw.start, raw.end)
                if key in seen:
                    continue
                seen.add(key)
                line, col = _line_col(text, raw.start)
                report.findings.append(
                    Finding(
                        detector=detector.name,
                        severity=Severity(raw.severity),
                        match=raw.match,
                        start=raw.start,
                        end=raw.end,
                        line=line,
                        column=col,
                        message=raw.message,
                    )
                )
        report.findings.sort(key=lambda f: (-f.severity, f.start))
        return report
