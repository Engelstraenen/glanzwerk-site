#!/usr/bin/env python3
"""Erzeugt die Leistungs-Unterseiten site/leistung-*.html aus einer Vorlage."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · GLANZWERK</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0c1012">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=2">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230c1012'/%3E%3Cpath d='M9 22 L16 8 L23 22' fill='none' stroke='%235eeab0' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
</head>
<body class="sub">
<header class="sub-nav">
  <div class="wrap">
    <a class="sub-back" href="index.html#leistungen">Alle Leistungen</a>
    <a class="btn btn-mint" href="index.html#angebot">Angebot in 60 Sek.</a>
  </div>
</header>
<main>
'''

FOOT = '''
<section class="sub-sec sub-cta">
  <div class="wrap">
    <p class="kicker">Nächster Schritt</p>
    <h2 class="h-sec">Begehung in 48 Stunden.<br><span class="mint">Ohne Telefon-Pingpong.</span></h2>
    <div class="row"><a class="btn btn-mint" href="index.html#angebot">Fläche eingeben</a><a class="btn btn-ghost" href="index.html#leistungen">Alle Leistungen</a></div>
    <div class="sub-next">{nexts}</div>
  </div>
</section>
</main>
<footer class="foot">
  <p class="wrap foot-demo">Musterseite für Gebäudereinigungen. GLANZWERK ist ein erfundener Betrieb, alle Werte sind Beispiele, Branchenzahlen mit Quelle.</p>
</footer>
<script src="assets/js/img.js?v=2"></script>
<script src="assets/js/sub.js?v=1"></script>
</body>
</html>
'''

PAGES = {
    'innen': dict(
        title='Unterhaltsreinigung', desc='Büroreinigung über Nacht: Ablauf, Bodenpflege, Rhythmus und Richtwerte. GLANZWERK Musterseite.',
        hero='buero-sauber', kicker='Leistung 1 · Innen', h1='Morgens wie neu. <span class="mint">Jeden Morgen.</span>',
        lead='Büros, Praxen und Kanzleien. Wir kommen, wenn alle gehen, und sind weg, bevor der erste Kaffee läuft.',
        steps=[('Schlüssel', 'Aus dem Tresor, Zutritt wird mit Uhrzeit protokolliert.'),
               ('Tische & Müll', 'Arbeitsflächen frei wischen, Behälter leeren, Wertstoffe trennen.'),
               ('Sanitär & Küche', 'Eigene Tücher je Bereich, farbcodiert, nie gemischt.'),
               ('Boden', 'Einscheibenmaschine, bis der Stein wieder spiegelt.')],
        ba=('nacht-buero', 'buero-sauber'),
        extra='''<section class="sub-sec"><div class="wrap">
  <p class="kicker">Rhythmus</p><h2 class="h-sec">Täglich ist pro m² <span class="mint">am effizientesten.</span></h2>
  <figure class="fact rv" style="max-width:760px">
    <div class="bars">
      <div class="bar"><span>täglich</span><div class="tr"><div class="fl" style="--w:100%">150 m²/h</div></div></div>
      <div class="bar b2"><span>jeden 2. Tag</span><div class="tr"><div class="fl" style="--w:73%">110 m²/h</div></div></div>
    </div>
    <p>Wer seltener reinigt, zahlt mehr Zeit pro Quadratmeter, weil sich Schmutz festsetzt.</p>
    <small>Richtwert Büroreinigung aus Zeitstudien (u. a. FIGR, RAL): <a href="https://shop.forum-verlag.com/media/pdf/LP_1805_objektarten.pdf" target="_blank" rel="noopener">Forum Verlag</a></small>
  </figure></div></section>''',
        faq=[('Wer hat unseren Schlüssel?', 'Er liegt bei uns im Tresor. Jede Entnahme wird mit Name und Uhrzeit protokolliert, Sie sehen es im Morgenbericht.'),
             ('Kommt immer dasselbe Team?', 'Ja. Feste Touren, feste Crew. Urlaubsvertretung kennt Ihr Objekt aus der Einarbeitung.'),
             ('Was passiert, wenn etwas kaputt ist?', 'Foto um 6 Uhr im Bericht, Hinweis an Ihre Haustechnik. Wir sind versichert.'),
             ('Können wir Betriebsferien pausieren?', 'Ja. Im Konfigurator einfach die Wochen abziehen, die Nächte pro Jahr passen sich an.')],
        nexts=['glas', 'aussen']),
    'glas': dict(
        title='Glas & Fassade', desc='Glas- und Fassadenreinigung mit Seilzugang bis zum 18. Stock. GLANZWERK Musterseite.',
        hero='fassade', kicker='Leistung 2 · Glas & Fassade', h1='Klar. <span class="mint">Bis zum 18. Stock.</span>',
        lead='Fenster, Glasfassaden, Lichtkuppeln. Mit Seilzugang, Hebebühne oder Reinwasser-Teleskop, je nach Gebäude.',
        steps=[('Sichern', 'Zwei Seile, geprüfte Anschlagpunkte, Absperrung unten nur nachts.'),
               ('Einwaschen', 'Einwascher mit mildem Reiniger, Staub und Regenränder lösen.'),
               ('Abziehen', 'Edelstahl-Abzieher in langen Bahnen, Kante für Kante.'),
               ('Prüfen', 'Fotos vom Seil im Morgenbericht, Rahmen und Dichtungen gleich mit.')],
        ba=None,
        extra='''<section class="sub-sec"><div class="wrap">
  <p class="kicker">Seil statt Gerüst</p><h2 class="h-sec">Kein Gerüst. <span class="mint">Keine Straßensperre.</span></h2>
  <div class="facts-grid">
    <figure class="fact rv"><h3>Seilzugang</h3><p>Aufbau in Minuten, nachts oder am frühen Morgen, kein Gerüst vor den Fenstern Ihrer Mieter.</p></figure>
    <figure class="fact rv"><h3>Hebebühne</h3><p>Für Hallen, Vordächer und niedrige Fassaden. Wir bringen sie mit, auch für Lichtkuppeln.</p></figure>
    <figure class="fact rv"><h3>Reinwasser-Teleskop</h3><p>Bis ca. 4 Etagen vom Boden aus, ohne Reinigungsmittel, trocknet ohne Streifen.</p></figure>
  </div>
  <div class="ba" data-need="l-glas" style="aspect-ratio:3/4;max-width:520px;margin-top:28px"><img data-img="l-glas" alt="Abzieher zieht eine klare Bahn über das staubige Glas"></div>
</div></section>''',
        faq=[('Wie oft sollte Glas gereinigt werden?', 'Büro-Fenster meist 2 bis 4 Mal im Jahr, Eingangsbereiche öfter. Wir schlagen bei der Begehung einen Plan vor.'),
             ('Ist das bei Wind sicher?', 'Bei starkem Wind oder Frost wird nicht gearbeitet. Der Termin rutscht, Sie bekommen Bescheid.'),
             ('Sehen uns die Monteure ins Büro?', 'Wir arbeiten außerhalb Ihrer Bürozeiten, auf Wunsch abends oder ab 5 Uhr morgens.'),
             ('Reinigen Sie auch Sonnenschutz?', 'Ja, Lamellen, Markisen und Rahmen auf Wunsch im selben Einsatz.')],
        nexts=['innen', 'aussen']),
    'aussen': dict(
        title='Außenflächen', desc='Hochdruckreinigung von Höfen, Parkdecks und Eingängen über Nacht. GLANZWERK Musterseite.',
        hero='hof-sauber', kicker='Leistung 3 · Außen', h1='Tausende m². <span class="mint">Eine Nacht.</span>',
        lead='Höfe, Parkdecks, Eingänge und Wege. Moos, Algen, Kaugummi und Öl raus, Bahn für Bahn, unter Flutlicht.',
        steps=[('Ausleuchten', 'Mobile LED-Masten, damit keine Ecke im Schatten liegt.'),
               ('Flächenreiniger', 'Rotierende Düsen unter der Haube, kein Spritzwasser an Fassade und Autos.'),
               ('Fugen', 'Moos aus den Fugen, auf Wunsch neu verfüllen.'),
               ('Abnahme', 'Vorher/Nachher-Foto aus derselben Position im Morgenbericht.')],
        ba=('hof-vorher', 'hof-sauber'),
        extra='''<section class="sub-sec"><div class="wrap">
  <p class="kicker">Was rausgeht</p><h2 class="h-sec">Vier Gegner. <span class="mint">Vier Verfahren.</span></h2>
  <div class="facts-grid">
    <figure class="fact rv"><h3>Moos & Algen</h3><p>Heißwasser-Hochdruck, danach Fugen ausbürsten. Kommt so langsamer zurück.</p></figure>
    <figure class="fact rv"><h3>Kaugummi</h3><p>Dampf und Spezialdüse, Stück für Stück, ohne den Stein anzugreifen.</p></figure>
    <figure class="fact rv"><h3>Öl & Reifenspuren</h3><p>Vorbehandlung mit Öllöser, Abwasser wird aufgefangen, nicht in den Gully.</p></figure>
  </div>
</div></section>''',
        faq=[('Wird es laut?', 'Flächenreiniger sind leiser als offene Lanzen. In Wohnnähe planen wir die lauten Teile vor 22 Uhr oder ab 6 Uhr.'),
             ('Wohin geht das Schmutzwasser?', 'Bei Öl wird es aufgefangen und entsorgt, sonst nach den Vorgaben Ihrer Gemeinde.'),
             ('Müssen Autos weg?', 'Nur von der Fläche, die in der Nacht dran ist. Wir planen Abschnitte, damit nicht alles gleichzeitig frei sein muss.'),
             ('Wie lange hält das?', 'Je nach Lage und Schatten ein bis zwei Jahre. Mit Fugenversiegelung deutlich länger.')],
        nexts=['innen', 'glas']),
}
NAMES = {'innen': ('Unterhaltsreinigung', 'l-innen'), 'glas': ('Glas & Fassade', 'l-glas'), 'aussen': ('Außenflächen', 'l-aussen')}

for key, P in PAGES.items():
    steps = ''.join(f'<li class="rv"><h3>{t}</h3><p>{d}</p></li>' for t, d in P['steps'])
    ba = ''
    if P['ba']:
        a, b = P['ba']
        ba = f'''<section class="sub-sec"><div class="wrap">
  <p class="kicker">Vorher / Nachher</p><h2 class="h-sec">Selbst <span class="mint">schieben.</span></h2>
  <div class="ba" data-need="{a}">
    <img class="ba-a" data-img="{a}" alt="Vorher"><div class="ba-b"><img data-img="{b}" alt="Nachher"></div>
    <span class="ba-line"></span><span class="ba-knob">⇆</span><span class="ba-tag l">vorher</span><span class="ba-tag r">nachher</span>
    <input type="range" min="0" max="100" value="50" aria-label="Vorher-Nachher-Regler">
  </div></div></section>'''
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in P['faq'])
    nexts = ''.join(f'<a href="leistung-{n}.html"><img data-img="{NAMES[n][1]}" alt="{NAMES[n][0]}"><span>{NAMES[n][0]} →</span></a>' for n in P['nexts'])
    html = HEAD.format(title=P['title'], desc=P['desc']) + f'''
<section class="sub-hero">
  <img data-img="{P['hero']}" alt="{P['title']}">
  <div class="wrap">
    <p class="kicker">{P['kicker']}</p>
    <h1>{P['h1']}</h1>
    <p class="lead">{P['lead']}</p>
  </div>
</section>
<section class="sub-sec"><div class="wrap">
  <p class="kicker">Ablauf</p><h2 class="h-sec">So läuft <span class="mint">die Nacht.</span></h2>
  <ol class="steps4">{steps}</ol>
</div></section>
{ba}
{P['extra']}
<section class="sub-sec"><div class="wrap">
  <p class="kicker">Häufige Fragen</p><h2 class="h-sec">Kurz <span class="mint">beantwortet.</span></h2>
  <div class="faq">{faq}</div>
</div></section>
''' + FOOT.format(nexts=nexts)
    open(os.path.join(ROOT, 'site', f'leistung-{key}.html'), 'w').write(html)
    print('ok', key)
