/**
 * Vérification des VRAIS exports, quand ils ont été générés dans web/data/ :
 *   playbook-export --lang fr -o web/data/playbooks.fr.json
 *   playbook-export --lang en -o web/data/playbooks.en.json
 * En CI, ils le sont toujours avant les tests ; en local, ces tests sont sautés s'ils manquent.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";

import { parseExport, type ExportDoc, type Lang } from "../src/data.ts";
import { actionKey } from "../src/checklist.ts";

const path = (lang: Lang): URL => new URL(`../data/playbooks.${lang}.json`, import.meta.url);
const available = existsSync(path("fr")) && existsSync(path("en"));
const read = (lang: Lang): ExportDoc => parseExport(JSON.parse(readFileSync(path(lang), "utf8")), lang);

test("les exports réels sont valides dans les deux langues", { skip: !available && "exports absents de web/data/" }, () => {
  const fr = read("fr");
  const en = read("en");
  assert.equal(fr.playbooks.length, en.playbooks.length);
  assert.ok(fr.obligations.items.some((o) => o.hours !== null), "au moins un délai légal chiffré");
});

test("une action cochée garde la même clé d'une langue à l'autre", { skip: !available && "exports absents de web/data/" }, () => {
  const keys = (doc: ExportDoc): string[] => doc.playbooks.flatMap((p) =>
    p.sections.flatMap((s) => s.actions.map((_a, i) => actionKey(p.id, s.number, i))));
  assert.deepEqual(keys(read("fr")), keys(read("en")));
});

test("mêmes délais chiffrés et même grille dans les deux langues", { skip: !available && "exports absents de web/data/" }, () => {
  const fr = read("fr");
  const en = read("en");
  assert.deepEqual(fr.obligations.items.map((o) => o.hours), en.obligations.items.map((o) => o.hours));
  assert.equal(fr.severity.criteria.length, en.severity.criteria.length);
});
