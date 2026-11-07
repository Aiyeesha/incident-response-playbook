---
id: T03
lang: en
title: Crisis communication
review: 2026-11-07
---

# T03 — Crisis communication

[↑ Templates](README.md)

Message templates to adapt, so that nothing has to be written from scratch under pressure. Only the
people designated in the [RACI](../docs/D03-raci-matrix.md) send these messages, after approval by
management and, for external messages, by legal.

> ✍️ **Writing rules**
> - Say **what is known**, what is **not known yet**, what is **being done**, and **when** you will
>   update the recipients.
> - Never speculate about the attacker, never downplay ("minor incident") before you are sure.
> - Do not give technical details useful to an attacker (systems not affected, weaknesses).
> - If email is compromised, send from a safe channel ([D02](../docs/D02-escalation.md), §4).

## M1 — Internal alert (employees)

> **Subject: IT incident in progress — instructions**
>
> Hello everyone,
>
> Since [time], we have been dealing with an IT security incident affecting [scope: email, file server,
> some workstations…]. Our teams and [provider, if any] are working on it.
>
> **Until further notice:**
> - [do not switch off your computer / disconnect your computer from the network];
> - do not use [affected service];
> - report any abnormal behaviour to [service desk phone number];
> - do **not** share any information about this incident outside the company, including on social
>   media; redirect any external question to [designated person].
>
> Next update: [date and time], via [channel].
>
> [Name, role]

## M2 — Customers and partners

> **Subject: Information about a security incident**
>
> Dear Sir or Madam,
>
> On [date], [company name] detected an IT security incident affecting [services concerned]. We
> immediately [measures: isolated systems, brought in experts, informed the competent authorities].
>
> At this stage, [what is known of the impact for the recipient: service unavailable, data concerned
> or not]. Our investigation is ongoing.
>
> **As a precaution:** any request from us to change bank details or make an unusual payment must be
> verified by phone on [number already known].
>
> We will get back to you by [date] at the latest. For any question: [dedicated contact].
>
> [Name, role]

## M3 — Informing people affected by a personal data breach (GDPR, article 34)

This message is **mandatory when the risk to individuals is high** ([D04](../docs/D04-regulatory-context.md),
§2). It must be written in **clear and plain language** and contain at least: the nature of the
breach, the contact details of the data protection officer, the likely consequences and the measures
taken or proposed.

> **Subject: Important information about your personal data**
>
> Dear Sir or Madam,
>
> **What happened.** On [date], we discovered that [plain description: a third party may have
> accessed…].
>
> **The data concerned.** [Precise list: name, email address, phone number…]. [Not concerned: …].
>
> **The risks for you.** [Concrete examples: fraudulent emails or calls pretending to be us, identity
> theft attempt…].
>
> **What we have done.** [Measures: access closed, passwords reset, authorities informed, complaint
> filed].
>
> **What we advise you to do.** [Concrete actions: change your password on our service and on any
> service where you used the same one; be wary of messages asking for your bank details; …]. We will
> **never** ask for your password.
>
> **For any question**, our data protection officer can be reached at [dedicated address or form].
> You may also lodge a complaint with the data protection authority (the CNIL in France).
>
> [Name, role]

## M4 — Press statement

> On [date], [company name] detected a cybersecurity incident affecting [general scope]. As soon as it
> was detected, our teams took the necessary measures to [contain the incident and protect our
> customers], with the support of [provider / authorities]. [The competent authorities have been
> informed and a complaint has been filed.]
>
> [Impact on customers: services restored / being restored, data concerned or not at this stage.]
> The investigation is ongoing; we will communicate again as soon as we have verified information.
>
> Press contact: [name, phone, address].

## Communication log

| Date and time (UTC) | Message (M1 to M4) | Recipients | Channel | Approved by | Sent by |
|---|---|---|---|---|---|
| | | | | | |
