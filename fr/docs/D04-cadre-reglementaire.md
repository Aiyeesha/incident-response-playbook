---
id: D04
lang: fr
title: Cadre réglementaire et signalements
review: 2026-11-07
---

# D04 — Cadre réglementaire et signalements

[↑ Documents de référence](README.md)

Un incident de cybersécurité est aussi un **événement juridique**. Plusieurs obligations peuvent
s'appliquer **en même temps**, chacune avec son propre délai, qui court souvent pendant que l'équipe
technique est encore en plein confinement. Ce document les rassemble pour qu'aucune ne soit oubliée.

> ⚠️ **Ce document n'est pas un avis juridique.** Il donne des repères vérifiés à la date de révision
> indiquée en tête, avec la source officielle de chaque obligation. Avant toute notification,
> faites valider la démarche par votre juridique ou votre DPO.

## 1. Vue d'ensemble des délais

| Obligation | Qui est concerné | Délai | Destinataire |
|---|---|---|---|
| Violation de données personnelles (RGPD, art. 33) | Tout responsable de traitement | **72 heures** après en avoir pris connaissance, si la violation présente un risque | CNIL |
| Information des personnes (RGPD, art. 34) | Tout responsable de traitement | Dans les meilleurs délais, si le risque est **élevé** | Personnes concernées |
| Registre des violations (RGPD, art. 33.5) | Tout responsable de traitement | **Toujours**, même sans notification | Document interne |
| Alerte précoce NIS 2 (directive, art. 23) | Entités essentielles et importantes | **24 heures** après avoir pris connaissance d'un incident important | CSIRT ou autorité compétente |
| Notification d'incident NIS 2 | Idem | **72 heures** | Idem |
| Rapport final NIS 2 | Idem | **1 mois** après la notification | Idem |
| Plainte pour être indemnisé (Code des assurances, art. L. 12-10-1) | Professionnels assurés contre le risque cyber | **72 heures** après la connaissance de l'atteinte | Police, gendarmerie ou procureur |

Ces délais **ne se remplacent pas** : une même attaque par rançongiciel avec vol de données peut
exiger, dans la même semaine, une notification à la CNIL, une alerte NIS 2, une plainte et une
déclaration à l'assureur.

## 2. RGPD : violation de données personnelles

**Qu'est-ce qu'une violation ?** Toute destruction, perte, altération, divulgation ou tout accès non
autorisé à des données personnelles, qu'il soit accidentel ou malveillant. Un rançongiciel qui
chiffre un fichier client est une violation (perte de disponibilité), même sans vol.

| Étape | Ce que dit la CNIL |
|---|---|
| **Évaluer le risque** | Pas de risque pour les droits et libertés des personnes : pas de notification, mais documentation interne obligatoire. **En cas de doute, notifier.** |
| **Notifier sous 72 heures** | Dans les meilleurs délais et, si possible, dans les 72 heures suivant la constatation. Au-delà, expliquer les motifs du retard. |
| **Notifier en plusieurs temps** | Une notification initiale, puis une notification complémentaire dès que les informations manquantes sont connues. |
| **Informer les personnes** | Obligatoire en cas de **risque élevé**. La CNIL peut l'imposer si ce n'est pas fait. |
| **Documenter** | **Toutes** les violations, notifiées ou non : nature, catégories et nombre approximatif de personnes et d'enregistrements, conséquences probables, mesures prises. |

**Comment notifier :** le téléservice de la CNIL, réservé aux responsables de traitement
(lien en section 6). Un document préparatoire permet de rassembler les informations à l'avance.

## 3. NIS 2 : incidents importants

La directive (UE) 2022/2555, dite **NIS 2**, impose aux entités **essentielles** et **importantes**
de signaler leurs **incidents importants**.

**Incident important** (article 23.3) : un incident qui a causé, ou peut causer, une perturbation
opérationnelle grave des services ou des pertes financières pour l'entité, **ou** qui a affecté, ou
peut affecter, d'autres personnes en causant des dommages matériels ou moraux considérables.

**Les échéances** (article 23.4), destinées au CSIRT ou à l'autorité compétente :

| Échéance | Contenu attendu |
|---|---|
| **24 heures** — alerte précoce | Indiquer si l'incident semble causé par un acte illicite ou malveillant, et s'il peut avoir un impact transfrontière |
| **72 heures** — notification d'incident | Mettre à jour l'alerte, donner une première évaluation (gravité, impact) et les indicateurs de compromission disponibles |
| **Sur demande** — rapport intermédiaire | Points de situation demandés par le CSIRT ou l'autorité |
| **1 mois** après la notification — rapport final | Description détaillée, cause probable, mesures appliquées, impact transfrontière éventuel |
| Si l'incident dure encore au moment du rapport final | Rapport d'avancement, puis rapport final dans le mois suivant la fin de l'incident |

