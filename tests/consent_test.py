"""Consent Mode v2 basic + Google Ads conversion checks against the built site served with production headers (:8766).
Google is unreachable from here, so gtag.js is replaced by a stub that behaves like the tag for what we test:
it reads the dataLayer and fires one image request per conversion to googleadservices.com (allowed by our CSP)."""
import asyncio, json, sys
from playwright.async_api import async_playwright
import os as _os
_CH = _os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
LAUNCH = dict(args=['--no-sandbox'], **({'executable_path': _CH} if _os.path.exists(_CH) else {}))

B = 'http://127.0.0.1:8766/'
TEL = 'AW-18540345955/XIrxCOOG3KsdEOP03IhF'; WA = 'AW-18540345955/HsRYCKHHzKsdEOP03IhF'
GOOGLE = ('googletagmanager.com', 'googleadservices.com', 'doubleclick.net', 'google.com', 'google.pl', 'googlesyndication.com', 'google-analytics.com')
STUB = r"""(function(){ window.__stubLoads = (window.__stubLoads||0) + 1; window.__stubSeen = [];
 function handle(a){ if(!a || typeof a.length !== 'number') return; window.__stubSeen.push(a[0] + ':' + a[1]);
   if(a[0]==='event' && a[1]==='conversion'){ var p = a[2].send_to.split('/'); var i = new Image(); i.src = 'https://www.googleadservices.com/pagead/conversion/' + p[0].slice(3) + '/?label=' + p[1] + '&url=' + encodeURIComponent(location.href); }
   if(a[0]==='config'){ var j = new Image(); j.src = 'https://googleads.g.doubleclick.net/pagead/viewthroughconversion/' + a[1].slice(3) + '/?stub=1&url=' + encodeURIComponent(location.href); } }
 var dl = window.dataLayer = window.dataLayer || []; for(var k=0;k<dl.length;k++) handle(dl[k]);
 var push = dl.push; dl.push = function(x){ handle(x); return push.apply(dl, arguments); }; })();"""
GIF = bytes.fromhex('47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b')
INIT = r"""window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + (e.blockedURI||'inline')));
window.__blocked = []; window.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[href]'); if(!a) return; const h = a.getAttribute('href')||'';
  if(/^tel:/.test(h) || /wa\.me/.test(a.href)){ window.__blocked.push(e.defaultPrevented); e.preventDefault(); } }, false);"""
results = []
def check(name, ok, detail=''):
    results.append((bool(ok), name, detail))

DL = """() => (window.dataLayer||[]).map(a => { try { const x = Array.prototype.slice.call(a); return JSON.stringify(x[0]==='js' ? ['js'] : x); } catch(e){ return JSON.stringify(a); } })"""
CONV = """() => (window.dataLayer||[]).filter(a => a[0]==='event' && a[1]==='conversion').map(a => a[2])"""

async def new_page(b, mob, block_tag=False, perms=True):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844} if mob else {'width': 1440, 'height': 900}, is_mobile=mob, has_touch=mob)
    if perms: await ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=B.rstrip('/'))
    await ctx.add_init_script(INIT)
    reqs = []
    async def gtm(r):
        if block_tag: await r.abort()
        else: await r.fulfill(status=200, content_type='application/javascript', body=STUB)
    async def pix(r):
        await r.fulfill(status=200, content_type='image/gif', body=GIF)
    await ctx.route('https://www.googletagmanager.com/**', gtm)
    for h in ('https://www.googleadservices.com/**', 'https://googleads.g.doubleclick.net/**', 'https://www.google.com/**', 'https://www.google.pl/**', 'https://*.doubleclick.net/**', 'https://pagead2.googlesyndication.com/**'):
        await ctx.route(h, pix)
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('request', lambda r: reqs.append(r.url) if any(g in r.url for g in GOOGLE) else None)
    return ctx, pg, reqs, errs

def google(reqs): return [u for u in reqs if any(g in u for g in GOOGLE)]

async def click(pg, sel, wait=150):
    await pg.evaluate(f"document.querySelector({json.dumps(sel)}).scrollIntoView({{block:'center'}})")
    await pg.click(sel, force=True); await pg.wait_for_timeout(wait)

