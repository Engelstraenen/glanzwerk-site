#!/usr/bin/env python3
"""Rohbilder (assets-roh/GW-xx.png|jpg) -> site/assets/img/<name>.webp (3840) + <name>-m.webp (1800) + img.js.
Merkt sich Quelle+mtime (Cache), damit Dropbox unveränderte Quellen nicht neu lädt."""
import json, os, sys, time
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, OUT = os.path.join(ROOT, 'assets-roh'), os.path.join(ROOT, 'site/assets/img')
MAP = {'GW-01': 'nacht-buero', 'GW-02': 'hof-vorher', 'GW-03': 'fassade', 'GW-04': 'morgen', 'GW-05': 'karriere',
       'GW-06': 'buero-sauber', 'GW-07': 'hof-sauber', 'GW-08': 'l-innen', 'GW-09': 'l-glas', 'GW-10': 'l-aussen'}
SIZES = {'': 3840, '-m': 1800}
os.makedirs(OUT, exist_ok=True)
cache_f = os.path.join(ROOT, 'tools/.assets_cache.json')
cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
man = {}
for gid, name in MAP.items():
    src = next((os.path.join(RAW, gid + e) for e in ('.png', '.jpg') if os.path.exists(os.path.join(RAW, gid + e))), None)
    if not src:
        continue
    key = f'{os.path.getmtime(src)}'
    if cache.get(name, {}).get('key') == key and all(os.path.exists(os.path.join(OUT, name + s + '.webp')) for s in SIZES):
        man[name] = cache[name]['dim']; continue
    im = Image.open(src).convert('RGB')
    for suf, w in SIZES.items():
        w2 = min(w, im.width); h2 = round(im.height * w2 / im.width)
        im.resize((w2, h2), Image.LANCZOS).save(os.path.join(OUT, name + suf + '.webp'), 'WEBP', quality=84, method=5)
    man[name] = {'w': im.width, 'h': im.height}
    cache[name] = {'key': key, 'dim': man[name]}
    print('neu', name, im.size)
json.dump(cache, open(cache_f, 'w'))
man['_v'] = int(time.time()) % 100000
open(os.path.join(ROOT, 'site/assets/js/img.js'), 'w').write('window.GW_IMG = ' + json.dumps(man) + ';\n')
print('img.js:', sorted(k for k in man if k != '_v'))
