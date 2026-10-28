# -*- coding: utf-8 -*-
"""Builds two outputs from src/ + i18n.py + site_config.json (contacts and company data):
   build/artifact/  PL body-only index.html + EN full page, everything inline (for the claude.ai artifact)
   build/dist/      the real static site: PL + EN, self-hosted fonts, config.js, robots, sitemap, favicon, og image
Usage: python3 build.py [--base https://example.pl/]"""
import json, os, re, shutil, sys, hashlib
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i18n import LANGS, DISTRICTS
import scene as SCENE

BASE = 'https://wyniose.pl/'
if '--base' in sys.argv: BASE = sys.argv[sys.argv.index('--base') + 1].rstrip('/') + '/'
SRC = os.path.join(HERE, 'src')
OUT_A = os.path.join(HERE, 'build', 'artifact')
OUT_D = os.path.join(HERE, 'build', 'dist')
FS = os.environ.get('FONTSOURCE', '/nonexistent')

css = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read()
js = '\n'.join(open(os.path.join(SRC, f), encoding='utf-8').read() for f in ('app.js', 'stair.js', 'consent.js'))
env = Environment(loader=FileSystemLoader(SRC), autoescape=True, keep_trailing_newline=True)
tpl = env.get_template('page.html.j2')

GF_LAT = 'https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@800;900&family=Rethink+Sans:ital,wght@0,400;0,500;0,600;0,700;1,500&display=swap'
GF_CYR = 'https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@900&family=Oswald:wght@500;600;700&family=Onest:wght@400;500;600;700&display=swap'

CFG = json.load(open(os.path.join(HERE, 'site_config.json'), encoding='utf-8'))
def digits(x): return re.sub(r'[^\d+]', '', x or '')
def company_line(co):
    if isinstance(co, str): return co
    return ', '.join(x for x in [co.get('name'), co.get('address'), ('NIP ' + co['nip']) if co.get('nip') else '', ('REGON ' + co['regon']) if co.get('regon') else ''] if x)
def contact(with_privacy):
    return dict(phone=CFG.get('phone', ''), tel=('tel:' + digits(CFG['phone'])) if CFG.get('phone') else '',
                phone2=CFG.get('phone2', ''), tel2=('tel:' + digits(CFG['phone2'])) if CFG.get('phone2') else '',
                email=CFG.get('email', ''), company_line=company_line(CFG.get('company', '')),
                privacy=CFG.get('privacyUrl', '') if with_privacy else '')
def site_js(with_privacy):
    d = dict(CFG)
    if not with_privacy: d['privacyUrl'] = ''; d.pop('ads', None)   # the claude.ai preview never loads Google tags
    return d

def jsdump(o):
    return Markup(json.dumps(o, ensure_ascii=False).replace('</', '<\\/'))

def lang_strings(t):
    d = dict(t['js']); d.update(hook=t['hook'], hookWord=t['hook_word'], q1=t['q1'], q2=t['q2'], player=t['player'])
    return d

def path_of(code):  # site-relative path of a language page
    return '' if code == 'pl' else code + '/'

def ld_json(t):
    co = CFG.get('company', {}) if isinstance(CFG.get('company'), dict) else {}
    adr = {'@type': 'PostalAddress', 'addressLocality': 'Wrocław', 'addressCountry': 'PL'}
    if co.get('address'):
        m = re.match(r'^(.*?),\s*(\d{2}-\d{3})\s+(.+)$', co['address'])
        if m: adr.update(streetAddress=m.group(1), postalCode=m.group(2), addressLocality=m.group(3))
        else: adr['streetAddress'] = co['address']
    d = {'@context': 'https://schema.org', '@type': 'LocalBusiness', 'name': 'Wyniosę', 'url': BASE + path_of(t['lang']),
         'image': BASE + 'og.png', 'description': t['desc'], 'address': adr,
         'areaServed': {'@type': 'GeoCircle', 'geoMidpoint': {'@type': 'GeoCoordinates', 'latitude': 51.1079, 'longitude': 17.0385}, 'geoRadius': '70000'},
         'knowsLanguage': ['pl', 'uk', 'ru', 'en'], 'paymentAccepted': 'Cash, BLIK, bank transfer'}
    if CFG.get('phone'): d['telephone'] = digits(CFG['phone'])
    if CFG.get('email'): d['email'] = CFG['email']
    if co.get('nip'): d['taxID'] = co['nip']
    if co.get('name'): d['legalName'] = co['name']
    return jsdump(d)

