---
id: P07
lang: en
title: Compromised account and payment fraud
severity: [S1, S2]
mitre: [T1078.004, T1110.003, T1621, T1539, T1114.003, T1564.008, T1534, T1657]
owner: SOC lead
review: 2026-11-07
---

# P07 — Compromised account and payment fraud

[↑ Playbooks](README.md)

**When to use it:** an email or cloud account (Microsoft 365, Google Workspace…) is used by a third
party, especially when the account serves a **payment fraud** (business email compromise): fake change
of a supplier's bank details, fake urgent request from an executive ("CEO fraud"), fake invoice sent to
customers. These frauds rely on a real compromised mailbox or on an address that imitates it.

| Item | Value |
|---|---|
| Usual severity | **S2**; **S1** if a fraudulent transfer was made, if the account belongs to an executive or an administrator, or if customers received fake messages ([D01](../docs/D01-severity-and-timelines.md)) |
| Owner | SOC lead, with the finance department if a transfer is involved |
| Related documents | [P04 — Phishing](P04-phishing.md) · [D04 — Regulatory context](../docs/D04-regulatory-context.md) · [D05 — Evidence](../docs/D05-evidence-preservation.md) |

> 💸 **If a fraudulent transfer has left, every hour counts.** The finance department contacts the bank
> **immediately** to request a **recall of the funds**: the faster the request, the higher the chances
> of recovering the money. This action comes **before** the technical analysis.

## 1. Detection

| Signal | Usual source | Technique |
|---|---|---|
| Successful logon from an unusual country, device or Internet provider | Cloud sign-in logs (Entra ID, Google) | T1078.004 |
| Many failures on many accounts from the same sources, then one success | Cloud sign-in logs | T1110.003 |
| Burst of rejected multi-factor authentication requests, then one accepted | Authentication logs, user report | T1621 |
| Same session used from two places at once, without new authentication (cookie theft) | Cloud sign-in logs | T1539 |
| New forwarding rule to an external address | Mail audit log | T1114.003 |
| Rule moving or deleting certain messages (keywords "transfer", "bank details", "invoice", a supplier's name) | Mail audit log | T1564.008 |
| Phishing messages sent **from** the account to colleagues or customers | Email logs, reports | T1534 |
| Request to change bank details, urgent and confidential transfer request | Accounting, management | T1657 |

## 2. Triage

- [ ] Open the case, record the detection time (UTC); **if a transfer has left: alert the bank first** (box above)
- [ ] Check with the account owner, **by phone** (never through the compromised mailbox), whether they recognise the logons and actions
- [ ] List the suspicious logons: IP addresses, countries, devices, applications, period
- [ ] Look for **mailbox rules** created or modified (forwarding, moving, deleting) and third-party applications authorised on the account
- [ ] Look for messages sent by the attacker from the account, and their recipients (internal and external)
- [ ] Rate the severity ([D01](../docs/D01-severity-and-timelines.md)): transfer made, executive or administrator account = S1

## 3. Containment

- [ ] **Reset the password and revoke all sessions and tokens** of the account: a simple password change does not always log the attacker out
- [ ] Remove the authentication factors added by the attacker and re-register the owner's
- [ ] Disable the forwarding and hiding rules created, and withdraw consent from suspicious third-party applications
- [ ] Block the IP addresses and domains used (including look-alike domains of the company or a supplier)
- [ ] Quickly warn the recipients of the fake messages (colleagues, customers, suppliers), **by phone** for financial exchanges
- [ ] Freeze any pending payment to recently changed bank details until verified

## 4. Evidence

- [ ] Export the account's sign-in and audit logs for the whole period (at least 30 days before detection if possible)
- [ ] Keep the mailbox rules created by the attacker (export before deletion), the fake messages in original format and the exchanges with the bank
- [ ] Keep the transfer records: payment order, fraudulent bank details, exchanges that triggered it ([D05](../docs/D05-evidence-preservation.md))

## 5. Eradication

- [ ] Find the entry point: phishing ([P04](P04-phishing.md)), reused password, missing multi-factor authentication, authentication requests accepted out of fatigue
- [ ] Enforce **phishing-resistant** multi-factor authentication (security key, passkey) for sensitive accounts: executives, finance, administrators
- [ ] Check the other accounts targeted by the same attempts and the same campaign
- [ ] Forbid or control automatic forwarding to external addresses across the whole mail system

## 6. Recovery

- [ ] Hand the account back to its owner with new authentication factors and a unique password
- [ ] Restore the messages deleted or moved by the attacker's rules
- [ ] Monitor the account and those of its department for at least 30 days (logons, rules, sending)

## 7. Obligations and communication

- [ ] Payment fraud: **police complaint** (fraud), with the bank records, within 72 hours if the organisation wants insurance compensation in France ([D04](../docs/D04-regulatory-context.md), §4)
- [ ] A compromised mailbox almost always holds personal data: involve the DPO and assess notification to the CNIL ([D04](../docs/D04-regulatory-context.md), §2)
- [ ] Warn the customers and suppliers concerned, with a clear rule: **any change of bank details is verified by a call back** to a number already known
- [ ] Declare the claim to the insurer (cyber or fraud) as soon as possible

## 8. Closure

- [ ] The attacker has no access left to the account (sessions, rules, applications, authentication factors checked)
- [ ] The outcome of the transfer is known (fund recall successful or not) and documented
- [ ] The recipients of the fake messages have been warned
- [ ] Obligations in section 7 are met or formally ruled out
- [ ] Lessons learned completed; bank-detail change verification procedure introduced or reiterated

## Decision tree

```text
Suspicious account or unusual transfer request
  │
  ├─ Has a fraudulent transfer left? ── YES → bank immediately (fund recall) → S1
  │
  ├─ Does the owner recognise the activity (checked by phone)? ── YES → false positive, record it
  │
  └─ NO → reset, revoke sessions and tokens, remove malicious rules
            │
            ├─ Fake messages sent from the account?  ── YES → warn the recipients by phone
            ├─ Executive or administrator account?    ── YES → S1, immediate escalation
            └─ Otherwise                                     → S2
                      │
                      └─ Find the entry point (P04?) → phishing-resistant authentication
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1078.004](https://attack.mitre.org/techniques/T1078/004/) | Valid Accounts: Cloud Accounts | Cloud sign-in logs |
| [T1110.003](https://attack.mitre.org/techniques/T1110/003/) | Brute Force: Password Spraying | Cloud sign-in logs |
| [T1621](https://attack.mitre.org/techniques/T1621/) | Multi-Factor Authentication Request Generation | Authentication logs |
| [T1539](https://attack.mitre.org/techniques/T1539/) | Steal Web Session Cookie | Cloud sign-in logs |
| [T1114.003](https://attack.mitre.org/techniques/T1114/003/) | Email Collection: Email Forwarding Rule | Mail audit log |
| [T1564.008](https://attack.mitre.org/techniques/T1564/008/) | Hide Artifacts: Email Hiding Rules | Mail audit log |
| [T1534](https://attack.mitre.org/techniques/T1534/) | Internal Spearphishing | Email logs |
| [T1657](https://attack.mitre.org/techniques/T1657/) | Financial Theft | Accounting, bank |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**.