async def run(b, mob, path=''):
    tag = ('mobile' if mob else 'desktop') + ' /' + path
    tel_sel = ['.hero .js-call', '.call-line a', '.final .js-call', 'footer .js-phone', 'footer .js-phone2'] + (['.dock .js-call'] if mob else [])

    # 1. first visit, no decision
    ctx, pg, reqs, errs = await new_page(b, mob)
    await pg.goto(B + path + '?gclid=TEST-GCLID&utm_source=google&utm_campaign=wy', wait_until='networkidle'); await pg.wait_for_timeout(1500)
    check(f'{tag}: banner shown on first visit', await pg.is_visible('#consent'))
    check(f'{tag}: no Google request before a decision (basic mode)', not google(reqs), google(reqs))
    dl = await pg.evaluate(DL)
    check(f'{tag}: consent default denied queued, no config/event before consent', dl[:1] == ['["consent","default",{"ad_storage":"denied","ad_user_data":"denied","ad_personalization":"denied","analytics_storage":"denied"}]'] and not any('"config"' in x or '"event"' in x for x in dl), dl)
    await click(pg, '.hero .js-call')
    check(f'{tag}: tel click before consent sends nothing', not await pg.evaluate(CONV) and not google(reqs))
    en = await pg.get_attribute('.langs-nav a[hreflang="en"]' if not path else '.langs-nav a[hreflang="pl"]', 'href')
    check(f'{tag}: ad-click parameters kept on the language switch', 'gclid=TEST-GCLID' in en and 'utm_campaign=wy' in en, en)
    # 2. refuse
    await click(pg, '#consent-no')
    check(f'{tag}: refusal hides the banner and is stored', not await pg.is_visible('#consent') and (await pg.evaluate("JSON.parse(localStorage.getItem('wyniose-consent-v1')).ads")) == 'denied')
    for s in tel_sel: await click(pg, s, 50)
    await pg.fill('#k-co', 'szafa'); await click(pg, '#send')
    check(f'{tag}: after refusal no conversions and no Google requests', not await pg.evaluate(CONV) and not google(reqs), google(reqs))
    await pg.reload(wait_until='networkidle'); await pg.wait_for_timeout(800)
    check(f'{tag}: after refusal + reload no banner, still no Google request', not await pg.is_visible('#consent') and not google(reqs))
    check(f'{tag}: CTAs not blocked without consent', all(v is False for v in await pg.evaluate('window.__blocked')), await pg.evaluate('window.__blocked'))
    check(f'{tag}: no CSP violations / errors (refusal path)', not await pg.evaluate('window.__csp') and not errs, (await pg.evaluate('window.__csp'), errs))
    await ctx.close()

    # 3. consent
    ctx, pg, reqs, errs = await new_page(b, mob)
    await pg.goto(B + path + '?gclid=TEST-GCLID', wait_until='networkidle'); await pg.wait_for_timeout(800)
    await click(pg, '.hero .js-call')          # a click before consent must not be replayed later
    await click(pg, '#consent-yes', 600)
    gtm = [u for u in reqs if 'googletagmanager.com' in u]
    check(f'{tag}: Google tag requested exactly once after consent', len(gtm) == 1 and await pg.evaluate('document.querySelectorAll("script[src*=googletagmanager]").length') == 1 and 'id=AW-18540345955' in gtm[0], gtm)
    dl = await pg.evaluate(DL)
    upd = [x for x in dl if x.startswith('["consent","update"')]
    check(f'{tag}: consent update grants only ad_storage + ad_user_data', upd == ['["consent","update",{"ad_storage":"granted","ad_user_data":"granted"}]'], upd)
    check(f'{tag}: exactly one config, after default and update', [x for x in dl if '"config"' in x] == ['["config","AW-18540345955"]'] and dl.index('["config","AW-18540345955"]') > dl.index(upd[0]), dl)
    check(f'{tag}: click made before consent not replayed', not await pg.evaluate(CONV))
    # each tel CTA: one event per click (3.1 s apart, the dedupe window is 3 s)
    per = []
    for s in tel_sel:
        before = len(await pg.evaluate(CONV)); await click(pg, s, 3150); after = await pg.evaluate(CONV)
        per.append((s, len(after) - before, after[-1] if len(after) > before else None))
    check(f'{tag}: every tel CTA sends exactly one Telefon conversion', all(n == 1 and e == {'send_to': TEL} for _, n, e in per), per)
    before = len(await pg.evaluate(CONV)); await pg.dblclick('.hero .js-call', force=True); await pg.wait_for_timeout(200)
    check(f'{tag}: double tap = one event', len(await pg.evaluate(CONV)) - before == 1)
    # job card -> WhatsApp
    await pg.click('label[for="o2"]', force=True); await pg.click('label[for="f4"]', force=True); await pg.click('label[for="l1"]', force=True)
    await pg.fill('#k-co', 'szafa, wersalka'); await pg.dispatch_event('#k-co', 'input'); await pg.wait_for_timeout(3200)
    before = len(await pg.evaluate(CONV)); await click(pg, '#send', 300); after = await pg.evaluate(CONV)
    check(f'{tag}: WhatsApp button sends exactly one WhatsApp conversion', len(after) - before == 1 and after[-1] == {'send_to': WA}, after[before:])
    href = await pg.get_attribute('#send', 'href')
    check(f'{tag}: WhatsApp message carries items, object, floor and lift', all(x in href for x in (['szafa', 'wersalka', 'dom', 'IV', 'bez%20windy'] if not path else ['szafa', 'wersalka', 'house', '4th', 'no%20lift'])), href[:160])
    check(f'{tag}: conversion events carry only send_to (no message, phone, address)', all(set(e.keys()) == {'send_to'} for e in after))
    pix = [u for u in reqs if 'googleadservices.com/pagead/conversion' in u]
    check(f'{tag}: conversion hits reach Google with the right labels, nothing personal in them', any('XIrxCOOG3KsdEOP03IhF' in u for u in pix) and any('HsRYCKHHzKsdEOP03IhF' in u for u in pix) and not any('szafa' in u or '516721072' in u for u in pix), pix[:2])
    # copy: diagnostic only
    before = len(await pg.evaluate(CONV)); await click(pg, '#copy', 600)
    check(f'{tag}: copying is not a conversion, only a local diagnostic event', len(await pg.evaluate(CONV)) == before and any(d['type'] == 'copy_job_card' for d in await pg.evaluate('window.__wyDiag')), await pg.evaluate('window.__wyDiag.map(d=>d.type)'))
    check(f'{tag}: gclid visible to the tag after consent', any('TEST-GCLID' in u for u in reqs if 'doubleclick' in u or 'googleadservices' in u))
    # 4. reload: stored consent, tag once, nothing replayed
    n0 = len(reqs); await pg.reload(wait_until='networkidle'); await pg.wait_for_timeout(800)
    gtm2 = [u for u in reqs[n0:] if 'googletagmanager.com' in u]
    check(f'{tag}: reload with stored consent: no banner, tag once, no replayed conversions', not await pg.is_visible('#consent') and len(gtm2) == 1 and not await pg.evaluate(CONV) and await pg.evaluate('document.querySelectorAll("script[src*=googletagmanager]").length') == 1)
    # 5. withdraw
    await pg.evaluate("document.cookie = '_gcl_au=1.1.test; path=/'")
    await click(pg, '#consent-open', 200)
    check(f'{tag}: "Ustawienia cookie" reopens the banner', await pg.is_visible('#consent'))
    await click(pg, '#consent-no', 300)
    dl = await pg.evaluate(DL)
    check(f'{tag}: withdrawal pushes consent update denied and removes _gcl cookies', dl[-1] == '["consent","update",{"ad_storage":"denied","ad_user_data":"denied"}]' and '_gcl_au' not in await pg.evaluate('document.cookie'), dl[-1])
    before = len(await pg.evaluate(CONV)); await click(pg, '.hero .js-call', 3200); await click(pg, '#send', 200)
    check(f'{tag}: after withdrawal no conversions', len(await pg.evaluate(CONV)) == before)
    check(f'{tag}: CTAs never blocked with consent', all(v is False for v in await pg.evaluate('window.__blocked')))
    check(f'{tag}: no CSP violations / errors (consent path)', not await pg.evaluate('window.__csp') and not errs, (await pg.evaluate('window.__csp'), errs))
    await ctx.close()

    # 6. tag blocked (ad blocker): CTAs still work, no errors
    ctx, pg, reqs, errs = await new_page(b, mob, block_tag=True)
    await pg.goto(B + path, wait_until='networkidle'); await pg.wait_for_timeout(500)
    await click(pg, '#consent-yes', 800)
    await click(pg, '.hero .js-call'); await pg.fill('#k-co', 'szafa'); await pg.dispatch_event('#k-co', 'input'); await click(pg, '#send')
    st = await pg.evaluate('window.__consent.state()')
    check(f'{tag}: tag blocked: CTAs work, failure noted, no page errors', st['failed'] and all(v is False for v in await pg.evaluate('window.__blocked')) and not [e for e in errs if 'ERR_FAILED' not in e and 'Failed to load resource' not in e], (st, errs))
    await ctx.close()

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**LAUNCH)
        for mob in (False, True):
            for path in ('', 'en/'):
                await run(b, mob, path)
        # anchors used by the ads
        pg = await b.new_page(); await pg.goto(B, wait_until='networkidle')
        ids = await pg.evaluate("['uslugi','wycena','droga','faq'].map(i => [i, !!document.getElementById(i)])")
        check('ad anchors #uslugi #wycena #droga #faq exist', all(x[1] for x in ids), ids)
        await b.close()
    ok = sum(1 for r in results if r[0])
    print(f'PASSED {ok}/{len(results)}')
    for r in results:
        if not r[0]: print('FAIL', r[1], json.dumps(r[2], ensure_ascii=False, default=str)[:400])
    sys.exit(0 if ok == len(results) else 1)

asyncio.run(main())
