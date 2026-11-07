---
id: T02
lang: en
title: Post-mortem
review: 2026-11-07
---

# T02 — Post-mortem

[↑ Templates](README.md)

> 🤝 **Principle: blameless.** The post-mortem looks for what, in tools, procedures and organisation,
> allowed the incident or slowed the response. A person who clicked a link is not "the cause": the
> cause is the missing filtering, multi-factor authentication or detection that should have caught
> that click. Without this principle, mistakes stop being reported and the team stops improving.

**When:** within the timelines set by [D01](../docs/D01-severity-and-timelines.md) (within 5 business
days for an S1). **Duration:** 60 to 90 minutes. **Participants:** the people who held a role in the
[RACI](../docs/D03-raci-matrix.md) during the incident, and a facilitator who was not involved if
possible.

## 1. Summary

| Field | Value |
|---|---|
| Incident reference | `INC-YYYY-NNN` ([T01](T01-incident-report.md)) |
| Highest severity reached | S_ |
| Duration (detection → recovery) | |
| Impact (business, data, estimated costs) | |
| In one sentence: what happened? | |

## 2. Timeline

Take the time markers from the incident report and add what was missing: **when did the attack really
start, and why was it not seen earlier?**

| Date and time (UTC) | Event | Could it have been detected? With what? |
|---|---|---|
| | | |

## 3. What went well

-
-

## 4. What went less well

-
-

## 5. Root causes

"5 whys" method: start from the observed fact and ask "why?" until reaching a cause the organisation
can act on.

| Level | Question | Answer |
|---|---|---|
| 1 | Why could the attacker get in? | |
| 2 | Why? | |
| 3 | Why? | |
| 4 | Why? | |
| 5 | Why? | |

## 6. Action plan

Each action has **a single owner**, a **due date** and a **verifiable completion criterion**.

| No. | Action | Owner | Due date | Completion criterion | Status |
|---|---|---|---|---|---|
| 1 | | | | | To do |

## 7. Documentation updates

- [ ] Do the playbooks involved need fixing? (which ones, what)
- [ ] Do the RACI matrix, crisis directory or timelines ([D01](../docs/D01-severity-and-timelines.md), [D02](../docs/D02-escalation.md), [D03](../docs/D03-raci-matrix.md)) need reviewing?
- [ ] Should new detection rules be created?
- [ ] Should a tabletop exercise ([D06](../docs/D06-tabletop-exercise.md)) replay this scenario?
