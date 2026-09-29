"""
promptsentinel REST API
---------------------
Run:  uvicorn api.main:app --reload
Docs: http://localhost:8000/docs
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from promptsentinel import __version__
from promptsentinel.detectors import ALL_DETECTORS
from promptsentinel.scanner import Scanner, Severity

from .dashboard import get_dashboard_html
from .models import FindingOut, HealthResponse, ScanRequest, ScanResponse

app = FastAPI(
    title="promptsentinel API",
    description="Scan LLM prompts for PII, secrets, prompt injection, and jailbreaks.",
    version=__version__,
    license_info={"name": "MIT"},
    contact={
        "name": "Sandeep Mothukuri",
        "url": "https://github.com/sandeepmothukuri/promptsentinel",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
def dashboard() -> HTMLResponse:
    """Render the interactive PromptSentinel Security Operations Console."""
    return HTMLResponse(content=get_dashboard_html(), status_code=200)


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__, detectors=len(ALL_DETECTORS))


@app.post("/scan", response_model=ScanResponse, tags=["Scanning"])
def scan(req: ScanRequest) -> ScanResponse:
    try:
        min_sev = Severity.parse(req.min_severity)
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=422, detail=f"Invalid min_severity: {req.min_severity!r}"
        ) from exc

    scanner = Scanner(disabled=req.disabled)
    report = scanner.scan(req.text)
    findings = report.filter(min_sev)

    return ScanResponse(
        summary=report.summary(),
        count=len(findings),
        blocked=report.has_findings(min_sev),
        risk_score=report.risk_score,
        findings=[
            FindingOut(
                detector=f.detector,
                severity=f.severity.name,
                match=f.match,
                line=f.line,
                column=f.column,
                message=f.message,
            )
            for f in findings
        ],
    )


@app.get("/detectors", tags=["System"])
def list_detectors() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for d in ALL_DETECTORS:
        category = d.name.split(".")[0]
        groups.setdefault(category, []).append(d.name)
    return groups
