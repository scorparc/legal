# scorparc/legal

Zentrale Rechtstexte (Impressum & Datenschutzerklärungen) für alle Apps von
Marc Neumann: ScootRules, PlakettenAlarm, ScootKeeper.

Dieses Repo ist die **führende Quelle**. Die Apps laden die JSON-Dateien
periodisch (empfohlen: max. 1x/24h) und cachen sie lokal für den Offline-Betrieb.
Ein gebündelter Fallback (`assets/legal/*.json` in der jeweiligen App) sorgt
dafür, dass das Impressum auch ganz ohne Internetverbindung sofort verfügbar ist.

## Struktur

- `impressum.html` / `impressum.json` – identisch für alle drei Apps
- `<app>/datenschutz.html` / `<app>/datenschutz.json` – app-spezifisch, gleiche
  Formatierung/Struktur (nummerierte Abschnitte, `style.css`)
- `style.css` – gemeinsames Stylesheet (Akzentfarbe `#0B7A55`, Dark-Mode-Support)

## URLs (GitHub Pages)

- Impressum: `https://scorparc.github.io/legal/impressum.html`
- Datenschutz ScootRules: `https://scorparc.github.io/legal/scootrules/datenschutz.html`
- Datenschutz PlakettenAlarm: `https://scorparc.github.io/legal/plakettenalarm/datenschutz.html`
- Datenschutz ScootKeeper: `https://scorparc.github.io/legal/scootkeeper/datenschutz.html`

## Raw-JSON für In-App-Fetch

Basis: `https://raw.githubusercontent.com/scorparc/legal/main/`

- `impressum.json`
- `scootrules/datenschutz.json`
- `plakettenalarm/datenschutz.json`
- `scootkeeper/datenschutz.json`

## Änderungen vornehmen

1. HTML **und** JSON der betroffenen Datei parallel pflegen (gleicher Inhalt,
   zwei Formate – JSON fürs native In-App-Rendering, HTML für den öffentlichen
   Play-Store-Link).
2. `stand`/`updated`-Feld aktualisieren.
3. Committen & pushen – GitHub Pages baut automatisch neu (ca. 1 Minute).
4. Apps holen die neue Version beim nächsten planmäßigen Sync automatisch ab
   (kein App-Update nötig).

## Cross-Promotion (`apps.json`)

Zentrale Liste aller eigenen Apps für gegenseitige Verlinkung. Jede App lädt
`apps.json` (gleicher Sync-/Cache-Mechanismus wie die Rechtstexte) und zeigt in
einem „Weitere Apps"-Bereich alle Einträge an, die

1. `active: true` sind **und**
2. einen **anderen** `packageName` als die eigene App haben (Selbst-Filter).

**Neue App live schalten:** Sobald eine App im Play Store veröffentlicht ist,
hier `"active": true` setzen und committen. Die jeweils anderen Apps blenden sie
beim nächsten planmäßigen Sync automatisch ein – **kein App-Update nötig**.

Raw-URL für In-App-Fetch:
`https://raw.githubusercontent.com/scorparc/legal/main/apps.json`

## Play Console

Bei jeder App unter „App-Inhalte → Datenschutzerklärung" die jeweilige
`datenschutz.html`-URL von oben eintragen.
