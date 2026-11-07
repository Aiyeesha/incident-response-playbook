---
id: P01
lang: fr
title: Infection par logiciel malveillant
severity: [S1, S2, S3]
mitre: [T1566.001, T1204.002, T1059.001, T1547.001, T1105, T1071.001]
owner: Responsable SOC
review: 2026-11-07
---

# P01 — Infection par logiciel malveillant

[↑ Playbooks](README.md)

**Quand l'utiliser :** un poste ou un serveur exécute, ou a exécuté, un programme malveillant
(cheval de Troie, voleur d'identifiants, porte dérobée, chargeur…), **sans chiffrement massif de
fichiers**. Si des fichiers sont chiffrés ou qu'une note de rançon apparaît, passer immédiatement au
[P02 — Rançongiciel](P02-rancongiciel.md).

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S3** pour un poste isolé ; **S2** si plusieurs postes ou un serveur ; **S1** si un compte à privilèges est compromis ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsable | Responsable SOC |
| Documents liés | [D02 — Escalade](../docs/D02-escalade.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Pièce jointe Office ou archive ouverte depuis la messagerie, suivie d'un processus inhabituel | Passerelle de messagerie, EDR | T1566.001, T1204.002 |
| PowerShell lancé par Word, Excel ou le navigateur, ligne de commande encodée (`-enc`) | EDR, journaux PowerShell (événement 4104) | T1059.001 |
| Nouvelle valeur dans une clé `Run` du registre ou un raccourci dans le dossier Démarrage | EDR, Sysmon (événements 12 à 14) | T1547.001 |
| Téléchargement d'un exécutable par un processus système (`certutil`, `bitsadmin`, `curl`) | Proxy, EDR | T1105 |
| Connexions HTTPS régulières vers un domaine récent ou rare (« balise ») | Proxy, DNS, pare-feu | T1071.001 |
| Alerte antivirus ou EDR, signalement d'un utilisateur (« mon PC est lent », fenêtre étrange) | Antivirus, service d'assistance | — |

## 2. Triage

- [ ] Ouvrir le dossier d'incident et noter l'heure de l'alerte (UTC)
- [ ] Confirmer que l'alerte n'est pas un faux positif : réputation du fichier (empreinte SHA-256), chemin, éditeur, processus parent
- [ ] Identifier le **patient zéro** : poste, utilisateur, heure de la première exécution, vecteur d'entrée (courriel, clé USB, site web)
- [ ] Rechercher la même empreinte, le même domaine ou la même adresse IP sur **tout le parc** (EDR, SIEM, proxy)
- [ ] Vérifier si des identifiants ont pu être volés (navigateur, gestionnaire de mots de passe, comptes ouverts sur le poste)
- [ ] Qualifier la gravité avec [D01](../docs/D01-gravite-et-delais.md) et escalader selon [D02](../docs/D02-escalade.md)

## 3. Confinement

- [ ] **Isoler du réseau** le ou les postes touchés (isolation EDR de préférence), **sans les éteindre**
- [ ] Bloquer les indicateurs connus : empreinte du fichier (EDR), domaines et adresses IP de commande (proxy, DNS, pare-feu)
- [ ] Mettre en quarantaine le courriel d'origine dans **toutes** les boîtes qui l'ont reçu
- [ ] Réinitialiser le mot de passe et révoquer les sessions de l'utilisateur concerné ; idem pour tout compte utilisé sur le poste
- [ ] Si un compte à privilèges a été utilisé sur le poste : requalifier en **S1** et escalader immédiatement

## 4. Preuves

- [ ] Faire une **capture de la mémoire vive** avant toute autre action sur le poste ([D05](../docs/D05-preservation-des-preuves.md), §2)
- [ ] Collecter le fichier malveillant et calculer son empreinte SHA-256
- [ ] Exporter les journaux utiles : EDR, Sysmon, PowerShell, proxy, DNS, messagerie, avec la plage horaire de l'incident
- [ ] Consigner chaque élément dans le registre de preuves (chaîne de custody)

## 5. Éradication

- [ ] Identifier **tous** les mécanismes de persistance (clés `Run`, tâches planifiées, services, extensions de navigateur)
- [ ] **Réinstaller** le poste à partir d'une image saine plutôt que de le « nettoyer » : on ne peut jamais être sûr d'avoir tout trouvé
- [ ] Corriger le vecteur d'entrée : règle de filtrage de la messagerie, blocage des macros, correctif de sécurité, sensibilisation de l'utilisateur
- [ ] Rechercher une dernière fois les indicateurs sur l'ensemble du parc avant de passer à la restauration

## 6. Restauration

- [ ] Remettre le poste en service sur le réseau sous **surveillance renforcée** (règle de détection dédiée pendant au moins 7 jours)
- [ ] Restaurer les données de l'utilisateur depuis une sauvegarde **antérieure** à l'infection, après analyse antivirus
- [ ] Confirmer avec l'utilisateur que le poste fonctionne normalement

## 7. Obligations et communication

- [ ] Si des identifiants ou des données personnelles ont pu être volés : associer le DPO et évaluer la notification à la CNIL ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Si l'entité relève de NIS 2 et que l'incident est important : alerte précoce sous 24 heures ([D04](../docs/D04-cadre-reglementaire.md), §3)
- [ ] Si l'organisation est assurée et souhaite être indemnisée : porter plainte sous 72 heures ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] Informer l'utilisateur et son responsable de ce qui s'est passé et des consignes à suivre

## 8. Clôture

- [ ] Plus aucune trace des indicateurs sur le parc depuis au moins 72 heures
- [ ] Tous les comptes exposés ont été réinitialisés
- [ ] Le rapport d'incident est complet (chronologie, actions, heures de prise en charge et de confinement)
- [ ] Retour d'expérience planifié selon la gravité ([D01](../docs/D01-gravite-et-delais.md), §3)
- [ ] Les nouveaux indicateurs et règles de détection sont ajoutés au SIEM ou à l'EDR

## Arbre de décision

```text
Alerte logiciel malveillant
  │
  ├─ Fichiers chiffrés ou note de rançon ? ── OUI → passer au P02
  │
  └─ NON → Faux positif ? ── OUI → consigner, ajuster la règle, clore
            │
            └─ NON → Isoler le poste (sans l'éteindre) → capturer la mémoire
                      │
                      ├─ Compte à privilèges utilisé sur le poste ? ── OUI → S1, escalade immédiate
                      ├─ Même indicateur sur d'autres postes ?      ── OUI → S2, isoler chacun
                      └─ Poste unique                                     → S3
                                │
                                └─ Réinstaller → surveiller 7 jours → clore
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1566.001](https://attack.mitre.org/techniques/T1566/001/) | Spearphishing Attachment | Passerelle de messagerie |
| [T1204.002](https://attack.mitre.org/techniques/T1204/002/) | User Execution: Malicious File | EDR (arbre des processus) |
| [T1059.001](https://attack.mitre.org/techniques/T1059/001/) | Command and Scripting Interpreter: PowerShell | Journal PowerShell, EDR |
| [T1547.001](https://attack.mitre.org/techniques/T1547/001/) | Registry Run Keys / Startup Folder | Sysmon, EDR |
| [T1105](https://attack.mitre.org/techniques/T1105/) | Ingress Tool Transfer | Proxy, EDR |
| [T1071.001](https://attack.mitre.org/techniques/T1071/001/) | Application Layer Protocol: Web Protocols | Proxy, DNS |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
