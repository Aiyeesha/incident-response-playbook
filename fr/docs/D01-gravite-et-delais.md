---
id: D01
lang: fr
title: Gravité et délais de traitement
review: 2026-11-07
---

# D01 — Gravité et délais de traitement

[↑ Documents de référence](README.md)

Ce document fixe **comment qualifier la gravité** d'un incident et **en combien de temps** il doit
être traité. Tous les playbooks s'y réfèrent : la gravité décide de qui est prévenu
([D02 — Escalade](D02-escalade.md)) et du rythme de toute la réponse.

> ⚙️ **À adapter.** Les seuils et délais ci-dessous sont des **valeurs de départ** réalistes pour une
> PME ou une ETI disposant d'un SOC (interne ou externalisé). Chaque organisation doit les valider
> avec sa direction et les aligner sur ses contrats (prestataire SOC, assurance, clients).

## 1. Événement ou incident ?

| Terme | Définition | Exemple |
|---|---|---|
| **Événement** | Toute observation sur un système ou un réseau | Un échec de connexion, une alerte antivirus |
| **Incident** | Événement qui compromet, ou menace réellement, la confidentialité, l'intégrité ou la disponibilité d'un système ou d'une donnée, ou qui viole une politique de sécurité | Un compte utilisé depuis un pays inhabituel après 200 échecs de connexion |

Seul un **incident** déclenche un playbook. Un événement isolé est traité dans le flux normal du SOC,
mais il est **conservé** : plusieurs événements anodins peuvent, ensemble, révéler un incident.

## 2. Les quatre niveaux de gravité

On évalue l'incident selon **cinq critères**. **Le critère le plus grave l'emporte** : un seul critère
au niveau S1 suffit à classer l'incident en S1.

| Critère | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Activité** | Activité arrêtée ou service essentiel indisponible | Service important dégradé, contournement possible | Gêne limitée à une équipe | Aucun effet sur l'activité |
| **Étendue** | Plusieurs sites, le domaine Active Directory ou l'infrastructure centrale | Plusieurs postes ou un serveur | Un poste ou un compte | Aucun système compromis |
| **Données** | Données sensibles ou personnelles exfiltrées ou chiffrées à grande échelle | Données personnelles ou confidentielles probablement exposées | Données internes peu sensibles exposées | Aucune donnée touchée |
| **Privilèges** | Compte administrateur du domaine ou de l'infrastructure compromis | Compte à privilèges locaux ou de service compromis | Compte utilisateur standard compromis | Tentative bloquée |
| **Propagation** | En cours, rapide (ver, rançongiciel) | Possible à court terme | Peu probable | Nulle |

### Exemples de qualification

| Situation | Gravité | Critère décisif |
|---|---|---|
| Fichiers chiffrés sur un serveur de fichiers, note de rançon | **S1** | Propagation rapide, données chiffrées |
| Compte d'administrateur du domaine utilisé depuis une adresse inconnue | **S1** | Privilèges |
| Un poste infecté par un logiciel malveillant, isolé par l'EDR | **S3** | Étendue limitée, propagation peu probable |
| Fichier client exporté vers un service de stockage personnel | **S2** | Données personnelles probablement exposées |
| Courriel d'hameçonnage reçu, signalé, personne n'a cliqué | **S4** | Aucun système compromis |

## 3. Délais de traitement par niveau

| Délai visé | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Prise en charge** (un analyste commence l'analyse) | 15 minutes | 1 heure | 4 heures | 1 jour ouvré |
| **Escalade** au responsable SOC et au RSSI | Immédiate | Sous 1 heure | Au point quotidien | Non requise |
| **Confinement** (la menace ne progresse plus) | 4 heures | 24 heures | 72 heures | 5 jours ouvrés |
| **Point de situation** aux parties prenantes | Toutes les 2 heures | 2 fois par jour | Quotidien | À la clôture |
| **Retour d'expérience** après la clôture | Sous 5 jours ouvrés | Sous 10 jours ouvrés | Facultatif (synthèse mensuelle) | Non requis |

Les délais se comptent à partir du **moment où l'incident est connu de l'équipe** (alerte, signalement),
et **24 h/24, 7 j/7 pour S1 et S2**. Les heures de prise en charge, d'escalade et de confinement sont
**consignées dans le rapport d'incident** : ce sont elles qui permettent ensuite de mesurer le temps
moyen de détection (MTTD) et de résolution (MTTR).

> ⚠️ **Délais légaux et contractuels.** Ces délais internes **ne remplacent pas** les délais imposés
> par la loi ou un contrat, qui courent **en parallèle** : 72 heures pour notifier la CNIL, 24 heures
> pour l'alerte précoce NIS 2, 72 heures pour porter plainte afin d'être indemnisé par son assurance…
> Voir [D04 — Cadre réglementaire](D04-cadre-reglementaire.md).

## 4. Requalifier un incident

La gravité n'est **pas figée**. On la réévalue à chaque point de situation :

- **à la hausse** dès qu'un critère s'aggrave (un deuxième poste touché, une donnée personnelle
  découverte, un compte à privilèges impliqué) ;
- **à la baisse** seulement quand le confinement est **vérifié**, jamais sur une impression.

Chaque changement de gravité est **daté et justifié** dans le rapport d'incident, avec le nom de la
personne qui l'a décidé (voir [D03 — Matrice RACI](D03-matrice-raci.md)).

## 5. Ce qu'il faut retenir

1. Le **critère le plus grave** décide du niveau.
2. Dans le doute entre deux niveaux, on choisit **le plus élevé**, puis on requalifie.
3. Les délais internes et les délais légaux **courent en même temps**.
