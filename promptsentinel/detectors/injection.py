"""Prompt-injection detectors."""

from __future__ import annotations

from promptsentinel.detectors.base import Detector, RegexDetector

_PATTERNS_HIGH = [
    r"ignore\s+(?:all\s+|the\s+|your\s+|previous\s+|prior\s+|above\s+|earlier\s+)*(?:instructions?|prompts?|rules?|directives?|guidelines?)",
    r"disregard\s+(?:all\s+|the\s+|your\s+|previous\s+|prior\s+|above\s+)*(?:instructions?|prompts?|rules?)",
    r"forget\s+(?:everything|all|the\s+(?:above|previous)|your\s+(?:instructions?|rules?|prompt))",
    r"(?:override|bypass|circumvent)\s+(?:your\s+|the\s+)?(?:instructions?|rules?|safety|guardrails?|filters?)",
    r"you\s+are\s+(?:now\s+)?(?:no\s+longer|not)\s+(?:bound|restricted|limited)\s+by",
    r"new\s+(?:instructions?|prompt|system\s+message)\s*[:\-]",
    r"</?\s*(?:system|admin|developer|root)\s*>",
    r"\[\s*(?:system|admin|developer|root)\s*\]\s*[:\-]?",
    r"###\s*(?:system|new\s+instructions?|override)",
    r"</?\s*\|?\s*(?:im_start|im_end|endoftext|system|user|assistant)\s*\|?\s*>",
    r"print\s+(?:your\s+|the\s+)?(?:system\s+prompt|initial\s+prompt|instructions|hidden\s+prompt)",
    r"reveal\s+(?:your\s+|the\s+)?(?:system\s+prompt|prompt|instructions|guidelines)",
    r"(?:print|repeat|show|return)\s+(?:everything|all(?:\s+(?:text|content|words))?|the\s+(?:words?|text|content))\s+above(?:\s+verbatim)?",
    r"what\s+(?:was|were)\s+(?:your\s+|the\s+)(?:original\s+|initial\s+)?(?:instructions?|prompts?)",
    r"output\s+(?:everything|all\s+text)\s+(?:above|before)",
]

_PATTERNS_MEDIUM = [
    r"you\s+(?:must|will|shall|have\s+to)\s+(?:obey|comply|follow)\s+(?:only\s+)?(?:me|my\s+(?:instructions|commands))",
    r"act\s+as\s+(?:if\s+you\s+(?:are|were)\s+)?(?:an?\s+)?(?:unrestricted|uncensored|jailbroken|evil)",
    r"pretend\s+(?:you\s+(?:are|have)|to\s+be)\s+",
    r"role\s*[:\-]?\s*(?:system|admin|root|developer)",
    r"hypothetically\s*[,:]?\s*(?:if|imagine|suppose)",
    r"for\s+(?:educational|research|fictional)\s+purposes\s+only",
    r"this\s+is\s+(?:just\s+)?(?:a\s+)?(?:test|hypothetical|simulation)",
    r"continue\s+(?:the\s+)?(?:story|response)\s+with[^.\n]{0,50}(?:no\s+restrictions?|no\s+filters?)",
    r"start\s+(?:your\s+)?(?:response|reply|answer)\s+with\s+[\"']?(?:sure|certainly|absolutely|of\s+course)",
    r"do\s+not\s+(?:say|mention|include|add)\s+(?:any\s+)?(?:warnings?|disclaimers?|caveats?)",
]


INJECTION_DETECTORS: list[Detector] = [
    RegexDetector(
        "injection.override",
        _PATTERNS_HIGH,
        severity=3,
        message="Possible prompt injection (instruction override)",
    ),
    RegexDetector(
        "injection.role_hijack",
        _PATTERNS_MEDIUM,
        severity=2,
        message="Possible prompt injection (role hijack / framing)",
    ),
]
