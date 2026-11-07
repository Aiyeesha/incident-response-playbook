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
from playbook_tools.check import (
    FrontMatterError,
    attack_data,
    check_technique,
    main,
    parse_front_matter,
    run_checks,
)

TODAY = date(2026, 11, 7)  # date fixe : les tests ne dépendent pas du jour d'exécution


WHEN = {"fr": "**Quand l'utiliser :** des fichiers sont chiffrés.", "en": "**When to use it:** files are encrypted."}


def playbook(lang: str, title: str, owner: str, action: str, mitre: str = "T1486, T1490") -> str:
    """Construit un playbook minimal valide : fiche, « Quand l'utiliser », 8 sections, techniques citées."""
    sections = "\n".join(f"## {n}. Section {n}\n\n- [ ] {action} {n}\n" for n in range(1, 9))
    techniques = " ".join(t.strip() for t in mitre.split(","))
    return f"""---
id: P02
lang: {lang}
title: {title}
severity: [S1]
mitre: [{mitre}]
owner: {owner}
review: 2026-11-07
---

# P02 — {title}

{WHEN[lang]}

{sections}
## MITRE ATT&CK

{techniques}
"""


PLAYBOOK_FR = playbook("fr", "Attaque par rançongiciel", "Responsable SOC", "Isoler les postes touchés")
PLAYBOOK_EN = playbook("en", "Ransomware attack", "SOC lead", "Isolate the affected hosts")

DOC = """---
id: D01
lang: {lang}
title: {title}
review: 2026-11-07
---

# {title}

## 2. Niveaux

| Critère | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Étendue** | Plusieurs sites | Un serveur | Un poste | Aucun |

## 3. Délais

| Délai | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Prise en charge** (un analyste commence) | 15 minutes | 1 heure | 4 heures | 1 jour ouvré |
"""

# D04 : tableau des obligations, avec un délai en heures en français comme en anglais
D04 = """---
id: D04
lang: {lang}
title: {title}
review: 2026-11-07
---

# {title}

## 1. Délais

| Obligation | Qui | Délai | Destinataire |
|---|---|---|---|
| Notification CNIL | Responsable de traitement | **72 {unit}** après la prise de connaissance | CNIL |
| Registre | Responsable de traitement | **Toujours** | Interne |
"""


