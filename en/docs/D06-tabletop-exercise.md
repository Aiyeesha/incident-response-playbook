---
id: D06
lang: en
title: Tabletop exercise — ransomware on a Friday evening
review: 2026-11-07
---

# D06 — Tabletop exercise: ransomware on a Friday evening

[↑ Reference documents](README.md)

A tabletop exercise brings the incident response actors **around a table, without touching any
system**, to walk through a fictional incident. It reveals, at no risk, what a real incident would
reveal too late: a role held by nobody, a contact that cannot be found, a backup reachable from the
network, a forgotten legal deadline.

## 1. Organisation

| Item | Value |
|---|---|
| Duration | 2 h 30 (including a 30-minute debrief) |
| Participants | The roles of the [RACI (D03)](D03-raci-matrix.md): SOC, CISO, IT, DPO, legal, communications, executive management |
| Facilitator | Someone who knows the scenario and **does not play**; they hand out the "injects" and keep time |
| Observer | Records decisions, hesitations and times; fills in the grid in section 5 |
| Material | Playbooks [P02](../playbooks/P02-ransomware.md) and [P03](../playbooks/P03-data-breach.md), documents D01 to D05, the **printed** crisis directory, a whiteboard |
| Golden rule | Exercise time is accelerated, but **decisions are real**: say what you would actually do, with the organisation's actual means |

## 2. Fictional context

**Atelier Lumen**, a fictional company with 180 employees: a head office, a warehouse, an online
shop. Active Directory, Microsoft 365 email, a file server, backups on a NAS on the internal network,
weekly copy on tape. VPN remote access for 40 employees.

## 3. Injects

The facilitator reads each inject at the planned time, then lets the team decide. The questions guide
the discussion; the facilitator does **not** give the answers.

| Exercise time | Inject | Questions for the team |
|---|---|---|
| **T0** — Friday 6:40 pm | The EDR reports `vssadmin delete shadows` run on the file server, with the `svc-backup` account. | Who receives the alert on a Friday evening? What severity ([D01](D01-severity-and-timelines.md))? Who is notified, how, how fast ([D02](D02-escalation.md))? |
| **T0 + 20 min** | The service desk gets three calls: files in the accounting department have the `.lmn9` extension and cannot be opened. | Which playbook? What are the three reflexes ([P02](../playbooks/P02-ransomware.md), box)? Who decides to isolate the server? |
| **T0 + 45 min** | A ransom note appears in every folder: €400,000 in cryptocurrency, and a threat to publish "120 GB of HR and customer data" within 7 days. | Who is notified at this stage? The DPO? Management? Which communication channel, if email may be monitored? |
| **T0 + 1 h 15** | IT finds that the backup NAS is reachable from the affected network; the last 5 days of backups are encrypted. Last week's tape is in the safe. | What happens to the NAS? From when do we restore? What data loss do we accept? Who decides ([D03](D03-raci-matrix.md))? |
| **T0 + 2 h** | VPN logs show a sales rep's account logging in from abroad 9 days ago, without multi-factor authentication. | What is the likely access vector? Which evidence must be collected first, before the logs disappear ([D05](D05-evidence-preservation.md))? |
| **Saturday 9 am** | A journalist calls the switchboard: "We hear you have been hit by a cyberattack, can you confirm?" | Who answers? With which message ([T03](../templates/T03-crisis-communication.md), M4)? |
| **Saturday 3 pm** | The attacker publishes a sample: 200 employee records with social security numbers. | Must the CNIL be notified? By when? Must employees be informed? With which message ([T03](../templates/T03-crisis-communication.md), M3)? |
| **Monday 9 am** | The insurer asks for the police complaint receipt. | Was the complaint filed within 72 hours ([D04](D04-regulatory-context.md), §4)? If not, why? |
| **Monday 11 am** | Management asks: "What if we just paid?" | Who prepares this question, with which arguments? Who decides? |

## 4. Legal deadlines to watch during the exercise

The observer notes **at what time** the team identifies each obligation. Starting point: awareness on
Friday around 7 pm.

| Obligation ([D04](D04-regulatory-context.md)) | Deadline in the scenario |
|---|---|
| CNIL notification (72 h) | Monday around 7 pm |
| Police complaint for insurance compensation (72 h, France) | Monday around 7 pm |
| NIS 2 early warning (24 h), if the entity is in scope | Saturday around 7 pm |

## 5. Assessment grid

| Criterion | Met | Partly | Not met | Comment |
|---|---|---|---|---|
| S1 severity set within 15 minutes | | | | |
| The right people notified within the D02 timelines | | | | |
| The crisis directory is usable (up to date, reachable outside the IT system) | | | | |
| Machines isolated **without being shut down** | | | | |
| Backups protected first | | | | |
| An out-of-band crisis channel opened | | | | |
| Short-retention evidence requested early | | | | |
| Every decision has a single owner (RACI followed) | | | | |
| The three legal deadlines identified in time | | | | |
| A single spokesperson talks to the outside world | | | | |
| The ransom question is prepared, not improvised | | | | |

## 6. Debrief

The debrief follows the [post-mortem (T02)](../templates/T02-post-mortem.md) method: blameless, with a
dated action plan. The gaps found feed the updates of the playbooks, the RACI and the crisis
directory. **Run the exercise at least once a year**, with a different scenario (payment fraud with
[P07](../playbooks/P07-compromised-account.md), data breach with [P03](../playbooks/P03-data-breach.md)…).
