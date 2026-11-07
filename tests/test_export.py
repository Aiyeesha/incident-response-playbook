"""
Tests de l'export JSON (commande « playbook-export »).

On réutilise le dépôt fictif valide des tests du validateur (fixture `repo`) :
l'export doit en extraire la bonne structure, et le REFUSER dès qu'il y a un problème.
"""

import json

import pytest
from test_check import repo, write  # noqa: F401  (repo est une fixture pytest)

from playbook_tools import __version__
from playbook_tools.export import SCHEMA_VERSION, actions, build_export, main, plain_text, section_titles


# ── Nettoyage du Markdown ───────────────────────────────────
@pytest.mark.parametrize(
    ("markdown", "attendu"),
    [
        ("Prévenir le **DPO** ([D03](../docs/D03-matrice-raci.md))", "Prévenir le DPO (D03)"),
        ("Lancer `vssadmin list shadows`", "Lancer vssadmin list shadows"),
        ("  Texte simple  ", "Texte simple"),
    ],
)
def test_texte_simple(markdown, attendu):
    assert plain_text(markdown) == attendu


def test_titres_de_section():
    corps = "## 1. Détection\n\ntexte\n\n## 3. **Confinement**\n\n## Annexe\n"
    assert section_titles(corps) == {1: "Détection", 3: "Confinement"}


def test_actions_dans_l_ordre_et_sans_les_cases_cochees():
    section = "- [ ] Première\n  * [ ] Deuxième, **importante**\n- [x] Déjà faite\n- Simple puce\n"
    assert actions(section) == ["Première", "Deuxième, importante"]


# ── Document complet ────────────────────────────────────────
def test_structure_de_l_export(repo):  # noqa: F811
    document = build_export(repo, "fr")
    assert document["schema_version"] == SCHEMA_VERSION
    assert document["tool_version"] == __version__
    assert document["attack_version"] == "20.1"
    assert document["lang"] == "fr"
    # Format 2 : grille de gravité (D01) et obligations légales (D04) lues dans la documentation
    assert [level["id"] for level in document["severity"]["levels"]] == ["S1", "S2", "S3", "S4"]
    assert document["severity"]["criteria"][0]["name"] == "Étendue"
    assert document["severity"]["timelines"][0]["levels"]["S1"] == "15 minutes"
    assert document["severity"]["source"] == "fr/docs/D01-gravite.md"
    assert [o["hours"] for o in document["obligations"]["items"]] == [72, None]
    assert document["obligations"]["source"] == "fr/docs/D04-cadre.md"

    (playbook,) = document["playbooks"]  # les documents D.. ne sont pas exportés
    assert playbook["id"] == "P02"
    assert playbook["title"] == "Attaque par rançongiciel"
    assert playbook["severity"] == ["S1"]
    assert playbook["owner"] == "Responsable SOC"
    assert playbook["when"] == "des fichiers sont chiffrés."
    assert playbook["source"] == "fr/playbooks/P02-rancongiciel.md"
    assert playbook["mitre"] == [
        {"id": "T1486", "name": "Data Encrypted for Impact"},
        {"id": "T1490", "name": "Inhibit System Recovery"},
    ]
    assert [s["number"] for s in playbook["sections"]] == list(range(1, 9))
    assert playbook["sections"][2] == {
        "number": 3,
        "title": "Section 3",
        "actions": ["Isoler les postes touchés 3"],
    }


def test_export_anglais(repo):  # noqa: F811
    (playbook,) = build_export(repo, "en")["playbooks"]
    assert playbook["source"] == "en/playbooks/P02-ransomware.md"
    assert playbook["sections"][0]["actions"] == ["Isolate the affected hosts 1"]


def test_export_refuse_sans_document_de_reference(repo):  # noqa: F811
    # D04 retiré dans les DEUX langues : la documentation reste cohérente, mais l'interface n'aurait
    # plus les délais légaux, donc l'export est refusé
    (repo / "fr/docs/D04-cadre.md").unlink()
    (repo / "en/docs/D04-context.md").unlink()
    with pytest.raises(ValueError, match="D04 absent en « fr »"):
        build_export(repo, "fr")


def test_export_refuse_si_la_documentation_est_invalide(repo):  # noqa: F811
    write(repo, "README.md", "[cassé](absent.md)\n")
    with pytest.raises(ValueError, match="export refusé"):
        build_export(repo, "fr")


# ── Ligne de commande ───────────────────────────────────────
def test_ligne_de_commande_vers_la_sortie_standard(repo, capsys):  # noqa: F811
    assert main([str(repo), "--lang", "en"]) == 0
    assert json.loads(capsys.readouterr().out)["lang"] == "en"


def test_ligne_de_commande_vers_un_fichier(repo, tmp_path, capsys):  # noqa: F811
    cible = tmp_path / "playbooks.fr.json"
    assert main([str(repo), "--lang", "fr", "-o", str(cible)]) == 0
    assert "1 playbook(s), 8 action(s)" in capsys.readouterr().out
    # UTF-8 sans échappement : les accents restent lisibles dans le fichier
    assert "rançongiciel" in cible.read_text(encoding="utf-8")


def test_ligne_de_commande_documentation_invalide(repo, capsys):  # noqa: F811
    write(repo, "README.md", "[cassé](absent.md)\n")
    assert main([str(repo), "--lang", "fr"]) == 1
    assert "playbook-check" in capsys.readouterr().err


def test_ligne_de_commande_mauvaise_racine(tmp_path, capsys):
    assert main([str(tmp_path), "--lang", "fr"]) == 2
    assert "fr/ et en/" in capsys.readouterr().err


def test_langue_obligatoire(repo):  # noqa: F811
    with pytest.raises(SystemExit) as erreur:
        main([str(repo)])
    assert erreur.value.code == 2
