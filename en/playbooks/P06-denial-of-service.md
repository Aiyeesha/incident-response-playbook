---
id: P06
lang: en
title: Denial of service
severity: [S1, S2, S3]
mitre: [T1498.001, T1498.002, T1499.002, T1499.003]
owner: SOC lead and network lead
review: 2026-11-07
---

# P06 — Denial of service

[↑ Playbooks](README.md)

**When to use it:** a service (website, application, Internet access, VPN) becomes slow or unavailable
because it is **flooded with requests or traffic**. A distributed denial-of-service (DDoS) attack comes
from thousands of machines at once; it is sometimes also used as a **diversion** during another
intrusion.

| Item | Value |
|---|---|
| Usual severity | **S3** if a secondary service slows down; **S2** if an important service is degraded; **S1** if an essential service or the company's Internet access is down ([D01](../docs/D01-severity-and-timelines.md)) |
| Owners | SOC lead and network lead; hosting provider and ISP in support |
| Related documents | [D02 — Escalation](../docs/D02-escalation.md) · [D04 — Regulatory context](../docs/D04-regulatory-context.md) |

> 📞 **To prepare before the incident:** the emergency contacts of the hosting provider, the ISP and
> the anti-DDoS protection service, with the procedure to activate protection, belong in the
> [crisis directory (D02, §5)](../docs/D02-escalation.md#5-crisis-directory-to-be-completed). During
> the attack, it is too late to look for them.

## 1. Detection

| Signal | Usual source | Technique |
|---|---|---|
| Internet link saturated, surge in incoming packets | Network monitoring, ISP | T1498.001 |
| Large volume of unsolicited DNS, NTP or memcached responses (reflection and amplification attack) | Firewall, network monitoring | T1498.002 |
| Abnormal number of connections or requests per second on a service (SYN flood, HTTP requests) | Load balancer, firewall, web server | T1499.002 |
| Repeated requests to the most expensive pages or functions (search, login, export) | Web logs, web application firewall | T1499.003 |
| Availability alerts, complaints from customers or users | Monitoring, customer service | — |

## 2. Triage

- [ ] Confirm the attack and rule out a **legitimate cause**: expected traffic peak (sales campaign, press article), outage, faulty update
- [ ] Identify the target (IP address, service, page), the type of traffic (protocol, volume, number of sources) and the start time (UTC)
- [ ] Measure the business impact and rate the severity ([D01](../docs/D01-severity-and-timelines.md))
- [ ] Check that **another attack** is not running in parallel (unusual logons, EDR alerts): denial of service can hide an intrusion
- [ ] Look for a related ransom demand (email, social media message)

## 3. Containment

- [ ] Alert the **hosting provider** and the **ISP** and activate anti-DDoS protection (upstream filtering, traffic "scrubbing")
- [ ] Apply local measures: rate limiting per source, web application firewall rules, geo-blocking if the service has no legitimate users in those countries
- [ ] Enable caching or a static fallback page for the most requested pages
- [ ] Protect essential services first (employee access, payment, order taking)
- [ ] Do not answer any ransom demand: decision by management, prepared by legal ([D03](../docs/D03-raci-matrix.md))

## 4. Evidence

- [ ] Keep traffic samples (limited captures, flow logs) and the firewall, load balancer and web server logs
- [ ] Obtain the hosting provider's and ISP's records of the attack (volumes, sources, times)
- [ ] Keep any ransom demand or claim of responsibility, with its timestamp ([D05](../docs/D05-evidence-preservation.md))

## 5. Eradication

- [ ] Fix what made the service vulnerable: open DNS or NTP server used as an amplifier, expensive function without rate limiting, missing cache
- [ ] Keep the filtering rules in place while the attack may resume; attacks in waves are common
- [ ] Check that the company's own infrastructure is not taking part in attacks (compromised machines, open services)

## 6. Recovery

- [ ] Gradually lift emergency measures that hinder legitimate users (geo-blocking, fallback pages)
- [ ] Check that every service works and measure response times
- [ ] Monitor closely for at least 7 days: a new wave is frequent

## 7. Obligations and communication

- [ ] NIS 2 entities: a severe service outage is potentially a significant incident (early warning within 24 hours, [D04](../docs/D04-regulatory-context.md), §3)
- [ ] File a police complaint (hindering the operation of a system, article 323-2 of the French Penal Code), within 72 hours if the organisation wants insurance compensation ([D04](../docs/D04-regulatory-context.md), §4)
- [ ] Inform customers and users of the outage and its resolution, through the designated people ([D03](../docs/D03-raci-matrix.md))
- [ ] Check contractual availability commitments (towards customers, from the hosting provider)

## 8. Closure

- [ ] Traffic has been back to normal for at least 24 hours
- [ ] Services are restored and hindering emergency measures lifted
- [ ] No parallel intrusion was found, or it has its own case
- [ ] Complete incident report (duration, volumes, impact, actions) and lessons learned completed
- [ ] The anti-DDoS protection contract and the crisis directory are reviewed if needed

## Decision tree

```text
Service slow or unavailable
  │
  ├─ Legitimate cause (expected peak, outage, update)? ── YES → capacity or outage management
  │
  └─ NO → likely attack
            │
            ├─ Alert the hosting provider and ISP → activate anti-DDoS protection
            ├─ Local measures: rate limiting, filtering, cache, fallback page
            │
            ├─ Another attack in parallel? ── YES → open a separate case (P01, P05…)
            ├─ Ransom demand?              ── YES → do not answer, legal and management
            │
            └─ Essential service down? ── YES → S1, immediate escalation
                                        └─ NO  → S2 or S3 depending on impact
```

## MITRE ATT&CK techniques

| Technique | Name | Where to observe it |
|---|---|---|
| [T1498.001](https://attack.mitre.org/techniques/T1498/001/) | Network Denial of Service: Direct Network Flood | Network monitoring, ISP |
| [T1498.002](https://attack.mitre.org/techniques/T1498/002/) | Network Denial of Service: Reflection Amplification | Firewall, network monitoring |
| [T1499.002](https://attack.mitre.org/techniques/T1499/002/) | Endpoint Denial of Service: Service Exhaustion Flood | Load balancer, web server |
| [T1499.003](https://attack.mitre.org/techniques/T1499/003/) | Endpoint Denial of Service: Application Exhaustion Flood | Web logs, web application firewall |

Identifiers checked against MITRE ATT&CK Enterprise **v20.1**.
