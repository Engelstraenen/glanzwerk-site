# PROJEKT-MASTERFILE – GLANZWERK
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Musterwebseite (Demo) für Reinigungsfirmen / Gebäudereinigung, erfundene Firma GLANZWERK. Modern, cool, praxisnah, löst Branchenprobleme. Gleiche Liga wie WARMHERZ, FARBKANTE, LICHTBOGEN.

## 2. Qualitätsanspruch & Referenzen
Aufbau wie FLUTLICHT27/FARBKANTE: Film-Kapitel (Scroll spult Vorher → Arbeit → Ergebnis) im Wechsel mit Motion-Design-Kapiteln. Leitmotiv eindeutig Profi-Reinigung (Industriekletterer + Abzieher, Hochdruck-Flächenreiniger, Einscheibenmaschine).
Branchenprobleme, die die Seite löst: Personal finden (Recruiting-Kapitel, Bewerbung in 60 s), Anfragen ohne Telefon-Pingpong (Fläche + Intervall + Fotos → Begehungstermin), Vertrauen (versichert, feste Teams, Schlüsselmanagement), Qualitätsnachweis (digitales Reinigungsprotokoll), Bewertungen (nur markierte Beispiele).

## 3. Regeln
Medien nur Unlimited (0 Credits). Ab 24.11.2026 (Eugen): Bilder NUR Dreamina GPT Image 2.5 Sunburst (2K, Medium, Unlimited; Alternativen Flare, Seedream 5.5), Videos Dreamina Seedance 2.5 720P Unlimited. Dreamina Unlimited = kontoweit 1 Auftrag gleichzeitig. Videos: Draft gratis, Endrender MiniMax H3 2K nur nach OK + Preis. Mobil-Check 4 Größen + Kopfzeile 1081–1600 px.

## 4. Skills/Plugins
Keine extra (bei Motion-Kapiteln ggf. hyperframes nach OK).

## 5. Zugänge
sjinn.ai (Chrome eingeloggt) ✅ · GitHub Engelstraenen (gh) – vor Push prüfen

## 6. Workflow & Freigabepunkte
1. 3 Storyboards (GSB-1 Klarsicht, GSB-2 Die Bahn, GSB-3 Nachtschicht) → Eugen wählt
2. First Frames 4K → Video-Drafts → Freigabe
3. Seite bauen, prüfen, GitHub Pages

## 7. Befehle
- Vorschau: `python3 tools/serve.py 4412` → http://127.0.0.1:4412/ (Port 4412 gehört GLANZWERK)
- Bilder: Rohbilder `assets-roh/GW-xx.jpg` → `python3 tools/assets.py` (WebP 3840/1800 + img.js)
- Prüfen: `python3 tools/desktop_check.py`, `python3 tools/mobil_check.py`
- GitHub: Engelstraenen/glanzwerk-site, Pages über Branch gh-pages (`git subtree split --prefix site`)

## 8. Offene Fragen
–

## 9. Entschieden
- 23.11.2026: Projektname GLANZWERK (Arbeitstitel), 3 Konzepte als Storyboards.
- 23.11.2026 (Eugen): Look + Storytelling = 3 Nachtschicht (Graphit + Mint, leeres Büro nachts → morgens wie neu). Dazu Klarsicht (Glas/Fassade, Industriekletterer) und Die Bahn (Hochdruck, tausende m² Außenfläche) als Leistungen einbauen. Zwei Mix-Storyboards: MIX-A „Eine Nacht, ein Gebäude“, MIX-B „Die Einsatzzentrale“.
- 23.11.2026 (Eugen): MIX-A gewählt = verbindliches Storyboard (konzepte/mix-a-eine-nacht.jpg).

- 24.11.2026 (Eugen): Bilder nur Dreamina Sunburst/Flare/Seedream 5.5 (Unlimited), Webseitenbilder damit 2560×1440 statt 4K.

## 10. Ablage
konzepte/ Storyboards + prompts.md · tools/sjinn_queue.js · site/ (folgt)
