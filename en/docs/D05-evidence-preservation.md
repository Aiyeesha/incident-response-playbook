---
id: D05
lang: en
title: Evidence preservation
review: 2026-11-07
---

# D05 — Evidence preservation

[↑ Reference documents](README.md)

Evidence is used to **understand** the attack (how the attacker got in, what they did), to **verify**
that they are gone, and to **support** a police complaint or an insurance claim. Badly collected
evidence is often lost for good: a reboot wipes memory, a reinstall wipes the disk.

This document builds on **RFC 3227** ("Guidelines for Evidence Collection and Archiving"), the basic
reference for digital evidence collection.

## 1. Principles

1. **Collect first, analyse later.** Freeze the state of the system before trying to understand it.
2. **From most volatile to least volatile** (section 2).
3. **Change as little as possible.** Every command run on a compromised machine leaves traces and may
   overwrite clues.
4. **Do not trust the compromised system.** Its tools (`netstat`, `ps`, `dir`) may have been replaced
   by the attacker: use tools run from write-protected external media.
5. **Work on a copy**, never on the original.
6. **Write everything down, in UTC.** Every action is timestamped, stating whether the time is UTC or
   local (convention in this repository: **UTC**).
7. **Respect the law and privacy.** Collection is limited to what the investigation needs; involve the
   DPO as soon as employee or customer personal data is concerned.

## 2. Collection order

Order of volatility recommended by RFC 3227, from most fragile to most durable:

| Order | Item | Lifetime | Example tools (indicative) |
|---|---|---|---|
| 1 | CPU registers and cache | Nanoseconds | Rarely collected in practice |
| 2 | Memory, processes, network connections, routing table, ARP cache | Until shutdown | WinPmem, DumpIt (Windows); LiME, AVML (Linux); EDR collection |
| 3 | Temporary file systems | Until reboot | Copy of `/tmp`, `%TEMP%` |
| 4 | Disk | Until overwritten | Bit-by-bit disk image (FTK Imager, `dd`, `dc3dd`); targeted collection (KAPE, Velociraptor) |
| 5 | Remote logs and monitoring data | Depends on retention | SIEM export, firewall, directory, proxy and EDR logs |
| 6 | Physical configuration and network topology | Long | Diagrams, device configurations |
| 7 | Archival media | Very long | Backups |

> 🕒 **In practice, remote logs (order 5) often have the shortest retention.** A firewall or proxy may
> keep only a few days. Request their export **as soon as the incident is opened**, in parallel with
> collection on the hosts.

## 3. What not to do

| Avoid | Why | Instead |
|---|---|---|
| **Shutting down or rebooting** the machine | Memory is lost; an attacker may have booby-trapped the startup | **Isolate it from the network** (EDR isolation, switch port, quarantine VLAN) and leave it running |
| Running an antivirus "to clean up" | It deletes the malicious files before they are analysed | Collect first, eradicate later |
| Copying files with Explorer, `xcopy` or `tar` | Access times change | Disk image or forensic collection tool |
| Pulling the cable **without thinking** | Some malware wipes its traces when it loses the network | Assess with L2; with active ransomware, isolation remains the priority |
| Analysing the original | Any change weakens the value of the evidence | Work on a copy with a verified hash |

## 4. Proving evidence has not been altered

Each collected item gets a **SHA-256 hash**, computed **at collection time** and recomputed **at every
transfer**. Two identical hashes prove the file has not changed.

```powershell
# Windows (PowerShell): hash of a memory image
Get-FileHash -Algorithm SHA256 .\host42-memory.raw
```

```bash
# Linux: hash of a disk image
sha256sum host42-disk.img
```

The hash is copied into the **evidence log** (section 5), never only into a file stored next to the
evidence.

## 5. Chain of custody

The chain of custody is the **complete history** of a piece of evidence: where and when it was found,
who handled it, where it was stored and who it was handed to. Without it, evidence can be challenged.
For each item, record:

| Field | Example |
|---|---|
| Evidence ID | `INC-2026-014-E03` |
| Description | Memory image of host PC-ACCOUNTING-07 |
| Source | Host name, serial number, IP address |
| Collection | 2026-11-07 14:32 UTC, by A. Smith (L2), with WinPmem run from a write-protected USB drive |
| SHA-256 hash | Full value |
| Storage | Encrypted disk no. 3, SOC safe |
| Transfers | Date and time, from whom to whom, reason, hash verified (yes or no) |

A ready-to-fill template, the **evidence log**, will be added with the other templates (step 5 of the
project).

## 6. Storing and protecting evidence

- **Encrypted, access-restricted storage**: evidence contains sensitive data and, sometimes, live
  malware.
- **Collected malware** is kept in a password-protected archive (common convention: `infected`), on
  an isolated analysis machine, never on an office workstation.
- **Retention period** agreed with legal: at least until the end of any legal or insurance proceedings
  related to the incident.
- **Never in this repository**: `.gitignore` excludes common evidence formats, but the rule is simple:
  no data from a real incident goes to GitHub.

## 7. Source

- [RFC 3227 — Guidelines for Evidence Collection and Archiving](https://www.rfc-editor.org/rfc/rfc3227)
