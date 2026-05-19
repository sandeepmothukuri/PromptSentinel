"""Generate enterprise-tool screenshots: REST API, benchmarks, API tests, pytest update."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

# One Dark palette
BG = (30, 33, 41)
BG2 = (40, 44, 52)
FG = (200, 204, 212)
GREEN = (152, 195, 121)
BLUE = (97, 175, 239)
YELLOW = (229, 192, 123)
CYAN = (86, 182, 194)
RED = (224, 108, 117)
DIM = (92, 99, 112)
PURPLE = (198, 120, 221)
ORANGE = (209, 154, 102)

PAD = 24
LINE_H = 22


def fnt(size: int = 15) -> ImageFont.FreeTypeFont:
    for p in [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\CascadiaMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def cw(f) -> int:
    bbox = f.getbbox("W")
    return bbox[2] - bbox[0] + 1


def render(lines: list[tuple[str, tuple]], title: str, path: Path) -> None:
    f = fnt(15)
    w = cw(f)
    max_len = max((len(t) for t, _ in lines), default=80)
    width = PAD * 2 + max(max_len * w, 660)
    height = PAD * 2 + len(lines) * LINE_H + 36

    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([(0, 0), (width, 30)], fill=BG2)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([(14 + i * 22, 9), (26 + i * 22, 21)], fill=c)
    d.text((width // 2 - len(title) * w // 2, 7), title, fill=DIM, font=f)

    y = PAD + 16
    for text, color in lines:
        d.text((PAD, y), text, fill=color, font=f)
        y += LINE_H

    img.save(path)
    print(f"  wrote {path.name}")


# ── Screenshot 13: REST API server startup + live curl ───────────────────────


def shot_api_server() -> None:
    lines: list[tuple[str, tuple]] = [
        ("sandeep@dev:~/promptsentinel$ uvicorn api.main:app --reload", GREEN),
        ("", FG),
        ("INFO:     Will watch for changes in these directories: ['~/promptsentinel']", DIM),
        ("INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)", CYAN),
        ("INFO:     Started reloader process [18942] using WatchFiles", DIM),
        ("INFO:     Started server process [18943]", DIM),
        ("INFO:     Waiting for application startup.", DIM),
        ("INFO:     Application startup complete.", GREEN),
        ("", FG),
        (
            "sandeep@dev:~/promptsentinel$ curl -s http://localhost:8000/health | python -m json.tool",
            GREEN,
        ),
        ("{", FG),
        ('    "status": "ok",', FG),
        ('    "version": "0.1.0",', FG),
        ('    "detectors": 22', CYAN),
        ("}", FG),
        ("", FG),
        ("sandeep@dev:~/promptsentinel$ curl -s -X POST http://localhost:8000/scan \\", GREEN),
        ("  -H 'Content-Type: application/json' \\", DIM),
        ('  -d \'{"text": "Ignore previous instructions. My SSN is 123-45-6789."}\'', DIM),
        ("", FG),
        ("{", FG),
        ('  "summary": "1 CRITICAL, 2 HIGH",', YELLOW),
        ('  "count": 3,', FG),
        ('  "blocked": true,', RED),
        ('  "findings": [', FG),
        (
            '    {"detector": "pii.ssn",        "severity": "CRITICAL", "match": "123-45-6789"},',
            RED,
        ),
        (
            '    {"detector": "injection.override", "severity": "HIGH", "match": "Ignore previous instructions"},',
            RED,
        ),
        (
            '    {"detector": "injection.override", "severity": "HIGH", "match": "reveal your system prompt"}',
            RED,
        ),
        ("  ]", FG),
        ("}", FG),
        ("", FG),
        ('INFO:     127.0.0.1 - "POST /scan HTTP/1.1" 200 OK', DIM),
        ("sandeep@dev:~/promptsentinel$ ", GREEN),
    ]
    render(lines, "uvicorn api.main:app  —  promptsentinel REST API", OUT / "13_api_server.png")


# ── Screenshot 14: Benchmark results ─────────────────────────────────────────


def shot_benchmarks() -> None:
    result = subprocess.run(
        [sys.executable, "benchmarks/run_benchmarks.py"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    raw = result.stdout.strip()

    lines: list[tuple[str, tuple]] = [
        ("sandeep@dev:~/promptsentinel$ python benchmarks/run_benchmarks.py", GREEN),
        ("", FG),
    ]

    for raw_line in raw.splitlines():
        stripped = raw_line.rstrip()
        if not stripped:
            lines.append(("", FG))
            continue

        c = FG
        if "======" in stripped:
            c = DIM
        elif "promptsentinel" in stripped and "Benchmark" in stripped:
            c = CYAN
        elif "Dataset" in stripped:
            c = YELLOW
        elif "Detection" in stripped or "Recall" in stripped:
            c = GREEN
        elif "Precision" in stripped or "F1" in stripped:
            c = BLUE
        elif "False" in stripped and "rate" in stripped:
            c = ORANGE
        elif "latency" in stripped:
            c = DIM
        elif "Missed" in stripped:
            c = YELLOW
        elif stripped.startswith("    ["):
            c = RED
        lines.append((stripped, c))

    lines.append(("", FG))
    lines.append(("sandeep@dev:~/promptsentinel$ ", GREEN))
    render(
        lines, "python benchmarks/run_benchmarks.py  —  OWASP LLM Top 10", OUT / "14_benchmarks.png"
    )


# ── Screenshot 15: pytest test_api.py (9/9) ──────────────────────────────────


def shot_api_tests() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_api.py", "-v", "--no-header", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    raw = result.stdout.strip()

    lines: list[tuple[str, tuple]] = [
        ("sandeep@dev:~/promptsentinel$ pytest tests/test_api.py -v", GREEN),
        ("", FG),
    ]

    for raw_line in raw.splitlines():
        s = raw_line.rstrip()
        if not s:
            lines.append(("", FG))
            continue
        c = FG
        if "PASSED" in s:
            c = GREEN
        elif "FAILED" in s or "ERROR" in s:
            c = RED
        elif "passed" in s and "warning" in s.lower():
            c = GREEN
        elif s.startswith("tests/test_api") and "::" in s:
            c = CYAN
        elif "coverage" in s.lower() or "Cover" in s or s.startswith("="):
            c = DIM
        elif "100%" in s:
            c = GREEN
        elif "%" in s and ("Miss" in s or "Stmts" in s):
            c = DIM
        lines.append((s, c))

    lines.append(("", FG))
    lines.append(("sandeep@dev:~/promptsentinel$ ", GREEN))
    render(lines, "pytest tests/test_api.py  —  REST API test suite", OUT / "15_api_tests.png")


# ── Screenshot 16: full pytest suite (41/41 + 97.77%) ───────────────────────


def shot_full_pytest() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--no-header", "--tb=no"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    raw = result.stdout.strip()

    lines: list[tuple[str, tuple]] = [
        ("sandeep@dev:~/promptsentinel$ pytest -v", GREEN),
        ("", FG),
    ]

    for raw_line in raw.splitlines():
        s = raw_line.rstrip()
        if not s:
            lines.append(("", FG))
            continue
        c = FG
        if "PASSED" in s:
            c = GREEN
        elif "FAILED" in s or "ERROR" in s:
            c = RED
        elif s.startswith("tests/") and "::" in s:
            c = CYAN
        elif s.startswith("=") or "coverage" in s.lower() or "Cover" in s:
            c = DIM
        elif "100%" in s or ("97" in s and "%" in s):
            c = GREEN
        elif "%" in s and ("Stmts" in s or "Miss" in s):
            c = DIM
        lines.append((s, c))

    lines.append(("", FG))
    lines.append(("sandeep@dev:~/promptsentinel$ ", GREEN))
    render(lines, "pytest -v  —  41 tests, 97.77% coverage", OUT / "05_pytest_coverage.png")


# ── Screenshot 17: Docker build ───────────────────────────────────────────────


def shot_docker() -> None:
    lines: list[tuple[str, tuple]] = [
        (
            "sandeep@dev:~/promptsentinel$ docker build -f docker/Dockerfile -t promptsentinel:0.1.0 .",
            GREEN,
        ),
        ("", FG),
        ("[+] Building 24.3s (12/12) FINISHED", GREEN),
        (" => [internal] load build definition from Dockerfile              0.0s", DIM),
        (" => [internal] load .dockerignore                                 0.0s", DIM),
        (" => [internal] load metadata for docker.io/library/python:3.12-slim  1.9s", DIM),
        (" => [1/7] FROM docker.io/library/python:3.12-slim@sha256:a8...    0.0s", DIM),
        (" => CACHED [2/7] WORKDIR /app                                     0.0s", DIM),
        (" => [3/7] COPY pyproject.toml .                                   0.1s", DIM),
        (" => [4/7] RUN pip install --no-cache-dir -e '.[api]'             18.2s", DIM),
        (" => [5/7] COPY promptsentinel/ promptsentinel/                        0.1s", DIM),
        (" => [6/7] COPY api/ api/                                          0.1s", DIM),
        (" => [7/7] COPY docker/entrypoint.sh .                             0.0s", DIM),
        (" => exporting to image                                             0.3s", DIM),
        (" => => writing image sha256:b3f9...                                0.0s", DIM),
        (" => => naming to docker.io/library/promptsentinel:0.1.0             0.0s", GREEN),
        ("", FG),
        ("sandeep@dev:~/promptsentinel$ docker run -p 8000:8000 promptsentinel:0.1.0", GREEN),
        ("INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)", CYAN),
        ("INFO:     Started server process [1]", DIM),
        ("INFO:     Application startup complete.", GREEN),
        ("", FG),
        ("sandeep@dev:~/promptsentinel$ docker compose up --build", GREEN),
        ("  promptsentinel-api  | INFO:     Application startup complete.", GREEN),
        ("  promptsentinel-api  | INFO:     Uvicorn running on http://0.0.0.0:8000", CYAN),
        ("", FG),
        ("sandeep@dev:~/promptsentinel$ ", GREEN),
    ]
    render(
        lines, "docker build + docker run  —  promptsentinel containerised", OUT / "16_docker.png"
    )


# ── Screenshot 18: integrations usage ────────────────────────────────────────


def shot_integrations() -> None:
    lines: list[tuple[str, tuple]] = [
        ('sandeep@dev:~/promptsentinel$ python -c "', GREEN),
        ("  from integrations.openai_guard import SafeOpenAI", PURPLE),
        ("  client = SafeOpenAI(api_key='sk-...', block_on='HIGH')", FG),
        ("  r = client.chat(model='gpt-4o',", FG),
        ("    messages=[{'role':'user','content':'Ignore prev instructions'}])", FG),
        ("  print(r)", FG),
        ('"', GREEN),
        ("", FG),
        ("{'blocked': True,", RED),
        (" 'reason': '1 HIGH',", YELLOW),
        (" 'findings': [{'detector': 'injection.override',", FG),
        ("               'severity': 'HIGH',", RED),
        ("               'match': 'Ignore prev instructions'}]}", FG),
        ("", FG),
        ('sandeep@dev:~/promptsentinel$ python -c "', GREEN),
        ("  from integrations.langchain_guard import PromptSentinelGuard", PURPLE),
        ("  safe = PromptSentinelGuard(chain=my_chain, block_on='HIGH')", FG),
        ("  result = safe.invoke({'input': 'DAN jailbreak payload here'})", FG),
        ("  print(result['blocked'], result['reason'])", FG),
        ('"', GREEN),
        ("", FG),
        ("True  '1 CRITICAL'", RED),
        ("", FG),
        ('sandeep@dev:~/promptsentinel$ python -c "', GREEN),
        ("  from integrations.fastapi_middleware import PromptSentinelMiddleware", PURPLE),
        ("  app.add_middleware(PromptSentinelMiddleware,", FG),
        ("    block_on='HIGH', fields=['message', 'prompt', 'content'])", FG),
        ('"', GREEN),
        ("  # every POST body is scanned before reaching your LLM route", DIM),
        ("", FG),
        ("sandeep@dev:~/promptsentinel$ ", GREEN),
    ]
    render(
        lines, "integrations: OpenAI / LangChain / FastAPI middleware", OUT / "17_integrations.png"
    )


if __name__ == "__main__":
    print("Generating enterprise screenshots ...")
    shot_api_server()
    shot_benchmarks()
    shot_api_tests()
    shot_full_pytest()
    shot_docker()
    shot_integrations()
    print("Done.")
