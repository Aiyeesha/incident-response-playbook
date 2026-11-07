# Incident Response Playbook

🇫🇷 [Version française](README.fr.md)

Cybersecurity incident response procedures **a team can use as-is**: for each incident type,
who does what, in which order, which evidence to preserve and which obligations apply.

> 🚧 **Work in progress** (v0.1.0 — scaffold). Playbooks land in steps 2 to 5.

## What the repository will contain

| Folder | Content |
|---|---|
| [`fr/`](fr/) · [`en/`](en/) | The full documentation, in French and English |
| `…/playbooks/` | P01 to P07: step-by-step procedures per incident type |
| `…/docs/` | Severity and timelines, escalation, RACI matrix, regulatory context, evidence, tabletop exercise |
| `…/templates/` | Incident report, post-mortem, crisis communication, evidence log |
| [`src/playbook_tools/`](src/playbook_tools/) | `playbook-check` validation tool (and, in step 7, JSON export) |

## Frameworks

- **NIST SP 800-61 Rev. 3** (April 2025), incident response recommendations aligned with the
  **NIST Cybersecurity Framework 2.0**; it supersedes Rev. 2 (2012).
- **MITRE ATT&CK** to describe the attack techniques of each playbook.
- French context: **ANSSI** and **CERT-FR** guidance, **Cybermalveillance.gouv.fr**,
  **GDPR** (articles 33 and 34) and the **NIS 2** directive.

## Roadmap

| Step | Content | Status |
|---|---|---|
| 1 | Repository, layout, automated checks in CI | ✅ |
| 2 | Common foundation: severity and timelines, escalation, RACI, regulatory context, evidence | ✅ |
| 3 | Playbooks P01 to P03: malware, ransomware, data breach | ✅ |
| 4 | Playbooks P04 to P07: phishing, unauthorised access, denial of service, compromised account | ✅ |
| 5 | Templates and tabletop exercise | ⏳ |
| 6 | Full English version | ⏳ |
| 7 | JSON export of the action checklists → **v1.0.0** | ⏳ |

## Document format

Each document starts with a **front matter** block between two `---` lines, rendered by GitHub as a
table and validated by `playbook-check`:

```yaml
---
id: P02                     # P = playbook, D = reference document, T = template
lang: en                    # must match the fr/ or en/ folder
title: Ransomware attack
severity: [S1]              # playbooks: possible severities, from S1 (critical) to S4 (low)
mitre: [T1486, T1490]       # playbooks: MITRE ATT&CK techniques
owner: SOC lead             # playbooks: procedure owner
review: 2026-11-07          # last review date (YYYY-MM-DD)
---
```

The accepted format is a **strict subset** of YAML (`key: value` and `key: [a, b]`): anything else is
rejected with a clear message, to avoid the pitfalls of full YAML.

`playbook-check` also verifies:

- that every document exists **in both languages**, with the same severities and MITRE techniques;
- that every MITRE ATT&CK technique **exists and is active** in the bundled official version (a revoked
  technique is reported with its replacement) and is **explained in the text**;
- that every playbook has its **8 numbered sections**, in order, with checklist actions;
- that **no internal link is broken**.

The technique list is extracted from MITRE's official data by `python scripts/update_attack_data.py`,
to be rerun for every new ATT&CK release (current version: **20.1**).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
playbook-check          # validate the documentation
pytest -v               # test the validation tool
```

## License

[MIT](LICENSE) © Aïcha Imène Dahoumane — free to adapt for your organisation.
