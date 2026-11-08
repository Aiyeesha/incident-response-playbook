/**
 * Export JSON minimal et valide (format 2), utilisé par tous les tests.
 * Chaque test le copie (structuredClone) avant de le modifier : aucun test n'en influence un autre.
 */

import { parseExport, type ExportDoc } from "../src/data.ts";

const levels = (s1: string, s2: string, s3: string, s4: string) => ({ S1: s1, S2: s2, S3: s3, S4: s4 });

export const RAW = {
  schema_version: 2,
  tool_version: "1.1.0",
  attack_version: "20.1",
  lang: "fr",
  severity: {
    levels: [
      { id: "S1", label: "Critique" }, { id: "S2", label: "Élevée" },
      { id: "S3", label: "Moyenne" }, { id: "S4", label: "Faible" },
    ],
    criteria: [
      { name: "Activité", levels: levels("Activité arrêtée", "Service dégradé", "Gêne limitée", "Aucun effet") },
      { name: "Étendue", levels: levels("Plusieurs sites", "Un serveur", "Un poste", "Aucun système") },
      { name: "Données", levels: levels("Exfiltrées", "Exposées | probable", "Peu sensibles", "Aucune") },
    ],
    timelines: [
      { name: "Prise en charge", description: "Prise en charge (un analyste commence)", levels: levels("15 minutes", "1 heure", "4 heures", "1 jour ouvré") },
    ],
    source: "fr/docs/D01-gravite-et-delais.md",
  },
  obligations: {
    items: [
      { name: "Notification CNIL", who: "Responsable de traitement", deadline: "72 heures après la prise de connaissance", recipient: "CNIL", hours: 72 },
      { name: "Alerte précoce NIS 2", who: "Entités NIS 2", deadline: "24 heures", recipient: "CSIRT", hours: 24 },
      { name: "Registre des violations", who: "Responsable de traitement", deadline: "Toujours", recipient: "Document interne", hours: null },
    ],
    source: "fr/docs/D04-cadre-reglementaire.md",
  },
  playbooks: [
    {
      id: "P02",
      title: "Attaque par rançongiciel",
      severity: ["S1"],
      owner: "Responsable SOC",
      review: "2026-11-07",
      when: "des fichiers sont chiffrés",
      mitre: [{ id: "T1486", name: "Data Encrypted for Impact" }],
      source: "fr/playbooks/P02-rancongiciel.md",
      sections: [
        { number: 1, title: "Détection", actions: [] },
        { number: 2, title: "Triage", actions: ["Ouvrir le dossier", "Ouvrir un canal de crise"] },
        { number: 3, title: "Confinement", actions: ["Isoler les postes"] },
      ],
    },
    {
      id: "P04",
      title: "Hameçonnage",
      severity: ["S2", "S3", "S4"],
      owner: "Responsable SOC",
      review: "2026-11-07",
      when: "un courriel frauduleux est signalé",
      mitre: [{ id: "T1566", name: "Phishing" }],
      source: "fr/playbooks/P04-hameconnage.md",
      sections: [{ number: 2, title: "Triage", actions: ["Isoler le courriel"] }],
    },
  ],
};

/** Copie modifiable de l'export brut. */
export function raw(): typeof RAW {
  return structuredClone(RAW);
}

/** Export validé, prêt à l'emploi. */
export function doc(): ExportDoc {
  return parseExport(raw(), "fr");
}
