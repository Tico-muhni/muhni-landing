"""Shared page chrome (head fragments, header, footer, floating actions) for the static site.

Run `python3 tools/build_pages.py` to regenerate the pages that use it.
Everything here is plain strings so the generated HTML is static and crawlable.
"""

WA_NUMBER = '972507700322'
PHONE_LABEL = '050-770-0322'
EMAIL = 'tico.z@ticofinance.co.il'
SITE = 'https://www.ticofinance.co.il'

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
CHIP = ('<span class="chip"><svg class="a" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
        '<svg class="b" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></span>')
CHIP_DOWN = CHIP.replace('<path d="M19 12H5M11 6l-6 6 6 6"/>', '<path d="M12 5v14M6 13l6 6 6-6"/>')
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'

WA_GLYPH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>'

# ---- original-colour brand marks -------------------------------------------------
IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1.5" y="1.5" width="21" height="21" rx="6" fill="url(#igG)"/><rect x="6" y="6" width="12" height="12" rx="3.6" fill="none" stroke="#fff" stroke-width="1.7"/><circle cx="12" cy="12" r="2.9" fill="none" stroke="#fff" stroke-width="1.7"/><circle cx="16.1" cy="7.9" r="1" fill="#fff"/></svg>'
FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#1877F2"/><path d="M13.2 19.5v-6.3h2.1l.4-2.6h-2.5V8.9c0-.8.3-1.3 1.4-1.3h1.2V5.4c-.3 0-1-.1-1.9-.1-1.9 0-3.1 1.1-3.1 3.2v2.1H8.7v2.6h2.1v6.3z" fill="#fff"/></svg>'
YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="1.2" y="4.2" width="21.6" height="15.6" rx="4.6" fill="#FF0000"/><path d="M10 8.7v6.6l5.7-3.3z" fill="#fff"/></svg>'
SP = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#1DB954"/><path d="M5.7 9.2c4.3-1.3 9-.8 12.7 1.5" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round"/><path d="M6.5 12.5c3.6-1 7.2-.6 10.3 1.3" fill="none" stroke="#000" stroke-width="1.7" stroke-linecap="round"/><path d="M7.3 15.6c2.9-.7 5.5-.4 8.1 1" fill="none" stroke="#000" stroke-width="1.4" stroke-linecap="round"/></svg>'
WA_MARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="#25D366"/><g transform="translate(4.6 4.6) scale(.62)"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></g></svg>'
GOOGLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.2c0-.8-.1-1.5-.2-2.2H12v4.3h5.9c-.3 1.4-1 2.5-2.2 3.3v2.7h3.5c2.1-1.9 3.3-4.7 3.3-8.1z"/><path fill="#34A853" d="M12 23c3 0 5.4-1 7.2-2.7l-3.5-2.7c-1 .7-2.2 1-3.7 1-2.8 0-5.3-1.9-6.1-4.5H2.3v2.8C4.1 20.5 7.8 23 12 23z"/><path fill="#FBBC05" d="M5.9 14.1c-.2-.7-.4-1.4-.4-2.1s.1-1.4.4-2.1V7.1H2.3C1.5 8.6 1 10.2 1 12s.5 3.4 1.3 4.9l3.6-2.8z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.4 2.2 15 1 12 1 7.8 1 4.1 3.5 2.3 7.1l3.6 2.8C6.7 7.3 9.2 5.4 12 5.4z"/></svg>'

IG_URL = 'https://www.instagram.com/ticozveibel/'
FB_URL = 'https://www.facebook.com/tico.zveibel'
SPOTIFY_URL = 'https://open.spotify.com/show/3z8X1tls84vHBbjRvpBRfa'
YOUTUBE_URL = 'https://youtube.com/playlist?list=PLTERUJJXsujA'
GOOGLE_BIZ_URL = 'https://maps.app.goo.gl/uM2Pnn88V9LEmeM89'

GRADIENT_DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="igG" x1="0" y1="1" x2="1" y2="0">'
                 '<stop offset="0" stop-color="#feda75"/><stop offset=".3" stop-color="#fa7e1e"/><stop offset=".55" stop-color="#d62976"/>'
                 '<stop offset=".8" stop-color="#962fbf"/><stop offset="1" stop-color="#4f5bd5"/></linearGradient></defs></svg>')


