/**
 * Types et validation de l'export JSON (format 2) produit par « playbook-export ».
 *
 * Le fichier vient du même site, mais l'interface ne lui fait pas confiance aveuglément :
 * chaque champ est vérifié avant usage. Un fichier tronqué, d'un autre format ou modifié
 * provoque une erreur claire au lieu d'un affichage incohérent pendant un incident.
 */

// ─────────────────────────────────────────────────────────────
// 1. Types du format 2
// ─────────────────────────────────────────────────────────────
export type LevelId = "S1" | "S2" | "S3" | "S4";
/** Du plus grave au moins grave : l'indice sert à comparer deux niveaux. */
export const LEVEL_IDS: readonly LevelId[] = ["S1", "S2", "S3", "S4"];
export type Lang = "fr" | "en";

export interface Level { readonly id: LevelId; readonly label: string }
/** Une ligne de la grille de D01 : un critère (ou un délai) décrit pour chaque niveau. */
export interface LevelRow { readonly name: string; readonly levels: Readonly<Record<LevelId, string>> }
export interface Timeline extends LevelRow { readonly description: string }

export interface Obligation {
  readonly name: string;
  readonly who: string;
  readonly deadline: string;
  readonly recipient: string;
  /** Délai en heures depuis la prise de connaissance, ou null s'il n'est pas chiffré. */
  readonly hours: number | null;
}

export interface Section { readonly number: number; readonly title: string; readonly actions: readonly string[] }
export interface Technique { readonly id: string; readonly name: string }

export interface Playbook {
  readonly id: string;
  readonly title: string;
  readonly severity: readonly LevelId[];
  readonly owner: string;
  readonly review: string;
  readonly when: string;
  readonly mitre: readonly Technique[];
  readonly source: string;
  readonly sections: readonly Section[];
}

export interface ExportDoc {
  readonly schema_version: 2;
  readonly tool_version: string;
  readonly attack_version: string;
  readonly lang: Lang;
  readonly severity: {
    readonly levels: readonly Level[];
    readonly criteria: readonly LevelRow[];
    readonly timelines: readonly Timeline[];
    readonly source: string;
  };
  readonly obligations: { readonly items: readonly Obligation[]; readonly source: string };
  readonly playbooks: readonly Playbook[];
}

/** Erreur de format : le message indique le chemin du champ fautif (ex. « playbooks[2].when »). */
export class DataError extends Error {
  override name = "DataError";
}

// ─────────────────────────────────────────────────────────────
// 2. Petits vérificateurs : chacun renvoie la valeur typée ou lève DataError
// ─────────────────────────────────────────────────────────────
type Json = Record<string, unknown>;

function record(value: unknown, path: string): Json {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new DataError(`${path} : objet attendu`);
  }
  return value as Json;
}

function text(value: unknown, path: string): string {
  if (typeof value !== "string" || value.trim() === "") throw new DataError(`${path} : texte non vide attendu`);
  return value;
}

function list(value: unknown, path: string): readonly unknown[] {
  if (!Array.isArray(value)) throw new DataError(`${path} : liste attendue`);
  return value;
}

function levelId(value: unknown, path: string): LevelId {
  if (!LEVEL_IDS.includes(value as LevelId)) throw new DataError(`${path} : niveau S1 à S4 attendu`);
  return value as LevelId;
}

function levelTexts(value: unknown, path: string): Record<LevelId, string> {
  const obj = record(value, path);
  const out = {} as Record<LevelId, string>;
  for (const id of LEVEL_IDS) out[id] = text(obj[id], `${path}.${id}`);
  return out;
}

