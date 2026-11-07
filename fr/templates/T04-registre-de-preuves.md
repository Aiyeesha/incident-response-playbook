---
id: T04
lang: fr
title: Registre de preuves
review: 2026-11-07
---

# T04 — Registre de preuves

[↑ Modèles](README.md)

Ce registre trace **l'historique complet** de chaque preuve : sa collecte, son intégrité, sa garde et
ses transferts. Il met en pratique le document [D05 — Préservation des preuves](../docs/D05-preservation-des-preuves.md).

> 🔒 **À tenir hors de ce dépôt**, dans un espace à accès restreint. Toutes les heures sont en **UTC**.
> On ne modifie jamais une ligne : on en ajoute une nouvelle (correction, transfert, restitution).

## 1. En-tête

| Champ | Valeur |
|---|---|
| Incident | `INC-AAAA-NNN` ([T01](T01-rapport-d-incident.md)) |
| Responsable du registre | |
| Lieu de stockage des preuves | |
| Ouvert le (UTC) | |

## 2. Inventaire des preuves

| Réf. | Description | Source (machine, n° de série, IP) | Collecte : date, heure (UTC), auteur | Méthode et outil | Empreinte SHA-256 | Taille | Emplacement |
|---|---|---|---|---|---|---|---|
| `INC-AAAA-NNN-P01` | Exemple : image mémoire | PC-COMPTA-07, SN …, 10.0.2.47 | 2026-11-07 14:32, A. Dupont | WinPmem depuis une clé protégée en écriture | `…` | 16 Go | Disque chiffré n° 3 |
| | | | | | | | |

## 3. Chaîne de custody

Une ligne **à chaque changement de main** et à chaque accès à une preuve.

| Réf. | Date et heure (UTC) | Remis par | Reçu par | Motif (analyse, copie, transmission aux enquêteurs…) | Empreinte vérifiée (oui / non) | Signature |
|---|---|---|---|---|---|---|
| | | | | | | |

## 4. Restitution ou destruction

| Réf. | Date (UTC) | Action (restitution, destruction, archivage) | Autorisée par | Réalisée par | Méthode |
|---|---|---|---|---|---|
| | | | | | |

La durée de conservation est fixée avec le juridique : au moins jusqu'à la fin de toute procédure
judiciaire ou d'assurance liée à l'incident.