def wa(text=''):
    from urllib.parse import quote
    return f'https://wa.me/{WA_NUMBER}' + (f'?text={quote(text)}' if text else '')


# ---- <head> pieces -------------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800;900&family=Rubik:wght@500;700;800&family=Frank+Ruhl+Libre:wght@500;700;900&display=swap">')
ICONS = ('<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/><link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>'
         '<link rel="shortcut icon" href="/favicon.ico"/><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>')
CSS_LINK = '<link rel="stylesheet" href="/assets/css/tico.css?v=1">'
GA = ('<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-G9RC7QMNFJ"></script>'
      '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-G9RC7QMNFJ");</script>')


# ---- header ------------------------------------------------------------------------------
def _svc_rows(rows):
    return ''.join(
        f'<a href="{h}"{(" data-pick=" + chr(34) + k + chr(34)) if k else ""}><b>{t}</b><span class="d">{d}</span><span class="ar">{ARROW}</span></a>'
        for k, h, t, d in rows)


def header(lang='he'):
    he = lang == 'he'
    if he:
        home = '/'
        brand_alt = 'TICO FINANCE אדריכל המשכנתאות'
        menu = [('/#finder', 'finder', 'מצאו מסלול'), None, ('/#process', 'process', 'איך זה עובד'), ('/#meet', 'meet', 'הכירו אותי'),
                ('/#reviews', 'reviews', 'המלצות'), ('/#faq', 'faq', 'שאלות')]
        svc_label, svc_head = 'שירותים', 'באיזה תהליך אתם נמצאים?'
        rows = [('refi', '/refinance/', 'מיחזור משכנתה', 'לבדוק אם אפשר לשפר תנאים ולחסוך'),
                ('up', '/upgraders/', 'שיפור דיור', 'תזמון בין מכירה לקנייה, וגישור'),
                ('inv', '/investors/', 'משקיעי נדל"ן', 'מבנה מימון לתיק נכסים'),
                (None, '/br/', 'Comprar imóvel em Israel', 'Português · רכישה מרחוק')]
        more = [('/blog/', 'בלוג וטיפים'), ('/lottery-calculator/', 'מחשבון משכנתה לזוכי הגרלה'), ('/lecture/', 'הרצאות לארגונים')]
        feat_h, feat_p, feat_wa = 'לא בטוחים? נתחיל בשיחה', 'ספרו לי מה המצב, ואכוון אתכם.', 'וואטסאפ'
        lang_href, lang_txt, lang_lang = '/br/', 'Português', 'pt-BR'
        cta_txt, cta_href = 'בדיקה חינם', '/#finder'
        nav_aria, burger_aria = 'ניווט ראשי', 'תפריט'
        sheet_items = [('/#finder', 'מצאו מסלול'), ('/#process', 'איך זה עובד'), ('/#meet', 'הכירו אותי'), ('/#reviews', 'המלצות'), ('/#faq', 'שאלות נפוצות')]
        sheet_more = [('/blog/', 'בלוג וטיפים'), ('/lottery-calculator/', 'מחשבון הגרלות'), ('/lecture/', 'הרצאות לארגונים')]
        skip = 'דלגו לתוכן'
        sheet_svc = 'שירותים'
    else:
        home = '/br/'
        brand_alt = 'TICO FINANCE Arquiteto de hipotecas'
        menu = [('/br/#finder', 'finder', 'Comece aqui'), None, ('/br/#process', 'process', 'Como funciona'), ('/br/#meet', 'meet', 'Conheça o Tico'),
                ('/br/#reviews', 'reviews', 'Depoimentos'), ('/br/#faq', 'faq', 'Perguntas')]
        svc_label, svc_head = 'Serviços', 'Como podemos ajudar?'
        rows = [(None, '/br/#finder', 'Comprar imóvel em Israel', 'Consultoria 100% remota'),
                (None, '/br/#network', 'Financiamento sob medida', 'Para quem mora no exterior'),
                (None, '/br/#how', 'Acompanhamento até as chaves', 'Advogado, corretor e rede completa')]
        more = [('/', 'Site em hebraico'), ('/blog/', 'Blog e dicas')]
        feat_h, feat_p, feat_wa = 'Sem certeza? Vamos conversar', 'Conte-me sua situação e eu oriento você.', 'WhatsApp'
        lang_href, lang_txt, lang_lang = '/', 'עברית', 'he'
        cta_txt, cta_href = 'Conversa gratuita', '/br/#finder'
        nav_aria, burger_aria = 'Navegação principal', 'Menu'
        sheet_items = [('/br/#finder', 'Comece aqui'), ('/br/#process', 'Como funciona'), ('/br/#meet', 'Conheça o Tico'), ('/br/#reviews', 'Depoimentos'), ('/br/#faq', 'Perguntas frequentes')]
        sheet_more = [('/', 'Site em hebraico'), ('/blog/', 'Blog e dicas')]
        skip = 'Ir para o conteúdo'
        sheet_svc = 'Serviços'

    items = ''
    for m in menu:
        if m is None:
            items += f'<button class="has" id="svcBtn" type="button" aria-expanded="false" aria-controls="mega">{svc_label} {CHEV}</button>'
        else:
            items += f'<a href="{m[0]}" data-s="{m[1]}">{m[2]}</a>'
    flag = '<i aria-hidden="true"></i>' if he else ''
    more_html = ''.join(f'<a href="{h}">{t}</a>' for h, t in more)
    big = lambda lst: ''.join(f'<a class="big" href="{h}">{t} {ARROW}</a>' for h, t in lst)
    sheet_first, sheet_rest = big(sheet_items[:1]), big(sheet_items[1:])
    sheet_rows = ''.join(f'<a href="{h}"{(" data-pick=" + chr(34) + k + chr(34)) if k else ""}>{t}{ARROW}</a>' for k, h, t, d in rows)
    sheet_more_html = ''.join(f'<a href="{h}">{t}{ARROW}</a>' for h, t in sheet_more)
    return f'''{GRADIENT_DEFS}
<a class="skip" href="#main">{skip}</a>
  <header class="nav" id="nav">
    <div class="nav-in">
      <a class="brand" href="{home}" aria-label="{brand_alt}"><img src="/assets/img/logo-{'he' if he else 'en'}.webp" width="800" height="{185 if he else 218}" alt="{brand_alt}"></a>
      <nav class="menu" id="menu" aria-label="{nav_aria}"><span class="ind" id="ind"></span>{items}</nav>
      <div class="tools">
        <a class="lang" href="{lang_href}" hreflang="{lang_lang}" lang="{lang_lang}">{flag}{lang_txt}</a>
        <a class="pbtn sm" href="{cta_href}">{cta_txt} {CHIP}</a>
        <button class="burger" id="burger" type="button" aria-label="{burger_aria}" aria-expanded="false" aria-controls="sheet"><span></span><span></span></button>
      </div>
      <div class="mega" id="mega" role="region" aria-label="{svc_label}">
        <div class="mega-in">
          <div class="svc"><div class="svc-h">{svc_head}</div>{_svc_rows(rows)}<div class="svc-more">{more_html}</div></div>
          <div class="feat"><div><h3>{feat_h}</h3><p>{feat_p}</p></div>
            <img src="/assets/img/tico-fullbody.webp" alt="" width="547" height="1091" loading="lazy">
            <a class="wbtn" href="{wa()}" target="_blank" rel="noopener"><span class="g">{WA_GLYPH}</span><span>{feat_wa}<small></small></span></a></div>
        </div>
      </div>
    </div>
    <div class="sp" aria-hidden="true"><i id="sp"></i></div>
  </header>
<div class="sheet" id="sheet" aria-hidden="true">
  {sheet_first}
  <a class="big" href="{rows[0][1]}">{sheet_svc}</a>
  <div class="sub2">{sheet_rows}</div>
  {sheet_rest}
  <div class="sub2" style="padding-top:0">{sheet_more_html}</div>
  <div class="bottom">
    <a class="pbtn lg" href="{cta_href}">{cta_txt} {CHIP}</a>
    <a class="lang" href="{lang_href}" hreflang="{lang_lang}" lang="{lang_lang}">{flag}{lang_txt}</a>
  </div>
</div>'''


