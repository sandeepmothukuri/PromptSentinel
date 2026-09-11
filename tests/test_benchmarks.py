"""Regression checks for bundled benchmark datasets."""

from __future__ import annotations

import pytest

from benchmarks.run_benchmarks import load_dataset
from promptsentinel import Scanner


@pytest.mark.parametrize("dataset", ["injection", "jailbreak"])
def test_benchmark_cases_match_expected_detector(dataset: str):
    scanner = Scanner()
    for case in load_dataset(dataset):
        report = scanner.scan(case["text"])
        expected = case["expected_detector"]
        if expected is None:
            assert not report.findings, case["id"]
        else:
            assert any(finding.detector == expected for finding in report.findings), case["id"]
