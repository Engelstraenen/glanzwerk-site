#!/usr/bin/env python3
"""Service-Point-Logo als reine Vektoren in der Seiten-CI (Graphit + Mint).
Skyline: Kontur aus dem Original-Logo (assets-roh/service-point/image00111.jpg) per OpenCV,
Schrift: Inter Tight als Pfade (fontTools). Ausgabe: site/assets/img/logo-sp*.svg"""
import os, sys, cv2, numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTDIR = sys.argv[1]
src = cv2.imread(os.path.join(ROOT, 'assets-roh/service-point/image00111.jpg'))
h0, w0 = src.shape[:2]
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
mask = (gray < 215).astype(np.uint8) * 255                    # alles, was nicht Weiß ist
sky = mask[:218, :]                               # nur Skyline (oberer Teil)
sky = cv2.morphologyEx(sky, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8))
cs, hier = cv2.findContours(sky, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
print('Konturen', len(cs))
ys, xs = np.where(sky > 0)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
S = 1000 / (x1 - x0)                                          # Skyline auf 1000 Einheiten Breite
def pts(c):
    c = cv2.approxPolyDP(c, 0.8, True)
    return ' '.join(f'{(p[0][0]-x0)*S:.1f},{(p[0][1]-y0)*S:.1f}' for p in c)
sky_d = ''.join(f'M{pts(c)}Z' for c in cs if cv2.contourArea(c) > 4 or len(c) > 20)
SKY_H = (y1 - y0) * S

def text_path(txt, font, size, x, y, track=0):
    f = TTFont(font); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    sc = size / upm; out = []; cx = x
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is None: continue
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        out.append(pen.getCommands()); cx += gs[g].width * sc + track
    return ''.join(out), cx - track - x

def build(mint, txt, bar_txt, bar_bg, name):
    t1, w1 = text_path('SERVICE.POINT', f'{FONTDIR}/IT800.ttf', 150, 0, 0, 6)
    t2, w2 = text_path('DIENSTLEISTUNGEN GMBH', f'{FONTDIR}/IT500.ttf', 54, 0, 0, 8)
    W = max(1000, w1)
    # Zeilen setzen
    sk_x = (W - 1000) / 2
    y_t1 = SKY_H + 160
    t1, _ = text_path('SERVICE.POINT', f'{FONTDIR}/IT800.ttf', 150, (W - w1) / 2, y_t1, 6)
    bar_y = y_t1 + 40; bar_h = 84
    t2, _ = text_path('DIENSTLEISTUNGEN GMBH', f'{FONTDIR}/IT500.ttf', 54, (W - w2) / 2, bar_y + 61, 8)
    H = bar_y + bar_h
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 {W+20:.0f} {H+20:.0f}" role="img" aria-label="Service Point Dienstleistungen GmbH">
<path fill="{mint}" transform="translate({sk_x:.1f},0)" fill-rule="evenodd" d="{sky_d}"/>
<path fill="{txt}" d="{t1}"/>
<rect x="0" y="{bar_y:.1f}" width="{W:.1f}" height="{bar_h}" rx="10" fill="{bar_bg}"/>
<path fill="{bar_txt}" d="{t2}"/>
</svg>'''
    open(os.path.join(ROOT, 'site/assets/img', name), 'w').write(svg)
    print(name, len(svg), 'Bytes')

build('#5eeab0', '#eef3f2', '#062018', '#5eeab0', 'logo-sp.svg')        # dunkler Grund
build('#2fc98d', '#0c1012', '#eef3f2', '#0c1012', 'logo-sp-hell.svg')   # heller Grund
# Kompakt-Marke (nur Skyline) für Kopfzeile/Favicon
mark = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 1020 {SKY_H+20:.0f}"><path fill="#5eeab0" fill-rule="evenodd" d="{sky_d}"/></svg>'
open(os.path.join(ROOT, 'site/assets/img/logo-sp-mark.svg'), 'w').write(mark)
print('mark ok, Skyline-Höhe', round(SKY_H))
