/**
 * Rapport Markdown de suivi, à coller dans le rapport d'incident (modèle T01).
 *
 * Toutes les heures sont en UTC, comme l'exige le registre de preuves (T04).
 * La seule saisie libre (la référence de l'incident) est filtrée : elle ne peut pas
 * injecter de Markdown ni de lien dans le rapport.
 */

import { LEVEL_IDS, type ExportDoc, type LevelId, type Playbook } from "./data.ts";
import type { Answer } from "./triage.ts";
import { actionKey, type Checked } from "./checklist.ts";
import { computeDeadlines, utcStamp } from "./deadlines.ts";
import type { Messages } from "./i18n.ts";

export interface ReportInput {
  readonly doc: ExportDoc;
  readonly playbook: Playbook | null;
  readonly level: LevelId | null;
  readonly raisedNote: string | null;
  readonly answers: readonly (Answer | undefined)[];
  readonly awareness: Date | null;
  readonly checked: Checked;
  readonly reference: string;
  readonly now: Date;
}

/** Référence d'incident sûre : lettres, chiffres, tiret, point, souligné ; 40 caractères au plus. */
export function sanitizeReference(value: string): string {
  return value.replace(/[^A-Za-z0-9._-]/g, "").slice(0, 40);
}

/** Une cellule de tableau Markdown ne doit pas contenir de « | » ni de retour à la ligne. */
const cell = (value: string): string => value.replace(/\|/g, "\\|").replace(/\s+/g, " ").trim();

export function buildReport(input: ReportInput, messages: Messages): string {
  const r = messages.report;
  const { doc, playbook, level, checked } = input;
  const label = (id: LevelId): string => `${id} — ${doc.severity.levels[LEVEL_IDS.indexOf(id)]?.label ?? ""}`;
  const reference = sanitizeReference(input.reference);
  const lines: string[] = [];

  // ── En-tête ─────────────────────────────────────────────
  lines.push(`# ${r.title}${reference ? ` — ${reference}` : ""}`, "");
  if (reference) lines.push(`- **${r.reference}** : ${reference}`);
  lines.push(`- **${r.generated}** : ${utcStamp(input.now)}`);
  lines.push(`- **${r.playbook}** : ${playbook ? `${playbook.id} — ${playbook.title}` : r.notAnswered}`);
  lines.push(`- **${r.severity}** : ${level ? label(level) : r.severityNone}${input.raisedNote ? ` (${input.raisedNote})` : ""}`);
  lines.push(`- **${r.awareness}** : ${input.awareness ? utcStamp(input.awareness) : r.notAnswered}`, "");

  // ── Critères de gravité ─────────────────────────────────
  lines.push(`## ${r.criteria}`, "", "| | |", "|---|---|");
  doc.severity.criteria.forEach((criterion, i) => {
    const answer = input.answers[i];
    const value = answer && answer !== "unknown" ? `${label(answer)} : ${criterion.levels[answer]}` : messages.unknown;
    lines.push(`| ${cell(criterion.name)} | ${cell(answer === undefined ? r.notAnswered : value)} |`);
  });
  lines.push("");

  // ── Échéances légales ───────────────────────────────────
  lines.push(`## ${r.deadlines}`, "");
  const dues = input.awareness ? computeDeadlines(doc.obligations.items, input.awareness, input.now) : [];
  doc.obligations.items.forEach((obligation, i) => {
    const due = dues[i]?.due;
    const when = due ? `${r.due} ${utcStamp(due)}` : `${r.untimed} — ${obligation.deadline}`;
    lines.push(`- **${obligation.name}** (${obligation.recipient}) : ${when}`);
  });
  lines.push("");

  // ── Actions, section par section ────────────────────────
  if (playbook) {
    lines.push(`## ${r.actions} — ${playbook.id}`, "");
    for (const section of playbook.sections) {
      lines.push(`### ${section.number}. ${section.title}`, "");
      section.actions.forEach((action, i) => {
        const doneAt = checked[actionKey(playbook.id, section.number, i)];
        lines.push(doneAt ? `- [x] ${action} — ${r.doneAt} ${utcStamp(new Date(doneAt))}` : `- [ ] ${action}`);
      });
      lines.push("");
    }
  }

  // ── Pied de rapport : traçabilité des sources ───────────
  const sources = [doc.severity.source, doc.obligations.source, ...(playbook ? [playbook.source] : [])].join(", ");
  lines.push("---", "", r.footer(doc.tool_version, sources), "");
  return lines.join("\n");
}
