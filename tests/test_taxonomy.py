"""Tests for the threat taxonomy module."""

from __future__ import annotations

from models.threat_taxonomy import get_threat_info, risk_score
from promptsentinel.detectors import ALL_DETECTORS


def test_all_detectors_mapped_in_taxonomy():
    """Verify every registered detector in ALL_DETECTORS has a valid taxonomy entry."""
    for detector in ALL_DETECTORS:
        info = get_threat_info(detector.name)
        assert "owasp" in info, f"Missing OWASP mapping for {detector.name}"
        assert "name" in info, f"Missing threat name for {detector.name}"
        assert "mitre_atlas" in info, f"Missing MITRE ATLAS mapping for {detector.name}"
        assert info["owasp"].startswith("LLM"), f"Invalid OWASP ID for {detector.name}"
        assert info["mitre_atlas"].startswith("AML."), f"Invalid MITRE ATLAS ID for {detector.name}"


def test_get_threat_info_unknown_detector():
    """Verify fallback for unmapped or custom detector."""
    info = get_threat_info("unknown.detector")
    assert info["owasp"] == "LLM06"
    assert info["mitre_atlas"] == "AML.T0024"


def test_risk_score_empty():
    assert risk_score([]) == 0


def test_risk_score_calculation():
    findings = [
        {"severity": "LOW"},
        {"severity": "MEDIUM"},
    ]
    assert risk_score(findings) == 50


def test_risk_score_capped_at_100():
    findings = [
        {"severity": "CRITICAL"},
        {"severity": "HIGH"},
    ]
    assert risk_score(findings) == 100
