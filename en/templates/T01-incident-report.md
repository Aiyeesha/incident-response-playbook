---
id: T01
lang: en
title: Incident report
review: 2026-11-07
---

# T01 — Incident report

[↑ Templates](README.md)

> 📝 **How to use it.** Copy this template **outside this repository** (ticketing tool, secure document
> space) when the incident starts and fill it in **as you go**, not at the end. All times are in
> **UTC**. A completed report contains sensitive information: it must never be published.

## 1. Identification

| Field | Value |
|---|---|
| Reference | `INC-YYYY-NNN` |
| Short title | |
| Playbook followed | P0_ — |
| Author | |
| Incident owner (A in the [RACI](../docs/D03-raci-matrix.md)) | |
| Status | Open · Contained · Eradicated · Recovered · Closed |

## 2. Time markers

These times feed the SOC metrics: mean time to detect (MTTD = detection − estimated start) and mean
time to resolve (MTTR = recovery − detection).

| Step | Date and time (UTC) | Source or comment |
|---|---|---|
| Estimated start of the attack | | |
| Detection (alert or report) | | |
| Acknowledgement by an analyst | | |
| Escalation (L3, CISO…) | | |
| Containment verified | | |
| Eradication complete | | |
| Recovery complete | | |
| Closure | | |

## 3. Severity

| Date and time (UTC) | Severity ([D01](../docs/D01-severity-and-timelines.md)) | Deciding criterion | Decided by |
|---|---|---|---|
| | S_ | | |

## 4. Scope

| Item | Detail |
|---|---|
| Affected systems (name, role, IP address) | |
| Affected accounts | |
| Affected data (categories, volume, people concerned) | |
| Affected sites or services | |
| Business impact | |

## 5. Indicators of compromise

| Type (IP, domain, hash, account, file…) | Value | First seen (UTC) | Blocked? |
|---|---|---|---|
| | | | |

## 6. Action log

One line per action or decision, **at the time it happens**.

| Date and time (UTC) | Author | Action or decision | Result |
|---|---|---|---|
| | | | |

## 7. Evidence

Refer to the [evidence log (T04)](T04-evidence-log.md): log reference and number of items collected.

## 8. Obligations and reporting

| Obligation ([D04](../docs/D04-regulatory-context.md)) | Applicable? | Deadline (UTC) | Done on (UTC) | Reference |
|---|---|---|---|---|
| Breach register (GDPR) | Yes · No | — | | |
| CNIL notification (72 h) | Yes · No | | | |
| Informing data subjects | Yes · No | | | |
| NIS 2 — early warning (24 h) | Yes · No | | | |
| NIS 2 — notification (72 h) | Yes · No | | | |
| NIS 2 — final report (1 month) | Yes · No | | | |
| Police complaint (72 h for insurance, France) | Yes · No | | | |
| Insurance claim | Yes · No | | | |

For each "No", state the justification in one sentence.

## 9. Closure summary

| Field | Value |
|---|---|
| Root cause | |
| Initial access vector | |
| Immediate corrective measures | |
| Post-mortem scheduled on | [T02](T02-post-mortem.md) |
| Approved by (incident owner) | Name, date |
