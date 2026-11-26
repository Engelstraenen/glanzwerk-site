#!/usr/bin/env python3
"""Prüft die V2.69-Bausteine: Vorher/Nachher, Zahlen, Konfigurator, Unterseiten. Screens + Querscroll + Konsole."""
import os, sys
from playwright.sync_api import sync_playwright
BASE = 'http://127.0.0.1:4412/'
OUT = '/private/tmp/claude-501/gw-check/neu/'
os.makedirs(OUT, exist_ok=True)
SIZES = [(1440, 900), (390, 844), (360, 740), (430, 932), (844, 390)]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in SIZES:
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.on('console', lambda m: m.type == 'error' and errs.append(f'{w}: {m.text}'))
        pg.on('pageerror', lambda e: errs.append(f'{w}: {e}'))
        pg.goto(BASE, wait_until='load'); pg.wait_for_timeout(800)
        for sel in ['#leistungen', '#vorher-nachher', '#team', '#zahlen', '#angebot', '#bewertungen']:
            pg.evaluate(f"document.querySelector('{sel}').scrollIntoView({{block:'start'}})")
            pg.wait_for_timeout(2200)
            pg.screenshot(path=f'{OUT}{w}x{h}_{sel[1:]}.jpg', type='jpeg', quality=70)
        # Konfigurator bedienen
        pg.evaluate("document.querySelector('input[name=mat][value=parkett]').click(); document.querySelector('input[name=pause][value=\"4\"]').click(); document.querySelector('input[name=art][value=glas]').click()")
        pg.wait_for_timeout(300)
        pg.evaluate("document.querySelector('.report').scrollIntoView({block:'center'})"); pg.wait_for_timeout(400)
        pg.screenshot(path=f'{OUT}{w}x{h}_report.jpg', type='jpeg', quality=70)
        info = pg.evaluate("[document.querySelector('#r-n').textContent, document.querySelector('#mat-info').textContent.slice(0,40), document.querySelectorAll('#rep li').length]")
        sx = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
        print(w, h, 'index querscroll', sx, info)
        for k in ['innen', 'glas', 'aussen', 'hausmeister']:
            pg.goto(BASE + f'leistung-{k}.html', wait_until='load'); pg.wait_for_timeout(900)
            pg.screenshot(path=f'{OUT}{w}x{h}_sub-{k}-0.jpg', type='jpeg', quality=70)
            hh = pg.evaluate('document.documentElement.scrollHeight')
            for f in (0.35, 0.7):
                pg.evaluate(f'window.scrollTo(0,{int(hh * f)})'); pg.wait_for_timeout(900)
                pg.screenshot(path=f'{OUT}{w}x{h}_sub-{k}-{int(f*100)}.jpg', type='jpeg', quality=70)
            sx = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
            small = pg.evaluate("""[...document.querySelectorAll('a,button,summary,input')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&r.height<44&&getComputedStyle(e).opacity!=='0'}).map(e=>(e.textContent||e.type).trim().slice(0,20)+':'+Math.round(e.getBoundingClientRect().height)).slice(0,5)""")
            fs = pg.evaluate("""[...document.querySelectorAll('p,li,small,span,a')].filter(e=>e.offsetParent&&e.childElementCount===0&&e.textContent.trim()&&parseFloat(getComputedStyle(e).fontSize)<14).map(e=>e.textContent.trim().slice(0,20)).slice(0,5)""")
            print('   ', k, 'querscroll', sx, 'klein<44', small, 'font<14', fs)
        ctx.close()
    b.close()
print('konsole:', len(errs), errs[:5])
