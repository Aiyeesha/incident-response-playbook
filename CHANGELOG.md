# Journal des modifications

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionnage [sémantique](https://semver.org/lang/fr/).

Ce dépôt reprend et fusionne deux anciens dépôts (`incident-response-playbook` en anglais et
`playbook-reponse-incidents` en français), archivés en privé.

## [Non publié]

### Ajouté
- README FR/EN : badges (vérifications, Python, dépendances, version ATT&CK, licence) et capture d'une
  exécution réelle de `playbook-check` et `playbook-export` (`assets/playbook-check.png`).

## [1.0.0] — 2026-11-07

Première version stable.

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
- Playbooks P01 (infection par logiciel malveillant), P02 (rançongiciel) et P03 (fuite de données),
  en français et en anglais : 8 sections numérotées (détection, triage, confinement, preuves,
  éradication, restauration, obligations et communication, clôture), arbre de décision et
  techniques MITRE ATT&CK avec leurs sources d'observation.
- Liste officielle des techniques MITRE ATT&CK Enterprise (v20.1) embarquée dans le paquet et script
  `scripts/update_attack_data.py` pour la régénérer à partir des données STIX de MITRE.
- `playbook-check` : techniques inconnues, révoquées (avec leur remplaçant) ou dépréciées refusées ;
  structure en 8 sections numérotées imposée aux playbooks, avec une action à cocher dans chaque
  section 2 à 8 ; chaque technique de la fiche doit être citée dans le texte.
- Playbooks P04 (hameçonnage), P05 (accès non autorisé), P06 (déni de service) et P07 (compte
  compromis et fraude au virement, nouveau), en français et en anglais, et tableau « Par où
  commencer ? » dans l'index des playbooks.
- Modèles, en français et en anglais : T01 rapport d'incident (repères de temps pour le MTTD et le
  MTTR, journal des actions, suivi des obligations), T02 post-mortem sans recherche de coupable
  (« 5 pourquoi », plan d'action), T03 communication de crise (salariés, clients, personnes concernées
  selon l'article 34 du RGPD, presse), T04 registre de preuves (inventaire, chaîne de custody,
  restitution).
- D06 — exercice sur table : scénario de rançongiciel en 9 injections, délais légaux à surveiller et
  grille d'évaluation. D05 renvoie désormais au registre de preuves T04.
- Version anglaise complète de toute la documentation (playbooks, documents, modèles, index).
- Commande `playbook-export` : export JSON des playbooks d'une langue (métadonnées, noms officiels
  des techniques MITRE ATT&CK, actions à cocher regroupées par section), refusé si `playbook-check`
  trouve un problème. L'export des deux langues est vérifié en CI et joint à chaque version publiée.
- P04 : signalement des SMS et appels indésirables au 33700, par transfert du SMS ou via le
  formulaire de 33700.fr.

### Corrigé
- Accents illisibles dans la sortie des commandes sous Windows lorsqu'elle est redirigée vers un
  fichier ou un autre programme : la sortie est désormais toujours écrite en UTF-8.
