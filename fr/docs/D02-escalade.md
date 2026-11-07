---
id: D02
lang: fr
title: Procédure d'escalade
review: 2026-11-07
---

# D02 — Procédure d'escalade

[↑ Documents de référence](README.md)

Escalader, c'est **faire monter l'information** vers les personnes qui ont l'autorité ou la
compétence de décider. Une escalade trop tardive est l'une des causes les plus fréquentes
d'incidents qui dégénèrent ; une escalade précoce ne coûte presque rien.

## 1. Les niveaux

| Niveau | Rôle | Décide de… |
|---|---|---|
| **N1** | Analyste SOC | Trier l'alerte, qualifier une première gravité, ouvrir le dossier |
| **N2** | Analyste réponse à incident | Investiguer, proposer et appliquer le confinement technique |
| **N3** | Responsable SOC / responsable de la réponse | Valider la gravité, coordonner, mobiliser les équipes |
| **N4** | RSSI | Arbitrer les mesures lourdes (couper un service, isoler un site), alerter la direction |
| **N5** | Direction / cellule de crise | Décisions d'entreprise : continuité d'activité, communication externe, rançon, recours à un prestataire |

Le détail de « qui réalise, qui valide » pour chaque phase est dans la
[matrice RACI (D03)](D03-matrice-raci.md).

## 2. Qui prévenir, et quand

| Gravité ([D01](D01-gravite-et-delais.md)) | Prévenir | Délai | Canal |
|---|---|---|---|
| **S1 — Critique** | N3, RSSI, DSI, direction ; DPO et juridique si des données personnelles sont en jeu | **Immédiat** | Téléphone, puis canal de crise |
| **S2 — Élevée** | N3, RSSI ; DPO si des données personnelles sont en jeu | Sous 1 heure | Téléphone ou messagerie |
| **S3 — Moyenne** | N3 | Au point quotidien | Outil de ticketing |
| **S4 — Faible** | Personne (consigné dans le ticket) | — | Outil de ticketing |

### Déclencheurs d'escalade immédiate, quelle que soit la gravité initiale

- un **compte à privilèges** (administrateur du domaine, de l'hyperviseur, du cloud) est impliqué ;
- des **données personnelles** ou confidentielles ont pu être consultées ou extraites ;
- un **rançongiciel** ou une propagation rapide est suspecté ;
- l'incident touche un **système de sauvegarde** ou de sécurité (EDR, pare-feu, SIEM) ;
- un **média, un client ou une autorité** a connaissance de l'incident ;
- l'équipe **ne sait pas** quoi faire ou n'a pas les droits nécessaires.

## 3. Arbre de décision

```text
Alerte ou signalement reçu
  │
  ├─ Est-ce un incident ? (D01, §1) ── NON → traiter comme événement, consigner
  │
  └─ OUI → Qualifier la gravité (D01, §2)
            │
            ├─ Un déclencheur d'escalade immédiate (§2) ? ── OUI → escalade N3 + RSSI tout de suite
            │
            ├─ S1 → N3 + RSSI + DSI + direction, immédiatement → ouvrir la cellule de crise
            ├─ S2 → N3 + RSSI sous 1 heure
            ├─ S3 → N3 au point quotidien
            └─ S4 → consigner dans le ticket
                      │
                      └─ À chaque point de situation : la gravité a-t-elle changé ? → requalifier
```

## 4. Règles de communication pendant l'incident

1. **Utiliser un canal hors bande** si la messagerie ou l'annuaire de l'entreprise peuvent être
   compromis : téléphone, messagerie sécurisée externe, pont audio dédié. Un attaquant présent dans
   la messagerie lit aussi les échanges de l'équipe de réponse.
2. **Une seule voix** vers l'extérieur : seule la personne désignée dans la [RACI (D03)](D03-matrice-raci.md)
   communique avec la presse, les clients ou les autorités.
3. **Écrire, dater, conserver** : chaque décision prise oralement est notée dans le rapport d'incident
   avec l'heure et son auteur.
4. **Besoin d'en connaître** : on ne partage les détails techniques qu'avec les personnes qui en ont
   besoin ; un incident en cours n'est pas un sujet de discussion générale.

## 5. Annuaire de crise (à compléter)

À tenir **hors du système d'information** (version imprimée et copie sur un support personnel
sécurisé) et à vérifier **chaque trimestre** : un annuaire de crise inaccessible pendant un
rançongiciel ne sert à rien.

| Rôle | Nom | Téléphone | Téléphone de secours | Suppléant |
|---|---|---|---|---|
| Responsable SOC | | | | |
| RSSI | | | | |
| DSI | | | | |
| DPO | | | | |
| Juridique | | | | |
| Communication | | | | |
| Direction générale | | | | |
| Prestataire de réponse à incident | | | | |
| Assureur (ligne sinistre cyber) | | | | |

Les contacts publics (CERT-FR, 17Cyber, CNIL, dépôt de plainte) figurent dans
[D04 — Cadre réglementaire](D04-cadre-reglementaire.md).
