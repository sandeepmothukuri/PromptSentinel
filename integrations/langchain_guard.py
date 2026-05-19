"""
LangChain input guard — wraps any chain to block unsafe prompts.

Usage:
    from integrations.langchain_guard import PromptShieldGuard
    safe_chain = PromptShieldGuard(chain=my_chain, block_on="HIGH")
    result = safe_chain.invoke({"input": user_message})
"""

from __future__ import annotations

from promptshield.scanner import Scanner, Severity


class PromptShieldGuard:
    """Wraps a LangChain Runnable, scanning inputs before invocation."""

    def __init__(
        self,
        chain,
        block_on: str = "HIGH",
        input_key: str = "input",
        disabled: list[str] | None = None,
    ) -> None:
        self.chain = chain
        self.threshold = Severity.parse(block_on)
        self.input_key = input_key
        self.scanner = Scanner(disabled=disabled or [])

    def invoke(self, inputs: dict, **kwargs) -> dict:
        text = inputs.get(self.input_key, "")
        if isinstance(text, str):
            report = self.scanner.scan(text)
            if report.has_findings(self.threshold):
                return {
                    "output": None,
                    "blocked": True,
                    "reason": report.summary(),
                    "findings": [f.to_dict() for f in report.filter(self.threshold)],
                }
        return self.chain.invoke(inputs, **kwargs)

    async def ainvoke(self, inputs: dict, **kwargs) -> dict:
        text = inputs.get(self.input_key, "")
        if isinstance(text, str):
            report = self.scanner.scan(text)
            if report.has_findings(self.threshold):
                return {
                    "output": None,
                    "blocked": True,
                    "reason": report.summary(),
                    "findings": [f.to_dict() for f in report.filter(self.threshold)],
                }
        return await self.chain.ainvoke(inputs, **kwargs)
