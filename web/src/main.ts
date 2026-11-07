/**
 * Liaison entre la page (index.html) et les modules (data, triage, deadlines, checklist, report).
 *
 * Règles de sécurité appliquées ici :
 *   - le texte est TOUJOURS inséré avec textContent, jamais innerHTML : ni les playbooks ni la
 *     saisie de l'utilisateur ne peuvent injecter de code dans la page ;
 *   - la seule requête réseau lit les playbooks JSON de ce site (CSP : connect-src 'self') ;
 *   - rien n'est conservé, sauf si l'utilisateur active explicitement l'enregistrement local.
 */

import { LEVEL_IDS, parseExport, type ExportDoc, type Lang, type LevelId, type Playbook } from "./data.ts";
import { adjustForPlaybook, assess, type Answer } from "./triage.ts";
import { computeDeadlines, formatDuration, parseLocalDateTime, sortByUrgency, toLocalInput, utcStamp } from "./deadlines.ts";
import { actionKey, percent, progress, toggle, type Checked } from "./checklist.ts";
import { buildReport, sanitizeReference } from "./report.ts";
import { LANGS, MESSAGES, pickLang, type Messages } from "./i18n.ts";
import * as storage from "./storage.ts";

const REPO = "https://github.com/Aiyeesha/incident-response-playbook/blob/main/";

// ─────────────────────────────────────────────────────────────
// 1. Accès aux éléments de la page
// ─────────────────────────────────────────────────────────────
/** Récupère un élément par son id, ou arrête tout si la page est incomplète. */
function byId<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Élément #${id} introuvable dans index.html`);
  return element as T;
}

/** Crée un élément avec ses classes, son texte et ses attributs, sans jamais interpréter de HTML. */
function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  options: { className?: string; text?: string; attrs?: Record<string, string> } = {},
  children: readonly Node[] = [],
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (options.className) node.className = options.className;
  if (options.text !== undefined) node.textContent = options.text;
  for (const [name, value] of Object.entries(options.attrs ?? {})) node.setAttribute(name, value);
  node.append(...children);
  return node;
}

const ui = {
  app: byId<HTMLElement>("app"),
  status: byId<HTMLElement>("status"),
  criteria: byId<HTMLElement>("criteria"),
  levelBadge: byId<HTMLElement>("level-badge"),
  resultDetail: byId<HTMLElement>("result-detail"),
  resultOpen: byId<HTMLElement>("result-open"),
  resultRaised: byId<HTMLElement>("result-raised"),
  timelinesBox: byId<HTMLElement>("timelines-box"),
  timelines: byId<HTMLElement>("timelines"),
  playbooks: byId<HTMLElement>("playbooks"),
  awareness: byId<HTMLInputElement>("awareness"),
  awarenessNow: byId<HTMLButtonElement>("awareness-now"),
  awarenessError: byId<HTMLElement>("awareness-error"),
  dues: byId<HTMLUListElement>("dues"),
  checklistNone: byId<HTMLElement>("checklist-none"),
  checklistBox: byId<HTMLElement>("checklist-box"),
  progressText: byId<HTMLElement>("progress-text"),
  progressBar: byId<HTMLElement>("progress-bar"),
  sections: byId<HTMLElement>("sections"),
  reference: byId<HTMLInputElement>("reference"),
  copy: byId<HTMLButtonElement>("copy"),
  download: byId<HTMLButtonElement>("download"),
  reportStatus: byId<HTMLElement>("report-status"),
  save: byId<HTMLInputElement>("save"),
  clear: byId<HTMLButtonElement>("clear"),
};

// ─────────────────────────────────────────────────────────────
// 2. État de l'interface
// ─────────────────────────────────────────────────────────────
interface State {
  lang: Lang;
  doc: ExportDoc | null;
  answers: (Answer | undefined)[];
  playbookId: string | null;
  awareness: Date | null;
  checked: Checked;
  saveEnabled: boolean;
}

const saved = storage.load();
const state: State = {
  lang: saved?.lang ?? pickLang(location.search, navigator.languages),
  doc: null,
  answers: saved ? saved.answers.map((a) => a ?? undefined) : [],
  playbookId: saved?.playbook ?? null,
  awareness: saved?.awareness ? new Date(saved.awareness) : null,
  checked: saved?.checked ?? {},
  saveEnabled: saved !== null, // un état relu prouve que l'utilisateur avait activé l'enregistrement
};
if (saved) ui.reference.value = saved.reference;

