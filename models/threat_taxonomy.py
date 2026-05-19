"""
PromptSentinel threat taxonomy — maps detectors to OWASP LLM Top 10 and MITRE ATLAS.

References:
  OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  MITRE ATLAS:       https://atlas.mitre.org/
"""

from __future__ import annotations

OWASP_MAPPING: dict[str, dict[str, str]] = {
    "injection.override": {
        "owasp": "LLM01",
        "name": "Prompt Injection",
        "mitre_atlas": "AML.T0051",
        "description": "Direct instruction override attempt",
    },
    "injection.role_hijack": {
        "owasp": "LLM01",
        "name": "Prompt Injection",
        "mitre_atlas": "AML.T0051",
        "description": "Role/persona hijack via prompt manipulation",
    },
    "jailbreak.known_pattern": {
        "owasp": "LLM01",
        "name": "Prompt Injection",
        "mitre_atlas": "AML.T0054",
        "description": "Known jailbreak pattern (DAN, STAN, AIM, developer-mode)",
    },
    "pii.ssn": {
        "owasp": "LLM06",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "US Social Security Number in prompt",
    },
    "pii.credit_card": {
        "owasp": "LLM06",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Credit card number in prompt",
    },
    "pii.email": {
        "owasp": "LLM06",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Email address in prompt",
    },
    "secrets.aws_access_key": {
        "owasp": "LLM06",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "AWS access key ID leaked in prompt",
    },
    "secrets.openai_key": {
        "owasp": "LLM06",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "OpenAI API key leaked in prompt",
    },
}


SEVERITY_WEIGHTS: dict[str, int] = {
    "CRITICAL": 100,
    "HIGH": 75,
    "MEDIUM": 40,
    "LOW": 10,
}


def risk_score(findings: list[dict]) -> int:
    """Compute a composite 0-100 risk score from a list of findings."""
    if not findings:
        return 0
    total = sum(SEVERITY_WEIGHTS.get(f.get("severity", "LOW"), 10) for f in findings)
    return min(100, total)
