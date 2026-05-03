# P03 — Data Breach

**Severity**: S1 Critical (PII / financial data) or S2 High  
**Trigger**: DLP alert, unusual data transfer, employee report, external notification  
**Owner**: SOC Analyst + Legal + DPO  

---

## 1. Detection & Initial Triage

- [ ] Confirm data was actually accessed or exfiltrated (not just attempted)
- [ ] Identify **what data** was accessed (PII, financial, IP, health data?)
- [ ] Identify **how much** data (number of records, file sizes)
- [ ] Identify **who** accessed it (internal user, external attacker, third party?)
- [ ] Identify **when** it started and whether exfiltration is ongoing
- [ ] Immediately notify Legal and DPO if PII is involved

## 2. Containment

- [ ] Revoke access for the compromised account or third party
- [ ] Terminate active sessions (VPN, web app, API tokens)
- [ ] Block exfiltration channel (IP, domain, upload service)
- [ ] Change credentials for affected accounts
- [ ] Enable enhanced logging on affected systems
- [ ] Preserve all relevant logs (do not delete or rotate)

## 3. Investigation

- [ ] Reconstruct the full timeline of data access
- [ ] Enumerate all data repositories accessed
- [ ] Identify all exfiltration vectors (USB, email, cloud upload, API)
- [ ] Check for persistence (backdoor, scheduled task, OAuth token)
- [ ] Determine if attacker still has access
- [ ] Collect and preserve evidence: logs, PCAP, memory dump

## 4. Notification Requirements

### Internal

- [ ] Notify Management within 1 hour
- [ ] Notify Legal + DPO if personal data involved
- [ ] Notify affected business unit managers

### Regulatory (if PII / sensitive data)

| Regulation | Deadline | Action |
|------------|----------|--------|
| GDPR | 72 hours from discovery | Notify supervisory authority (CNIL in France) |
| GDPR | Without undue delay | Notify affected individuals if high risk |
| NIS2 | 24 hours | Early warning to competent authority |
| Sector-specific | Varies | Check applicable regulations |

### External

- [ ] Prepare customer/partner notification with Legal approval
- [ ] Prepare press statement if breach may become public
- [ ] Set up a dedicated response mailbox for affected individuals

## 5. Eradication & Recovery

- [ ] Revoke all compromised credentials and API tokens
- [ ] Patch the vulnerability exploited for initial access
- [ ] Review and tighten data access controls (least privilege)
- [ ] Enable MFA on all accounts that lacked it
- [ ] Review DLP rules and tighten alert thresholds

## 6. Post-Incident

- [ ] Complete [incident report](../templates/incident-report.md)
- [ ] Conduct [post-mortem](../templates/post-mortem.md)
- [ ] Review data classification policy
- [ ] Conduct privacy impact assessment if required
- [ ] Implement additional monitoring on sensitive data repositories
