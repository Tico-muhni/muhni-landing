/* Smart NPV embedded form: auto-size the iframe and count a lead when the form swaps to its thank-you view. */
(function () {
  'use strict';
  var D = document, iframe = D.getElementById('embedded-form-iframe');
  if (!iframe) return;
  function init() {
    if (typeof window.iFrameResize !== 'function') return;
    var touched = false, sent = false, base = null, last = null;
    window.addEventListener('blur', function () { setTimeout(function () { if (D.activeElement === iframe && !touched) { touched = true; base = last; } }, 0); });
    window.iFrameResize({
      log: false, checkOrigin: false,
      onResized: function (d) {
        var h = parseInt(d.height, 10); if (!h) return; last = h;
        if (!touched || sent) return; if (base === null) { base = h; return; }
        var delta = Math.abs(h - base);
        if (delta >= 120 || delta / base >= 0.2) { sent = true; if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { event_category: 'form', event_label: 'refinance_snpv' }); }
      }
    }, '#embedded-form-iframe');
  }
  if (typeof window.iFrameResize === 'function') { init(); return; }
  var sc = D.createElement('script'); sc.src = 'https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/4.3.9/iframeResizer.min.js'; sc.onload = init; D.head.appendChild(sc);
})();
