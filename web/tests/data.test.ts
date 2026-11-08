/**
 * Validation de l'export JSON : ce qui est accepté, et surtout ce qui est refusé.
 */

import { test } from "node:test";
import assert from "node:assert/strict";

import { DataError, parseExport } from "../src/data.ts";
import { raw } from "./fixture.ts";

test("un export valide est accepté et typé", () => {
  const doc = parseExport(raw(), "fr");
  assert.equal(doc.playbooks.length, 2);
  assert.equal(doc.obligations.items[0]?.hours, 72);
  assert.equal(doc.obligations.items[2]?.hours, null);
  assert.equal(doc.severity.criteria[1]?.levels.S3, "Un poste");
});

test("un ancien format est refusé avec un message clair", () => {
  const data = { ...raw(), schema_version: 1 };
  assert.throws(() => parseExport(data, "fr"), /format 1 non pris en charge \(attendu : 2\)/);
});

test("un export d'une autre langue est refusé", () => {
  assert.throws(() => parseExport(raw(), "en"), /langue « fr » au lieu de « en »/);
});

test("le chemin du champ fautif est indiqué", () => {
  const data = raw();
  (data.playbooks[1] as { when: string }).when = "";
  assert.throws(() => parseExport(data, "fr"), (error: unknown) =>
    error instanceof DataError && error.message === "playbooks[1].when : texte non vide attendu");
});

test("les niveaux doivent être S1, S2, S3, S4 dans cet ordre", () => {
  const data = raw();
  data.severity.levels.reverse();
  assert.throws(() => parseExport(data, "fr"), /S1, S2, S3, S4 attendus/);
});

test("un délai en heures doit être un entier positif ou null", () => {
  for (const hours of [0, -24, 1.5, "72"]) {
    const data = raw();
    (data.obligations.items[0] as { hours: unknown }).hours = hours;
    assert.throws(() => parseExport(data, "fr"), /hours : entier positif ou null attendu/, String(hours));
  }
});

test("un identifiant de playbook en double ou mal formé est refusé", () => {
  const double = raw();
  double.playbooks[1]!.id = "P02";
  assert.throws(() => parseExport(double, "fr"), /identifiant invalide ou en double/);
  const malforme = raw();
  malforme.playbooks[0]!.id = "<img>";
  assert.throws(() => parseExport(malforme, "fr"), /identifiant invalide ou en double/);
});

test("une gravité de playbook inconnue est refusée", () => {
  const data = raw();
  data.playbooks[0]!.severity = ["S5"];
  assert.throws(() => parseExport(data, "fr"), /playbooks\[0\]\.severity\[0\] : niveau S1 à S4 attendu/);
});

test("une valeur qui n'est pas un objet est refusée", () => {
  assert.throws(() => parseExport(null, "fr"), /export : objet attendu/);
  assert.throws(() => parseExport([], "fr"), /export : objet attendu/);
});
