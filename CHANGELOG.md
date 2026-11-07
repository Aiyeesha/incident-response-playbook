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
