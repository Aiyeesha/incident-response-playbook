# Severity Classification

Use this matrix to assign a severity level at the start of every incident.

## Severity Levels

| Level | Label | Response Time | Definition |
|-------|-------|---------------|------------|
| S1 | **Critical** | Immediate (< 15 min) | Active breach, data exfiltration in progress, ransomware spreading, full service outage |
| S2 | **High** | < 1 hour | Confirmed compromise of a single system, significant data at risk, partial service degradation |
| S3 | **Medium** | < 4 hours | Suspicious activity requiring investigation, limited impact, no confirmed breach |
| S4 | **Low** | < 24 hours | Policy violation, failed attack attempt, informational alert |

## Scoring Criteria

Rate each dimension 1–3 and sum the scores.

| Dimension | 1 — Low | 2 — Medium | 3 — High |
|-----------|---------|------------|----------|
| **Scope** | 1 device | Department | Whole network |
| **Data sensitivity** | Public | Internal | Confidential / PII |
| **Business impact** | Minimal | Moderate | Critical operations affected |
| **Propagation risk** | Contained | Limited spread | Active spreading |

**Score 4–5 → S4 / Low** 
**Score 6–7 → S3 / Medium** 
**Score 8–10 → S2 / High** 
**Score 11–12 → S1 / Critical**

## Examples

- Single endpoint malware, no network access → **S3 Medium** (score 6)
- Active ransomware spreading across file shares → **S1 Critical** (score 12)
- Phishing email opened, no payload executed → **S4 Low** (score 4)
- Admin credentials found in public GitHub repo → **S2 High** (score 9)
