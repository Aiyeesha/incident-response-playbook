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
| P04 | [Hameçonnage](P04-hameconnage.md) | S2 – S4 | T1566.001, T1566.002, T1598.003, T1204.001, T1056.003 |
| P05 | [Accès non autorisé](P05-acces-non-autorise.md) | S1 – S3 | T1110.001, T1110.003, T1190, T1133, T1078.002, T1068, T1136, T1098 |
| P06 | [Déni de service](P06-deni-de-service.md) | S1 – S3 | T1498.001, T1498.002, T1499.002, T1499.003 |
| P07 | [Compte compromis et fraude au virement](P07-compte-compromis.md) | S1 – S2 | T1078.004, T1110.003, T1621, T1539, T1114.003, T1564.008, T1534, T1657 |

### Par où commencer ?

| Situation | Playbook |
|---|---|
| Courriel suspect reçu, lien cliqué | P04, puis P01 ou P07 selon ce qui s'est passé |
| Alerte antivirus ou EDR, programme suspect | P01 |
| Fichiers chiffrés, note de rançon | P02 |
| Données copiées, exposées ou publiées | P03 |
| Connexion d'un tiers à un serveur ou à l'annuaire | P05 |
| Service lent ou indisponible sous un afflux de trafic | P06 |
| Boîte de messagerie piratée, demande de virement ou de changement de RIB suspecte | P07 |
