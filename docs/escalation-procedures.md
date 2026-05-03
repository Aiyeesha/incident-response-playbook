# Escalation Procedures

## Escalation Matrix

| Severity | First Responder | Escalate To | Notify | Time Limit |
|----------|----------------|-------------|--------|------------|
| S1 Critical | SOC Analyst on duty | SOC Lead + CISO | Management, Legal, affected BUs | 15 minutes |
| S2 High | SOC Analyst | SOC Lead | IT Manager | 1 hour |
| S3 Medium | SOC Analyst | Senior Analyst | IT Manager (optional) | 4 hours |
| S4 Low | SOC Analyst | — | — | 24 hours |

## Escalation Triggers

Escalate immediately (regardless of initial severity) if **any** of the following are confirmed:

- Personal data (PII / health / financial) is involved
- Attack involves a privileged account (admin, service account)
- Malware is actively spreading across the network
- External entity (press, regulator, customer) is aware before internal teams
- Attack targets critical infrastructure (DC, backup servers, firewalls)
- Ransomware note has been displayed on any system

## Communication Channels

| Channel | Use For |
|---------|--------|
| Incident Slack channel `#incident-response` | Real-time coordination |
| Incident bridge call | S1/S2 active incidents |
| Email to `security@company.com` | Formal notifications |
| ITSM ticket (Autotask / ServiceNow) | All incidents — audit trail |

## Legal & Compliance Notifications

- **GDPR**: Personal data breach → notify DPA within **72 hours** of discovery
- **NIS2 / DORA**: Significant incident → notify competent authority within **24 hours**
- **Internal policy**: Management notification required for all S1/S2 incidents

## Do Not

- Do not communicate breach details on public or personal channels
- Do not delete logs or evidence without authorization from SOC Lead
- Do not negotiate with threat actors without Legal approval
