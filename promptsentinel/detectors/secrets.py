"""Secret / API key detectors."""

from __future__ import annotations

import math
import re
from collections.abc import Iterable

from promptsentinel.detectors.base import Detector, RawFinding, RegexDetector

SECRET_DETECTORS: list[Detector] = [
    RegexDetector(
        "secrets.aws_access_key",
        [r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASCA)[0-9A-Z]{16}\b"],
        severity=4,
        message="AWS access key ID",
        flags=0,
    ),
    RegexDetector(
        "secrets.aws_secret_key",
        [r"(?i)aws(.{0,20})?(secret|sk)[^\n]{0,5}['\"][0-9a-zA-Z/+]{40}['\"]"],
        severity=4,
        message="AWS secret access key",
    ),
    RegexDetector(
        "secrets.github_token",
        [
            r"\bghp_[A-Za-z0-9]{36}\b",
            r"\bgho_[A-Za-z0-9]{36}\b",
            r"\bghu_[A-Za-z0-9]{36}\b",
            r"\bghs_[A-Za-z0-9]{36}\b",
            r"\bghr_[A-Za-z0-9]{36}\b",
            r"\bgithub_pat_[A-Za-z0-9_]{82}\b",
        ],
        severity=4,
        message="GitHub token",
        flags=0,
    ),
    RegexDetector(
        "secrets.openai_key",
        [r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"],
        severity=4,
        message="OpenAI API key",
        flags=0,
    ),
    RegexDetector(
        "secrets.anthropic_key",
        [r"\bsk-ant-[A-Za-z0-9_-]{30,}\b"],
        severity=4,
        message="Anthropic API key",
        flags=0,
    ),
    RegexDetector(
        "secrets.google_api_key",
        [r"\bAIza[0-9A-Za-z_-]{35}\b"],
        severity=4,
        message="Google API key",
        flags=0,
    ),
    RegexDetector(
        "secrets.slack_token",
        [r"\bxox[abpsr]-[A-Za-z0-9-]{10,}\b"],
        severity=4,
        message="Slack token",
        flags=0,
    ),
    RegexDetector(
        "secrets.stripe_key",
        [r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{24,}\b"],
        severity=4,
        message="Stripe API key",
        flags=0,
    ),
    RegexDetector(
        "secrets.jwt",
        [r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"],
        severity=3,
        message="JSON Web Token",
        flags=0,
    ),
    RegexDetector(
        "secrets.private_key",
        [r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"],
        severity=4,
        message="Private key block",
        flags=0,
    ),
]


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq: dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


class GenericHighEntropyDetector(Detector):
    """Detect long high-entropy strings near secret-y keywords."""

    name = "secrets.generic_high_entropy"
    severity = 2  # MEDIUM
    message = "Possible secret (high-entropy string)"

    _candidate = re.compile(
        r"(?i)(?:secret|token|api[_-]?key|password|passwd|pwd|auth)[\"'\s:=]{1,5}([A-Za-z0-9_\-+/=]{20,})"
    )

    def detect(self, text: str) -> Iterable[RawFinding]:
        for m in self._candidate.finditer(text):
            candidate = m.group(1)
            if _shannon_entropy(candidate) >= 3.5:
                yield RawFinding(
                    match=candidate,
                    start=m.start(1),
                    end=m.end(1),
                    severity=self.severity,
                    message=self.message,
                )


SECRET_DETECTORS.append(GenericHighEntropyDetector())
