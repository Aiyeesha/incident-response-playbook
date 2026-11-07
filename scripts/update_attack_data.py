"""
Met à jour la liste officielle des techniques MITRE ATT&CK (domaine Enterprise).

Usage :   python scripts/update_attack_data.py
Résultat : src/playbook_tools/data/attack-enterprise.json

Pourquoi un fichier extrait plutôt que la base complète ?
  - la base STIX officielle pèse plus de 50 Mo : trop lourde pour le dépôt et pour la CI ;
  - playbook-check n'a besoin que de l'identifiant, du nom et du statut de chaque technique.

Le script n'est PAS lancé en CI : on le relance à la main à chaque nouvelle version
d'ATT&CK, puis on vérifie que les playbooks passent toujours (techniques révoquées…).
Bibliothèque standard uniquement.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

# Source officielle : dépôt « attack-stix-data » publié par MITRE sur GitHub
SOURCE = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
)
TARGET = Path(__file__).resolve().parent.parent / "src" / "playbook_tools" / "data" / "attack-enterprise.json"


def mitre_id(obj: dict) -> str | None:
    """Identifiant ATT&CK (T1486…) d'un objet STIX, ou None."""
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id")
    return None


def main() -> None:
    # Téléchargement (HTTPS, adresse fixe : aucune donnée utilisateur dans l'URL)
    with urllib.request.urlopen(SOURCE, timeout=120) as response:  # noqa: S310 — URL https constante
        bundle = json.load(response)

    objects = bundle["objects"]
    collection = next((o for o in objects if o["type"] == "x-mitre-collection"), {})
    by_ref = {o["id"]: o for o in objects}

    # Techniques remplaçantes : relation « revoked-by » (ancienne → nouvelle)
    replaced_by = {}
    for rel in objects:
        if rel["type"] == "relationship" and rel.get("relationship_type") == "revoked-by":
            old, new = by_ref.get(rel["source_ref"]), by_ref.get(rel["target_ref"])
            if old and new:
                replaced_by[mitre_id(old)] = mitre_id(new)

    techniques = {}
    for obj in objects:
        tid = mitre_id(obj) if obj["type"] == "attack-pattern" else None
        if not tid:
            continue
        status = "revoked" if obj.get("revoked") else "deprecated" if obj.get("x_mitre_deprecated") else "active"
        entry = {"name": obj["name"], "status": status}
        if tid in replaced_by:
            entry["replaced_by"] = replaced_by[tid]
        techniques[tid] = entry

    data = {
        "source": SOURCE,
        "attack_version": collection.get("x_mitre_version", "inconnue"),
        "techniques": dict(sorted(techniques.items())),
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    active = sum(1 for t in techniques.values() if t["status"] == "active")
    print(f"ATT&CK {data['attack_version']} : {len(techniques)} techniques ({active} actives) → {TARGET}")


if __name__ == "__main__":
    main()
