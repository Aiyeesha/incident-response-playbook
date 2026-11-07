---
id: D04
lang: en
title: Regulatory context and reporting
review: 2026-11-07
---

# D04 — Regulatory context and reporting

[↑ Reference documents](README.md)

A cybersecurity incident is also a **legal event**. Several obligations may apply **at the same
time**, each with its own deadline, often running while the technical team is still busy containing
the attack. This document gathers them so that none is forgotten. It covers **EU law and the French
context**; organisations elsewhere must map their own national requirements.

> ⚠️ **This document is not legal advice.** It gives reference points checked on the review date shown
> at the top, with the official source of each obligation. Before any notification, have the process
> validated by your legal team or DPO.

## 1. Deadlines at a glance

| Obligation | Who | Deadline | Recipient |
|---|---|---|---|
| Personal data breach (GDPR, art. 33) | Every data controller | **72 hours** after becoming aware of it, if the breach poses a risk | Supervisory authority (CNIL in France) |
| Informing data subjects (GDPR, art. 34) | Every data controller | Without undue delay, if the risk is **high** | Data subjects |
| Breach register (GDPR, art. 33(5)) | Every data controller | **Always**, even without notification | Internal document |
| NIS 2 early warning (directive, art. 23) | Essential and important entities | **24 hours** after becoming aware of a significant incident | CSIRT or competent authority |
| NIS 2 incident notification | Same | **72 hours** | Same |
| NIS 2 final report | Same | **1 month** after the notification | Same |
| Police complaint to be compensated (French Insurance Code, art. L. 12-10-1) | Businesses insured against cyber risk in France | **72 hours** after becoming aware of the attack | Police, gendarmerie or public prosecutor |

These deadlines **do not replace each other**: one ransomware attack with data theft can require, in
the same week, a CNIL notification, a NIS 2 early warning, a police complaint and an insurance claim.

## 2. GDPR: personal data breach

**What is a breach?** Any accidental or unlawful destruction, loss, alteration, disclosure of, or
access to, personal data. Ransomware encrypting a customer file is a breach (loss of availability),
even without theft.

| Step | What the CNIL says |
|---|---|
| **Assess the risk** | No risk to the rights and freedoms of individuals: no notification, but internal documentation is mandatory. **When in doubt, notify.** |
| **Notify within 72 hours** | Without undue delay and, where feasible, within 72 hours of becoming aware. Beyond that, explain the reasons for the delay. |
| **Notify in phases** | An initial notification, then a follow-up notification as soon as the missing information is available. |
| **Inform individuals** | Mandatory when the risk is **high**. The CNIL can require it if it has not been done. |
| **Document** | **All** breaches, notified or not: nature, categories and approximate number of individuals and records, likely consequences, measures taken. |

**How to notify (France):** the CNIL online notification service, reserved for data controllers
(link in section 6). A preparatory document helps gather the information in advance.

## 3. NIS 2: significant incidents

Directive (EU) 2022/2555, known as **NIS 2**, requires **essential** and **important** entities to
report their **significant incidents**.

**Significant incident** (article 23(3)): an incident that has caused, or is capable of causing,
severe operational disruption of the services or financial loss for the entity, **or** that has
affected, or is capable of affecting, other natural or legal persons by causing considerable
material or non-material damage.

**The deadlines** (article 23(4)), to the CSIRT or the competent authority:

| Deadline | Expected content |
|---|---|
| **24 hours** — early warning | State whether the incident is suspected of being caused by unlawful or malicious acts, and whether it could have a cross-border impact |
| **72 hours** — incident notification | Update the early warning, give an initial assessment (severity, impact) and the indicators of compromise available |
| **On request** — intermediate report | Status updates requested by the CSIRT or the authority |
| **1 month** after the notification — final report | Detailed description, likely root cause, mitigation measures applied, any cross-border impact |
| If the incident is still ongoing at the time of the final report | Progress report, then a final report within one month of handling the incident |

> ⚠️ **French transposition in progress.** On the review date of this document, the official ANSSI
> page describes the French transposing law as a **"Résilience" bill** still under examination. French
> arrangements (exact scope, authority, reporting platform) may therefore still change: check the ANSSI
> NIS 2 page before relying on them. Since 17 March 2026, ANSSI has published the **Référentiel Cyber
> France (ReCyF)**, the cybersecurity framework provided for by that bill.

## 4. Filing a police complaint (France)

A cyberattack is a **criminal offence**: attacks on automated data processing systems are covered by
articles 323-1 to 323-3-1 of the French Penal Code.

- **Why file a complaint?** To enable an investigation, to obtain a receipt useful with partners and
  banks and, for insured businesses, **to be compensated**.
- **Condition for insurance compensation** (article L. 12-10-1 of the French Insurance Code, in force
  since 24 April 2023): any payment by an insurer for an attack on an information system is
  conditional on a complaint filed **no later than 72 hours after the victim becomes aware of the
  attack**. This applies to **legal entities** and to **individuals acting in a professional
  capacity**.
- **Where?** At a police station, a gendarmerie unit, or in writing to the public prosecutor. The
  **17Cyber** service points to the right contact.
- **What to bring?** The timeline, the technical elements already gathered (without altering the
  evidence, see [D05](D05-evidence-preservation.md)), and the list of affected systems and data.

## 5. Getting help: public contacts (France)

| Service | For whom | What it offers |
|---|---|---|
| **17Cyber** (run by Cybermalveillance.gouv.fr, the police and the gendarmerie) | Individuals, businesses, local authorities | 24/7 online diagnosis, advice, referral to a provider or to law enforcement |
| **Cybermalveillance.gouv.fr** | Individuals, businesses, local authorities | Quick-reaction guides, directory of certified providers |
| **CERT-FR (ANSSI)** | Primarily: government, operators of vital importance and of essential services; can act nationwide | Online incident reporting; immediate assistance by phone on **3218** (or +33 9 70 83 32 18) or by email at cert-fr@ssi.gouv.fr |
| **CNIL** | Data controllers | Online personal data breach notification service |

## 6. Official sources

- GDPR — [notifying a personal data breach (CNIL, in French)](https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles)
- NIS 2 — [text of Directive (EU) 2022/2555 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) and
  [ANSSI NIS 2 page (in French)](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/)
- CERT-FR — [in case of an incident (ANSSI, in French)](https://cyber.gouv.fr/en-cas-dincident)
- Insurance — article L. 12-10-1 of the French Insurance Code, introduced by Law No. 2023-22 of
  24 January 2023: [French Treasury FAQ on the complaint requirement (in French)](https://www.tresor.economie.gouv.fr/Institutionnel/Niveau2/Pages/39db1de3-1230-46a0-8e1b-d38a739e0885/files/9065d98f-099e-4eb4-9ba5-23b68cd50feb)
- 17Cyber — [17cyber.gouv.fr](https://17cyber.gouv.fr)
- Cybermalveillance — [cybermalveillance.gouv.fr](https://www.cybermalveillance.gouv.fr)

> 🗓️ **To review at every revision of this document**: the status of the NIS 2 transposition in France
> and the related reporting platforms.
