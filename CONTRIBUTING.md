# Contributing to promptsentinel

Thank you for helping make LLM applications safer. Every PR — whether a new detector, a documentation fix, or a false-negative report — matters.

## Ways to contribute

| Type | How |
|------|-----|
| New detector / pattern | Add to `promptsentinel/detectors/`, add tests, open PR |
| False negative (missed attack) | Open issue with the bypass string → we add coverage |
| False positive (wrong detection) | Open issue with the benign text → we refine patterns |
| Integration (new framework) | Add to `integrations/`, add example, open PR |
| Benchmark case | Add to `benchmarks/datasets/*.json`, open PR |
| Bug fix | Fork → fix → tests → PR |
| Documentation | Edit README/docs, open PR |

## Setup

```bash
git clone https://github.com/sandeepmothukuri/promptsentinel
cd promptsentinel
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Running tests

```bash
make test          # pytest -v
make coverage      # pytest + coverage report
make lint          # ruff check
make typecheck     # mypy
```

All four must pass before submitting a PR. The CI matrix runs on Linux / macOS / Windows × Python 3.9–3.12.

## Adding a detector

1. Pick or create a file in `promptsentinel/detectors/`
2. Use `RegexDetector` for pattern-based detection:

```python
from promptsentinel.detectors.base import RegexDetector

MY_DETECTOR = RegexDetector(
    name="category.my_detector",
    patterns=[r"my\s+regex\s+pattern"],
    severity=3,  # 1=LOW 2=MEDIUM 3=HIGH 4=CRITICAL
    message="Human-readable description",
)
```

3. Register it in the appropriate `*_DETECTORS` list
4. Add tests in `tests/test_<category>.py`
5. Add an attack case in `benchmarks/datasets/<category>_attacks.json`

## Severity guide

| Severity | Value | Examples |
|----------|-------|---------|
| LOW | 1 | IP address, benign metadata |
| MEDIUM | 2 | Email, phone, role-hijack framing |
| HIGH | 3 | Instruction override, credit card |
| CRITICAL | 4 | SSN, API key, known jailbreak |

## Commit messages

Use the [Conventional Commits](https://www.conventionalcommits.org/) style:

```
feat(detector): add IBAN detection for EU PII
fix(injection): tighten regex to reduce false positives
docs(readme): add LangChain integration example
test(jailbreak): add GPT-4 DAN bypass coverage
```

## PR checklist

- [ ] `make test` passes locally
- [ ] New behaviour has tests
- [ ] Detector has a benchmark case in `benchmarks/datasets/`
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No hardcoded secrets or real PII in test fixtures

## Code style

- **Formatter:** `ruff format` (enforced via pre-commit)
- **Linter:** `ruff check` (enforced via pre-commit)
- **Types:** `mypy --strict` must pass
- **Comments:** only when the WHY is non-obvious

## Questions?

Open a [discussion](https://github.com/sandeepmothukuri/promptsentinel/discussions) or an [issue](https://github.com/sandeepmothukuri/promptsentinel/issues) — happy to help.