def render(t, *, full, proto, root, inline, fonts_url, gfonts, config_inline, icon, canonical, alt, og_image, css_href=None, js_href=None, title=None):
    code = t['lang']
    langs = [(c, label, root + path_of(c) + ('index.html' if inline else ''), name) for c, label, name, _ in LANGS]
    if not inline:  # dist: clean directory URLs, but keep them relative so the site works from any folder
        langs = [(c, label, (root + path_of(c)) or './', name) for c, label, name, _ in LANGS]
    return tpl.render(
        t=t, lang=code, cyr=t['cyr'], title=title or t['title'], full=full, proto=proto, root=root,
        langs=langs, districts=DISTRICTS, fonts_url=fonts_url, gfonts=gfonts, icon=icon,
        css=Markup(css) if inline else None, js=Markup(js) if inline else None, css_href=css_href, js_href=js_href,
        config_inline=jsdump(site_js(False)) if config_inline else None, jsl=jsdump(lang_strings(t)),
        canonical=canonical, alt=alt, og_image=og_image, scene=Markup(SCENE.svg(t['scene_title'])),
        c=contact(not inline), ldjson=None if inline else ld_json(t))

def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

def tidy(s):
    return re.sub(r'\n\s*\n+', '\n', s)

# ---------- artifact ----------
shutil.rmtree(OUT_A, ignore_errors=True)
for code, label, name, t in LANGS:
    full = code != 'pl'
    root = '' if code == 'pl' else '../'
    html = render(t, full=full, proto=True, root=root, inline=True, fonts_url=GF_CYR if t['cyr'] else GF_LAT, gfonts=True,
                  config_inline=True, icon=False, canonical=None, alt=[], og_image='', title='Wyniosę Homepage' if code == 'pl' else None)
    write(os.path.join(OUT_A, path_of(code), 'index.html'), tidy(html))

# ---------- dist ----------
shutil.rmtree(OUT_D, ignore_errors=True)
os.makedirs(os.path.join(OUT_D, 'assets', 'fonts'))

# self-hosted fonts (no request to Google from the visitor's browser)
CYR = any(t['cyr'] for *_, t in LANGS)   # Cyrillic fonts only while a UA/RU page is built
WANT = {'big-shoulders-display': ([800, 900], ['normal']), 'rethink-sans': ([400, 500, 600, 700], ['normal'])}
if CYR: WANT.update({'oswald': ([500, 600, 700], ['normal']), 'onest': ([400, 500, 600, 700], ['normal'])})
SUBSETS = ('latin', 'latin-ext') + (('cyrillic', 'cyrillic-ext') if CYR else ())
faces = []
def take_faces(pkg, weight, style):
    cssf = os.path.join(FS, pkg, f'{weight}{"-italic" if style == "italic" else ""}.css')
    for m in re.finditer(r'/\* (\S+) \*/\s*@font-face\s*\{(.*?)\}', open(cssf).read(), re.S):
        tag, body = m.group(1), m.group(2)
        sub = tag[len(pkg) + 1:].rsplit('-', 2)[0]
        if sub not in SUBSETS: continue
        fn = f'{tag}.woff2'
        src = os.path.join(FS, pkg, 'files', fn)
        if not os.path.exists(src): continue
        shutil.copy(src, os.path.join(OUT_D, 'assets', 'fonts', fn))
        body = re.sub(r'src:[^;]+;', f"src: url(fonts/{fn}) format('woff2');", body)
        faces.append('@font-face {' + body.strip() + '}')
