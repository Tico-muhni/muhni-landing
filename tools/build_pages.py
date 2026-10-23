#!/usr/bin/env python3
"""Regenerates the public pages of ticofinance.co.il from their existing content plus the shared chrome.

Usage: python3 tools/build_pages.py            (run from the repository root)

Each page keeps its own <head> metadata (title, description, canonical, JSON-LD, hreflang).
Hidden pages (noindex tools, /check, /street, /card, /clients, /topsecret, /tf-*, ...) are never touched.
"""
import html as _html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import chrome as C  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(text)


def git_show(path):
    """Original version of a page from main (the redesign overwrites the working copy)."""
    try:
        return subprocess.check_output(['git', 'show', f'origin/main:{path}'], cwd=ROOT).decode('utf-8')
    except Exception:
        return read(path)


# ---------------------------------------------------------------------------------------------
def clean_head(src):
    """Keep metadata, drop old CSS / fonts / duplicated analytics helper; add the shared CSS and fonts."""
    head = re.search(r'<head>(.*?)</head>', src, re.S).group(1)
    head = re.sub(r'<style.*?</style>', '', head, flags=re.S)
    head = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>', '', head)
    head = re.sub(r'<script>\s*document\.addEventListener\(\'click\', function\(e\) \{\s*var link = e\.target\.closest\(\'a\[href\*="wa\.me"\]\'\);.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<link rel="icon"[^>]*>|<link rel="shortcut icon"[^>]*>|<link rel="apple-touch-icon"[^>]*>', '', head)
    head = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-G9RC7QMNFJ"></script>\s*<script>.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<meta content="width=device-width[^>]*>|<meta name="viewport"[^>]*>|<meta charset[^>]*>', '', head)
    head = re.sub(r'<script defer src="/_vercel/insights/script.js"></script>', '', head)
    head = re.sub(r'\n\s*\n+', '\n', head).strip()
    return ('<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1"/>\n<meta name="color-scheme" content="only light"/>\n<meta name="theme-color" content="#ffffff"/>\n' + C.ICONS + '\n' + C.GA + '\n' + head + '\n' + C.FONTS + '\n' + C.CSS_LINK)


def document(lang, head, body, scripts='', main_class=''):
    d = 'rtl' if lang == 'he' else 'ltr'
    l = 'he' if lang == 'he' else 'pt-BR'
    return (f'<!DOCTYPE html>\n<html dir="{d}" lang="{l}">\n<head>\n{head}\n</head>\n<body>\n'
            f'{C.header(lang)}\n<main id="main" class="page{(" " + main_class) if main_class else ""}">\n{body}\n</main>\n'
            f'{C.footer(lang)}\n{scripts}\n{C.SCRIPTS}\n</body>\n</html>\n')


def esc(t):
    return _html.escape(t, quote=False)


# ---------------------------------------------------------------------------------------------
# shared building blocks
def banks_strip(lang):
    names = [('leumi', 'בנק לאומי'), ('mizrahi', 'מזרחי טפחות'), ('hapoalim', 'בנק הפועלים'), ('discount', 'בנק דיסקונט'),
             ('jerusalem', 'בנק ירושלים'), ('mercantile', 'בנק מרכנתיל'), ('fibi', 'הבנק הבינלאומי')]
    sizes = {'leumi': 288, 'mizrahi': 216, 'hapoalim': 409, 'discount': 227, 'jerusalem': 221, 'mercantile': 191, 'fibi': 483}

    def imgs(dup):
        return ''.join(f'<img src="/assets/img/banks/{k}.webp" width="{round(sizes[k] * 30 / 88)}" height="30" alt="{"" if dup else n}" loading="lazy" decoding="async">' for k, n in names)
    label = 'עובדים מול כל הבנקים בישראל' if lang == 'he' else 'Trabalhamos com os principais bancos de Israel'
    return f'<section class="banks" aria-label="{label}"><p>{label}</p><div class="track">{imgs(False)}{imgs(True)}</div></section>'


def wizard(lang):
    he = lang == 'he'
    head = ('<div class="kicker">60 שניות</div><h2 class="h2">בואו נמצא את <em>המסלול שלכם</em></h2>'
            '<p class="lede">שתי שאלות קצרות, ותדעו מה בדיוק נבדוק עבורכם. בלי התחייבות.</p>') if he else (
        '<div class="kicker">60 segundos</div><h2 class="h2">Vamos encontrar <em>o seu caminho</em></h2>'
        '<p class="lede">Duas perguntas rápidas e você saberá o que vamos analisar para você. Sem compromisso.</p>')
    step = 'שלב 1 מתוך 4' if he else 'Etapa 1 de 3'
    back = 'חזרה' if he else 'Voltar'
    return (f'<section class="finder" id="finder"><div class="finder-head">{head}</div>'
            f'<div class="card" id="wizard"><div class="prog"><span id="stepTxt">{step}</span><div class="bar"><i id="barFill" style="width:25%"></i></div>'
            f'<button class="back" id="backBtn" type="button" hidden>{back}</button></div><div id="stage" aria-live="polite"></div></div></section>')


def review_cards(reviews, lang, visible=6):
    out = []
    for i, r in enumerate(reviews):
        cls = 'rv' + (' hl' if i == 0 else '') + (' more' if i >= visible else '')
        name = f'<bdi>{esc(r["name"])}</bdi>' if re.search(r'[A-Za-z]', r['name']) else esc(r['name'])
        role = r['role']
        if lang == 'pt' and role == 'ביקורת בגוגל':
            role = 'Avaliação no Google'
        out.append(f'<figure class="{cls}"><div class="stars" aria-hidden="true">★★★★★</div><p>{esc(r["quote"])}</p><footer>{name} <span>{esc(role)}</span></footer></figure>')
    return '\n'.join(out)


def parse_reviews():
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(git_show('index.html'), 'lxml')
    items = []
    for c in soup.select('.t-card'):
        q = c.find('p').get_text(' ', strip=True).strip('"“”')
        items.append({'quote': q, 'name': c.select_one('.t-name').get_text(strip=True), 'role': c.select_one('.t-role').get_text(strip=True)})
    # featured first: the long strategic review, then the Google ones that read best on a wall
    pri = ['נדב ל.', 'דימה ב.', 'אסף ר.', 'Isaac L.', 'Orel L.', 'Yom Tov A.']
    first = []
    for n in pri:
        for it in items:
            if it['name'] == n:
                first.append(it)
    rest = [it for it in items if it not in first]
    return first + rest


def reviews_section(lang, reviews):
    he = lang == 'he'
    head = ('<div><div class="kicker">מה אומרים עלינו</div><h2 class="h2">לקוחות <em>מספרים</em></h2></div>'
            '<div class="score"><b>5.0</b><span><span class="stars" aria-hidden="true">★★★★★</span>דירוג בגוגל</span></div>') if he else (
        '<div><div class="kicker">O que dizem</div><h2 class="h2">Clientes <em>contam</em></h2></div>'
        '<div class="score"><b>5.0</b><span><span class="stars" aria-hidden="true">★★★★★</span>Nota no Google</span></div>')
    note = '' if he else '<p class="lede" style="margin-bottom:22px">Avaliações originais de clientes, em hebraico.</p>'
    more = ('הצגת כל ההמלצות', 'Ver todas as avaliações')[0 if he else 1]
    gtxt = 'קישור לביקורות בגוגל ביזנס' if he else 'Link para as avaliações no Google Business'
    return (f'<section class="reviews" id="reviews"><div class="rv-head">{head}</div>{note}'
            f'<div class="wall" id="wall">{review_cards(reviews, lang)}</div>'
            f'<div class="wall-more"><button class="sbtn" type="button" data-more="#wall">{more}</button></div>'
            f'<div class="gline"><span class="gmark">{C.GOOGLE}</span><a class="sbtn" href="{C.GOOGLE_BIZ_URL}" target="_blank" rel="noopener">{gtxt} {C.ARROW}</a></div></section>')


