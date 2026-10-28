"""Security checks against the built site served with its production headers (hserve.py on :8766).
1 headers present  2 no CSP violations while the page works  3 no third-party requests  4 XSS payloads in the job card
5 links: https only, target=_blank has noopener  6 clickjacking: page refuses to be framed  7 secrets / leftovers scan."""
import asyncio, json, os, re, sys
from playwright.async_api import async_playwright
import os as _os
_CH = _os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
LAUNCH = dict(args=['--no-sandbox'], **({'executable_path': _CH} if _os.path.exists(_CH) else {}))
B = 'http://127.0.0.1:8766/'
DIST = os.environ.get('SITE_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
PAGES = ['', 'en/', 'polityka-prywatnosci/', 'nie-ma-takiej-strony/',
         'oproznianie-piwnic-strychow-garazy/', 'oproznianie-mieszkania-po-zmarlym/', 'wywoz-mebli-wroclaw/',
         'dla-firm/', 'obszar-dzialania/', 'jak-pozbyc-sie-starych-mebli-wroclaw/']
PAYLOADS = ['<img src=x onerror="window.__xss=1">', '"><script>window.__xss=1</script>', "javascript:window.__xss=1", '<svg onload="window.__xss=1">', '${7*7}{{7*7}}']
INIT = """window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + (e.blockedURI || 'inline') + ' ' + (e.sample || '')));"""
res = {'pass': [], 'fail': []}
def ok(cond, what):
    (res['pass'] if cond else res['fail']).append(what)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**LAUNCH)
        for vp, mob in [({'width': 1440, 'height': 900}, False), ({'width': 390, 'height': 844}, True)]:
            ctx = await b.new_context(viewport=vp, is_mobile=mob, has_touch=mob)
            await ctx.add_init_script(INIT)
            for path in PAGES:
                pg = await ctx.new_page(); reqs = []; errs = []
                pg.on('request', lambda r, reqs=reqs: reqs.append(r.url))
                pg.on('pageerror', lambda e, errs=errs: errs.append(str(e)))
                resp = await pg.goto(B + path, wait_until='networkidle'); await pg.wait_for_timeout(600)
                tag = f"{'mobile' if mob else 'desktop'} /{path}"
                h = resp.headers
                for k in ('content-security-policy', 'strict-transport-security', 'x-content-type-options', 'x-frame-options', 'referrer-policy', 'permissions-policy'):
                    ok(k in h, f'{tag}: header {k}')
                if path in ('', 'en/'):
                    # exercise the page: animation + job card, then look for CSP violations
                    await pg.evaluate("window.__stair && window.__stair.draw(0.5)"); await pg.wait_for_timeout(200)
                    ok(await pg.evaluate("!!document.querySelector('#scene').getAttribute('viewBox')"), f'{tag}: stairwell runs under CSP')
                    for i, p in enumerate(PAYLOADS):
                        await pg.fill('#k-co', p); await pg.dispatch_event('#k-co', 'input')
                        await pg.fill('#k-area', p); await pg.dispatch_event('#k-area', 'input')
                        await pg.wait_for_timeout(120)
                    ok(await pg.evaluate("typeof window.__xss === 'undefined'"), f'{tag}: XSS payloads not executed')
                    ok(await pg.evaluate("!document.querySelector('#items img, #items script, #items svg, #msg img, #msg script')"), f'{tag}: payloads rendered as text only')
                    href = await pg.get_attribute('#send', 'href') or ''
                    ok(href.startswith('https://wa.me/') and '<' not in href and '"' not in href, f'{tag}: WhatsApp link encoded ({href[:40]}…)')
                    await pg.click('#copy'); await pg.wait_for_timeout(200)
                csp = await pg.evaluate('window.__csp')
                ok(not csp, f'{tag}: no CSP violations' + (f' {csp[:3]}' if csp else ''))
                ok(not errs, f'{tag}: no script errors' + (f' {errs[:2]}' if errs else ''))
                third = [u for u in reqs if not u.startswith(B) and not u.startswith('data:')]
                ok(not third, f'{tag}: no third-party requests without consent' + (f' {third[:3]}' if third else ''))
                links = await pg.evaluate("[...document.querySelectorAll('a[href]')].map(a => [a.getAttribute('href'), a.target, a.rel])")
                bad_http = [l[0] for l in links if l[0].startswith('http://')]
                ok(not bad_http, f'{tag}: no plain-http links' + (f' {bad_http}' if bad_http else ''))
                bad_blank = [l[0] for l in links if l[1] == '_blank' and 'noopener' not in (l[2] or '')]
                ok(not bad_blank, f'{tag}: target=_blank links have noopener' + (f' {bad_blank}' if bad_blank else ''))
                if path == 'nie-ma-takiej-strony/': ok(resp.status == 404, f'{tag}: missing page returns 404')
                await pg.close()
            await ctx.close()
        # clickjacking: try to frame the site from another origin
        ctx = await b.new_context(); pg = await ctx.new_page()
        await pg.set_content(f'<iframe id="f" src="{B}" width="800" height="600"></iframe>'); await pg.wait_for_timeout(1500)
        framed = await pg.evaluate("(() => { try { const d = document.getElementById('f').contentDocument; return d && d.body && d.body.innerText.length > 0; } catch(e) { return 'cross-origin'; } })()")
        frames = [f.url for f in pg.frames]
        loaded = any(u.startswith(B) for u in frames) and framed not in (False,)
        child = [f for f in pg.frames if f.url.startswith(B)]
        content = ''
        if child:
            try: content = await child[0].evaluate('document.body ? document.body.innerText.slice(0, 40) : ""')
            except Exception as e: content = ''
        ok(not content, 'clickjacking: site refuses to load inside a foreign frame')
        await b.close()
    # static scan of the built files
    leftovers = []
    pat = re.compile(r'(api[_-]?key|secret|password|token|BEGIN (RSA|OPENSSH) PRIVATE|AKIA[0-9A-Z]{16}|localhost|127\.0\.0\.1|/home/claude|\{\{|\{%)', re.I)
    for d, _, fs in os.walk(DIST):
        for f in fs:
            if f.endswith(('.woff2', '.png')): continue
            txt = open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
            for m in pat.finditer(txt):
                leftovers.append(f'{os.path.relpath(os.path.join(d, f), DIST)}: {m.group(0)}')
    ok(not leftovers, 'no secrets, local paths or template leftovers in the files' + (f' {leftovers[:5]}' if leftovers else ''))
    print(json.dumps({'passed': len(res['pass']), 'failed': res['fail']}, ensure_ascii=False, indent=1))
    sys.exit(1 if res['fail'] else 0)

asyncio.run(main())
