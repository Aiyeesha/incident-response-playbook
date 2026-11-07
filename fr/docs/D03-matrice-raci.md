---
id: D03
lang: fr
title: Matrice RACI de la réponse aux incidents
review: 2026-11-07
---

# D03 — Matrice RACI de la réponse aux incidents

[↑ Documents de référence](README.md)

La matrice RACI dit, pour chaque activité, **qui fait quoi**. Elle évite les deux échecs classiques
d'une crise : la tâche que tout le monde croit faite par quelqu'un d'autre, et la décision que
personne n'ose prendre.

| Lettre | Signification | Règle |
|---|---|---|
| **R** — Réalise | Exécute l'activité | Au moins un par ligne |
| **A** — Approuve | Rend des comptes et tranche | **Exactement un** par ligne |
| **C** — Consulté | Donne un avis **avant** la décision | Échange dans les deux sens |
| **I** — Informé | Est tenu au courant **après** | Information dans un seul sens |

## 1. Les rôles

| Code | Rôle |
|---|---|
| **N1** | Analyste SOC (niveau 1) |
| **N2** | Analyste réponse à incident (niveau 2) |
| **RS** | Responsable SOC / responsable de la réponse |
| **RSSI** | Responsable de la sécurité des systèmes d'information |
| **IT** | Équipes systèmes, réseau et poste de travail (DSI) |
| **DPO** | Délégué à la protection des données |
| **JUR** | Juridique |
| **COM** | Communication |
| **DIR** | Direction générale / cellule de crise |

## 2. La matrice

| Activité | N1 | N2 | RS | RSSI | IT | DPO | JUR | COM | DIR |
|---|---|---|---|---|---|---|---|---|---|
| Détecter et trier l'alerte | **R** | C | A | | | | | | |
| Qualifier la gravité ([D01](D01-gravite-et-delais.md)) | R | R | **A** | I | | | | | |
| Escalader ([D02](D02-escalade.md)) | R | R | **A** | I | | | | | I |
| Collecter et préserver les preuves ([D05](D05-preservation-des-preuves.md)) | | **R** | A | I | C | | C | | |
| Confinement technique | | R | **A** | C | R | | | | I |
| Couper un service ou isoler un site | | C | R | **A** | R | | | I | C |
| Éradication | | R | **A** | I | R | | | | |
| Restauration et remise en service | | C | R | I | **R** | | | | **A** |
| Évaluer la violation de données personnelles | | C | C | C | | **R** | C | | **A** |
| Notifier la CNIL ([D04](D04-cadre-reglementaire.md)) | | | C | C | | **R** | C | | **A** |
| Informer les personnes concernées | | | | C | | R | C | R | **A** |
| Notifier l'autorité NIS 2 / le CERT-FR | | | R | **R** | | | C | | **A** |
| Déposer plainte | | | C | R | | | **R** | | **A** |
| Déclarer le sinistre à l'assureur | | | C | R | | | R | | **A** |
| Communication interne | | | C | C | | | C | **R** | **A** |
| Communication externe (clients, presse) | | | | C | | C | C | **R** | **A** |
| Décider d'un éventuel paiement de rançon | | | C | C | | | R | | **A** |
| Retour d'expérience | C | R | **A** | R | R | C | C | C | I |

> 💡 **Lecture.** Dans la ligne « Restauration », l'IT **réalise** et la direction **approuve** : c'est
> la direction qui décide de remettre l'activité en route, car elle en porte le risque. Dans la ligne
> « Notifier la CNIL », le DPO prépare et transmet, mais c'est le **responsable de traitement**
> (représenté par la direction) qui est légalement tenu de notifier. Pour une éventuelle rançon, le
> juridique **instruit** le dossier (légalité, sanctions internationales, position de l'assureur) et
> la direction **décide**.

## 3. Règles d'utilisation

1. **Un seul A par ligne.** Deux personnes qui « approuvent » ensemble, c'est en pratique personne.
2. **Un suppléant pour chaque A**, désigné à l'avance dans l'[annuaire de crise (D02, §5)](D02-escalade.md#5-annuaire-de-crise-à-compléter).
   Un incident S1 éclate souvent un vendredi soir.
3. **Adapter à la taille de l'organisation** : dans une PME, une même personne peut tenir plusieurs
   rôles (par exemple RSSI et DSI). On garde alors les lignes, mais on note le nom réel.
4. **Rejouer la matrice** lors de chaque exercice sur table : c'est le meilleur moyen de découvrir
   qu'un rôle n'est tenu par personne.
