/* Refinance page: bank instructions modal and the savings calculator (logic unchanged). */
(function(){
const bankData = {
    leumi: {
      name:"בנק לאומי", url:"https://mortgage.leumi.co.il/he/login",
      phone:"*6062", hours:"א'–ה' 8:00–16:00",
      steps:[
        "היכנסו לאזור האישי עם שם משתמש וסיסמא",
        "לחצו על <strong>הלוואות ומשכנתאות</strong> בתפריט הצד הימני",
        "בחרו <strong>הזמנת מסמכי משכנתאות</strong>",
        "בחרו <strong>אישור יתרות לסילוק</strong>",
        "הדוח יגיע לתיבת הדואר באזור האישי"
      ]
    },
    mizrahi: {
      name:"מזרחי טפחות", url:"https://www.mizrahi-tefahot.co.il/he/bank/private/loans-and-mortgages/mortgages/pages/mortgage-login.aspx",
      phone:"*8860", hours:"א'–ה' 8:30–18:30 | ו' 8:00–13:00",
      steps:[
        "<strong>אם יש לך חשבון עו&quot;ש:</strong> כנס באתר ← כניסה לחשבון ← הלוואות ומשכנתאות ← המשכנתה שלי ← טפסים ואישורים",
        "<strong>אם יש לך רק משכנתה:</strong> כנס לקישור לקוחות טפחות ← הזן ת&quot;ז ומספר חשבון ← קבל קוד SMS"
      ]
    },
    hapoalim: {
      name:"בנק הפועלים", url:"https://login.bankhapoalim.co.il/",
      phone:"*2401", hours:"א'–ה' 8:00–16:00",
      note:"רק אם יש לך חשבון עו&quot;ש בבנק הפועלים",
      steps:[
        "היכנסו לאזור האישי עם שם משתמש וסיסמא",
        "בחרו <strong>דוח פרטי משכנתאות</strong>",
        "אשרו קבלת דוח",
        "מקבלים מיד את הדוח ב-PDF"
      ]
    },
    discount: {
      name:"בנק דיסקונט", url:"https://www.discountbank.co.il/DB/he/private/mortgage",
      phone:"*2009", hours:"א'–ה' 8:00–19:00 | ו' 8:00–13:00",
      note:"רק אם יש לך חשבון עו&quot;ש בבנק",
      steps:[
        "כנסו לאזור האישי ← <strong>כניסה לחשבונות פרטיים</strong>",
        "הזינו קוד משתמש וסיסמא",
        "תפריט ימין ← בחרו <strong>משכנתאות</strong>",
        "לחצו <strong>פירוט המשכנתה המלא כולל יתרה לסילוק (תדפיס)</strong>"
      ]
    },
    jerusalem: {
      name:"בנק ירושלים", url:"#",
      phone:"076-8095115", hours:"א',ג',ד' 8:30–15:30 | ב',ה' 9:00–14:00 ו-16:00–18:00 | ו' 9:00–12:00",
      phoneOnly:true,
      steps:["הוצאת הדוח מתבצעת <strong>דרך המוקד הטלפוני בלבד</strong>. התקשר ובקש אישור יתרות לסילוק"]
    },
    mercantile: {
      name:"בנק מרכנתיל", url:"https://www.mercantile.co.il/private/mortgages/mortgage-data",
      phone:"*3477", hours:"א',ג',ה' 8:30–13:45 | ב',ד' 8:30–13:00 ו-16:00–18:15",
      note:"רק אם יש לך חשבון עו&quot;ש בבנק",
      steps:[
        "כנסו לאזור האישי ← <strong>כניסה לחשבונות פרטיים</strong>",
        "הזינו קוד משתמש וסיסמא",
        "תפריט ימין ← בחרו <strong>משכנתאות</strong>",
        "לחצו <strong>פירוט המשכנתה המלא כולל יתרה לסילוק</strong>"
      ]
    },
    fibi: {
      name:"הבנק הבינלאומי", url:"#",
      phone:"1-700-700-185 שלוחה 2", hours:"א'–ה' 8:00–18:00",
      phoneOnly:true,
      steps:["הוצאת הדוח מתבצעת <strong>דרך המוקד הטלפוני בלבד</strong>. התקשר ובקש אישור יתרות לסילוק"]
    },
    other: {
      name:"בנק אחר", url:"#", phone:"", hours:"",
      steps:[
        "פנה לאזור האישי באתר הבנק",
        "חפש הלוואות ומשכנתאות ← המשכנתה שלי",
        "בקש <strong>אישור יתרות לסילוק</strong>",
        "לחילופין, התקשר למוקד שירות הלקוחות"
      ]
    }
  };

  function openBankModal(bankId, card) {
    document.querySelectorAll('.bank-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    const sel = document.getElementById('bank_select');
    if (sel) sel.value = bankId;
    const bank = bankData[bankId];
    if (!bank) return;
    const stepsHtml = bank.steps.map((s,i) => `<div style="display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;">${bank.phoneOnly?'<span style="font-size:20px;">📞</span>':`<span style="min-width:24px;height:24px;background:var(--green);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0;">${i+1}</span>`}<span style="font-size:14px;line-height:1.6;">${s}</span></div>`).join('');
    const noteHtml = bank.note ? `<div style="background:#fff8e1;border-radius:8px;padding:10px 14px;margin-bottom:16px;font-size:13px;color:#7a5a00;">⚠️ ${bank.note}</div>` : '';
    const phoneHtml = bank.phone ? `<div style="margin-top:20px;padding:16px;background:var(--purple-light);border-radius:12px;"><div style="font-weight:700;font-size:13px;color:var(--green);margin-bottom:6px;">📞 ${bank.phoneOnly?'המוקד הטלפוני:':'לחילופין, דרך המוקד:'}</div><div style="font-size:18px;font-weight:800;direction:ltr;text-align:right;">${bank.phone}</div><div style="font-size:12px;color:var(--text-muted);margin-top:4px;">${bank.hours}</div></div>` : '';
    document.getElementById('modal-content').innerHTML = `<h3 style="font-size:20px;font-weight:800;color:var(--green);margin-bottom:4px;">איך מוציאים דוח יתרות?</h3><p style="font-size:14px;color:var(--text-muted);margin-bottom:20px;">${bank.name}</p>${noteHtml}${stepsHtml}${phoneHtml}<p style="font-size:12px;color:var(--text-muted);margin-top:16px;">לאחר הורדת הדוח, חזרו לכאן והעלו אותו בטופס 👇</p>`;
    const link = document.getElementById('modal-link');
    if (bank.url && bank.url !== '#') { link.href = bank.url; link.style.display = 'flex'; } else { link.style.display = 'none'; }
    document.getElementById('bank-modal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
  function closeModal() { document.getElementById('bank-modal').style.display = 'none'; document.body.style.overflow = ''; }
  function closeModalAndScroll() { closeModal(); setTimeout(() => document.getElementById('form').scrollIntoView({behavior:'smooth'}), 100); }
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  
// ===== CALCULATOR =====
  const PRIME_RATE = 5.25;
  const CPI_FORECAST = 1.8;
  // ריביות שוק ממוצעות (לפי נתוני יועץ, אוגוסט 2026)
  // ק"צ = קבועה צמודה | קל"צ = קבועה לא צמודה
  const MARKET_RATES = {
    'fixed_cpi':     2.90,  // ק"צ: 2.79%-3.17%
    'fixed_nominal': 4.55,  // קל"צ: 4.35%-4.65%
    'var_nominal':   0.90,  // מל"צ: עוגן + 0.85%-0.94%
    'var_cpi':       1.28,  // מ"צ: עוגן + 1.28%
    'prime':        -0.80,  // פריים: פריים - 0.80%-0.85%
  };
  const TRACK_TYPES = [
    { label:'ק"צ - קבועה צמודה למדד', type:'fixed_cpi', anchor:1.82 },
    { label:'קל"צ - קבועה לא צמודה', type:'fixed_nominal', anchor:3.60 },
    { label:'מל"צ - משתנה לא צמודה', type:'var_nominal', anchor:3.60 },
    { label:'מ"צ - משתנה צמודה', type:'var_cpi', anchor:1.82 },
    { label:'פריים', type:'prime', anchor:PRIME_RATE },
  ];
  let trackCount = 0;
  function getMarketRateDisplay(type, anchor) {
    const m = MARKET_RATES[type];
    if (type==='var_nominal'||type==='var_cpi') return (anchor+m).toFixed(2)+'%';
    if (type==='prime') return (PRIME_RATE+m).toFixed(2)+'%';
    return m.toFixed(2)+'%';
  }
  function addTrack() {
    if (trackCount >= 10) { document.getElementById('add-track-btn').style.display='none'; return; }
    trackCount++;
    const today = new Date();
    const defEnd = new Date(today.getFullYear()+20, today.getMonth(), 1).toISOString().slice(0,7);
    const opts = TRACK_TYPES.map(t => `<option value="${t.type}" data-anchor="${t.anchor}">${t.label}</option>`).join('');
    const div = document.createElement('div');
    div.id = `track-${trackCount}`;
    div.style.cssText = 'background:var(--bg);border:1.5px solid var(--border);border-radius:16px;padding:24px;margin-bottom:16px;';
    div.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
        <span style="font-weight:800;font-size:15px;color:var(--green);">מסלול ${trackCount}</span>
        ${trackCount>1?`<button onclick="removeTrack(${trackCount})" style="background:none;border:none;color:#ccc;font-size:18px;cursor:pointer;">✕</button>`:''}
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div style="grid-column:1/-1;">
          <label style="font-size:13px;font-weight:700;display:block;margin-bottom:6px;">סוג מסלול</label>
          <select id="tt-${trackCount}" onchange="updateMarket(${trackCount})" style="width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;background:white;appearance:none;">${opts}</select>
        </div>
        <div><label style="font-size:13px;font-weight:700;display:block;margin-bottom:6px;">יתרת המסלול (₪)</label><input type="number" id="tb-${trackCount}" placeholder="500000" style="width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;"/></div>
        <div><label style="font-size:13px;font-weight:700;display:block;margin-bottom:6px;">ריבית נוכחית (%)</label><input type="number" id="tr-${trackCount}" step="0.01" placeholder="3.50" style="width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;"/></div>
        <div><label style="font-size:13px;font-weight:700;display:block;margin-bottom:6px;">תאריך סיום</label><input type="month" id="te-${trackCount}" value="${defEnd}" style="width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;direction:ltr;"/></div>
        <div><label style="font-size:13px;font-weight:700;display:block;margin-bottom:6px;">החזר חודשי (₪)</label><input type="number" id="tp-${trackCount}" placeholder="2800" style="width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;"/></div>
      </div>`;
    document.getElementById('tracks-container').appendChild(div);
    updateMarket(trackCount);
    if (trackCount>=10) document.getElementById('add-track-btn').style.display='none';
  }
  function removeTrack(id) {
    const el=document.getElementById(`track-${id}`); if(el) el.remove();
    document.getElementById('add-track-btn').style.display='block';
    trackCount=document.querySelectorAll('[id^="track-"]').length;
  }
  function updateMarket(id) {
    const sel=document.getElementById(`tt-${id}`); if(!sel) return;
    const type=sel.value;
    const anchor=parseFloat(sel.options[sel.selectedIndex].dataset.anchor)||3.6;
    const el=document.getElementById(`tm-${id}`); if(el) el.textContent=getMarketRateDisplay(type,anchor);
  }
  function calcPmt(P,r,n) { if(r===0) return P/n; r/=100*12; return P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1); }
  function calculateSavings() {
    const ids=[...document.querySelectorAll('[id^="tt-"]')].map(e=>e.id.replace('tt-',''));
    if(!ids.length) { alert('אנא הוסף לפחות מסלול אחד'); return; }
    let totCurM=0,totNewM=0,totCurT=0,totNewT=0,valid=true,results=[];
    ids.forEach(id=>{
      const sel=document.getElementById(`tt-${id}`);
      const type=sel.value;
      const anchor=parseFloat(sel.options[sel.selectedIndex].dataset.anchor)||3.6;
      const bal=parseFloat(document.getElementById(`tb-${id}`)?.value);
      const rate=parseFloat(document.getElementById(`tr-${id}`)?.value);
      const endStr=document.getElementById(`te-${id}`)?.value;
      const pmt=parseFloat(document.getElementById(`tp-${id}`)?.value);
      if(!bal||!rate||!endStr) { valid=false; return; }
      const [ey,em]=endStr.split('-').map(Number);
      const now=new Date(); const months=Math.max(1,(ey-now.getFullYear())*12+(em-(now.getMonth()+1)));
      const marg=MARKET_RATES[type];
      let mktRate;
      if(type==='var_nominal') mktRate=anchor+marg;
      else if(type==='var_cpi') mktRate=marg; // ריבית שוק ממוצעת ישירה: 3.0%
      else if(type==='prime') mktRate=PRIME_RATE+marg;
      else mktRate=marg;
      let curRate=rate, newRate=mktRate;
      const isCpi=(type==='fixed_cpi'||type==='var_cpi');
      if(isCpi) { curRate+=CPI_FORECAST; newRate+=CPI_FORECAST; }
      const curM=pmt||calcPmt(bal,curRate,months);
      const newM=calcPmt(bal,newRate,months);
      totCurM+=curM; totNewM+=newM; totCurT+=curM*months; totNewT+=newM*months;
      results.push({type:sel.options[sel.selectedIndex].text,inputRate:rate,curRate,newRate,isCpi,diff:curM-newM,totalDiff:curM*months-newM*months});
    });
    if(!valid||!results.length) { alert('אנא מלא את כל השדות: יתרה, ריבית ותאריך סיום'); return; }
    const mDiff=totCurM-totNewM, tDiff=totCurT-totNewT, saving=tDiff>500;
    const tracksHtml=results.map(t=>`<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);"><div><div style="font-weight:700;font-size:14px;">${t.type}</div><div style="font-size:12px;color:var(--text-muted);">ריבית נוכחית: ${t.inputRate.toFixed(2)}%${t.isCpi?` <span title="כולל תחזית מדד ${CPI_FORECAST}%" style="color:#b07d00;cursor:help;">(${t.curRate.toFixed(2)}% כולל מדד)</span>`:''}</div></div><div style="font-size:13px;color:${t.diff>0?'var(--success)':'#e74c3c'};font-weight:700;">${t.diff>0?'−':'+'}&rlm;₪${Math.abs(Math.round(t.diff)).toLocaleString()}/חודש</div></div>`).join('');
    const res=document.getElementById('calc-results');
    res.style.display='block';
    res.innerHTML=`<div style="border-radius:20px;overflow:hidden;box-shadow:0 8px 32px rgba(46,139,87,.12);">
      <div style="background:linear-gradient(135deg,#1d6b40,#2E8B57);padding:32px;color:white;text-align:center;">
        <div style="font-size:13px;opacity:.8;margin-bottom:6px;">הערכת פוטנציאל חיסכון</div>
        ${saving?`
          <div style="font-size:13px;opacity:.75;margin-bottom:2px;">חיסכון כולל לאורך כל התקופה</div>
          <div style="font-size:54px;font-weight:900;letter-spacing:-2px;">₪${Math.round(Math.abs(tDiff)).toLocaleString()}</div>
          <div style="width:50px;height:3px;background:rgba(255,255,255,.4);border-radius:2px;margin:10px auto 14px;"></div>
          <div style="background:rgba(255,255,255,.18);border-radius:12px;padding:10px 20px;display:inline-block;">
            <span style="font-size:14px;opacity:.9;">החזר חודשי נמוך ב־ </span><span style="font-weight:900;font-size:20px;">₪${Math.round(Math.abs(mDiff)).toLocaleString()}</span>
          </div>`:`
          <div style="font-size:20px;font-weight:800;margin-bottom:8px;">${tDiff<-5000?'התנאים שלך מעולים!':'ללא שינוי משמעותי'}</div>
          <div style="font-size:14px;opacity:.85;">${tDiff<-5000?'נראה שמיחזור בתנאי השוק הנוכחיים יעלה לך יותר.':'ייתכן שיש פוטנציאל בשינוי מבנה התמהיל.'}</div>`}
      </div>
      <div style="background:white;padding:24px 28px;"><div style="font-weight:800;font-size:13px;margin-bottom:12px;color:var(--text-muted);">פירוט לפי מסלול</div>${tracksHtml}</div>
      <div style="background:var(--bg);padding:20px 28px;">
        <p style="font-size:12px;color:var(--text-muted);margin-bottom:16px;line-height:1.6;">⚠️ <strong>חשוב:</strong> זוהי הערכה גסה בלבד. החיסכון האמיתי תלוי בעמלות פירעון מוקדם, מבנה התמהיל המלא ומצבך האישי. לסימולציה מדויקת, מלא את הטופס.</p>
        <a href="#form" onclick="document.getElementById('form').scrollIntoView({behavior:'smooth'});return false;" style="display:block;background:var(--g-600);color:white;text-align:center;padding:16px;border-radius:12px;font-weight:800;font-size:16px;text-decoration:none;">קבל סימולציה מדויקת ממומחה ←</a>
      </div>
    </div>`;
    res.scrollIntoView({behavior:'smooth',block:'start'});
  }
  addTrack();
  const bankSelectEl = document.getElementById('bank_select');
  if (bankSelectEl) bankSelectEl.addEventListener('change', function() {
    document.querySelectorAll('[id^="tt-"]').forEach(sel => updateMarket(sel.id.replace('tt-','')));
  });

  window.openBankModal=openBankModal; window.closeModal=closeModal; window.closeModalAndScroll=closeModalAndScroll;
  window.addTrack=addTrack; window.removeTrack=removeTrack; window.updateMarket=updateMarket; window.calculateSavings=calculateSavings;
})();
