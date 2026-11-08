/**
 * Échéances légales à partir de l'heure de prise de connaissance de l'incident (D04).
 *
 * Seules les obligations dont le délai est chiffré en heures ont un compte à rebours
 * (CNIL 72 h, NIS 2 24 h et 72 h, plainte 72 h). Les autres restent affichées en texte.
 * Toutes les heures sont calculées en millisecondes depuis l'époque Unix : pas de fuseau,
 * pas de changement d'heure qui fausserait le décompte.
 */

import type { Obligation } from "./data.ts";

const HOUR = 3_600_000;
const MINUTE = 60_000;
/** Moins de 6 heures restantes : l'échéance passe en alerte. */
export const SOON_MS = 6 * HOUR;

export type DueStatus = "pending" | "soon" | "overdue" | "untimed";

export interface Due {
  readonly obligation: Obligation;
  readonly due: Date | null;
  /** Millisecondes restantes (négatif si dépassé), null sans délai chiffré. */
  readonly remaining: number | null;
  readonly status: DueStatus;
}

// ─────────────────────────────────────────────────────────────
// 1. Calcul des échéances
// ─────────────────────────────────────────────────────────────
export function computeDeadlines(items: readonly Obligation[], awareness: Date, now: Date): Due[] {
  return items.map((obligation) => {
    if (obligation.hours === null) return { obligation, due: null, remaining: null, status: "untimed" };
    const due = new Date(awareness.getTime() + obligation.hours * HOUR);
    const remaining = due.getTime() - now.getTime();
    const status: DueStatus = remaining < 0 ? "overdue" : remaining <= SOON_MS ? "soon" : "pending";
    return { obligation, due, remaining, status };
  });
}

/** Échéances chiffrées d'abord, de la plus proche à la plus lointaine ; l'ordre de D04 sinon. */
export function sortByUrgency(list: readonly Due[]): Due[] {
  return [...list].sort((a, b) => {
    if (a.due && b.due) return a.due.getTime() - b.due.getTime();
    return a.due ? -1 : b.due ? 1 : 0;
  });
}

// ─────────────────────────────────────────────────────────────
// 2. Mise en forme
// ─────────────────────────────────────────────────────────────
/** Durée lisible : « 2 j 04 h 12 min » (fr) ou « 2 d 04 h 12 min » (en), à la minute près. */
export function formatDuration(ms: number, lang: "fr" | "en"): string {
  const total = Math.floor(Math.abs(ms) / MINUTE);
  const days = Math.floor(total / (24 * 60));
  const hours = Math.floor((total % (24 * 60)) / 60);
  const minutes = total % 60;
  const pad = (n: number): string => String(n).padStart(2, "0");
  const dayUnit = lang === "fr" ? "j" : "d";
  return days > 0 ? `${days} ${dayUnit} ${pad(hours)} h ${pad(minutes)} min` : `${hours} h ${pad(minutes)} min`;
}

/** Horodatage UTC sans ambiguïté, pour le rapport : « 2026-11-08 14:32 UTC ». */
export function utcStamp(date: Date): string {
  return `${date.toISOString().slice(0, 16).replace("T", " ")} UTC`;
}

/**
 * Lit la valeur d'un champ <input type="datetime-local"> (« 2026-11-08T14:32 », heure LOCALE).
 * Renvoie null si la valeur est absente ou incohérente (31 février…).
 */
export function parseLocalDateTime(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})$/.exec(value);
  if (!match) return null;
  const [year, month, day, hour, minute] = match.slice(1).map(Number) as [number, number, number, number, number];
  const date = new Date(year, month - 1, day, hour, minute);
  const coherent = date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day
    && date.getHours() === hour && date.getMinutes() === minute;
  return coherent ? date : null;
}

/** Valeur pour un champ datetime-local, en heure locale : l'inverse de parseLocalDateTime. */
export function toLocalInput(date: Date): string {
  const pad = (n: number): string => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
