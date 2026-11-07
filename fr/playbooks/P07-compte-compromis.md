---
id: P07
lang: fr
title: Compte compromis et fraude au virement
severity: [S1, S2]
mitre: [T1078.004, T1110.003, T1621, T1539, T1114.003, T1564.008, T1534, T1657]
owner: Responsable SOC
review: 2026-11-07
---

# P07 — Compte compromis et fraude au virement

[↑ Playbooks](README.md)

**Quand l'utiliser :** un compte de messagerie ou un compte cloud (Microsoft 365, Google Workspace…)
est utilisé par un tiers, et en particulier quand ce compte sert à une **fraude au virement** :
faux changement de coordonnées bancaires d'un fournisseur, fausse demande urgente d'un dirigeant
(« fraude au président »), fausse facture envoyée aux clients. Ces fraudes s'appuient sur une
vraie boîte compromise ou sur une adresse qui l'imite.

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S2** ; **S1** si un virement frauduleux a été émis, si le compte est celui d'un dirigeant ou d'un administrateur, ou si des clients ont reçu de faux messages ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsable | Responsable SOC, avec la direction financière en cas de virement |
| Documents liés | [P04 — Hameçonnage](P04-hameconnage.md) · [D04 — Cadre réglementaire](../docs/D04-cadre-reglementaire.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

> 💸 **Si un virement frauduleux est parti, chaque heure compte.** La direction financière contacte
> **immédiatement** la banque pour demander le **rappel des fonds** : plus la demande est rapide,
> plus les chances de récupérer l'argent sont élevées. Cette action passe **avant** l'analyse
> technique.

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Connexion réussie depuis un pays, un appareil ou un fournisseur d'accès inhabituel | Journaux de connexion du cloud (Entra ID, Google) | T1078.004 |
| Nombreux échecs sur beaucoup de comptes depuis les mêmes sources, puis un succès | Journaux de connexion du cloud | T1110.003 |
| Rafale de demandes d'authentification multifacteur refusées, puis une acceptée | Journaux d'authentification, signalement utilisateur | T1621 |
| Même session utilisée depuis deux endroits à la fois, sans nouvelle authentification (vol de cookie) | Journaux de connexion du cloud | T1539 |
| Nouvelle règle de transfert vers une adresse externe | Journal d'audit de la messagerie | T1114.003 |
| Règle qui déplace ou supprime certains messages (mots-clés « virement », « RIB », « facture », nom d'un fournisseur) | Journal d'audit de la messagerie | T1564.008 |
| Messages d'hameçonnage envoyés **depuis** le compte vers des collègues ou des clients | Journaux de messagerie, signalements | T1534 |
| Demande de changement de coordonnées bancaires, demande de virement urgent et confidentiel | Comptabilité, direction | T1657 |

## 2. Triage

- [ ] Ouvrir le dossier, noter l'heure de détection (UTC) ; **si un virement est parti : alerter la banque d'abord** (encadré ci-dessus)
- [ ] Vérifier auprès du titulaire, **par téléphone** (jamais par la messagerie compromise), s'il reconnaît les connexions et les actions
- [ ] Lister les connexions suspectes : adresses IP, pays, appareils, applications, période
- [ ] Rechercher les **règles de messagerie** créées ou modifiées (transfert, déplacement, suppression) et les applications tierces autorisées sur le compte
- [ ] Rechercher les messages envoyés par l'attaquant depuis le compte, et leurs destinataires (internes et externes)
- [ ] Qualifier la gravité ([D01](../docs/D01-gravite-et-delais.md)) : virement émis, compte de dirigeant ou d'administrateur = S1

## 3. Confinement

- [ ] **Réinitialiser le mot de passe et révoquer toutes les sessions et jetons** du compte : un simple changement de mot de passe ne déconnecte pas toujours l'attaquant
- [ ] Supprimer les facteurs d'authentification ajoutés par l'attaquant et réenregistrer ceux du titulaire
- [ ] Désactiver les règles de transfert et de masquage créées, et retirer les autorisations des applications tierces suspectes
- [ ] Bloquer les adresses IP et les domaines utilisés (y compris les domaines qui imitent celui de l'entreprise ou d'un fournisseur)
- [ ] Prévenir rapidement les destinataires des faux messages (collègues, clients, fournisseurs), **par téléphone** pour les échanges financiers
- [ ] Geler tout paiement en attente vers des coordonnées bancaires modifiées récemment, jusqu'à vérification

## 4. Preuves

- [ ] Exporter les journaux de connexion et d'audit du compte sur toute la période (au moins 30 jours avant la détection si possible)
- [ ] Conserver les règles de messagerie créées par l'attaquant (export avant suppression), les faux messages au format original et les échanges avec la banque
- [ ] Conserver les éléments du virement : ordre, coordonnées bancaires frauduleuses, échanges qui l'ont déclenché ([D05](../docs/D05-preservation-des-preuves.md))

## 5. Éradication

- [ ] Trouver la porte d'entrée : hameçonnage ([P04](P04-hameconnage.md)), mot de passe réutilisé, absence d'authentification multifacteur, demandes d'authentification acceptées par lassitude
- [ ] Imposer une authentification multifacteur **résistante à l'hameçonnage** (clé de sécurité, passkey) aux comptes sensibles : direction, finances, administrateurs
- [ ] Vérifier les autres comptes qui ont reçu les mêmes tentatives et la même campagne
- [ ] Interdire ou encadrer le transfert automatique vers des adresses externes au niveau de toute la messagerie

## 6. Restauration

- [ ] Rendre le compte au titulaire avec ses nouveaux facteurs d'authentification et un mot de passe unique
- [ ] Restaurer les messages supprimés ou déplacés par les règles de l'attaquant
- [ ] Surveiller le compte et ceux de son service pendant au moins 30 jours (connexions, règles, envois)

## 7. Obligations et communication

- [ ] Fraude au virement : **plainte** (escroquerie), avec les éléments bancaires, sous 72 heures si l'organisation veut être indemnisée par son assurance ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] La boîte compromise contient presque toujours des données personnelles : associer le DPO et évaluer la notification à la CNIL ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Prévenir les clients et fournisseurs concernés, avec une procédure claire : **toute modification de coordonnées bancaires est vérifiée par un rappel téléphonique** à un numéro déjà connu
- [ ] Déclarer le sinistre à l'assureur (cyber ou fraude) dès que possible

## 8. Clôture

- [ ] L'attaquant n'a plus aucun accès au compte (sessions, règles, applications, facteurs d'authentification vérifiés)
- [ ] Le sort du virement est connu (rappel des fonds réussi ou non) et documenté
- [ ] Les destinataires des faux messages ont été prévenus
- [ ] Les obligations de la section 7 sont remplies ou formellement écartées
- [ ] Retour d'expérience réalisé ; procédure de vérification des changements de coordonnées bancaires mise en place ou rappelée

## Arbre de décision

```text
Compte suspect ou demande de virement inhabituelle
  │
  ├─ Un virement frauduleux est-il parti ? ── OUI → banque immédiatement (rappel des fonds) → S1
  │
  ├─ Le titulaire reconnaît-il l'activité (vérifié par téléphone) ? ── OUI → faux positif, consigner
  │
  └─ NON → réinitialiser, révoquer sessions et jetons, supprimer les règles malveillantes
            │
            ├─ Faux messages envoyés depuis le compte ? ── OUI → prévenir les destinataires par téléphone
            ├─ Compte de dirigeant ou d'administrateur ? ── OUI → S1, escalade immédiate
            └─ Sinon                                          → S2
                      │
                      └─ Trouver la porte d'entrée (P04 ?) → authentification résistante à l'hameçonnage
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1078.004](https://attack.mitre.org/techniques/T1078/004/) | Valid Accounts: Cloud Accounts | Journaux de connexion du cloud |
| [T1110.003](https://attack.mitre.org/techniques/T1110/003/) | Brute Force: Password Spraying | Journaux de connexion du cloud |
| [T1621](https://attack.mitre.org/techniques/T1621/) | Multi-Factor Authentication Request Generation | Journaux d'authentification |
| [T1539](https://attack.mitre.org/techniques/T1539/) | Steal Web Session Cookie | Journaux de connexion du cloud |
| [T1114.003](https://attack.mitre.org/techniques/T1114/003/) | Email Collection: Email Forwarding Rule | Journal d'audit de la messagerie |
| [T1564.008](https://attack.mitre.org/techniques/T1564/008/) | Hide Artifacts: Email Hiding Rules | Journal d'audit de la messagerie |
| [T1534](https://attack.mitre.org/techniques/T1534/) | Internal Spearphishing | Journaux de messagerie |
| [T1657](https://attack.mitre.org/techniques/T1657/) | Financial Theft | Comptabilité, banque |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
