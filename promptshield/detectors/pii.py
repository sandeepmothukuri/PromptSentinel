"""PII detectors."""
from __future__ import annotations

import re
from collections.abc import Iterable

from promptshield.detectors.base import Detector, RawFinding, RegexDetector

EMAIL_RE = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_RE = r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}(?!\d)"
SSN_RE = r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"
IPV4_RE = r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b"
IPV6_RE = r"\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b"
IBAN_RE = r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b"
PASSPORT_RE = r"\b[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]\b"


def _luhn_ok(digits: str) -> bool:
    s = 0
    for i, ch in enumerate(reversed(digits)):
        d = ord(ch) - 48
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s % 10 == 0


class CreditCardDetector(Detector):
    name = "pii.credit_card"
    severity = 3  # HIGH
    message = "Credit card number detected"

    _pattern = re.compile(r"\b(?:\d[ -]?){13,19}\b")

    def detect(self, text: str) -> Iterable[RawFinding]:
        for m in self._pattern.finditer(text):
            digits = re.sub(r"\D", "", m.group(0))
            if 13 <= len(digits) <= 19 and _luhn_ok(digits):
                yield RawFinding(
                    match=m.group(0),
                    start=m.start(),
                    end=m.end(),
                    severity=self.severity,
                    message=self.message,
                )


PII_DETECTORS: list[Detector] = [
    RegexDetector("pii.email", [EMAIL_RE], severity=2, message="Email address"),
    RegexDetector("pii.phone", [PHONE_RE], severity=2, message="Phone number"),
    RegexDetector("pii.ssn", [SSN_RE], severity=4, message="US Social Security Number"),
    RegexDetector("pii.ipv4", [IPV4_RE], severity=1, message="IPv4 address"),
    RegexDetector("pii.ipv6", [IPV6_RE], severity=1, message="IPv6 address"),
    RegexDetector("pii.iban", [IBAN_RE], severity=3, message="IBAN bank account"),
    RegexDetector("pii.passport", [PASSPORT_RE], severity=3, message="Passport-like ID"),
    CreditCardDetector(),
]
