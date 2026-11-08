/**
 * Conservation FACULTATIVE de la progression dans le navigateur (localStorage).
 *
 * Désactivée par défaut : les détails d'un incident sont sensibles. Quand l'utilisateur
 * l'active, l'état est écrit sur cet appareil uniquement ; « Tout effacer » le supprime.
 * Chaque accès est protégé : un navigateur qui bloque le stockage (navigation privée,
 * politique d'entreprise) ne doit jamais casser la page.
 */

import { LEVEL_IDS, type Lang } from "./data.ts";
import type { Answer } from "./triage.ts";
import type { Checked } from "./checklist.ts";

const KEY = "incident-response-playbook:state";

export interface SavedState {
  readonly v: 1;
  readonly lang: Lang;
  readonly playbook: string | null;
  readonly answers: readonly (Answer | null)[];
  readonly awareness: string | null;
  readonly checked: Checked;
  readonly reference: string;
}

/** Lecture de l'objet de stockage : null s'il est inaccessible (bloqué ou absent). */
function store(): Storage | null {
  try {
    return globalThis.localStorage ?? null;
  } catch {
    return null;
  }
}

export function storageAvailable(): boolean {
  const s = store();
  if (!s) return false;
  try {
    s.setItem(`${KEY}:test`, "1");
    s.removeItem(`${KEY}:test`);
    return true;
  } catch {
    return false;
  }
}

/** Vérifie la forme d'un état relu : une donnée modifiée à la main est ignorée, pas exécutée. */
export function parseSaved(raw: string | null): SavedState | null {
  if (!raw) return null;
  try {
    const data = JSON.parse(raw) as Record<string, unknown>;
    const answers = data["answers"];
    const checked = data["checked"];
    const valid = data["v"] === 1
      && (data["lang"] === "fr" || data["lang"] === "en")
      && (data["playbook"] === null || (typeof data["playbook"] === "string" && /^P\d{2}$/.test(data["playbook"])))
      && Array.isArray(answers)
      && answers.every((a) => a === null || a === "unknown" || LEVEL_IDS.includes(a as never))
      && (data["awareness"] === null || (typeof data["awareness"] === "string" && !Number.isNaN(Date.parse(data["awareness"]))))
      && typeof checked === "object" && checked !== null && !Array.isArray(checked)
      && Object.entries(checked).every(([k, v]) => /^P\d{2}:\d+:\d+$/.test(k) && typeof v === "string" && !Number.isNaN(Date.parse(v)))
      && typeof data["reference"] === "string";
    return valid ? (data as unknown as SavedState) : null;
  } catch {
    return null;
  }
}

export function load(): SavedState | null {
  try {
    return parseSaved(store()?.getItem(KEY) ?? null);
  } catch {
    return null;
  }
}

export function save(state: SavedState): boolean {
  try {
    store()?.setItem(KEY, JSON.stringify(state));
    return true;
  } catch {
    return false;
  }
}

export function clear(): void {
  try {
    store()?.removeItem(KEY);
  } catch {
    // Rien à faire : si le stockage est bloqué, il n'y a rien à effacer
  }
}
