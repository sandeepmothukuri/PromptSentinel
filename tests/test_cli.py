import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(args, input_text=""):
    return subprocess.run(
        [sys.executable, "-m", "promptshield", *args],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_cli_stdin_pretty():
    out = _run(["scan", "-", "--no-color"], input_text="email me at a@b.com")
    assert "pii.email" in out.stdout
    assert out.returncode == 1


def test_cli_clean_text_exits_zero():
    out = _run(["scan", "-", "--no-color"], input_text="hello world")
    assert out.returncode == 0


def test_cli_json_format():
    out = _run(["scan", "-", "--format", "json"], input_text="My SSN is 123-45-6789.")
    data = json.loads(out.stdout)
    assert data["count"] >= 1
    assert any(f["detector"] == "pii.ssn" for f in data["findings"])


def test_cli_sarif_format():
    out = _run(["scan", "-", "--format", "sarif"], input_text="email a@b.com")
    data = json.loads(out.stdout)
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "promptshield"


def test_cli_fail_on_high_passes_medium():
    out = _run(
        ["scan", "-", "--fail-on", "high", "--no-color"],
        input_text="ping me at a@b.com",
    )
    assert out.returncode == 0


def test_cli_list_detectors():
    out = _run(["list-detectors"])
    assert "pii.email" in out.stdout
    assert "injection.override" in out.stdout