LOCAL_FONTS = os.path.join(HERE, 'fonts')
if os.path.isdir(FS):
    for pkg, (ws, styles) in WANT.items():
        for w in ws:
            for st in styles: take_faces(pkg, w, st)
    take_faces('rethink-sans', 500, 'italic')
    fonts_css = '\n'.join(faces) + '\n'
    shutil.rmtree(LOCAL_FONTS, ignore_errors=True)
    shutil.copytree(os.path.join(OUT_D, 'assets', 'fonts'), LOCAL_FONTS)
    open(os.path.join(LOCAL_FONTS, 'fonts.css'), 'w').write(fonts_css)
else:  # no fontsource checkout: reuse the copies kept next to the sources
    for fn in os.listdir(LOCAL_FONTS):
        if fn.endswith('.woff2'): shutil.copy(os.path.join(LOCAL_FONTS, fn), os.path.join(OUT_D, 'assets', 'fonts', fn))
    fonts_css = open(os.path.join(LOCAL_FONTS, 'fonts.css')).read()
write(os.path.join(OUT_D, 'assets', 'fonts.css'), fonts_css)

ver = hashlib.sha1((css + js + fonts_css).encode()).hexdigest()[:8]
write(os.path.join(OUT_D, 'assets', 'style.css'), css)
write(os.path.join(OUT_D, 'assets', 'site.js'), js)
cfg_head = open(os.path.join(HERE, 'config.template.js'), encoding='utf-8').read().split('window.SITE')[0]
write(os.path.join(OUT_D, 'config.js'), cfg_head + 'window.SITE = ' + json.dumps(CFG, ensure_ascii=False, indent=2) + ';\n')

hreflang = {'pl': 'pl', 'uk': 'uk', 'ru': 'ru', 'en': 'en'}
alt = [(hreflang[c], BASE + path_of(c)) for c, *_ in LANGS] + [('x-default', BASE)]
for code, label, name, t in LANGS:
    root = '' if code == 'pl' else '../'
    html = render(t, full=True, proto=False, root=root, inline=False, fonts_url=root + 'assets/fonts.css?v=' + ver, gfonts=False,
                  config_inline=False, icon=True, canonical=BASE + path_of(code), alt=alt, og_image=BASE + 'og.png',
                  css_href=root + 'assets/style.css?v=' + ver, js_href=root + 'assets/site.js?v=' + ver)
    write(os.path.join(OUT_D, path_of(code), 'index.html'), tidy(html))

