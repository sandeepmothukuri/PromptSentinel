# Roadmap

> Status: **Active Development** — contributions welcome

## v0.1.x — Current (Stable)

- [x] Core scanner with 22 detectors (PII, secrets, injection, jailbreak)
- [x] CLI with pretty/JSON/SARIF output
- [x] Python library API
- [x] pytest-cov: 96.65% coverage
- [x] ruff + mypy strict: zero errors
- [x] pre-commit hooks
- [x] GitHub Actions CI matrix (Linux/macOS/Windows × Python 3.9–3.12)
- [x] CodeQL security scanning
- [x] Branch protection + CODEOWNERS
- [x] FastAPI REST server (`api/`)
- [x] Docker + docker-compose
- [x] LangChain / FastAPI / OpenAI integrations
- [x] Attack simulation benchmarks

## v0.2.0 — Q3 2026

- [ ] **Semantic injection detection** via local embedding similarity (Ollama/sentence-transformers)
- [ ] **Obfuscation bypass detection** — leetspeak, Unicode homoglyphs, reversed text
- [ ] **Multi-language PII** — EU GDPR data types (NL BSN, DE Steuer-ID, FR NIR)
- [ ] **Rate-limiting middleware** — per-user scan quotas
- [ ] **Allowlist/denylist** — custom pattern override per deployment
- [ ] **Streaming scanner** — token-by-token response scanning
- [ ] `promptsentinel serve` CLI command (wraps uvicorn)

## v0.3.0 — Q4 2026

- [ ] **VS Code extension** — real-time scan in prompt files
- [ ] **Browser extension** — pre-send scan for ChatGPT, Gemini, and other AI chat interfaces
- [ ] **Benchmark dataset expansion** — 500+ labeled attack examples
- [ ] **Webhook support** — POST scan results to SIEM / Slack / PagerDuty
- [ ] **Audit log** — append-only JSON log of all findings with timestamps
- [ ] **Async scanner** — `await scanner.scan_async(text)`
- [ ] **OpenTelemetry traces** — span per detector

## v1.0.0 — 2027

- [ ] **Stable public API** — semantic versioning guarantee
- [ ] **WASM build** — run in browser, Edge, Cloudflare Workers
- [ ] **Policy-as-code** — YAML rule files for custom orgs
- [ ] **Enterprise audit report** — PDF/HTML compliance reports
- [ ] **SOC 2 alignment guide**

## Ideas Backlog

| Idea | Status | Champion |
|------|--------|----------|
| Rust rewrite for core scanner | Exploring | — |
| Go CLI binary (no Python dep) | Exploring | — |
| GitHub App (scan PRs automatically) | Planned | — |
| Hugging Face Spaces demo | Planned | — |
| PyPI publish | Ready | @sandeepmothukuri |

---

**Want to claim an item?** Open a [feature request](https://github.com/sandeepmothukuri/promptsentinel/issues/new?template=feature_request.md) and tag it with the milestone.