// ─────────────────────────────────────────────────────────────
// 3. Validation complète
// ─────────────────────────────────────────────────────────────
/** Vérifie un export JSON déjà décodé et le renvoie typé ; « lang » est la langue attendue. */
export function parseExport(raw: unknown, lang: Lang): ExportDoc {
  const doc = record(raw, "export");
  if (doc["schema_version"] !== 2) {
    throw new DataError(`export : format ${String(doc["schema_version"])} non pris en charge (attendu : 2)`);
  }
  if (doc["lang"] !== lang) throw new DataError(`export : langue « ${String(doc["lang"])} » au lieu de « ${lang} »`);

  // Grille de gravité : les 4 niveaux, dans l'ordre
  const severity = record(doc["severity"], "severity");
  const levels = list(severity["levels"], "severity.levels").map((item, i) => {
    const level = record(item, `severity.levels[${i}]`);
    return { id: levelId(level["id"], `severity.levels[${i}].id`), label: text(level["label"], `severity.levels[${i}].label`) };
  });
  if (levels.map((l) => l.id).join() !== LEVEL_IDS.join()) throw new DataError("severity.levels : S1, S2, S3, S4 attendus");

  const rows = (value: unknown, path: string): LevelRow[] =>
    list(value, path).map((item, i) => {
      const row = record(item, `${path}[${i}]`);
      return { name: text(row["name"], `${path}[${i}].name`), levels: levelTexts(row["levels"], `${path}[${i}].levels`) };
    });
  const criteria = rows(severity["criteria"], "severity.criteria");
  if (criteria.length === 0) throw new DataError("severity.criteria : au moins un critère attendu");
  const timelines = list(severity["timelines"], "severity.timelines").map((item, i) => {
    const row = record(item, `severity.timelines[${i}]`);
    return {
      name: text(row["name"], `severity.timelines[${i}].name`),
      description: text(row["description"], `severity.timelines[${i}].description`),
      levels: levelTexts(row["levels"], `severity.timelines[${i}].levels`),
    };
  });

  // Obligations : « hours » est un entier positif ou null
  const obligationsBlock = record(doc["obligations"], "obligations");
  const items = list(obligationsBlock["items"], "obligations.items").map((item, i) => {
    const o = record(item, `obligations.items[${i}]`);
    const hours = o["hours"];
    if (hours !== null && !(Number.isInteger(hours) && (hours as number) > 0)) {
      throw new DataError(`obligations.items[${i}].hours : entier positif ou null attendu`);
    }
    return {
      name: text(o["name"], `obligations.items[${i}].name`),
      who: text(o["who"], `obligations.items[${i}].who`),
      deadline: text(o["deadline"], `obligations.items[${i}].deadline`),
      recipient: text(o["recipient"], `obligations.items[${i}].recipient`),
      hours: hours as number | null,
    };
  });

  // Playbooks : identifiants uniques, sections numérotées, actions textuelles
  const seen = new Set<string>();
  const playbooks = list(doc["playbooks"], "playbooks").map((item, i): Playbook => {
    const p = record(item, `playbooks[${i}]`);
    const id = text(p["id"], `playbooks[${i}].id`);
    if (!/^P\d{2}$/.test(id) || seen.has(id)) throw new DataError(`playbooks[${i}].id : identifiant invalide ou en double`);
    seen.add(id);
    return {
      id,
      title: text(p["title"], `playbooks[${i}].title`),
      severity: list(p["severity"], `playbooks[${i}].severity`).map((s, j) => levelId(s, `playbooks[${i}].severity[${j}]`)),
      owner: text(p["owner"], `playbooks[${i}].owner`),
      review: text(p["review"], `playbooks[${i}].review`),
      when: text(p["when"], `playbooks[${i}].when`),
      mitre: list(p["mitre"], `playbooks[${i}].mitre`).map((t, j) => {
        const technique = record(t, `playbooks[${i}].mitre[${j}]`);
        return { id: text(technique["id"], `playbooks[${i}].mitre[${j}].id`), name: text(technique["name"], `playbooks[${i}].mitre[${j}].name`) };
      }),
      source: text(p["source"], `playbooks[${i}].source`),
      sections: list(p["sections"], `playbooks[${i}].sections`).map((s, j) => {
        const section = record(s, `playbooks[${i}].sections[${j}]`);
        const number = section["number"];
        if (!Number.isInteger(number)) throw new DataError(`playbooks[${i}].sections[${j}].number : entier attendu`);
        return {
          number: number as number,
          title: text(section["title"], `playbooks[${i}].sections[${j}].title`),
          actions: list(section["actions"], `playbooks[${i}].sections[${j}].actions`).map((a, k) =>
            text(a, `playbooks[${i}].sections[${j}].actions[${k}]`)),
        };
      }),
    };
  });
  if (playbooks.length === 0) throw new DataError("playbooks : au moins un playbook attendu");

  return {
    schema_version: 2,
    tool_version: text(doc["tool_version"], "tool_version"),
    attack_version: text(doc["attack_version"], "attack_version"),
    lang,
    severity: { levels, criteria, timelines, source: text(severity["source"], "severity.source") },
    obligations: { items, source: text(obligationsBlock["source"], "obligations.source") },
    playbooks,
  };
}
