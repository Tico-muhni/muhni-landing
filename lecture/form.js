/* TICO FINANCE – טפסי הרצאות (ארגונים + עובדים) → Google Apps Script */
(function () {
  var SCRIPT_URL = 'https://script.google.com/macros/s/__LECTURE_SCRIPT_ID__/exec';
  var MAX_FILE = 10 * 1024 * 1024;
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign'];

  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  var params = new URLSearchParams(location.search);
  var utm = {};
  UTM_KEYS.forEach(function (k) {
    var v = params.get(k);
    if (v) store('tf_' + k, v);
    utm[k] = v || store('tf_' + k) || '';
  });

  function readFile(file) {
    return new Promise(function (resolve, reject) {
      var r = new FileReader();
      r.onload = function () { resolve(String(r.result).split(',')[1]); };
      r.onerror = reject;
      r.readAsDataURL(file);
    });
  }

  function val(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || '').trim() : '';
  }

  window.TicoLectureForm = function (form, opts) {
    var btn = form.querySelector('.submit-btn');
    var err = form.querySelector('.form-error');
    var label = btn.textContent;

    function fail(msg) {
      err.textContent = msg; err.hidden = false;
      btn.disabled = false; btn.textContent = label;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      err.hidden = true;
      if (!val(form, 'name')) return fail('נא למלא שם מלא');
      var phone = val(form, 'phone').replace(/[^\d+]/g, '');
      if (phone.length < 9) return fail('נא למלא מספר טלפון תקין');
      if (opts.requireOrg && !val(form, 'org')) return fail('נא למלא את שם הארגון');
      if (!form.elements.consent.checked) return fail('נא לאשר את מדיניות הפרטיות');

      var data = { type: opts.type, website: val(form, 'website'), page: location.pathname };
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.type !== 'file' && el.type !== 'checkbox' && !(el.name in data)) data[el.name] = String(el.value || '').trim();
      });
      if (opts.org) data.org = opts.org;
      var d = opts.defaultUtm || {};
      UTM_KEYS.forEach(function (k) { data[k] = utm[k] || d[k] || ''; });

      btn.disabled = true; btn.textContent = 'שולח...';

      var fileInput = form.querySelector('input[type=file]');
      var file = fileInput && fileInput.files[0];
      var ready = Promise.resolve();
      if (file) {
        if (file.size > MAX_FILE) return fail('הקובץ גדול מ-10MB. אפשר לשלוח צילום מסך או לדלג ולשלוח אחר כך');
        ready = readFile(file).then(function (b64) { data.file = { name: file.name, type: file.type, data: b64 }; });
      }

      ready.then(function () {
        return fetch(SCRIPT_URL, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) });
      }).then(function () {
        if (window.gtag) gtag('event', 'generate_lead', { form_type: 'lecture_' + opts.type, utm_campaign: data.utm_campaign });
        if (window.va) va('event', { name: 'lecture_' + opts.type });
        form.hidden = true;
        var ok = document.getElementById(opts.successId);
        ok.hidden = false;
        ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }).catch(function () {
        fail('משהו השתבש בשליחה. אפשר לנסות שוב או לשלוח וואטסאפ ל-050-770-0322');
      });
    });
  };
})();
