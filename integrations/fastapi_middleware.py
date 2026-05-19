"""
FastAPI middleware — scan every request body for prompt injection before it
reaches your LLM route.

Usage:
    from integrations.fastapi_middleware import PromptShieldMiddleware
    app.add_middleware(PromptShieldMiddleware, block_on="HIGH", fields=["message"])
"""

from __future__ import annotations

import json
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from promptshield.scanner import Scanner, Severity


class PromptShieldMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        block_on: str = "HIGH",
        fields: list[str] | None = None,
        disabled: list[str] | None = None,
    ) -> None:
        super().__init__(app)
        self.threshold = Severity.parse(block_on)
        self.fields = fields or ["message", "prompt", "content", "text", "query"]
        self.scanner = Scanner(disabled=disabled or [])

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method == "POST":
            try:
                body = await request.body()
                data = json.loads(body)
                for field in self.fields:
                    if field in data and isinstance(data[field], str):
                        report = self.scanner.scan(data[field])
                        if report.has_findings(self.threshold):
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "error": "blocked_by_promptshield",
                                    "reason": report.summary(),
                                    "findings": [
                                        {
                                            "detector": f.detector,
                                            "severity": f.severity.name,
                                            "match": f.match,
                                        }
                                        for f in report.filter(self.threshold)
                                    ],
                                },
                            )
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        return await call_next(request)