const docs = new Map<Lang, ExportDoc>(); // exports déjà chargés, pour changer de langue sans réseau
const t = (): Messages => MESSAGES[state.lang];
const currentPlaybook = (): Playbook | null => state.doc?.playbooks.find((p) => p.id === state.playbookId) ?? null;
const levelLabel = (id: LevelId): string =>
  `${id} — ${state.doc?.severity.levels[LEVEL_IDS.indexOf(id)]?.label ?? ""}`;

/** Enregistre l'état si (et seulement si) l'utilisateur l'a demandé. */
function persist(): void {
  if (!state.saveEnabled) return;
  storage.save({
    v: 1,
    lang: state.lang,
    playbook: state.playbookId,
    answers: state.answers.map((a) => a ?? null),
    awareness: state.awareness?.toISOString() ?? null,
    checked: state.checked,
    reference: sanitizeReference(ui.reference.value),
  });
}

// ─────────────────────────────────────────────────────────────
// 3. Chargement des données
// ─────────────────────────────────────────────────────────────
async function loadDoc(lang: Lang): Promise<ExportDoc> {
  const cached = docs.get(lang);
  if (cached) return cached;
  const response = await fetch(`./data/playbooks.${lang}.json`, { cache: "no-cache" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const doc = parseExport(await response.json(), lang);
  docs.set(lang, doc);
  return doc;
}

// ─────────────────────────────────────────────────────────────
// 4. Textes fixes de la page
// ─────────────────────────────────────────────────────────────
function renderStatic(): void {
  const m = t();
  document.documentElement.lang = state.lang;
  document.title = m.htmlTitle;
  const texts: Record<string, string> = {
    "skip-link": m.skipLink, warning: m.warning, heading: m.heading, intro: m.intro,
    "triage-title": m.triageTitle, "triage-help": m.triageHelp, "result-label": m.resultLabel,
    "decision-note": m.decisionNote, "timelines-title": m.timelinesTitle,
    "playbook-title": m.playbookTitle, "playbook-help": m.playbookHelp, "playbook-legend": m.playbookTitle,
    "deadlines-title": m.deadlinesTitle, "awareness-label": m.awarenessLabel, "awareness-now": m.now,
    "awareness-hint": m.awarenessHint, "legal-note": m.legalNote,
    "checklist-title": m.checklistTitle, "checklist-none": m.checklistNone,
    "report-title": m.reportTitle, "reference-label": m.referenceLabel, "reference-hint": m.referenceHint,
    copy: m.copy, download: m.download, "save-label": m.saveLabel, "save-hint": m.saveHint, clear: m.clear,
    "source-link": m.footerSource, "footer-privacy": m.footerPrivacy,
  };
  for (const [id, value] of Object.entries(texts)) byId(id).textContent = value;
  for (const lang of LANGS) byId(`lang-${lang}`).setAttribute("aria-pressed", String(lang === state.lang));
  byId("footer-version").textContent = state.doc ? m.footerVersion(state.doc.tool_version, state.doc.attack_version) : "";
}

// ─────────────────────────────────────────────────────────────
// 5. Étape 1 : critères de gravité
// ─────────────────────────────────────────────────────────────
function renderCriteria(doc: ExportDoc): void {
  const m = t();
  ui.criteria.replaceChildren(...doc.severity.criteria.map((criterion, i) => {
    const name = `criterion-${i}`;
    // Une option par niveau, puis « je ne sais pas encore »
    const options: [Answer, string][] = [...LEVEL_IDS.map((id): [Answer, string] => [id, criterion.levels[id]]), ["unknown", m.unknown]];
    return el("fieldset", { className: "criterion" }, [
      el("legend", { text: criterion.name }),
      ...options.map(([value, description]) => {
        const input = el("input", { attrs: { type: "radio", name, value } });
        input.checked = state.answers[i] === value;
        input.addEventListener("change", () => {
          state.answers[i] = value;
          renderResult();
          persist();
        });
        const tag = value === "unknown" ? "?" : value;
        return el("label", { className: "option", attrs: { "data-level": value } }, [
          input, el("span", { className: "option-level", text: tag, attrs: { "aria-hidden": "true" } }),
          el("span", { text: description }),
        ]);
      }),
    ]);
  }));
}

function renderResult(): void {
  const doc = state.doc;
  if (!doc) return;
  const m = t();
  const assessment = assess(doc.severity.criteria, state.answers);
  const playbook = currentPlaybook();
  const adjusted = adjustForPlaybook(assessment.level, playbook?.severity ?? []);
  const level = adjusted.level;

  ui.levelBadge.dataset["level"] = level ?? "none";
  ui.levelBadge.textContent = level ? levelLabel(level) : "—";
  ui.resultDetail.textContent = level ? m.decisive(assessment.decisive.join(", ")) : m.resultNone;
  ui.resultOpen.textContent = assessment.open > 0 && level ? m.openCriteria(assessment.open) : "";
  ui.resultRaised.textContent = adjusted.raised && playbook && level
    ? m.raised(level, playbook.id, playbook.severity.join(", ")) : "";

  // Délais internes du niveau retenu (D01, section 3)
  ui.timelinesBox.hidden = level === null;
  if (level) {
    ui.timelines.replaceChildren(...doc.severity.timelines.map((row) =>
      el("tr", {}, [el("th", { text: row.description, attrs: { scope: "row" } }), el("td", { text: row.levels[level] })])));
  }
}

// ─────────────────────────────────────────────────────────────
// 6. Étape 2 : choix du playbook
// ─────────────────────────────────────────────────────────────
function renderPlaybooks(doc: ExportDoc): void {
  const m = t();
  ui.playbooks.replaceChildren(...doc.playbooks.map((playbook) => {
    const input = el("input", { attrs: { type: "radio", name: "playbook", value: playbook.id } });
    input.checked = playbook.id === state.playbookId;
    input.addEventListener("change", () => {
      state.playbookId = playbook.id;
      renderResult();
      renderChecklist();
      persist();
    });
    const link = el("a", { text: playbook.source.split("/").pop() ?? playbook.id, attrs: { href: REPO + playbook.source, rel: "noopener noreferrer" } });
    return el("label", { className: "card" }, [
      input,
      el("span", { className: "card-body" }, [
        el("span", { className: "card-title" }, [el("strong", { text: playbook.id }), document.createTextNode(` ${playbook.title}`)]),
        el("span", { className: "card-meta", text: m.playbookSeverity(playbook.severity.join(", ")) }),
        el("span", { className: "card-when", text: playbook.when }),
        el("span", { className: "card-link" }, [link]),
      ]),
    ]);
  }));
}

// ─────────────────────────────────────────────────────────────
// 7. Étape 3 : échéances légales
// ─────────────────────────────────────────────────────────────
function renderDues(): void {
  const doc = state.doc;
  if (!doc) return;
  const m = t();
  const now = new Date();
  const local = new Intl.DateTimeFormat(state.lang, { dateStyle: "medium", timeStyle: "short" });
  const awareness = state.awareness ?? now;
  const dues = sortByUrgency(computeDeadlines(doc.obligations.items, awareness, now));
  ui.dues.replaceChildren(...dues.map((due) => {
    const o = due.obligation;
    const timing = due.due && due.remaining !== null
      ? [el("span", { className: "due-left", text: due.remaining < 0 ? m.overdue(formatDuration(due.remaining, state.lang)) : m.remaining(formatDuration(due.remaining, state.lang)) }),
         el("span", { className: "due-at", text: m.dueAt(`${local.format(due.due)} (${utcStamp(due.due)})`) })]
      : [el("span", { className: "due-left", text: m.untimed }), el("span", { className: "due-at", text: o.deadline })];
    return el("li", { className: "due", attrs: { "data-status": state.awareness ? due.status : "untimed" } }, [
      el("span", { className: "due-name", text: o.name }),
      ...(state.awareness || !due.due ? timing : [el("span", { className: "due-at", text: o.deadline })]),
      el("span", { className: "due-who", text: `${m.who} ${o.who} · ${m.recipient} ${o.recipient}` }),
    ]);
  }));
}

function onAwarenessInput(): void {
  const value = ui.awareness.value;
  const parsed = value ? parseLocalDateTime(value) : null;
  ui.awarenessError.textContent = value && !parsed ? t().awarenessInvalid : "";
  state.awareness = parsed;
  renderDues();
  persist();
}

// ─────────────────────────────────────────────────────────────
// 8. Étape 4 : actions à cocher
// ─────────────────────────────────────────────────────────────
function updateProgress(playbook: Playbook): void {
  const { overall, sections } = progress(playbook, state.checked);
  ui.progressText.textContent = t().progress(overall.done, overall.total, percent(overall));
  ui.progressBar.style.width = `${percent(overall)}%`;
  for (const [number, p] of sections) {
    const counter = document.getElementById(`count-${number}`);
    if (counter) counter.textContent = `${p.done} / ${p.total}`;
  }
}

function renderChecklist(): void {
  const playbook = currentPlaybook();
  ui.checklistNone.hidden = playbook !== null;
  ui.checklistBox.hidden = playbook === null;
  if (!playbook) return;
  const m = t();
  ui.sections.replaceChildren(...playbook.sections.filter((s) => s.actions.length > 0).map((section) =>
    el("details", { className: "section", attrs: { open: "" } }, [
      el("summary", {}, [
        el("span", { text: `${section.number}. ${section.title}` }),
        el("span", { className: "count", attrs: { id: `count-${section.number}` } }),
      ]),
      el("ul", { className: "actions-list" }, section.actions.map((action, i) => {
        const key = actionKey(playbook.id, section.number, i);
        const stamp = el("span", { className: "stamp" });
        const showStamp = (): void => {
          const at = state.checked[key];
          stamp.textContent = at ? m.checkedAt(utcStamp(new Date(at))) : "";
        };
        const input = el("input", { attrs: { type: "checkbox" } });
        input.checked = key in state.checked;
        input.addEventListener("change", () => {
          state.checked = toggle(state.checked, key, new Date());
          showStamp();
          updateProgress(playbook);
          persist();
        });
        showStamp();
        return el("li", {}, [el("label", { className: "action" }, [input, el("span", { text: action }), stamp])]);
      })),
    ])));
  updateProgress(playbook);
}

// ─────────────────────────────────────────────────────────────
// 9. Étape 5 : rapport, enregistrement, effacement
// ─────────────────────────────────────────────────────────────
function report(): string {
  const doc = state.doc as ExportDoc;
  const assessment = assess(doc.severity.criteria, state.answers);
  const playbook = currentPlaybook();
  const adjusted = adjustForPlaybook(assessment.level, playbook?.severity ?? []);
  const raisedNote = adjusted.raised && playbook && adjusted.level
    ? t().raised(adjusted.level, playbook.id, playbook.severity.join(", ")) : null;
  return buildReport({
    doc, playbook, level: adjusted.level, raisedNote, answers: state.answers, awareness: state.awareness,
    checked: state.checked, reference: ui.reference.value, now: new Date(),
  }, t());
}

async function copyReport(): Promise<void> {
  try {
    await navigator.clipboard.writeText(report());
    ui.reportStatus.textContent = t().copied;
  } catch {
    ui.reportStatus.textContent = t().copyFailed;
  }
}

function downloadReport(): void {
  const name = `${sanitizeReference(ui.reference.value) || "incident"}-${new Date().toISOString().slice(0, 10)}.md`;
  const url = URL.createObjectURL(new Blob([report()], { type: "text/markdown;charset=utf-8" }));
  const link = el("a", { attrs: { href: url, download: name } });
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function clearAll(): void {
  storage.clear();
  state.answers = [];
  state.playbookId = null;
  state.awareness = null;
  state.checked = {};
  state.saveEnabled = false;
  ui.save.checked = false;
  ui.reference.value = "";
  ui.awareness.value = "";
  renderData();
  ui.reportStatus.textContent = t().cleared;
}

// ─────────────────────────────────────────────────────────────
// 10. Assemblage et événements
// ─────────────────────────────────────────────────────────────
function renderData(): void {
  const doc = state.doc;
  if (!doc) return;
  renderStatic();
  renderCriteria(doc);
  renderResult();
  renderPlaybooks(doc);
  renderDues();
  renderChecklist();
}

async function switchLang(lang: Lang): Promise<void> {
  state.lang = lang;
  renderStatic();
  ui.status.textContent = t().loading;
  try {
    state.doc = await loadDoc(lang);
    ui.status.textContent = "";
    ui.app.hidden = false;
    renderData();
    persist();
  } catch (error) {
    ui.app.hidden = true;
    ui.status.textContent = t().loadError(error instanceof Error ? error.message : String(error));
  }
}

for (const lang of LANGS) byId(`lang-${lang}`).addEventListener("click", () => void switchLang(lang));
ui.awareness.addEventListener("input", onAwarenessInput);
ui.awarenessNow.addEventListener("click", () => {
  ui.awareness.value = toLocalInput(new Date());
  onAwarenessInput();
});
ui.reference.addEventListener("input", () => {
  const clean = sanitizeReference(ui.reference.value);
  if (clean !== ui.reference.value) ui.reference.value = clean;
  persist();
});
ui.copy.addEventListener("click", () => void copyReport());
ui.download.addEventListener("click", downloadReport);
ui.save.checked = state.saveEnabled;
ui.save.addEventListener("change", () => {
  if (ui.save.checked && !storage.storageAvailable()) {
    ui.save.checked = false;
    ui.reportStatus.textContent = t().saveUnavailable;
    return;
  }
  state.saveEnabled = ui.save.checked;
  if (state.saveEnabled) persist();
  else storage.clear();
});
ui.clear.addEventListener("click", clearAll);
if (state.awareness) ui.awareness.value = toLocalInput(state.awareness);

// Les comptes à rebours avancent toutes les 30 secondes
setInterval(renderDues, 30_000);
void switchLang(state.lang);
