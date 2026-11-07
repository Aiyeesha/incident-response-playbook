"""
Export des playbooks au format JSON (commande « playbook-export »).

Transforme les playbooks Markdown d'une langue en un document JSON structuré, lisible par
d'autres outils : un outil de ticketing, un tableau de bord SOC, la page /admin/incidents du
portfolio… Chaque playbook y apparaît avec ses métadonnées, les noms officiels de ses
techniques MITRE ATT&CK et ses actions à cocher, regroupées par section numérotée.

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
    parse_front_matter,
    run_checks,
    split_sections,
)
from playbook_tools.console import setup_streams

# Version du format JSON produit : à incrémenter si la structure change de façon incompatible
SCHEMA_VERSION = 1

# Nettoyage du Markdown pour obtenir un texte simple
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")  # [texte](cible) → texte
_EMPHASIS = re.compile(r"\*\*|__|`")  # gras et code en ligne
# Titre de section numérotée, ligne entière : « ## 3. Confinement »
_SECTION_TITLE = re.compile(r"^## (?P<number>\d+)\. (?P<title>.+?)\s*$", flags=re.MULTILINE)
# Action à cocher : on capture TOUT le texte qui suit la case « - [ ] »
_ACTION = re.compile(r"^\s*[-*] \[ \] (?P<text>.+?)\s*$", flags=re.MULTILINE)


def plain_text(markdown: str) -> str:
    """Texte lisible sans syntaxe Markdown : liens réduits à leur texte, gras et code retirés."""
    return _EMPHASIS.sub("", _LINK.sub(r"\1", markdown)).strip()


def section_titles(body: str) -> dict[int, str]:
    """Titre de chaque section numérotée : « ## 3. Confinement » → {3: "Confinement"}."""
    return {int(m.group("number")): plain_text(m.group("title")) for m in _SECTION_TITLE.finditer(body)}


def actions(section_text: str) -> list[str]:
    """Liste des actions à cocher d'une section, en texte simple et dans l'ordre du document."""
    return [plain_text(m.group("text")) for m in _ACTION.finditer(section_text)]


def export_playbook(doc: Document, root: Path) -> dict:
    """Représentation JSON d'un playbook déjà validé."""
    text = doc.path.read_text(encoding="utf-8")
    _meta, body_start = parse_front_matter(text)
    body = "\n".join(text.splitlines()[body_start - 1 :])
    titles = section_titles(body)
    techniques = attack_data()["techniques"]
    return {
        "id": doc.doc_id,
        "title": doc.meta["title"],
        "severity": doc.meta["severity"],
        "owner": doc.meta["owner"],
        "review": doc.meta["review"],
        "mitre": [{"id": tid, "name": techniques[tid]["name"]} for tid in doc.meta["mitre"]],
        "source": doc.path.relative_to(root).as_posix(),  # ex. fr/playbooks/P02-rancongiciel.md
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
    playbooks = sorted(
        (doc for doc in documents if doc.kind == "playbook" and doc.lang == lang), key=lambda d: d.doc_id
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_version": __version__,
        "attack_version": attack_data()["attack_version"],
        "lang": lang,
        "playbooks": [export_playbook(doc, root) for doc in playbooks],
    }


def main(argv: list[str] | None = None) -> int:
    """Codes de retour : 0 = export réussi, 1 = documentation invalide, 2 = mauvais usage."""
    setup_streams()
    parser = argparse.ArgumentParser(
        prog="playbook-export",
        description="Exporte les playbooks d'une langue au format JSON (actions à cocher par section).",
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
