---
id: T03
lang: fr
title: Communication de crise
review: 2026-11-07
---

# T03 — Communication de crise

[↑ Modèles](README.md)

Des messages types à adapter, pour ne pas rédiger dans l'urgence. Seules les personnes désignées dans
la [RACI](../docs/D03-matrice-raci.md) envoient ces messages, après validation de la direction et, pour
les messages externes, du juridique.

> ✍️ **Règles d'écriture**
> - Dire **ce que l'on sait**, ce que l'on **ne sait pas encore**, ce que l'on **fait**, et **quand**
>   on reviendra vers les destinataires.
> - Ne jamais spéculer sur l'attaquant, ne jamais minimiser (« incident mineur ») avant d'en être sûr.
> - Ne pas donner de détails techniques utiles à un attaquant (systèmes non touchés, failles).
> - Si la messagerie est compromise, envoyer depuis un canal sûr ([D02](../docs/D02-escalade.md), §4).

## M1 — Alerte interne (salariés)

> **Objet : Incident informatique en cours — consignes**
>
> Bonjour à toutes et à tous,
>
> Nous faisons face depuis [heure] à un incident de sécurité informatique qui touche [périmètre :
> messagerie, serveur de fichiers, certains postes…]. Nos équipes et [prestataire, le cas échéant]
> sont mobilisées.
>
> **En attendant de nouvelles consignes :**
> - [n'éteignez pas votre poste / déconnectez votre poste du réseau] ;
> - n'utilisez pas [service touché] ;
> - signalez tout comportement anormal au [numéro de téléphone du support] ;
> - ne communiquez **aucune** information sur cet incident à l'extérieur, y compris sur les réseaux
>   sociaux ; orientez toute question externe vers [nom de la personne désignée].
>
> Prochain point d'information : [date et heure], par [canal].
>
> [Nom, fonction]

## M2 — Information des clients et partenaires

> **Objet : Information concernant un incident de sécurité**
>
> Madame, Monsieur,
>
> Le [date], [nom de l'entreprise] a détecté un incident de sécurité informatique affectant
> [services concernés]. Nous avons immédiatement [mesures : isolé les systèmes, mobilisé des
> experts, informé les autorités compétentes].
>
> À ce stade, [ce que l'on sait de l'impact pour le destinataire : service indisponible, données
> concernées ou non]. Nos investigations se poursuivent.
>
> **Par précaution :** toute demande de modification de coordonnées bancaires ou de paiement
> inhabituel provenant de notre part doit être vérifiée par téléphone au [numéro déjà connu].
>
> Nous reviendrons vers vous au plus tard le [date]. Pour toute question : [contact dédié].
>
> [Nom, fonction]

## M3 — Information des personnes concernées par une violation de données (RGPD, article 34)

Ce message est **obligatoire en cas de risque élevé** pour les personnes ([D04](../docs/D04-cadre-reglementaire.md),
§2). Il doit être rédigé **en termes clairs et simples** et contenir au moins : la nature de la
violation, le contact du délégué à la protection des données, les conséquences probables et les
mesures prises ou proposées.

> **Objet : Information importante concernant vos données personnelles**
>
> Madame, Monsieur,
>
> **Ce qui s'est passé.** Le [date], nous avons découvert que [description simple : un tiers a pu
> accéder à…].
>
> **Les données concernées.** [Liste précise : nom, adresse électronique, numéro de téléphone…].
> [Ne sont pas concernées : …].
>
> **Les risques pour vous.** [Exemples concrets : courriels ou appels frauduleux se faisant passer
> pour nous, tentative d'usurpation d'identité…].
>
> **Ce que nous avons fait.** [Mesures : accès fermé, mots de passe réinitialisés, autorités
> informées, plainte déposée].
>
> **Ce que nous vous conseillons.** [Actions concrètes : changer votre mot de passe sur notre service
> et sur tout service où vous utilisiez le même ; vous méfier des messages qui demandent vos
> coordonnées bancaires ; …]. Nous ne vous demanderons **jamais** votre mot de passe.
>
> **Pour toute question**, notre délégué à la protection des données est joignable à [adresse ou
> formulaire dédié]. Vous pouvez également adresser une réclamation à la CNIL.
>
> [Nom, fonction]

## M4 — Déclaration à la presse

> [Nom de l'entreprise] a détecté le [date] un incident de cybersécurité affectant [périmètre
> général]. Dès sa détection, nos équipes ont pris les mesures nécessaires pour [contenir l'incident
> et protéger nos clients], avec l'appui de [prestataire / autorités]. [Les autorités compétentes
> ont été informées et une plainte a été déposée.]
>
> [Impact sur les clients : services rétablis / en cours de rétablissement, données concernées ou
> non à ce stade.] Les investigations se poursuivent ; nous communiquerons de nouveau dès que nous
> disposerons d'informations vérifiées.
>
> Contact presse : [nom, téléphone, adresse].

## Suivi des communications

| Date et heure (UTC) | Message (M1 à M4) | Destinataires | Canal | Validé par | Envoyé par |
|---|---|---|---|---|---|
| | | | | | |
