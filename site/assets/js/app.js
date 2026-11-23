/* GLANZWERK – Musterseite Gebäudereinigung. Vanilla-JS, alles hängt an der Scroll-Position. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = document.documentElement;
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var seg = function (p, a, b) { return clamp((p - a) / (b - a), 0, 1); };
  var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var eout = function (t) { return 1 - Math.pow(1 - t, 3); };
  var band = function (p, a, b, f) { f = f || .03; return Math.min(seg(p, a, a + f), 1 - seg(p, b - f, b)); };
  var mobile = function () { return innerWidth < 900; };
  var fmt = function (n) { return Math.round(n).toLocaleString('de-DE'); };

  /* ---------- Bilder: data-img="name" → assets/img/name.webp (Handy name-m.webp) ---------- */
  var IMG = window.GW_IMG || {}, VID = window.GW_VID || {};
  $$('[data-img]').forEach(function (el) {
    var n = el.getAttribute('data-img');
    if (IMG[n]) { el.src = 'assets/img/' + n + (mobile() ? '-m' : '') + '.webp?v=' + (IMG._v || 1); el.decoding = 'async'; }
    else { el.removeAttribute('src'); el.style.display = 'none'; el.classList.add('missing'); }
  });
  // Teile, deren Foto noch fehlt, ganz ausblenden (nie Platzhalter zeigen)
  $$('[data-need]').forEach(function (el) { if (!IMG[el.getAttribute('data-need')]) el.style.display = 'none'; });

  /* ---------- Persönlicher Link: ?firma=Muster+Reinigung ---------- */
  (function () {
    var f = null;
    try { f = new URLSearchParams(location.search).get('firma'); if (f) sessionStorage.setItem('gw-firma', f); else f = sessionStorage.getItem('gw-firma'); } catch (e) {}
    if (!f) return;
    f = f.slice(0, 40);
    $$('[data-firma]').forEach(function (el) { el.textContent = f; });
    document.title = f + ' · Gebäudereinigung über Nacht';
  })();

  /* ---------- Menü, Toast, Dialoge ---------- */
  var burger = $('.nav-burger');
  burger.addEventListener('click', function () {
    var o = root.classList.toggle('menu-open'); burger.setAttribute('aria-expanded', o); burger.setAttribute('aria-label', o ? 'Menü schließen' : 'Menü öffnen');
  });
  $$('.menu a').forEach(function (a) { a.addEventListener('click', function () { root.classList.remove('menu-open'); burger.setAttribute('aria-expanded', false); }); });
  var toastT;
  function toast(t) { var el = $('.toast'); el.textContent = t; el.hidden = false; clearTimeout(toastT); toastT = setTimeout(function () { el.hidden = true; }, 3200); }
  function openM(id) {
    root.classList.remove('menu-open');
    var m = $('#m-' + id); if (!m) return;
    if (id === 'termin') $('#m-sum').textContent = cfgSummary();
    if (id === 'bewerbung') apReset();
    if (m.showModal) m.showModal(); else m.setAttribute('open', '');
  }
  $$('[data-open]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); openM(b.getAttribute('data-open')); }); });
  $$('.modal').forEach(function (m) {
    m.addEventListener('click', function (e) { if (e.target === m) m.close(); });
    $$('[data-close]', m).forEach(function (b) { b.addEventListener('click', function () { m.close(); }); });
  });
  $('#m-termin form').addEventListener('submit', function (e) {
    var btn = e.submitter;
    if (btn && btn.value === 'ok') { toast('Demo: Ihre Anfrage wäre jetzt bei der Objektleitung.'); }
  });

  /* Wunschtermine: nächste 5 Werktage */
  (function () {
    var box = $('#slots'), d = new Date(), n = 0, wd = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
    while (n < 5) {
      d.setDate(d.getDate() + 1);
      if (d.getDay() === 0 || d.getDay() === 6) continue;
      var t = wd[d.getDay()] + ' ' + d.getDate() + '.' + (d.getMonth() + 1) + '. · ' + (n % 2 ? '14:00' : '10:00');
      box.insertAdjacentHTML('beforeend', '<label><input type="radio" name="slot" value="' + t + '"' + (n ? '' : ' checked') + '><span>' + t + '</span></label>');
      n++;
    }
  })();

  /* ---------- Film-Szene: Video spulen, sonst Standbild ---------- */
  function Film(scene) {
    var v = $('.vid', scene), key = v && v.getAttribute('data-key'), ok = false, want = 0, cur = 0;
    if (v && VID[key]) {
      var s = document.createElement('source');
      s.src = v.getAttribute('data-src') + (mobile() ? '-m' : '') + '.mp4?v=' + (VID._v || 1); s.type = 'video/mp4'; v.appendChild(s);
      v.addEventListener('loadeddata', function () { ok = true; scene.classList.add('has-vid'); });
      v.load(); var pr = v.play && v.play(); if (pr && pr.then) pr.then(function () { v.pause(); }).catch(function () {});
    }
    return {
      has: function () { return ok; },
      set: function (p) {
        if (!ok || !v.duration) return;
        want = (v.duration - .05) * p; cur += (want - cur) * .35;
        if (Math.abs(v.currentTime - cur) > .02) v.currentTime = cur;
      }
    };
  }

  /* ---------- Kapitel 1: Eine Nacht ---------- */
  var N = $('#nacht'), sc = $$('.scene', N), beats = $$('.beat', N);
  var F0 = Film(sc[0]), F2 = Film(sc[1]), F3 = Film(sc[2]);
  var after = $('.after', sc[0]), stripes = $('.stripes', N), count = $('.count', N), tbLine = $('.tb-line', N), tbMarks = $$('.tb-line b', N), tbClock = $('.tb-clock', N), tbLabel = $('.tb-label', N), hint = $('.scroll-hint', N);
  var hasAfter = after && !after.classList.contains('missing');
  // Zeitachse: Scroll-Anteil → Minuten ab 22:00
  var TP = [[0, 0], [.1, 10], [.32, 90], [.36, 240], [.58, 330], [.62, 420], [.82, 470], [.86, 478], [1, 480]];
  function minutes(p) {
    for (var i = 1; i < TP.length; i++) if (p <= TP[i][0]) { var a = TP[i - 1], b = TP[i]; return a[1] + (b[1] - a[1]) * seg(p, a[0], b[0]); }
    return 480;
  }
  function clock(m) { var t = (22 * 60 + Math.round(m / 5) * 5) % 1440; return ('0' + Math.floor(t / 60)).slice(-2) + ':' + ('0' + t % 60).slice(-2); }
  // Hochdruck-Bahnen: 9 Bahnen nacheinander von oben nach unten
  var NS = 9;
  function stripeMask(t) {
    if (!stripes) return;
    var img = $('img', stripes), imgs = [], sizes = [], pos = [], w = 100 / NS;
    for (var i = 0; i < NS; i++) {
      var f = seg(t, i / NS, (i + 1) / NS);
      if (f <= 0) break;
      imgs.push('linear-gradient(#000,#000)'); sizes.push((w + .2).toFixed(2) + '% ' + (f * 100).toFixed(1) + '%');
      pos.push((i * w / (100 - w) * 100).toFixed(2) + '% 0%');
    }
    var mi = imgs.length ? imgs.join(',') : 'linear-gradient(transparent,transparent)';
    img.style.webkitMaskImage = img.style.maskImage = mi;
    img.style.webkitMaskSize = img.style.maskSize = sizes.join(',') || '0 0';
    img.style.webkitMaskPosition = img.style.maskPosition = pos.join(',') || '0 0';
    img.style.webkitMaskRepeat = img.style.maskRepeat = 'no-repeat';
  }
  function show(el, o, dy, keepY) {
    if (!el) return;
    el.style.opacity = o.toFixed(3);
    el.style.transform = (keepY ? 'translateY(-50%) ' : '') + 'translateY(' + ((1 - o) * (dy == null ? 26 : dy)).toFixed(1) + 'px)';
    el.style.visibility = o < .01 ? 'hidden' : 'visible';
  }
  function night(p) {
    // Szenen überblenden
    sc[0].style.opacity = 1;
    sc[1].style.opacity = seg(p, .32, .36).toFixed(3);
    sc[2].style.opacity = seg(p, .58, .62).toFixed(3);
    sc[3].style.opacity = seg(p, .82, .86).toFixed(3);
    // Innen
    var pi = seg(p, .06, .32);
    if (F0.has()) F0.set(pi);
    else if (hasAfter) after.style.opacity = ease(seg(p, .16, .28)).toFixed(3);
    sc[0].style.setProperty('--z', (1 + .08 * ease(pi)).toFixed(4));
    // Außen
    var pa = seg(p, .36, .58);
    if (F2.has()) F2.set(pa); else stripeMask(seg(p, .37, .56));
    sc[1].style.setProperty('--z', (1.06 - .06 * ease(pa)).toFixed(4));
    if (count) count.textContent = fmt(3200 * eout(seg(p, .38, .55)));
    // Glas
    var pg = seg(p, .62, .82);
    if (F3.has()) F3.set(pg);
    sc[2].style.setProperty('--z', (1 + .12 * ease(pg)).toFixed(4));
    sc[3].style.setProperty('--z', (1.08 - .08 * eout(seg(p, .82, 1))).toFixed(4));
    // Texte
    show(beats[0], 1 - seg(p, .04, .1), -40, true);
    show(beats[1], band(p, .12, .31));
    show(beats[2], band(p, .38, .57), 26, true);
    show(beats[3], band(p, .64, .81));
    show(beats[4], seg(p, .87, .92));
    hint.style.opacity = 1 - seg(p, 0, .03);
    // Zeitleiste
    var m = minutes(p);
    tbClock.textContent = clock(m);
    tbLine.style.setProperty('--p', (m / 480 * 100).toFixed(2) + '%');
    tbLabel.textContent = p < .1 ? '22:00' : p < .34 ? 'Innen' : p < .6 ? 'Außen' : p < .84 ? 'Glas' : 'Fertig';
    tbMarks.forEach(function (b, i) { b.classList.toggle('on', m / 480 >= [.22, .5, .78][i]); });
  }

  /* ---------- Fortschritt je Kapitel ---------- */
  function prog(sec) {
    var r = sec.getBoundingClientRect(), h = sec.offsetHeight - innerHeight;
    return h > 0 ? clamp(-r.top / h, 0, 1) : 0;
  }

  /* ---------- Kapitel 3: Objekt live ---------- */
  var L = $('#live'), lk = $$('[data-k]', L), floors = $$('.fl', L), pins = $('.pins', L), tl = $('.tl-line', L);
  var KS = [.06, .2, .44, .64, .84];
  function live(p) {
    lk.forEach(function (el) { var k = +el.getAttribute('data-k'); if (k !== 1 || el.tagName === 'LI') el.classList.toggle('on', p >= KS[k]); });
    floors.forEach(function (f, i) { f.classList.toggle('on', p >= KS[1] + i * .05); });
    pins.classList.toggle('on', p >= KS[2]);
    tl.style.setProperty('--p', (seg(p, .02, .9) * 100).toFixed(1) + '%');
  }

  /* ---------- Kinetik-Typo (Vertrauen, Karriere) ---------- */
  function kin(sec, a, step) {
    var sp = $$('.kin span', sec);
    return function (p) {
      sp.forEach(function (s, i) {
        var t = eout(seg(p, a + i * step, a + i * step + step * 1.1));
        s.style.opacity = t.toFixed(3);
        s.style.transform = 'translateX(' + ((1 - t) * -8).toFixed(2) + 'vw)';
      });
    };
  }
  var T = $('#vertrauen'), C = $('#karriere'), kT = kin(T, .08, .16), kC = kin(C, .06, .14);
  var FC = Film($('.career-bg', C));

  /* ---------- Scroll-Schleife ---------- */
  var nav = $('.nav'), ticking = false;
  function frame() {
    ticking = false;
    nav.classList.toggle('solid', scrollY > N.offsetHeight - innerHeight * 1.2);
    night(prog(N));
    live(prog(L));
    kT(prog(T));
    kC(prog(C));
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  addEventListener('scroll', req, { passive: true });
  addEventListener('resize', req);
  frame();
  // Videos laufen beim Spulen nach: einige Frames weiterrechnen
  setInterval(function () { if (F0.has() || F2.has() || F3.has()) night(prog(N)); }, 50);
  // Karriere-Film läuft als Schleife, sobald sichtbar
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) { var v = $('video', C); if (!FC.has()) return; if (e.isIntersecting) { var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else v.pause(); });
    }).observe(C);
  }

  /* ---------- Leistungen: Karte aufklappen ---------- */
  var cards = $$('.card');
  function openCard(c) { cards.forEach(function (x) { x.classList.toggle('is-open', x === c); }); }
  cards.forEach(function (c) {
    c.addEventListener('click', function () { openCard(c); });
    c.addEventListener('mouseenter', function () { if (!mobile()) openCard(c); });
    c.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openCard(c); } });
  });

  /* ---------- Angebot: Konfigurator ---------- */
  var area = $('#area'), out = $('#m2'), cfg = $('#cfg');
  var RATE = { innen: 220, glas: 70, aussen: 380 }, NAMES = { innen: 'Innen', glas: 'Glas', aussen: 'Außen' };
  function m2() { var v = +area.value; return Math.max(100, Math.round(100 * Math.pow(200, v / 100) / 50) * 50); }
  function calc() {
    var a = m2(), arts = $$('input[name=art]:checked', cfg).map(function (i) { return i.value; });
    if (!arts.length) { $$('input[name=art]', cfg)[0].checked = true; arts = ['innen']; }
    var h = arts.reduce(function (s, k) { return s + a / RATE[k]; }, 0);
    var team = Math.max(1, Math.ceil(h / 6)), per = Math.max(1, Math.round(h / team * 2) / 2);
    out.textContent = fmt(a) + ' m²';
    area.style.setProperty('--v', area.value + '%');
    $('#r-h').textContent = 'ca. ' + String(per).replace('.', ',') + ' Std.';
    $('#r-t').textContent = team + (team > 1 ? ' Personen' : ' Person');
  }
  function cfgSummary() {
    var arts = $$('input[name=art]:checked', cfg).map(function (i) { return NAMES[i.value]; }).join(' + ');
    var obj = ($('input[name=obj]:checked', cfg) || {}).value, iv = $('input[name=int]:checked', cfg);
    return arts + ' · ' + obj + ' · ' + fmt(m2()) + ' m² · ' + (iv ? iv.nextElementSibling.textContent : '');
  }
  cfg.addEventListener('input', calc); cfg.addEventListener('change', calc); calc();
  $('#pics').addEventListener('change', function () { var n = this.files.length; $('#picn').textContent = n ? n + (n > 1 ? ' Fotos ausgewählt (bleiben auf Ihrem Gerät)' : ' Foto ausgewählt (bleibt auf Ihrem Gerät)') : 'Hilft uns bei der Einschätzung'; });

  /* ---------- Bewerbung in 60 Sekunden ---------- */
  var QS = [
    ['Wo arbeitest du lieber?', ['Drinnen', 'Draußen + Glas']],
    ['Welche Schicht passt dir?', ['Nachtschicht', 'Frühschicht']],
    ['Hast du einen Führerschein?', ['Ja', 'Noch nicht']],
    ['Schon mal gereinigt?', ['Ja, Erfahrung', 'Quereinstieg']],
    ['Ab wann kannst du starten?', ['Sofort', 'In 1–2 Monaten']]
  ];
  var ap = $('#m-bewerbung'), apI = 0;
  function apShow() {
    $('.ap-bar', ap).style.setProperty('--p', ((apI + 1) / QS.length * 100) + '%');
    $('.ap-n', ap).textContent = 'Frage ' + (apI + 1) + ' von ' + QS.length;
    $('.ap-q', ap).textContent = QS[apI][0];
    $('.ap-a', ap).innerHTML = QS[apI][1].map(function (t) { return '<button type="button">' + t + '</button>'; }).join('');
  }
  function apReset() { apI = 0; $('.ap-card', ap).hidden = false; $('.ap-n', ap).hidden = false; $('.ap-done', ap).hidden = true; apShow(); }
  $('.ap-a', ap).addEventListener('click', function (e) {
    if (e.target.tagName !== 'BUTTON') return;
    var card = $('.ap-card', ap); card.classList.add('out');
    setTimeout(function () {
      card.classList.remove('out'); apI++;
      if (apI >= QS.length) { card.hidden = true; $('.ap-n', ap).textContent = 'Alle 5 Fragen beantwortet'; $('.ap-done', ap).hidden = false; }
      else apShow();
    }, 280);
  });
  $('.ap-done', ap).addEventListener('submit', function () { if (!this.checkValidity()) return; ap.close(); toast('Demo: Bewerbung wäre jetzt raus. Rückruf meist am selben Tag.'); });

  /* ---------- Bewertungen: hochzählen, Sterne füllen ---------- */
  var scores = $$('.score'), counted = false;
  function countUp() {
    if (counted) return; counted = true;
    var t0 = performance.now();
    (function step(t) {
      var k = eout(clamp((t - t0) / 1600, 0, 1));
      scores.forEach(function (s) {
        var v = +s.getAttribute('data-score'), n = +s.getAttribute('data-n');
        $('.sc-num', s).textContent = (v * k).toFixed(1).replace('.', ',');
        $('.sc-n', s).textContent = fmt(n * k);
        $('.stars i', s).style.setProperty('--w', (v / 5 * 100 * k) + '%');
      });
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) countUp(); }, { threshold: .3 }).observe($('.scores'));
  else countUp();
  var qs = $$('.q'), qi = 0;
  setInterval(function () { qs[qi].classList.remove('on'); qi = (qi + 1) % qs.length; qs[qi].classList.add('on'); }, 5500);
})();
