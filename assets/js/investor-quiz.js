/* "What kind of investor are you?" quiz. Six questions, a scored result, and a lead form that posts to the same Apps Script endpoint as the other pages. */
(function () {
  'use strict';
  var D = document, stage = D.getElementById('stage');
  if (!stage) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwCzY2nAC0xl61tXUhvA2q6th9v1ecYhP_3HsFuvJdm26-f_PElfu2xiGOYwtFWZUl0/exec';
  var WA = '972507700322';
  var stepTxt = D.getElementById('stepTxt'), barFill = D.getElementById('barFill'), backBtn = D.getElementById('backBtn');

  var TYPES = {
    flip: {
      name: 'פליפר', short: 'פליפ', tag: 'קונים, משפצים, מוכרים. ומהר.',
      what: 'אתם מחפשים רווח מהיר מההפרש בין קנייה למכירה, ומוכנים להשקיע זמן ומעורבות כדי לקבל אותו.',
      know: [
        'הרווח האמיתי נקבע אחרי כל העלויות: רכישה, שיפוץ, תיווך, מיסוי וחודשי החזקה.',
        'כל חודש שהנכס עומד עולה כסף, ולכן הזמן הוא חלק מהחישוב.',
        'חריגה בשיפוץ או מכירה שמתעכבת יכולות למחוק את כל הרווח.'
      ],
      mort: 'בדרך כלל זה לא מתאים למשכנתה ארוכה. הבסיס הוא הון עצמי ומימון לטווח קצר, ולכן בודקים מראש את עלות המימון ואת התנאים ליציאה מוקדמת.',
      risk: 'הפער בין התכנון לביצוע, והזמן שלוקח למכור.'
    },
    presale: {
      name: 'משקיע פריסייל', short: 'פריסייל', tag: 'מרוויחים מעליית ערך בזמן שהדירה נבנית.',
      what: 'אתם רוצים להתחיל בהון עצמי קטן ככל האפשר, ולהרוויח מעליית הערך בשנות הבנייה, בלי לנהל נכס בינתיים.',
      know: [
        'משלמים לפי התקדמות הבנייה, ולכן צריך לתכנן את לוח התשלומים מראש.',
        'עיכוב במסירה משפיע על התזרים ועל התוכניות שלכם, לא רק על הקבלן.',
        'ההון העצמי נעול כמה שנים, והמשכנתה נפתחת רק לקראת המסירה.'
      ],
      mort: 'המשכנתה נפתחת לקראת הסוף, ולכן צריך לדעת כבר היום אם היכולת שלכם תאפשר לקבל אותה בעוד שנים. בונים תוכנית לאורך כל תקופת הבנייה, ולא רק ליום החתימה.',
      risk: 'עיכובים, הצמדה למדד, ושינוי ביכולת ההחזר עד המסירה.'
    },
    mid: {
      name: 'מחזיק לטווח בינוני', short: 'טווח בינוני', tag: 'שנתיים עד חמש שנים, ויוצאים בזמן.',
      what: 'אתם רוצים גם הכנסה מהנכס וגם גמישות לצאת כשהשוק או החיים משתנים.',
      know: [
        'הרווח מגיע משכירות ומעליית ערך, ושניהם נבדקים אחרי מימון ומס.',
        'חשוב להבין מראש מה עולה לצאת מהנכס, כולל עמלת פירעון מוקדם.',
        'צריך תוכנית ליום שבו תחליטו למכור, ולא רק ליום שבו קניתם.'
      ],
      mort: 'משכנתה רגילה עם תמהיל גמיש, כך שאפשר לצאת בלי לשלם יותר מדי. בודקים את עמלות היציאה לפני שבוחרים מסלולים.',
      risk: 'הצורך למכור בזמן לא נוח.'
    },
    long: {
      name: 'משקיע לטווח ארוך', short: 'טווח ארוך', tag: 'תזרים שקט לשנים, בלי לרוץ אחרי השוק.',
      what: 'אתם מעדיפים יציבות. מחזיקים נכס חמש עד עשר שנים, ונותנים לזמן ולשכירות לעבוד בשבילכם.',
      know: [
        'התשואה האמיתית היא נטו, אחרי עלות המימון וההוצאות.',
        'תחזוקה, ועד בית ותקופות ריקות הם חלק קבוע מהחישוב.',
        'הנכס צריך לעמוד בעצמו גם כשהריבית משתנה.'
      ],
      mort: 'תמהיל יציב לתקופה ארוכה, 25 עד 30 שנה. היציבות חשובה כאן יותר מהריבית הנמוכה ביותר, ובודקים תרחיש של עליית ריבית.',
      risk: 'ריבית משתנה והוצאות לא צפויות לאורך השנים.'
    },
    portfolio: {
      name: 'בונה פורטפוליו', short: 'פורטפוליו', tag: 'חושבים על הנכס הבא לפני שקנו את הנוכחי.',
      what: 'אתם לא בונים עסקה אחת אלא מערכת. כל נכס צריך לקדם את הבא, ולא לחסום אותו.',
      know: [
        'סדר הרכישות, ועל שם מי רשום כל נכס, משפיעים על היכולת להמשיך.',
        'כל הלוואה קיימת נכנסת לחישוב של הבנק בבקשה הבאה.',
        'השאלה היא לא כמה העסקה עולה, אלא מה היא מאפשרת.'
      ],
      mort: 'בונים מבנה מימון לכל הנכסים יחד, עם תכנון של סדר הרכישות והמינוף, ובודקים מחזורים בהמשך כדי לפנות הון לנכס הבא.',
      risk: 'ריכוז סיכון ומינוף גבוה מדי כשכמה נכסים תלויים זה בזה.'
    }
  };
  var ORDER = ['flip', 'presale', 'mid', 'long', 'portfolio'];

  var QUESTIONS = [
    { q: 'מתי אתם מצפים לראות את הכסף חוזר?', o: [
      ['תוך שנה', { flip: 3 }],
      ['בעוד 2 עד 4 שנים, כשהפרויקט מסתיים', { presale: 3, mid: 1 }],
      ['בין שנתיים לחמש שנים', { mid: 3, presale: 1 }],
      ['בין 5 ל-10 שנים', { long: 3, portfolio: 1 }],
      ['אני לא מתכנן/ת למכור', { portfolio: 3, long: 2 }]
    ] },
    { q: 'כמה הון עצמי אתם מוכנים להכניס בתחילת הדרך?', o: [
      ['סכום משמעותי, אבל לזמן קצר', { flip: 2, mid: 1 }],
      ['כמה שפחות עכשיו, ויותר בהמשך', { presale: 3 }],
      ['סכום בינוני', { mid: 2, presale: 1 }],
      ['סכום גדול בבת אחת', { long: 2, mid: 1 }],
      ['הון שמתחלק בין כמה נכסים', { portfolio: 3 }]
    ] },
    { q: 'כמה מעורבות אתם מוכנים לתת לנכס?', o: [
      ['שיפוץ, קבלנים ומכירה', { flip: 3 }],
      ['כמעט כלום עד המסירה', { presale: 3 }],
      ['שוכר ותחזוקה שוטפת', { mid: 2, long: 1 }],
      ['מעט, עם מנהל נכס', { long: 3, portfolio: 1 }],
      ['מערכת מסודרת שעובדת לבד', { portfolio: 3 }]
    ] },
    { q: 'איך אתם מרגישים לגבי סיכון?', o: [
      ['מוכנים לסיכון גבוה בשביל רווח מהיר', { flip: 3, presale: 1 }],
      ['מוכנים לחכות ולהתמודד עם עיכובים', { presale: 3 }],
      ['מחפשים איזון', { mid: 3 }],
      ['מעדיפים יציבות', { long: 3 }],
      ['מעדיפים לפזר בין כמה נכסים', { portfolio: 3 }]
    ] },
    { q: 'מה הכי חשוב לכם?', o: [
      ['רווח חד-פעמי מהיר', { flip: 3 }],
      ['עליית ערך בזמן שהדירה נבנית', { presale: 3 }],
      ['גמישות לצאת מתי שאני רוצה', { mid: 3 }],
      ['תזרים שקט לאורך שנים', { long: 3 }],
      ['נכסים שיישארו לדורות', { portfolio: 3 }]
    ] },
    { q: 'איפה אתם עומדים היום?', o: [
      ['זה יהיה הנכס הראשון שלי', { long: 2, mid: 1 }],
      ['יש לי דירה אחת, ואני שוקל/ת נכס נוסף', { mid: 1, long: 1, presale: 1 }],
      ['יש לי כבר נכס להשקעה אחד', { portfolio: 2, mid: 1 }],
      ['יש לי כמה נכסים', { portfolio: 3 }]
    ] }
  ];

  var ARW = '<svg class="ar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
  var CK = '<svg class="ck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>';
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>';
  var WAI = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>';

  var idx = 0, answers = [], result = null;

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function setProg(n) {
    stepTxt.textContent = 'שאלה ' + n + ' מתוך ' + QUESTIONS.length;
    barFill.style.width = (n / QUESTIONS.length * 100) + '%';
    backBtn.hidden = (n === 1);
  }
  function focusHead() { var h = stage.querySelector('.q,h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } }

  function renderQ() {
    var q = QUESTIONS[idx];
    D.getElementById('prog').hidden = false;
    setProg(idx + 1);
    stage.innerHTML = '<h3 class="q">' + esc(q.q) + '</h3><div class="opts one" role="radiogroup">' +
      q.o.map(function (o, j) {
        return '<button type="button" role="radio" aria-checked="' + (answers[idx] === j ? 'true' : 'false') + '" class="tile opt" data-o="' + j + '"><span class="tt">' + esc(o[0]) + '</span><span class="go">' + CK + '</span></button>';
      }).join('') + '</div>';
    focusHead();
    Array.prototype.forEach.call(stage.querySelectorAll('.tile'), function (b) {
      b.addEventListener('click', function () {
        answers[idx] = +b.getAttribute('data-o');
        Array.prototype.forEach.call(stage.querySelectorAll('.tile'), function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); });
        setTimeout(function () { if (idx < QUESTIONS.length - 1) { idx++; renderQ(); } else { finish(); } }, reduce ? 0 : 240);
      });
    });
  }

  function compute() {
    var total = { flip: 0, presale: 0, mid: 0, long: 0, portfolio: 0 };
    answers.forEach(function (a, qi) { var w = QUESTIONS[qi].o[a][1]; for (var k in w) total[k] += w[k]; });
    var first = QUESTIONS[0].o[answers[0]][1];
    var ranked = ORDER.slice().sort(function (a, b) { return (total[b] + (first[b] || 0) * 0.01) - (total[a] + (first[a] || 0) * 0.01); });
    return { total: total, ranked: ranked };
  }

  function waHref(t, second) {
    var msg = 'היי צ\'יקו, עשיתי את השאלון "איזה סוג משקיע אתה" ויצאתי: ' + t.name + ' (במקום שני: ' + second.short + '). אשמח לבדוק איך זה נראה אצלי במספרים.';
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }

  function finish() {
    var c = compute(); result = c;
    var t = TYPES[c.ranked[0]], second = TYPES[c.ranked[1]];
    D.getElementById('prog').hidden = true;
    var max = Math.max.apply(null, ORDER.map(function (k) { return c.total[k]; }).concat([1]));
    var fit = c.ranked.map(function (k, n) {
      var pct = Math.round(c.total[k] / max * 100);
      return '<div class="fit' + (n === 0 ? ' top' : '') + '"><span>' + esc(TYPES[k].short) + '</span><div class="bar"><i style="width:' + pct + '%"></i></div><b>' + pct + '%</b></div>';
    }).join('');
    stage.innerHTML =
      '<div class="rhead"><span class="rtag">התוצאה שלכם</span><h2 class="rname">' + esc(t.name) + '</h2><p class="rline">' + esc(t.tag) + '</p><p class="rwhat">' + esc(t.what) + '</p></div>' +
      '<h3 class="rh">מה חשוב לדעת</h3><ul class="sum">' + t.know.map(function (k) { return '<li>' + CHECK + '<span>' + esc(k) + '</span></li>'; }).join('') + '</ul>' +
      '<div class="rbox"><h3 class="rh">איך המשכנתה בנויה בדרך כלל</h3><p>' + esc(t.mort) + '</p></div>' +
      '<div class="rbox warn"><h3 class="rh">הסיכון המרכזי</h3><p>' + esc(t.risk) + '</p></div>' +
      '<h3 class="rh">ההתאמה שלכם לכל הסוגים</h3><div class="fits">' + fit + '</div>' +
      '<div class="rlead"><h3 class="q">רוצים שנבדוק את זה על העסקה שלכם?</h3><p class="rsub">השאירו פרטים ואחזור אליכם. בלי עלות ובלי התחייבות.</p>' +
      '<form class="form" id="lead" novalidate>' +
      '<div class="fld"><label for="nm">שם מלא</label><input id="nm" autocomplete="name" placeholder="ישראל ישראלי"><div class="err" id="nmE"></div></div>' +
      '<div class="fld"><label for="ph">טלפון</label><input id="ph" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="050-0000000"><div class="err" id="phE"></div></div>' +
      '<label class="consent"><input type="checkbox" id="cs"><span>אני מאשר/ת קבלת מידע מ-TICO FINANCE בהתאם ל<a href="/privacy.html">מדיניות הפרטיות</a></span></label>' +
      '<button class="sbm" id="sub" data-s="idle" type="submit"><span class="l">שלחו לי ניתוח מותאם</span><span class="ld"><svg class="spin" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"><circle cx="12" cy="12" r="9" opacity=".3"/><path d="M12 3a9 9 0 0 1 9 9"/></svg></span><span class="ok"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path class="ck-draw" d="M5 12l5 5 9-10"/></svg>נשלח</span></button></form>' +
      '<div class="alt-wa"><a class="wbtn" href="' + waHref(t, second) + '" target="_blank" rel="noopener"><span class="g">' + WAI + '</span><span>או בוואטסאפ<small>עם התוצאה מוכנה בהודעה</small></span></a></div></div>' +
      '<div class="rfoot"><button class="sbtn" id="again" type="button">מילוי מחדש</button><button class="sbtn" id="copy" type="button">העתקת קישור לשיתוף</button><span id="copyNote" class="cnote" aria-live="polite"></span></div>' +
      '<p class="disclaimer">השאלון כללי ולא מהווה ייעוץ השקעות או ייעוץ מס. לכל סוג השקעה יש סיכונים, והמימון תלוי בבנק, בהון העצמי ובאישור הסופי.</p>';
    focusHead();
    if (typeof window.gtag === 'function') window.gtag('event', 'quiz_complete', { event_category: 'quiz', event_label: c.ranked[0] });
    D.getElementById('again').addEventListener('click', restart);
    D.getElementById('copy').addEventListener('click', function () {
      var text = 'יצאתי ' + t.name + ' בשאלון של TICO FINANCE. ואתם? ' + location.href.split('#')[0];
      var note = D.getElementById('copyNote');
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { note.textContent = 'הועתק'; }, function () { note.textContent = text; });
      else note.textContent = text;
    });
    D.getElementById('lead').addEventListener('submit', function (e) {
      e.preventDefault();
      var nm = D.getElementById('nm').value.trim(), raw = D.getElementById('ph').value.trim(), dg = raw.replace(/[^\d]/g, ''), ok = true;
      D.getElementById('nmE').textContent = nm.length < 2 ? 'כתבו שם מלא' : ''; if (nm.length < 2) ok = false;
      var phOk = /^0\d{8,9}$/.test(dg) || /^972\d{8,9}$/.test(dg);
      D.getElementById('phE').textContent = phOk ? '' : 'כתבו מספר טלפון תקין, למשל 050-0000000'; if (!phOk) ok = false;
      if (ok && !D.getElementById('cs').checked) { ok = false; D.getElementById('phE').textContent = 'סמנו את אישור הפרטיות'; }
      if (!ok) return;
      var sb = D.getElementById('sub'); sb.dataset.s = 'loading';
      var scores = ORDER.map(function (k) { return TYPES[k].short + ' ' + c.total[k]; }).join(', ');
      var payload = { full_name: nm, phone_number: raw, page_source: 'investor-type', process: 'שאלון סוג משקיע', answers: t.name + ' | ' + scores };
      fetch(SCRIPT_URL, { method: 'POST', mode: 'no-cors', body: JSON.stringify(payload) }).then(function () {
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'form', event_label: 'investor-type' });
        sb.dataset.s = 'ok';
        setTimeout(function () { window.location.href = '/thank-you.html'; }, reduce ? 0 : 900);
      }, function () { sb.dataset.s = 'idle'; D.getElementById('phE').textContent = 'לא הצלחנו לשלוח כרגע. נסו שוב או כתבו לי בוואטסאפ.'; });
    });
  }

  function restart() { idx = 0; answers = []; result = null; renderQ(); window.scrollTo({ top: D.getElementById('quiz').offsetTop - 100, behavior: reduce ? 'auto' : 'smooth' }); }
  backBtn.addEventListener('click', function () { if (idx > 0) { idx--; renderQ(); } });
  renderQ();
})();
