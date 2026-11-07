"""
Vérification de la documentation (commande « playbook-check »).

Chaque document des dossiers fr/ et en/ commence par une courte FICHE STRUCTURÉE
(« front matter ») entre deux lignes « --- ». Exemple :

    ---
    id: P02
    lang: fr
    title: Attaque par rançongiciel
    severity: [S1]
    mitre: [T1486, T1490]
    owner: Responsable SOC
    review: 2026-11-07
    ---

Ce module vérifie, sans aucune dépendance externe :
  1. que chaque fiche est complète, sans champ inconnu, et que ses valeurs sont valides ;
  2. que le nom du fichier correspond à son identifiant, et le dossier à sa langue ;
  3. que les versions française et anglaise existent toutes les deux et partagent
     les mêmes métadonnées non traduites (gravité, techniques MITRE…) ;
  4. qu'aucun lien relatif d'un fichier Markdown ne pointe vers un fichier absent.

Pourquoi un sous-ensemble de YAML et pas une bibliothèque YAML ?
  - GitHub affiche une fiche YAML sous forme de tableau en tête du document : c'est lisible ;
  - Python ne lit pas le YAML sans bibliothèque externe, et ce dépôt n'en veut aucune ;
  - YAML complet est notoirement piégeux (« no » lu comme False, dates implicites…).
Le format accepté est donc volontairement minuscule : « clé: valeur » et « clé: [a, b] ».
Tout le reste est REFUSÉ avec un message clair, plutôt que deviné.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date
from functools import cache
from importlib import resources
from pathlib import Path

from playbook_tools.console import setup_streams

# ─────────────────────────────────────────────────────────────
# 1. Règles du format
# ─────────────────────────────────────────────────────────────

LANGUAGES = ("fr", "en")  # une version par langue, obligatoirement

# Type de document → (dossier, préfixe d'identifiant)
KINDS = {
    "playbook": ("playbooks", "P"),
    "doc": ("docs", "D"),
    "template": ("templates", "T"),
}

# Champs obligatoires et autorisés par type de document
COMMON_FIELDS = {"id", "lang", "title", "review"}
REQUIRED_FIELDS = {
    "playbook": COMMON_FIELDS | {"severity", "mitre", "owner"},
    "doc": COMMON_FIELDS,
    "template": COMMON_FIELDS,
}
# Champs dont la valeur est une liste « [a, b] »
LIST_FIELDS = {"severity", "mitre"}
# Champs identiques en français et en anglais (ils ne se traduisent pas)
SHARED_FIELDS = {"id", "severity", "mitre"}

SEVERITIES = ("S1", "S2", "S3", "S4")  # S1 = critique … S4 = faible (voir D01)

# Formes acceptées
FILE_NAME = re.compile(r"(?P<id>[PDT]\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md")  # ex. P02-rancongiciel.md
MITRE_ID = re.compile(r"T\d{4}(?:\.\d{3})?")  # technique ou sous-technique : T1486, T1110.003
KEY_LINE = re.compile(r"(?P<key>[a-z_]+):(?:[ ]+(?P<value>.*))?")
# Lien Markdown en ligne : [texte](cible) — on ignore les images et liens externes plus bas
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")

# Structure imposée à tout playbook : 8 sections numérotées, dans cet ordre, identiques en FR et en EN
# (le titre de chaque section est traduit, son numéro ne change jamais ; l'export JSON s'appuie dessus).
#   1 Détection · 2 Triage · 3 Confinement · 4 Preuves · 5 Éradication · 6 Restauration
#   7 Obligations et communication · 8 Clôture
PLAYBOOK_SECTIONS = range(1, 9)
# Sections qui doivent contenir au moins une action à cocher (la section 1 décrit les signaux)
ACTION_SECTIONS = range(2, 9)
SECTION_HEADING = re.compile(r"^## (?P<number>\d+)\. \S", flags=re.MULTILINE)
CHECKBOX = re.compile(r"^\s*[-*] \[ \] \S", flags=re.MULTILINE)

# Dossiers jamais parcourus lors du contrôle des liens
SKIP_DIRS = {".git", ".venv", "node_modules", "build", "dist", ".pytest_cache", ".ruff_cache"}


# ─────────────────────────────────────────────────────────────
# 2. Structures de données
# ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Problem:
    """Un problème détecté, rattaché à un fichier (et à une ligne si possible)."""

    path: Path
    message: str
    line: int | None = None

    def render(self, root: Path) -> str:
        """Format « chemin:ligne: message », reconnu par les éditeurs et la CI."""
        try:
            shown = self.path.relative_to(root).as_posix()
        except ValueError:
            shown = self.path.as_posix()
        where = f"{shown}:{self.line}" if self.line else shown
        return f"{where}: {self.message}"


@dataclass
class Document:
    """Un document de la documentation, avec sa fiche déjà lue."""

    path: Path
    kind: str
    lang: str
    meta: dict[str, str | list[str]] = field(default_factory=dict)

    @property
    def doc_id(self) -> str:
        return str(self.meta.get("id", ""))


class FrontMatterError(ValueError):
    """Fiche mal formée ; « line » est le numéro de ligne dans le fichier."""

    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


@cache
def attack_data() -> dict:
    """
    Liste officielle des techniques MITRE ATT&CK, embarquée dans le paquet
    (générée par scripts/update_attack_data.py). Lue une seule fois grâce au cache.
    """
    text = resources.files("playbook_tools").joinpath("data", "attack-enterprise.json").read_text(encoding="utf-8")
    return json.loads(text)


def check_technique(technique: str) -> str | None:
    """Renvoie un message d'erreur si la technique n'existe pas ou n'est plus active, sinon None."""
    data = attack_data()
    entry = data["techniques"].get(technique)
    version = data["attack_version"]
    if entry is None:
        return f"technique « {technique} » inconnue dans MITRE ATT&CK {version}"
    if entry["status"] == "revoked":
        hint = f", remplacée par {entry['replaced_by']}" if entry.get("replaced_by") else ""
        return f"technique « {technique} » ({entry['name']}) révoquée dans ATT&CK {version}{hint}"
    if entry["status"] == "deprecated":
        return f"technique « {technique} » ({entry['name']}) dépréciée dans ATT&CK {version}"
    return None


