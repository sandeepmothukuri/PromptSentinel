# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-19

### Added
- Core `Scanner` class with pluggable detector architecture
- **PII detectors**: email, phone, SSN, credit card (Luhn-validated), IPv4/IPv6, IBAN, passport-pattern
- **Secret detectors**: AWS access/secret keys, GitHub tokens (ghp/gho/ghu/ghs/ghr/PAT), OpenAI, Anthropic, Google, Slack, Stripe API keys, JWTs, PEM private key blocks, generic high-entropy strings
- **Prompt-injection detectors**: 25+ patterns covering instruction overrides, system tag injections, prompt-reveal attacks, role hijacks, hypothetical framing
- **Jailbreak detectors**: DAN, STAN, AIM, developer-mode, evil-confidant, opposite-day, translation-bypass, base64-obfuscation patterns
- CLI (`promptsentinel scan`) with `pretty`, `json`, and `sarif` output modes
- `--fail-on` severity flag for CI/CD gating
- `--disable` flag to suppress specific detectors
- `list-detectors` subcommand
- Library API (`Scanner`, `Report`, `Finding`, `Severity`)
- 32 unit tests covering all detectors and CLI paths
- GitHub Actions CI matrix: Linux / macOS / Windows × Python 3.9–3.12
- Auto-publish workflow for PyPI on GitHub release
- SARIF output compatible with GitHub Code Scanning

[0.1.0]: https://github.com/sandeepmothukuri/promptsentinel/releases/tag/v0.1.0
