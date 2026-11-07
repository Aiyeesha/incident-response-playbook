# Playbook de réponse aux incidents

🇬🇧 [English version](README.md)

Procédures de réponse aux incidents de cybersécurité, **directement utilisables par une équipe** :
pour chaque type d'incident, qui fait quoi, dans quel ordre, avec quelles preuves à préserver
et quelles obligations à respecter.

> 🚧 **En cours de construction** (v0.1.0 — ossature). Les playbooks arrivent aux étapes 2 à 5.

## Ce que contiendra le dépôt

| Dossier | Contenu |
|---|---|
| [`fr/`](fr/) · [`en/`](en/) | La documentation complète, en français et en anglais |
| `…/playbooks/` | P01 à P07 : procédures pas à pas, par type d'incident |
| `…/docs/` | Gravité et délais, escalade, matrice RACI, cadre réglementaire, preuves, exercice sur table |
| `…/templates/` | Rapport d'incident, post-mortem, communication de crise, registre de preuves |
| [`src/playbook_tools/`](src/playbook_tools/) | Outil de vérification `playbook-check` (et, à l'étape 7, export JSON) |

## Référentiels

- **NIST SP 800-61 Rev. 3** (avril 2025), recommandations de réponse aux incidents alignées sur le
  **NIST Cybersecurity Framework 2.0** ; elle remplace la révision 2 de 2012.
- **MITRE ATT&CK** pour décrire les techniques d'attaque de chaque playbook.
- Contexte français : guides de l'**ANSSI** et du **CERT-FR**, **Cybermalveillance.gouv.fr**,
  **RGPD** (articles 33 et 34) et directive **NIS 2**.

## Feuille de route

| Étape | Contenu | État |
|---|---|---|
| 1 | Dépôt, structure, vérification automatique en CI | ✅ |
| 2 | Socle commun : gravité et délais, escalade, RACI, cadre réglementaire, preuves | ✅ |
| 3 | Playbooks P01 à P03 : logiciel malveillant, rançongiciel, fuite de données | ✅ |
| 4 | Playbooks P04 à P07 : hameçonnage, accès non autorisé, déni de service, compte compromis | ✅ |
| 5 | Modèles et exercice sur table | ✅ |
| 6 | Version anglaise complète | ⏳ |
| 7 | Export JSON des listes d'actions → **v1.0.0** | ⏳ |

## Le format d'un document

Chaque document commence par une **fiche** entre deux lignes `---`, que GitHub affiche sous forme
de tableau et que `playbook-check` vérifie :

```yaml
---
id: P02                     # P = playbook, D = document de référence, T = modèle
lang: fr                    # doit correspondre au dossier fr/ ou en/
title: Attaque par rançongiciel
severity: [S1]              # playbooks : gravités possibles, de S1 (critique) à S4 (faible)
mitre: [T1486, T1490]       # playbooks : techniques MITRE ATT&CK
owner: Responsable SOC      # playbooks : responsable de la procédure
review: 2026-11-07          # date de dernière révision (AAAA-MM-JJ)
---
```

Le format accepté est un **sous-ensemble strict** de YAML (`clé: valeur` et `clé: [a, b]`) : tout le
reste est refusé avec un message clair, pour éviter les pièges de YAML complet.

`playbook-check` vérifie aussi :

- que chaque document existe **dans les deux langues**, avec les mêmes gravités et techniques MITRE ;
- que chaque technique MITRE ATT&CK **existe et est active** dans la version officielle embarquée
  (une technique révoquée est signalée avec son remplaçant) et qu'elle est **expliquée dans le texte** ;
- que chaque playbook a ses **8 sections numérotées**, dans l'ordre, avec des actions à cocher ;
- qu'**aucun lien interne n'est cassé**.

La liste des techniques est extraite des données officielles de MITRE par
`python scripts/update_attack_data.py`, à relancer à chaque nouvelle version d'ATT&CK
(version actuelle : **20.1**).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
playbook-check          # vérifie la documentation
pytest -v               # teste l'outil de vérification
```

## Licence

[MIT](LICENSE) © Aïcha Imène Dahoumane — libre d'adaptation pour votre organisation.
