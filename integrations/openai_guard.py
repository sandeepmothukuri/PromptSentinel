"""
OpenAI guard — drop-in wrapper around the OpenAI Python client.

Usage:
    from integrations.openai_guard import SafeOpenAI
    client = SafeOpenAI(api_key="sk-...", block_on="HIGH")
    response = client.chat(model="gpt-4o", messages=[{"role": "user", "content": msg}])
"""

from __future__ import annotations

from promptshield.scanner import Scanner, Severity


class SafeOpenAI:
    def __init__(
        self,
        api_key: str | None = None,
        block_on: str = "HIGH",
        disabled: list[str] | None = None,
    ) -> None:
        try:
            from openai import OpenAI

            self._client = OpenAI(api_key=api_key)
        except ImportError as e:
            raise ImportError("pip install openai") from e
        self.threshold = Severity.parse(block_on)
        self.scanner = Scanner(disabled=disabled or [])

    def chat(self, model: str = "gpt-4o-mini", messages: list[dict] | None = None, **kwargs):
        messages = messages or []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                report = self.scanner.scan(content)
                if report.has_findings(self.threshold):
                    return {
                        "blocked": True,
                        "reason": report.summary(),
                        "findings": [f.to_dict() for f in report.filter(self.threshold)],
                    }
        return self._client.chat.completions.create(model=model, messages=messages, **kwargs)
