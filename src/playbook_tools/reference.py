"""
Données de référence lues DANS la documentation Markdown, pour l'export JSON et l'interface web.

Trois sources, sans aucune copie à maintenir à la main :
  - D01, section 2 : la grille de gravité (5 critères × 4 niveaux S1 à S4) ;
  - D01, section 3 : les délais internes de traitement par niveau ;
  - D04, section 1 : les obligations légales et leurs délais ;
  - chaque playbook : le paragraphe « Quand l'utiliser » qui aide à choisir le bon playbook.

Le Markdown reste la seule source de vérité. playbook-check vérifie que ces tableaux ont la forme
attendue, dans les deux langues, pour que l'export ne puisse jamais produire de données bancales.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from playbook_tools.check import SEVERITIES, Document, Problem, parse_front_matter, split_sections

# ─────────────────────────────────────────────────────────────
# 1. Texte simple et tableaux Markdown
# ─────────────────────────────────────────────────────────────

_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")  # [texte](cible) → texte
_EMPHASIS = re.compile(r"\*\*|__|`")  # gras et code en ligne
_SEPARATOR = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$")  # |---|---| sous l'en-tête
_LEVEL_HEADER = re.compile(r"^(?P<id>S[1-4]) — (?P<label>.+)$")  # « S1 — Critique »
_BOLD_START = re.compile(r"^\*\*(?P<name>[^*]+)\*\*")  # « **Confinement** (la menace…) »
# Délai chiffré en heures en DÉBUT de cellule : « **72 heures** après… » ; « **1 mois** » n'en est pas un
_HOURS = re.compile(r"^\*\*(?P<hours>\d+) (?:heures|hours)\*\*")

# Paragraphe d'aide au choix, en tête de chaque playbook
WHEN_MARKERS = {"fr": "**Quand l'utiliser :**", "en": "**When to use it:**"}


class ReferenceError(ValueError):
    """Tableau de référence absent ou mal formé ; le message dit quoi corriger."""


def plain_text(markdown: str) -> str:
    """Texte lisible sans syntaxe Markdown : liens réduits à leur texte, gras et code retirés."""
    return _EMPHASIS.sub("", _LINK.sub(r"\1", markdown)).strip()


def first_table(text: str) -> list[list[str]]:
    """Cellules (Markdown brut) du premier tableau du texte, ligne de séparation exclue."""
    rows: list[list[str]] = []
    for line in text.splitlines():
        if line.startswith("|"):
            if not _SEPARATOR.match(line):
                rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows:  # le tableau s'arrête à la première ligne qui n'en fait pas partie
            break
    return rows


def body_of(path: Path) -> str:
    """Corps d'un document, sans sa fiche (front matter)."""
    text = path.read_text(encoding="utf-8")
    _meta, start = parse_front_matter(text)
    return "\n".join(text.splitlines()[start - 1 :])


def bold_name(cell: str) -> str:
    """Nom court d'une ligne : la partie en gras du début de cellule, sinon toute la cellule."""
    match = _BOLD_START.match(cell)
    return match.group("name").strip() if match else plain_text(cell)


# ─────────────────────────────────────────────────────────────
# 2. D01 — grille de gravité et délais internes
# ─────────────────────────────────────────────────────────────


def _level_table(body: str, number: int, what: str) -> tuple[list[dict], list[dict]]:
    """Tableau « nom | S1 — … | S2 — … | S3 — … | S4 — … » de la section « ## number. »."""
    table = first_table(split_sections(body).get(number, ""))
    if not table:
        raise ReferenceError(f"section {number} : tableau {what} introuvable")
    header, *rows = table
    if len(header) != 1 + len(SEVERITIES):
        raise ReferenceError(f"section {number} : l'en-tête du tableau {what} doit avoir 5 colonnes")
    levels = []
    for cell, expected in zip(header[1:], SEVERITIES, strict=True):
        match = _LEVEL_HEADER.match(plain_text(cell))
        if not match or match.group("id") != expected:
            raise ReferenceError(f"section {number} : colonne « {cell} », attendu « {expected} — libellé »")
        levels.append({"id": expected, "label": match.group("label").strip()})
    if not rows:
        raise ReferenceError(f"section {number} : le tableau {what} est vide")
    entries = []
    for row in rows:
        if len(row) != 1 + len(SEVERITIES):
            raise ReferenceError(f"section {number} : la ligne « {plain_text(row[0])} » doit avoir 5 colonnes")
        entries.append({"cell": row[0], "levels": dict(zip(SEVERITIES, map(plain_text, row[1:]), strict=True))})
    return levels, entries


