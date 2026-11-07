---
id: P06
lang: fr
title: Déni de service
severity: [S1, S2, S3]
mitre: [T1498.001, T1498.002, T1499.002, T1499.003]
owner: Responsable SOC et responsable réseau
review: 2026-11-07
---

# P06 — Déni de service

[↑ Playbooks](README.md)

**Quand l'utiliser :** un service (site web, application, accès Internet, VPN) devient lent ou
indisponible parce qu'il est **submergé de requêtes ou de trafic**. Une attaque par déni de service
distribué (DDoS) vient de milliers de machines à la fois ; elle sert parfois aussi de **diversion**
pendant une autre intrusion.

| Repère | Valeur |
|---|---|
| Gravité habituelle | **S3** si un service secondaire est ralenti ; **S2** si un service important est dégradé ; **S1** si un service essentiel ou l'accès Internet de l'entreprise est coupé ([D01](../docs/D01-gravite-et-delais.md)) |
| Responsables | Responsable SOC et responsable réseau ; hébergeur et opérateur en appui |
| Documents liés | [D02 — Escalade](../docs/D02-escalade.md) · [D04 — Cadre réglementaire](../docs/D04-cadre-reglementaire.md) |

> 📞 **À préparer avant l'incident :** les contacts d'urgence de l'hébergeur, de l'opérateur et du
> service de protection anti-DDoS, avec la procédure pour activer la protection, figurent dans
> l'[annuaire de crise (D02, §5)](../docs/D02-escalade.md#5-annuaire-de-crise-à-compléter). Pendant
> l'attaque, il est trop tard pour les chercher.

## 1. Détection

| Signal | Source habituelle | Technique |
|---|---|---|
| Saturation du lien Internet, explosion du nombre de paquets entrants | Supervision réseau, opérateur | T1498.001 |
| Grand volume de réponses DNS, NTP ou memcached non sollicitées (attaque par réflexion et amplification) | Pare-feu, supervision réseau | T1498.002 |
| Nombre anormal de connexions ou de requêtes par seconde sur un service (inondation SYN, requêtes HTTP) | Équilibreur de charge, pare-feu, serveur web | T1499.002 |
| Requêtes répétées vers les pages ou fonctions les plus coûteuses (recherche, connexion, export) | Journaux web, pare-feu applicatif | T1499.003 |
| Alertes de disponibilité, plaintes de clients ou d'utilisateurs | Supervision, service client | — |

## 2. Triage

- [ ] Confirmer l'attaque et écarter une **cause légitime** : pic de trafic attendu (opération commerciale, article de presse), panne, mise à jour défectueuse
- [ ] Identifier la cible (adresse IP, service, page), le type de trafic (protocole, volume, nombre de sources) et l'heure de début (UTC)
- [ ] Mesurer l'impact sur l'activité et qualifier la gravité ([D01](../docs/D01-gravite-et-delais.md))
- [ ] Vérifier qu'une **autre attaque** n'est pas en cours en parallèle (connexions inhabituelles, alertes EDR) : le déni de service peut masquer une intrusion
- [ ] Rechercher une éventuelle demande de rançon associée (courriel, message sur un réseau social)

## 3. Confinement

- [ ] Prévenir l'**hébergeur** et l'**opérateur** et activer la protection anti-DDoS (filtrage en amont, « nettoyage » du trafic)
- [ ] Appliquer des mesures locales : limitation du nombre de requêtes par source, règles de pare-feu applicatif, blocage géographique si le service n'a pas d'utilisateurs légitimes dans ces pays
- [ ] Activer la mise en cache ou une page statique de secours pour les pages les plus demandées
- [ ] Protéger en priorité les services essentiels (accès des salariés, paiement, prise de commande)
- [ ] Ne pas répondre à une éventuelle demande de rançon : décision de la direction, instruite par le juridique ([D03](../docs/D03-matrice-raci.md))

## 4. Preuves

