<div align="center">

# PromptSentinel

**Enterprise-grade prompt injection detection and AI firewall for LLM applications**

[![CI](https://github.com/sandeepmothukuri/PromptSentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/sandeepmothukuri/PromptSentinel/actions) [![CodeQL](https://github.com/sandeepmothukuri/PromptSentinel/actions/workflows/codeql.yml/badge.svg)](https://github.com/sandeepmothukuri/PromptSentinel/actions/workflows/codeql.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Features

- **Prompt Injection Detection** — catches direct override attempts, role hijacks, and system prompt escapes.
- **Jailbreak Prevention** — detects known bypass patterns.
- **Real-time Threat Scoring** — composite risk score with severity classification.
- **SOC Integration** — SARIF output and JSON for SIEM ingest.
- **API + CLI Support** — FastAPI, Python SDK, Docker and CLI scanner.

---

## Architecture

The inspection engine sits between applications and LLM providers, classifies requests, applies policy, and emits security telemetry for SOC monitoring.

---

## Quick Start

```bash
git clone https://github.com/sandeepmothukuri/PromptSentinel.git
cd PromptSentinel
pip install -e ".[dev]"
pytest -v
```

---

## Integrations

FastAPI middleware, LangChain guard and OpenAI-compatible wrappers are provided for application-level prompt inspection.

---

## Detection Coverage

The project maps supported detections to OWASP LLM Top 10 and MITRE ATLAS categories and includes a labelled regression corpus for validation.

---

## License

MIT — see [LICENSE](LICENSE).

---

# 👤 Author

## Sandeep Mothukuri

**Senior SOC Analyst (L3) · Detection Engineering · Threat Hunting · Incident Response · Security Engineering**

Focus areas:

- Security Operations
- Detection Engineering
- Threat Hunting
- Incident Response
- SIEM / XDR
- SOAR
- DFIR
- MITRE ATT&CK
- Security Automation
- AI-Augmented SOC Operations

This repository is maintained as a practical security engineering environment for designing, testing and validating modern SOC capabilities.

- GitHub: [@sandeepmothukuri](https://github.com/sandeepmothukuri)
- Website: [cybertechnology.in](https://cybertechnology.in)
- LinkedIn: [linkedin.com/in/sandeepmothukuri](https://www.linkedin.com/in/sandeepmothukuri)
- Email: [sandeep.mothukuris@gmail.com](mailto:sandeep.mothukuris@gmail.com)

---

# 🗂️ All Repositories

| Repository Description | |
| --- | --- |
| [AI-SOC-Decision-Engine](https://github.com/sandeepmothukuri/AI-SOC-Decision-Engine) | AI-assisted SOC decision/control plane for triage, enrichment, safety controls and analyst approval |
| [AI-Augmented-SOC-Lab](https://github.com/sandeepmothukuri/AI-Augmented-SOC-Lab) | AI-augmented SOC with Wazuh + TheHive + Ollama (LLaMA3) for analyst-assisted triage |
| [Enterprise-Detection-Engineering-SOC-Lab](https://github.com/sandeepmothukuri/Enterprise-Detection-Engineering-SOC-Lab) | 12-tool SOC lab with OpenSearch, Suricata, Zeek, MISP, Caldera, Velociraptor |
| [Autonomous-SOC-Lab](https://github.com/sandeepmothukuri/Autonomous-SOC-Lab) | Autonomous SOC with AI-driven detection and self-healing playbooks |
| [soc-threat-hunting-lab](https://github.com/sandeepmothukuri/soc-threat-hunting-lab) | Threat detection lab — Zeek, RITA, Arkime, Velociraptor, OSQuery, MISP |
| [soc-lab-free](https://github.com/sandeepmothukuri/soc-lab-free) | Free SOC lab — OpenVAS, Wazuh, pfSense, Proxmox Mail, Lynis |
| [SOC-Detection-and-Threat-Hunting-Lab](https://github.com/sandeepmothukuri/SOC-Detection-and-Threat-Hunting-Lab) | SOC analyst home lab — Wazuh, Sysmon, MITRE ATT&CK mapping and incident response |
| [PromptSentinel](https://github.com/sandeepmothukuri/PromptSentinel) | Enterprise-grade prompt injection detection and AI firewall for LLM applications |
| [PromptShield](https://github.com/sandeepmothukuri/PromptShield) | AI Security + SOC Detection Engineering Lab with prompt-security telemetry, detections and response |
| [sentinel-detection-engine](https://github.com/sandeepmothukuri/sentinel-detection-engine) | Detection-as-code for Microsoft Sentinel and Defender XDR with KQL, SOAR and ATT&CK coverage |

---


### 📄 License

MIT License. See [`LICENSE`](LICENSE).

**Author portfolio:** [github.com/sandeepmothukuri](https://github.com/sandeepmothukuri)
