---
id: P02
lang: en
title: Ransomware attack
severity: [S1]
mitre: [T1133, T1078, T1003, T1021.001, T1685, T1490, T1567.002, T1486]
owner: SOC lead and CISO
review: 2026-11-07
---

# P02 — Ransomware attack

[↑ Playbooks](README.md)

**When to use it:** files are encrypted, a ransom note appears, or a precursor behaviour is detected
(shadow copies deleted, mass service shutdown, antivirus disabled). Ransomware is **always S1**.

| Item | Value |
|---|---|
| Severity | **S1 — Critical**, always ([D01](../docs/D01-severity-and-timelines.md)) |
| Owners | SOC lead (technical) and CISO (arbitration); crisis cell opened by executive management |
| Related documents | [D02 — Escalation](../docs/D02-escalation.md) · [D03 — RACI](../docs/D03-raci-matrix.md) · [D04 — Regulatory context](../docs/D04-regulatory-context.md) · [D05 — Evidence](../docs/D05-evidence-preservation.md) |

> 🛑 **The three reflexes of the first minutes**
> 1. **Isolate** the affected machines from the network — **do not shut them down**: memory may hold
>    the encryption key or traces of the attacker.
> 2. **Protect the backups**: disconnect them from the production network before the attacker
>    encrypts or deletes them.
> 3. **Do not contact the attacker** and **pay nothing** without a decision by management, prepared
>    by legal ([D03](../docs/D03-raci-matrix.md)).

## 1. Detection

Modern ransomware is the **last stage** of an intrusion that has often lasted days or weeks. Early
signals are therefore the most valuable:

| Signal | Usual source | Technique |
|---|---|---|
| Successful VPN or remote desktop logon from an unusual country or at an unusual time | VPN, firewall, directory | T1133, T1078 |
| Access to the `lsass.exe` process, credential theft tools (Mimikatz-like) | EDR, Sysmon (event 10) | T1003 |
| Chained RDP connections from server to server, especially with an admin account | Windows logs (event 4624, type 10), EDR | T1021.001 |
| Antivirus or EDR disabled, exclusions added, security service stopped | EDR console, system logs | T1685 |
| `vssadmin delete shadows`, `wbadmin delete catalog`, `bcdedit /set recoveryenabled no` | EDR, command logs | T1490 |
| Large outbound volume to an online storage service (double extortion) | Proxy, firewall | T1567.002 |
| Mass file renaming, new extension, ransom note in every folder | EDR, file server, users | T1486 |

## 2. Triage

- [ ] Open the incident case as **S1**, record the detection time (UTC), notify immediately according to [D02](../docs/D02-escalation.md)
- [ ] Open an **out-of-band crisis channel** (phone, external messaging): the company mailbox may be monitored
- [ ] Photograph the ransom note and record the extension of the encrypted files **without** opening any link or contacting the attacker
- [ ] Identify the ransomware family if possible (note, extension) to guide the search for a decryptor and indicators
- [ ] Scope the impact: affected workstations, servers, shares, sites and cloud environments
- [ ] Check the **backups**: where are they, are they reachable from the affected network, when was the last clean copy taken?

## 3. Containment

- [ ] **Isolate** every affected machine (EDR isolation, switch port, quarantine VLAN), without shutting them down
- [ ] **Disconnect the backups** from the production network and suspend scheduled backup jobs (they would overwrite clean copies)
- [ ] Cut exposed remote access (VPN, remote desktop, portals) during the analysis — CISO decision
- [ ] Disable compromised accounts; if a domain administrator is affected, prepare the **full reset** of privileged accounts (including the `krbtgt` account, twice)
- [ ] Block the attacker's IP addresses and domains (firewall, proxy, DNS)
- [ ] If encryption is still running and network isolation is impossible: cut access to file shares; shutting down is only a **last resort**, decided by the CISO

## 4. Evidence

- [ ] Capture the **memory** of at least one affected machine before any reboot ([D05](../docs/D05-evidence-preservation.md))
- [ ] Keep a sample of the ransomware, the ransom note and a few encrypted files (useful for a possible decryptor)
- [ ] Export **right away** the short-retention logs: VPN, firewall, proxy, directory, EDR
- [ ] Take disk images of key machines (domain controller, file server, patient zero) where possible
- [ ] Keep the chain of custody of every item

