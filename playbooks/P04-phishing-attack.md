# P04 — Phishing Attack

**Severity**: S4 Low (no click) → S2 High (credentials harvested) → S1 Critical (payload executed)  
**Trigger**: User report, email gateway alert, SIEM correlation  
**Owner**: SOC Analyst  

---

## 1. Detection & Initial Triage

- [ ] Obtain original email (with headers) — ask user NOT to delete it
- [ ] Identify: sender address, display name, sending IP, subject
- [ ] Check: was the link clicked? Was an attachment opened? Were credentials entered?
- [ ] Identify all recipients of the same campaign
- [ ] Assign severity based on user actions taken

## 2. Containment

### Email Not Clicked (S4)

- [ ] Block sender domain/IP at email gateway
- [ ] Purge email from all mailboxes (M365: Content Search + Purge)
- [ ] Add URL/domain to proxy/DNS blacklist
- [ ] No further action unless more recipients found

### Link Clicked / Credentials Entered (S2+)

- [ ] **Immediately reset** compromised user's password
- [ ] **Revoke all sessions** and OAuth tokens for the account
- [ ] **Enable MFA** if not already active
- [ ] Check for inbox rules created by attacker (email forwarding)
- [ ] Review account for suspicious activity (sent mail, downloads, sign-ins)
- [ ] Notify user's manager

### Payload Executed (S1 — treat as Malware / P01)

- [ ] Follow [P01 Malware Infection playbook](./P01-malware-infection.md) in parallel
- [ ] Isolate host immediately

## 3. Investigation

- [ ] Extract IOCs from email: URLs, hashes, IPs, domains
- [ ] Check threat intel: VirusTotal, URLscan.io, PhishTank
- [ ] Search all mailboxes for the same campaign
- [ ] Review authentication logs for account takeover indicators
- [ ] Check if credentials were used after phishing (SIEM correlation)

## 4. Eradication

- [ ] Purge all phishing emails organization-wide
- [ ] Block all IOCs at firewall, DNS, email gateway
- [ ] Reset credentials for all users who entered data on phishing site
- [ ] Invalidate active sessions for affected accounts

## 5. Recovery

- [ ] Restore any mailbox rules deleted or modified by attacker
- [ ] Re-enable account after credential reset and MFA enrollment
- [ ] Monitor account for 7 days

## 6. Post-Incident

- [ ] Complete [incident report](../templates/incident-report.md)
- [ ] Send targeted security awareness communication to affected users
- [ ] Run a phishing simulation within 30 days to measure improvement
- [ ] Review email gateway rules and update blocklists

---

## Phishing Indicators Checklist

| Indicator | Where to Check |
|-----------|---------------|
| Sender domain mismatch | Email headers |
| Lookalike domain (paypa1.com) | WHOIS, registration date |
| Urgency / fear language | Email body |
| Unexpected attachment | Email |
| Credential harvest page | URLscan.io |
| Login from unusual location | Azure AD / Okta sign-in logs |
| New inbox forwarding rule | Exchange admin center |