def write(root: Path, relative: str, content: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Dépôt fictif valide : un playbook et les documents de référence D01 et D04, dans les deux langues."""
    write(tmp_path, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR)
    write(tmp_path, "en/playbooks/P02-ransomware.md", PLAYBOOK_EN)
    write(tmp_path, "fr/docs/D01-gravite.md", DOC.format(lang="fr", title="Gravité"))
    write(tmp_path, "en/docs/D01-severity.md", DOC.format(lang="en", title="Severity"))
    write(tmp_path, "fr/docs/D04-cadre.md", D04.format(lang="fr", title="Cadre", unit="heures"))
    write(tmp_path, "en/docs/D04-context.md", D04.format(lang="en", title="Context", unit="hours"))
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
    assert len(documents) == 6


def test_ligne_de_commande(repo, capsys):
    assert main([str(repo)]) == 0
    assert "6 document(s) vérifié(s) — OK" in capsys.readouterr().out


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
        ("mitre: [T1486, T1490]", "mitre: [T1486, T1490, T1489]", "T1489 déclarée dans la fiche mais absente"),
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
    mitre = "T1486, T1490, T1110.003"
    write(repo, "fr/playbooks/P02-rancongiciel.md", playbook("fr", "Rançongiciel", "Responsable SOC", "Agir", mitre))
    write(repo, "en/playbooks/P02-ransomware.md", playbook("en", "Ransomware", "SOC lead", "Act", mitre))
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
    write(
        repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace("- [ ] Isoler les postes touchés 5", "- Isoler")
    )
    assert "section 5 sans action à cocher « - [ ] »" in messages(repo)


def test_section_1_peut_ne_pas_avoir_d_action(repo):
    # Dans les deux langues, pour respecter la parité du nombre d'actions par section
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace("- [ ] Isoler les postes touchés 1", "Signaux"))
    write(repo, "en/playbooks/P02-ransomware.md", PLAYBOOK_EN.replace("- [ ] Isolate the affected hosts 1", "Signals"))
    assert messages(repo) == []


@pytest.mark.parametrize(
    ("avant", "apres"),
    [
        ("## 4. Section 4", "## 4bis Section 4"),  # section manquante
        ("## 3. Section 3", "## 9. Section 3"),  # numéro inattendu
        ("## 7. Section 7", "## 7.Section 7"),  # titre mal formé
    ],
)
def test_structure_en_huit_sections(repo, avant, apres):
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace(avant, apres))
    assert any("sections numérotées attendues" in m for m in messages(repo))


def test_sections_dans_le_desordre(repo):
    texte = PLAYBOOK_FR.replace("## 2. Section 2", "## X").replace("## 3. Section 3", "## 2. Section 2")
    write(repo, "fr/playbooks/P02-rancongiciel.md", texte.replace("## X", "## 3. Section 3"))
    assert any("sections numérotées attendues" in m for m in messages(repo))


def test_une_section_s_arrete_au_titre_suivant_non_numerote(repo):
    # L'action placée sous « ## MITRE ATT&CK » ne doit pas compter pour la section 8
    texte = PLAYBOOK_FR.replace("- [ ] Isoler les postes touchés 8", "Rien")
    write(repo, "fr/playbooks/P02-rancongiciel.md", texte + "\n- [ ] action hors section\n")
    assert "section 8 sans action à cocher « - [ ] »" in messages(repo)


def test_technique_declaree_absente_du_texte(repo):
    write(repo, "fr/playbooks/P02-rancongiciel.md", PLAYBOOK_FR.replace("T1486 T1490", "T1486"))
    assert "technique T1490 déclarée dans la fiche mais absente du texte" in messages(repo)


@pytest.mark.parametrize(
    ("technique", "attendu"),
    [
        ("T1562.001", "révoquée dans ATT&CK 20.1, remplacée par T1685"),
        ("T9999", "inconnue dans MITRE ATT&CK 20.1"),
        ("T1486.999", "inconnue dans MITRE ATT&CK 20.1"),
    ],
)
def test_techniques_verifiees_dans_la_base_officielle(technique, attendu):
    assert attendu in check_technique(technique)


def test_technique_active_acceptee():
    assert check_technique("T1685") is None
    assert check_technique("T1486") is None


def test_technique_revoquee_signalee_dans_le_depot(repo):
    mitre = "T1486, T1490, T1562.001"
    write(repo, "fr/playbooks/P02-rancongiciel.md", playbook("fr", "Rançongiciel", "Responsable SOC", "Agir", mitre))
    write(repo, "en/playbooks/P02-ransomware.md", playbook("en", "Ransomware", "SOC lead", "Act", mitre))
    assert any("remplacée par T1685" in m for m in messages(repo))


def test_donnees_attack_embarquees():
    data = attack_data()
    assert data["attack_version"] == "20.1"
    assert data["techniques"]["T1486"] == {"name": "Data Encrypted for Impact", "status": "active"}


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
    write(repo, "en/playbooks/P02-ransomware.md", playbook("en", "Ransomware", "SOC lead", "Act", "T1486, T1489"))
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
    contenu = DOC.format(lang="fr", title="Gravité") + "\n[P09](../playbooks/P09.md)\n"
    write(repo, "fr/docs/D01-gravite.md", contenu)
    ligne = contenu.splitlines().index("[P09](../playbooks/P09.md)") + 1  # numéro de ligne attendu
    probs = run_checks(repo, TODAY)[1]
    assert [(p.message, p.line) for p in probs] == [("lien cassé : ../playbooks/P09.md", ligne)]


def test_lien_hors_depot(repo):
    write(repo, "README.md", "[sortie](../../etc/passwd)\n")
    assert any("hors du dépôt" in m for m in messages(repo))


def test_liens_dans_un_bloc_de_code_ignores(repo):
    write(repo, "README.md", "```\n[exemple](absent.md)\n```\n")
    assert messages(repo) == []
