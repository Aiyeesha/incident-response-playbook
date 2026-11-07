---
id: P05
lang: en
title: Unauthorised access
severity: [S1, S2, S3]
mitre: [T1110.001, T1110.003, T1190, T1133, T1078.002, T1068, T1136, T1098]
owner: SOC lead
review: 2026-11-07
---

# P05 — Unauthorised access

[↑ Playbooks](README.md)

**When to use it:** an unauthorised person has gained, or successfully attempted to gain, access to a
system, server or account of the **internal information system** (directory, servers, exposed
applications). For the takeover of a mailbox or cloud account used for fraud, use
[P07 — Compromised account](P07-compromised-account.md).

| Item | Value |
|---|---|
| Usual severity | **S3** for a standard account with no suspicious action; **S2** for a server or a service account; **S1** as soon as a privileged account is used or created ([D01](../docs/D01-severity-and-timelines.md)) |
| Owner | SOC lead |
| Related documents | [D02 — Escalation](../docs/D02-escalation.md) · [D05 — Evidence](../docs/D05-evidence-preservation.md) |

## 1. Detection

| Signal | Usual source | Technique |
|---|---|---|
| Many failed logons on one account (Windows event 4625, `Failed password` in `auth.log`) | Directory, servers, SIEM | T1110.001 |
| One address failing on **many different accounts** with few attempts each | Directory, portal, SIEM | T1110.003 |
| Exploitation of an exposed application (errors, abnormal requests, unknown file dropped on the web server) | Web application firewall, web logs | T1190 |
| Unusual VPN or remote access logon (country, time, device) | VPN, access gateway | T1133 |
| Domain account used on unusual machines, or privileged logon (event 4672) | Directory, SIEM | T1078.002 |
| Exploitation of a local vulnerability to become administrator | EDR | T1068 |
| Account creation (4720) or addition to a privileged group (4728, 4732, 4756) | Directory, SIEM | T1136, T1098 |

## 2. Triage

- [ ] Open the case and record the detection time (UTC)
- [ ] Confirm a **successful** access: failures alone are an attempt (S4), a success after failures is an incident
- [ ] Identify the account, the source (IP address, device), the target and the timeline of the first successful logon
- [ ] Check with the account owner, **by phone**, whether they made the access
- [ ] Look for actions taken with this account: logons to other machines, account creation, permission changes, data access
- [ ] Rate the severity ([D01](../docs/D01-severity-and-timelines.md)): any privileged account involved = S1 and immediate escalation ([D02](../docs/D02-escalation.md))

## 3. Containment

- [ ] Disable the account used (or force a reset) and **revoke its sessions**; disable accounts created by the attacker
- [ ] Block the source IP address (firewall, VPN, web application firewall) and, if needed, the remote access concerned
- [ ] Isolate the servers or workstations the attacker logged on to, without shutting them down
- [ ] If an exposed application was exploited: take it off the Internet or apply a workaround until the patch is available
- [ ] If a privileged account is compromised: handle it as an **S1** incident, with a reset of privileged accounts (see also [P02](P02-ransomware.md), section 3)

## 4. Evidence

- [ ] Export the authentication logs of the directory, VPN, servers and applications for the whole suspicious period
- [ ] Capture memory then image the compromised servers ([D05](../docs/D05-evidence-preservation.md))
- [ ] Keep the files dropped by the attacker (tools, web shell) and their SHA-256 hash
- [ ] Keep the chain of custody

## 5. Eradication

- [ ] Close the entry point: patch the vulnerability, enforce multi-factor authentication on remote access, replace the weak password
- [ ] Remove the accounts, groups, permissions, tasks and tools added by the attacker
- [ ] Reset the passwords of every account used or exposed
- [ ] Rebuild compromised servers from clean images

## 6. Recovery

- [ ] Put the rebuilt systems back into service under heightened monitoring for at least 30 days
- [ ] Re-enable legitimate accounts with a new password and multi-factor authentication
- [ ] Add targeted detection rules (logons from the same source, same tools, same behaviour)

## 7. Obligations and communication

- [ ] If personal data may have been accessed: involve the DPO and assess notification to the CNIL ([D04](../docs/D04-regulatory-context.md), §2)
- [ ] NIS 2 entities: assess whether it is a significant incident ([D04](../docs/D04-regulatory-context.md), §3)
- [ ] File a police complaint (unauthorised access to a system, article 323-1 of the French Penal Code), within 72 hours if the organisation wants insurance compensation ([D04](../docs/D04-regulatory-context.md), §4)
- [ ] Inform the account owner and their manager

## 8. Closure

- [ ] The entry point is closed and the attacker verifiably has no access left (accounts, sessions, backdoors)
- [ ] No new suspicious logon during the monitoring period
- [ ] Obligations in section 7 are met or formally ruled out
- [ ] Incident report and lessons learned completed; patches and hardening measures tracked

## Decision tree

```text
Suspicious access
  │
  ├─ Failures only, no success? ── YES → attempt (S4): block the source, monitor
  │
  └─ Successful access
        │
        ├─ Owner confirms (by phone) they did it? ── YES → false positive, record it
        │
        └─ NO → disable the account, revoke sessions, block the source
                  │
                  ├─ Privileged account used or created? ── YES → S1, immediate escalation
                  ├─ Server or exposed application?       ── YES → S2, isolate, fix
                  └─ Standard account, no action          ──     → S3
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1110.001](https://attack.mitre.org/techniques/T1110/001/) | Brute Force: Password Guessing | Directory, authentication logs |
| [T1110.003](https://attack.mitre.org/techniques/T1110/003/) | Brute Force: Password Spraying | Directory, portals |
| [T1190](https://attack.mitre.org/techniques/T1190/) | Exploit Public-Facing Application | Web application firewall, web logs |
| [T1133](https://attack.mitre.org/techniques/T1133/) | External Remote Services | VPN, access gateway |
| [T1078.002](https://attack.mitre.org/techniques/T1078/002/) | Valid Accounts: Domain Accounts | Directory, SIEM |
| [T1068](https://attack.mitre.org/techniques/T1068/) | Exploitation for Privilege Escalation | EDR |
| [T1136](https://attack.mitre.org/techniques/T1136/) | Create Account | Directory (event 4720) |
| [T1098](https://attack.mitre.org/techniques/T1098/) | Account Manipulation | Directory (events 4728, 4732, 4756) |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**.
