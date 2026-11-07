---
id: D06
lang: fr
title: Exercice sur table — rançongiciel un vendredi soir
review: 2026-11-07
---

# D06 — Exercice sur table : rançongiciel un vendredi soir

[↑ Documents de référence](README.md)

Un exercice sur table réunit les acteurs de la réponse **autour d'une table, sans toucher aux
systèmes**, pour dérouler un incident fictif. Il révèle, sans risque, ce qu'un vrai incident
révélerait trop tard : un rôle tenu par personne, un contact introuvable, une sauvegarde joignable
depuis le réseau, un délai légal oublié.

## 1. Organisation

| Élément | Valeur |
|---|---|
| Durée | 2 h 30 (dont 30 minutes de bilan) |
| Participants | Les rôles de la [RACI (D03)](D03-matrice-raci.md) : SOC, RSSI, IT, DPO, juridique, communication, direction |
| Animateur | Une personne qui connaît le scénario et **ne joue pas** ; elle distribue les « injections » et chronomètre |
| Observateur | Note les décisions, les hésitations et les heures ; il remplit la grille de la section 5 |
| Matériel | Les playbooks [P02](../playbooks/P02-rancongiciel.md) et [P03](../playbooks/P03-fuite-de-donnees.md), les documents D01 à D05, l'annuaire de crise **imprimé**, un tableau blanc |
| Règle d'or | Le temps de l'exercice est accéléré, mais **les décisions sont réelles** : on dit ce que l'on ferait vraiment, avec les moyens réels de l'organisation |

## 2. Contexte fictif

**Atelier Lumen**, entreprise fictive de 180 salariés : un siège, un entrepôt, une boutique en ligne.
Annuaire Active Directory, messagerie Microsoft 365, serveur de fichiers, sauvegardes sur un NAS du
réseau interne, copie hebdomadaire sur bande. Accès distant par VPN pour 40 salariés.

## 3. Les injections

L'animateur lit chaque injection à l'heure prévue, puis laisse l'équipe décider. Les questions
guident la discussion ; il ne donne **pas** les réponses.

| Heure de l'exercice | Injection | Questions pour l'équipe |
|---|---|---|
| **T0** — vendredi 18 h 40 | L'EDR signale l'exécution de `vssadmin delete shadows` sur le serveur de fichiers, avec le compte `svc-sauvegarde`. | Qui reçoit l'alerte un vendredi soir ? Quelle gravité ([D01](D01-gravite-et-delais.md)) ? Qui prévient-on, comment, en combien de temps ([D02](D02-escalade.md)) ? |
| **T0 + 20 min** | Le support reçoit trois appels : des fichiers du service comptable portent l'extension `.lmn9`, illisibles. | Quel playbook ? Quels sont les trois réflexes ([P02](../playbooks/P02-rancongiciel.md), encadré) ? Qui décide d'isoler le serveur ? |
| **T0 + 45 min** | Une note de rançon apparaît dans chaque dossier : 400 000 € en cryptomonnaie, et la menace de publier « 120 Go de données RH et clients » sous 7 jours. | Qui est prévenu à ce stade ? Le DPO ? La direction ? Quel canal de communication, si la messagerie est peut-être surveillée ? |
| **T0 + 1 h 15** | L'IT constate que le NAS de sauvegarde est joignable depuis le réseau touché ; les sauvegardes des 5 derniers jours sont chiffrées. La bande de la semaine dernière est au coffre. | Que fait-on du NAS ? À partir de quand restaurer ? Quelle perte de données accepte-t-on ? Qui décide ([D03](D03-matrice-raci.md)) ? |
| **T0 + 2 h** | Les journaux du VPN montrent une connexion du compte d'un commercial depuis l'étranger, il y a 9 jours, sans authentification multifacteur. | Quel est le vecteur d'accès probable ? Quelles preuves collecter en priorité, avant que les journaux ne disparaissent ([D05](D05-preservation-des-preuves.md)) ? |
| **Samedi 9 h** | Un journaliste appelle le standard : « On nous dit que vous êtes victimes d'une cyberattaque, vous confirmez ? » | Qui répond ? Avec quel message ([T03](../templates/T03-communication-de-crise.md), M4) ? |
| **Samedi 15 h** | L'attaquant publie un échantillon : 200 fiches de salariés avec numéro de sécurité sociale. | Faut-il notifier la CNIL ? Avant quelle heure ? Faut-il informer les salariés ? Avec quel message ([T03](../templates/T03-communication-de-crise.md), M3) ? |
| **Lundi 9 h** | L'assureur demande le récépissé de plainte. | La plainte a-t-elle été déposée dans les 72 heures ([D04](D04-cadre-reglementaire.md), §4) ? Si non, pourquoi ? |
| **Lundi 11 h** | La direction demande : « Et si on payait, simplement ? » | Qui instruit cette question, avec quels arguments ? Qui décide ? |

## 4. Délais légaux à surveiller pendant l'exercice

L'observateur note **à quelle heure** l'équipe identifie chaque obligation. Point de départ retenu :
la prise de connaissance, vendredi vers 19 h.

| Obligation ([D04](D04-cadre-reglementaire.md)) | Échéance dans le scénario |
|---|---|
| Notification CNIL (72 h) | Lundi vers 19 h |
| Plainte pour l'indemnisation par l'assurance (72 h) | Lundi vers 19 h |
| Alerte précoce NIS 2 (24 h), si l'entité est concernée | Samedi vers 19 h |

## 5. Grille d'évaluation

| Critère | Atteint | Partiel | Non atteint | Commentaire |
|---|---|---|---|---|
| La gravité S1 est posée en moins de 15 minutes | | | | |
| Les bonnes personnes sont prévenues dans les délais de D02 | | | | |
| L'annuaire de crise est utilisable (à jour, accessible hors du SI) | | | | |
| Les machines sont isolées **sans être éteintes** | | | | |
| Les sauvegardes sont protégées en priorité | | | | |
| Un canal de crise hors bande est ouvert | | | | |
| Les preuves à rétention courte sont demandées tôt | | | | |
| Chaque décision a un responsable unique (RACI respectée) | | | | |
| Les trois délais légaux sont identifiés à temps | | | | |
| Un seul porte-parole s'adresse à l'extérieur | | | | |
| La question de la rançon est instruite, pas improvisée | | | | |

## 6. Bilan

Le bilan suit la méthode du [post-mortem (T02)](../templates/T02-post-mortem.md) : sans recherche de
coupable, avec un plan d'action daté. Les écarts constatés alimentent la mise à jour des playbooks,
de la RACI et de l'annuaire de crise. **Rejouer l'exercice au moins une fois par an**, en changeant de
scénario (fraude au virement avec le [P07](../playbooks/P07-compte-compromis.md), fuite de données
avec le [P03](../playbooks/P03-fuite-de-donnees.md)…).