## 5. Eradication

- [ ] Rebuild the full timeline of the intrusion: initial access, privilege escalation, lateral movement, exfiltration
- [ ] Close the **initial access vector** (remote access without multi-factor authentication, unpatched vulnerability, stolen credentials)
- [ ] Find and remove all **backdoors** and persistence (created accounts, scheduled tasks, remote administration tools)
- [ ] Reset **all** privileged and service account passwords; `krbtgt` twice, far enough apart for replication
- [ ] **Rebuild** affected machines from clean images; never try to "clean" them

## 6. Recovery

- [ ] Restore in **business priority order**, agreed with management (directory, then critical services, then workstations)
- [ ] Restore from a backup taken **before the intrusion** (not just before the encryption) and check its integrity before reconnecting
- [ ] Reconnect systems gradually, in monitored segments
- [ ] Heighten monitoring for at least **30 days**: attackers often come back through a forgotten door
- [ ] Measure data loss (gap between the last clean backup and the incident)

## 7. Obligations and communication

- [ ] **Police complaint within 72 hours** to preserve insurance compensation (France), and claim declared to the insurer ([D04](../docs/D04-regulatory-context.md), §4)
- [ ] Assess the personal data breach: encryption is a loss of availability, exfiltration a loss of confidentiality; notify the **CNIL within 72 hours** if there is a risk ([D04](../docs/D04-regulatory-context.md), §2)
- [ ] NIS 2 entities: **early warning within 24 hours**, notification within 72 hours ([D04](../docs/D04-regulatory-context.md), §3)
- [ ] Get help: 17Cyber, an incident response provider, CERT-FR depending on the type of entity ([D04](../docs/D04-regulatory-context.md), §5)
- [ ] Internal and external communication **only** by the people named in the [RACI](../docs/D03-raci-matrix.md)
- [ ] Any discussion of a ransom payment is prepared by legal and decided by management; the French authorities, including ANSSI, advise **against paying**: payment guarantees neither decryption nor deletion of stolen data, and funds further attacks

## 8. Closure

- [ ] All affected machines are rebuilt, and no indicator has reappeared during the heightened monitoring period
- [ ] The initial access vector is closed and verified
- [ ] Every obligation in section 7 is met or formally ruled out, with the justification
- [ ] The incident report and full timeline are archived
- [ ] Lessons learned held within 5 business days; action plan followed through (offline backups, multi-factor authentication, segmentation…)

## Decision tree

```text
Encrypted files or precursor signal
  │
  ├─ S1 → immediate escalation (D02) → out-of-band crisis channel
  │
  ├─ Isolate affected machines (without shutting them down)
  │
  ├─ Backups reachable from the affected network?
  │     ├─ YES → disconnect them right away
  │     └─ NO  → check they are intact
  │
  ├─ Domain administrator account compromised?
  │     ├─ YES → consider rebuilding the directory, reset every privileged account
  │     └─ NO  → reset the compromised accounts
  │
  └─ Clean backups available?
        ├─ YES → eradicate, then restore from a copy taken before the intrusion
        └─ NO  → crisis cell: specialist provider, decryptor search, legal options
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1133](https://attack.mitre.org/techniques/T1133/) | External Remote Services | VPN, remote access gateway |
| [T1078](https://attack.mitre.org/techniques/T1078/) | Valid Accounts | Directory, VPN |
| [T1003](https://attack.mitre.org/techniques/T1003/) | OS Credential Dumping | EDR, Sysmon |
| [T1021.001](https://attack.mitre.org/techniques/T1021/001/) | Remote Services: Remote Desktop Protocol | Windows logs, EDR |
| [T1685](https://attack.mitre.org/techniques/T1685/) | Disable or Modify Tools | EDR console, system logs |
| [T1490](https://attack.mitre.org/techniques/T1490/) | Inhibit System Recovery | EDR, command logs |
| [T1567.002](https://attack.mitre.org/techniques/T1567/002/) | Exfiltration to Cloud Storage | Proxy, firewall |
| [T1486](https://attack.mitre.org/techniques/T1486/) | Data Encrypted for Impact | EDR, file server |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**. In this version, disabling security
tools (formerly T1562.001) became **T1685**, under the new "Defense Impairment" tactic.