def meet_section(lang, extra_he=''):
    he = lang == 'he'
    play = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'
    if he:
        head = '<div class="kicker">הכירו אותי</div><h2 class="h2">מי עומד <em>מאחורי התוכנית</em></h2>'
        vid = f'<button class="vid" type="button" data-video aria-label="הפעלת הסרטון הכירו אותי"><img src="/assets/img/tico-fullbody.webp" alt="" width="547" height="1091" loading="lazy"><span class="play">{play}</span><span class="vtag">הכירו אותי · 90 שניות</span></button>'
        bio = ('<div class="bio"><p>אני מאמין שמשכנתה היא אף פעם לא רק "השוואת ריביות", אלא <strong>ארכיטקטורה פיננסית שלמה</strong>. אני מסתכל על הפאזל המלא של החיים והעסקים שלכם - ובונה עבורכם את המסלול המדויק ביותר, בהתאמה אישית מלאה.</p>'
               '<p>בין אם אתם ממחזרים משכנתה קיימת, מתכננים מעבר דירה, בונים תיק נדל"ן להשקעה, או קונים נכס בישראל מרחוק - אני כאן ללוות אתכם צעד אחר צעד, מול הבנקים ומול המספרים הקטנים שעושים את כל ההבדל.</p></div>')
    else:
        head = '<div class="kicker">Conheça o Tico</div><h2 class="h2">Quem cuida <em>do seu processo</em></h2>'
        vid = f'<button class="vid" type="button" data-video aria-label="Assistir ao vídeo de apresentação"><img src="/assets/img/tico-fullbody.webp" alt="" width="547" height="1091" loading="lazy"><span class="play">{play}</span><span class="vtag">Conheça o Tico · 90 segundos</span></button>'
        bio = ('<div class="bio"><p>A TICO FINANCE nasceu para ajudar brasileiros a realizarem o sonho de ter um imóvel em Israel, mesmo estando a milhares de quilômetros de distância. Com mais de 3 anos de experiência no mercado imobiliário israelense, Tico Zveibel entende os dois lados: o brasileiro que quer investir, e o mercado israelense que precisa ser decifrado.</p>'
               '<p>Você não precisa confiar às cegas: cada etapa é acompanhada de perto, com transparência total e atualizações constantes. Porque distância não deveria significar insegurança.</p></div>')
    return f'<section class="meet" id="meet">{head}<div class="meet-grid">{vid}</div>{bio}</section>'


def community_section(lang):
    he = lang == 'he'
    def soc():
        L = [(C.IG_URL, C.IG, 'אינסטגרם' if he else 'Instagram', '@ticozveibel'), (C.FB_URL, C.FB, 'פייסבוק' if he else 'Facebook', 'tico.zveibel'),
             (C.YOUTUBE_URL, C.YT, 'יוטיוב' if he else 'YouTube', 'הפרקים המלאים' if he else 'Episódios completos'),
             (C.wa(), C.WA_MARK, 'וואטסאפ' if he else 'WhatsApp', C.PHONE_LABEL if he else '+972 50-770-0322')]
        return '<div class="soc">' + ''.join(f'<a href="{h}" target="_blank" rel="noopener"><span class="si">{ic}</span><span><b>{t}</b><small>{sm}</small></span></a>' for h, ic, t, sm in L) + '</div>'
    if he:
        head = '<div class="kicker">עוד דרכים להכיר</div><h2 class="h2">ממשיכים <em>גם מחוץ לאתר</em></h2>'
        pod = (f'<div class="pod"><div class="pod-l"><span class="pod-k">הפודקאסט</span><b>תשואה משולשת</b><p>פודקאסט משכנתאות בהנחיית צ\'יקו זוויבל, הדס יעקובסון ואבי הנפלינג.</p>'
               f'<span class="pod-row"><a class="pod-b" href="{C.SPOTIFY_URL}" target="_blank" rel="noopener">האזנה בספוטיפיי {C.ARROW}</a><a class="pod-b ghost2" href="{C.YOUTUBE_URL}" target="_blank" rel="noopener">צפייה ביוטיוב</a></span></div><div class="pod-r" aria-hidden="true">{C.SP}</div></div>')
    else:
        head = '<div class="kicker">Siga o Tico</div><h2 class="h2">Continue <em>fora do site</em></h2>'
        pod = (f'<div class="pod"><div class="pod-l"><span class="pod-k">Podcast</span><b>תשואה משולשת</b><p>Podcast sobre financiamento imobiliário, em hebraico, com Tico Zveibel, Hadas Yaakobson e Avi Hanefling.</p>'
               f'<span class="pod-row"><a class="pod-b" href="{C.SPOTIFY_URL}" target="_blank" rel="noopener">Ouvir no Spotify {C.ARROW}</a><a class="pod-b ghost2" href="{C.YOUTUBE_URL}" target="_blank" rel="noopener">Assistir no YouTube</a></span></div><div class="pod-r" aria-hidden="true">{C.SP}</div></div>')
    return f'<section class="community" id="community">{head}<div class="comm-grid">{pod}{soc()}</div></section>'


def refer_section(lang):
    if lang == 'he':
        body = ('<div><div class="kicker">מכירים מישהו?</div><h2 class="h2">הפנו חבר, <em>ואדאג לו כמו לכם</em></h2>'
                '<p class="lede" style="margin:0">שלחו לו את האתר בוואטסאפ. כל אחד מקבל ליווי אישי, וגם הוא יתחיל בבדיקה חינם.</p></div>'
                f'<div class="refer-btns"><a class="wbtn" data-ref-wa href="{C.wa()}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>שלחו בוואטסאפ<small>הודעה מוכנה</small></span></a>'
                '<button class="sbtn" type="button" data-ref-copy data-done="הועתק"><span data-copy-label>העתקת קישור</span></button></div>')
    else:
        body = ('<div><div class="kicker">Conhece alguém?</div><h2 class="h2">Indique um amigo, <em>e eu cuido dele como cuidei de você</em></h2>'
                '<p class="lede" style="margin:0">Envie o site pelo WhatsApp. Cada pessoa recebe atendimento pessoal e começa com uma conversa gratuita.</p></div>'
                f'<div class="refer-btns"><a class="wbtn" data-ref-wa href="{C.wa()}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>Enviar pelo WhatsApp<small>Mensagem pronta</small></span></a>'
                '<button class="sbtn" type="button" data-ref-copy data-done="Copiado"><span data-copy-label>Copiar link</span></button></div>')
    return f'<section class="refer" id="refer"><div class="refer-in">{body}</div></section>'


def close_section(lang):
    he = lang == 'he'
    acta = (f'<a class="acta" href="{"/#finder" if he else "/br/#finder"}"><span class="avw"><span class="av"><img src="/assets/img/tico-fullbody.webp" alt="" width="547" height="1091"></span><span class="dot"></span></span>'
            f'<span class="t"><small>{"ליווי אישי ממני" if he else "Acompanhamento pessoal comigo"}</small><b>{"בדיקה חינם · 60 שניות" if he else "Conversa gratuita · 60 segundos"}</b></span>'
            f'<span class="go">{C.ARROW}</span></a>')
    cp = (f'<div class="cp"><span class="num">{C.PHONE_LABEL if he else "+972 50-770-0322"}</span><button type="button" data-copy="{C.PHONE_LABEL if he else "+972507700322"}">'
          f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg>'
          f'<span data-copy-label>{"העתקה" if he else "Copiar"}</span></button></div>')
    if he:
        h = '<div class="kicker">מוכנים לתכנן?</div><h2 class="h2">התוכנית שלכם <em>מתחילה בשיחה אחת</em></h2><p class="lede">השאירו פרטים וחזרתי אליכם, או כתבו לי ישר בוואטסאפ.</p>'
    else:
        h = '<div class="kicker">Vamos conversar?</div><h2 class="h2">Seu plano <em>começa com uma conversa</em></h2><p class="lede">Deixe seus dados e eu retorno, ou escreva direto no WhatsApp.</p>'
    return f'<section class="close">{h}<div class="closeRow">{acta}{cp}</div></section>'


def faq_section(kicker, h2, items):
    its = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}<i>+</i></summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    return f'<section class="faq" id="faq"><div><div class="kicker">{kicker}</div><h2 class="h2">{h2}</h2></div><div>{its}</div></section>'


def band_section(h2, nums, cta_html):
    n = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in nums)
    return f'<section class="band"><h2>{h2}</h2><div class="nums">{n}</div>{cta_html}</section>'


