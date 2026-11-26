#!/usr/bin/env python3
"""LCP lokal messen wie PageSpeed (Handy: langsames 4G + 4x CPU-Drosselung).

Start: python3 tools/lcp_check.py [url] [runs]
Gibt je Lauf LCP-Zeit, LCP-Element und FCP aus.
"""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:4381/index.html'
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
JS = """() => new Promise(res => {
  let last = null;
  new PerformanceObserver(l => { for (const e of l.getEntries()) last = e; }).observe({ type: 'largest-contentful-paint', buffered: true });
  setTimeout(() => {
    const fcp = performance.getEntriesByName('first-contentful-paint')[0];
    const el = last && last.element;
    res({ lcp: last ? Math.round(last.startTime) : null, size: last ? last.size : 0,
          el: el ? (el.tagName + '.' + [...el.classList].join('.') + ' ' + (el.currentSrc || el.textContent || '').slice(-60).trim()) : (last && last.url),
          fcp: fcp ? Math.round(fcp.startTime) : null });
  }, 9000);
})"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for i in range(runs):
        ctx = b.new_context(viewport={'width': 412, 'height': 823}, is_mobile=True, has_touch=True, device_scale_factor=1.75)
        pg = ctx.new_page()
        cdp = ctx.new_cdp_session(pg)
        cdp.send('Network.enable')
        cdp.send('Network.setCacheDisabled', {'cacheDisabled': True})
        # Lighthouse „Slow 4G“: 150 ms RTT, 1,6 Mbit/s runter, 750 kbit/s hoch
        cdp.send('Network.emulateNetworkConditions', {'offline': False, 'latency': 150, 'downloadThroughput': 1.6 * 1024 * 1024 / 8, 'uploadThroughput': 750 * 1024 / 8})
        cdp.send('Emulation.setCPUThrottlingRate', {'rate': 4})
        pg.goto(url, wait_until='commit', timeout=120000)
        r = pg.evaluate(JS)
        print(f'Lauf {i + 1}: LCP {r["lcp"]} ms · FCP {r["fcp"]} ms · Element {r["el"]}')
        ctx.close()
    b.close()
