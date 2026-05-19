"""Render a realistic terminal screenshot of promptshield in action."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Terminal palette (One Dark-ish)
BG = (30, 33, 41)
FG = (200, 204, 212)
PROMPT_USER = (152, 195, 121)
PROMPT_HOST = (97, 175, 239)
PROMPT_PATH = (224, 175, 104)
DIM = (130, 137, 151)

SEV_COLOR = {
    "CRITICAL": (224, 108, 117),
    "HIGH": (224, 108, 117),
    "MEDIUM": (229, 192, 123),
    "LOW": (97, 175, 239),
}

PAD = 24
LINE_H = 22
CHAR_W = 10


def _load_font(size: int = 16) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:\\Windows\\Fonts\\consola.ttf",
        "C:\\Windows\\Fonts\\CascadiaMono.ttf",
        "C:\\Windows\\Fonts\\CascadiaCode.ttf",
        "/System/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def run_scan() -> str:
    result = subprocess.run(
        [sys.executable, "-m", "promptshield", "scan", "examples/sample_prompt.txt", "--no-color"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return result.stdout


def render(lines: list[tuple[str, tuple[int, int, int] | None]], path: Path) -> None:
    font = _load_font(16)
    _load_font(16)
    max_len = max((len(ln[0]) for ln in lines), default=80)
    width = PAD * 2 + max_len * CHAR_W
    height = PAD * 2 + len(lines) * LINE_H + 30

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # title bar
    draw.rectangle([(0, 0), (width, 28)], fill=(40, 44, 52))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([(14 + i * 22, 8), (28 + i * 22, 22)], fill=color)
    draw.text((width // 2 - 80, 6), "promptshield ~ demo", fill=DIM, font=font)

    y = PAD + 14
    for text, color in lines:
        draw.text((PAD, y), text, fill=color or FG, font=font)
        y += LINE_H

    img.save(path)


def build_lines(scan_output: str) -> list[tuple[str, tuple[int, int, int] | None]]:
    lines: list[tuple[str, tuple[int, int, int] | None]] = []

    # Shell prompts + commands
    def prompt_line(cmd: str):
        return (f"sandeep@kali:~/promptshield$ {cmd}", PROMPT_USER)

    lines.append(prompt_line("cat examples/sample_prompt.txt"))
    sample = (ROOT / "examples" / "sample_prompt.txt").read_text(encoding="utf-8")
    for ln in sample.strip().splitlines():
        lines.append((ln, FG))
    lines.append(("", None))
    lines.append(prompt_line("promptshield scan examples/sample_prompt.txt"))

    for raw in scan_output.splitlines():
        if not raw.strip():
            lines.append(("", None))
            continue
        color = FG
        for sev, c in SEV_COLOR.items():
            if raw.lstrip().startswith(f"[{sev}]"):
                color = c
                break
        if "finding(s)" in raw:
            color = (229, 192, 123)
        lines.append((raw, color))

    lines.append(("", None))
    lines.append(prompt_line("echo $?"))
    lines.append(("1", FG))
    lines.append(prompt_line(""))
    return lines


def main() -> None:
    scan_output = run_scan()
    lines = build_lines(scan_output)
    out = OUT_DIR / "demo.png"
    render(lines, out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