# ---------------------------------------------------------------------------------------------
def build_home():
    src = git_show('index.html')
    head = clean_head(src)
    reviews = parse_reviews()
    wa_msg = "היי צ'יקו! הגעתי מהאתר ורוצה לבדוק אם כדאי לי למחזר את המשכנתה."
    hero = f'''<section class="hero">
  <div class="copy">
    <div class="kicker" data-greet>אדריכל המשכנתאות</div>
    <h1><span class="l1">משכנתה היא לא השוואת ריביות.</span><span class="l2">היא תוכנית.</span></h1>
    <p class="sub">ליווי אישי ומקצועי בכל תהליך פיננסי הקשור לנדל"ן: מיחזור, שיפור דיור, השקעות, ואפילו רכישת נכס בישראל מרחוק. כי בלי תכנון, אין כלום.</p>
    <div class="cta">
      <a class="pbtn lg" href="#finder">מצאו את המסלול שלכם {C.CHIP_DOWN}</a>
      <div class="wawrap"><div class="bubble" role="tooltip"><b>ההודעה שתישלח</b>{esc(wa_msg)}</div><a class="wbtn" href="{C.wa(wa_msg)}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>דברו איתי בוואטסאפ<small>ישר אליי, בלי טפסים</small></span></a></div>
    </div>
    <div class="proof"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5.0</b> בגוגל · <b>100+</b> לקוחות מלווים</span></div>
  </div>
  <div class="visual">
    <div class="panel"><img class="portrait" src="/assets/img/tico-fullbody.webp" width="547" height="1091" alt="צ'יקו זוויבל, יועץ משכנתאות ואדריכל המשכנתאות" fetchpriority="high"></div>
    <div class="sim"><h2>כמה אפשר לחסוך?</h2>
      <div class="big"><span id="mo">500</span><small>₪ לחודש</small></div>
      <div class="row"><label for="loan">יתרת המשכנתה</label><output id="loanOut" for="loan"></output></div>
      <input id="loan" type="range" min="300000" max="3000000" step="50000" value="1200000">
      <div class="row"><label for="diff">הפרש ריבית</label><output id="diffOut" for="diff"></output></div>
      <input id="diff" type="range" min="0.2" max="1.5" step="0.05" value="0.5">
      <div class="fine">הערכה גסה להמחשה בלבד. הבדיקה האמיתית נעשית על דוח היתרות שלכם.</div></div>
  </div>
</section>'''

    paths = f'''<section class="sec" id="paths"><div class="sec-head"><div class="kicker">כל המסלולים</div><h2 class="h2">ארבעה דרכים <em>להתחיל</em></h2>
<p class="lede">כל תהליך פיננסי הוא שונה. בחרו את המסלול שהכי מתאים למצב שלכם, ונתחיל משם.</p></div>
<div class="cards">
<a class="xcard" href="/refinance/"><h3>מיחזור משכנתה</h3><p>יש לכם משכנתה קיימת ואתם רוצים לבדוק אם אפשר לשפר תנאים ולחסוך? בדיקה חינם תוך 24 שעות.</p><span class="go">בדקו כדאיות מיחזור {C.ARROW}</span></a>
<a class="xcard" href="/upgraders/"><h3>משפרי דיור</h3><p>מוכרים דירה וקונים דירה גדולה יותר? נבנה את תזמון המימון והגישור בין שתי העסקאות.</p><span class="go">תכננו את המעבר {C.ARROW}</span></a>
<a class="xcard" href="/investors/"><h3>משקיעי נדל"ן</h3><p>בונים תיק נדל"ן ורוצים למקסם תשואה עם מבנה מימון חכם? ליווי אישי לכל נכס.</p><span class="go">בנו את האסטרטגיה שלכם {C.ARROW}</span></a>
<a class="xcard" href="/br/"><h3>Comprar imóvel em Israel</h3><p>Você mora no Brasil e quer comprar um imóvel em Israel? Consultoria completa, 100% à distância.</p><span class="go">Saiba mais {C.ARROW}</span></a>
</div></section>'''

    process = '''<section class="process" id="process"><div class="kicker">התהליך</div><h2 class="h2">שלושה צעדים, <em>ואני אצלכם</em></h2>
<p class="lede">אתם לא צריכים להבין ריביות כדי להתחיל. אני מלווה מהשיחה הראשונה ועד החתימה בבנק.</p>
<div class="steps"><div class="step"><div class="n">1</div><h3>משאירים פרטים</h3><p>מילוי קצר, בלי עלות ובלי התחייבות.</p><span class="t">30 שניות</span></div>
<div class="step"><div class="n">2</div><h3>מקבלים מה שצריך להכין</h3><p>אם צריך מסמכים, אשלח רשימה קצרה ולינק נוח. ישר לנייד או בוואטסאפ.</p><span class="t">דקה</span></div>
<div class="step"><div class="n">3</div><h3>ניתוח מלא ממני</h3><p>אני בודק את התמהיל ומחזיר לכם תמונה ברורה.</p><span class="t">תוך 24 שעות</span></div></div></section>'''

    bens = '''<section class="sec" id="why"><div class="sec-head"><div class="kicker">למה אנחנו?</div><h2 class="h2">למה לבדוק <em>איתנו?</em></h2></div>
<div class="bens"><div class="ben"><h3>מומחיות אנושית</h3><p>ליווי אישי שמזהה הזדמנויות שאלגוריתם לא רואה.</p></div>
<div class="ben"><h3>100% אובייקטיביות</h3><p>עובדים בשבילכם, לא בשביל הבנק.</p></div>
<div class="ben"><h3>חיסכון משמעותי</h3><p>תכנון נכון שחוזר לכיס שלכם לאורך שנים.</p></div>
<div class="ben"><h3>פרטיות מלאה</h3><p>סודיות מוחלטת בכל שלב בתהליך.</p></div></div></section>'''

    blog = f'''<section class="sec" id="blog"><div class="sec-head"><div class="kicker">ידע אסטרטגי</div><h2 class="h2">מהבלוג</h2>
<p class="lede">טיפים ומדריכים שיעזרו לכם לקבל החלטות פיננסיות נכונות.</p></div>
<div class="posts">
<a class="post" href="/blog/refinance-timing/"><span class="tag">מאמר</span><h3>מתי באמת כדאי למחזר משכנתה?</h3><p>הסימנים שאומרים שהגיע הזמן לבדוק מחדש את התנאים שלכם.</p><span class="more">קראו עוד {C.ARROW}</span></a>
<a class="post" href="/blog/apartment-not-selling/"><span class="tag">מאמר</span><h3>מה עושים אם הדירה לא נמכרת בזמן?</h3><p>תרחישי גיבוי שכל משפר דיור צריך להכיר.</p><span class="more">קראו עוד {C.ARROW}</span></a>
<a class="post" href="/blog/leverage-guide/"><span class="tag">מאמר</span><h3>מינוף הוא לא הימור</h3><p>עקרונות לבניית מבנה מימון נכון למשקיעים.</p><span class="more">קראו עוד {C.ARROW}</span></a>
</div><div class="more-row"><a class="sbtn" href="/blog/">לכל המאמרים {C.ARROW}</a></div></section>'''

    band = band_section('מקרה אמיתי: ₪100,000 נחסכו על משכנתה של ₪230,000.',
                        [('100+', 'לקוחות שעברו תהליך מוצלח'), ('5.0', 'דירוג לקוחות בגוגל'), ('24 שעות', 'לניתוח ראשוני')],
                        f'<a class="pbtn inv lg" href="#finder">בדקו את המשכנתה שלי {C.CHIP}</a>')

    faq = faq_section('שאלות נפוצות', 'לפני שמתחילים, <em>כמה תשובות</em>', [
        ('כמה עולה הבדיקה הראשונית?', 'הבדיקה הראשונית בחינם ובלי התחייבות. תקבלו תמונה ברורה לפני שמחליטים אם להתקדם.'),
        ('כמה זמן לוקח לקבל תשובה?', 'אחרי שמעבירים את הפרטים, הניתוח מגיע תוך 24 שעות.'),
        ('מה צריך להכין?', 'תלוי בתהליך. במיחזור, בעיקר דוח יתרות לסילוק מהבנק. בשאר התהליכים נתחיל משיחה, ואגיד לכם בדיוק מה כדאי להכין.'),
        ('עובדים מול כל הבנקים?', 'כן. התהליך מתאים לכל הבנקים בישראל.'),
        ('אני גר בחו"ל. אפשר לרכוש נכס בישראל?', 'כן. יש ליווי מלא מרחוק לברזילאים שרוצים לרכוש נכס בישראל, בפורטוגזית.')])

    body = '\n'.join([hero, banks_strip('he'), wizard('he'), paths, process, reviews_section('he', reviews), meet_section('he'), bens,
                      community_section('he'), refer_section('he'), band, blog, faq, close_section('he')])
    scripts = '<script src="/assets/js/home.js" defer></script>\n<script src="/assets/js/wizard.js" defer></script>'
    write('index.html', document('he', head, body, scripts))


