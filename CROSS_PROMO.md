# Cross-Promotion-Standard (Schema 2)

Gilt für alle Vardholt-Apps. Daten: `apps.json` in diesem Repo.
Remote: `https://raw.githubusercontent.com/scorparc/legal/main/apps.json`

## Datenmodell `apps.json`

| Feld | Bedeutung |
|---|---|
| `id`, `packageName`, `name` | Kennung, Play-Package, Anzeigename |
| `names` | optional, Anzeigename je Sprachcode (z. B. ZahnTagebuch → `en: Tooth Diary`); fehlt die Sprache → `name` |
| `tagline` | deutscher Kurztext (String, bleibt für ältere App-Versionen ein String) |
| `taglines` | Kurztext je Sprachcode: `en`, `es`, `fr`, `it`, `pt` |
| `storeUrl` | `https://play.google.com/store/apps/details?id=<package>` |
| `active` | nur `true`, wenn die App live im Store ist |
| `showIn` | Packages der Apps, in denen dieser Eintrag empfohlen wird |

Reihenfolge der Liste = Anzeigereihenfolge. Unbekannte Felder werden ignoriert.

## Anzeigeregel (in jeder App identisch)

Ein Eintrag erscheint in der App `X`, wenn **alle** gelten:

1. `active == true`
2. `X` steht in `showIn`
3. Eintrag ist nicht `X` selbst
4. `storeUrl` ist `https://` auf Host `play.google.com`

Kein `showIn` → nie anzeigen. Tagline in der Anzeigesprache (Sprachcode, `pt` auch für pt-BR/pt-PT), **ohne** Rückfall auf Deutsch: fehlt sie, keine Unterzeile.

## UI

- Abschnitt **„Weitere Apps“** in Einstellungen oder Menü. Nie neben Werbeflächen oder im Arbeitsablauf der App. (Google wertet einen More-Apps-Bereich im Menü nicht als Werbung, eingebettete Banner schon.)
- Je Empfehlung eine anklickbare Zeile: Name, Tagline, Open-in-new-Icon → `storeUrl`.
- Darunter immer **„Alle Apps von Vardholt“** → `https://play.google.com/store/apps/developer?id=Vardholt` (Konstante in der App).
- Öffnen extern; fehlt ein Handler, still ignorieren.
- Keine Analytics, keine UTM, keine Pop-ups, keine neuen Bibliotheken.
- FamilyBash (Families Policy) bekommt **keinen** Abschnitt.

| Sprache | Abschnitt | Entwicklerlink |
|---|---|---|
| de | Weitere Apps | Alle Apps von Vardholt |
| en | More apps | All apps by Vardholt |
| es | Más aplicaciones | Todas las apps de Vardholt |
| fr | Autres applications | Toutes les apps de Vardholt |
| it | Altre app | Tutte le app di Vardholt |
| pt (PT) | Mais aplicações | Todas as apps da Vardholt |
| pt (BR) | Mais aplicativos | Todos os apps da Vardholt |

## Laden

Wie die Rechtstexte: gebündelte Kopie dieser `apps.json` als Offline-Fallback, Remote-Sync (24 h), defektes Remote-JSON fällt auf Cache bzw. Asset zurück. Bei jedem Release die gebündelte Kopie aktualisieren.

## Pflicht-Tests (in jeder App)

1. Filter + Reihenfolge (aktiv, showIn, nicht selbst, Play-URL)
2. Ohne `showIn` → leer
3. Tagline je Sprache, kein deutscher Fallback; `names` je Sprache mit Fallback auf `name`
4. Entwicklerlink ist Play-URL mit `developer?id=Vardholt`
5. Gebündelte `apps.json` valide: jede `storeUrl` Play, keine App in ihrem eigenen `showIn`, Taglines für de/en/es/fr/it/pt

## Referenz-Implementierung (Flutter)

Identisch in BonSafe, ScootRules, PlakettenAlarm:
`promo_app.dart` (Modell, Parser, Filter, Konstante), Abschnitt in den Einstellungen, `promo_app_test.dart`.
Pfade: `BonSafe/lib/core/promo/promo_app.dart`, `BonSafe/lib/features/settings/more_apps_section.dart`, `BonSafe/test/promo_app_test.dart`.

## Ablauf bei neuen Apps / Änderungen

1. Eintrag in `apps.json` mit `active: false` und `showIn` anlegen bzw. pflegen (nur zentral, nicht parallel aus mehreren App-Chats).
2. App auf den Standard heben, Release.
3. Nach Freigabe durch Google: `active: true` setzen, commit, push. Wirkt ohne App-Update nach dem nächsten Sync.

App-Versionen vor Schema 2 ignorieren `showIn` und zeigen alle aktiven Einträge. Deshalb zuerst umstellen, dann aktivieren.

## Matrix (Stand 03.10.2026)

| App | zeigt |
|---|---|
| ScootRules | PlakettenAlarm, ScootKeeper |
| PlakettenAlarm | ScootRules, ScootKeeper |
| ScootKeeper | ScootRules, PlakettenAlarm |
| BabyLog | SleepLog, ZahnTagebuch, FamilyBash |
| SleepLog | BabyLog, ZahnTagebuch |
| ZahnTagebuch | BabyLog, SleepLog, FamilyBash |
| BonSafe | PaperSnap |
| PaperSnap | BonSafe, ConcreteCalc |
| ConcreteCalc | PaperSnap, BonSafe |
| FamilyBash | – (kein Abschnitt) |