write(os.path.join(OUT_D, 'robots.txt'), f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for code, *_ in LANGS:
    sm.append(f'  <url><loc>{BASE + path_of(code)}</loc>')
    for h, u in alt: sm.append(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>')
    sm.append('  </url>')
sm.append('</urlset>')
write(os.path.join(OUT_D, 'sitemap.xml'), '\n'.join(sm) + '\n')
# privacy policy: company and contact data baked into the HTML (config.js can still override them later)
from markupsafe import escape
pp = open(os.path.join(HERE, 'static', 'polityka-prywatnosci.html'), encoding='utf-8').read()
co = CFG.get('company', {}) if isinstance(CFG.get('company'), dict) else {'name': CFG.get('company', '')}
def tel_link(n): return f'<a href="tel:{digits(n)}">{escape(n)}</a>'
fills = {'NAME': escape(co.get('name', '')), 'ADDR': escape(co.get('address', '')), 'NIP': escape(co.get('nip', '')), 'REGON': escape(co.get('regon', '')),
         'EMAIL': f'<a href="mailto:{escape(CFG["email"])}">{escape(CFG["email"])}</a>' if CFG.get('email') else '',
         'PHONE': tel_link(CFG['phone']) if CFG.get('phone') else '', 'PHONE2': tel_link(CFG['phone2']) if CFG.get('phone2') else '',
         'DATE': escape(CFG.get('privacyDate', ''))}
for k, v in fills.items():
    if v: pp = re.sub(r'<!--%s-->.*?<!--/%s-->' % (k, k), str(v), pp, flags=re.S)
    else: pp = pp.replace('<!--%s-->' % k, '').replace('<!--/%s-->' % k, '')
for k, field in (('ADDR_HIDDEN', co.get('address')), ('REGON_HIDDEN', co.get('regon')), ('PHONE2_HIDDEN', CFG.get('phone2'))):
    pp = pp.replace('<!--%s-->' % k, '' if field else ' hidden')
write(os.path.join(OUT_D, 'polityka-prywatnosci', 'index.html'), pp)
for extra in ('favicon.svg', 'og.png', '404.html'):
    p = os.path.join(HERE, 'static', extra)
    if os.path.exists(p): shutil.copy(p, os.path.join(OUT_D, extra))

# ---------- security: strict CSP (inline scripts allowed only by hash), headers for Netlify/Cloudflare (_headers) and Apache/OVH (.htaccess) ----------
import base64
hashes = set()
for d, _, fs in os.walk(OUT_D):
    for f in fs:
        if not f.endswith('.html'): continue
        html = open(os.path.join(d, f), encoding='utf-8').read()
        for m in re.finditer(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', html, re.S):
            if 'application/ld+json' in m.group(1): continue
            hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(m.group(2).encode('utf-8')).digest()).decode() + "'")
# Google Ads hosts per developers.google.com/tag-platform/security/guides/csp (loaded only after consent, see consent.js)
G_SCRIPT = "https://www.googletagmanager.com https://www.googleadservices.com https://www.google.com"
G_IMG = "https://www.googletagmanager.com https://www.googleadservices.com https://googleads.g.doubleclick.net https://pagead2.googlesyndication.com https://www.google.com https://www.google.pl"
G_CONNECT = G_IMG + " https://ad.doubleclick.net"
G_FRAME = "https://www.googletagmanager.com https://td.doubleclick.net"
CSP = ("default-src 'none'; script-src 'self' " + ' '.join(sorted(hashes)) + " " + G_SCRIPT + "; style-src 'self' 'unsafe-inline'; img-src 'self' data: " + G_IMG + "; "
       "font-src 'self'; connect-src 'self' " + G_CONNECT + "; frame-src " + G_FRAME + "; manifest-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests")
SEC = [('Content-Security-Policy', CSP), ('Strict-Transport-Security', 'max-age=31536000'), ('X-Content-Type-Options', 'nosniff'),
       ('X-Frame-Options', 'DENY'), ('Referrer-Policy', 'strict-origin-when-cross-origin'),
       ('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()'),
       ('Cross-Origin-Opener-Policy', 'same-origin'), ('Cross-Origin-Resource-Policy', 'same-origin')]
write(os.path.join(OUT_D, '_headers'), '/*\n' + ''.join(f'  {k}: {v}\n' for k, v in SEC) +
      '/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n/config.js\n  Cache-Control: no-cache\n')
write(os.path.join(OUT_D, '.htaccess'), '''# Wyniosę: Apache / OVH hosting
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteCond %{HTTP:X-Forwarded-Proto} !https
  RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
  RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
</IfModule>
<IfModule mod_headers.c>
''' + ''.join(f'  Header always set {k} "{v}"\n' for k, v in SEC) + '''  <FilesMatch "\\.(woff2|css|js|svg|png)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "^config\\.js$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
</IfModule>
''')
import datetime
exp = (datetime.date.today() + datetime.timedelta(days=360)).isoformat() + 'T00:00:00.000Z'
sectxt = (f"Contact: mailto:{CFG.get('email', '')}\nExpires: {exp}\nPreferred-Languages: pl, en, uk, ru\n"
          f"Canonical: {BASE}.well-known/security.txt\n")
write(os.path.join(OUT_D, '.well-known', 'security.txt'), sectxt)
write(os.path.join(OUT_D, 'security.txt'), sectxt)
# Netlify Drop skips dot-folders, so serve /.well-known/security.txt from the root copy
write(os.path.join(OUT_D, '_redirects'), '/.well-known/security.txt  /security.txt  200\n')
print('artifact:', sorted(os.path.relpath(os.path.join(d, f), OUT_A) for d, _, fs in os.walk(OUT_A) for f in fs))
print('dist:', len([1 for d, _, fs in os.walk(OUT_D) for f in fs]), 'files, base', BASE, 'ver', ver)
