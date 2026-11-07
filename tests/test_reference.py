"""
Tests des données de référence (grille de gravité D01, obligations D04, « Quand l'utiliser »).

Les fonctions d'extraction sont testées sur de petits extraits Markdown, puis les contrôles de
playbook-check sur le dépôt fictif valide des tests du validateur (fixture `repo`).
"""

import pytest
from test_check import DOC, TODAY, repo, write  # noqa: F401  (repo est une fixture pytest)

from playbook_tools.check import run_checks
from playbook_tools.reference import (
    ReferenceError,
    first_table,
    obligations_reference,
    severity_reference,
    when_to_use,
)

# ── Extraits Markdown réutilisés ────────────────────────────
GRILLE = """## 2. Niveaux

| Critère | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Étendue** | Plusieurs sites | Un serveur | Un poste | Aucun |
| **Données** | Exfiltrées | Exposées | Peu sensibles | Aucune |

### Exemples

| Situation | Gravité |
|---|---|
| Ignoré : seul le premier tableau compte | S1 |
"""

DELAIS = """## 3. Délais

| Délai | S1 — Critique | S2 — Élevée | S3 — Moyenne | S4 — Faible |
|---|---|---|---|---|
| **Confinement** (la menace ne progresse plus) | 4 heures | 24 heures | 72 heures | 5 jours ouvrés |
"""

OBLIGATIONS = """## 1. Délais

| Obligation | Qui | Délai | Destinataire |
|---|---|---|---|
| Violation (RGPD, [art. 33](https://eur-lex.europa.eu)) | Responsable | **72 heures** après connaissance | CNIL |
| Rapport final NIS 2 | Entités | **1 mois** après la notification | CSIRT |
| Registre | Responsable | **Toujours** | Interne |
"""


# ── Tableaux Markdown ───────────────────────────────────────
def test_premier_tableau_sans_la_ligne_de_separation():
    assert first_table("Texte\n\n| a | b |\n|---|:---:|\n| 1 | 2 |\n\nSuite\n| x |\n") == [["a", "b"], ["1", "2"]]


def test_pas_de_tableau():
    assert first_table("Aucun tableau ici.\n") == []


# ── D01 : grille de gravité et délais ───────────────────────
def test_grille_de_gravite():
    data = severity_reference(GRILLE + DELAIS)
    assert data["levels"] == [
        {"id": "S1", "label": "Critique"},
        {"id": "S2", "label": "Élevée"},
        {"id": "S3", "label": "Moyenne"},
        {"id": "S4", "label": "Faible"},
    ]
    assert [c["name"] for c in data["criteria"]] == ["Étendue", "Données"]
    assert data["criteria"][1]["levels"]["S2"] == "Exposées"
    (delai,) = data["timelines"]
    assert delai["name"] == "Confinement"
    assert delai["description"] == "Confinement (la menace ne progresse plus)"
    assert delai["levels"] == {"S1": "4 heures", "S2": "24 heures", "S3": "72 heures", "S4": "5 jours ouvrés"}


def test_grille_absente():
    with pytest.raises(ReferenceError, match="section 2 : tableau des critères de gravité introuvable"):
        severity_reference(DELAIS)


def test_niveaux_dans_le_mauvais_ordre():
    inverse = GRILLE.replace("S1 — Critique | S2 — Élevée", "S2 — Élevée | S1 — Critique")
    with pytest.raises(ReferenceError, match="attendu « S1 — libellé »"):
        severity_reference(inverse + DELAIS)


def test_ligne_incomplete():
    incomplete = GRILLE.replace("| Exfiltrées | Exposées |", "| Exfiltrées |")
    with pytest.raises(ReferenceError, match="la ligne « Données » doit avoir 5 colonnes"):
        severity_reference(incomplete + DELAIS)


def test_libelles_differents_entre_sections():
    autre = DELAIS.replace("S4 — Faible", "S4 — Basse")
    with pytest.raises(ReferenceError, match="libellés des niveaux diffèrent"):
        severity_reference(GRILLE + autre)


# ── D04 : obligations ───────────────────────────────────────
def test_obligations_et_delais_en_heures():
    items = obligations_reference(OBLIGATIONS)
    assert [o["hours"] for o in items] == [72, None, None]  # « 1 mois » et « Toujours » : pas de compte à rebours
    assert items[0] == {
        "name": "Violation (RGPD, art. 33)",
        "who": "Responsable",
        "deadline": "72 heures après connaissance",
        "recipient": "CNIL",
        "hours": 72,
    }


