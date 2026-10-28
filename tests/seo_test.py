"""Static SEO checks on the built site folder (no browser, no network).
1 every sitemap URL exists, is indexable, has its own canonical, one H1, a unique title and a description of sane length
2 JSON-LD parses and names the business (#firma)   3 every internal link and anchor resolves
4 every page in the sitemap is linked from the home page   5 service pages are not thin   6 robots.txt points to the sitemap"""
import html.parser, json, os, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

SITE = os.environ.get('SITE_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
BASE = 'https://wyniose.pl/'
res = {'pass': [], 'fail': []}
def ok(cond, what): (res['pass'] if cond else res['fail']).append(what)

class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ''; self._in = None; self.h1 = 0; self.meta = {}; self.links = []; self.ids = set()
        self.canonical = None; self.ld = []; self.text = []; self._skip = 0; self.in_body = False
    def handle_starttag(self, tag, a):
        a = dict(a)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'body': self.in_body = True
        if tag == 'title' and not self.in_body and not self.title: self._in = 'title'
        elif tag == 'h1': self.h1 += 1
        elif tag == 'meta' and a.get('name'): self.meta[a['name']] = a.get('content', '')
        elif tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        elif tag == 'a' and a.get('href'): self.links.append(a['href'])
        elif tag == 'script' and a.get('type') == 'application/ld+json': self._in = 'ld'
        if tag in ('script', 'style', 'svg'): self._skip += 1
    def handle_endtag(self, tag):
        if tag in ('title', 'script'): self._in = None
        if tag in ('script', 'style', 'svg'): self._skip = max(0, self._skip - 1)
    def handle_data(self, d):
        if self._in == 'title': self.title += d
        elif self._in == 'ld': self.ld.append(d)
        elif not self._skip: self.text.append(d)

def file_for(url):
    path = urlparse(url).path
    f = os.path.join(SITE, path.lstrip('/'))
    return os.path.join(f, 'index.html') if path.endswith('/') else f

def parse(f):
    p = P(); p.feed(open(f, encoding='utf-8').read()); return p

locs = [e.text for e in ET.parse(os.path.join(SITE, 'sitemap.xml')).getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
ok(len(locs) >= 8, f'sitemap lists the pages ({len(locs)})')
robots = open(os.path.join(SITE, 'robots.txt'), encoding='utf-8').read()
ok('Sitemap: ' + BASE + 'sitemap.xml' in robots and 'Disallow: /' not in robots, 'robots.txt allows crawling and points to the sitemap')

titles = {}
parsed = {}
for url in locs:
    f = file_for(url)
    if not os.path.exists(f): ok(False, f'{url}: file exists'); continue
    p = parse(f); parsed[url] = p
    ok(p.canonical == url, f'{url}: canonical is itself ({p.canonical})')
    ok('noindex' not in p.meta.get('robots', ''), f'{url}: indexable')
    ok(p.h1 == 1, f'{url}: exactly one H1 ({p.h1})')
    t = p.title.strip(); ok(10 <= len(t) <= 65, f'{url}: title length {len(t)}')
    titles.setdefault(t, []).append(url)
    d = p.meta.get('description', ''); ok(70 <= len(d) <= 165, f'{url}: description length {len(d)}')
    try:
        ld = json.loads(''.join(p.ld)); ok('#firma' in json.dumps(ld), f'{url}: JSON-LD names the business')
    except Exception as e:
        ok(False, f'{url}: JSON-LD parses ({e})')
for t, us in titles.items(): ok(len(us) == 1, f'title unique: {t}')

# internal links and anchors on every built HTML page
for d, _, fs in os.walk(SITE):
    for fn in fs:
        if not fn.endswith('.html') or fn == '404.html': continue
        f = os.path.join(d, fn); rel = os.path.relpath(f, SITE).replace(os.sep, '/')
        page_url = BASE + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)
        p = parse(f); bad = []
        for h in p.links:
            if re.match(r'^(tel:|mailto:|https?://(?!wyniose\.pl))', h): continue
            u = urljoin(page_url, h); target = u.split('#')[0]; frag = u.split('#')[1] if '#' in u else ''
            tf = file_for(target)
            if not os.path.exists(tf): bad.append(h); continue
            if frag and frag not in parse(tf).ids: bad.append(h)
        ok(not bad, f'/{rel}: internal links resolve' + (f' {bad[:4]}' if bad else ''))

home = parsed.get(BASE)
if home:
    linked = {urljoin(BASE, h).split('#')[0] for h in home.links}
    for url in locs:
        if url != BASE: ok(url in linked, f'home links to {url}')
for url, p in parsed.items():
    if url in (BASE, BASE + 'en/'): continue
    words = len(re.findall(r'\w+', ' '.join(p.text)))
    ok(words >= 450, f'{url}: not thin ({words} words incl. header and footer)')

print(json.dumps({'passed': len(res['pass']), 'failed': res['fail']}, ensure_ascii=False, indent=1))
sys.exit(1 if res['fail'] else 0)
