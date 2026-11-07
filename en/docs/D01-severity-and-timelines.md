---
id: D01
lang: en
title: Severity and response timelines
review: 2026-11-07
---

# D01 — Severity and response timelines

[↑ Reference documents](README.md)

This document defines **how to rate the severity** of an incident and **how fast** it must be
handled. Every playbook refers to it: severity decides who is notified
([D02 — Escalation](D02-escalation.md)) and sets the pace of the whole response.

> ⚙️ **To be adapted.** The thresholds and timelines below are realistic **starting values** for a
> small or mid-sized company with a SOC (in-house or outsourced). Each organisation must validate
> them with its management and align them with its contracts (SOC provider, insurance, customers).

## 1. Event or incident?

| Term | Definition | Example |
|---|---|---|
| **Event** | Any observable occurrence on a system or network | A failed logon, an antivirus alert |
| **Incident** | An event that compromises, or actually threatens, the confidentiality, integrity or availability of a system or data, or that violates a security policy | An account used from an unusual country after 200 failed logons |

Only an **incident** triggers a playbook. An isolated event is handled in the normal SOC workflow
but **kept**: several harmless-looking events can, together, reveal an incident.

## 2. The four severity levels

The incident is assessed against **five criteria**. **The most severe criterion wins**: a single
criterion at S1 is enough to classify the incident as S1.

| Criterion | S1 — Critical | S2 — High | S3 — Medium | S4 — Low |
|---|---|---|---|---|
| **Business** | Operations stopped or essential service unavailable | Important service degraded, workaround possible | Limited impact on one team | No business impact |
| **Scope** | Several sites, the Active Directory domain or core infrastructure | Several workstations or one server | One workstation or one account | No system compromised |
| **Data** | Sensitive or personal data exfiltrated or encrypted at scale | Personal or confidential data likely exposed | Low-sensitivity internal data exposed | No data affected |
| **Privileges** | Domain or infrastructure administrator account compromised | Local privileged or service account compromised | Standard user account compromised | Attempt blocked |
| **Spread** | Ongoing and fast (worm, ransomware) | Possible in the short term | Unlikely | None |

### Rating examples

| Situation | Severity | Deciding criterion |
|---|---|---|
| Files encrypted on a file server, ransom note | **S1** | Fast spread, encrypted data |
| Domain administrator account used from an unknown address | **S1** | Privileges |
| One workstation infected by malware, isolated by the EDR | **S3** | Limited scope, spread unlikely |
| Customer file exported to a personal storage service | **S2** | Personal data likely exposed |
| Phishing email received and reported, nobody clicked | **S4** | No system compromised |

## 3. Response timelines per level

| Target | S1 — Critical | S2 — High | S3 — Medium | S4 — Low |
|---|---|---|---|---|
| **Acknowledgement** (an analyst starts working on it) | 15 minutes | 1 hour | 4 hours | 1 business day |
| **Escalation** to the SOC lead and the CISO | Immediate | Within 1 hour | At the daily stand-up | Not required |
| **Containment** (the threat no longer progresses) | 4 hours | 24 hours | 72 hours | 5 business days |
| **Status update** to stakeholders | Every 2 hours | Twice a day | Daily | At closure |
| **Lessons learned** after closure | Within 5 business days | Within 10 business days | Optional (monthly summary) | Not required |

Timelines start from the **moment the team becomes aware of the incident** (alert, report) and run
**24/7 for S1 and S2**. Acknowledgement, escalation and containment times are **recorded in the
incident report**: they are what later makes it possible to measure mean time to detect (MTTD) and
to resolve (MTTR).

> ⚠️ **Legal and contractual deadlines.** These internal timelines **do not replace** deadlines set by
> law or contract, which run **in parallel**: 72 hours to notify the French data protection authority
> (CNIL), 24 hours for the NIS 2 early warning, 72 hours to file a police complaint in order to be
> compensated by an insurer in France… See [D04 — Regulatory context](D04-regulatory-context.md).

## 4. Re-rating an incident

Severity is **not fixed**. It is reassessed at every status update:

- **upwards** as soon as a criterion worsens (a second host affected, personal data discovered,
  a privileged account involved);
- **downwards** only once containment is **verified**, never on a hunch.

Every severity change is **dated and justified** in the incident report, with the name of the person
who decided it (see [D03 — RACI matrix](D03-raci-matrix.md)).

## 5. Key takeaways

1. The **most severe criterion** sets the level.
2. When hesitating between two levels, pick **the higher one**, then re-rate.
3. Internal timelines and legal deadlines **run at the same time**.
