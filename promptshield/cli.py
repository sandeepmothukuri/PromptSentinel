"""Command-line interface — pure stdlib, no required deps."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from promptshield import __version__
from promptshield.scanner import Scanner, Severity


_SEV_COLOR = {
    "LOW": "\033[36m",
    "MEDIUM": "\033[33m",
    "HIGH": "\033[31m",
    "CRITICAL": "\033[1;31m",
}
_RESET = "\033[0m"


def _format_pretty(report, use_color: bool) -> str:
    lines = []
    for f in report.findings:
        sev = f.severity.name
        prefix = f"[{sev}]"
        if use_color:
            prefix = f"{_SEV_COLOR.get(sev, '')}{prefix}{_RESET}"
        match = f.match if len(f.match) < 60 else f.match[:57] + "..."
        lines.append(
            f"{prefix:<22} {f.detector:<30} {match!r:<40} (line {f.line}, col {f.column})"
        )
    if not lines:
        return "OK — no findings\n"
    lines.append("")
    lines.append(f"{len(report.findings)} finding(s) — {report.summary()}")
    return "\n".join(lines) + "\n"


def _format_sarif(report, source: str) -> str:
    rules: dict[str, dict] = {}
    results = []
    for f in report.findings:
        rules.setdefault(
            f.detector,
            {
                "id": f.detector,
                "shortDescription": {"text": f.detector},
                "fullDescription": {"text": f.message or f.detector},
                "defaultConfiguration": {"level": _sarif_level(f.severity)},
            },
        )
        results.append(
            {
                "ruleId": f.detector,
                "level": _sarif_level(f.severity),
                "message": {"text": f.message or f.detector},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": source},
                            "region": {
                                "startLine": f.line,
                                "startColumn": f.column,
                                "snippet": {"text": f.match},
                            },
                        }
                    }
                ],
            }
        )
    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "promptshield",
                        "version": __version__,
                        "informationUri": "https://github.com/sandeepmothukuri/promptshield",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(sarif, indent=2)


def _sarif_level(sev: Severity) -> str:
    if sev >= Severity.HIGH:
        return "error"
    if sev == Severity.MEDIUM:
        return "warning"
    return "note"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="promptshield",
        description="Scan LLM prompts/responses for PII, secrets, prompt injection, and jailbreak attempts.",
    )
    parser.add_argument("--version", action="version", version=f"promptshield {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan a file or stdin")
    scan.add_argument("path", help="File path, or '-' for stdin")
    scan.add_argument(
        "--format",
        choices=["pretty", "json", "sarif"],
        default="pretty",
        help="Output format (default: pretty)",
    )
    scan.add_argument(
        "--fail-on",
        default="low",
        help="Exit non-zero if any finding >= this severity (low/medium/high/critical)",
    )
    scan.add_argument(
        "--disable",
        default="",
        help="Comma-separated detector names to disable (e.g. pii.phone,secrets.generic)",
    )
    scan.add_argument("--no-color", action="store_true", help="Disable ANSI color output")

    sub.add_parser("list-detectors", help="List all available detectors")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "list-detectors":
        from promptshield.detectors import ALL_DETECTORS

        for d in ALL_DETECTORS:
            print(d.name)
        return 0

    if args.path == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        p = Path(args.path)
        if not p.exists():
            print(f"error: file not found: {args.path}", file=sys.stderr)
            return 2
        text = p.read_text(encoding="utf-8", errors="replace")
        source = str(p)

    scanner = Scanner(disabled=args.disable.split(",") if args.disable else [])
    report = scanner.scan(text)

    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2))
    elif args.format == "sarif":
        print(_format_sarif(report, source))
    else:
        use_color = (not args.no_color) and sys.stdout.isatty()
        sys.stdout.write(_format_pretty(report, use_color))

    threshold = Severity.parse(args.fail_on)
    return 1 if report.has_findings(threshold) else 0


if __name__ == "__main__":
    raise SystemExit(main())
