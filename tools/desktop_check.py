#!/usr/bin/env python3
"""Desktop-Prüfung: Kopfzeile 1081-1600 px (rechte Kante <= Fensterbreite), Querscroll, Konsolenfehler, Screens je Kapitel in 1440x900."""
import sys, os
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4412/"
OUT = "/private/tmp/claude-501/gw-check/desk/"; os.makedirs(OUT, exist_ok=True)
CH = ["nacht", "leistungen", "live", "vertrauen", "angebot", "karriere", "bewertungen"]
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    for w in (1081, 1180, 1241, 1280, 1366, 1440, 1600):
        pg = b.new_page(viewport={"width": w, "height": 860})
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL, wait_until="load")
        r = pg.evaluate("()=>{let m=0;document.querySelectorAll('.nav *').forEach(e=>{const s=getComputedStyle(e);if(s.display==='none'||s.visibility==='hidden'||e.closest('.menu')&&getComputedStyle(document.querySelector('.menu')).visibility==='hidden')return;const r=e.getBoundingClientRect();if(r.width)m=Math.max(m,r.right)});return [Math.round(m),innerWidth,document.documentElement.scrollWidth-innerWidth]}")
        print(w, "kopfzeile rechts", r[0], "/", r[1], "querscroll", r[2], "OK" if r[0] <= r[1] and r[2] <= 0 else "FEHLER")
        if w == 1440:
            for ch in CH:
                hh = pg.evaluate("(id)=>document.getElementById(id).offsetHeight", ch)
                for f in ([0, .15, .3, .45, .6, .75, .9, 1] if hh > 1300 else [.5]):
                    pg.evaluate("([id,f])=>{const s=document.getElementById(id);window.scrollTo(0,s.offsetTop+Math.max(0,s.offsetHeight-innerHeight)*f)}", [ch, f])
                    pg.wait_for_timeout(500)
                    pg.screenshot(path=OUT + f"{ch}-{int(f*100):03d}.jpg", type="jpeg", quality=70)
        pg.close()
    print("konsole:", errs[:5] or "0 Fehler")
