---
id: P03
lang: fr
title: Fuite de données
severity: [S1, S2]
mitre: [T1078, T1213, T1530, T1005, T1560, T1567.002, T1048, T1041]
owner: Responsable SOC et DPO
review: 2026-11-07
---

# P03 — Fuite de données

[↑ Playbooks](README.md)

**Quand l'utiliser :** des données confidentielles ou personnelles ont été, ou ont pu être,
**consultées, copiées ou divulguées** par une personne non autorisée : vol par un attaquant, export
par un salarié, partage public par erreur, base de données exposée sur Internet, données retrouvées
sur un site de fuite.

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S2** ; **S1** si des données sensibles ou personnelles sont touchées à grande échelle ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsables | Responsable SOC (investigation) et DPO (évaluation de la violation) |
| Documents liés | [D03 — RACI](../docs/D03-matrice-raci.md) · [D04 — Cadre réglementaire](../docs/D04-cadre-reglementaire.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

> ⏱️ **Le délai de 72 heures pour la CNIL court dès que l'organisation a connaissance de la
> violation**, pas à la fin de l'enquête. Le DPO est prévenu **dès l'ouverture** du dossier, et une
> notification initiale incomplète vaut mieux qu'une notification tardive
> ([D04](../docs/D04-cadre-reglementaire.md), §2).

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Compte valide qui consulte un volume inhabituel de documents, ou à une heure inhabituelle | Annuaire, journaux d'accès, outil de prévention des fuites (DLP) | T1078, T1213 |
| Téléchargements massifs depuis un espace de stockage cloud (SharePoint, OneDrive, compartiment S3…) | Journaux d'audit cloud | T1530 |
| Collecte de fichiers locaux puis création d'archives (`.zip`, `.7z`, `.rar`) volumineuses | EDR | T1005, T1560 |
| Envoi vers un service de stockage personnel ou de partage de fichiers | Proxy, DLP, pare-feu | T1567.002 |
| Flux sortant inhabituel par un autre protocole (FTP, DNS, SMTP) | Pare-feu, DNS | T1048 |
| Volume sortant élevé vers l'adresse de commande d'un logiciel malveillant | Pare-feu, EDR | T1041 |
| Données de l'entreprise retrouvées en ligne, signalement par un client, un chercheur ou un journaliste | Veille, signalement externe | — |

## 2. Triage

- [ ] Ouvrir le dossier, noter l'heure de **prise de connaissance** (UTC) : c'est le point de départ des délais légaux
- [ ] Prévenir le **DPO** et le juridique immédiatement ([D02](../docs/D02-escalade.md), déclencheurs d'escalade)
- [ ] Déterminer **quelles données** : catégories (identité, coordonnées, données bancaires, santé, identifiants), volume approximatif, personnes concernées (clients, salariés, mineurs ?)
- [ ] Déterminer **comment** : attaque externe, erreur de configuration, action d'un salarié, prestataire
- [ ] Déterminer **si la fuite continue** : accès toujours ouvert, compte toujours actif, lien de partage toujours public
- [ ] Qualifier la gravité ([D01](../docs/D01-gravite-et-delais.md)) : données sensibles à grande échelle = S1

## 3. Confinement

- [ ] Fermer la source : supprimer le lien public, restreindre le compartiment cloud, couper l'accès exposé
- [ ] Désactiver ou réinitialiser les comptes utilisés pour la fuite et révoquer leurs sessions et jetons d'accès
- [ ] Bloquer les destinations d'exfiltration identifiées (domaines, adresses IP, services de stockage)
- [ ] S'il s'agit d'un salarié : associer le juridique et les ressources humaines **avant** toute action visible, pour respecter le droit du travail et ne pas compromettre l'enquête
- [ ] Demander le retrait des données publiées (hébergeur, plateforme) avec l'aide du juridique

## 4. Preuves

- [ ] Exporter les journaux d'accès et d'audit couvrant toute la période suspecte (annuaire, cloud, applications, proxy, DLP)
- [ ] Conserver une copie des données exposées **telles qu'elles ont fuité**, dans un espace chiffré et à accès restreint, pour mesurer l'étendue
- [ ] Faire des captures horodatées des publications en ligne (page, URL, date), sans interagir avec les auteurs
- [ ] Tenir la chaîne de custody ([D05](../docs/D05-preservation-des-preuves.md))

## 5. Éradication

- [ ] Corriger la cause : configuration du stockage, droits excessifs, vulnérabilité exploitée, absence d'authentification multifacteur
- [ ] Si un logiciel malveillant est en cause : traiter selon le [P01](P01-logiciel-malveillant.md)
- [ ] Réinitialiser tous les secrets exposés dans les données (mots de passe, clés d'API, jetons, certificats)
- [ ] Revoir les droits d'accès aux données concernées (principe du moindre privilège)

## 6. Restauration

- [ ] Rouvrir les accès légitimes avec les nouveaux contrôles en place
- [ ] Mettre en place une surveillance renforcée des accès aux données concernées (règle DLP ou SIEM dédiée)
- [ ] Vérifier régulièrement si les données réapparaissent en ligne (veille) pendant plusieurs semaines

## 7. Obligations et communication

- [ ] Inscrire la violation au **registre des violations**, même si elle n'est pas notifiée ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Si la violation présente un risque pour les personnes : **notifier la CNIL** dans les 72 heures, en plusieurs temps si nécessaire
- [ ] Si le risque est **élevé** : informer les personnes concernées dans les meilleurs délais, avec des conseils concrets (changer de mot de passe, se méfier des appels frauduleux…)
- [ ] Entités NIS 2 : évaluer s'il s'agit d'un incident important et respecter les délais de 24 heures, 72 heures et 1 mois ([D04](../docs/D04-cadre-reglementaire.md), §3)
- [ ] En cas d'acte malveillant : porter plainte, sous 72 heures si l'organisation veut être indemnisée par son assurance ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] Prévenir les clients ou partenaires contractuellement concernés (clauses de notification des contrats)

## 8. Clôture

- [ ] La source de la fuite est fermée et la cause corrigée
- [ ] La notification CNIL est complète (notification complémentaire envoyée si besoin) ou la décision de ne pas notifier est **justifiée et documentée**
- [ ] Les personnes concernées ont été informées si le risque est élevé
- [ ] Le registre des violations et le rapport d'incident sont à jour
- [ ] Retour d'expérience tenu ; mesures de prévention suivies (classification des données, DLP, revue des droits)

## Arbre de décision

```text
Fuite de données suspectée
  │
  ├─ Prévenir le DPO tout de suite → l'horloge des 72 heures tourne
  │
  ├─ La fuite continue-t-elle ? ── OUI → fermer la source en priorité
  │
  ├─ Des données personnelles sont-elles concernées ?
  │     ├─ NON → incident de confidentialité : investigation, plainte si acte malveillant
  │     └─ OUI → inscrire au registre des violations
  │               │
  │               ├─ Risque pour les personnes ? ── NON → documenter la justification
  │               └─ OUI → notifier la CNIL sous 72 heures
  │                         │
  │                         └─ Risque élevé ? ── OUI → informer les personnes concernées
  │
  └─ Origine malveillante ? ── OUI → plainte (sous 72 heures pour l'assurance)
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1078](https://attack.mitre.org/techniques/T1078/) | Valid Accounts | Annuaire, journaux d'accès |
| [T1213](https://attack.mitre.org/techniques/T1213/) | Data from Information Repositories | Journaux d'audit (SharePoint, wiki, outils métier) |
| [T1530](https://attack.mitre.org/techniques/T1530/) | Data from Cloud Storage | Journaux d'audit cloud |
| [T1005](https://attack.mitre.org/techniques/T1005/) | Data from Local System | EDR |
| [T1560](https://attack.mitre.org/techniques/T1560/) | Archive Collected Data | EDR |
| [T1567.002](https://attack.mitre.org/techniques/T1567/002/) | Exfiltration to Cloud Storage | Proxy, DLP |
| [T1048](https://attack.mitre.org/techniques/T1048/) | Exfiltration Over Alternative Protocol | Pare-feu, DNS |
| [T1041](https://attack.mitre.org/techniques/T1041/) | Exfiltration Over C2 Channel | Pare-feu, EDR |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
