"""
PromptSentinel threat taxonomy — maps detectors to OWASP LLM Top 10 and MITRE ATLAS.

References:
  OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  MITRE ATLAS:       https://atlas.mitre.org/
"""

from __future__ import annotations

OWASP_MAPPING: dict[str, dict[str, str]] = {
    # Direct & Indirect Prompt Injection (OWASP LLM01)
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
    # Sensitive Information Disclosure: PII (OWASP LLM02)
    "pii.email": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Email address in prompt",
    },
    "pii.phone": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Telephone number in prompt",
    },
    "pii.ssn": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "US Social Security Number in prompt",
    },
    "pii.ipv4": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "IPv4 address in prompt",
    },
    "pii.ipv6": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "IPv6 address in prompt",
    },
    "pii.iban": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "International Bank Account Number (IBAN) in prompt",
    },
    "pii.passport": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Passport number in prompt",
    },
    "pii.credit_card": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Credit card number in prompt",
    },
    # Sensitive Information Disclosure: Secrets & API Keys (OWASP LLM02)
    "secrets.aws_access_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "AWS access key ID leaked in prompt",
    },
    "secrets.aws_secret_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "AWS secret access key leaked in prompt",
    },
    "secrets.github_token": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "GitHub personal access token leaked in prompt",
    },
    "secrets.openai_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "OpenAI API key leaked in prompt",
    },
    "secrets.anthropic_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Anthropic API key leaked in prompt",
    },
    "secrets.google_api_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Google API key leaked in prompt",
    },
    "secrets.slack_token": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Slack API token leaked in prompt",
    },
    "secrets.stripe_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Stripe API key leaked in prompt",
    },
    "secrets.jwt": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "JSON Web Token (JWT) leaked in prompt",
    },
    "secrets.private_key": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "Private key block leaked in prompt",
    },
    "secrets.generic_high_entropy": {
        "owasp": "LLM02",
        "name": "Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024",
        "description": "High-entropy secret string near credential keywords",
    },
}


def get_threat_info(detector_name: str) -> dict[str, str]:
    """Retrieve taxonomy classification for a given detector name."""
    return OWASP_MAPPING.get(
        detector_name,
        {
            "owasp": "LLM02",
            "name": "Sensitive Information Disclosure",
            "mitre_atlas": "AML.T0024",
            "description": "Unclassified security finding",
        },
    )


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