# ─────────────────────────────────────────────────────────────
# 3. Lecture de la fiche (sous-ensemble strict de YAML)
# ─────────────────────────────────────────────────────────────


def _parse_scalar(raw: str, line: int) -> str:
    """Valeur simple : texte brut, ou entre guillemets doubles s'il contient des signes spéciaux."""
    value = raw.strip()
    if value.startswith('"'):
        if len(value) < 2 or not value.endswith('"') or '"' in value[1:-1]:
            raise FrontMatterError("guillemets mal fermés", line)
        return value[1:-1]
    # Ces caractères ont un sens particulier en YAML : on exige des guillemets pour lever toute ambiguïté
    if value and (value[0] in "[]{}&*!|>'%@`#" or ": " in value or " #" in value):
        raise FrontMatterError(f"valeur ambiguë « {value} » : mettez-la entre guillemets doubles", line)
    return value


def parse_front_matter(text: str) -> tuple[dict[str, str | list[str]], int]:
    """
    Lit la fiche en tête d'un document.

    Renvoie (champs, numéro de la ligne qui suit la fiche).
    Lève FrontMatterError si la fiche est absente ou mal formée.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontMatterError("fiche absente : le fichier doit commencer par une ligne « --- »", 1)

    meta: dict[str, str | list[str]] = {}
    for index, raw_line in enumerate(lines[1:], start=2):
        stripped = raw_line.strip()
        if stripped == "---":  # fin de la fiche
            return meta, index + 1
        if not stripped or stripped.startswith("#"):  # ligne vide ou commentaire
            continue
        if raw_line[0] in " \t":
            raise FrontMatterError("indentation interdite : une clé par ligne, sans imbrication", index)

        match = KEY_LINE.fullmatch(raw_line.rstrip())
        if not match or match.group("value") is None:
            raise FrontMatterError("ligne invalide : format attendu « clé: valeur »", index)
        key, value = match.group("key"), match.group("value").strip()
        if key in meta:
            raise FrontMatterError(f"clé « {key} » répétée", index)

        if value.startswith("["):
            # Liste en ligne : [a, b, c] — éléments simples uniquement
            if not value.endswith("]"):
                raise FrontMatterError(f"liste « {key} » mal fermée", index)
            inner = value[1:-1].strip()
            items = [_parse_scalar(item, index) for item in inner.split(",")] if inner else []
            if any(not item for item in items):
                raise FrontMatterError(f"élément vide dans la liste « {key} »", index)
            meta[key] = items
        else:
            meta[key] = _parse_scalar(value, index)

    raise FrontMatterError("fiche non terminée : ligne « --- » de fin manquante", len(lines))


# ─────────────────────────────────────────────────────────────
# 4. Contrôle d'un document
# ─────────────────────────────────────────────────────────────


def check_metadata(doc: Document, today: date) -> list[Problem]:
    """Vérifie les champs de la fiche d'un document déjà lu."""
    problems: list[Problem] = []
    meta = doc.meta

    def problem(message: str) -> None:
        problems.append(Problem(doc.path, message, 1))

    # ── Champs manquants ou inconnus (une faute de frappe crée un champ inconnu) ──
    required = REQUIRED_FIELDS[doc.kind]
    for missing in sorted(required - meta.keys()):
        problem(f"champ obligatoire manquant : « {missing} »")
    for unknown in sorted(meta.keys() - required):
        problem(f"champ inconnu : « {unknown} »")

    # ── Forme des valeurs : liste là où on l'attend, texte ailleurs, jamais vide ──
    for key, value in meta.items():
        if key in LIST_FIELDS and not isinstance(value, list):
            problem(f"« {key} » doit être une liste : [a, b]")
        elif key not in LIST_FIELDS and isinstance(value, list):
            problem(f"« {key} » doit être une valeur simple, pas une liste")
        elif not value:
            problem(f"« {key} » est vide")

    # ── Identifiant cohérent avec le nom du fichier et le type de document ──
    name_match = FILE_NAME.fullmatch(doc.path.name)
    expected_prefix = KINDS[doc.kind][1]
    if not name_match:
        problem("nom de fichier invalide : attendu « P01-mot-cle.md » (minuscules, chiffres et tirets)")
    elif meta.get("id") != name_match.group("id"):
        problem(f"« id » ({meta.get('id')}) différent du préfixe du fichier ({name_match.group('id')})")
    if isinstance(meta.get("id"), str) and not str(meta["id"]).startswith(expected_prefix):
        problem(f"un document du dossier « {KINDS[doc.kind][0]} » doit avoir un identifiant en {expected_prefix}…")

    # ── Langue cohérente avec le dossier ──
    if meta.get("lang") not in (None, doc.lang):
        problem(f"« lang » ({meta.get('lang')}) ne correspond pas au dossier « {doc.lang}/ »")

    # ── Date de révision : format AAAA-MM-JJ, réelle, pas dans le futur ──
    review = meta.get("review")
    if isinstance(review, str) and review:
        try:
            reviewed = date.fromisoformat(review)
        except ValueError:
            problem(f"« review » invalide ({review}) : format attendu AAAA-MM-JJ")
        else:
            if len(review) != 10:
                problem(f"« review » invalide ({review}) : format attendu AAAA-MM-JJ")
            elif reviewed > today:
                problem(f"« review » ({review}) est dans le futur")

    # ── Gravités et techniques MITRE ATT&CK (playbooks) ──
    severity = meta.get("severity")
    if isinstance(severity, list):
        for level in severity:
            if level not in SEVERITIES:
                problem(f"gravité inconnue « {level} » (valeurs permises : {', '.join(SEVERITIES)})")
        if len(set(severity)) != len(severity):
            problem("« severity » contient un doublon")
    mitre = meta.get("mitre")
    if isinstance(mitre, list):
        for technique in mitre:
            if not MITRE_ID.fullmatch(technique):
                problem(f"technique MITRE ATT&CK invalide « {technique} » (attendu : T1234 ou T1234.001)")
            elif message := check_technique(technique):
                problem(message)
        if len(set(mitre)) != len(mitre):
            problem("« mitre » contient un doublon")

    return problems


