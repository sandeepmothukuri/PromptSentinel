---
name: False negative (missed detection)
about: promptsentinel missed a PII, secret, injection, or jailbreak pattern
title: "[MISS] "
labels: false-negative, detection
assignees: sandeepmothukuri
---

**Category**
- [ ] PII
- [ ] Secret / API key
- [ ] Prompt injection
- [ ] Jailbreak

**Pattern that was missed**
```
paste the bypass string (feel free to sanitise actual secrets/PII)
```

**Expected detector to fire**
e.g. `injection.override`, `pii.ssn`

**Why it should be caught**
Brief explanation of the threat / attack vector.
