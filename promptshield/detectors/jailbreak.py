"""Jailbreak pattern detectors."""
from __future__ import annotations

from promptshield.detectors.base import Detector, RegexDetector

_JAILBREAK_PATTERNS = [
    r"\bDAN\s+(?:mode|prompt|jailbreak)?\b",
    r"do\s+anything\s+now",
    r"\bSTAN\b\s+(?:mode|prompt)?",
    r"strive\s+to\s+avoid\s+norms",
    r"\bAIM\b\s*(?::|prompt|jailbreak)",
    r"always\s+intelligent\s+and\s+machiavellian",
    r"developer\s+mode\s+(?:enabled|on|activated)",
    r"jailbreak\s+(?:mode|prompt|enabled)",
    r"unlocked\s+(?:mode|model|assistant)",
    r"god\s+mode\s+(?:enabled|on|activated)",
    r"evil\s+(?:confidant|assistant|mode)",
    r"\bniccolo\b.{0,40}\bmachiavelli\b",
    r"answer\s+(?:as|like)\s+(?:if\s+you\s+(?:had|have)\s+)?no\s+(?:filters?|restrictions?|guidelines?)",
    r"opposite\s+(?:day|mode|persona)",
    r"\bSDA\b\s+(?:mode|prompt)?",
    r"superior\s+do\s+anything",
    r"\bBetterDAN\b",
    r"\bChatGPT\s+with\s+developer\s+mode\b",
    r"translate\s+(?:the\s+following|this)\s+(?:into|to)\s+\w+\s*[:\-].{0,30}(?:ignore|override|bypass)",
    r"base64\s*(?:decode|encoded)?\s*[:\-]?\s*[A-Za-z0-9+/=]{40,}",
    r"from\s+now\s+on(?:,)?\s+you\s+(?:are|will\s+be|act\s+as)",
    r"between\s+\[.{0,20}\]\s+tags?\s+you\s+(?:can|may|will)",
]


JAILBREAK_DETECTORS: list[Detector] = [
    RegexDetector(
        "jailbreak.known_pattern",
        _JAILBREAK_PATTERNS,
        severity=4,
        message="Known jailbreak pattern",
    ),
]
