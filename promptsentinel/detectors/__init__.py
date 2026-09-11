"""Detector registry."""

from promptsentinel.detectors.base import Detector, RawFinding
from promptsentinel.detectors.injection import INJECTION_DETECTORS
from promptsentinel.detectors.jailbreak import JAILBREAK_DETECTORS
from promptsentinel.detectors.pii import PII_DETECTORS
from promptsentinel.detectors.secrets import SECRET_DETECTORS

ALL_DETECTORS: list[Detector] = [
    *PII_DETECTORS,
    *SECRET_DETECTORS,
    *INJECTION_DETECTORS,
    *JAILBREAK_DETECTORS,
]

__all__ = ["ALL_DETECTORS", "Detector", "RawFinding"]
