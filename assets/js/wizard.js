/* Path finder: pick a process, answer two short questions, leave details.
   Expects #wizard with #stepTxt, #barFill, #backBtn and #stage. Language from <html lang>. */
(function () {
  'use strict';
  var D = document, root = D.documentElement;
  var PT = (root.getAttribute('lang') || '').toLowerCase().indexOf('pt') === 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stage = D.getElementById('stage'), stepTxt = D.getElementById('stepTxt'), barFill = D.getElementById('barFill'), backBtn = D.getElementById('backBtn');
  if (!stage) return;
  var SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxPxMs-PTgr2iFpx7M-izBzzm5-UBwpmryeHsSl8LvdRNOVksgrV63PPUyYTRwp76aTZg/exec';
  var SNPV_URL = 'https://www.snpv.co.il/public/embedded_pages/Leads_balance_report/preview/d66f08c6-e409-4e59-8c4c-e577273cd516?source=website_home_refi';
  var WA = '972507700322';

  var S = PT ? {
    step: function (n, t) { return 'Etapa ' + n + ' de ' + t; }, back: 'Voltar', choose: 'Como podemos ajudar?',
    form: 'Ótimo. Veja o que vamos analisar para você', nm: 'Nome completo', nmPh: 'Seu nome', ph: 'Telefone (WhatsApp)', phPh: '+55 11 90000-0000',
    consent: 'Autorizo o contato da TICO FINANCE conforme a ', privacy: 'Política de Privacidade', privacyHref: '/br/privacidade.html', send: 'Quero receber minha análise', sent: 'Enviado',
    eName: 'Escreva seu nome completo', ePhone: 'Escreva um telefone válido, com DDD ou código do país', eCons: 'Marque a autorização de privacidade',
    eSend: 'Não foi possível enviar agora. Tente novamente ou escreva no WhatsApp.',
    thanks: function (n) { return 'Obrigado, ' + n + '. Recebi.'; }, now: 'Veja o que acontece agora, para você não ficar na dúvida.',
    t1: 'Recebi seus dados', t1s: 'Está tudo comigo', t2: 'Estou analisando seu caso', t2tag: 'agora', t2s: 'Análise completa em até 24 horas',
    t3: 'Volto com um retrato claro', t3s: 'Por telefone ou WhatsApp, como for melhor para você', prepT: 'Enquanto isso',
    resume: function (n) { return 'Que bom ver você de novo. Você começou uma análise: ' + n + '.'; }, resGo: 'Continuar de onde parei', resNo: 'Começar de novo',
    pathsLbl: 'Processo', bubble: 'Mensagem que será enviada', sign: 'Tico', ref: 'Conhece alguém? Indique um amigo', more: 'Mais sobre este processo',
    waMsg: function (p, a) { return 'Olá Tico! Deixei meus dados no site. ' + p + ' | ' + a.join(' | '); }
  } : {
    step: function (n, t) { return 'שלב ' + n + ' מתוך ' + t; }, back: 'חזרה', choose: 'באיזה תהליך אתם נמצאים?',
    form: 'מצוין. זה מה שנבדוק עבורכם', nm: 'שם מלא', nmPh: 'ישראל ישראלי', ph: 'טלפון', phPh: '050-0000000',
    consent: 'אני מאשר/ת קבלת מידע מ-TICO FINANCE בהתאם ל', privacy: 'מדיניות הפרטיות', privacyHref: '/privacy.html', send: 'שלחו לי ניתוח מומחה', sent: 'נשלח',
    eName: 'כתבו שם מלא', ePhone: 'כתבו מספר טלפון תקין, למשל 050-0000000', eCons: 'סמנו את אישור הפרטיות',
    eSend: 'לא הצלחנו לשלוח כרגע. נסו שוב או כתבו לי בוואטסאפ.',
    thanks: function (n) { return 'תודה ' + n + ', קיבלתי.'; }, now: 'הנה מה שקורה עכשיו, כדי שלא תצטרכו לנחש.',
    t1: 'קיבלתי את הפרטים', t1s: 'הכול אצלי', t2: 'אני בודק את הנתונים', t2tag: 'עכשיו', t2s: 'ניתוח מלא תוך 24 שעות',
    t3: 'חוזר אליכם עם תמונה ברורה', t3s: 'בטלפון או בוואטסאפ, איך שנוח לכם', prepT: 'בינתיים, אם אפשר',
    resume: function (n) { return 'שמחים לראות אתכם שוב. התחלתם בדיקה של ' + n + '.'; }, resGo: 'להמשיך מאיפה שעצרתם', resNo: 'להתחיל מחדש',
    pathsLbl: 'תהליך', bubble: 'ההודעה שתישלח', sign: 'צ\'יקו', ref: 'מכירים עוד מישהו? אפשר להפנות חבר', more: 'עוד על המסלול',
    waMsg: function (p, a) { return 'היי צ\'יקו! השארתי פרטים באתר. ' + p + ' | ' + a.join(' | '); }
  };

  var I = {
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
    loop: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 0 1-14 5.3M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4M6 21v-4h4"/></svg>',
    up: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>',
    flag: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>',
    ck: '<svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>',
    ring: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/></svg>',
    wa: '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>'
  };

  var PATHS = PT ? {
    br: {
      name: 'Comprar imóvel em Israel', ic: I.flag, sub: 'Consultoria 100% remota', page: '/br/', src: 'br-wizard',
      qs: [{ q: 'Qual é o seu objetivo?', o: ['Morar', 'Investir e alugar', 'Ainda não sei'] },
           { q: 'Em que etapa você está?', o: ['Estou pesquisando', 'Já tenho um imóvel em vista', 'Preciso entender o financiamento'] }],
      sum: function (a) { return ['Vamos explicar como funciona o financiamento para quem mora no exterior, de acordo com o seu objetivo: ' + a[0].toLowerCase() + '.', 'Vamos organizar a documentação e a transferência internacional de valores.', 'Vamos montar um plano para a etapa em que você está: ' + a[1].toLowerCase() + '.']; },
      prep: 'Se já tiver um imóvel em vista, envie os detalhes pelo WhatsApp. Também podemos começar sem ele.', waLbl: 'Continuar no WhatsApp', waSub: 'Direto comigo'
    }
  } : {
    refi: {
      name: 'מיחזור משכנתה', ic: I.loop, sub: 'יש לי משכנתה ורוצה לבדוק תנאים', page: '/refinance/', src: 'home-refinance', snpv: true,
      qs: [{ q: 'כמה זמן עבר מאז שלקחתם את המשכנתה?', o: ['פחות משנה', 'שנה עד 3 שנים', '3 עד 7 שנים', 'יותר מ-7 שנים'] },
           { q: 'מה הכי חשוב לכם?', o: ['להקטין החזר חודשי', 'לחסוך בסך הכל', 'לשחרר כסף לצרכים', 'עוד לא בטוח'] }],
      sum: function (a) { return ['נבדוק אם מיחזור משתלם אחרי עמלת פירעון מוקדם והוצאות נוספות.', 'נתאים את הבדיקה למטרה שלכם: ' + a[1] + '.', 'נבנה תמהיל חלופי ונשווה אותו למה שיש לכם היום.']; },
      prep: 'דוח יתרות לסילוק מהבנק. אפשר להתחיל בלעדיו, ולשלוח אותו בוואטסאפ כשיש.', waLbl: 'שלחו לי את הדוח בוואטסאפ', waSub: 'ישר אליי'
    },
    up: {
      name: 'שיפור דיור', ic: I.home, sub: 'מוכרים דירה וקונים גדולה יותר', page: '/upgraders/', src: 'home-upgraders',
      qs: [{ q: 'באיזה שלב אתם?', o: ['רק חושבים על זה', 'מחפשים דירה', 'מצאנו ויש הצעה', 'כבר חתמנו'] },
           { q: 'מה המצב של הדירה הנוכחית?', o: ['עוד לא למכירה', 'בתהליך מכירה', 'נמכרה'] }],
      sum: function (a) { return ['נתכנן את התזמון בין מכירת הדירה הישנה לקניית החדשה.', 'נבדוק אם צריך מימון ביניים ומה הכי נכון למצב: ' + a[1] + '.', 'נבנה תוכנית שמראה מראש כמה בנק יאשר ומה ההחזר הצפוי.']; },
      prep: 'אם כבר יש לכם הצעה לדירה החדשה, אפשר לשלוח אותה בוואטסאפ. אפשר להתחיל גם בלעדיה.', waLbl: 'המשיכו בוואטסאפ', waSub: 'ישר אליי'
    },
    inv: {
      name: 'משקיעי נדל"ן', ic: I.up, sub: 'בונים או מרחיבים תיק נכסים', page: '/investors/', src: 'home-investors',
      qs: [{ q: 'כמה נכסים יש לכם היום?', o: ['אף אחד', 'נכס אחד', '2 עד 3', '4 ומעלה'] },
           { q: 'מה המטרה העיקרית?', o: ['תזרים חודשי', 'צמיחה בהון', 'שילוב של השניים'] }],
      sum: function (a) { return ['נבנה מבנה מימון לתיק שלכם, כשאתם עכשיו עם ' + a[0] + '.', 'נתמקד במטרה שבחרתם: ' + a[1] + '.', 'נתכנן נקודות יציאה וגמישות לפני שחותמים על הנכס הבא.']; },
      prep: 'אם יש נכס שאתם שוקלים, אפשר לשלוח עליו פרטים בוואטסאפ. אפשר להתחיל גם בלעדיו.', waLbl: 'המשיכו בוואטסאפ', waSub: 'ישר אליי'
    }
  };

  var st = { path: null, ans: [], step: 0 };
  function total() { return PT ? 3 : 4; }
  function save() { try { localStorage.setItem('tico_wiz', JSON.stringify({ lang: PT ? 'pt' : 'he', path: st.path, ans: st.ans, step: st.step })); } catch (e) {} }
  function clearSave() { try { localStorage.removeItem('tico_wiz'); } catch (e) {} }
  function setProg(n) {
    stepTxt.textContent = S.step(n, total()); barFill.style.width = (n / total() * 100) + '%';
    backBtn.hidden = (n === 1); backBtn.textContent = S.back;
  }
  function focusHead() { var h = stage.querySelector('.q,h3'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var ARW = '<svg class="ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
  function tile(attrs, icon, title, small, tag) {
    var opt = icon === I.ring;
    return '<' + (tag || 'button') + (tag ? '' : ' type="button" role="radio" aria-checked="false"') + ' class="tile' + (opt ? ' opt' : '') + '" ' + attrs + '><span class="tt">' + title + (small ? '<small>' + small + '</small>' : '') + '</span><span class="go">' + (opt ? '' : ARW) + I.ck + '</span></' + (tag || 'button') + '>';
  }

  function renderChoose() {
    st = { path: null, ans: [], step: 0 };
    if (PT) { st.path = 'br'; st.step = 1; renderQ(); return; }
    setProg(1);
    stage.innerHTML = '<h3 class="q">' + S.choose + '</h3><div class="opts" role="radiogroup" aria-label="' + S.pathsLbl + '">' +
      Object.keys(PATHS).map(function (k) { var p = PATHS[k]; return tile('data-path="' + k + '"', p.ic, p.name, p.sub); }).join('') +
      '</div><a class="ptlink" href="/br/" hreflang="pt-BR" lang="pt-BR">Comprar imóvel em Israel · Português ' + ARW + '</a>';
    [].forEach.call(stage.querySelectorAll('[data-path]'), function (b) {
      b.addEventListener('click', function () {
        b.setAttribute('aria-checked', 'true'); st.path = b.getAttribute('data-path');
        setTimeout(function () { st.step = 1; renderQ(); }, reduce ? 0 : 380);
      });
    });
  }
  function renderQ() {
    var p = PATHS[st.path], i = st.step - 1, q = p.qs[i];
    setProg(PT ? st.step : st.step + 1); save();
    stage.innerHTML = '<h3 class="q">' + q.q + '</h3><div class="opts" role="radiogroup">' + q.o.map(function (o, j) { return tile('data-o="' + j + '"', I.ring, o); }).join('') + '</div>';
    var btns = [].slice.call(stage.querySelectorAll('[data-o]'));
    btns.forEach(function (b) { if (st.ans[i] === q.o[+b.getAttribute('data-o')]) b.setAttribute('aria-checked', 'true'); });
    focusHead();
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        btns.forEach(function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); });
        st.ans[i] = q.o[+b.getAttribute('data-o')];
        setTimeout(function () { if (st.step < p.qs.length) { st.step++; renderQ(); } else { st.step++; renderForm(); } }, reduce ? 0 : 380);
      });
    });
  }
  function waHref(p) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(S.waMsg(p.name, st.ans)); }
  function timeline() {
    return '<ol class="tl"><li class="ok"><span class="d">' + I.check.replace('<svg', '<svg width="16" height="16"') + '</span><div><b>' + S.t1 + '</b><span class="t">' + S.t1s + '</span></div></li>' +
      '<li class="now"><span class="d">2</span><div><b>' + S.t2 + '<span class="tag">' + S.t2tag + '</span></b><span class="t">' + S.t2s + '</span></div></li>' +
      '<li><span class="d">3</span><div><b>' + S.t3 + '</b><span class="t">' + S.t3s + '</span></div></li></ol>';
  }
  function renderForm() {
    var p = PATHS[st.path]; setProg(total()); save();
    var head = '<h3 class="q">' + S.form + '</h3><ul class="sum">' + p.sum(st.ans).map(function (t) { return '<li>' + I.check + '<span>' + esc(t) + '</span></li>'; }).join('') + '</ul>';
    if (p.snpv) {
      stage.innerHTML = head + '<iframe id="snpv" class="snpv" title="' + esc(p.name) + '" src="' + SNPV_URL + '" scrolling="no" frameborder="0"></iframe>' +
        '<div class="alt-wa"><a class="wbtn" href="' + waHref(p) + '" target="_blank" rel="noopener"><span class="g">' + I.wa + '</span><span>' + p.waLbl + '<small>' + p.waSub + '</small></span></a></div>';
      focusHead(); loadResizer(); return;
    }
    stage.innerHTML = head +
      '<form class="form" id="lead" novalidate>' +
      '<div class="fld"><label for="nm">' + S.nm + '</label><input id="nm" autocomplete="name" placeholder="' + S.nmPh + '"><div class="err" id="nmE"></div></div>' +
      '<div class="fld"><label for="ph">' + S.ph + '</label><input id="ph" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="' + S.phPh + '"><div class="err" id="phE"></div></div>' +
      '<label class="consent"><input type="checkbox" id="cs"><span>' + S.consent + '<a href="' + S.privacyHref + '">' + S.privacy + '</a></span></label>' +
      '<button class="sbm" id="sub" data-s="idle" type="submit"><span class="l">' + S.send + '</span><span class="ld"><svg class="spin" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><circle cx="12" cy="12" r="9" opacity=".3"/><path d="M12 3a9 9 0 0 1 9 9"/></svg></span><span class="ok"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path class="ck-draw" d="M5 12l5 5 9-10"/></svg>' + S.sent + '</span></button></form>' +
      '<div class="alt-wa"><a class="wbtn" href="' + waHref(p) + '" target="_blank" rel="noopener"><span class="g">' + I.wa + '</span><span>' + p.waLbl + '<small>' + p.waSub + '</small></span></a></div>';
    focusHead();
    D.getElementById('lead').addEventListener('submit', function (e) {
      e.preventDefault();
      var nm = D.getElementById('nm').value.trim(), raw = D.getElementById('ph').value.trim(), dg = raw.replace(/[^\d]/g, ''), ok = true;
      D.getElementById('nmE').textContent = nm.length < 2 ? S.eName : ''; if (nm.length < 2) ok = false;
      var phOk = PT ? /^\d{8,15}$/.test(dg) : /^0\d{8,9}$/.test(dg) || /^972\d{8,9}$/.test(dg);
      D.getElementById('phE').textContent = phOk ? '' : S.ePhone; if (!phOk) ok = false;
      if (ok && !D.getElementById('cs').checked) { ok = false; D.getElementById('phE').textContent = S.eCons; }
      if (!ok) return;
      var sb = D.getElementById('sub'); sb.dataset.s = 'loading';
      var payload = { full_name: nm, phone_number: raw, page_source: p.src, process: p.name, answers: st.ans.join(' | ') };
      fetch(SCRIPT_URL, { method: 'POST', mode: 'no-cors', body: JSON.stringify(payload) }).then(function () {
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'form', event_label: p.src });
        sb.dataset.s = 'ok'; setTimeout(function () { renderDone(nm); }, reduce ? 0 : 900);
      }, function () { sb.dataset.s = 'idle'; D.getElementById('phE').textContent = S.eSend; });
    });
  }
  function renderDone(nm) {
    var p = PATHS[st.path]; setProg(total()); barFill.style.width = '100%'; backBtn.hidden = true; clearSave();
    var first = nm.split(' ')[0];
    stage.innerHTML = '<div class="done"><div class="tick">' + I.check + '</div><h3>' + S.thanks(esc(first)) + '</h3><p>' + S.now + '</p>' + timeline() +
      '<div class="prep"><h4>' + S.prepT + '</h4><p>' + p.prep + '</p></div>' +
      '<div class="wawrap"><div class="bubble" role="tooltip"><b>' + S.bubble + '</b>' + esc(S.waMsg(p.name, st.ans)) + '</div><a class="wbtn" href="' + waHref(p) + '" target="_blank" rel="noopener"><span class="g">' + I.wa + '</span><span>' + p.waLbl + '<small>' + p.waSub + '</small></span></a></div>' +
      '<div class="sign">' + S.sign + '</div><a class="reflink" href="#refer">' + S.ref + '</a></div>';
    focusHead();
  }

  /* SNPV embedded form: auto-size, and count a lead when the form swaps to its thank-you view */
  function loadResizer() {
    function init() {
      var iframe = D.getElementById('snpv'); if (!iframe || typeof window.iFrameResize !== 'function') return;
      var touched = false, sent = false, base = null, last = null;
      window.addEventListener('blur', function () { setTimeout(function () { if (D.activeElement === iframe && !touched) { touched = true; base = last; } }, 0); });
      window.iFrameResize({
        log: false, checkOrigin: false, onResized: function (d) {
          var h = parseInt(d.height, 10); if (!h) return; last = h;
          if (!touched || sent) return; if (base === null) { base = h; return; }
          var delta = Math.abs(h - base);
          if (delta >= 120 || delta / base >= 0.2) { sent = true; clearSave(); if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'form', event_label: 'home_refinance_snpv' }); }
        }
      }, '#snpv');
    }
    if (typeof window.iFrameResize === 'function') { init(); return; }
    var sc = D.createElement('script'); sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/4.3.9/iframeResizer.min.js'; sc.onload = init; D.head.appendChild(sc);
  }

  backBtn.addEventListener('click', function () { if (st.step <= 1) { renderChoose(); return; } st.step--; renderQ(); });

  /* arrive with a pre-selected path: /#finder?p=refi or window.__pickPath */
  window.__pickPath = function (k) {
    if (!PATHS[k]) return; st = { path: k, ans: [], step: 1 }; renderQ();
    D.getElementById('finder').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  };
  [].forEach.call(D.querySelectorAll('[data-pick]'), function (a) {
    a.addEventListener('click', function (e) { var k = a.getAttribute('data-pick'); if (!PATHS[k]) return; e.preventDefault(); if (window.__closeMega) window.__closeMega(); window.__pickPath(k); });
  });

  /* resume where the visitor stopped */
  (function () {
    var saved = null; try { saved = JSON.parse(localStorage.getItem('tico_wiz') || 'null'); } catch (e) {}
    if (!saved || saved.lang !== (PT ? 'pt' : 'he') || !PATHS[saved.path] || !(saved.step >= 1)) return;
    var el = D.createElement('div'); el.className = 'resume'; el.setAttribute('role', 'status');
    el.innerHTML = '<span>' + esc(S.resume(PATHS[saved.path].name)) + '</span><div><button type="button" class="go">' + S.resGo + '</button><button type="button" class="no">' + S.resNo + '</button></div>';
    D.getElementById('wizard').parentNode.insertBefore(el, D.getElementById('wizard'));
    el.querySelector('.go').addEventListener('click', function () {
      st = saved; var n = PATHS[st.path].qs.length; st.step = Math.min(st.step, n + 1);
      if (st.step > n) renderForm(); else renderQ(); el.remove();
    });
    el.querySelector('.no').addEventListener('click', function () { clearSave(); el.remove(); });
  })();

  renderChoose();
})();