def split_sections(body: str) -> dict[int, str]:
    """Découpe le corps d'un playbook en sections numérotées « ## N. Titre » → texte de la section."""
    sections: dict[int, str] = {}
    matches = list(SECTION_HEADING.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        # La section s'arrête aussi au prochain titre de niveau 2 non numéroté (« ## Arbre de décision »)
        text = body[match.end() : end]
        next_plain = re.search(r"^## (?!\d+\. )", text, flags=re.MULTILINE)
        sections[int(match.group("number"))] = text[: next_plain.start()] if next_plain else text
    return sections


def check_playbook_body(doc: Document, body: str, first_line: int) -> list[Problem]:
    """Structure en 8 sections, actions à cocher, et techniques MITRE expliquées dans le texte."""
    problems: list[Problem] = []
    numbers = [int(m.group("number")) for m in SECTION_HEADING.finditer(body)]
    if numbers != list(PLAYBOOK_SECTIONS):
        expected = ", ".join(str(n) for n in PLAYBOOK_SECTIONS)
        found = ", ".join(str(n) for n in numbers) or "aucune"
        problems.append(
            Problem(doc.path, f"sections numérotées attendues : {expected} (trouvées : {found})", first_line)
        )
    else:
        sections = split_sections(body)
        for number in ACTION_SECTIONS:
            if not CHECKBOX.search(sections[number]):
                problems.append(Problem(doc.path, f"section {number} sans action à cocher « - [ ] »", first_line))
    techniques = doc.meta.get("mitre")
    if isinstance(techniques, list):
        for technique in techniques:
            if not re.search(rf"\b{re.escape(technique)}\b", body):
                problems.append(
                    Problem(doc.path, f"technique {technique} déclarée dans la fiche mais absente du texte")
                )
    return problems


# ─────────────────────────────────────────────────────────────
# 5. Parcours du dépôt
# ─────────────────────────────────────────────────────────────


def collect_documents(root: Path, today: date) -> tuple[list[Document], list[Problem]]:
    """Lit et vérifie individuellement chaque document de fr/ et en/."""
    documents: list[Document] = []
    problems: list[Problem] = []
    for lang in LANGUAGES:
        for kind, (folder, _prefix) in KINDS.items():
            directory = root / lang / folder
            if not directory.is_dir():
                continue
            for path in sorted(directory.iterdir()):
                # README.md sert d'index du dossier : il n'a pas de fiche
                if path.name == "README.md" or path.is_dir():
                    continue
                if path.suffix != ".md":
                    problems.append(Problem(path, "fichier inattendu : seuls les documents .md sont permis ici"))
                    continue
                text = path.read_text(encoding="utf-8")
                doc = Document(path, kind, lang)
                try:
                    doc.meta, body_start = parse_front_matter(text)
                except FrontMatterError as exc:
                    problems.append(Problem(path, f"fiche : {exc}", exc.line))
                    continue
                problems.extend(check_metadata(doc, today))
                if kind == "playbook":
                    body = "\n".join(text.splitlines()[body_start - 1 :])
                    problems.extend(check_playbook_body(doc, body, body_start))
                documents.append(doc)
    return documents, problems


def check_parity(documents: Iterable[Document]) -> list[Problem]:
    """Chaque document existe dans les deux langues, avec les mêmes métadonnées partagées."""
    problems: list[Problem] = []
    by_lang: dict[str, dict[str, Document]] = {lang: {} for lang in LANGUAGES}
    for doc in documents:
        if doc.doc_id in by_lang[doc.lang]:
            problems.append(Problem(doc.path, f"identifiant « {doc.doc_id} » déjà utilisé dans « {doc.lang}/ »"))
        else:
            by_lang[doc.lang][doc.doc_id] = doc

    reference, other = LANGUAGES
    for doc_id in sorted(by_lang[reference].keys() | by_lang[other].keys()):
        mine, theirs = by_lang[reference].get(doc_id), by_lang[other].get(doc_id)
        if mine is None or theirs is None:
            present = mine or theirs
            missing = other if theirs is None else reference
            problems.append(Problem(present.path, f"version « {missing} » manquante pour {doc_id}"))
            continue
        # Le préfixe de l'identifiant (P, D, T) fixe le type : un même id est donc du même type partout.
        # Les noms de fichiers, eux, peuvent différer (le mot-clé est traduit : rancongiciel / ransomware).
        for key in sorted(SHARED_FIELDS):
            if mine.meta.get(key) != theirs.meta.get(key):
                problems.append(
                    Problem(theirs.path, f"« {key} » diffère de la version « {reference} » ({mine.meta.get(key)})")
                )
    return problems


def iter_markdown(root: Path) -> Iterable[Path]:
    """Tous les fichiers .md du dépôt, hors dossiers techniques."""
    for path in sorted(root.rglob("*.md")):
        if not SKIP_DIRS.intersection(part for part in path.relative_to(root).parts):
            yield path


def check_links(root: Path) -> list[Problem]:
    """Aucun lien relatif ne doit pointer vers un fichier ou dossier absent."""
    problems: list[Problem] = []
    resolved_root = root.resolve()
    for path in iter_markdown(root):
        in_code = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if FENCE.match(line):  # les blocs de code ne contiennent pas de vrais liens
                in_code = not in_code
                continue
            if in_code:
                continue
            for match in MD_LINK.finditer(line):
                target = match.group("target")
                # Liens externes, ancres internes et adresses e-mail : hors périmètre
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, flags=re.IGNORECASE) or target.startswith("#"):
                    continue
                relative = target.split("#", 1)[0].split("?", 1)[0]
                destination = (path.parent / relative).resolve()
                if not destination.is_relative_to(resolved_root):
                    problems.append(Problem(path, f"lien hors du dépôt : {target}", number))
                elif not destination.exists():
                    problems.append(Problem(path, f"lien cassé : {target}", number))
    return problems


