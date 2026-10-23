/* Simple lead form for landing pages that post to the Apps Script endpoint. */
(function () {
  'use strict';
  var D = document, form = D.getElementById('leadForm');
  if (!form) return;
  var URL_ = 'https://script.google.com/macros/s/AKfycbwCzY2nAC0xl61tXUhvA2q6th9v1ecYhP_3HsFuvJdm26-f_PElfu2xiGOYwtFWZUl0/exec';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sb = D.getElementById('sub'), box = D.getElementById('errbox');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var nm = D.getElementById('full_name').value.trim(), raw = D.getElementById('phone').value.trim(), dg = raw.replace(/[^\d]/g, ''), ok = true;
    D.getElementById('nmE').textContent = nm.length < 2 ? 'כתבו שם מלא' : ''; if (nm.length < 2) ok = false;
    var phOk = /^0\d{8,9}$/.test(dg) || /^972\d{8,9}$/.test(dg);
    D.getElementById('phE').textContent = phOk ? '' : 'כתבו מספר טלפון תקין, למשל 050-0000000'; if (!phOk) ok = false;
    box.style.display = 'none';
    if (ok && !D.getElementById('consent').checked) { ok = false; box.textContent = 'סמנו את אישור הפרטיות כדי להמשיך'; box.style.display = 'block'; }
    if (!ok) return;
    sb.dataset.s = 'loading';
    fetch(URL_, { method: 'POST', mode: 'no-cors', body: JSON.stringify({ full_name: nm, phone_number: raw, page_source: form.getAttribute('data-source') }) }).then(function () {
      if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'form', event_label: form.getAttribute('data-source') });
      sb.dataset.s = 'ok';
      setTimeout(function () { window.location.href = '/thank-you.html'; }, reduce ? 0 : 900);
    }, function () { sb.dataset.s = 'idle'; box.textContent = 'לא הצלחנו לשלוח כרגע. נסו שוב או כתבו לי בוואטסאפ.'; box.style.display = 'block'; });
  });
})();
