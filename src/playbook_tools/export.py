"""
Export des playbooks au format JSON (commande « playbook-export »).

Transforme la documentation d'une langue en un document JSON structuré, lisible par d'autres
outils : l'interface web du dépôt, un outil de ticketing, un tableau de bord SOC… On y trouve :
  - chaque playbook avec ses métadonnées, son paragraphe « Quand l'utiliser », les noms officiels
    de ses techniques MITRE ATT&CK et ses actions à cocher, regroupées par section numérotée ;
  - la grille de gravité et les délais internes de D01 ;
  - les obligations légales de D04, avec leur délai en heures quand il est chiffré.

Format (schema_version 2) : 1 + « severity », « obligations » et, par playbook, « when ».

Règle de sécurité : l'export est REFUSÉ si playbook-check trouve le moindre problème.
On ne diffuse jamais une liste d'actions incomplète ou incohérente.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from playbook_tools import __version__
from playbook_tools.check import (
    LANGUAGES,
    Document,
    attack_data,
    run_checks,
    split_sections,
)
from playbook_tools.console import setup_streams
from playbook_tools.reference import body_of, obligations_reference, plain_text, severity_reference, when_to_use

# Version du format JSON, incrémentée à chaque évolution de la structure.
# 1 : playbooks seuls. 2 : + « severity » (D01), « obligations » (D04) et « when » par playbook.
SCHEMA_VERSION = 2

# Titre de section numérotée, ligne entière : « ## 3. Confinement »
_SECTION_TITLE = re.compile(r"^## (?P<number>\d+)\. (?P<title>.+?)\s*$", flags=re.MULTILINE)
# Action à cocher : on capture TOUT le texte qui suit la case « - [ ] »
_ACTION = re.compile(r"^\s*[-*] \[ \] (?P<text>.+?)\s*$", flags=re.MULTILINE)


def section_titles(body: str) -> dict[int, str]:
    """Titre de chaque section numérotée : « ## 3. Confinement » → {3: "Confinement"}."""
    return {int(m.group("number")): plain_text(m.group("title")) for m in _SECTION_TITLE.finditer(body)}


def actions(section_text: str) -> list[str]:
    """Liste des actions à cocher d'une section, en texte simple et dans l'ordre du document."""
    return [plain_text(m.group("text")) for m in _ACTION.finditer(section_text)]


def export_playbook(doc: Document, root: Path) -> dict:
    """Représentation JSON d'un playbook déjà validé."""
    body = body_of(doc.path)
    titles = section_titles(body)
    techniques = attack_data()["techniques"]
    return {
        "id": doc.doc_id,
        "title": doc.meta["title"],
        "severity": doc.meta["severity"],
        "owner": doc.meta["owner"],
        "review": doc.meta["review"],
        "when": when_to_use(body, doc.lang),  # aide au choix du playbook (vérifiée par playbook-check)
        "mitre": [{"id": tid, "name": techniques[tid]["name"]} for tid in doc.meta["mitre"]],
        "source": _source(doc, root),  # ex. fr/playbooks/P02-rancongiciel.md
        "sections": [
            {"number": number, "title": titles[number], "actions": actions(section)}
            for number, section in sorted(split_sections(body).items())
        ],
    }


def build_export(root: Path, lang: str) -> dict:
    """Document JSON complet d'une langue. Lève ValueError si la documentation n'est pas valide."""
    documents, problems = run_checks(root)
    if problems:
        raise ValueError(f"{len(problems)} problème(s) détecté(s) par playbook-check : export refusé.")
    in_lang = [doc for doc in documents if doc.lang == lang]
    playbooks = sorted((doc for doc in in_lang if doc.kind == "playbook"), key=lambda d: d.doc_id)
    # Les deux documents de référence sont indispensables à l'interface : leur absence bloque l'export
    reference = {doc.doc_id: doc for doc in in_lang if doc.kind == "doc" and doc.doc_id in ("D01", "D04")}
    for missing in sorted({"D01", "D04"} - reference.keys()):
        raise ValueError(f"document de référence {missing} absent en « {lang} » : export refusé.")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_version": __version__,
        "attack_version": attack_data()["attack_version"],
        "lang": lang,
        "severity": {**severity_reference(body_of(reference["D01"].path)), "source": _source(reference["D01"], root)},
        "obligations": {
            "items": obligations_reference(body_of(reference["D04"].path)),
            "source": _source(reference["D04"], root),
        },
        "playbooks": [export_playbook(doc, root) for doc in playbooks],
    }


def _source(doc: Document, root: Path) -> str:
    """Chemin du document dans le dépôt, avec des « / » : fr/docs/D01-gravite-et-delais.md."""
    return doc.path.relative_to(root).as_posix()


def main(argv: list[str] | None = None) -> int:
    """Codes de retour : 0 = export réussi, 1 = documentation invalide, 2 = mauvais usage."""
    setup_streams()
    parser = argparse.ArgumentParser(
        prog="playbook-export",
        description="Exporte la documentation d'une langue au format JSON (gravité, obligations, playbooks).",
    )
    parser.add_argument("root", nargs="?", default=".", help="racine du dépôt (défaut : dossier courant)")
    parser.add_argument("--lang", choices=LANGUAGES, required=True, help="langue à exporter")
    parser.add_argument("-o", "--output", type=Path, help="fichier de sortie (défaut : sortie standard)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / "fr").is_dir() or not (root / "en").is_dir():
        print(f"Erreur : « {root} » ne contient pas les dossiers fr/ et en/.", file=sys.stderr)
        return 2
    try:
        document = build_export(root, args.lang)
    except ValueError as exc:
        print(f"Erreur : {exc} Lancez playbook-check pour le détail.", file=sys.stderr)
        return 1

    text = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        count = sum(len(s["actions"]) for p in document["playbooks"] for s in p["sections"])
        print(f"{len(document['playbooks'])} playbook(s), {count} action(s) → {args.output}")
    else:
        sys.stdout.write(text)
    return 0
