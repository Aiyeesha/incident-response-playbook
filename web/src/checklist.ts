/**
 * État des actions à cocher : quelles actions sont faites, et à quelle heure.
 *
 * L'état est un simple objet « clé → horodatage ISO », jamais modifié en place (chaque
 * changement crée un nouvel objet) : facile à tester, à enregistrer et à exporter.
 */

import type { Playbook } from "./data.ts";

/** Clé d'une action → date et heure à laquelle elle a été cochée (ISO 8601, UTC). */
export type Checked = Readonly<Record<string, string>>;

export interface Progress { readonly done: number; readonly total: number }

/** Clé stable d'une action : « P02:3:0 » = playbook P02, section 3, première action. */
export function actionKey(playbookId: string, section: number, index: number): string {
  return `${playbookId}:${section}:${index}`;
}

/** Coche ou décoche une action ; la date de la coche est conservée pour le rapport. */
export function toggle(checked: Checked, key: string, now: Date): Checked {
  const next = { ...checked };
  if (key in next) delete next[key];
  else next[key] = now.toISOString();
  return next;
}

/** Avancement global et par section, en ne comptant que les actions de CE playbook. */
export function progress(playbook: Playbook, checked: Checked): { overall: Progress; sections: Map<number, Progress> } {
  const sections = new Map<number, Progress>();
  let done = 0;
  let total = 0;
  for (const section of playbook.sections) {
    const sectionDone = section.actions.filter((_a, i) => actionKey(playbook.id, section.number, i) in checked).length;
    sections.set(section.number, { done: sectionDone, total: section.actions.length });
    done += sectionDone;
    total += section.actions.length;
  }
  return { overall: { done, total }, sections };
}

/** Pourcentage arrondi à l'entier inférieur (100 % seulement quand tout est fait). */
export function percent({ done, total }: Progress): number {
  return total === 0 ? 0 : Math.floor((done / total) * 100);
}
