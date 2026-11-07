---
id: P03
lang: en
title: Data breach
severity: [S1, S2]
mitre: [T1078, T1213, T1530, T1005, T1560, T1567.002, T1048, T1041]
owner: SOC lead and DPO
review: 2026-11-07
---

# P03 — Data breach

[↑ Playbooks](README.md)

**When to use it:** confidential or personal data has been, or may have been, **accessed, copied or
disclosed** by an unauthorised person: theft by an attacker, export by an employee, accidental public
sharing, database exposed on the Internet, data found on a leak site.

| Item | Value |
|---|---|
| Usual severity | **S2**; **S1** if sensitive or personal data is affected at scale ([D01](../docs/D01-severity-and-timelines.md)) |
| Owners | SOC lead (investigation) and DPO (breach assessment) |
| Related documents | [D03 — RACI](../docs/D03-raci-matrix.md) · [D04 — Regulatory context](../docs/D04-regulatory-context.md) · [D05 — Evidence](../docs/D05-evidence-preservation.md) |

> ⏱️ **The 72-hour CNIL deadline starts when the organisation becomes aware of the breach**, not at
> the end of the investigation. The DPO is notified **as soon as** the case is opened, and an
> incomplete initial notification is better than a late one ([D04](../docs/D04-regulatory-context.md), §2).

## 1. Detection

| Signal | Usual source | Technique |
|---|---|---|
| Valid account accessing an unusual volume of documents, or at an unusual time | Directory, access logs, data loss prevention (DLP) tool | T1078, T1213 |
| Mass downloads from a cloud storage space (SharePoint, OneDrive, S3 bucket…) | Cloud audit logs | T1530 |
| Local files collected then large archives created (`.zip`, `.7z`, `.rar`) | EDR | T1005, T1560 |
| Upload to a personal storage or file-sharing service | Proxy, DLP, firewall | T1567.002 |
| Unusual outbound flow over another protocol (FTP, DNS, SMTP) | Firewall, DNS | T1048 |
| High outbound volume to a malware command-and-control address | Firewall, EDR | T1041 |
| Company data found online, report from a customer, a researcher or a journalist | Threat watch, external report | — |

## 2. Triage

- [ ] Open the case and record the **time of awareness** (UTC): it is the starting point of the legal deadlines
- [ ] Notify the **DPO** and legal immediately ([D02](../docs/D02-escalation.md), escalation triggers)
- [ ] Determine **which data**: categories (identity, contact details, bank data, health, credentials), approximate volume, people concerned (customers, employees, minors?)
- [ ] Determine **how**: external attack, misconfiguration, employee action, supplier
- [ ] Determine **whether the leak is ongoing**: access still open, account still active, sharing link still public
- [ ] Rate the severity ([D01](../docs/D01-severity-and-timelines.md)): sensitive data at scale = S1

## 3. Containment

- [ ] Close the source: remove the public link, restrict the cloud bucket, cut the exposed access
- [ ] Disable or reset the accounts used for the leak and revoke their sessions and access tokens
- [ ] Block the identified exfiltration destinations (domains, IP addresses, storage services)
- [ ] If an employee is involved: involve legal and human resources **before** any visible action, to comply with employment law and avoid compromising the investigation
- [ ] Request takedown of published data (host, platform) with legal's help

## 4. Evidence

- [ ] Export the access and audit logs covering the whole suspicious period (directory, cloud, applications, proxy, DLP)
- [ ] Keep a copy of the exposed data **as it leaked**, in an encrypted, access-restricted location, to measure the scope
- [ ] Take timestamped captures of online publications (page, URL, date), without interacting with the authors
- [ ] Keep the chain of custody ([D05](../docs/D05-evidence-preservation.md))

## 5. Eradication

- [ ] Fix the cause: storage configuration, excessive permissions, exploited vulnerability, missing multi-factor authentication
- [ ] If malware is involved: handle it with [P01](P01-malware.md)
- [ ] Rotate every secret exposed in the data (passwords, API keys, tokens, certificates)
- [ ] Review access rights to the data concerned (least privilege)

## 6. Recovery

- [ ] Reopen legitimate access with the new controls in place
- [ ] Set up heightened monitoring of access to the data concerned (dedicated DLP or SIEM rule)
- [ ] Regularly check whether the data reappears online (threat watch) for several weeks

## 7. Obligations and communication

- [ ] Record the breach in the **breach register**, even if it is not notified ([D04](../docs/D04-regulatory-context.md), §2)
- [ ] If the breach poses a risk to individuals: **notify the CNIL** within 72 hours, in phases if needed
- [ ] If the risk is **high**: inform the people concerned without undue delay, with practical advice (change passwords, beware of fraudulent calls…)
- [ ] NIS 2 entities: assess whether it is a significant incident and meet the 24-hour, 72-hour and 1-month deadlines ([D04](../docs/D04-regulatory-context.md), §3)
- [ ] For a malicious act: file a police complaint, within 72 hours if the organisation wants insurance compensation in France ([D04](../docs/D04-regulatory-context.md), §4)
- [ ] Notify customers or partners with contractual notification clauses

## 8. Closure

- [ ] The source of the leak is closed and the cause fixed
- [ ] The CNIL notification is complete (follow-up sent if needed), or the decision not to notify is **justified and documented**
- [ ] The people concerned have been informed if the risk is high
- [ ] The breach register and incident report are up to date
- [ ] Lessons learned held; prevention measures tracked (data classification, DLP, access reviews)

## Decision tree

```text
Suspected data breach
  │
  ├─ Notify the DPO right away → the 72-hour clock is running
  │
  ├─ Is the leak ongoing? ── YES → close the source first
  │
  ├─ Is personal data involved?
  │     ├─ NO  → confidentiality incident: investigate, complaint if malicious
  │     └─ YES → record in the breach register
  │               │
  │               ├─ Risk to individuals? ── NO  → document the justification
  │               └─ YES → notify the CNIL within 72 hours
  │                         │
  │                         └─ High risk? ── YES → inform the people concerned
  │
  └─ Malicious origin? ── YES → police complaint (within 72 hours for insurance)
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1078](https://attack.mitre.org/techniques/T1078/) | Valid Accounts | Directory, access logs |
| [T1213](https://attack.mitre.org/techniques/T1213/) | Data from Information Repositories | Audit logs (SharePoint, wiki, business tools) |
| [T1530](https://attack.mitre.org/techniques/T1530/) | Data from Cloud Storage | Cloud audit logs |
| [T1005](https://attack.mitre.org/techniques/T1005/) | Data from Local System | EDR |
| [T1560](https://attack.mitre.org/techniques/T1560/) | Archive Collected Data | EDR |
| [T1567.002](https://attack.mitre.org/techniques/T1567/002/) | Exfiltration to Cloud Storage | Proxy, DLP |
| [T1048](https://attack.mitre.org/techniques/T1048/) | Exfiltration Over Alternative Protocol | Firewall, DNS |
| [T1041](https://attack.mitre.org/techniques/T1041/) | Exfiltration Over C2 Channel | Firewall, EDR |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**.