def severity_reference(body: str) -> dict:
    """Grille de gravité (section 2) et délais internes (section 3) de D01."""
    levels, criteria = _level_table(body, 2, "des critères de gravité")
    timeline_levels, timelines = _level_table(body, 3, "des délais de traitement")
    if timeline_levels != levels:
        raise ReferenceError("section 3 : les libellés des niveaux diffèrent de ceux de la section 2")
    return {
        "levels": levels,
        "criteria": [{"name": bold_name(e["cell"]), "levels": e["levels"]} for e in criteria],
        "timelines": [
            {"name": bold_name(e["cell"]), "description": plain_text(e["cell"]), "levels": e["levels"]}
            for e in timelines
        ],
    }


# ─────────────────────────────────────────────────────────────
# 3. D04 — obligations légales et délais
# ─────────────────────────────────────────────────────────────


def obligations_reference(body: str) -> list[dict]:
    """Tableau « Obligation | Qui | Délai | Destinataire » de la section 1 de D04."""
    table = first_table(split_sections(body).get(1, ""))
    if not table:
        raise ReferenceError("section 1 : tableau des obligations introuvable")
    header, *rows = table
    if len(header) != 4:
        raise ReferenceError("section 1 : le tableau des obligations doit avoir 4 colonnes")
    obligations = []
    for row in rows:
        if len(row) != 4:
            raise ReferenceError(f"section 1 : la ligne « {plain_text(row[0])} » doit avoir 4 colonnes")
        hours = _HOURS.match(row[2])
        obligations.append(
            {
                "name": plain_text(row[0]),
                "who": plain_text(row[1]),
                "deadline": plain_text(row[2]),
                "recipient": plain_text(row[3]),
                # Compte à rebours possible seulement pour un délai en heures depuis la prise de connaissance
                "hours": int(hours.group("hours")) if hours else None,
            }
        )
    if not any(o["hours"] for o in obligations):
        raise ReferenceError(
            "section 1 : aucun délai en heures (attendu par ex. « **72 heures** » en début de cellule)"
        )
    return obligations


# ─────────────────────────────────────────────────────────────
# 4. Playbooks — paragraphe « Quand l'utiliser »
# ─────────────────────────────────────────────────────────────


def when_to_use(body: str, lang: str) -> str | None:
    """Texte du paragraphe « Quand l'utiliser : … » (il peut tenir sur plusieurs lignes)."""
    marker = WHEN_MARKERS[lang]
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(marker):
            paragraph = [line[len(marker) :]]
            for following in lines[index + 1 :]:
                if not following.strip():  # un paragraphe s'arrête à la première ligne vide
                    break
                paragraph.append(following)
            return plain_text(" ".join(part.strip() for part in paragraph))
    return None


# ─────────────────────────────────────────────────────────────
# 5. Contrôles pour playbook-check
# ─────────────────────────────────────────────────────────────

# Document de référence → fonction d'extraction
PARSERS: dict[str, Callable[[str], Any]] = {"D01": severity_reference, "D04": obligations_reference}


def _shape(doc_id: str, data: Any) -> object:
    """Ce qui doit être identique entre le français et l'anglais (le texte, lui, est traduit)."""
    if doc_id == "D01":
        return (len(data["criteria"]), len(data["timelines"]))
    return [o["hours"] for o in data]  # D04 : mêmes délais chiffrés, dans le même ordre


def check_reference(documents: Iterable[Document]) -> list[Problem]:
    """Tableaux de D01 et D04 bien formés et identiques en FR/EN ; « Quand l'utiliser » dans chaque playbook."""
    problems: list[Problem] = []
    extracted: dict[tuple[str, str], tuple[Document, Any]] = {}
    for doc in documents:
        if doc.kind == "playbook":
            if when_to_use(body_of(doc.path), doc.lang) is None:
                marker = WHEN_MARKERS[doc.lang]
                problems.append(Problem(doc.path, f"paragraphe « {marker} » introuvable (aide au choix du playbook)"))
        elif doc.kind == "doc" and doc.doc_id in PARSERS:
            try:
                extracted[(doc.doc_id, doc.lang)] = (doc, PARSERS[doc.doc_id](body_of(doc.path)))
            except ReferenceError as exc:
                problems.append(Problem(doc.path, str(exc)))
    for doc_id in PARSERS:
        if (doc_id, "fr") in extracted and (doc_id, "en") in extracted:
            (_fr_doc, fr_data), (en_doc, en_data) = extracted[(doc_id, "fr")], extracted[(doc_id, "en")]
            if _shape(doc_id, fr_data) != _shape(doc_id, en_data):
                problems.append(
                    Problem(
                        en_doc.path,
                        f"tableaux de référence différents de la version « fr » ({_shape(doc_id, en_data)})",
                    )
                )
    return problems