- [ ] Conserver des échantillons de trafic (captures limitées, journaux de flux) et les journaux du pare-feu, de l'équilibreur et du serveur web
- [ ] Récupérer auprès de l'hébergeur et de l'opérateur leurs relevés de l'attaque (volumes, sources, horaires)
- [ ] Conserver toute demande de rançon ou revendication, avec son horodatage ([D05](../docs/D05-preservation-des-preuves.md))

## 5. Éradication

- [ ] Corriger ce qui a rendu le service vulnérable : serveur DNS ou NTP ouvert utilisé comme amplificateur, fonction coûteuse sans limitation, absence de cache
- [ ] Maintenir les règles de filtrage tant que l'attaque peut reprendre ; les attaques par vagues sont courantes
- [ ] Vérifier que l'infrastructure de l'entreprise ne participe pas elle-même à des attaques (machines compromises, services ouverts)

## 6. Restauration

- [ ] Lever progressivement les mesures d'urgence qui gênent les utilisateurs légitimes (blocages géographiques, pages de secours)
- [ ] Vérifier le bon fonctionnement de chaque service et les temps de réponse
- [ ] Surveiller de près pendant au moins 7 jours : une nouvelle vague est fréquente

## 7. Obligations et communication

- [ ] Entités NIS 2 : une indisponibilité grave d'un service est un incident potentiellement important (alerte précoce sous 24 heures, [D04](../docs/D04-cadre-reglementaire.md), §3)
- [ ] Porter plainte (entrave au fonctionnement d'un système, article 323-2 du Code pénal), sous 72 heures si l'organisation veut être indemnisée par son assurance ([D04](../docs/D04-cadre-reglementaire.md), §4)
- [ ] Informer les clients et utilisateurs de l'indisponibilité et de son rétablissement, par les personnes désignées ([D03](../docs/D03-matrice-raci.md))
- [ ] Vérifier les engagements contractuels de disponibilité (envers les clients, de la part de l'hébergeur)

## 8. Clôture

- [ ] Le trafic est revenu à la normale depuis au moins 24 heures
- [ ] Les services sont rétablis et les mesures d'urgence gênantes levées
- [ ] Aucune intrusion parallèle n'a été trouvée, ou elle a son propre dossier
- [ ] Rapport d'incident complet (durée, volumes, impact, actions) et retour d'expérience réalisés
- [ ] Le contrat de protection anti-DDoS et l'annuaire de crise sont revus si nécessaire

## Arbre de décision

```text
Service lent ou indisponible
  │
  ├─ Cause légitime (pic attendu, panne, mise à jour) ? ── OUI → gestion de la capacité ou de la panne
  │
  └─ NON → attaque probable
            │
            ├─ Prévenir l'hébergeur et l'opérateur → activer la protection anti-DDoS
            ├─ Mesures locales : limitation, filtrage, cache, page de secours
            │
            ├─ Autre attaque en parallèle ? ── OUI → ouvrir un dossier séparé (P01, P05…)
            ├─ Demande de rançon ?          ── OUI → ne pas répondre, juridique et direction
            │
            └─ Service essentiel coupé ? ── OUI → S1, escalade immédiate
                                          └─ NON → S2 ou S3 selon l'impact
```

## Techniques MITRE ATT&CK

| Technique | Nom | Où l'observer |
|---|---|---|
| [T1498.001](https://attack.mitre.org/techniques/T1498/001/) | Network Denial of Service: Direct Network Flood | Supervision réseau, opérateur |
| [T1498.002](https://attack.mitre.org/techniques/T1498/002/) | Network Denial of Service: Reflection Amplification | Pare-feu, supervision réseau |
| [T1499.002](https://attack.mitre.org/techniques/T1499/002/) | Endpoint Denial of Service: Service Exhaustion Flood | Équilibreur de charge, serveur web |
| [T1499.003](https://attack.mitre.org/techniques/T1499/003/) | Endpoint Denial of Service: Application Exhaustion Flood | Journaux web, pare-feu applicatif |

Identifiants vérifiés dans MITRE ATT&CK Enterprise **v20.1**.
