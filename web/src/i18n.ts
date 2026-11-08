/**
 * Textes de l'interface, en français et en anglais.
 *
 * Le CONTENU métier (critères, délais, actions) vient de l'export JSON de la langue choisie ;
 * ce fichier ne contient que les libellés de l'interface elle-même. Les deux langues doivent
 * définir exactement les mêmes clés (vérifié par les tests).
 */

import type { Lang } from "./data.ts";

export const LANGS: readonly Lang[] = ["fr", "en"];

export interface Messages {
  readonly htmlTitle: string;
  readonly skipLink: string;
  readonly warning: string;
  readonly heading: string;
  readonly intro: string;
  readonly loading: string;
  readonly loadError: (detail: string) => string;
  // 1. Qualifier
  readonly triageTitle: string;
  readonly triageHelp: string;
  readonly unknown: string;
  readonly resultLabel: string;
  readonly resultNone: string;
  readonly decisive: (names: string) => string;
  readonly openCriteria: (count: number) => string;
  readonly raised: (level: string, playbook: string, allowed: string) => string;
  readonly timelinesTitle: string;
  readonly decisionNote: string;
  // 2. Choisir le playbook
  readonly playbookTitle: string;
  readonly playbookHelp: string;
  readonly playbookSeverity: (levels: string) => string;
  // 3. Échéances
  readonly deadlinesTitle: string;
  readonly awarenessLabel: string;
  readonly awarenessHint: string;
  readonly now: string;
  readonly awarenessInvalid: string;
  readonly remaining: (duration: string) => string;
  readonly overdue: (duration: string) => string;
  readonly dueAt: (stamp: string) => string;
  readonly untimed: string;
  readonly who: string;
  readonly recipient: string;
  readonly legalNote: string;
  // 4. Répondre
  readonly checklistTitle: string;
  readonly checklistNone: string;
  readonly progress: (done: number, total: number, pct: number) => string;
  readonly checkedAt: (stamp: string) => string;
  // 5. Rapport et enregistrement
  readonly reportTitle: string;
  readonly referenceLabel: string;
  readonly referenceHint: string;
  readonly copy: string;
  readonly copied: string;
  readonly copyFailed: string;
  readonly download: string;
  readonly saveLabel: string;
  readonly saveHint: string;
  readonly saveUnavailable: string;
  readonly clear: string;
  readonly cleared: string;
  // Pied de page
  readonly footerSource: string;
  readonly footerPrivacy: string;
  readonly footerVersion: (tool: string, attack: string) => string;
  // Rapport Markdown
  readonly report: {
    readonly title: string;
    readonly reference: string;
    readonly generated: string;
    readonly playbook: string;
    readonly severity: string;
    readonly severityNone: string;
    readonly criteria: string;
    readonly notAnswered: string;
    readonly awareness: string;
    readonly deadlines: string;
    readonly due: string;
    readonly untimed: string;
    readonly actions: string;
    readonly doneAt: string;
    readonly footer: (tool: string, sources: string) => string;
  };
}

