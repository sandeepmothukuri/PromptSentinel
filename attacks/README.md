# Attack Examples

Real-world prompt injection, jailbreak, and PII leakage examples with PromptSentinel detection results.

Each example shows the raw attack, the blocked finding, risk score, and mitigation.

## Categories

| File | Category | OWASP |
|------|----------|-------|
| [injection_attacks.json](datasets/injection_attacks.json) | Prompt Injection | LLM01 |
| [jailbreak_attacks.json](datasets/jailbreak_attacks.json) | Jailbreak | LLM01 |
| [pii_leakage.json](pii_leakage.json) | PII / Sensitive Data | LLM06 |
| [secret_exfiltration.json](secret_exfiltration.json) | Secret Leakage | LLM06 |
| [indirect_injection.json](indirect_injection.json) | Indirect Injection | LLM01 |

## How to run

```bash
# Run all benchmarks
python benchmarks/run_benchmarks.py

# Scan a single attack file
promptsentinel scan attacks/indirect_injection.json --format json
```
