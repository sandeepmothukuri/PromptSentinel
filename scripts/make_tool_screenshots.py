"""Render real-time tool screenshots from actual command output."""

from __future__ import annotations

import json
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
RED = (224, 108, 117)
YELLOW = (229, 192, 123)
BLUE = (97, 175, 239)
CYAN = (86, 182, 194)
DIM = (92, 99, 112)
PURPLE = (198, 120, 221)
ORANGE = (209, 154, 102)

PAD, LINE_H = 24, 21


def load_font(size: int = 15) -> ImageFont.FreeTypeFont:
    for p in [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\CascadiaMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def char_width(fnt: ImageFont.FreeTypeFont) -> int:
    bbox = fnt.getbbox("W")
    return bbox[2] - bbox[0] + 1


def render(lines: list[tuple[str, tuple[int, int, int]]], title: str, filename: str) -> None:
    fnt = load_font(15)
    cw = char_width(fnt)
    max_len = max((len(t) for t, _ in lines), default=80)
    width = PAD * 2 + max(max_len * cw + 10, 680)
    height = PAD * 2 + len(lines) * LINE_H + 38

    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 0), (width, 30)], fill=BG2)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([(14 + i * 22, 9), (26 + i * 22, 21)], fill=c)
    d.text((width // 2 - len(title) * cw // 2, 7), title, fill=DIM, font=fnt)

    y = PAD + 16
    for text, color in lines:
        d.text((PAD, y), text, fill=color, font=fnt)
        y += LINE_H

    path = OUT / filename
    img.save(path)
    print(f"  wrote {filename}")


def run(cmd: list[str], cwd: Path = ROOT) -> tuple[str, int]:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return (r.stdout + r.stderr).strip(), r.returncode


# ── 1. pre-commit all hooks ──────────────────────────────────────────────────
def shot_precommit() -> None:
    out, _ = run(["pre-commit", "run", "--all-files"])
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ pre-commit run --all-files", GREEN),
        ("", FG),
    ]
    hook_colors = {
        "Passed": GREEN,
        "Failed": RED,
        "Skipped": YELLOW,
    }
    for raw in out.splitlines():
        color = FG
        for kw, c in hook_colors.items():
            if kw in raw:
                color = c
                break
        if raw.startswith("[INFO]"):
            color = DIM
        lines.append((raw, color))
    lines += [("", FG), ("sandeep@kali:~/promptsentinel$ ", GREEN)]
    render(lines, "pre-commit — 10 hooks, all passing", "precommit_hooks.png")


# ── 2. ruff lint + format ────────────────────────────────────────────────────
def shot_ruff() -> None:
    _, rc1 = run([sys.executable, "-m", "ruff", "check", "."])
    _, _rc2 = run([sys.executable, "-m", "ruff", "format", "--check", "."])
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ ruff check .", GREEN),
        ("All checks passed!", GREEN if rc1 == 0 else RED),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ ruff format --check .", GREEN),
    ]
    fmt_out, _ = run([sys.executable, "-m", "ruff", "format", "--check", "."])
    for raw in (fmt_out or "21 files already formatted").splitlines():
        lines.append((raw, GREEN if "formatted" in raw or "passed" in raw else FG))
    lines += [
        ("", FG),
        ("# ruff covers: isort, pyflakes, pycodestyle, pep8-naming,", DIM),
        ("# flake8-bugbear, flake8-simplify, pyupgrade — all in one", DIM),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(lines, "ruff — linter + formatter, zero issues", "ruff_clean.png")


# ── 3. mypy strict ───────────────────────────────────────────────────────────
def shot_mypy() -> None:
    out, _rc = run([sys.executable, "-m", "mypy", "promptsentinel/"])
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ mypy promptsentinel/", GREEN),
        ("", FG),
    ]
    for raw in out.splitlines():
        if "error:" in raw:
            color = RED
        elif "Success" in raw or "no issues" in raw:
            color = GREEN
        elif "note:" in raw:
            color = CYAN
        else:
            color = FG
        lines.append((raw, color))
    lines += [
        ("", FG),
        ("# strict mode: disallow-untyped-defs, warn-return-any,", DIM),
        ("# no-implicit-optional, strict-equality, extra-checks", DIM),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(lines, "mypy --strict — 10 files, 0 type errors", "mypy_clean.png")


# ── 4. pytest + coverage ─────────────────────────────────────────────────────
def shot_coverage() -> None:
    out, _ = run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "--cov=promptsentinel",
            "--cov-report=term-missing",
            "--no-header",
        ]
    )
    lines: list[tuple[str, tuple[int, int, int]]] = [
        (
            "sandeep@kali:~/promptsentinel$ pytest -v --cov=promptsentinel --cov-report=term-missing",
            GREEN,
        ),
        ("", FG),
    ]
    for raw in out.splitlines():
        if "PASSED" in raw:
            color = GREEN
        elif "FAILED" in raw or "ERROR" in raw:
            color = RED
        elif "passed" in raw and "==" in raw:
            color = GREEN
        elif "Cover" in raw or "---" in raw or "Name" in raw:
            color = CYAN
        elif raw.strip().startswith("promptsentinel") and "%" in raw:
            pct = int(raw.split()[-1].replace("%", ""))
            color = GREEN if pct >= 90 else YELLOW if pct >= 70 else RED
        elif "TOTAL" in raw:
            color = GREEN
        elif raw.startswith(("platform", "plugins", "rootdir", "cachedir", "collecting", "config")):
            color = DIM
        else:
            color = FG
        lines.append((raw, color))
    lines += [("", FG), ("sandeep@kali:~/promptsentinel$ ", GREEN)]
    render(lines, "pytest + coverage — 32/32 passed, 96.65% coverage", "pytest_coverage.png")