> ⚠️ **Transposition française en cours.** À la date de révision de ce document, la page officielle
> de l'ANSSI présente la loi française de transposition comme un **projet de loi « Résilience »**
> encore en cours d'examen. Les modalités françaises (périmètre exact, autorité, plateforme de
> déclaration) peuvent donc encore évoluer : vérifiez la page NIS 2 de l'ANSSI avant de vous y
> fier. Depuis le 17 mars 2026, l'ANSSI publie le **Référentiel Cyber France (ReCyF)**, prévu par
> ce projet de loi.

## 4. Porter plainte

Une cyberattaque est une **infraction pénale** : les atteintes aux systèmes de traitement
automatisé de données sont prévues par les articles 323-1 à 323-3-1 du Code pénal.

- **Pourquoi porter plainte ?** Pour permettre l'enquête, pour obtenir un récépissé utile auprès des
  partenaires et des banques et, pour les professionnels assurés, **pour être indemnisé**.
- **Condition d'indemnisation par l'assurance** (article L. 12-10-1 du Code des assurances, en
  vigueur depuis le 24 avril 2023) : le versement d'une indemnité au titre d'une atteinte à un
  système d'information est subordonné à une plainte déposée **au plus tard 72 heures après la
  connaissance de l'atteinte par la victime**. Cela concerne les **personnes morales** et les
  **personnes physiques dans le cadre de leur activité professionnelle**.
- **Où ?** Au commissariat de police, à la brigade de gendarmerie, ou par écrit auprès du procureur
  de la République. Le service **17Cyber** oriente vers le bon interlocuteur.
- **Quoi apporter ?** La chronologie, les éléments techniques déjà réunis (sans altérer les preuves,
  voir [D05](D05-preservation-des-preuves.md)), et la liste des systèmes et données touchés.

## 5. Se faire aider : les contacts publics

| Service | Pour qui | Ce qu'il apporte |
|---|---|---|
| **17Cyber** (opéré par Cybermalveillance.gouv.fr, la police et la gendarmerie) | Particuliers, entreprises, collectivités | Diagnostic en ligne 24 h/24, conseils, mise en relation avec un prestataire ou avec les forces de l'ordre |
| **Cybermalveillance.gouv.fr** | Particuliers, entreprises, collectivités | Fiches réflexes, annuaire de prestataires labellisés |
| **CERT-FR (ANSSI)** | En priorité : État, opérateurs d'importance vitale et de services essentiels ; peut intervenir sur tout le territoire | Déclaration d'incident en ligne ; assistance immédiate par téléphone au **3218** (ou +33 9 70 83 32 18) ou par courriel à cert-fr@ssi.gouv.fr |
| **CNIL** | Responsables de traitement | Téléservice de notification des violations de données |

## 6. Sources officielles

- RGPD — [notifier une violation de données personnelles (CNIL)](https://www.cnil.fr/fr/notifier-une-violation-de-donnees-personnelles)
- NIS 2 — [texte de la directive (UE) 2022/2555 (EUR-Lex)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) et
  [page NIS 2 de l'ANSSI](https://cyber.gouv.fr/reglementation/cybersecurite-systemes-dinformation/directives-nis-nis2-et-dispositif-saiv/directive-nis-2/)
- CERT-FR — [en cas d'incident (ANSSI)](https://cyber.gouv.fr/en-cas-dincident)
- Assurance — article L. 12-10-1 du Code des assurances, issu de la loi n° 2023-22 du 24 janvier 2023 :
  [FAQ de la Direction générale du Trésor sur l'obligation de dépôt de plainte](https://www.tresor.economie.gouv.fr/Institutionnel/Niveau2/Pages/39db1de3-1230-46a0-8e1b-d38a739e0885/files/9065d98f-099e-4eb4-9ba5-23b68cd50feb)
- 17Cyber — [17cyber.gouv.fr](https://17cyber.gouv.fr)
- Cybermalveillance — [cybermalveillance.gouv.fr](https://www.cybermalveillance.gouv.fr)

> 🗓️ **À revoir à chaque révision du document** : l'état de la transposition de NIS 2 en France et
> les plateformes de déclaration associées.
