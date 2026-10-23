/* TICO FINANCE shared behaviour: navigation, dock, greeting, accessibility widget, small helpers.
   Language comes from <html lang>; layout direction from <html dir>. */
(function () {
  'use strict';
  var D = document, root = D.documentElement;
  var PT = (root.getAttribute('lang') || '').toLowerCase().indexOf('pt') === 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || D).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || D).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {} return null; }

  /* ---------- WhatsApp click tracking (GA4) ---------- */
  D.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('a[href*="wa.me"]');
    if (!link || typeof window.gtag !== 'function') return;
    var label = (link.textContent || '').trim().slice(0, 60) || link.getAttribute('aria-label') || 'whatsapp';
    window.gtag('event', 'whatsapp_click', { event_category: 'engagement', event_label: label, page_location: location.href });
  });

  /* ---------- greeting by the visitor's own clock ---------- */
  function greet() {
    var h = new Date().getHours(), hi;
    if (PT) hi = h >= 5 && h < 12 ? 'Bom dia' : h >= 12 && h < 18 ? 'Boa tarde' : h >= 18 ? 'Boa noite' : 'Olá';
    else hi = h >= 5 && h < 11 ? 'בוקר טוב' : h >= 11 && h < 16 ? 'צהריים טובים' : h >= 16 ? 'ערב טוב' : 'שלום';
    $$('[data-greet]').forEach(function (el) {
      el.textContent = hi + (PT ? '. Eu sou o Tico Zveibel.' : '. אני צ\'יקו, אדריכל המשכנתאות');
    });
  }
  greet(); setInterval(greet, 60000);

  /* ---------- navigation ---------- */
  var nav = $('#nav');
  if (nav) {
    var menu = $('#menu'), ind = $('#ind'), sp = $('#sp'), btn = $('#svcBtn'), mega = $('#mega'), burger = $('#burger'), sheet = $('#sheet');
    var active = null, hoverT;
    function moveTo(el) {
      if (!ind) return;
      if (!el || !el.offsetWidth) { ind.style.opacity = 0; return; }
      ind.style.left = el.offsetLeft + 'px'; ind.style.width = el.offsetWidth + 'px'; ind.style.opacity = 1;
    }
    function onScroll() {
      nav.classList.toggle('scrolled', window.scrollY > 8);
      if (sp) {
        var d = root, max = d.scrollHeight - window.innerHeight;
        sp.style.width = (max > 0 ? Math.min(100, window.scrollY / max * 100) : 0) + '%';
      }
      updateDock();
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    if (menu) {
      var items = $$('a,button.has', menu);
      items.forEach(function (l) {
        l.addEventListener('mouseenter', function () { moveTo(l); });
        l.addEventListener('focus', function () { moveTo(l); });
      });
      menu.addEventListener('mouseleave', function () { moveTo(active); });
      /* current section on pages that have the sections */
      var map = {};
      $$('a[data-s]', menu).forEach(function (a) { if ($('#' + a.dataset.s)) map[a.dataset.s] = a; });
      if (window.IntersectionObserver && Object.keys(map).length) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            if (!e.isIntersecting) return;
            var a = map[e.target.id]; if (!a) return;
            $$('.on', menu).forEach(function (x) { x.classList.remove('on'); });
            a.classList.add('on'); active = a; moveTo(a);
          });
        }, { rootMargin: '-35% 0px -55% 0px' });
        Object.keys(map).forEach(function (id) { io.observe($('#' + id)); });
      }
      /* current page inside the services menu */
      var here = location.pathname.replace(/index\.html$/, '');
      $$('.svc a[href]').forEach(function (a) {
        var p = a.getAttribute('href').split('#')[0]; if (p && p === here) { a.classList.add('cur'); a.setAttribute('aria-current', 'page'); if (btn) btn.classList.add('on'); active = active || btn; }
      });
      if (active) moveTo(active);
    }
    if (btn && mega) {
      var openM = function () { mega.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); moveTo(btn); };
      var closeM = function () { mega.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); moveTo(active); };
      btn.addEventListener('click', function () { mega.classList.contains('open') ? closeM() : openM(); });
      btn.addEventListener('mouseenter', function () { clearTimeout(hoverT); hoverT = setTimeout(openM, 120); });
      nav.addEventListener('mouseleave', function () { clearTimeout(hoverT); hoverT = setTimeout(closeM, 220); });
      mega.addEventListener('mouseenter', function () { clearTimeout(hoverT); });
      D.addEventListener('click', function (e) { if (!nav.contains(e.target)) closeM(); });
      window.__closeMega = closeM;
    }
    function openSheet() { sheet.classList.add('open'); sheet.setAttribute('aria-hidden', 'false'); burger.setAttribute('aria-expanded', 'true'); root.style.overflow = 'hidden'; }
    function closeSheet() { sheet.classList.remove('open'); sheet.setAttribute('aria-hidden', 'true'); burger.setAttribute('aria-expanded', 'false'); root.style.overflow = ''; }
    if (burger && sheet) {
      burger.addEventListener('click', function () { sheet.classList.contains('open') ? closeSheet() : openSheet(); });
      $$('a', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
    }
    window.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (window.__closeMega) window.__closeMega();
      if (sheet) closeSheet();
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 980 && sheet) closeSheet(); moveTo(active); });
    if (D.fonts && D.fonts.ready) D.fonts.ready.then(function () { moveTo(active); });
    onScroll();
  }

  /* ---------- floating quick actions ---------- */
  var dock = $('#dock');
  function updateDock() {
    if (!dock) return;
    var target = $('#finder') || $('#form'), hidden = false;
    if (target) { var r = target.getBoundingClientRect(); hidden = r.top < window.innerHeight * 0.6 && r.bottom > window.innerHeight * 0.3; }
    dock.classList.toggle('show', window.scrollY > 520 && !hidden);
  }
  if (dock) {
    var main = $('a.main', dock);
    if (main && !$('#finder') && $('#form')) main.setAttribute('href', '#form');
    updateDock();
  }

  /* ---------- reviews: show the rest ---------- */
  $$('[data-more]').forEach(function (b) {
    b.addEventListener('click', function () {
      var wall = $(b.getAttribute('data-more')); if (!wall) return;
      wall.classList.add('open'); b.hidden = true;
    });
  });

  /* ---------- copy to clipboard ---------- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var text = b.getAttribute('data-copy'), label = $('[data-copy-label]', b) || b, old = label.textContent;
      function done() { label.textContent = b.getAttribute('data-done') || (PT ? 'Copiado' : 'הועתק'); b.setAttribute('data-ok', '1'); setTimeout(function () { label.textContent = old; b.removeAttribute('data-ok'); }, 1800); }
      function sel() {
        var el = $('.num', b.parentNode); if (el) { var r = D.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); }
        done();
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, sel); else sel();
    });
  });

  /* ---------- refer a friend ---------- */
  var SHARE_URL = 'https://www.ticofinance.co.il/' + (PT ? 'br/' : '');
  var shareMsg = PT ? 'Olá! O Tico Zveibel me ajudou e lembrei de você. Veja o site: ' + SHARE_URL
    : 'היי! צ\'יקו זוויבל עזר לי עם המשכנתה והמלצתי לך עליו. הנה האתר: ' + SHARE_URL;
  $$('[data-ref-wa]').forEach(function (a) { a.href = 'https://wa.me/?text=' + encodeURIComponent(shareMsg); });
  $$('[data-ref-copy]').forEach(function (b) { b.setAttribute('data-copy', SHARE_URL); });
  $$('[data-copy]').forEach(function () {}); /* data-copy set above is read at click time */

  /* ---------- intro video lightbox ---------- */
  var vids = $$('[data-video]');
  if (vids.length) {
    var VID = window.TICO_VIDEO_ID || '';
    var lb = D.createElement('div'); lb.className = 'lb'; lb.hidden = true; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', PT ? 'Vídeo' : 'וידאו');
    lb.innerHTML = '<div class="lb-in"><button class="lb-x" type="button" aria-label="' + (PT ? 'Fechar' : 'סגירה') + '">&times;</button><div class="lb-frame"></div></div>';
    D.body.appendChild(lb);
    var frame = $('.lb-frame', lb), x = $('.lb-x', lb), last = null;
    function open() {
      last = D.activeElement;
      frame.innerHTML = VID
        ? '<iframe src="https://www.youtube-nocookie.com/embed/' + VID + '?autoplay=1&rel=0" title="' + (PT ? 'Conheça o Tico' : 'הכירו אותי') + '" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>'
        : '<div class="lb-ph">' + (PT ? 'O vídeo de apresentação será publicado em breve. Enquanto isso, escreva direto no WhatsApp.' : 'הסרטון "הכירו אותי" יעלה בקרוב. בינתיים אפשר לכתוב לי ישר בוואטסאפ.') + '</div>';
      lb.hidden = false; root.style.overflow = 'hidden'; x.focus();
    }
    function close() { lb.hidden = true; frame.innerHTML = ''; root.style.overflow = ''; if (last) last.focus(); }
    vids.forEach(function (v) { v.addEventListener('click', open); });
    x.addEventListener('click', close);
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    window.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  /* ---------- accessibility widget ---------- */
  var T = PT ? {
    btn: 'Ferramentas de acessibilidade', title: 'Acessibilidade', size: 'Tamanho do texto', reset: 'Redefinir', contrast: 'Contraste',
    high: 'Alto', invert: 'Inverter', normal: 'Normal', links: 'Destacar links', spacing: 'Espaçamento maior', anim: 'Sem animações',
    stmt: 'Declaração de acessibilidade', href: '/accessibility.html', close: 'Fechar'
  } : {
    btn: 'כלי נגישות', title: 'כלי נגישות', size: 'גודל טקסט', reset: 'איפוס', contrast: 'ניגודיות',
    high: 'גבוהה', invert: 'הפוך', normal: 'רגיל', links: 'הדגשת קישורים', spacing: 'מרווח שורות רחב', anim: 'ללא אנימציות',
    stmt: 'הצהרת נגישות', href: '/accessibility.html', close: 'סגירה'
  };
  var w = D.createElement('div'); w.className = 'a11y'; w.id = 'a11y-widget';
  w.innerHTML =
    '<button class="a11y-btn" id="a11y-btn" type="button" aria-label="' + T.btn + '" aria-expanded="false" aria-controls="a11y-panel"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="12" cy="4" r="2"/><path d="M19 9h-6V7h-2v2H5l1 2h2.5l-1.8 7h2l1.3-5h4l1.3 5h2l-1.8-7H18z"/></svg></button>' +
    '<div class="a11y-panel" id="a11y-panel" role="dialog" aria-label="' + T.title + '" hidden>' +
    '<div class="a11y-head"><span>' + T.title + '</span><button type="button" class="a11y-x" aria-label="' + T.close + '">&times;</button></div>' +
    '<div class="a11y-body">' +
    '<div class="a11y-grp"><div class="a11y-lbl">' + T.size + '</div><div class="a11y-row"><button type="button" data-f="-1">A−</button><button type="button" data-f="0">' + T.reset + '</button><button type="button" data-f="1">A+</button></div></div>' +
    '<div class="a11y-grp"><div class="a11y-lbl">' + T.contrast + '</div><div class="a11y-row"><button type="button" data-c="high">' + T.high + '</button><button type="button" data-c="invert">' + T.invert + '</button><button type="button" data-c="none">' + T.normal + '</button></div></div>' +
    '<div class="a11y-grp a11y-tog"><label><span>' + T.links + '</span><input type="checkbox" data-t="a11y-links"></label><label><span>' + T.spacing + '</span><input type="checkbox" data-t="a11y-spacing"></label><label><span>' + T.anim + '</span><input type="checkbox" data-t="a11y-no-anim"></label></div>' +
    '<a class="a11y-stmt" href="' + T.href + '">' + T.stmt + ' &rarr;</a></div></div>';
  D.body.appendChild(w);
  var panel = $('#a11y-panel'), abtn = $('#a11y-btn'), scale = 0, S = {};
  function save() { store('tico_a11y', JSON.stringify(S)); }
  function applyFont() { root.style.fontSize = scale === 0 ? '' : (100 + scale * 10) + '%'; S.f = scale; }
  function setContrast(m) {
    D.body.classList.remove('a11y-high-contrast', 'a11y-invert');
    if (m === 'high') D.body.classList.add('a11y-high-contrast');
    if (m === 'invert') D.body.classList.add('a11y-invert');
    S.c = m;
  }
  function toggle(open) { panel.hidden = !open; abtn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  abtn.addEventListener('click', function () { toggle(panel.hidden); });
  $('.a11y-x', w).addEventListener('click', function () { toggle(false); abtn.focus(); });
  D.addEventListener('click', function (e) { if (!panel.hidden && !w.contains(e.target)) toggle(false); });
  window.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { toggle(false); abtn.focus(); } });
  $$('[data-f]', w).forEach(function (b) {
    b.addEventListener('click', function () {
      var d = +b.getAttribute('data-f'); scale = d === 0 ? 0 : Math.max(-2, Math.min(4, scale + d)); applyFont(); save();
    });
  });
  $$('[data-c]', w).forEach(function (b) { b.addEventListener('click', function () { setContrast(b.getAttribute('data-c')); save(); }); });
  $$('[data-t]', w).forEach(function (i) {
    i.addEventListener('change', function () { D.body.classList.toggle(i.getAttribute('data-t'), i.checked); S[i.getAttribute('data-t')] = i.checked; save(); });
  });
  try {
    var saved = JSON.parse(store('tico_a11y') || 'null');
    if (saved) {
      S = saved; scale = saved.f || 0; applyFont(); setContrast(saved.c || 'none');
      $$('[data-t]', w).forEach(function (i) { var k = i.getAttribute('data-t'); if (saved[k]) { i.checked = true; D.body.classList.add(k); } });
    }
  } catch (e) {}
})();