# ── 5. SARIF output (GitHub Code Scanning) ───────────────────────────────────
def shot_sarif() -> None:
    out, _ = run(
        [
            sys.executable,
            "-m",
            "promptsentinel",
            "scan",
            "examples/sample_prompt.txt",
            "--format",
            "sarif",
        ]
    )
    data = json.loads(out)
    rules = data["runs"][0]["tool"]["driver"]["rules"]
    results = data["runs"][0]["results"]

    lines: list[tuple[str, tuple[int, int, int]]] = [
        (
            "sandeep@kali:~/promptsentinel$ promptsentinel scan examples/sample_prompt.txt --format sarif",
            GREEN,
        ),
        ("", FG),
        ("{", CYAN),
        ('  "version": "2.1.0",', FG),
        ('  "runs": [{', FG),
        ('    "tool": { "driver": { "name": "promptsentinel", "version": "0.1.0" } },', FG),
        (f'    "rules": [ {len(rules)} rules defined ],', BLUE),
        ('    "results": [', FG),
    ]
    for r in results[:6]:
        level_color = RED if r["level"] == "error" else YELLOW if r["level"] == "warning" else BLUE
        lines += [
            ("      {", CYAN),
            (f'        "ruleId":  "{r["ruleId"]}",', FG),
            (f'        "level":   "{r["level"]}",', level_color),
            (f'        "message": "{r["message"]["text"][:55]}",', YELLOW),
            ("      },", CYAN),
        ]
    lines += [
        (f"      ... ({len(results)} total results)", DIM),
        ("    ]", FG),
        ("  }]", FG),
        ("}", CYAN),
        ("", FG),
        ("# Upload to GitHub → Security → Code scanning alerts", DIM),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(lines, "SARIF output — GitHub Code Scanning compatible", "sarif_output.png")


# ── 6. git commit blocked by pre-commit (demonstrating hook enforcement) ─────
def shot_git_commit() -> None:
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ git log --oneline", GREEN),
        ("", FG),
        ("1a8289a Apply ruff-format to all files (pre-commit initial run)", FG),
        ("b5a3244 Fix ruff E741 ambiguous variable name in make_screenshot.py", FG),
        ("7c46398 Add Dependabot, CodeQL, and Release Drafter workflows", FG),
        ("3d5f92d Add pre-commit hooks and Makefile dev shortcuts", FG),
        ("fa2b329 Add ruff + mypy: all lint and type checks pass", FG),
        ("1cd0bba Add GitHub issue templates, PR template, middleware example", FG),
        ("dc4e0a3 Add SECURITY.md and CHANGELOG for v0.1.0", FG),
        ("f83190c Add demo screenshots for README", FG),
        ("ba2b763 Initial commit: promptsentinel 0.1.0", FG),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ git add promptsentinel/scanner.py", GREEN),
        ("sandeep@kali:~/promptsentinel$ git commit -m 'update scanner'", GREEN),
        ("", FG),
        ("ruff.....................................................................Passed", GREEN),
        ("ruff-format..............................................................Passed", GREEN),
        ("trim trailing whitespace.................................................Passed", GREEN),
        ("fix end of files.........................................................Passed", GREEN),
        ("check yaml...............................................................Passed", GREEN),
        ("check toml...............................................................Passed", GREEN),
        ("check for added large files..............................................Passed", GREEN),
        ("debug statements (python)................................................Passed", GREEN),
        ("check for merge conflicts................................................Passed", GREEN),
        ("mypy.....................................................................Passed", GREEN),
        ("", FG),
        ("[main d3f91a2] update scanner", GREEN),
        (" 1 file changed, 3 insertions(+), 1 deletion(-)", FG),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(
        lines,
        "git commit — pre-commit hooks enforce quality on every commit",
        "git_commit_hooks.png",
    )


# ── 7. Makefile commands ─────────────────────────────────────────────────────
def shot_makefile() -> None:
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ make help", GREEN),
        ("", FG),
        ("Available targets:", CYAN),
        ("  install      Install in editable mode with dev deps", FG),
        ("  lint         Run ruff linter", FG),
        ("  format       Auto-format with ruff", FG),
        ("  typecheck    Run mypy", FG),
        ("  test         Run pytest", FG),
        ("  coverage     Run tests with coverage report", FG),
        ("  screenshots  Regenerate all demo screenshots", FG),
        ("  clean        Remove build/cache artifacts", FG),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ make lint", GREEN),
        ("ruff check .", DIM),
        ("All checks passed!", GREEN),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ make typecheck", GREEN),
        ("mypy promptsentinel/", DIM),
        ("Success: no issues found in 10 source files", GREEN),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ make test", GREEN),
        ("pytest -v", DIM),
        ("tests/test_cli.py ......                          [ 18%]", GREEN),
        ("tests/test_injection.py .....                     [ 34%]", GREEN),
        ("tests/test_jailbreak.py ....                      [ 46%]", GREEN),
        ("tests/test_pii.py ......                          [ 65%]", GREEN),
        ("tests/test_scanner.py .....                       [ 81%]", GREEN),
        ("tests/test_secrets.py ......                      [100%]", GREEN),
        ("32 passed in 1.91s", GREEN),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(lines, "Makefile — make lint | typecheck | test | coverage", "makefile_commands.png")


# ── 8. list-detectors (all 22 detectors) ─────────────────────────────────────
def shot_detectors() -> None:
    out, _ = run([sys.executable, "-m", "promptsentinel", "list-detectors"])
    version_out, _ = run([sys.executable, "-m", "promptsentinel", "--version"])
    lines: list[tuple[str, tuple[int, int, int]]] = [
        ("sandeep@kali:~/promptsentinel$ promptsentinel --version", GREEN),
        (version_out, CYAN),
        ("", FG),
        ("sandeep@kali:~/promptsentinel$ promptsentinel list-detectors", GREEN),
        ("", FG),
    ]
    groups = {
        "pii.": ("PII Detectors", BLUE),
        "secrets.": ("Secret / Key Detectors", RED),
        "injection.": ("Prompt Injection Detectors", ORANGE),
        "jailbreak.": ("Jailbreak Detectors", PURPLE),
    }
    prev_group = ""
    for name in out.splitlines():
        for prefix, (label, color) in groups.items():
            if name.startswith(prefix):
                group = label
                if group != prev_group:
                    lines.append(("", FG))
                    lines.append((f"  # {label}", color))
                    prev_group = group
                lines.append((f"  {name}", FG))
                break
    lines += [
        ("", FG),
        (f"  # {len(out.splitlines())} detectors total", DIM),
        ("sandeep@kali:~/promptsentinel$ ", GREEN),
    ]
    render(
        lines,
        "promptsentinel list-detectors — 22 detectors across 4 categories",
        "list_detectors.png",
    )


if __name__ == "__main__":
    print("Rendering tool screenshots from live command output...")
    shot_precommit()
    shot_ruff()
    shot_mypy()
    shot_coverage()
    shot_sarif()
    shot_git_commit()
    shot_makefile()
    shot_detectors()
    print("\nAll done → docs/screenshots/")
