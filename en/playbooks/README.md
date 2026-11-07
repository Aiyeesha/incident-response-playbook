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

_Playbooks P04 to P07 (phishing, unauthorised access, denial of service, compromised account) land in
step 4._
