/**
 * Rapport Markdown, textes de l'interface et état enregistré.
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import { buildReport, sanitizeReference } from "../src/report.ts";
import { LANGS, MESSAGES, pickLang } from "../src/i18n.ts";
import { load, parseSaved, storageAvailable } from "../src/storage.ts";
import { doc } from "./fixture.ts";

const NOW = new Date("2026-11-08T15:00:00Z");

function sample(overrides: Partial<Parameters<typeof buildReport>[0]> = {}): string {
  const data = doc();
  return buildReport({
    doc: data,
    playbook: data.playbooks[0]!,
    level: "S1",
    raisedNote: "Relevée à S1 : le playbook P02 prévoit S1.",
    answers: ["S3", undefined, "unknown"],
    awareness: new Date("2026-11-08T10:00:00Z"),
    checked: { "P02:2:0": "2026-11-08T10:05:00Z" },
    reference: "INC-2026-014",
    now: NOW,
    ...overrides,
  }, MESSAGES.fr);
}

// ── Rapport ─────────────────────────────────────────────────
test("le rapport reprend gravité, critères, échéances et actions horodatées en UTC", () => {
  const text = sample();
  assert.match(text, /^# Suivi d'incident — INC-2026-014$/m);
  assert.match(text, /^- \*\*Rapport généré le\*\* : 2026-11-08 15:00 UTC$/m);
  assert.match(text, /^- \*\*Gravité\*\* : S1 — Critique \(Relevée à S1 : le playbook P02 prévoit S1\.\)$/m);
  assert.match(text, /^\| Activité \| S3 — Moyenne : Gêne limitée \|$/m);
  assert.match(text, /^\| Étendue \| non renseigné \|$/m);
  assert.match(text, /^\| Données \| Je ne sais pas encore \|$/m);
  assert.match(text, /^- \*\*Notification CNIL\*\* \(CNIL\) : échéance 2026-11-11 10:00 UTC$/m);
  assert.match(text, /^- \*\*Registre des violations\*\* \(Document interne\) : délai non chiffré — Toujours$/m);
  assert.match(text, /^- \[x\] Ouvrir le dossier — faite le 2026-11-08 10:05 UTC$/m);
  assert.match(text, /^- \[ \] Ouvrir un canal de crise$/m);
  assert.match(text, /fr\/docs\/D01-gravite-et-delais\.md, fr\/docs\/D04-cadre-reglementaire\.md, fr\/playbooks\/P02-rancongiciel\.md/);
});

test("un « | » dans une cellule est échappé pour ne pas casser le tableau", () => {
  assert.match(sample({ answers: [undefined, undefined, "S2"] }), /^\| Données \| S2 — Élevée : Exposées \\\| probable \|$/m);
});

test("sans playbook ni heure de prise de connaissance, le rapport reste lisible", () => {
  const text = sample({ playbook: null, awareness: null, level: null, raisedNote: null, reference: "" });
  assert.match(text, /^# Suivi d'incident$/m);
  assert.match(text, /^- \*\*Gravité\*\* : non qualifiée$/m);
  assert.match(text, /^- \*\*Notification CNIL\*\* \(CNIL\) : délai non chiffré — 72 heures/m);
  assert.doesNotMatch(text, /## Actions/);
});

test("la référence saisie ne peut pas injecter de Markdown ni de lien", () => {
  assert.equal(sanitizeReference("INC-2026-014"), "INC-2026-014");
  assert.equal(sanitizeReference("[clic](https://x.y) <script>"), "clichttpsx.yscript");
  assert.equal(sanitizeReference("A".repeat(60)).length, 40);
});

// ── Textes ──────────────────────────────────────────────────
test("le français et l'anglais définissent exactement les mêmes clés", () => {
  assert.deepEqual(Object.keys(MESSAGES.fr).sort(), Object.keys(MESSAGES.en).sort());
  assert.deepEqual(Object.keys(MESSAGES.fr.report).sort(), Object.keys(MESSAGES.en.report).sort());
});

test("aucun texte vide, dans aucune langue", () => {
  for (const lang of LANGS) {
    for (const [key, value] of Object.entries(MESSAGES[lang])) {
      if (typeof value === "string") assert.ok(value.trim().length > 0, `${lang}.${key}`);
    }
  }
});

test("choix de la langue : paramètre, puis navigateur, puis français", () => {
  assert.equal(pickLang("?lang=en", ["fr-FR"]), "en");
  assert.equal(pickLang("?lang=de", ["en-GB"]), "en");
  assert.equal(pickLang("", ["de-DE", "fr-CA"]), "fr");
  assert.equal(pickLang("", ["de-DE"]), "fr");
});

// ── État enregistré ─────────────────────────────────────────
const VALID = {
  v: 1, lang: "fr", playbook: "P02", answers: ["S1", null, "unknown"], awareness: "2026-11-08T10:00:00.000Z",
  checked: { "P02:3:0": "2026-11-08T10:05:00.000Z" }, reference: "INC-1",
};

test("un état enregistré valide est relu", () => {
  assert.deepEqual(parseSaved(JSON.stringify(VALID)), VALID);
});

test("un état modifié ou corrompu est ignoré", () => {
  const variants: unknown[] = [
    { ...VALID, v: 2 },
    { ...VALID, lang: "de" },
    { ...VALID, playbook: "<script>" },
    { ...VALID, answers: ["S9"] },
    { ...VALID, awareness: "hier" },
    { ...VALID, checked: { "../x": "2026-11-08T10:00:00Z" } },
    { ...VALID, checked: [] },
    { ...VALID, reference: 42 },
  ];
  for (const variant of variants) assert.equal(parseSaved(JSON.stringify(variant)), null, JSON.stringify(variant));
  assert.equal(parseSaved("{pas du JSON"), null);
  assert.equal(parseSaved(null), null);
});

test("sans stockage disponible, rien n'échoue", () => {
  assert.equal(storageAvailable(), false); // Node.js : pas de localStorage par défaut
  assert.equal(load(), null);
});