def build_br():
    src = read('br/index.html') if 'tico.css' not in read('br/index.html') else git_show('br/index.html')
    head = clean_head(src)
    reviews = parse_reviews()
    wa_msg = 'Olá Tico! Vim do site e quero saber mais sobre comprar um imóvel em Israel.'
    hero = f'''<section class="hero">
  <div class="copy">
    <div class="kicker" data-greet>Consultoria para brasileiros que vivem no Brasil</div>
    <h1><span class="l1">Comprar um imóvel em Israel</span><span class="l2">é possível.</span></h1>
    <p class="sub">Mesmo morando no Brasil. Você não precisa estar em Israel para dar o primeiro passo. Cuido de todo o processo com você: financiamento, advogado, corretor e muito mais, para fechar seu imóvel à distância, com segurança e confiança total.</p>
    <div class="cta">
      <a class="pbtn lg" href="#finder">Comece por aqui {C.CHIP_DOWN}</a>
      <div class="wawrap"><div class="bubble" role="tooltip"><b>Mensagem que será enviada</b>{esc(wa_msg)}</div><a class="wbtn" href="{C.wa(wa_msg)}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>Falar agora no WhatsApp<small>Direto comigo, sem formulários</small></span></a></div>
    </div>
    <div class="proof"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5.0</b> no Google · <b>100+</b> clientes atendidos · <b>100%</b> à distância</span></div>
    <p class="tel"><a class="tel" href="mailto:{C.EMAIL}">ou envie um e-mail: <b>{C.EMAIL}</b></a></p>
  </div>
  <div class="visual">
    <div class="panel"><img class="portrait" src="/assets/img/tico-fullbody.webp" width="547" height="1091" alt="Tico Zveibel, TICO FINANCE" fetchpriority="high"></div>
    <div class="sim"><h2>Financiamento no exterior</h2><div class="big">50%<small>do valor do imóvel</small></div>
      <p class="fine2">75% para quem tem cidadania israelense. Cada caso é analisado individualmente durante a consultoria.</p></div>
  </div>
</section>'''

    net = f'''<section class="sec" id="network"><div class="sec-head"><div class="kicker">Muito além do financiamento</div><h2 class="h2">Uma rede completa de profissionais, <em>cuidando de cada etapa</em></h2>
<p class="lede">Comprar um imóvel em outro país parece complicado. Até você ter as pessoas certas ao seu lado. Eu conecto você a tudo o que precisa para fechar o negócio, sem sair de casa.</p></div>
<div class="cards">
<div class="xcard"><h3>Financiamento sob medida</h3><p>Negociação direta com os bancos em Israel para as melhores condições de financiamento para residentes no exterior: até 50% do valor do imóvel (75% para quem tem cidadania israelense).</p></div>
<div class="xcard"><h3>Advogado especializado</h3><p>Conexão com advogados de confiança que revisam cada contrato e protegem seus interesses do início ao fim do processo.</p></div>
<div class="xcard"><h3>Corretor parceiro</h3><p>Indicação de corretores que conhecem o mercado local e ajudam a encontrar o imóvel certo para o seu objetivo: moradia, investimento ou renda.</p></div>
<div class="xcard"><h3>Grupos de compra</h3><p>Acesso a oportunidades exclusivas em grupos de compra (<bdi dir="rtl">קבוצת רכישה</bdi>), com preços abaixo do mercado e planejamento em conjunto com outros compradores.</p></div>
</div></section>'''

    how = f'''<section class="process" id="process"><div id="how"></div><div class="kicker">Como funciona</div><h2 class="h2">Um processo claro, <em>mesmo à distância</em></h2>
<div class="steps s4">
<div class="step"><div class="n">1</div><h3>Conversa inicial</h3><p>Marcamos uma videochamada para entender seu objetivo, seu orçamento e sua situação financeira, sem compromisso.</p></div>
<div class="step"><div class="n">2</div><h3>Plano personalizado</h3><p>Analisamos seu perfil e montamos um plano de financiamento e compra, adaptado à sua realidade como residente no exterior.</p></div>
<div class="step"><div class="n">3</div><h3>Conexão com a equipe certa</h3><p>Apresento você ao advogado, corretor e demais profissionais necessários, todos coordenados por mim, em um só lugar.</p></div>
<div class="step"><div class="n">4</div><h3>Acompanhamento até as chaves</h3><p>Do sinal à assinatura final, acompanho cada etapa com você, sem que você precise pisar em Israel até a entrega das chaves.</p></div></div>
<div class="cta-row"><a class="pbtn" href="{C.wa('Olá Tico! Quero entender como funciona o processo de compra de imóvel em Israel.')}" target="_blank" rel="noopener">Quero entender meu processo {C.CHIP}</a></div></section>'''

    band = band_section('Consultoria 100% remota, do primeiro passo às chaves.',
                        [('100+', 'clientes atendidos'), ('100%', 'à distância'), ('3+ anos', 'de experiência no mercado imobiliário israelense')],
                        f'<a class="pbtn inv lg" href="{C.wa("Olá Tico! Quero saber se posso comprar um imóvel em Israel.")}" target="_blank" rel="noopener">Quero saber se posso comprar em Israel {C.CHIP}</a>')

    faq = faq_section('Perguntas frequentes', 'Ainda tem dúvidas? <em>Vamos esclarecer</em>', [
        ('Preciso estar em Israel para comprar um imóvel?', 'Não. A maior parte do processo pode ser conduzida remotamente, incluindo abertura de conta, financiamento e assinatura de documentos com procuração. Uma viagem pode ser útil em momentos pontuais, mas não é obrigatória.'),
        ('Quanto posso financiar sendo residente no exterior?', 'Como residente no exterior sem cidadania israelense, o financiamento máximo costuma ser de até 50% do valor do imóvel. Com cidadania israelense, pode chegar a 75%. Cada caso é analisado individualmente durante a consultoria.'),
        ('Quais documentos preciso enviar do Brasil?', 'Em geral: comprovante de renda, extratos bancários, documento de identidade e comprovante de residência. Envio a lista completa e ajudo a organizar tudo durante o processo.'),
        ('Como funciona o pagamento e a transferência de valores?', 'Trabalhamos com os canais corretos para transferências internacionais, sempre com orientação sobre taxas, impostos e a forma mais segura de movimentar seu dinheiro entre os dois países.'),
        ('A consultoria inicial tem custo?', 'Não. A primeira conversa é gratuita e sem compromisso. É o momento de entender se faz sentido para você.')])

    final = f'''<section class="final"><div><h2>Seu imóvel em Israel está mais perto do que você imagina, mesmo estando no Brasil</h2>
<p>Com a TICO FINANCE, você ganha um parceiro de confiança e uma rede completa de profissionais, com a tranquilidade de saber que cada etapa está sendo cuidada, onde quer que você esteja. Vamos conversar?</p>
<div class="acts"><a class="pbtn inv lg" href="{C.wa("Olá Tico! Vim do site e quero começar minha consultoria.")}" target="_blank" rel="noopener">Falar no WhatsApp {C.CHIP}</a><a class="tel" href="mailto:{C.EMAIL}">{C.EMAIL}</a></div></div>
<img src="/assets/img/tico-halfbody.webp" width="400" height="400" alt="Tico Zveibel - TICO FINANCE" loading="lazy"></section>'''

    body = '\n'.join([hero, banks_strip('pt'), wizard('pt'), net, how, reviews_section('pt', reviews), meet_section('pt'), community_section('pt'), refer_section('pt'), band, faq, final])
    scripts = '<script src="/assets/js/wizard.js" defer></script>'
    write('br/index.html', document('pt', head, body, scripts))



# ---------------------------------------------------------------------------------------------
# landing pages (upgraders, investors share one structure; refinance has its own tools)
def _txt(el):
    return el.get_text(' ', strip=True) if el else ''


def _inner(el):
    return ''.join(str(c) for c in el.children).strip() if el else ''


def _hero_h1(h1):
    """Split 'start <em>emphasis</em>' into the two-line display headline."""
    em = h1.find('em')
    emt = _txt(em)
    full = _txt(h1)
    first = full.replace(emt, '').strip() if emt else full
    return first, emt


def _steps(sec, cls='steps', with_badges=False):
    out = []
    for st in sec.select('.step'):
        n = _txt(st.select_one('.step-num'))
        h = _txt(st.find('h3')); p = _txt(st.find('p'))
        b = st.select_one('.client-badge')
        badge = f'<span class="badge">{esc(re.sub(r"[^\w\s]", "", _txt(b)).strip())}</span>' if (b and with_badges) else ''
        out.append(f'<div class="step"><div class="n">{n}</div>{badge}<h3>{esc(h)}</h3><p>{esc(p)}</p></div>')
    return f'<div class="{cls}">' + ''.join(out) + '</div>'


