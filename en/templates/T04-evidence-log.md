---
id: T04
lang: en
title: Evidence log
review: 2026-11-07
---

# T04 — Evidence log

[↑ Templates](README.md)

This log records the **complete history** of every piece of evidence: its collection, its integrity,
its custody and its transfers. It puts [D05 — Evidence preservation](../docs/D05-evidence-preservation.md)
into practice.

> 🔒 **Keep it outside this repository**, in an access-restricted space. All times are in **UTC**.
> Never edit a line: add a new one (correction, transfer, return).

## 1. Header

| Field | Value |
|---|---|
| Incident | `INC-YYYY-NNN` ([T01](T01-incident-report.md)) |
| Log owner | |
| Evidence storage location | |
| Opened on (UTC) | |

## 2. Evidence inventory

| Ref. | Description | Source (host, serial no., IP) | Collection: date, time (UTC), by | Method and tool | SHA-256 hash | Size | Location |
|---|---|---|---|---|---|---|---|
| `INC-YYYY-NNN-E01` | Example: memory image | PC-ACCOUNTING-07, SN …, 10.0.2.47 | 2026-11-07 14:32, A. Smith | WinPmem from a write-protected drive | `…` | 16 GB | Encrypted disk no. 3 |
| | | | | | | | |

## 3. Chain of custody

One line **every time the evidence changes hands** and every time it is accessed.

| Ref. | Date and time (UTC) | Handed over by | Received by | Reason (analysis, copy, transfer to investigators…) | Hash verified (yes / no) | Signature |
|---|---|---|---|---|---|---|
| | | | | | | |

## 4. Return or destruction

| Ref. | Date (UTC) | Action (return, destruction, archiving) | Authorised by | Performed by | Method |
|---|---|---|---|---|---|
| | | | | | |

The retention period is agreed with legal: at least until the end of any legal or insurance
proceedings related to the incident.
