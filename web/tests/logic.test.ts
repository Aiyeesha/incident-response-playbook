/**
 * Règles métier : gravité (D01), échéances légales (D04) et actions à cocher.
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import { adjustForPlaybook, assess } from "../src/triage.ts";
import {
  computeDeadlines, formatDuration, parseLocalDateTime, sortByUrgency, toLocalInput, utcStamp,
} from "../src/deadlines.ts";
import { actionKey, percent, progress, toggle } from "../src/checklist.ts";
import { doc } from "./fixture.ts";

const HOUR = 3_600_000;

// ── Gravité ─────────────────────────────────────────────────
test("le critère le plus grave l'emporte", () => {
  const { criteria } = doc().severity;
  const result = assess(criteria, ["S3", "S2", "S4"]);
  assert.equal(result.level, "S2");
  assert.deepEqual(result.decisive, ["Étendue"]);
  assert.equal(result.open, 0);
});

test("plusieurs critères décisifs sont tous cités", () => {
  const result = assess(doc().severity.criteria, ["S1", "S3", "S1"]);
  assert.deepEqual(result.decisive, ["Activité", "Données"]);
});

test("sans réponse, aucun niveau ; « je ne sais pas » compte comme critère ouvert", () => {
  const { criteria } = doc().severity;
  assert.deepEqual(assess(criteria, []), { level: null, decisive: [], open: 3 });
  const partial = assess(criteria, ["unknown", "S4"]);
  assert.equal(partial.level, "S4");
  assert.equal(partial.open, 2);
});

test("le playbook relève la gravité au niveau prévu le plus proche, sans jamais l'abaisser", () => {
  assert.deepEqual(adjustForPlaybook("S3", ["S1"]), { level: "S1", raised: true }); // rançongiciel : toujours S1
  assert.deepEqual(adjustForPlaybook("S4", ["S1", "S2"]), { level: "S2", raised: true });
  assert.deepEqual(adjustForPlaybook("S1", ["S2", "S3"]), { level: "S1", raised: false }); // plus grave : on garde
  assert.deepEqual(adjustForPlaybook("S3", ["S2", "S3", "S4"]), { level: "S3", raised: false });
  assert.deepEqual(adjustForPlaybook(null, ["S1"]), { level: null, raised: false });
  assert.deepEqual(adjustForPlaybook("S3", []), { level: "S3", raised: false });
});

// ── Échéances ───────────────────────────────────────────────
test("les échéances se calculent depuis la prise de connaissance", () => {
  const awareness = new Date("2026-11-08T10:00:00Z");
  const now = new Date("2026-11-09T06:00:00Z"); // 20 h plus tard
  const [cnil, nis2, registre] = computeDeadlines(doc().obligations.items, awareness, now);
  assert.equal(cnil?.due?.toISOString(), "2026-11-11T10:00:00.000Z");
  assert.equal(cnil?.status, "pending");
  assert.equal(nis2?.remaining, 4 * HOUR);
  assert.equal(nis2?.status, "soon"); // moins de 6 h
  assert.equal(registre?.status, "untimed");
  assert.equal(registre?.due, null);
});

test("une échéance dépassée a un reste négatif", () => {
  const dues = computeDeadlines(doc().obligations.items, new Date("2026-11-01T00:00:00Z"), new Date("2026-11-02T01:00:00Z"));
  assert.equal(dues[1]?.status, "overdue");
  assert.equal(dues[1]?.remaining, -1 * HOUR);
});

test("les échéances chiffrées passent d'abord, de la plus proche à la plus lointaine", () => {
  const dues = computeDeadlines(doc().obligations.items, new Date("2026-11-08T10:00:00Z"), new Date("2026-11-08T10:00:00Z"));
  assert.deepEqual(sortByUrgency(dues).map((d) => d.obligation.hours), [24, 72, null]);
});

test("durées lisibles en français et en anglais", () => {
  assert.equal(formatDuration(2 * 24 * HOUR + 4 * HOUR + 12 * 60_000, "fr"), "2 j 04 h 12 min");
  assert.equal(formatDuration(2 * 24 * HOUR + 4 * HOUR + 12 * 60_000, "en"), "2 d 04 h 12 min");
  assert.equal(formatDuration(-(3 * HOUR + 5 * 60_000), "fr"), "3 h 05 min"); // le signe est géré par l'appelant
  assert.equal(formatDuration(59_999, "en"), "0 h 00 min");
});

test("horodatage UTC du rapport", () => {
  assert.equal(utcStamp(new Date("2026-11-08T14:32:59Z")), "2026-11-08 14:32 UTC");
});

test("lecture du champ date et heure locale, dates impossibles refusées", () => {
  const date = parseLocalDateTime("2026-11-08T14:32");
  assert.ok(date);
  assert.equal(toLocalInput(date), "2026-11-08T14:32");
  for (const invalid of ["", "2026-02-31T10:00", "2026-11-08T25:00", "2026-11-08 14:32", "abc"]) {
    assert.equal(parseLocalDateTime(invalid), null, invalid);
  }
});

// ── Actions à cocher ────────────────────────────────────────
test("cocher puis décocher, sans modifier l'état d'origine", () => {
  const key = actionKey("P02", 3, 0);
  assert.equal(key, "P02:3:0");
  const empty = {};
  const checked = toggle(empty, key, new Date("2026-11-08T10:00:00Z"));
  assert.deepEqual(checked, { "P02:3:0": "2026-11-08T10:00:00.000Z" });
  assert.deepEqual(empty, {});
  assert.deepEqual(toggle(checked, key, new Date()), {});
});

test("avancement global et par section, limité au playbook choisi", () => {
  const playbook = doc().playbooks[0]!;
  const checked = { "P02:2:1": "2026-11-08T10:00:00Z", "P04:2:0": "2026-11-08T10:00:00Z" };
  const { overall, sections } = progress(playbook, checked);
  assert.deepEqual(overall, { done: 1, total: 3 });
  assert.deepEqual(sections.get(2), { done: 1, total: 2 });
  assert.deepEqual(sections.get(1), { done: 0, total: 0 });
  assert.equal(percent(overall), 33);
  assert.equal(percent({ done: 0, total: 0 }), 0);
  assert.equal(percent({ done: 3, total: 3 }), 100);
});
