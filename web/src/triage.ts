/**
 * Qualification de la gravité, selon la règle de D01 :
 *   « On évalue l'incident selon cinq critères. Le critère le plus grave l'emporte. »
 *
 * Ce module ne fait qu'appliquer la règle ; la décision finale reste à la personne qui
 * traite l'incident (l'interface le rappelle à côté du résultat).
 */

import { LEVEL_IDS, type LevelId, type LevelRow } from "./data.ts";

/** Réponse à un critère : un niveau, ou « je ne sais pas encore ». */
export type Answer = LevelId | "unknown";

export interface Assessment {
  /** Niveau retenu, ou null tant qu'aucun critère n'a de réponse. */
  readonly level: LevelId | null;
  /** Critères qui ont décidé du niveau (ceux qui sont au niveau retenu). */
  readonly decisive: readonly string[];
  /** Nombre de critères sans réponse ou « je ne sais pas » : à réévaluer au point suivant. */
  readonly open: number;
}

/** Rang d'un niveau : 0 pour S1 (le plus grave) … 3 pour S4. */
const rank = (level: LevelId): number => LEVEL_IDS.indexOf(level);

// ─────────────────────────────────────────────────────────────
// 1. Le critère le plus grave l'emporte
// ─────────────────────────────────────────────────────────────
export function assess(criteria: readonly LevelRow[], answers: readonly (Answer | undefined)[]): Assessment {
  let level: LevelId | null = null;
  let open = 0;
  criteria.forEach((_criterion, i) => {
    const answer = answers[i];
    if (answer === undefined || answer === "unknown") {
      open += 1;
      return;
    }
    if (level === null || rank(answer) < rank(level)) level = answer;
  });
  const retained = level as LevelId | null; // TypeScript ne suit pas l'affectation faite dans la boucle
  const decisive = retained === null ? [] : criteria.filter((_c, i) => answers[i] === retained).map((c) => c.name);
  return { level: retained, decisive, open };
}

// ─────────────────────────────────────────────────────────────
// 2. Cohérence avec le playbook choisi
// ─────────────────────────────────────────────────────────────
export interface Adjusted {
  readonly level: LevelId | null;
  /** true si le niveau a été RELEVÉ pour respecter les gravités prévues par le playbook. */
  readonly raised: boolean;
}

/**
 * Chaque playbook indique ses gravités possibles (un rançongiciel est « toujours S1 »).
 * Si l'évaluation donne un niveau moins grave que ce que prévoit le playbook, on le relève
 * au niveau prévu le plus proche. On ne l'abaisse JAMAIS : dans le doute, D01 impose le plus élevé.
 */
export function adjustForPlaybook(level: LevelId | null, allowed: readonly LevelId[]): Adjusted {
  if (level === null || allowed.length === 0 || allowed.includes(level)) return { level, raised: false };
  const moreSevere = allowed.filter((candidate) => rank(candidate) < rank(level));
  if (moreSevere.length === 0) return { level, raised: false }; // déjà plus grave que prévu : on garde
  const closest = moreSevere.reduce((a, b) => (rank(a) > rank(b) ? a : b));
  return { level: closest, raised: true };
}