def _cards(sec, c='cards'):
    items = []
    for cd in sec.select('.network-card'):
        items.append(f'<div class="xcard"><h3>{esc(_txt(cd.find("h3")))}</h3><p>{esc(_txt(cd.find("p")))}</p></div>')
    return f'<div class="{c}">' + ''.join(items) + '</div>'


def _faq(sec):
    return [(esc(_txt(d.find('summary'))), esc(_txt(d.find('p')))) for d in sec.select('details')]


def build_landing(slug, source_id=None, form_text=None):
    from bs4 import BeautifulSoup
    src = git_show(f'{slug}/index.html')
    soup = BeautifulSoup(src, 'lxml')
    head = clean_head(src)
    reviews = parse_reviews()
    hero = soup.find('section', class_='hero')
    eyebrow = _txt(hero.select_one('.hero-eyebrow')).lstrip('✦ ').strip()
    h1 = hero.find('h1'); first, emt = _hero_h1(h1)
    sub = _txt(hero.select_one('.hero-sub'))
    wa_href = hero.select_one('a.hero-btn')['href']
    cta_label = re.sub(r'ב-?WhatsApp', 'בוואטסאפ', _txt(hero.select_one('a.hero-btn')))
    about = soup.find('section', class_='about')
    a_lbl = _txt(about.select_one('.section-label')); a_h = _txt(about.select_one('.section-title'))
    a_ps = ''.join(f'<p>{esc(_txt(p))}</p>' for p in about.select('p'))
    a_cta = about.select_one('a.cta-strip'); a_cta_txt = _txt(a_cta).rstrip('→ ').strip(); a_cta_href = a_cta['href']
    net = soup.find('section', class_='network')
    n_lbl = _txt(net.select_one('.section-label')); n_h = _txt(net.select_one('.section-title')); n_sub = _txt(net.select_one('.section-sub'))
    how = soup.find('section', class_='how')
    h_lbl = _txt(how.select_one('.section-label')); h_h = _txt(how.select_one('.section-title'))
    how_cta = how.select_one('a.cta-strip')
    proc = soup.find('section', class_='process')
    faq = soup.find('section', class_='faq')
    fin = soup.find('section', class_='final-cta')
    f_h = _txt(fin.find('h2')); f_p = _txt(fin.find('p')); f_wa = fin.select_one('a.btn-wa')['href']

    hero_html = f'''<section class="hero">
  <div class="copy">
    <div class="kicker">{esc(eyebrow)}</div>
    <h1 class="hx">{esc(first)} <em>{esc(emt)}</em></h1>
    <p class="sub">{esc(sub)}</p>
    <div class="hero-cta2"><a class="pbtn lg" href="#form">השאירו פרטים {C.CHIP_DOWN}</a>
      <a class="wbtn" href="{wa_href}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>{esc(cta_label)}<small>ישר אליי, בלי טפסים</small></span></a></div>
    <div class="proof"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5.0</b> בגוגל · <b>100+</b> לקוחות מלווים · <a class="tel" href="tel:{C.PHONE_LABEL.replace("-", "")}"><b>{C.PHONE_LABEL}</b></a></span></div>
  </div>
  <div class="visual"><div class="panel"><img class="portrait" src="/assets/img/tico-fullbody.webp" width="547" height="1091" alt="צ'יקו זוויבל, יועץ משכנתאות ואדריכל המשכנתאות" fetchpriority="high"></div></div>
</section>'''

    about_html = f'''<section class="sec" id="about"><div class="split one"><div class="copy"><div class="kicker">{esc(a_lbl)}</div><h2 class="h2">{esc(a_h)}</h2>{a_ps}
<div class="cta-row"><a class="pbtn" href="{a_cta_href}" target="_blank" rel="noopener">{esc(a_cta_txt)} {C.CHIP}</a></div></div></div></section>'''

    net_html = f'<section class="sec" id="{net.get("id")}"><div class="sec-head"><div class="kicker">{esc(n_lbl)}</div><h2 class="h2">{esc(n_h)}</h2><p class="lede">{esc(n_sub)}</p></div>{_cards(net)}</section>'
    how_html = (f'<section class="sec" id="how"><div class="sec-head"><div class="kicker">{esc(h_lbl)}</div><h2 class="h2">{esc(h_h)}</h2></div>{_steps(how, "steps s4")}'
                f'<div class="cta-row"><a class="pbtn" href="{how_cta["href"]}" target="_blank" rel="noopener">{esc(_txt(how_cta).rstrip("→ ").strip())} {C.CHIP}</a></div></section>')
    proc_html = (f'<section class="sec" id="process"><div class="sec-head"><div class="kicker">{esc(_txt(proc.select_one(".section-label")))}</div><h2 class="h2">{esc(_txt(proc.select_one(".section-title")))}</h2>'
                 f'<p class="lede">{esc(_txt(proc.select_one(".process-intro")))}</p></div>{_steps(proc, "steps s4", with_badges=True)}</section>')
    faq_html = faq_section(esc(_txt(faq.select_one('.section-label'))), esc(_txt(faq.select_one('.section-title'))), _faq(faq))

    form_html = f'''<section class="sec formsec" id="form"><div class="card"><h2>השאירו פרטים ונחזור אליכם</h2><p class="sub2">נבחן את המצב שלכם ונחזור עם המלצה מותאמת אישית</p>
<form id="leadForm" novalidate data-source="{source_id or slug}">
<div class="fieldrow"><div class="fld"><label for="full_name">שם מלא</label><input type="text" id="full_name" autocomplete="name" placeholder="ישראל ישראלי"><div class="err" id="nmE"></div></div>
<div class="fld"><label for="phone">מספר טלפון</label><input type="tel" id="phone" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="050-0000000"><div class="err" id="phE"></div></div></div>
<label class="consent"><input type="checkbox" id="consent"><span>אני מאשר/ת קבלת מידע ממומחי TICO FINANCE בהתאם ל<a href="/privacy.html">מדיניות הפרטיות</a></span></label>
<button class="sbm" id="sub" data-s="idle" type="submit"><span class="l">השאירו פרטים ואחזור אליכם</span><span class="ld"><svg class="spin" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9" opacity=".3"/><path d="M12 3a9 9 0 0 1 9 9"/></svg></span><span class="ok"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path class="ck-draw" d="M5 12l5 5 9-10"/></svg>נשלח</span></button>
<div class="errbox" id="errbox" role="alert"></div></form>
<p class="trust">המידע מאובטח ומשמש רק ליצירת קשר</p>
<div class="alt-wa"><a class="wbtn" href="{wa_href}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>מעדיפים לדבר קודם? וואטסאפ<small>ישר אליי</small></span></a></div></div></section>'''

    final = (f'<section class="final"><div><h2>{esc(f_h)}</h2><p>{esc(f_p)}</p><div class="acts"><a class="pbtn inv lg" href="{f_wa}" target="_blank" rel="noopener">דברו איתי בוואטסאפ {C.CHIP}</a>'
             f'<a class="tel" href="tel:{C.PHONE_LABEL.replace("-", "")}">{C.PHONE_LABEL}</a></div></div><img src="/assets/img/tico-halfbody.webp" width="400" height="400" alt="צ\'יקו זוויבל - TICO FINANCE" loading="lazy"></section>')

    body = '\n'.join([hero_html, banks_strip('he'), about_html, net_html, how_html, proc_html, reviews_section('he', reviews), faq_html, form_html, refer_section('he'), final])
    write(f'{slug}/index.html', document('he', head, body, '<script src="/assets/js/lead-form.js" defer></script>'))


def build_upgraders():
    build_landing('upgraders')


def build_investors():
    build_landing('investors')