def run_checks(root: Path, today: date | None = None) -> tuple[list[Document], list[Problem]]:
    """Exécute tous les contrôles et renvoie (documents valides, problèmes)."""
    today = today or date.today()
    documents, problems = collect_documents(root, today)
    problems.extend(check_parity(documents))
    problems.extend(check_links(root))
    return documents, problems


# ─────────────────────────────────────────────────────────────
# 6. Ligne de commande
# ─────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    """Codes de retour : 0 = tout est valide, 1 = au moins un problème, 2 = mauvais usage."""
    setup_streams()
    parser = argparse.ArgumentParser(
        prog="playbook-check",
        description="Vérifie les fiches, la parité FR/EN et les liens de la documentation.",
    )
    parser.add_argument("root", nargs="?", default=".", help="racine du dépôt (défaut : dossier courant)")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / "fr").is_dir() or not (root / "en").is_dir():
        print(f"Erreur : « {root} » ne contient pas les dossiers fr/ et en/.", file=sys.stderr)
        return 2

    documents, problems = run_checks(root)
    for problem in sorted(problems, key=lambda p: (p.path.as_posix(), p.line or 0)):
        print(problem.render(root))
    status = "OK" if not problems else f"{len(problems)} problème(s)"
    print(f"{len(documents)} document(s) vérifié(s) — {status}")
    return 1 if problems else 0
