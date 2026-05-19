"""Detector registry."""
from promptshield.detectors.base import Detector, RawFinding
from promptshield.detectors.injection import INJECTION_DETECTORS
from promptshield.detectors.jailbreak import JAILBREAK_DETECTORS
from promptshield.detectors.pii import PII_DETECTORS
from promptshield.detectors.secrets import SECRET_DETECTORS

ALL_DETECTORS: list[Detector] = [
    *PII_DETECTORS,
    *SECRET_DETECTORS,
    *INJECTION_DETECTORS,
    *JAILBREAK_DETECTORS,
]

__all__ = ["ALL_DETECTORS", "Detector", "RawFinding"]
