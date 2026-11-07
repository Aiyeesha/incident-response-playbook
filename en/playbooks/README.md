# Playbooks

[↑ Documentation](../README.md)

Every playbook follows the same 8-section structure: 1 Detection · 2 Triage · 3 Containment ·
4 Evidence · 5 Eradication · 6 Recovery · 7 Obligations and communication · 8 Closure,
followed by a decision tree and the relevant MITRE ATT&CK techniques.

| ID | Playbook | Severity | MITRE ATT&CK techniques |
|---|---|---|---|
| P01 | [Malware infection](P01-malware.md) | S1 – S3 | T1566.001, T1204.002, T1059.001, T1547.001, T1105, T1071.001 |
| P02 | [Ransomware attack](P02-ransomware.md) | S1 | T1133, T1078, T1003, T1021.001, T1685, T1490, T1567.002, T1486 |
| P03 | [Data breach](P03-data-breach.md) | S1 – S2 | T1078, T1213, T1530, T1005, T1560, T1567.002, T1048, T1041 |
| P04 | [Phishing](P04-phishing.md) | S2 – S4 | T1566.001, T1566.002, T1598.003, T1204.001, T1056.003 |
| P05 | [Unauthorised access](P05-unauthorised-access.md) | S1 – S3 | T1110.001, T1110.003, T1190, T1133, T1078.002, T1068, T1136, T1098 |
| P06 | [Denial of service](P06-denial-of-service.md) | S1 – S3 | T1498.001, T1498.002, T1499.002, T1499.003 |
| P07 | [Compromised account and payment fraud](P07-compromised-account.md) | S1 – S2 | T1078.004, T1110.003, T1621, T1539, T1114.003, T1564.008, T1534, T1657 |

### Where to start?

| Situation | Playbook |
|---|---|
| Suspicious email received, link clicked | P04, then P01 or P07 depending on what happened |
| Antivirus or EDR alert, suspicious program | P01 |
| Encrypted files, ransom note | P02 |
| Data copied, exposed or published | P03 |
| Third party logged on to a server or the directory | P05 |
| Service slow or down under a traffic surge | P06 |
| Hacked mailbox, suspicious transfer or bank-detail change request | P07 |