def test_obligations_en_anglais():
    anglais = OBLIGATIONS.replace("**72 heures**", "**72 hours**")
    assert obligations_reference(anglais)[0]["hours"] == 72


def test_aucun_delai_en_heures():
    sans = OBLIGATIONS.replace("**72 heures**", "Sans délai")
    with pytest.raises(ReferenceError, match="aucun délai en heures"):
        obligations_reference(sans)


def test_tableau_des_obligations_a_quatre_colonnes():
    with pytest.raises(ReferenceError, match="4 colonnes"):
        obligations_reference("## 1. Délais\n\n| a | b | c |\n|---|---|---|\n| 1 | 2 | 3 |\n")


# ── Playbooks : « Quand l'utiliser » ────────────────────────
def test_quand_l_utiliser_sur_plusieurs_lignes():
    corps = "# P02\n\n**Quand l'utiliser :** des fichiers sont **chiffrés**,\nune note apparaît.\n\n| Élément |\n"
    assert when_to_use(corps, "fr") == "des fichiers sont chiffrés, une note apparaît."


def test_quand_l_utiliser_suivi_d_une_liste():
    corps = (
        "**When to use it:** a campaign; its consequences have their own playbooks:\n\n"
        "- an attachment was run → [P01 — Malware](P01-malware.md);\n"
        "- credentials were used → [P07](P07.md).\n\n| Item |\n"
    )
    attendu = "a campaign; its consequences have their own playbooks: an attachment was run → P01 — Malware;"
    assert when_to_use(corps, "en") == attendu + " credentials were used → P07."


def test_idem_reprend_la_ligne_precedente():
    tableau = OBLIGATIONS + "| Notification NIS 2 | Idem | **72 heures** | Idem |\n"
    derniere = obligations_reference(tableau)[-1]
    assert (derniere["who"], derniere["recipient"]) == ("Responsable", "Interne")


def test_idem_sur_la_premiere_ligne():
    tableau = OBLIGATIONS.replace(
        "| Violation (RGPD, [art. 33](https://eur-lex.europa.eu)) | Responsable |", "| Violation | Same |"
    )
    with pytest.raises(ReferenceError, match="« Same » sur la première ligne"):
        obligations_reference(tableau)


def test_quand_l_utiliser_absent():
    assert when_to_use("# P02\n\nTexte.\n", "en") is None


# ── Contrôles de playbook-check ─────────────────────────────
def messages(root):
    return [p.message for p in run_checks(root, TODAY)[1]]


def test_depot_de_reference_valide(repo):  # noqa: F811
    assert messages(repo) == []


def test_playbook_sans_quand_l_utiliser(repo):  # noqa: F811
    chemin = repo / "en/playbooks/P02-ransomware.md"
    chemin.write_text(chemin.read_text(encoding="utf-8").replace("**When to use it:**", "When:"), encoding="utf-8")
    assert messages(repo) == ["paragraphe « **When to use it:** » introuvable (aide au choix du playbook)"]


def test_grille_mal_formee_signalee(repo):  # noqa: F811
    write(repo, "fr/docs/D01-gravite.md", DOC.format(lang="fr", title="Gravité").replace("S3 — Moyenne", "S3"))
    assert messages(repo) == ["section 2 : colonne « S3 », attendu « S3 — libellé »"]


def test_parite_des_delais_chiffres(repo):  # noqa: F811
    chemin = repo / "en/docs/D04-context.md"
    chemin.write_text(chemin.read_text(encoding="utf-8").replace("**72 hours**", "**24 hours**"), encoding="utf-8")
    assert messages(repo) == ["tableaux de référence différents de la version « fr » ([24, None])"]


def test_parite_du_nombre_d_actions(repo):  # noqa: F811
    chemin = repo / "en/playbooks/P02-ransomware.md"
    ajout = "- [ ] Isolate the affected hosts 3\n- [ ] Extra action\n"
    texte = chemin.read_text(encoding="utf-8").replace("- [ ] Isolate the affected hosts 3\n", ajout)
    chemin.write_text(texte, encoding="utf-8")
    assert messages(repo) == ["nombre d'actions par section différent de la version « fr » ([1, 1, 2, 1, 1, 1, 1, 1])"]