def build_refinance():
    from bs4 import BeautifulSoup
    src = git_show('refinance/index.html')
    head = clean_head(src)
    reviews = parse_reviews()
    wa_msg = "היי צ'יקו! הגעתי מהאתר ורוצה לבדוק אם כדאי לי למחזר את המשכנתה."
    hero = f'''<section class="hero">
  <div class="copy">
    <div class="kicker">ליווי מקצועי למיחזור משכנתה</div>
    <h1 class="hx">בעידן של AI ודיגיטל, אין כמו יועץ <em>אמיתי</em> שיבדוק את המשכנתה שלך</h1>
    <p class="sub">תהליך של 2 דקות. ניתוח אנושי מקצועי. בלי עלויות מראש.</p>
    <div class="hero-cta2"><a class="pbtn lg" href="#form">אני רוצה לבדוק עכשיו {C.CHIP_DOWN}</a>
      <div class="wawrap"><div class="bubble" role="tooltip"><b>ההודעה שתישלח</b>{esc(wa_msg)}</div><a class="wbtn" href="{C.wa(wa_msg)}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>או כתבו לי בוואטסאפ<small>ישר אליי, בלי טפסים</small></span></a></div></div>
    <div class="proof"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5.0</b> בגוגל · <a class="tel" href="tel:{C.PHONE_LABEL.replace("-", "")}">או התקשרו: <b>{C.PHONE_LABEL}</b></a></span></div>
  </div>
  <div class="visual"><div class="panel"><img class="portrait" src="/assets/img/tico-fullbody.webp" width="547" height="1091" alt="צ'יקו זוויבל, אדריכל המשכנתאות" fetchpriority="high"></div>
    <div class="sim"><h2>ייעוץ אנושי מקצועי</h2><div class="big">₪847<small>חיסכון ממוצע לחודש</small></div><p class="fine2">100% ניתוח אנושי. TICO FINANCE · אדריכל המשכנתאות</p></div></div>
</section>'''

    how = '''<section class="sec" id="how"><div class="sec-head"><div class="kicker">התהליך</div><h2 class="h2">איך זה <em>עובד?</em></h2><p class="lede">תהליך פשוט שייקח פחות מ-2 דקות וייתן לך שקט נפשי</p></div>
<div class="steps s4"><div class="step"><div class="n">1</div><h3>בחר את הבנק</h3><p>בחר את הבנק שבו מתנהלת המשכנתא שלך מרשימת הבנקים.</p></div>
<div class="step"><div class="n">2</div><h3>העלה דוח יתרות</h3><p>העלה צילום או סריקה של דוח יתרות המשכנתא העדכני מהבנק.</p></div>
<div class="step"><div class="n">3</div><h3>ניתוח אנושי</h3><p>המומחים שלנו מנתחים את התמהיל ומזהים פוטנציאל חיסכון אמיתי.</p></div>
<div class="step"><div class="n">4</div><h3>חיסכון בפועל</h3><p>קבל המלצות מפורטות וליווי צמוד עד להשגת התנאים הטובים ביותר.</p></div></div></section>'''

    banks = [('leumi', 'בנק לאומי'), ('mizrahi', 'מזרחי טפחות'), ('hapoalim', 'בנק הפועלים'), ('discount', 'בנק דיסקונט'),
             ('jerusalem', 'בנק ירושלים'), ('mercantile', 'בנק מרכנתיל'), ('fibi', 'הבנק הבינלאומי')]
    ids = {'mizrahi': 'mizrahi', 'leumi': 'leumi', 'hapoalim': 'hapoalim', 'discount': 'discount', 'jerusalem': 'jerusalem', 'mercantile': 'mercantile', 'fibi': 'fibi'}
    cards = ''.join(f'<button class="bank-card" type="button" data-bank="{k}" onclick="openBankModal(\'{k}\', this)"><span class="bank-logo"><img src="/assets/img/banks/{k}.webp" alt="{n}" width="120" height="37" loading="lazy"></span><span class="bn">{n}</span><span class="bl">איך מוציאים דוח?</span></button>' for k, n in banks)
    cards += '<button class="bank-card" type="button" data-bank="other" onclick="openBankModal(\'other\', this)"><span class="bank-logo other" aria-hidden="true">' + C.ARROW.replace('<path d="M19 12H5M11 6l-6 6 6 6"/>', '<path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/>') + '</span><span class="bn">בנק אחר</span><span class="bl">איך מוציאים דוח?</span></button>'
    banks_html = f'''<section class="sec" id="banks"><div class="sec-head"><div class="kicker">הבנקים</div><h2 class="h2">בחר את <em>הבנק שלך</em></h2><p class="lede">לחצו על הבנק לעמוד הורדת דוח יתרות, ואז חזרו להעלות אותו.</p></div>
<div class="banks-grid">{cards}</div></section>
<div class="modal" id="bank-modal" role="dialog" aria-modal="true" aria-label="איך מוציאים דוח יתרות">
  <div class="modal-in"><button class="modal-x" type="button" onclick="closeModal()" aria-label="סגירה">&times;</button><div id="modal-content"></div>
    <div class="modal-acts"><a class="pbtn sm" id="modal-link" href="#" target="_blank" rel="noopener" onclick="closeModal()">כניסה לאזור האישי {C.CHIP}</a>
    <button class="sbtn" type="button" onclick="closeModalAndScroll()">המשך למילוי הטופס</button></div></div></div>'''

    calc = f'''<section class="sec" id="calculator"><div class="sec-head"><div class="kicker">מחשבון חיסכון</div><h2 class="h2">כמה תוכל <em>לחסוך במשכנתה?</em></h2>
<p class="lede">הכנס את נתוני המסלולים שלך וקבל הערכת חיסכון פוטנציאלי, בחינם ובשניות</p><p class="sec-note">מבוסס על ריביות שוק ממוצעות · עודכן 04/08/2026</p></div>
<div class="calc"><div id="tracks-container"></div>
<button class="sbtn wide" type="button" id="add-track-btn" onclick="addTrack()">+ הוסף מסלול נוסף</button>
<button class="pbtn lg wide" type="button" onclick="calculateSavings()">חשב פוטנציאל חיסכון {C.CHIP}</button>
<div id="calc-results" style="display:none;margin-top:28px"></div></div></section>'''

    form = f'''<section class="sec formsec" id="form"><div class="card"><h2>העלאת דוח ופרטי קשר</h2><p class="sub2">המידע שלך מאובטח ומשמש אך ורק לניתוח מקצועי</p>
<iframe id="embedded-form-iframe" class="snpv" src="https://www.snpv.co.il/public/embedded_pages/Leads_balance_report/preview/d66f08c6-e409-4e59-8c4c-e577273cd516?source=website_refinance" scrolling="no" frameborder="0" title="טופס בדיקת מיחזור משכנתה"></iframe>
<div class="alt-wa"><a class="wbtn" href="{C.wa(wa_msg)}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>מעדיפים לדבר קודם? וואטסאפ<small>ישר אליי</small></span></a></div></div></section>'''

    about = f'''<section class="sec" id="about"><div class="split one"><div class="copy"><div class="kicker">נעים להכיר</div><h2 class="h2">צ'יקו, <em>האדריכל הפיננסי שלך</em></h2>
<p>אני מאמין שמשכנתה היא אף פעם לא רק "השוואת ריביות", אלא <strong>ארכיטקטורה פיננסית שלמה</strong>. כמומחה למשקיעי נדל"ן ומשפרי דיור, אני מסתכל על הפאזל המלא של החיים והעסקים שלך, ובונה עבורך את המסלול המדויק ביותר, <strong>בהתאמה אישית מלאה</strong>.</p>
<p>אני מתמחה גם ב<strong>מיחזור משכנתאות</strong>: בדיקה מחדש של התנאים, התאמה לריביות השוק הנוכחיות ולמצב האישי שלך, והכל עם מטרה אחת: שהמשכנתה תעבוד בשבילך. מיחזור נכון יכול לחסוך עשרות ואף מאות אלפי שקלים.</p>
<p><strong>כי בלי תכנון, אין כלום.</strong></p>
<div class="cta-row"><a class="pbtn" href="{C.wa()}" target="_blank" rel="noopener">בוא נדבר בוואטסאפ {C.CHIP}</a></div></div></div></section>'''

    bens = '''<section class="sec" id="benefits"><div class="sec-head"><div class="kicker">למה אנחנו?</div><h2 class="h2">למה לבדוק <em>איתנו?</em></h2></div>
<div class="bens"><div class="ben"><h3>מומחיות אנושית מול AI</h3><p>בניגוד לאלגוריתמים קרים, המומחים שלנו מזהים הזדמנויות במצבים מורכבים ומבינים את הצרכים האישיים שלך.</p></div>
<div class="ben"><h3>100% אובייקטיביות</h3><p>אנחנו עובדים בשבילך, לא בשביל הבנק. האינטרס היחיד שלנו הוא למצוא עבורך את החיסכון המקסימלי.</p></div>
<div class="ben"><h3>חיסכון ממוצע של ₪847 בחודש</h3><p>לאורך חיי המשכנתא מדובר במאות אלפי שקלים שחוזרים לכיס שלך.</p></div>
<div class="ben"><h3>פרטיות וביטחון מלא</h3><p>הנתונים הפיננסיים שלך הם הקודש שלנו. הצפנה מתקדמת וסודיות מוחלטת בכל שלב.</p></div></div></section>'''

    final = (f'<section class="final"><div><h2>המשכנתה שלך יכולה לעבוד קשה יותר בשבילך</h2><p>שלחו דוח יתרות או כתבו לי ישר, ואחזור אליכם עם תמונה ברורה תוך 24 שעות.</p>'
             f'<div class="acts"><a class="pbtn inv lg" href="#form">בדיקה חינם {C.CHIP}</a><a class="tel" href="tel:{C.PHONE_LABEL.replace("-", "")}">{C.PHONE_LABEL}</a></div></div>'
             f'<img src="/assets/img/tico-halfbody.webp" width="400" height="400" alt="צ\'יקו זוויבל - TICO FINANCE" loading="lazy"></section>')

    body = '\n'.join([hero, banks_strip('he'), how, banks_html, calc, form, reviews_section('he', reviews), about, bens, refer_section('he'), final])
    scripts = '<script src="/assets/js/refinance.js" defer></script>\n<script src="/assets/js/snpv.js" defer></script>'
    write('refinance/index.html', document('he', head, body, scripts))



