# Politique de sécurité

## Signaler un problème

Merci de **ne pas ouvrir d'issue publique** pour une faille de l'outillage ou une erreur de
procédure qui pourrait aggraver un incident réel.

Utilisez le signalement privé de GitHub : onglet **Security** du dépôt → **Report a vulnerability**
(disponible une fois le dépôt public).

## Ce qui est concerné

- une consigne d'un playbook qui détruirait des preuves, propagerait une attaque ou ferait courir
  un risque juridique (par exemple un délai de notification erroné) ;
- une faiblesse de l'outil `playbook-check` (lecture de fichiers hors du dépôt, etc.).

## Données sensibles

Ce dépôt ne contient que des **modèles**. N'y publiez jamais un rapport rempli lors d'un vrai
incident : noms, adresses IP, preuves et chronologies sont des informations sensibles.
Le fichier `.gitignore` exclut par précaution le dossier `incidents/` et les fichiers de preuves
courants (`.evtx`, `.pcap`, `.mem`, `.dmp`).

## Délais

Projet personnel maintenu sur le temps libre : accusé de réception visé sous 7 jours.
