"""Request / response models for the promptsentinel API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    text: str = Field(..., description="Text to scan", min_length=1, max_length=100_000)
    disabled: list[str] = Field(default_factory=list, description="Detector names to skip")
    min_severity: str = Field("low", description="Minimum severity: low|medium|high|critical")


class FindingOut(BaseModel):
    detector: str
    severity: str
    match: str
    line: int
    column: int
    message: str


class ScanResponse(BaseModel):
    summary: str
    count: int
    blocked: bool
    findings: list[FindingOut]


class HealthResponse(BaseModel):
    status: str
    version: str
    detectors: int
