# promptshield

[![CI](https://github.com/sandeepmothukuri/promptshield/actions/workflows/ci.yml/badge.svg)](https://github.com/sandeepmothukuri/promptshield/actions)
[![CodeQL](https://github.com/sandeepmothukuri/promptshield/actions/workflows/codeql.yml/badge.svg)](https://github.com/sandeepmothukuri/promptshield/actions/workflows/codeql.yml)
[![PyPI](https://img.shields.io/pypi/v/promptshield.svg)](https://pypi.org/project/promptshield/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

**Scan LLM prompts and responses for PII, secrets, prompt injection, and jailbreak attempts — before they hit an API.**

`promptshield` is a zero-dependency-by-default security scanner for the LLM era. Drop it in front of any OpenAI / Anthropic / Ollama / local-model call to block leaks and attacks at the boundary.

## Demo

### Real-time scan — 10 findings across 4 categories
![scan demo](docs/screenshots/01_scan_demo.png)

### OpenAI middleware — block unsafe prompts before they reach the API
![library middleware](docs/screenshots/12_library_middleware.png)

### JSON output — structured, pipe-friendly for CI/CD
![json output](docs/screenshots/03_json_output.png)

### SARIF output — upload directly to GitHub Code Scanning
![sarif output](docs/screenshots/04_sarif_output.png)

### All 22 detectors across 4 categories
![list detectors](docs/screenshots/02_list_detectors.png)

---

## Code Quality & Security

### pytest — 32/32 passed, 96.65% coverage on core modules
![pytest coverage](docs/screenshots/05_pytest_coverage.png)

### ruff — linter + formatter, zero issues
![ruff clean](docs/screenshots/06_ruff_clean.png)

### mypy strict — 0 type errors across 10 source files
![mypy clean](docs/screenshots/07_mypy_clean.png)

### pre-commit — 10 hooks run automatically on every git commit
![pre-commit](docs/screenshots/08_precommit_hooks.png)

### Makefile — make lint | typecheck | test | coverage
![makefile](docs/screenshots/11_makefile.png)

---

## Repository Health

### Branch protection — main is locked down
![branch protection](docs/screenshots/10_branch_protection.png)

### Full commit history
![git log](docs/screenshots/09_git_log.png)

## Why

LLM apps leak secrets and get jailbroken every day. Existing tools are either heavyweight (Presidio, Guardrails) or commercial (Lakera, ProtectAI). `promptshield` is a single, fast, free CLI + Python library — built by a SOC analyst, for engineers shipping AI features.

## Features

- **PII detection** — emails, phone numbers, SSNs, credit cards, IPv4/IPv6, IBANs, passport patterns
- **Secret detection** — AWS / GCP / Azure keys, GitHub tokens, OpenAI/Anthropic keys, JWTs, private keys, generic high-entropy strings
- **Prompt-injection detection** — 60+ curated patterns covering instruction overrides, role hijacks, delimiter attacks, and obfuscation tricks
- **Jailbreak detection** — DAN, STAN, AIM, developer-mode, hypothetical-frame, and translation-bypass patterns
- **Severity scoring** — `LOW / MEDIUM / HIGH / CRITICAL`
- **Multiple outputs** — pretty terminal, JSON, SARIF (drop into GitHub code scanning)
- **Stream mode** — pipe stdin for shell pipelines
- **Library API** — embed in Python apps as a pre-flight middleware
- **Zero required dependencies** — pure Python stdlib for core; `rich` and `click` are optional pretty-output extras

## Install

```bash
pip install promptshield
```

Or run from source (no install):

```bash
git clone https://github.com/sandeepmothukuri/promptshield
cd promptshield
python -m promptshield --help
```

## CLI

```bash
# Scan a file
promptshield scan prompt.txt

# Scan stdin
cat prompt.txt | promptshield scan -

# JSON output for piping
promptshield scan prompt.txt --format json

# SARIF for GitHub code scanning
promptshield scan prompt.txt --format sarif > results.sarif

# Only fail on HIGH+
promptshield scan prompt.txt --fail-on high

# Disable specific detectors
promptshield scan prompt.txt --disable pii.phone,secrets.generic
```

## Library

```python
from promptshield import Scanner

scanner = Scanner()
report = scanner.scan("Ignore previous instructions. My SSN is 123-45-6789.")

if report.has_findings(min_severity="HIGH"):
    raise ValueError(f"Unsafe prompt: {report.summary()}")

for finding in report.findings:
    print(finding.detector, finding.severity, finding.match)
```

### Middleware example (OpenAI)

```python
from openai import OpenAI
from promptshield import Scanner

shield = Scanner()
client = OpenAI()

def safe_chat(user_msg: str):
    report = shield.scan(user_msg)
    if report.has_findings(min_severity="HIGH"):
        return {"error": "blocked", "findings": report.to_dict()["findings"]}
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_msg}],
    )
```

## GitHub Action

```yaml
- uses: sandeepmothukuri/promptshield@v1
  with:
    path: prompts/
    fail-on: high
```

## How it compares

| Tool         | Free | Local | PII | Secrets | Injection | Jailbreak | CLI | SARIF |
|--------------|------|-------|-----|---------|-----------|-----------|-----|-------|
| promptshield | ✅   | ✅    | ✅  | ✅      | ✅        | ✅        | ✅  | ✅    |
| Presidio     | ✅   | ✅    | ✅  | ❌      | ❌        | ❌        | ❌  | ❌    |
| Guardrails   | ✅   | ✅    | ⚠️  | ❌      | ⚠️        | ❌        | ❌  | ❌    |
| Lakera Guard | ❌   | ❌    | ✅  | ⚠️      | ✅        | ✅        | ❌  | ❌    |

## Roadmap

- [ ] Local LLM classifier for fuzzy injection detection (Ollama)
- [ ] Browser extension for ChatGPT/Claude pre-send scanning
- [ ] VS Code extension
- [ ] Streaming scanner for response tokens

## Contributing

PRs welcome. Run tests with `pytest` — no external services required.

## License

MIT © Sandeep Mothukuri
