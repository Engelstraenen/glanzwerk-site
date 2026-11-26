#!/usr/bin/env python3
"""Inter Tight lokal statt Google Fonts (schneller, DSGVO: keine Verbindung zu Google).
Lädt die woff2 (nur latin + latin-ext) nach site/assets/fonts/, schreibt site/assets/css/fonts.css
und ersetzt den Google-Link in site/*.html und tools/subpages.py.
Start: python3 tools/fonts_local.py   (Vorlage DRSCHIWAGO)
"""
import glob, os, re, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(HERE, 'site', 'assets', 'fonts')
URL = 'https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800&display=swap'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
KEEP = {'latin', 'latin-ext'}
os.makedirs(FONTS, exist_ok=True)
css = urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': UA})).read().decode()
out, files = [], {}
for subset, block in re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, re.S):
    if subset not in KEEP:
        continue
    url = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    if url not in files:  # variable Schrift: alle Stärken teilen sich eine Datei je Subset
        files[url] = f'inter-tight-{subset}.woff2'
        urllib.request.urlretrieve(url, os.path.join(FONTS, files[url]))
    out.append(f'/* {subset} */\n' + block.replace(url, '../fonts/' + files[url]))
open(os.path.join(HERE, 'site', 'assets', 'css', 'fonts.css'), 'w').write(
    '/* Schriften lokal (vorher Google Fonts), erzeugt mit tools/fonts_local.py */\n' + '\n'.join(out) + '\n')
print(len(out), 'Schnitte,', len(files), 'Dateien:', sorted(files.values()))

OLD = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
                 r'<link href="https://fonts\.googleapis\.com/[^"]+" rel="stylesheet">')
NEW = ('<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-tight-latin.woff2" crossorigin>\n'
       '<link rel="stylesheet" href="assets/css/fonts.css">')
for p in glob.glob(os.path.join(HERE, 'site', '*.html')) + [os.path.join(HERE, 'tools', 'subpages.py')]:
    s = open(p).read()
    s2, n = OLD.subn(NEW, s, count=1)
    if n:
        open(p, 'w').write(s2)
    print(os.path.basename(p), 'ersetzt' if n else 'nicht gefunden')
