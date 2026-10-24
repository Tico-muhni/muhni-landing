#!/usr/bin/env python3
"""Preview-only: re-skins the hidden (noindex) pages with the shared header/footer and brand tokens.

The original page CSS is kept but scoped under `.g` and remapped to the brand palette/fonts.
Usage: python3 tools/reskin_hidden.py [page ...]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_pages as B  # noqa: E402
import chrome as C  # noqa: E402

BRAND_VARS = {
    '--green': '#2E8B57', '--green-dark': '#1d6b40', '--navy': '#0B1F3A', '--orange': '#ffffff',
    '--bg': '#ffffff', '--border': '#e2ebe5', '--text': '#14211a', '--muted': '#5a6b60',
    '--green-deep': '#1d6b40', '--surface': '#ffffff', '--ink': '#14211a', '--ink-soft': '#5a6b60',
    '--purple': '#1d6b40', '--purple-light': '#e6f2ea', '--text-muted': '#5a6b60', '--green-light': '#e6f2ea',
}

LITE_CSS = '''
.gbar{display:flex;justify-content:center;padding:18px 0 6px}.gbar img{height:46px;width:auto}
.gfoot{text-align:center;padding:28px 16px 40px;color:var(--muted);font-size:13px;line-height:1.8}.gfoot a{color:var(--g-700)}
'''


def split_blocks(css):
    """Yield (prelude, body) pairs for top-level blocks."""
    i, n, out = 0, len(css), []
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {'{': 1, '}': -1}.get(css[k], 0)
            k += 1
        out.append((css[i:j].strip(), css[j + 1:k - 1]))
        i = k
    return out


def prefix_css(css, scope='.g'):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []
    for pre, body in split_blocks(css):
        if pre.startswith('@media') or pre.startswith('@supports'):
            out.append(f'{pre}{{{prefix_css(body, scope)}}}')
        elif pre.startswith('@'):
            out.append(f'{pre}{{{body}}}')
        else:
            sels = []
            for s in pre.split(','):
                s = s.strip()
                if s in ('html', 'body', ':root'):
                    s = scope
                elif s == '*' or s.startswith('*'):
                    s = f'{scope} {s}'
                else:
                    s = f'{scope} {s}'
                sels.append(s)
            out.append(f'{",".join(sels)}{{{body}}}')
    return '\n'.join(out)


def remap(css):
    def font(m):
        v = m.group(0)
        if v.startswith('font-family:var('):
            return v
        first = v.split(':', 1)[1].split(',')[0].strip(" '\"").lower()
        serif = first in ('georgia', 'frank ruhl libre', 'david') or re.search(r'(?<!sans-)serif\s*$', v)
        return 'font-family:var(--f-serif)' if serif else 'font-family:var(--f-display)'
    css = re.sub(r'font-family\s*:[^;}]*', font, css)
    for k, v in BRAND_VARS.items():
        css = re.sub(rf'({re.escape(k)}\s*:\s*)#[0-9a-fA-F]{{3,8}}', rf'\g<1>{v}', css)
    return css


def inner_body(src):
    m = re.search(r'<body[^>]*>(.*)</body>', src, re.S)
    return m.group(1)


def render(path, strip=(), extra_css='', main_class='', css_sub=(), lite=False, body_sub=(), bar=True):
    src = B.git_show(path)
    head = B.clean_head(src)
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', src, re.S))
    css = remap(prefix_css(css))
    for a, b in css_sub:
        css = css.replace(a, b)
    css += '\n' + extra_css + '\n.g{overflow-x:clip}.g input,.g textarea{min-width:0;max-width:100%}'
    body = inner_body(src)
    body = re.sub(r'<script defer src="/_vercel/insights/script.js"></script>', '', body)
    for a_, b_ in body_sub:
        body = body.replace(a_, b_)
    for pat in strip:
        body = re.sub(pat, '', body, flags=re.S)
    head += f'\n<style>{css}</style>' + (f'<style>{LITE_CSS}</style>' if lite else '')
    scripts = ''.join(re.findall(r'<script\b(?![^>]*src=)[^>]*>.*?</script>', body, re.S))
    body = re.sub(r'<script\b(?![^>]*src=)[^>]*>.*?</script>', '', body, flags=re.S)
    if lite:
        bar_html = '<header class="gbar"><a href="/" aria-label="TICO FINANCE"><img src="/assets/img/logo-he.webp" width="800" height="185" alt="TICO FINANCE אדריכל המשכנתאות"></a></header>'
        foot = '<footer class="gfoot">TICO FINANCE · צ\'יקו זוויבל, יועץ משכנתאות<br><a href="/privacy.html">מדיניות פרטיות</a> · <a href="/terms.html">תנאי שימוש</a> · <a href="/accessibility.html">הצהרת נגישות</a></footer>'
        bar = bar_html if bar else ''
        B.write(path, f'<!DOCTYPE html>\n<html dir="rtl" lang="he">\n<head>\n{head}\n</head>\n<body>\n{bar}\n<main id="main" class="page {main_class}"><div class="g">{body}</div></main>\n{foot}\n{scripts}\n{C.SCRIPTS}\n</body>\n</html>\n')
    else:
        B.write(path, B.document('he', head, f'<div class="g">{body}</div>', scripts, main_class))


GUIDE_EXTRA = '''
.g header.hero{margin-top:16px;border-radius:36px;background:linear-gradient(160deg,#3aa869,#2E8B57 55%,#1d6b40);padding:clamp(36px,6vw,64px) 24px clamp(64px,8vw,90px)}
.g header.hero h1{font-weight:900;font-size:clamp(1.9rem,4.4vw,3rem);line-height:1.12}
.g main{padding-top:48px}
.g .fact{box-shadow:0 18px 36px -24px rgba(20,33,26,.25);border-radius:20px}
.g .fact .num,.g .step-num{font-family:var(--f-num)}
.g .cta{border-radius:32px;background:linear-gradient(160deg,#2E8B57,#1d6b40)}
.g .cta .btn{background:#fff;color:var(--g-700);border-radius:999px;padding:14px 28px;font-weight:800}
.g .cta .btn:hover{background:var(--g-100)}
.g .disclaimer{background:var(--tint);border-color:var(--line);color:var(--muted)}
.g .disclaimer a{color:var(--g-700)!important}
.g .step{border-radius:22px}
'''

FOCUS_EXTRA = '''
.g{color:var(--ink)}
.g .hero{border-radius:36px;background:linear-gradient(160deg,#3aa869,#2E8B57 55%,#1d6b40)}
.g .hero h1,.g header h1{font-family:var(--f-serif);font-weight:900}
.g h1,.g h2,.g h3{font-family:var(--f-serif)}
.g .hero-btn,.g .btn-primary,.g .wa-btn{border-radius:999px}
'''

CARD_EXTRA = FOCUS_EXTRA + '''
.g .csheet{background:transparent}.g .hero{margin:10px 0 0;border-radius:36px;padding-top:34px}.g .hero h1{font-size:clamp(2rem,9vw,2.8rem);color:#fff}
.g .main{padding-top:30px}.g .about{border-radius:28px;border-color:var(--line)}.g .btn{border-radius:999px}
.g .section-title{font-family:var(--f-serif);color:var(--navy)}.g .about .result{border-radius:16px}
'''

PAGES = {
    'topsecret/index.html': dict(lite=True, bar=False, css_sub=[('#00c853', '#2E8B57'), ('#00a844', '#1d6b40'), ('0,200,83', '46,139,87'), ('#0c0', '#2E8B57')], extra_css='''
.g{color:var(--ink)}.g h1,.g h2,.g h3{font-family:var(--f-serif)}
'''),
    'card/index.html': dict(lite=True, strip=[r'<div class="top">.*?</div>'], extra_css=CARD_EXTRA, css_sub=[('.sheet', '.csheet')], body_sub=[('class="sheet"', 'class="csheet"')]),
    'clients/index.html': dict(lite=True, strip=[r'<div class="top">.*?</div>'], extra_css=CARD_EXTRA, css_sub=[('.sheet', '.csheet')], body_sub=[('class="sheet"', 'class="csheet"')]),
    'check/index.html': dict(lite=True, strip=[r'<div class="topbar">.*?</div>', r'<footer>.*?</footer>'], extra_css=FOCUS_EXTRA + '''
.g .hero{margin-top:10px;padding:44px 0 52px}.g .hero h1 em{color:#fff;text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:6px}
.g .me,.g .how{background:transparent}.g .proof-card{background:linear-gradient(160deg,#2E8B57,#1d6b40);border-radius:28px}
.g .step{border-radius:20px;background:var(--tint);border-color:var(--line)}.g .step-num{border-radius:50%}
.g .form-card{border-radius:28px;border-color:var(--line)}.g .form-card h2{font-family:var(--f-serif);color:var(--g-700)}
'''),
    'street/index.html': dict(lite=True, strip=[r'<img class="logo"[^>]*>', r'<div class="bars">.*?</div>', r'<div class="footer">.*?</div>'],
        css_sub=[('#0F243E', '#2E8B57'), ('#1B3A5E', '#1d6b40'), ('#1F6B43', '#2E8B57')], extra_css='''
.g{color:var(--ink)}.g h1,.g h2{color:var(--navy);font-family:var(--f-serif)}.g h1 span{color:var(--g-600)}
.g .btn{border-radius:999px}.g .step-num{font-family:var(--f-num)}.g .chips div{border-width:1.5px;border-color:var(--line);background:var(--tint)}
.g .cta-box{border-radius:32px;background:linear-gradient(160deg,#2E8B57,#1d6b40)}.g .cta-box *{color:#fff}.g .cta-box .btn-primary{background:#fff;color:var(--g-700)}
'''),
    'mashov/index.html': dict(lite=True, strip=[r'<img src="/hebrewlogo.png"[^>]*>'], extra_css=FOCUS_EXTRA + '''
.g .header{margin-top:10px;border-radius:36px;background:linear-gradient(160deg,#3aa869,#2E8B57 55%,#1d6b40)}.g .header h1{font-size:clamp(1.7rem,6vw,2.4rem);color:#fff}
.g .question-card{border-radius:24px}.g .q-text{color:var(--navy)}
'''),
    'lecture/join/index.html': dict(lite=True, strip=[r'<div class="logo-brand">.*?</div>'], extra_css='''
.g .hero h1{color:var(--navy)}
.g .hp{position:absolute!important;left:0!important;top:0;width:1px;height:1px;opacity:0;overflow:hidden;pointer-events:none}
'''),
    'ashrai/index.html': dict(strip=[r'<img src="/hebrewlogo.png"[^>]*>', r'<footer>.*?</footer>'], extra_css=GUIDE_EXTRA),
    'itrot/index.html': dict(strip=[r'<img src="/hebrewlogo.png"[^>]*>', r'<footer>.*?</footer>'], extra_css=GUIDE_EXTRA),
    'mismachim/index.html': dict(strip=[r'<img src="/hebrewlogo.png"[^>]*>', r'<footer>.*?</footer>'], extra_css=GUIDE_EXTRA),
}

if __name__ == '__main__':
    only = sys.argv[1:] or list(PAGES)
    for p in only:
        key = p if p.endswith('.html') else p.strip('/') + '/index.html'
        render(key, **PAGES[key])
        print('reskinned', key)
