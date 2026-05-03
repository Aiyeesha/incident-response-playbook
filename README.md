# Incident Response Playbook

Structured incident response procedures for the most common cybersecurity threats.
Designed for SOC teams, IT admins, and security analysts working in SMB to mid-market environments.

## Contents

| Section | Description |
|---------|-------------|
| [`playbooks/`](./playbooks/) | Step-by-step response procedures by incident type |
| [`templates/`](./templates/) | Incident report and post-mortem templates |
| [`docs/`](./docs/) | Severity classification, escalation procedures |

## Playbooks

| ID | Incident Type | Severity |
|----|--------------|----------|
| [P01](./playbooks/P01-malware-infection.md) | Malware Infection | High – Critical |
| [P02](./playbooks/P02-ransomware.md) | Ransomware Attack | Critical |
| [P03](./playbooks/P03-data-breach.md) | Data Breach | High – Critical |
| [P04](./playbooks/P04-phishing-attack.md) | Phishing Attack | Medium – High |
| [P05](./playbooks/P05-unauthorized-access.md) | Unauthorized Access | High – Critical |

## Incident Response Lifecycle

```
Detection → Triage → Containment → Eradication → Recovery → Lessons Learned
```

Each playbook follows this lifecycle with concrete, actionable steps.

## How to Use

1. **Identify** the incident type using the severity matrix → [`docs/severity-classification.md`](./docs/severity-classification.md)
2. **Open** the matching playbook and follow steps sequentially
3. **Log** all actions in real time using [`templates/incident-report.md`](./templates/incident-report.md)
4. **Escalate** according to [`docs/escalation-procedures.md`](./docs/escalation-procedures.md)
5. **Document** lessons learned using [`templates/post-mortem.md`](./templates/post-mortem.md)

## License

MIT — free to adapt for your organization.
