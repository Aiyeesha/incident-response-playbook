# P02 — Ransomware Attack

**Severity**: S1 Critical (always)  
**Trigger**: Ransom note displayed, mass file encryption, EDR alert  
**Owner**: SOC Lead + CISO  

> **Do NOT reboot infected systems** — doing so may destroy forensic evidence or trigger additional encryption stages.

---

## 1. Detection & Initial Triage

- [ ] Confirm ransomware: ransom note present? Files renamed with unknown extension?
- [ ] Identify patient zero: first infected host, user, and timeline
- [ ] Identify ransomware family if possible (e.g. LockBit, Cl0p, BlackCat)
- [ ] Determine blast radius: how many hosts / shares are affected?
- [ ] Immediately escalate to SOC Lead and CISO — this is always S1

## 2. Containment (Priority #1 — Act Within Minutes)

- [ ] **Isolate ALL infected hosts** from the network simultaneously
  - EDR network isolation (fastest)
  - VLAN quarantine at switch level
  - Disconnect physical network cables if needed
- [ ] **Disable shared drives and file server access** to stop encryption spread
- [ ] **Revoke all active sessions** (VPN, RDP, Citrix) for affected users
- [ ] **Block C2 infrastructure** at firewall (IP, domain) — check threat intel feeds
- [ ] **Disable compromised accounts** — especially privileged accounts
- [ ] **Do NOT pay ransom** without explicit authorization from Management + Legal

## 3. Assess Backup Integrity

- [ ] Identify last known clean backup for all affected systems
- [ ] Verify backups are **not encrypted** (check Acronis, Veeam, or NAS)
- [ ] Isolate backup infrastructure from production network immediately
- [ ] Check if cloud backups (Acronis Cloud, Azure Backup) are intact
- [ ] Estimate data loss (RPO gap between last backup and encryption time)

## 4. Eradication

- [ ] Re-image all infected hosts (do not attempt to decrypt in-place)
- [ ] Identify and patch the initial access vector:
  - Phishing → user training + mail gateway rule
  - RDP exposure → disable or move behind VPN, enable NLA
  - Vulnerable software → apply patch immediately
- [ ] Reset ALL domain credentials (assume full credential compromise)
- [ ] Audit privileged accounts — remove unnecessary admin rights
- [ ] Scan all remaining hosts for persistence mechanisms

## 5. Recovery

- [ ] Restore systems in priority order (critical servers first)
- [ ] Restore from last clean backup — validate integrity before reconnecting
- [ ] Re-deploy endpoints via Windows Autopilot or WDS
- [ ] Reconnect systems to network in monitored segments
- [ ] Monitor for 7 days — ransomware actors often maintain persistence

## 6. Legal & Regulatory

- [ ] Notify legal team immediately (ransomware = likely data breach)
- [ ] GDPR: if PII affected, notify DPA within 72 hours
- [ ] Preserve all evidence for potential law enforcement (do not wipe disks yet)
- [ ] Do NOT communicate publicly without legal + management approval
- [ ] Consider engaging a specialized IR firm for large-scale incidents

## 7. Post-Incident

- [ ] Complete [incident report](../templates/incident-report.md)
- [ ] Conduct [post-mortem](../templates/post-mortem.md) within 48 hours of recovery
- [ ] Review and harden backup strategy (immutable backups, 3-2-1 rule)
- [ ] Implement or review EDR, email filtering, network segmentation

---

## Ransomware Response Decision Tree

```
Encrypted files detected?
  ├─ YES → Isolate immediately → Check backups → Eradicate → Restore
  └─ NO (only ransom note) → Isolate → Forensic investigation → May still restore

Backups intact?
  ├─ YES → Restore from backup (preferred path)
  └─ NO → Consult Legal on decryption options / negotiate (last resort)
```
