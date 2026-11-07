# Journal des modifications

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionnage [sémantique](https://semver.org/lang/fr/).

Ce dépôt reprend et fusionne deux anciens dépôts (`incident-response-playbook` en anglais et
`playbook-reponse-incidents` en français), archivés en privé.

## [Non publié]

### Ajouté
- Ossature : documentation bilingue `fr/` et `en/` (playbooks, documents de référence, modèles).
- Outil `playbook-check` (paquet `playbook_tools`, sans dépendance) : fiche structurée obligatoire
  en tête de chaque document (sous-ensemble strict de YAML), champs obligatoires et inconnus,
  identifiant cohérent avec le nom du fichier, langue cohérente avec le dossier, date de révision,
  gravités S1–S4, techniques MITRE ATT&CK, parité FR/EN des métadonnées partagées, liens internes.
- Intégration continue GitHub Actions (vérification de la documentation, tests, Ruff) et Dependabot.
- README bilingue, politique de sécurité, licence MIT.
- Socle commun, en français et en anglais :
  - D01 — gravité et délais : niveaux S1 à S4 selon cinq critères (le plus grave l'emporte),
    délais de prise en charge, d'escalade, de confinement et de point de situation ;
  - D02 — escalade : niveaux N1 à N5, déclencheurs d'escalade immédiate, arbre de décision,
    règles de communication hors bande, annuaire de crise à compléter ;
  - D03 — matrice RACI : 9 rôles, 18 activités, un seul « A » par activité ;
  - D04 — cadre réglementaire : RGPD (art. 33 et 34, registre des violations), NIS 2 (art. 23 :
    24 h, 72 h, 1 mois ; transposition française signalée comme en cours), plainte sous 72 h pour
    l'indemnisation par l'assurance (Code des assurances, art. L. 12-10-1), contacts publics
    (17Cyber, Cybermalveillance.gouv.fr, CERT-FR, CNIL) et sources officielles ;
  - D05 — préservation des preuves : principes et ordre de volatilité de la RFC 3227, erreurs à
    éviter, empreintes SHA-256, chaîne de custody.
