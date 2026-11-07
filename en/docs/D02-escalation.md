---
id: D02
lang: en
title: Escalation procedure
review: 2026-11-07
---

# D02 — Escalation procedure

[↑ Reference documents](README.md)

Escalating means **passing information up** to the people who have the authority or the skills to
decide. Late escalation is one of the most common reasons incidents get out of hand; early
escalation costs almost nothing.

## 1. The levels

| Level | Role | Decides… |
|---|---|---|
| **L1** | SOC analyst | Triage the alert, give a first severity rating, open the case |
| **L2** | Incident response analyst | Investigate, propose and apply technical containment |
| **L3** | SOC lead / incident response lead | Validate severity, coordinate, mobilise teams |
| **L4** | CISO | Arbitrate heavy measures (shut down a service, isolate a site), alert management |
| **L5** | Executive management / crisis cell | Business decisions: continuity, external communication, ransom, hiring an external provider |

The detailed "who does, who approves" for each phase is in the
[RACI matrix (D03)](D03-raci-matrix.md).

## 2. Who to notify, and when

| Severity ([D01](D01-severity-and-timelines.md)) | Notify | Timeline | Channel |
|---|---|---|---|
| **S1 — Critical** | L3, CISO, CIO, management; DPO and legal if personal data is involved | **Immediately** | Phone, then crisis channel |
| **S2 — High** | L3, CISO; DPO if personal data is involved | Within 1 hour | Phone or messaging |
| **S3 — Medium** | L3 | At the daily stand-up | Ticketing tool |
| **S4 — Low** | Nobody (recorded in the ticket) | — | Ticketing tool |

### Immediate escalation triggers, whatever the initial severity

- a **privileged account** (domain, hypervisor or cloud administrator) is involved;
- **personal** or confidential **data** may have been accessed or exfiltrated;
- **ransomware** or fast spreading is suspected;
- the incident affects a **backup** or **security system** (EDR, firewall, SIEM);
- **the media, a customer or an authority** is aware of the incident;
- the team **does not know** what to do or lacks the required permissions.

## 3. Decision tree

```text
Alert or report received
  │
  ├─ Is it an incident? (D01, §1) ── NO → handle as an event, record it
  │
  └─ YES → Rate the severity (D01, §2)
            │
            ├─ Any immediate escalation trigger (§2)? ── YES → escalate to L3 + CISO right away
            │
            ├─ S1 → L3 + CISO + CIO + management, immediately → open the crisis cell
            ├─ S2 → L3 + CISO within 1 hour
            ├─ S3 → L3 at the daily stand-up
            └─ S4 → record in the ticket
                      │
                      └─ At every status update: has severity changed? → re-rate
```

## 4. Communication rules during the incident

1. **Use an out-of-band channel** if the company's email or directory may be compromised: phone,
   external secure messaging, a dedicated conference bridge. An attacker inside the mailbox also
   reads the response team's messages.
2. **One voice** to the outside world: only the person designated in the [RACI (D03)](D03-raci-matrix.md)
   talks to the press, customers or authorities.
3. **Write it down, timestamp it, keep it**: every decision made verbally is recorded in the
   incident report with the time and its author.
4. **Need to know**: technical details are shared only with those who need them; an ongoing
   incident is not a topic for general discussion.

## 5. Crisis directory (to be completed)

Keep it **outside the information system** (printed copy and a copy on a secured personal device)
and check it **every quarter**: a crisis directory that is unreachable during a ransomware attack is
useless.

| Role | Name | Phone | Backup phone | Deputy |
|---|---|---|---|---|
| SOC lead | | | | |
| CISO | | | | |
| CIO | | | | |
| DPO | | | | |
| Legal | | | | |
| Communications | | | | |
| CEO / executive management | | | | |
| Incident response provider | | | | |
| Insurer (cyber claims line) | | | | |

Public contacts (CERT-FR, 17Cyber, CNIL, police complaint) are listed in
[D04 — Regulatory context](D04-regulatory-context.md).
