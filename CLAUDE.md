# CLAUDE.md — legal (scorparc/legal)

## Projekt
Zentrale Rechtstexte (Impressum & Datenschutzerklärungen) für alle Apps von Marc Neumann: ScootRules, PlakettenAlarm, ScootKeeper, FamilyBash. **Die Rechtstexte liegen immer auf GitHub (`scorparc/legal`)** — das ist die führende Quelle. Apps laden die JSON von dort periodisch (max. 1×/24h) und cachen offline; gebündelter Fallback liegt in jeder App unter `assets/legal/`.

## Setup
- Statische Dateien (HTML/JSON/CSS), kein Build-System. Bearbeiten + committen genügt.
- Gehostet auf GitHub (`scorparc/legal`); Apps beziehen die JSON von dort.

## Hosting / URLs (aus App-Code belegt)
- **JSON** (Apps laden + cachen offline) über **raw.githubusercontent.com**:
  `https://raw.githubusercontent.com/scorparc/legal/main/impressum.json`,
  `…/main/<app>/datenschutz.json` (Sprachsuffix z. B. `datenschutz_en.json`),
  `…/main/apps.json`
- **HTML** (Button „im Browser öffnen") über **GitHub Pages**:
  `https://scorparc.github.io/legal/impressum.html`,
  `https://scorparc.github.io/legal/<app>/datenschutz.html`

## Befehle
- Lokale Vorschau: beliebiger statischer Server, z. B. `python -m http.server` im Repo-Root, dann `index.html` öffnen.
- Deploy: **Push nach GitHub (`main`)** — kein separater Build/Upload nötig.
  - JSON (raw) ist damit sofort live; Apps ziehen sie beim nächsten Sync (max. 1×/24h).
  - HTML-Seiten erfordern **aktiviertes GitHub Pages** im Repo `scorparc/legal` — sonst laufen die HTML-Buttons ins Leere.

## Struktur
- `impressum.html` / `impressum.json` — identisch für alle Apps
- `<app>/datenschutz.html` / `<app>/datenschutz.json` — je App (`familybash/`, `plakettenalarm/`, `scootkeeper/`, `scootrules/`)
- `apps.json`, `index.html`, `style.css`, `impressum.json`

## Konventionen
- HTML und JSON müssen inhaltlich synchron bleiben (App liest JSON, Web zeigt HTML).
- Nummerierte Abschnitte + gemeinsames `style.css`; Struktur über alle Apps gleich halten.

## Kontext
- Git-Repo, öffentlich gehostet. Änderungen wirken auf ALLE Apps → sorgfältig.
- Nach Textänderung ggf. gebündelten Fallback in den App-Repos (`assets/legal/`) nachziehen.