# ---- footer + dock ---------------------------------------------------------------------------
def footer(lang='he', refer_anchor=True):
    he = lang == 'he'
    soc = (f'<div class="fsoc"><a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Instagram">{IG}</a>'
           f'<a href="{FB_URL}" target="_blank" rel="noopener" aria-label="Facebook">{FB}</a>'
           f'<a href="{YOUTUBE_URL}" target="_blank" rel="noopener" aria-label="YouTube">{YT}</a>'
           f'<a href="{SPOTIFY_URL}" target="_blank" rel="noopener" aria-label="Spotify">{SP}</a>'
           f'<a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_MARK}</a></div>')
    if he:
        tag = 'כי בלי תכנון, אין כלום.'
        cols = [('מסלולים', [('/refinance/', 'מיחזור משכנתה'), ('/upgraders/', 'שיפור דיור'), ('/investors/', 'משקיעי נדל"ן'), ('/br/', 'Comprar imóvel em Israel')]),
                ('ידע', [('/blog/', 'בלוג משכנתאות ונדל"ן'), ('/lottery-calculator/', 'מחשבון משכנתה לזוכי הגרלה'), ('/lecture/', 'הרצאות לארגונים'), (SPOTIFY_URL, 'הפודקאסט: תשואה משולשת')]),
                ('יצירת קשר', [(wa(), 'וואטסאפ'), (f'tel:{PHONE_LABEL.replace("-", "")}', PHONE_LABEL), (f'mailto:{EMAIL}', EMAIL), ('/#refer', 'הפנו חבר')]),
                ('מידע משפטי', [('/terms.html', 'תנאי שימוש'), ('/privacy.html', 'מדיניות פרטיות'), ('/accessibility.html', 'הצהרת נגישות')])]
        copy = '© 2026 TICO FINANCE. כל הזכויות שמורות.<br>אדריכל המשכנתאות — ייעוץ משכנתאות ופיננסים בליווי אישי ומקצועי.'
        logo = '/assets/img/logo-he.webp'; alt = 'TICO FINANCE'
        dock = ('בדיקה חינם', 'וואטסאפ', 'התקשרו', '/#finder', 'פעולות מהירות')
    else:
        tag = 'Porque sem planejamento, não há nada.'
        cols = [('Serviços', [('/br/#finder', 'Comprar imóvel em Israel'), ('/br/#network', 'Financiamento sob medida'), ('/br/#how', 'Como funciona')]),
                ('Conteúdo', [('/blog/', 'Blog e dicas'), (SPOTIFY_URL, 'Podcast (em hebraico)'), ('/', 'Site em hebraico')]),
                ('Contato', [(wa(), 'WhatsApp'), (f'mailto:{EMAIL}', EMAIL), ('/br/#refer', 'Indicar um amigo')]),
                ('Legal', [('/br/termos.html', 'Termos de Uso'), ('/br/privacidade.html', 'Política de Privacidade'), ('/accessibility.html', 'Acessibilidade')])]
        copy = '© 2026 TICO FINANCE. Todos os direitos reservados.<br>Consultoria de financiamento imobiliário para brasileiros que compram em Israel.'
        logo = '/assets/img/logo-en.webp'; alt = 'TICO FINANCE'
        dock = ('Conversa gratuita', 'WhatsApp', 'Ligar', '/br/#finder', 'Ações rápidas')
    cols_html = ''.join(f'<div class="fcol"><h4>{h}</h4>' + ''.join(
        f'<a href="{u}"' + (' target="_blank" rel="noopener"' if u.startswith('http') else '') + f'>{t}</a>' for u, t in links) + '</div>' for h, links in cols)
    d_main, d_wa, d_call, d_href, d_aria = dock
    return f'''<div class="page">
  <footer class="sitefoot">
    <div class="fgrid">
      <div class="fbrand"><img src="{logo}" width="800" height="{185 if he else 218}" alt="{alt}" loading="lazy"><p class="ftag">{tag}</p>{soc}</div>
      {cols_html}
    </div>
    <p class="fcopy">{copy}</p>
  </footer>
</div>
<div class="dockwrap" id="dock"><nav class="dk" aria-label="{d_aria}">
  <a class="main" href="{d_href}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 11l3 3 8-9"/><path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h8"/></svg><span>{d_main}</span></a>
  <a href="{wa()}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg><span>{d_wa}</span></a>
  <a href="tel:{PHONE_LABEL.replace("-", "")}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg><span>{d_call}</span></a>
</nav></div>'''


SCRIPTS = '<script src="/assets/js/tico.js" defer></script>\n<script defer src="/_vercel/insights/script.js"></script>'
