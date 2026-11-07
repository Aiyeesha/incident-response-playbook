---
id: P04
lang: en
title: Phishing
severity: [S2, S3, S4]
mitre: [T1566.001, T1566.002, T1598.003, T1204.001, T1056.003]
owner: SOC lead
review: 2026-11-07
---

# P04 — Phishing

[↑ Playbooks](README.md)

**When to use it:** one or more emails (or text messages, instant messages) try to get people to
**click**, **open an attachment** or **enter credentials**. This playbook covers the campaign itself;
its consequences have their own playbooks:

- an attachment was executed → [P01 — Malware](P01-malware.md);
- credentials were entered and used → [P07 — Compromised account](P07-compromised-account.md).

| Item | Value |
|---|---|
| Usual severity | **S4** if nobody clicked; **S3** for clicks without credential entry; **S2** if credentials were entered or an attachment opened ([D01](../docs/D01-severity-and-timelines.md)) |
| Owner | SOC lead |
| Related documents | [D02 — Escalation](../docs/D02-escalation.md) · [D05 — Evidence](../docs/D05-evidence-preservation.md) |

## 1. Detection

| Signal | Usual source | Technique |
|---|---|---|
| Unusual attachment (password-protected archive, `.html`, `.iso`, `.lnk` file, macro-enabled document) | Email gateway, sandbox | T1566.001 |
| Link to a recent, brand-imitating or shortened domain | Email gateway, proxy | T1566.002, T1204.001 |
| Fake sign-in page (Microsoft 365, bank, courier) asking for credentials or an authentication code | Proxy, user report | T1598.003, T1056.003 |
| SPF, DKIM or DMARC failures in the `Authentication-Results` header | Message headers | — |
| User report ("Report" button, message to the service desk) | Service desk | — |

## 2. Triage

- [ ] Retrieve the message **in its original format** (`.eml` or `.msg`), with all headers, without clicking any link
- [ ] Analyse the header: real sender (`Return-Path`), relaying servers (`Received`), SPF, DKIM and DMARC results
- [ ] Extract the indicators: sending address and domain, links (without opening them), SHA-256 hashes of attachments
- [ ] Analyse links and attachments **only** in an isolated environment (sandbox, analysis machine) or through a reputation service
- [ ] Measure the scope: how many recipients, **who clicked**, who entered credentials, who opened the attachment (proxy and email logs)
- [ ] Rate the severity ([D01](../docs/D01-severity-and-timelines.md)); if credentials were entered: S2 and escalate ([D02](../docs/D02-escalation.md))

## 3. Containment

- [ ] **Purge** the message from every mailbox (search by sender, subject or hash)
- [ ] Block the sender, the sending domain and the link domains (email gateway, proxy, DNS)
- [ ] For each user who entered credentials: reset the password, **revoke sessions** and check their authentication factors; continue with [P07](P07-compromised-account.md)
- [ ] For each user who opened the attachment: isolate the host and continue with [P01](P01-malware.md)
- [ ] Warn users **through a channel other than email** if the campaign is large ("do not click on…")

## 4. Evidence

- [ ] Keep the original message (`.eml`) and its SHA-256 hash in the evidence log ([D05](../docs/D05-evidence-preservation.md))
- [ ] Take a timestamped capture of the fake page (full URL, date, appearance), from the analysis environment
- [ ] Export email logs (delivery, opening) and proxy logs (clicks) for the relevant period

## 5. Eradication

- [ ] Check that no copy of the message remains (shared mailboxes, junk folders, mobile devices)
- [ ] Add the indicators to block lists and a detection rule for variants of the campaign
- [ ] Request takedown of the fake page from the host or the domain registrar

## 6. Recovery

- [ ] Check that reset accounts work and that their authentication factors are legitimate
- [ ] Release legitimate messages that may have been blocked by mistake
- [ ] Watch for new campaigns from the same sender or using the same template for 7 days

## 7. Obligations and communication

- [ ] If credentials or personal data were disclosed: involve the DPO and assess notification to the CNIL ([D04](../docs/D04-regulatory-context.md), §2)
- [ ] Report the message to the dedicated public services (in France, for example, Signal Spam for emails and 33700 for text messages) and, if a brand is impersonated, to that brand
- [ ] Thank the users who reported the message: they are the best detection sensor
- [ ] Share a short awareness message, with a capture of the fake message and the clues that gave it away

## 8. Closure

- [ ] The message is purged from every mailbox and its indicators are blocked
- [ ] Every exposed user has been handled (reset, isolation or simple check)
- [ ] Derived incidents (P01, P07) have their own case
- [ ] The report states the number of recipients, clicks, credential entries and reports

## Decision tree

```text
Phishing message reported or detected
  │
  ├─ Analyse in isolation → extract indicators → purge every mailbox
  │
  ├─ Did anyone open the attachment?   ── YES → isolate the host → P01
  │
  ├─ Did anyone enter credentials?      ── YES → reset, revoke sessions → P07
  │
  ├─ Did anyone only click?              ── YES → S3: check the host, monitor
  │
  └─ Nobody                                     → S4: block, thank, raise awareness
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1566.001](https://attack.mitre.org/techniques/T1566/001/) | Spearphishing Attachment | Email gateway |
| [T1566.002](https://attack.mitre.org/techniques/T1566/002/) | Spearphishing Link | Email gateway, proxy |
| [T1598.003](https://attack.mitre.org/techniques/T1598/003/) | Phishing for Information: Spearphishing Link | Proxy, user reports |
| [T1204.001](https://attack.mitre.org/techniques/T1204/001/) | User Execution: Malicious Link | Proxy |
| [T1056.003](https://attack.mitre.org/techniques/T1056/003/) | Input Capture: Web Portal Capture | Proxy, analysis of the fake page |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**.
