---
id: T02
lang: fr
title: Post-mortem
review: 2026-11-07
---

# T02 — Post-mortem

[↑ Modèles](README.md)

> 🤝 **Principe : sans recherche de coupable.** Le post-mortem cherche ce qui, dans les outils, les
> procédures et l'organisation, a permis l'incident ou ralenti la réponse. Une personne qui a cliqué
> sur un lien n'est pas « la cause » : la cause est l'absence de filtrage, d'authentification
> multifacteur ou de détection qui aurait dû rattraper ce clic. Sans ce principe, les erreurs ne
> sont plus signalées, et l'équipe ne progresse plus.

**Quand :** dans les délais fixés par [D01](../docs/D01-gravite-et-delais.md) (sous 5 jours ouvrés
pour un S1). **Durée :** 60 à 90 minutes. **Participants :** les personnes qui ont tenu un rôle dans
la [RACI](../docs/D03-matrice-raci.md) pendant l'incident, et un animateur qui n'y a pas participé
si possible.

## 1. Résumé

| Champ | Valeur |
|---|---|
| Référence de l'incident | `INC-AAAA-NNN` ([T01](T01-rapport-d-incident.md)) |
| Gravité maximale atteinte | S_ |
| Durée (détection → restauration) | |
| Impact (activité, données, coûts estimés) | |
| En une phrase : que s'est-il passé ? | |

## 2. Chronologie

Reprendre les repères du rapport d'incident et ajouter ce qui manquait : **quand l'attaque a-t-elle
réellement commencé, et pourquoi ne l'a-t-on pas vue plus tôt ?**

| Date et heure (UTC) | Événement | Aurait-on pu le détecter ? Avec quoi ? |
|---|---|---|
| | | |

## 3. Ce qui a bien fonctionné

-
-

## 4. Ce qui a moins bien fonctionné

-
-

## 5. Causes profondes

Méthode des « 5 pourquoi » : partir du fait constaté et demander « pourquoi ? » jusqu'à atteindre une
cause sur laquelle l'organisation peut agir.

| Niveau | Question | Réponse |
|---|---|---|
| 1 | Pourquoi l'attaquant a-t-il pu entrer ? | |
| 2 | Pourquoi ? | |
| 3 | Pourquoi ? | |
| 4 | Pourquoi ? | |
| 5 | Pourquoi ? | |

## 6. Plan d'action

Chaque action a **un seul responsable**, une **échéance** et un **critère de fin vérifiable**.

| N° | Action | Responsable | Échéance | Critère de fin | Statut |
|---|---|---|---|---|---|
| 1 | | | | | À faire |

## 7. Mises à jour documentaires

- [ ] Les playbooks concernés sont-ils à corriger ? (lesquels, quoi)
- [ ] La matrice RACI, l'annuaire de crise ou les délais ([D01](../docs/D01-gravite-et-delais.md), [D02](../docs/D02-escalade.md), [D03](../docs/D03-matrice-raci.md)) sont-ils à revoir ?
- [ ] De nouvelles règles de détection sont-elles à créer ?
- [ ] Un exercice sur table ([D06](../docs/D06-exercice-sur-table.md)) doit-il rejouer ce scénario ?
