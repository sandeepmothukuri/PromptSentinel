# PromptSentinel completion

§G
Fix verified detection, taxonomy, docs, Docker/CI gaps; push validated repo.

§C
Python >=3.9; public API/CLI stable; no real secrets; Docker image/API health pass; docs measured, not invented.

§I
cmd: `promptsentinel scan <text>` → findings; finding exit 1.
api: `GET /health` → `{status,version,detectors}`.
api: `POST /scan` → `ScanResponse`.
docker: `docker compose up` → API port 8000.
data: `models.threat_taxonomy.OWASP_MAPPING` → detector→OWASP/MITRE metadata.

§V
V1: benchmark attack case expected detector → ≥1 matching finding.
V2: detector change → regression test; clean control stays clean.
V3: ∀ registered detector → explicit taxonomy entry; sensitive PII/secrets → OWASP `LLM02`.
V4: README counts, benchmark claims, OWASP IDs → current repo-measured values.
V5: root Compose & Dockerfile → build; container `/health` → HTTP 200.
V6: CI runs tests, lint, type check, Docker build.
V7: public cmd/API/interface shapes ∈ §I unchanged.

§T
id|status|task|cites
T1|x|fix benchmark misses; add detector regressions|V1,V2,V7
T2|x|fix OWASP taxonomy; validate explicit mappings|V3,V7
T3|x|sync README claims/docs with measured repo state|V4,V7
T4|x|harden Docker files; add CI image build|V5,V6,V7
T5|.|run full checks; commit & push|V1,V2,V3,V4,V5,V6,V7

§B
id|date|cause|fix
B1|2026-09-08|subset pytest hits global coverage gate|-