# ---------------------------------------------------------------------------------------------
# content pages: blog index, articles, legal documents, thank-you
def _lang_of(soup):
    return 'pt' if (soup.html.get('lang') or '').lower().startswith('pt') else 'he'


def build_blog_index():
    from bs4 import BeautifulSoup
    src = git_show('blog/index.html')
    soup = BeautifulSoup(src, 'lxml')
    head = clean_head(src)
    hero = soup.find('section', class_='hero')
    k = _txt(hero.select_one('.hero-eyebrow')).lstrip('✦ ').strip()
    t = _txt(hero.find('h1')); sub = _txt(hero.find('p'))
    blocks = []
    for cb in soup.select('.cat-block'):
        h = _txt(cb.find('h2')); a = cb.select_one('.cat-head a')
        cards = ''.join(f'<a class="post" href="{c["href"]}"><span class="tag">{esc(_txt(c.select_one(".post-badge")))}</span><h3>{esc(_txt(c.find("h3")))}</h3><p>{esc(_txt(c.find("p")))}</p><span class="more">{esc(_txt(c.select_one(".read-more")).rstrip("←→ ").strip())} {C.ARROW}</span></a>' for c in cb.select('a.post-card'))
        link = f'<a class="sbtn" href="{a["href"]}">{esc(_txt(a).rstrip("←→ ").strip())} {C.ARROW}</a>' if a else ''
        blocks.append(f'<section class="sec cat"><div class="cat-h"><h2 class="h2s" dir="auto">{esc(h)}</h2>{link}</div><div class="posts">{cards}</div></section>')
    body = (f'<div class="phead"><div class="kicker">{esc(k)}</div><h1 class="hx h1page">{esc(t)}</h1><p class="lede">{esc(sub)}</p></div>' + '\n'.join(blocks) + close_section('he'))
    write('blog/index.html', document('he', head, body))


def build_article(slug):
    from bs4 import BeautifulSoup
    path = f'blog/{slug}/index.html'
    src = git_show(path)
    soup = BeautifulSoup(src, 'lxml')
    lang = _lang_of(soup); he = lang == 'he'
    head = clean_head(src)
    hero = soup.find(class_='art-hero')
    badge = _txt(hero.select_one('.art-badge')); h1 = _txt(hero.find('h1')); meta = _txt(hero.select_one('.art-meta'))
    main = soup.find('main')
    parts = []
    cta = None
    for ch in list(main.children):
        if getattr(ch, 'name', None) is None:
            continue
        cls = ch.get('class') or []
        if 'cta-block' in cls:
            cta = ch; continue
        if 'art-links' in cls:
            continue
        if 'notice-box' in cls:
            parts.append(f'<div class="note">{_inner(ch)}</div>'); continue
        parts.append(str(ch))
    inner = '\n'.join(parts)
    inner = re.sub(r'class="art-lede"', 'class="art-lede"', inner)
    ch3 = _txt(cta.find('h3')) if cta else ''; cp = _txt(cta.find('p')) if cta else ''
    cwa = cta.find('a')['href'] if cta and cta.find('a') else C.wa()
    cbtn = ('דברו איתי בוואטסאפ' if he else 'Falar no WhatsApp')
    links = []
    for a in soup.select('.art-links a'):
        label = re.sub(r'^[^\w\u0590-\u05FF]+', '', _txt(a)).rstrip('←→ ').strip()
        links.append(f'<a class="sbtn" href="{a["href"]}">{esc(label)} {C.ARROW}</a>')
    crumbs = (f'<nav class="crumbs" aria-label="breadcrumbs"><a href="{"/" if he else "/br/"}">{"בית" if he else "Início"}</a><span>/</span><a href="/blog/">{"בלוג" if he else "Blog"}</a></nav>')
    pill = re.sub(r'^[^A-Za-z\u0590-\u05FF]+', '', badge)
    art = (f'{crumbs}<article class="art"><header class="art-hero"><span class="tagpill">{esc(pill)}</span><h1>{esc(h1)}</h1><div class="art-meta">{esc(meta)}</div></header>'
           f'{inner}'
           f'<div class="art-cta"><h3>{esc(ch3)}</h3><p>{esc(cp)}</p><a class="pbtn inv lg" href="{cwa}" target="_blank" rel="noopener">{cbtn} {C.CHIP}</a></div>'
           f'<div class="art-links">{"".join(links)}</div></article>')
    body = art + refer_section(lang)
    write(path, document(lang, head, body))


def build_doc(path):
    from bs4 import BeautifulSoup
    src = git_show(path)
    soup = BeautifulSoup(src, 'lxml')
    lang = _lang_of(soup)
    head = clean_head(src)
    h1 = _txt(soup.select_one('.legal-hero h1'))
    main = soup.find('main')
    upd = main.find('p', class_='updated'); upd_t = _txt(upd) if upd else ''
    bodyel = main.find(class_='legal-body') or main
    inner = _inner(bodyel)
    body = f'<article class="doc"><h1>{esc(h1)}</h1><p class="upd">{esc(upd_t)}</p>{inner}</article>'
    write(path, document(lang, head, body))


def build_thankyou():
    src = git_show('thank-you.html')
    head = clean_head(src)
    body = f'''<section class="ty"><div class="ty-in"><div class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg></div>
<h1 class="hx h1page">הפרטים התקבלו בהצלחה!</h1><p class="lede">תודה שבחרת ב-TICO FINANCE לבחון את המשכנתה שלך. מומחה מטעמנו יצור איתך קשר תוך 24 שעות.</p>
<ol class="tl"><li class="ok"><span class="d"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg></span><div><b>דוח התקבל</b><span class="t">הנתונים הועברו לצוות המומחים שלנו</span></div></li>
<li class="now"><span class="d">2</span><div><b>ניתוח אנושי מקצועי<span class="tag">עכשיו</span></b><span class="t">מומחה יבדוק ויבנה סימולציה מדויקת</span></div></li>
<li><span class="d">3</span><div><b>מענה תוך 24 שעות</b><span class="t">נחזור אליך עם המלצות מפורטות</span></div></li></ol>
<div class="ty-acts"><a class="wbtn" href="{C.wa()}" target="_blank" rel="noopener"><span class="g">{C.WA_GLYPH}</span><span>שאלות? צ'אט ישיר בוואטסאפ<small>ישר אליי</small></span></a><a class="sbtn" href="/">חזרה לדף הבית</a></div>
<div class="sign">צ'יקו</div><a class="reflink" href="/#refer">מכירים עוד מישהו? אפשר להפנות חבר</a></div></section>'''
    write('thank-you.html', document('he', head, body))


def build_articles():
    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, 'blog', '*', 'index.html'))):
        build_article(os.path.basename(os.path.dirname(f)))


def build_docs():
    for p in ['privacy.html', 'terms.html', 'accessibility.html', 'br/privacidade.html', 'br/termos.html']:
        build_doc(p)



