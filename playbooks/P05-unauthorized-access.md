# P05 — Unauthorized Access

**Severity**: S2 High → S1 Critical (depending on account privilege)  
**Trigger**: SIEM alert, anomalous login, threat intel, user report  
**Owner**: SOC Analyst  

---

## 1. Detection & Initial Triage

- [ ] Identify the account(s) involved
- [ ] Determine access type: external (internet-facing), internal, privileged
- [ ] Check login source: IP, geolocation, device, time
- [ ] Determine what was accessed: systems, data, admin consoles
- [ ] Check if access is ongoing
- [ ] Escalate immediately if account is privileged (admin, domain admin, service account)

## 2. Containment

- [ ] **Disable the compromised account** in Active Directory / IdP
- [ ] **Revoke all active sessions** and API tokens
- [ ] **Terminate active connections** (VPN, RDP, SSH, web sessions)
- [ ] Block the source IP at firewall
- [ ] Preserve all authentication logs (do not purge)
- [ ] Notify the legitimate account owner

## 3. Investigation

- [ ] Reconstruct attacker's timeline from authentication logs
- [ ] Identify all systems and data accessed
- [ ] Check for persistence (new accounts created, SSH keys added, scheduled tasks)
- [ ] Review privilege changes made during unauthorized access
- [ ] Check for data exfiltration (DLP, firewall outbound, cloud storage logs)
- [ ] Determine initial access vector:
  - Credential stuffing / brute force
  - Phishing (link with [P04](./P04-phishing-attack.md))
  - Insider threat
  - Third-party compromise
  - Stolen token / session hijacking

## 4. Eradication

- [ ] Reset all credentials for the compromised account
- [ ] Force password reset for accounts with shared credentials
- [ ] Revoke and reissue API keys, certificates, SSH keys
- [ ] Remove attacker-created accounts, backdoors, persistence
- [ ] Patch vulnerability used for initial access
- [ ] Enforce MFA on the account and review MFA bypass settings

## 5. Recovery

- [ ] Re-enable account after full credential reset and MFA enrollment
- [ ] Review and tighten access permissions (least privilege)
- [ ] Enable enhanced monitoring on the account for 30 days
- [ ] Review and revoke excessive standing privileges (JIT access consideration)

## 6. Post-Incident

- [ ] Complete [incident report](../templates/incident-report.md)
- [ ] Review identity governance: stale accounts, excessive permissions
- [ ] Verify MFA enrollment coverage across all privileged accounts
- [ ] Conduct [post-mortem](../templates/post-mortem.md)

---

## Privileged Account Compromise — Extra Steps

If a **domain admin**, **global admin**, or **service account** was compromised:

- [ ] Assume full domain/tenant compromise — treat as S1
- [ ] Reset **krbtgt** account password **twice** (24h apart) to invalidate Kerberos tickets
- [ ] Review all GPOs for unauthorized changes
- [ ] Audit all admin group memberships
- [ ] Check Azure AD / Entra ID for new conditional access policies, new MFA methods
- [ ] Consider engaging an external IR firm
