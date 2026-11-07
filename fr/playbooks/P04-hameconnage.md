---
id: P04
lang: fr
title: Hameçonnage
severity: [S2, S3, S4]
mitre: [T1566.001, T1566.002, T1598.003, T1204.001, T1056.003]
owner: Responsable SOC
review: 2026-11-07
---

# P04 — Hameçonnage

[↑ Playbooks](README.md)

**Quand l'utiliser :** un ou plusieurs courriels (ou SMS, messages de messagerie instantanée)
cherchent à faire **cliquer**, **ouvrir une pièce jointe** ou **saisir des identifiants**. Le
playbook couvre la campagne elle-même ; ses conséquences ont leurs propres playbooks :

- une pièce jointe a été exécutée → [P01 — Logiciel malveillant](P01-logiciel-malveillant.md) ;
- des identifiants ont été saisis et utilisés → [P07 — Compte compromis](P07-compte-compromis.md).

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S4** si personne n'a cliqué ; **S3** si des clics sans saisie ; **S2** si des identifiants ont été saisis ou une pièce jointe ouverte ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsable | Responsable SOC |
| Documents liés | [D02 — Escalade](../docs/D02-escalade.md) · [D05 — Preuves](../docs/D05-preservation-des-preuves.md) |

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Pièce jointe inhabituelle (archive protégée par mot de passe, fichier `.html`, `.iso`, `.lnk`, document à macros) | Passerelle de messagerie, bac à sable | T1566.001 |
| Lien vers un domaine récent, imitant une marque ou raccourci | Passerelle de messagerie, proxy | T1566.002, T1204.001 |
| Fausse page de connexion (Microsoft 365, banque, transporteur) qui demande identifiants ou code d'authentification | Proxy, signalement utilisateur | T1598.003, T1056.003 |
| Échec des contrôles SPF, DKIM ou DMARC dans l'en-tête `Authentication-Results` | En-têtes du message | — |
| Signalement par un utilisateur (bouton « Signaler », message au support) | Service d'assistance | — |

## 2. Triage

- [ ] Récupérer le message **au format original** (`.eml` ou `.msg`), avec tous ses en-têtes, sans cliquer sur les liens
- [ ] Analyser l'en-tête : expéditeur réel (`Return-Path`), serveurs traversés (`Received`), résultats SPF, DKIM et DMARC
- [ ] Extraire les indicateurs : adresse et domaine d'envoi, liens (sans les ouvrir), empreintes SHA-256 des pièces jointes
- [ ] Analyser liens et pièces jointes **uniquement** dans un environnement isolé (bac à sable, machine d'analyse) ou via un service de réputation
- [ ] Mesurer l'étendue : combien de destinataires, **qui a cliqué**, qui a saisi ses identifiants, qui a ouvert la pièce jointe (journaux proxy et messagerie)
- [ ] Qualifier la gravité ([D01](../docs/D01-gravite-et-delais.md)) ; si des identifiants ont été saisis : S2 et escalade ([D02](../docs/D02-escalade.md))

## 3. Confinement

- [ ] **Purger** le message de toutes les boîtes de réception (recherche par expéditeur, objet ou empreinte)
- [ ] Bloquer l'expéditeur, le domaine d'envoi et les domaines des liens (passerelle de messagerie, proxy, DNS)
- [ ] Pour chaque utilisateur ayant saisi ses identifiants : réinitialiser le mot de passe, **révoquer les sessions** et vérifier ses facteurs d'authentification ; poursuivre avec le [P07](P07-compte-compromis.md)
- [ ] Pour chaque utilisateur ayant ouvert la pièce jointe : isoler le poste et poursuivre avec le [P01](P01-logiciel-malveillant.md)
- [ ] Prévenir les utilisateurs **par un autre canal que la messagerie** si la campagne est massive (« ne cliquez pas sur… »)

## 4. Preuves

- [ ] Conserver le message original (`.eml`) et son empreinte SHA-256 dans le registre de preuves ([D05](../docs/D05-preservation-des-preuves.md))
- [ ] Faire une capture horodatée de la fausse page (URL complète, date, apparence), depuis l'environnement d'analyse
- [ ] Exporter les journaux de messagerie (livraison, ouverture) et du proxy (clics) pour la période concernée

## 5. Éradication

- [ ] Vérifier qu'aucune copie du message ne subsiste (boîtes partagées, dossiers « Courrier indésirable », appareils mobiles)
- [ ] Ajouter les indicateurs aux listes de blocage et une règle de détection pour les variantes de la campagne
- [ ] Demander le retrait de la fausse page auprès de l'hébergeur ou du registraire du domaine

## 6. Restauration

- [ ] Vérifier que les comptes réinitialisés fonctionnent et que leurs facteurs d'authentification sont légitimes
- [ ] Libérer les messages légitimes éventuellement bloqués par erreur
- [ ] Surveiller pendant 7 jours les nouvelles campagnes du même expéditeur ou au même modèle

## 7. Obligations et communication

- [ ] Si des identifiants ou des données personnelles ont été divulgués : associer le DPO et évaluer la notification à la CNIL ([D04](../docs/D04-cadre-reglementaire.md), §2)
- [ ] Signaler le message aux services publics dédiés (par exemple Signal Spam pour les courriels ; le 33700 pour les SMS et appels indésirables, en transférant le SMS au 33700 ou via le formulaire de 33700.fr) et, si une marque est imitée, à cette marque
- [ ] Remercier les utilisateurs qui ont signalé le message : c'est le meilleur capteur de détection
- [ ] Partager un message de sensibilisation court, avec une capture du faux message et les indices qui le trahissaient

## 8. Clôture

- [ ] Le message est purgé de toutes les boîtes, et ses indicateurs sont bloqués
- [ ] Tous les utilisateurs exposés ont été traités (réinitialisation, isolement ou simple vérification)
- [ ] Les incidents dérivés (P01, P07) ont leur propre dossier
- [ ] Le rapport indique le nombre de destinataires, de clics, de saisies et de signalements

## Arbre de décision

```text
Message d'hameçonnage signalé ou détecté
  │
  ├─ Analyser en environnement isolé → extraire les indicateurs → purger toutes les boîtes
  │
  ├─ Quelqu'un a-t-il ouvert la pièce jointe ? ── OUI → isoler le poste → P01
  │
  ├─ Quelqu'un a-t-il saisi ses identifiants ? ── OUI → réinitialiser, révoquer les sessions → P07
  │
  ├─ Quelqu'un a-t-il seulement cliqué ?        ── OUI → S3 : vérifier le poste, surveiller
  │
  └─ Personne                                         → S4 : bloquer, remercier, sensibiliser
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1566.001](https://attack.mitre.org/techniques/T1566/001/) | Spearphishing Attachment | Passerelle de messagerie |
| [T1566.002](https://attack.mitre.org/techniques/T1566/002/) | Spearphishing Link | Passerelle de messagerie, proxy |
| [T1598.003](https://attack.mitre.org/techniques/T1598/003/) | Phishing for Information: Spearphishing Link | Proxy, signalements |
| [T1204.001](https://attack.mitre.org/techniques/T1204/001/) | User Execution: Malicious Link | Proxy |
| [T1056.003](https://attack.mitre.org/techniques/T1056/003/) | Input Capture: Web Portal Capture | Proxy, analyse de la fausse page |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
