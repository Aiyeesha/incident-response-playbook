"""
Tests du validateur de documentation.

Chaque test construit un petit dépôt fictif dans un dossier temporaire (tmp_path),
puis vérifie que playbook-check accepte ce qui est valide et refuse le reste.
"""

from datetime import date
from importlib.metadata import version
from pathlib import Path

import pytest

import playbook_tools
from playbook_tools.check import FrontMatterError, main, parse_front_matter, run_checks

TODAY = date(2026, 11, 7)  # date fixe : les tests ne dépendent pas du jour d'exécution

PLAYBOOK_FR = """---
id: P02
lang: fr
title: Attaque par rançongiciel
severity: [S1]
mitre: [T1486, T1490]
owner: Responsable SOC
review: 2026-11-07
---

# P02 — Attaque par rançongiciel

- [ ] Isoler les postes touchés
"""

PLAYBOOK_EN = """---
id: P02
lang: en
title: Ransomware attack
severity: [S1]
mitre: [T1486, T1490]
owner: SOC lead
review: 2026-11-07
---

# P02 — Ransomware attack

- [ ] Isolate the affected hosts
"""

DOC = """---
id: D01
lang: {lang}
title: {title}
review: 2026-11-07
---

# {title}
"""


def write(root: Path, relative: str, content: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Dépôt fictif valide : un playbook et un document, dans les deux langues."""
    write(tmp_path, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR)
    write(tmp_path, "en/playbooks/P02-ransomware.md", PLAYBOOK_EN)
    write(tmp_path, "fr/docs/D01-gravite.md", DOC.format(lang="fr", title="Gravité"))
    write(tmp_path, "en/docs/D01-severity.md", DOC.format(lang="en", title="Severity"))
    write(tmp_path, "README.md", "[Playbook](fr/playbooks/P02-rancongiciel.md)\n")
    return tmp_path


def messages(root: Path) -> list[str]:
    return [p.message for p in run_checks(root, TODAY)[1]]


# ── Paquet ──────────────────────────────────────────────────
def test_version_coherente():
    assert version("incident-response-playbook") == playbook_tools.__version__


# ── Cas valide ──────────────────────────────────────────────
def test_depot_valide(repo):
    documents, problems = run_checks(repo, TODAY)
    assert problems == []
    assert len(documents) == 4


def test_ligne_de_commande(repo, capsys):
    assert main([str(repo)]) == 0
    assert "4 document(s) vérifié(s) — OK" in capsys.readouterr().out


def test_ligne_de_commande_mauvaise_racine(tmp_path, capsys):
    assert main([str(tmp_path)]) == 2
    assert "fr/ et en/" in capsys.readouterr().err


def test_ligne_de_commande_problemes(repo, capsys):
    write(repo, "README.md", "[cassé](absent.md)\n")
    assert main([str(repo)]) == 1
    assert "README.md:1: lien cassé : absent.md" in capsys.readouterr().out


# ── Lecture de la fiche (sous-ensemble YAML) ────────────────
def test_lecture_fiche():
    meta, body_start = parse_front_matter(PLAYBOOK_FR)
    assert meta["severity"] == ["S1"] and meta["mitre"] == ["T1486", "T1490"]
    assert meta["title"] == "Attaque par rançongiciel"
    assert body_start == 10


def test_guillemets_et_commentaires():
    meta, _ = parse_front_matter('---\n# commentaire\ntitle: "Accès : non autorisé"\n\n---\n')
    assert meta == {"title": "Accès : non autorisé"}


@pytest.mark.parametrize(
    ("texte", "attendu"),
    [
        ("# Titre\n", "fiche absente"),
        ("---\nid: P01\n", "non terminée"),
        ("---\n  id: P01\n---\n", "indentation"),
        ("---\nid P01\n---\n", "ligne invalide"),
        ("---\nid:\n---\n", "ligne invalide"),
        ("---\nid: P01\nid: P02\n---\n", "répétée"),
        ("---\nmitre: [T1486\n---\n", "mal fermée"),
        ("---\nmitre: [T1486, ]\n---\n", "élément vide"),
        ('---\ntitle: "abc\n---\n', "guillemets"),
        ("---\ntitle: a: b\n---\n", "ambiguë"),
        ("---\ntitle: {a}\n---\n", "ambiguë"),
        ("---\ntitle: texte # commentaire\n---\n", "ambiguë"),
        ("---\nTitle: X\n---\n", "ligne invalide"),
    ],
)
def test_fiches_mal_formees(texte, attendu):
    with pytest.raises(FrontMatterError, match=attendu):
        parse_front_matter(texte)


# ── Contenu de la fiche ─────────────────────────────────────
@pytest.mark.parametrize(
    ("avant", "apres", "attendu"),
    [
        ("owner: Responsable SOC\n", "", "champ obligatoire manquant : « owner »"),
        ("owner: Responsable SOC\n", "owner: Responsable SOC\nauteur: X\n", "champ inconnu : « auteur »"),
        ("severity: [S1]", "severity: [S5]", "gravité inconnue « S5 »"),
        ("severity: [S1]", "severity: [S1, S1]", "doublon"),
        ("severity: [S1]", "severity: S1", "doit être une liste"),
        ("severity: [S1]", "severity: []", "« severity » est vide"),
        ("mitre: [T1486, T1490]", "mitre: [T148]", "technique MITRE ATT&CK invalide"),
        ("mitre: [T1486, T1490]", "mitre: [T1486.1]", "technique MITRE ATT&CK invalide"),
        ("owner: Responsable SOC", "owner: [A, B]", "valeur simple"),
        ("review: 2026-11-07", "review: 07/11/2026", "AAAA-MM-JJ"),
        ("review: 2026-11-07", "review: 2026-02-30", "AAAA-MM-JJ"),
        ("review: 2026-11-07", "review: 20261107", "AAAA-MM-JJ"),
        ("review: 2026-11-07", "review: 2027-01-01", "dans le futur"),
        ("lang: fr", "lang: en", "ne correspond pas au dossier"),
        ("id: P02", "id: P03", "différent du préfixe du fichier"),
    ],
)
def test_fiches_invalides(repo, avant, apres, attendu):
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace(avant, apres, 1))
    assert any(attendu in m for m in messages(repo)), messages(repo)


def test_sous_technique_mitre_acceptee(repo):
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace("T1490]", "T1490, T1110.003]"))
    write(repo, "en/playbooks/P02-ransomware.md", PLAYBOOK_EN.replace("T1490]", "T1490, T1110.003]"))
    assert messages(repo) == []


@pytest.mark.parametrize("nom", ["P2-rancongiciel.md", "P02_rancongiciel.md", "P02-Rancongiciel.md", "P02.md"])
def test_nom_de_fichier_invalide(repo, nom):
    (repo / "fr/playbooks/P02-rancongiciel.md").rename(repo / "fr/playbooks" / nom)
    write(repo, "README.md", "")
    assert any("nom de fichier invalide" in m for m in messages(repo))


def test_prefixe_incoherent_avec_le_dossier(repo):
    write(repo, "fr/docs/P09-intrus.md", PLAYBOOK_FR.replace("id: P02", "id: P09"))
    assert any("identifiant en D" in m for m in messages(repo))


def test_playbook_sans_action_a_cocher(repo):
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace("- [ ] Isoler", "- Isoler"))
    assert any("action à cocher" in m for m in messages(repo))


def test_fichier_non_markdown_refuse(repo):
    write(repo, "fr/templates/notes.txt", "x")
    assert any("fichier inattendu" in m for m in messages(repo))


def test_readme_d_index_sans_fiche_accepte(repo):
    write(repo, "fr/playbooks/README.md", "# Index\n")
    write(repo, "en/playbooks/README.md", "# Index\n")
    assert messages(repo) == []


# ── Parité FR / EN ──────────────────────────────────────────
def test_version_anglaise_manquante(repo):
    (repo / "en/playbooks/P02-ransomware.md").unlink()
    assert any("version « en » manquante pour P02" in m for m in messages(repo))


def test_version_francaise_manquante(repo):
    (repo / "fr/docs/D01-gravite.md").unlink()
    assert any("version « fr » manquante pour D01" in m for m in messages(repo))


def test_metadonnees_partagees_differentes(repo):
    write(repo, "en/playbooks/P02-ransomware.md", PLAYBOOK_EN.replace("T1490]", "T1489]"))
    assert any("« mitre » diffère" in m for m in messages(repo))


def test_identifiant_en_double(repo):
    write(repo, "fr/playbooks/P02-autre.md", PLAYBOOK_FR)
    assert any("déjà utilisé" in m for m in messages(repo))


# ── Liens ───────────────────────────────────────────────────
@pytest.mark.parametrize(
    "lien",
    [
        "[ok](fr/playbooks/P02-rancongiciel.md)",
        "[ancre](fr/docs/D01-gravite.md#niveaux)",
        "[dossier](fr/playbooks)",
        "[externe](https://csrc.nist.gov/pubs/sp/800/61/r3/final)",
        "[mail](mailto:soc@example.org)",
        "[ancre locale](#section)",
        "![image absente](img/absente.png)",  # les images ne sont pas contrôlées
    ],
)
def test_liens_acceptes(repo, lien):
    write(repo, "README.md", lien + "\n")
    assert messages(repo) == []


def test_lien_casse(repo):
    write(repo, "fr/docs/D01-gravite.md", DOC.format(lang="fr", title="Gravité") + "\n[P09](../playbooks/P09.md)\n")
    probs = run_checks(repo, TODAY)[1]
    assert [(p.message, p.line) for p in probs] == [("lien cassé : ../playbooks/P09.md", 10)]


def test_lien_hors_depot(repo):
    write(repo, "README.md", "[sortie](../../etc/passwd)\n")
    assert any("hors du dépôt" in m for m in messages(repo))


def test_liens_dans_un_bloc_de_code_ignores(repo):
    write(repo, "README.md", "```\n[exemple](absent.md)\n```\n")
    assert messages(repo) == []
