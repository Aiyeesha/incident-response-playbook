---
id: D03
lang: en
title: Incident response RACI matrix
review: 2026-11-07
---

# D03 — Incident response RACI matrix

[↑ Reference documents](README.md)

The RACI matrix states, for each activity, **who does what**. It prevents the two classic failures of
a crisis: the task everyone believes someone else has done, and the decision nobody dares to take.

| Letter | Meaning | Rule |
|---|---|---|
| **R** — Responsible | Carries out the activity | At least one per row |
| **A** — Accountable | Answers for it and decides | **Exactly one** per row |
| **C** — Consulted | Gives an opinion **before** the decision | Two-way exchange |
| **I** — Informed | Kept up to date **afterwards** | One-way information |

## 1. Roles

| Code | Role |
|---|---|
| **L1** | SOC analyst (level 1) |
| **L2** | Incident response analyst (level 2) |
| **SL** | SOC lead / incident response lead |
| **CISO** | Chief information security officer |
| **IT** | Systems, network and workplace teams (IT department) |
| **DPO** | Data protection officer |
| **LEG** | Legal |
| **COM** | Communications |
| **EXE** | Executive management / crisis cell |

## 2. The matrix

| Activity | L1 | L2 | SL | CISO | IT | DPO | LEG | COM | EXE |
|---|---|---|---|---|---|---|---|---|---|
| Detect and triage the alert | **R** | C | A | | | | | | |
| Rate the severity ([D01](D01-severity-and-timelines.md)) | R | R | **A** | I | | | | | |
| Escalate ([D02](D02-escalation.md)) | R | R | **A** | I | | | | | I |
| Collect and preserve evidence ([D05](D05-evidence-preservation.md)) | | **R** | A | I | C | | C | | |
| Technical containment | | R | **A** | C | R | | | | I |
| Shut down a service or isolate a site | | C | R | **A** | R | | | I | C |
| Eradication | | R | **A** | I | R | | | | |
| Restore and return to service | | C | R | I | **R** | | | | **A** |
| Assess the personal data breach | | C | C | C | | **R** | C | | **A** |
| Notify the CNIL ([D04](D04-regulatory-context.md)) | | | C | C | | **R** | C | | **A** |
| Inform the data subjects | | | | C | | R | C | R | **A** |
| Notify the NIS 2 authority / CERT-FR | | | R | **R** | | | C | | **A** |
| File a police complaint | | | C | R | | | **R** | | **A** |
| Declare the claim to the insurer | | | C | R | | | R | | **A** |
| Internal communication | | | C | C | | | C | **R** | **A** |
| External communication (customers, press) | | | | C | | C | C | **R** | **A** |
| Decide on any ransom payment | | | C | C | | | R | | **A** |
| Lessons learned | C | R | **A** | R | R | C | C | C | I |

> 💡 **How to read it.** In the "Restore" row, IT **does the work** and executive management
> **approves**: management decides to restart operations because it carries the risk. In the
> "Notify the CNIL" row, the DPO prepares and submits, but the **data controller** (represented by
> management) is legally required to notify. For any ransom, legal **prepares** the case (lawfulness,
> international sanctions, insurer's position) and management **decides**.

## 3. Rules of use

1. **One A per row.** Two people "approving" together means, in practice, nobody.
2. **A deputy for every A**, named in advance in the [crisis directory (D02, §5)](D02-escalation.md#5-crisis-directory-to-be-completed).
   S1 incidents often break out on a Friday evening.
3. **Fit the size of the organisation**: in a small company, one person may hold several roles (for
   example CISO and CIO). Keep the rows, but write down the actual name.
4. **Replay the matrix** during every tabletop exercise: it is the best way to discover that a role
   is held by nobody.
