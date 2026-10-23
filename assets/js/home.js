/* Home page: savings simulator in the hero. */
(function () {
  'use strict';
  var D = document, loan = D.getElementById('loan'), diff = D.getElementById('diff'), mo = D.getElementById('mo');
  if (!loan || !diff || !mo) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nf = new Intl.NumberFormat('he-IL'), cur = 500, goal = 500, raf = 0;
  function tween() {
    cur += (goal - cur) * 0.2;
    if (Math.abs(goal - cur) < 0.6) cur = goal;
    mo.textContent = nf.format(Math.round(cur));
    if (cur !== goal) raf = requestAnimationFrame(tween);
  }
  function upd() {
    var L = +loan.value, d = +diff.value;
    goal = Math.round(L * d / 100 / 12 / 10) * 10;
    D.getElementById('loanOut').textContent = '₪' + nf.format(L);
    D.getElementById('diffOut').textContent = d.toFixed(2) + '%';
    cancelAnimationFrame(raf);
    if (reduce) { cur = goal; mo.textContent = nf.format(goal); } else tween();
  }
  loan.addEventListener('input', upd); diff.addEventListener('input', upd); upd();
})();