export const MESSAGES: Readonly<Record<Lang, Messages>> = {
  fr: {
    htmlTitle: "Réponse aux incidents — triage, actions et délais légaux",
    skipLink: "Aller au contenu",
    warning: "Aide à la décision : ne saisissez ici aucune donnée confidentielle (noms, adresses IP, identifiants).",
    heading: "Un incident commence : par où commencer ?",
    intro: "Qualifiez la gravité, choisissez le bon playbook, suivez les échéances légales et cochez les actions au fil de la réponse. Tout se passe dans votre navigateur.",
    loading: "Chargement des playbooks…",
    loadError: (detail) => `Impossible de charger les playbooks : ${detail}`,
    triageTitle: "1. Qualifier la gravité",
    triageHelp: "Pour chaque critère, choisissez la description la plus proche de la situation. Le critère le plus grave l'emporte (D01).",
    unknown: "Je ne sais pas encore",
    resultLabel: "Gravité estimée",
    resultNone: "Répondez à au moins un critère.",
    decisive: (names) => `Critère décisif : ${names}.`,
    openCriteria: (count) => `${count} critère(s) à préciser : dans le doute, retenez le niveau le plus élevé et réévaluez au prochain point de situation.`,
    raised: (level, playbook, allowed) => `Relevée à ${level} : le playbook ${playbook} prévoit ${allowed}.`,
    timelinesTitle: "Délais internes pour ce niveau",
    decisionNote: "La qualification finale revient à la personne qui pilote l'incident.",
    playbookTitle: "2. Choisir le playbook",
    playbookHelp: "Choisissez le playbook dont la description correspond le mieux à ce que vous observez.",
    playbookSeverity: (levels) => `Gravité prévue : ${levels}`,
    deadlinesTitle: "3. Échéances légales",
    awarenessLabel: "Prise de connaissance de l'incident (heure locale)",
    awarenessHint: "Les délais légaux courent à partir du moment où l'organisation a connaissance de l'incident.",
    now: "Maintenant",
    awarenessInvalid: "Date ou heure invalide.",
    remaining: (duration) => `reste ${duration}`,
    overdue: (duration) => `dépassée depuis ${duration}`,
    dueAt: (stamp) => `échéance : ${stamp}`,
    untimed: "Délai non chiffré",
    who: "Concerné :",
    recipient: "Destinataire :",
    legalNote: "Repères vérifiés, pas un avis juridique : faites valider chaque démarche par votre juridique ou votre DPO (D04).",
    checklistTitle: "4. Répondre",
    checklistNone: "Choisissez d'abord un playbook à l'étape 2.",
    progress: (done, total, pct) => `${done} / ${total} actions faites (${pct} %)`,
    checkedAt: (stamp) => `cochée ${stamp}`,
    reportTitle: "5. Rapport",
    referenceLabel: "Référence de l'incident (facultatif)",
    referenceHint: "Lettres, chiffres et tirets, par exemple INC-2026-014.",
    copy: "Copier le rapport Markdown",
    copied: "Rapport copié dans le presse-papiers.",
    copyFailed: "Copie impossible dans ce navigateur : utilisez le téléchargement.",
    download: "Télécharger (.md)",
    saveLabel: "Conserver la progression dans ce navigateur",
    saveHint: "Désactivé par défaut : les détails d'un incident sont sensibles. Une fois activé, l'état est conservé sur cet appareil, en clair, jusqu'à « Tout effacer ».",
    saveUnavailable: "Ce navigateur bloque le stockage local : la progression ne peut pas être conservée.",
    clear: "Tout effacer",
    cleared: "Tout est effacé.",
    footerSource: "Playbooks complets et code source sur GitHub",
    footerPrivacy: "Aucune donnée ne quitte votre navigateur : pas de serveur, pas de mesure d'audience, pas de cookie.",
    footerVersion: (tool, attack) => `incident-response-playbook ${tool} · MITRE ATT&CK ${attack}`,
    report: {
      title: "Suivi d'incident",
      reference: "Référence",
      generated: "Rapport généré le",
      playbook: "Playbook",
      severity: "Gravité",
      severityNone: "non qualifiée",
      criteria: "Critères (D01)",
      notAnswered: "non renseigné",
      awareness: "Prise de connaissance",
      deadlines: "Échéances légales (D04)",
      due: "échéance",
      untimed: "délai non chiffré",
      actions: "Actions",
      doneAt: "faite le",
      footer: (tool, sources) => `Généré avec incident-response-playbook ${tool}. Documents de référence : ${sources}. Toutes les heures sont en UTC.`,
    },
  },
  en: {
    htmlTitle: "Incident response — triage, actions and legal deadlines",
    skipLink: "Skip to content",
    warning: "Decision aid: do not enter any confidential data here (names, IP addresses, credentials).",
    heading: "An incident is starting: where do you begin?",
    intro: "Assess the severity, pick the right playbook, track the legal deadlines and tick the actions as the response unfolds. Everything happens in your browser.",
    loading: "Loading the playbooks…",
    loadError: (detail) => `The playbooks could not be loaded: ${detail}`,
    triageTitle: "1. Assess the severity",
    triageHelp: "For each criterion, choose the description closest to the situation. The most severe criterion wins (D01).",
    unknown: "Not known yet",
    resultLabel: "Estimated severity",
    resultNone: "Answer at least one criterion.",
    decisive: (names) => `Deciding criterion: ${names}.`,
    openCriteria: (count) => `${count} criterion/criteria still open: when in doubt, keep the higher level and reassess at the next status update.`,
    raised: (level, playbook, allowed) => `Raised to ${level}: playbook ${playbook} expects ${allowed}.`,
    timelinesTitle: "Internal timelines for this level",
    decisionNote: "The final classification belongs to the person leading the incident.",
    playbookTitle: "2. Pick the playbook",
    playbookHelp: "Choose the playbook whose description best matches what you observe.",
    playbookSeverity: (levels) => `Expected severity: ${levels}`,
    deadlinesTitle: "3. Legal deadlines",
    awarenessLabel: "Time the incident became known (local time)",
    awarenessHint: "Legal deadlines run from the moment the organisation becomes aware of the incident.",
    now: "Now",
    awarenessInvalid: "Invalid date or time.",
    remaining: (duration) => `${duration} left`,
    overdue: (duration) => `overdue by ${duration}`,
    dueAt: (stamp) => `due: ${stamp}`,
    untimed: "No fixed deadline",
    who: "Who:",
    recipient: "Recipient:",
    legalNote: "Verified reference points, not legal advice: have every step approved by your legal team or DPO (D04).",
    checklistTitle: "4. Respond",
    checklistNone: "Pick a playbook in step 2 first.",
    progress: (done, total, pct) => `${done} / ${total} actions done (${pct}%)`,
    checkedAt: (stamp) => `ticked ${stamp}`,
    reportTitle: "5. Report",
    referenceLabel: "Incident reference (optional)",
    referenceHint: "Letters, digits and dashes, for example INC-2026-014.",
    copy: "Copy the Markdown report",
    copied: "Report copied to the clipboard.",
    copyFailed: "Copying is not possible in this browser: use the download instead.",
    download: "Download (.md)",
    saveLabel: "Keep progress in this browser",
    saveHint: "Off by default: incident details are sensitive. Once enabled, the state is kept on this device, unencrypted, until \"Clear everything\".",
    saveUnavailable: "This browser blocks local storage: progress cannot be kept.",
    clear: "Clear everything",
    cleared: "Everything has been cleared.",
    footerSource: "Full playbooks and source code on GitHub",
    footerPrivacy: "No data leaves your browser: no server, no analytics, no cookies.",
    footerVersion: (tool, attack) => `incident-response-playbook ${tool} · MITRE ATT&CK ${attack}`,
    report: {
      title: "Incident tracking",
      reference: "Reference",
      generated: "Report generated on",
      playbook: "Playbook",
      severity: "Severity",
      severityNone: "not assessed",
      criteria: "Criteria (D01)",
      notAnswered: "not answered",
      awareness: "Became known",
      deadlines: "Legal deadlines (D04)",
      due: "due",
      untimed: "no fixed deadline",
      actions: "Actions",
      doneAt: "done on",
      footer: (tool, sources) => `Generated with incident-response-playbook ${tool}. Reference documents: ${sources}. All times are in UTC.`,
    },
  },
};

/** Langue de départ : paramètre « ?lang= », sinon langue du navigateur, sinon français. */
export function pickLang(search: string, navigatorLanguages: readonly string[]): Lang {
  const asked = new URLSearchParams(search).get("lang");
  if (asked === "fr" || asked === "en") return asked;
  for (const tag of navigatorLanguages) {
    const base = tag.toLowerCase().split("-")[0];
    if (base === "fr" || base === "en") return base;
  }
  return "fr";
}
