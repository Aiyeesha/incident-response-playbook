---
id: T01
lang: fr
title: Rapport d'incident
review: 2026-11-07
---

# T01 — Rapport d'incident

[↑ Modèles](README.md)

> 📝 **Mode d'emploi.** Copier ce modèle **hors de ce dépôt** (outil de ticketing, espace documentaire
> sécurisé) au début de l'incident et le remplir **au fil de l'eau**, pas à la fin. Toutes les heures
> sont en **UTC**. Un rapport rempli contient des informations sensibles : il ne doit jamais être
> publié.

## 1. Identification

| Champ | Valeur |
|---|---|
| Référence | `INC-AAAA-NNN` |
| Titre court | |
| Playbook suivi | P0_ — |
| Rédacteur | |
| Responsable de l'incident (A dans la [RACI](../docs/D03-matrice-raci.md)) | |
| Statut | Ouvert · Confiné · Éradiqué · Restauré · Clos |

## 2. Repères de temps

Ces heures alimentent les indicateurs du SOC : temps de détection (MTTD = détection − début
estimé) et temps de résolution (MTTR = restauration − détection).

| Étape | Date et heure (UTC) | Source ou commentaire |
|---|---|---|
| Début estimé de l'attaque | | |
| Détection (alerte ou signalement) | | |
| Prise en charge par un analyste | | |
| Escalade (N3, RSSI…) | | |
| Confinement vérifié | | |
| Éradication terminée | | |
| Restauration terminée | | |
| Clôture | | |

## 3. Gravité

| Date et heure (UTC) | Gravité ([D01](../docs/D01-gravite-et-delais.md)) | Critère décisif | Décidé par |
|---|---|---|---|
| | S_ | | |

## 4. Périmètre

| Élément | Détail |
|---|---|
| Systèmes touchés (nom, rôle, adresse IP) | |
| Comptes touchés | |
| Données touchées (catégories, volume, personnes concernées) | |
| Sites ou services touchés | |
| Impact sur l'activité | |

## 5. Indicateurs de compromission

| Type (IP, domaine, empreinte, compte, fichier…) | Valeur | Première observation (UTC) | Bloqué ? |
|---|---|---|---|
| | | | |

## 6. Journal des actions

Une ligne par action ou décision, **au moment où elle a lieu**.

| Date et heure (UTC) | Auteur | Action ou décision | Résultat |
|---|---|---|---|
| | | | |

## 7. Preuves

Renvoi vers le [registre de preuves (T04)](T04-registre-de-preuves.md) : référence du registre et
nombre d'éléments collectés.

## 8. Obligations et signalements

| Obligation ([D04](../docs/D04-cadre-reglementaire.md)) | Concernée ? | Échéance (UTC) | Faite le (UTC) | Référence |
|---|---|---|---|---|
| Registre des violations (RGPD) | Oui · Non | — | | |
| Notification CNIL (72 h) | Oui · Non | | | |
| Information des personnes concernées | Oui · Non | | | |
| NIS 2 — alerte précoce (24 h) | Oui · Non | | | |
| NIS 2 — notification (72 h) | Oui · Non | | | |
| NIS 2 — rapport final (1 mois) | Oui · Non | | | |
| Plainte (72 h pour l'assurance) | Oui · Non | | | |
| Déclaration à l'assureur | Oui · Non | | | |

Pour chaque « Non », indiquer en une phrase la justification.

## 9. Synthèse de clôture

| Champ | Valeur |
|---|---|
| Cause racine | |
| Vecteur d'accès initial | |
| Mesures correctives immédiates | |
| Post-mortem prévu le | [T02](T02-post-mortem.md) |
| Validé par (responsable de l'incident) | Nom, date |
