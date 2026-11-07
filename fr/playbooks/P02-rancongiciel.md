---
id: P02
lang: fr
title: Attaque par rançongiciel
severity: [S1]
mitre: [T1133, T1078, T1003, T1021.001, T1685, T1490, T1567.002, T1486]
owner: Responsable SOC et RSSI
review: 2026-11-07
---

# P02 — Attaque par rançongiciel

[↑ Playbooks](README.md)

**Quand l'utiliser :** des fichiers sont chiffrés, une note de rançon apparaît, ou un comportement
annonciateur est détecté (suppression des clichés instantanés, arrêt massif de services, désactivation
de l'antivirus). Un rançongiciel est **toujours S1**.

| Repère | Valeur |
|---|---|
| Gravité | **S1 — Critique**, toujours ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsables | Responsable SOC (technique) et RSSI (arbitrages) ; cellule de crise ouverte par la direction |
| Documents liés | [D02 — Escalade](../docs/D02-escalade.md) · [D03 — RACI](../docs/D03-matrice-raci.md) · [D04 — Cadre réglementaire](../docs/D04-cadre-reglementaire.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

> 🛑 **Les trois réflexes des premières minutes**
> 1. **Isoler** les machines touchées du réseau — **ne pas les éteindre** : la mémoire peut contenir
>    la clé de chiffrement ou des traces de l'attaquant.
> 2. **Protéger les sauvegardes** : les déconnecter du réseau de production avant que l'attaquant ne
>    les chiffre ou ne les supprime.
> 3. **Ne pas contacter l'attaquant** et **ne rien payer** sans décision de la direction, instruite
>    par le juridique ([D03](../docs/D03-matrice-raci.md)).

## 1. Détection

Un rançongiciel moderne est la **dernière étape** d'une intrusion qui a souvent duré des jours ou des
semaines. Les signaux précoces sont donc les plus précieux :

| Signal | Source habituelle | Technique |
|---|---|---|
| Connexion VPN ou bureau à distance réussie depuis un pays ou un horaire inhabituel | VPN, pare-feu, annuaire | T1133, T1078 |
| Accès au processus `lsass.exe`, outils de vol d'identifiants (type Mimikatz) | EDR, Sysmon (événement 10) | T1003 |
| Connexions RDP en cascade d'un serveur à l'autre, notamment avec un compte d'administration | Journaux Windows (événement 4624, type 10), EDR | T1021.001 |
| Antivirus ou EDR désactivé, exclusions ajoutées, service de sécurité arrêté | Console EDR, journaux système | T1685 |
| `vssadmin delete shadows`, `wbadmin delete catalog`, `bcdedit /set recoveryenabled no` | EDR, journaux de commandes | T1490 |
| Gros volume sortant vers un service de stockage en ligne (double extorsion) | Proxy, pare-feu | T1567.002 |
| Renommage massif de fichiers, nouvelle extension, note de rançon dans chaque dossier | EDR, serveur de fichiers, utilisateurs | T1486 |

## 2. Triage

- [ ] Ouvrir le dossier d'incident en **S1**, noter l'heure de détection (UTC), prévenir immédiatement selon [D02](../docs/D02-escalade.md)
- [ ] Ouvrir un **canal de crise hors bande** (téléphone, messagerie externe) : la messagerie de l'entreprise peut être surveillée
- [ ] Photographier la note de rançon et noter l'extension des fichiers chiffrés **sans** ouvrir de lien ni contacter l'attaquant
- [ ] Identifier la famille de rançongiciel si possible (note, extension) pour orienter la recherche de déchiffreur et d'indicateurs
- [ ] Délimiter le périmètre : postes, serveurs, partages, sites et environnements cloud touchés
- [ ] Vérifier l'état des **sauvegardes** : où sont-elles, sont-elles joignables depuis le réseau touché, la dernière copie saine date de quand ?

## 3. Confinement

- [ ] **Isoler** toutes les machines touchées (isolation EDR, port de switch, VLAN de quarantaine), sans les éteindre
- [ ] **Déconnecter les sauvegardes** du réseau de production et suspendre les tâches de sauvegarde planifiées (elles écraseraient les copies saines)
- [ ] Couper les accès distants exposés (VPN, bureau à distance, portails) le temps de l'analyse — décision du RSSI
- [ ] Désactiver les comptes compromis ; si un administrateur du domaine est touché, préparer la **réinitialisation complète** des comptes à privilèges (dont le compte `krbtgt`, deux fois)
- [ ] Bloquer les adresses IP et domaines de l'attaquant (pare-feu, proxy, DNS)
- [ ] Si le chiffrement est encore en cours et qu'une isolation réseau est impossible : couper l'accès aux partages de fichiers ; l'extinction n'est qu'un **dernier recours**, décidé par le RSSI

## 4. Preuves

- [ ] Capturer la **mémoire vive** d'au moins une machine touchée avant tout redémarrage ([D05](../docs/D05-preservation-des-preuves.md))
- [ ] Conserver un échantillon du rançongiciel, la note de rançon et quelques fichiers chiffrés (utiles pour un éventuel déchiffreur)
- [ ] Exporter **sans attendre** les journaux à rétention courte : VPN, pare-feu, proxy, annuaire, EDR
- [ ] Faire des images disque des machines clés (contrôleur de domaine, serveur de fichiers, patient zéro) si possible
- [ ] Tenir la chaîne de custody de chaque élément

## 5. Éradication

- [ ] Reconstituer la chronologie complète de l'intrusion : accès initial, élévation de privilèges, déplacements, exfiltration
- [ ] Fermer le **vecteur d'accès initial** (accès distant sans authentification multifacteur, vulnérabilité non corrigée, identifiants volés)
- [ ] Rechercher et supprimer toutes les **portes dérobées** et persistances (comptes créés, tâches planifiées, outils d'administration à distance)
- [ ] Réinitialiser **tous** les mots de passe des comptes à privilèges et de service ; `krbtgt` deux fois, à intervalle suffisant pour la réplication
- [ ] **Reconstruire** les machines touchées à partir d'images saines ; ne jamais tenter de les « nettoyer »

## 6. Restauration

- [ ] Restaurer par **ordre de priorité métier**, défini avec la direction (annuaire, puis services critiques, puis postes)
- [ ] Restaurer depuis une sauvegarde **antérieure à l'intrusion** (et pas seulement au chiffrement) et vérifier son intégrité avant reconnexion
- [ ] Reconnecter les systèmes progressivement, dans des segments surveillés
- [ ] Renforcer la surveillance pendant au moins **30 jours** : les attaquants reviennent souvent par une porte oubliée
- [ ] Mesurer la perte de données (écart entre la dernière sauvegarde saine et l'incident)

## 7. Obligations et communication

- [ ] **Plainte sous 72 heures** pour préserver l'indemnisation par l'assurance, et déclaration du sinistre à l'assureur ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] Évaluer la violation de données personnelles : un chiffrement est une perte de disponibilité, une exfiltration est une perte de confidentialité ; notification à la **CNIL sous 72 heures** si risque ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Entités NIS 2 : **alerte précoce sous 24 heures**, notification sous 72 heures ([D04](../docs/D04-cadre-reglementaire.md), §3)
- [ ] Se faire aider : 17Cyber, prestataire de réponse à incident, CERT-FR selon le type d'entité ([D04](../docs/D04-cadre-reglementaire.md), §5)
- [ ] Communication interne et externe **uniquement** par les personnes désignées dans la [RACI](../docs/D03-matrice-raci.md)
- [ ] Toute discussion sur un paiement de rançon est instruite par le juridique et décidée par la direction ; les autorités françaises, dont l'ANSSI, recommandent de **ne pas payer** : le paiement ne garantit ni le déchiffrement ni la suppression des données volées, et finance de nouvelles attaques

## 8. Clôture

- [ ] Toutes les machines touchées sont reconstruites, et aucun indicateur n'est réapparu pendant la période de surveillance renforcée
- [ ] Le vecteur d'accès initial est fermé et vérifié
- [ ] Toutes les obligations de la section 7 sont remplies ou formellement écartées, avec la justification
- [ ] Le rapport d'incident et la chronologie complète sont archivés
- [ ] Retour d'expérience tenu sous 5 jours ouvrés ; plan d'action suivi jusqu'à son terme (sauvegardes déconnectées, authentification multifacteur, segmentation…)

## Arbre de décision

```text
Fichiers chiffrés ou signal annonciateur
  │
  ├─ S1 → escalade immédiate (D02) → canal de crise hors bande
  │
  ├─ Isoler les machines touchées (sans les éteindre)
  │
  ├─ Sauvegardes joignables depuis le réseau touché ?
  │     ├─ OUI → les déconnecter tout de suite
  │     └─ NON → vérifier qu'elles sont intactes
  │
  ├─ Compte d'administrateur du domaine compromis ?
  │     ├─ OUI → reconstruction de l'annuaire à envisager, réinitialisation de tous les comptes à privilèges
  │     └─ NON → réinitialiser les comptes compromis
  │
  └─ Sauvegardes saines disponibles ?
        ├─ OUI → éradiquer, puis restaurer depuis une copie antérieure à l'intrusion
        └─ NON → cellule de crise : prestataire spécialisé, recherche de déchiffreur, options juridiques
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1133](https://attack.mitre.org/techniques/T1133/) | External Remote Services | VPN, passerelle d'accès distant |
| [T1078](https://attack.mitre.org/techniques/T1078/) | Valid Accounts | Annuaire, VPN |
| [T1003](https://attack.mitre.org/techniques/T1003/) | OS Credential Dumping | EDR, Sysmon |
| [T1021.001](https://attack.mitre.org/techniques/T1021/001/) | Remote Services: Remote Desktop Protocol | Journaux Windows, EDR |
| [T1685](https://attack.mitre.org/techniques/T1685/) | Disable or Modify Tools | Console EDR, journaux système |
| [T1490](https://attack.mitre.org/techniques/T1490/) | Inhibit System Recovery | EDR, journaux de commandes |
| [T1567.002](https://attack.mitre.org/techniques/T1567/002/) | Exfiltration to Cloud Storage | Proxy, pare-feu |
| [T1486](https://attack.mitre.org/techniques/T1486/) | Data Encrypted for Impact | EDR, serveur de fichiers |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**. Dans cette version, la désactivation des
outils de sécurité (ancien T1562.001) est devenue **T1685**, rattachée à la nouvelle tactique
« Defense Impairment ».
