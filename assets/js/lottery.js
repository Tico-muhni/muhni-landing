/* Lottery (מחיר למשתכן) calculator: logic unchanged. */
(function () {
  var VAT_PERCENT = 18;
  var BALCONY_FACTOR = 0.5;
  var STORAGE_FACTOR = 0.25;
  var PARKING_PRICE = 70000; // ₪ לחניה, כולל מע״מ - נוסף ישירות למחיר הכולל מע״מ
  var MORTGAGE_PRICE_CAP = 2100000;
  var MORTGAGE_LTV = 0.75;
  var MIN_EQUITY_WITH_GRANT = 60000;
  var MIN_EQUITY_NO_GRANT = 100000;
  var MORTGAGE_INTEREST_RATE_PERCENT = 4.7;
  var MORTGAGE_TERM_YEARS = [20, 25, 30];

  var currency = new Intl.NumberFormat('he-IL', { maximumFractionDigits: 0 });

  var SIZES = [
    { id: 1, label: '3 חדרים', mainSqm: 84 },
    { id: 2, label: '4 חדרים', mainSqm: 100 },
    { id: 3, label: '5 חדרים', mainSqm: 115 },
    { id: 4, label: '6 חדרים', mainSqm: 125 }
  ];

  function num(id) {
    var el = document.getElementById(id);
    var v = parseFloat(el.value);
    return isFinite(v) ? v : 0;
  }

  function selectedGrant() {
    var checked = document.querySelector('input[name="grant"]:checked');
    return checked ? parseFloat(checked.value) : 0;
  }

  function calculateEquityAndMortgage(contractPrice, marketValue, grant) {
    var minEquity = grant > 0 ? MIN_EQUITY_WITH_GRANT : MIN_EQUITY_NO_GRANT;
    var recognizedValue = marketValue > MORTGAGE_PRICE_CAP
      ? Math.max(MORTGAGE_PRICE_CAP, contractPrice)
      : marketValue;
    var mortgage = Math.max(
      Math.min(MORTGAGE_LTV * recognizedValue, contractPrice - minEquity),
      0
    );
    return { mortgage: mortgage, equity: contractPrice - mortgage };
  }

  function calculateMonthlyPayment(principal, years) {
    var monthlyRate = MORTGAGE_INTEREST_RATE_PERCENT / 100 / 12;
    var numPayments = years * 12;
    return (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -numPayments));
  }

  function recalculate() {
    var pricePerSqm = num('pricePerSqm');
    var discountPercent = num('discountPercent');
    var discountCap = num('discountCap');
    var referencePrice = num('referencePrice');
    var balconySqm = num('balconySqm');
    var storageSqm = num('storageSqm');
    var parkingCount = num('parkingCount');
    var grant = selectedGrant();

    // מ״ר עיקרי לכל גודל - ברירת מחדל סטנדרטית, ניתנת לעדכון בשדות
    // "מ״ר עיקרי בפועל" כשידוע המ״ר המדויק של הדירה הספציפית.
    var sizes = SIZES.map(function (s) {
      return { id: s.id, label: s.label, mainSqm: num('mainSqm' + s.id) };
    });

    var parkingCost = PARKING_PRICE * parkingCount;
    var balconySqmEquivalent = balconySqm * BALCONY_FACTOR;
    var storageSqmEquivalent = storageSqm * STORAGE_FACTOR;

    var priceBody = document.getElementById('priceResultsBody');
    var equityBody = document.getElementById('equityResultsBody');
    priceBody.innerHTML = '';
    equityBody.innerHTML = '';

    sizes.forEach(function (size) {
      var calcSqm = size.mainSqm + balconySqmEquivalent + storageSqmEquivalent;
      var preDiscountExVat = calcSqm * pricePerSqm;
      var preDiscountIncVat = preDiscountExVat * (1 + VAT_PERCENT / 100);

      var trackA = (discountPercent / 100) * preDiscountIncVat;
      var trackB = discountCap;
      var discount = Math.min(trackA, trackB, preDiscountIncVat);
      var boundBy = trackA <= trackB ? 'א׳ (אחוז)' : 'ב׳ (תקרה)';

      var finalIncVat = preDiscountIncVat - discount;
      var contractPrice = finalIncVat + parkingCost;

      var marketValue = referencePrice > 0
        ? referencePrice * calcSqm * (1 + VAT_PERCENT / 100)
        : preDiscountIncVat;

      var em = calculateEquityAndMortgage(contractPrice, marketValue, grant);
      var monthlyPaymentsHtml = MORTGAGE_TERM_YEARS.map(function (years) {
        return '<td>' + currency.format(calculateMonthlyPayment(em.mortgage, years)) + ' ₪</td>';
      }).join('');

      var priceRow = document.createElement('tr');
      priceRow.innerHTML =
        '<td><strong>' + escapeHtml(size.label) + '</strong> <span style="color:var(--text-muted);">(' + size.mainSqm + ' מ״ר)</span></td>' +
        '<td>' + calcSqm.toFixed(1) + '</td>' +
        '<td>' + currency.format(preDiscountIncVat) + ' ₪</td>' +
        '<td>' + currency.format(discount) + ' ₪</td>' +
        '<td>' + boundBy + '</td>' +
        '<td>' + currency.format(finalIncVat) + ' ₪</td>' +
        '<td class="highlight">' + currency.format(contractPrice) + ' ₪</td>';
      priceBody.appendChild(priceRow);

      var equityRow = document.createElement('tr');
      equityRow.innerHTML =
        '<td><strong>' + escapeHtml(size.label) + '</strong> <span style="color:var(--text-muted);">(' + size.mainSqm + ' מ״ר)</span></td>' +
        '<td>' + currency.format(contractPrice) + ' ₪</td>' +
        '<td class="highlight">' + currency.format(em.equity) + ' ₪</td>' +
        '<td>' + currency.format(grant) + ' ₪</td>' +
        '<td>' + currency.format(em.mortgage) + ' ₪</td>' +
        monthlyPaymentsHtml;
      equityBody.appendChild(equityRow);
    });

    document.getElementById('priceEmptyNote').style.display = pricePerSqm <= 0 ? 'block' : 'none';
  }

  function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  ['pricePerSqm', 'discountPercent', 'discountCap', 'referencePrice', 'balconySqm', 'storageSqm', 'parkingCount', 'mainSqm1', 'mainSqm2', 'mainSqm3', 'mainSqm4'].forEach(function (id) {
    document.getElementById(id).addEventListener('input', recalculate);
  });
  document.getElementById('grantOptions').addEventListener('change', recalculate);

  var hoverCapable = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function closeAllPinned() {
    document.querySelectorAll('.help-tip.open').forEach(function (t) { t.classList.remove('open'); });
  }

  // ממקם את חלונית העזרה עם קואורדינטות מוחלטות ביחס ל-viewport (position: fixed)
  // ומהדק אותה לגבולות המסך, כדי שלא תיחתך או "תקפוץ" במובייל בלי קשר לאיפה
  // כפתור ה-"?" נופל בפועל כשתווית השדה עוברת שורה.
  function positionPanel(tip) {
    var btn = tip.querySelector('.help-btn');
    var panel = tip.querySelector('.help-panel');
    var rect = btn.getBoundingClientRect();
    var margin = 12;
    var panelWidth = Math.min(280, window.innerWidth - margin * 2);
    var left = rect.right - panelWidth;
    left = Math.min(left, window.innerWidth - panelWidth - margin);
    left = Math.max(left, margin);
    var top = rect.bottom + 8;
    panel.style.width = panelWidth + 'px';
    panel.style.top = top + 'px';
    panel.style.left = left + 'px';
  }

  document.querySelectorAll('.help-tip').forEach(function (tip) {
    if (hoverCapable) {
      tip.addEventListener('mouseenter', function () {
        tip.classList.add('hovering');
        positionPanel(tip);
      });
      tip.addEventListener('mouseleave', function () {
        tip.classList.remove('hovering');
      });
    }
  });

  // הלחיצה מנעצת/משחררת רק את מצב ה"נעיצה" (open), בלי קשר למצב ה-hover -
  // כדי שלחיצה על מצביע שכבר נמצא בהובר תפתח אותה בנעיצה ולא תסגור אותה.
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.help-btn');
    if (btn) {
      var tip = btn.closest('.help-tip');
      var wasPinned = tip.classList.contains('open');
      closeAllPinned();
      if (!wasPinned) {
        tip.classList.add('open');
        positionPanel(tip);
      }
      return;
    }
    if (!e.target.closest('.help-panel')) closeAllPinned();
  });

  window.addEventListener('resize', function () {
    var activeTip = document.querySelector('.help-tip.open, .help-tip.hovering');
    if (activeTip) positionPanel(activeTip);
  });

  recalculate();
})();
