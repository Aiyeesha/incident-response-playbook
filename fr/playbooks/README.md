# Playbooks

[↑ Documentation](../README.md)

Chaque playbook suit la même structure en 8 sections : 1 Détection · 2 Triage · 3 Confinement ·
4 Preuves · 5 Éradication · 6 Restauration · 7 Obligations et communication · 8 Clôture,
suivies d'un arbre de décision et des techniques MITRE ATT&CK concernées.

| ID | Playbook | Gravité | Techniques MITRE ATT&CK |
|---|---|---|---|
| P01 | [Infection par logiciel malveillant](P01-logiciel-malveillant.md) | S1 – S3 | T1566.001, T1204.002, T1059.001, T1547.001, T1105, T1071.001 |
| P02 | [Attaque par rançongiciel](P02-rancongiciel.md) | S1 | T1133, T1078, T1003, T1021.001, T1685, T1490, T1567.002, T1486 |
| P03 | [Fuite de données](P03-fuite-de-donnees.md) | S1 – S2 | T1078, T1213, T1530, T1005, T1560, T1567.002, T1048, T1041 |

_Les playbooks P04 à P07 (hameçonnage, accès non autorisé, déni de service, compte compromis)
arrivent à l'étape 4._
