---
id: P05
lang: fr
title: Accès non autorisé
severity: [S1, S2, S3]
mitre: [T1110.001, T1110.003, T1190, T1133, T1078.002, T1068, T1136, T1098]
owner: Responsable SOC
review: 2026-11-07
---

# P05 — Accès non autorisé

[↑ Playbooks](README.md)

**Quand l'utiliser :** une personne non autorisée a obtenu, ou tenté d'obtenir avec succès, un accès à
un système, un serveur ou un compte du **système d'information interne** (annuaire, serveurs,
applications exposées). Pour la prise de contrôle d'une boîte de messagerie ou d'un compte cloud
utilisée à des fins de fraude, utiliser le [P07 — Compte compromis](P07-compte-compromis.md).

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S3** pour un compte standard sans action suspecte ; **S2** pour un serveur ou un compte de service ; **S1** dès qu'un compte à privilèges est utilisé ou créé ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsable | Responsable SOC |
| Documents liés | [D02 — Escalade](../docs/D02-escalade.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Nombreux échecs de connexion sur un même compte (événement Windows 4625, `Failed password` dans `auth.log`) | Annuaire, serveurs, SIEM | T1110.001 |
| Une même adresse qui échoue sur **beaucoup de comptes différents** avec peu d'essais chacun | Annuaire, portail, SIEM | T1110.003 |
| Exploitation d'une application exposée (erreurs, requêtes anormales, fichier inconnu déposé sur le serveur web) | Pare-feu applicatif, journaux web | T1190 |
| Connexion VPN ou accès distant inhabituel (pays, horaire, appareil) | VPN, passerelle d'accès | T1133 |
| Compte du domaine utilisé sur des machines inhabituelles, ou ouverture de session à privilèges (événement 4672) | Annuaire, SIEM | T1078.002 |
| Exploitation d'une vulnérabilité locale pour devenir administrateur | EDR | T1068 |
| Création de compte (4720) ou ajout à un groupe à privilèges (4728, 4732, 4756) | Annuaire, SIEM | T1136, T1098 |

## 2. Triage

- [ ] Ouvrir le dossier et noter l'heure de détection (UTC)
- [ ] Confirmer l'accès **réussi** : un échec seul relève d'une tentative (S4), un succès après des échecs est un incident
- [ ] Identifier le compte, la source (adresse IP, appareil), la cible et la chronologie de la première connexion réussie
- [ ] Vérifier auprès du titulaire du compte, **par téléphone**, s'il est à l'origine de l'accès
- [ ] Rechercher les actions faites avec ce compte : connexions à d'autres machines, création de comptes, changement de droits, accès aux données
- [ ] Qualifier la gravité ([D01](../docs/D01-gravite-et-delais.md)) : tout compte à privilèges impliqué = S1 et escalade immédiate ([D02](../docs/D02-escalade.md))

## 3. Confinement

- [ ] Désactiver le compte utilisé (ou forcer la réinitialisation) et **révoquer ses sessions** ; désactiver les comptes créés par l'attaquant
- [ ] Bloquer l'adresse IP source (pare-feu, VPN, pare-feu applicatif) et, si besoin, l'accès distant concerné
- [ ] Isoler les serveurs ou postes sur lesquels l'attaquant s'est connecté, sans les éteindre
- [ ] Si une application exposée a été exploitée : la retirer d'Internet ou appliquer une mesure de contournement en attendant le correctif
- [ ] Si un compte à privilèges est compromis : traiter comme un incident **S1**, avec réinitialisation des comptes à privilèges (voir aussi le [P02](P02-rancongiciel.md), section 3)

## 4. Preuves

- [ ] Exporter les journaux d'authentification de l'annuaire, du VPN, des serveurs et des applications, sur toute la période suspecte
- [ ] Capturer la mémoire puis faire une image des serveurs compromis ([D05](../docs/D05-preservation-des-preuves.md))
- [ ] Conserver les fichiers déposés par l'attaquant (outils, porte dérobée web) et leur empreinte SHA-256
- [ ] Tenir la chaîne de custody

## 5. Éradication

- [ ] Fermer la porte d'entrée : correctif de la vulnérabilité, authentification multifacteur sur l'accès distant, mot de passe faible remplacé
- [ ] Supprimer les comptes, groupes, droits, tâches et outils ajoutés par l'attaquant
- [ ] Réinitialiser les mots de passe de tous les comptes utilisés ou exposés
- [ ] Reconstruire les serveurs compromis à partir d'images saines

## 6. Restauration

- [ ] Remettre en service les systèmes reconstruits, sous surveillance renforcée pendant au moins 30 jours
- [ ] Réactiver les comptes légitimes avec un nouveau mot de passe et l'authentification multifacteur
- [ ] Ajouter des règles de détection ciblées (connexions depuis la même source, mêmes outils, même comportement)

## 7. Obligations et communication

- [ ] Si des données personnelles ont pu être consultées : associer le DPO et évaluer la notification à la CNIL ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Entités NIS 2 : évaluer s'il s'agit d'un incident important ([D04](../docs/D04-cadre-reglementaire.md), §3)
- [ ] Porter plainte (accès frauduleux à un système, article 323-1 du Code pénal), sous 72 heures si l'organisation veut être indemnisée par son assurance ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] Informer le titulaire du compte et son responsable

## 8. Clôture

- [ ] La porte d'entrée est fermée, et l'attaquant n'a plus aucun accès vérifiable (comptes, sessions, portes dérobées)
- [ ] Aucune nouvelle connexion suspecte pendant la période de surveillance
- [ ] Les obligations de la section 7 sont remplies ou formellement écartées
- [ ] Rapport d'incident et retour d'expérience réalisés ; correctifs et mesures de durcissement suivis

## Arbre de décision

```text
Accès suspect
  │
  ├─ Échecs seulement, aucun succès ? ── OUI → tentative (S4) : bloquer la source, surveiller
  │
  └─ Accès réussi
        │
        ├─ Le titulaire confirme (par téléphone) être à l'origine ? ── OUI → faux positif, consigner
        │
        └─ NON → désactiver le compte, révoquer les sessions, bloquer la source
                  │
                  ├─ Compte à privilèges utilisé ou créé ? ── OUI → S1, escalade immédiate
                  ├─ Serveur ou application exposée ?       ── OUI → S2, isoler, corriger
                  └─ Compte standard, aucune action         ──     → S3
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1110.001](https://attack.mitre.org/techniques/T1110/001/) | Brute Force: Password Guessing | Annuaire, journaux d'authentification |
| [T1110.003](https://attack.mitre.org/techniques/T1110/003/) | Brute Force: Password Spraying | Annuaire, portails |
| [T1190](https://attack.mitre.org/techniques/T1190/) | Exploit Public-Facing Application | Pare-feu applicatif, journaux web |
| [T1133](https://attack.mitre.org/techniques/T1133/) | External Remote Services | VPN, passerelle d'accès |
| [T1078.002](https://attack.mitre.org/techniques/T1078/002/) | Valid Accounts: Domain Accounts | Annuaire, SIEM |
| [T1068](https://attack.mitre.org/techniques/T1068/) | Exploitation for Privilege Escalation | EDR |
| [T1136](https://attack.mitre.org/techniques/T1136/) | Create Account | Annuaire (événement 4720) |
| [T1098](https://attack.mitre.org/techniques/T1098/) | Account Manipulation | Annuaire (événements 4728, 4732, 4756) |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