def build_lecture():
    from bs4 import BeautifulSoup
    src = git_show('lecture/index.html')
    soup = BeautifulSoup(src, 'lxml')
    head = clean_head(src)
    hero = soup.find('section', class_='hero')
    eb = _txt(hero.select_one('.hero-eyebrow'))
    h1 = hero.find('h1'); first = _txt(h1.contents[0]) if h1.contents else ''
    em = _txt(h1.find('em')); sub = _txt(hero.select_one('.hero-sub'))
    chips = ''.join(f'<li>{esc(_txt(c).lstrip("✓ ").strip())}</li>' for c in hero.select('.benefit-chip'))
    stats = ''.join(f'<div><b>{_inner(i.select_one(".stat-num"))}</b><span>{esc(_txt(i.select_one(".stat-label")))}</span></div>' for i in soup.select('.stat-item'))
    val = soup.find('section', class_='value-section')
    val_ps = []
    for p_ in val.find_all('p'):
        inner = _inner(p_)
        if p_.get('style') and 'warm-light' in p_.get('style'):
            val_ps.append(f'<div class="note big">{inner}</div>')
        else:
            val_ps.append(f'<p>{inner}</p>')
    about = soup.find('div', class_='about-card')
    a_h = _txt(about.find('h3')); a_role = _txt(about.select_one('.role')); a_ps = ''.join(f'<p>{_inner(p_)}</p>' for p_ in about.select('.about-text > p:not(.role)'))
    tags = ''.join(f'<span>{esc(_txt(t))}</span>' for t in about.select('.about-tag'))
    market = soup.find('section', class_='market-section')
    m_cards = ''.join(f'<div class="xcard{" hl" if "highlight" in c.get("class", []) else ""}"><span class="mlabel">{esc(_txt(c.select_one(".label")))}</span><h3>{esc(_txt(c.select_one(".value")))}</h3><p>{esc(_txt(c.select_one(".note")))}</p></div>' for c in market.select('.market-card'))
    secs = soup.find_all('section', class_='section')
    inc, emp, how = secs[0], secs[1], secs[2]
    inc_cards = ''.join(f'<div class="xcard{" hl" if "featured" in c.get("class", []) else ""}"><h3>{esc(_txt(c.find("h3")))}</h3><p>{esc(_txt(c.find("p")))}</p></div>' for c in inc.select('.content-item'))
    emp_steps = ''.join(f'<div class="step"><div class="n">{_txt(e.select_one(".number"))}</div><h3>{esc(_txt(e.find("h3")))}</h3><p>{esc(_txt(e.find("p")))}</p></div>' for e in emp.select('.emp-benefit'))
    how_steps = ''
    for st in how.select('.step'):
        bd = st.select_one('.step-body'); b = bd.select_one('.badge')
        how_steps += f'<div class="step"><div class="n">{_txt(st.select_one(".step-dot"))}</div>{("<span class=badge>" + esc(_txt(b)) + "</span>") if b else ""}<h3>{esc(_txt(bd.find("h3")))}</h3><p>{_inner(bd.find("p"))}</p></div>'
    cta = soup.find('section', class_='cta-section')
    form_sec = soup.find('section', id='hr-form')
    form = form_sec.find('form'); success = form_sec.find(id='hrSuccess')
    # keep the form's markup and ids so /lecture/form.js keeps working; restyle through classes
    form_html = str(form).replace('class="form-grid"', 'class="form fgrid2"').replace('class="field full"', 'class="fld full"').replace('class="field"', 'class="fld"').replace('class="field full hp"', 'class="fld full hp"').replace('class="submit-btn"', 'class="submit-btn sbm-lite pbtn lg"')
    succ_html = str(success).replace('class="form-success"', 'class="form-success done"')

    def sec_head(k, h, d=''):
        return f'<div class="sec-head"><div class="kicker">{esc(k)}</div><h2 class="h2">{h}</h2>{("<p class=lede>" + d + "</p>") if d else ""}</div>'

    body = f'''<section class="hero">
  <div class="copy"><div class="kicker">{esc(eb)}</div><h1 class="hx">{esc(first)} <em>{esc(em)}</em></h1><p class="sub">{esc(sub)}</p>
    <ul class="chips">{chips}</ul>
    <div class="hero-cta2"><a class="pbtn lg" href="#hr-form">אני רוצה לתאם הרצאה {C.CHIP_DOWN}</a></div></div>
  <div class="visual"><div class="panel"><img class="portrait" src="/assets/img/tico-fullbody.webp" width="547" height="1091" alt="צ'יקו זוויבל" fetchpriority="high"></div></div>
</section>
<section class="band slim"><div class="nums">{stats}</div></section>
<section class="sec"><div class="split"><div class="copy"><div class="kicker">למה זה שווה</div><h2 class="h2">{esc(_txt(val.find("h2")))}</h2>{"".join(val_ps)}</div>
<aside class="idcard"><div class="idtop"><span>TICO FINANCE</span><span>המרצה</span></div><div class="idbody"><div class="idph" aria-hidden="true"><span>TF</span></div><dl><div><dt>שם</dt><dd>{esc(a_h)}</dd></div><div><dt>תפקיד</dt><dd>{esc(a_role)}</dd></div></dl></div><div class="about-body">{a_ps}<div class="tags">{tags}</div></div></aside></div></section>
<section class="sec">{sec_head("השוק היום", esc(_txt(market.select_one(".section-title"))), esc(_txt(market.select_one(".section-desc"))))}<div class="cards c2">{m_cards}</div><div class="note big mb">{esc(_txt(market.select_one(".market-bottom")))}</div></section>
<section class="sec">{sec_head("התוכן", esc(_txt(inc.select_one(".section-title"))), _inner(inc.select_one(".section-desc")))}<div class="cards c3">{inc_cards}</div>
<div class="cta-row"><a class="pbtn" href="#hr-form">אני רוצה לתאם הרצאה לארגון שלי {C.CHIP}</a></div></section>
<section class="sec">{sec_head("לעובדים", esc(_txt(emp.select_one(".section-title"))), esc(_txt(emp.select_one(".section-desc"))))}<div class="steps">{emp_steps}</div></section>
<section class="sec">{sec_head("התהליך", esc(_txt(how.select_one(".section-title"))), esc(_txt(how.select_one(".section-desc"))))}<div class="steps s4">{how_steps}</div></section>
{band_section(esc(_txt(cta.find("h2"))), [], f'<p class="bandp">{esc(_txt(cta.find("p")))}</p><a class="pbtn inv lg" href="#hr-form">תיאום הרצאה {C.CHIP}</a>')}
<section class="sec formsec" id="hr-form"><div class="card"><h2>{esc(_txt(form_sec.find("h2")))}</h2><p class="sub2">{esc(_txt(form_sec.find("p")))}</p>{form_html}{succ_html}</div></section>'''
    scripts = '<script src="/lecture/form.js"></script>\n<script>TicoLectureForm(document.getElementById("hrForm"), { type:"hr", requireOrg:true, successId:"hrSuccess", defaultUtm:{ utm_source:"direct" } });</script>'
    write('lecture/index.html', document('he', head, body, scripts))



def build_lottery():
    from bs4 import BeautifulSoup
    src = git_show('lottery-calculator/index.html')
    soup = BeautifulSoup(src, 'lxml')
    head = clean_head(src)
    hero = soup.find('section', class_='hero')
    eb = _txt(hero.select_one('.hero-eyebrow')).lstrip('✦ ').strip(); h1 = _txt(hero.find('h1')); sub = _txt(hero.find('p'))
    calc = soup.find('section', id='calc')
    inner = _inner(calc.select_one('.section-inner'))
    inner = inner.replace('src="img/', 'src="/lottery-calculator/img/')
    inner = inner.replace('class="btn-wa"', 'class="wbtn sm"').replace('💬 ', '')
    fin = soup.find('section', class_='final-cta')
    f_h = _txt(fin.find('h2')); f_p = _txt(fin.find('p')); f_wa = fin.find('a')['href']
    body = (f'<div class="phead"><div class="kicker">{esc(eb)}</div><h1 class="hx h1page">{esc(h1)}</h1><p class="lede">{esc(sub)}</p></div>'
            f'<section class="sec lottery" id="calc">{inner}</section>'
            f'<section class="final"><div><h2>{esc(f_h)}</h2><p>{esc(f_p)}</p><div class="acts"><a class="pbtn inv lg" href="{f_wa}" target="_blank" rel="noopener">דברו איתי בוואטסאפ {C.CHIP}</a></div></div>'
            f'<img src="/assets/img/tico-halfbody.webp" width="400" height="400" alt="צ\'יקו זוויבל" loading="lazy"></section>')
    write('lottery-calculator/index.html', document('he', head, body, '<script src="/assets/js/lottery.js" defer></script>'))


if __name__ == '__main__':
    only = sys.argv[1:] or ['home', 'br']
    for name in only:
        globals()['build_' + name]()
        print('built', name)
