"""Consent Mode v2 basic + Google Ads conversion checks against the built site served with production headers (:8766).

Every page that carries the cookie banner is checked on a desktop and a phone viewport:
  A  first visit, no decision: banner shown, no Google request, consent default (4 x denied) queued first,
     every visible tel:/WhatsApp CTA works and sends nothing, ad-click parameters carried to the site's other pages
  B  refusal: stored, no Google request and no conversion on any CTA, nothing after a reload, parameters no longer carried
  C  consent: tag requested once, update grants only ad_storage + ad_user_data, config once after default and update,
     a click made before consent is not replayed, every visible CTA sends exactly one conversion with its own label
     and opens exactly one WhatsApp window, double tap = one event, job card (home): filling it sends nothing,
     "Wyślij na WhatsApp" sends one WhatsApp conversion with nothing personal in it, copying is diagnostic only;
     reload and a move to another page: no banner, tag once, one event per click (no duplicated listeners)
  D  withdrawal: consent update denied pushed, _gcl cookies removed, the page reloads so the loaded Google tag is gone,
     no tag and no conversion afterwards; consenting again works
  E  tag blocked (ad blocker): CTAs still work, failure noted, no page errors
  F  Google slow: CTAs work at once, nothing waits for the tag
  Calls from website: the phone snippet config is queued only after consent; when Google answers (stubbed for an ad
     visitor) the call buttons show and dial the forwarding number, while the footer, WhatsApp links and the drawing keep
     the real number; nothing changes before consent, after refusal or after withdrawal (gwcc removed)
Google is unreachable from here, so gtag.js is replaced by a stub that behaves like the tag for what we test:
it reads the dataLayer and fires one image request per config / conversion to Google hosts (allowed by our CSP).
The stub cannot show what the real Google tag collects on its own (automatic events, user-provided data):
that depends on the Google tag settings in the Google Ads account and is checked on the live site."""
import asyncio, json, os, sys
from playwright.async_api import async_playwright
_CH = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
LAUNCH = dict(args=['--no-sandbox'], **({'executable_path': _CH} if os.path.exists(_CH) else {}))

B = 'http://127.0.0.1:8766/'
SITE_DIR = os.environ.get('SITE_DIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
TEL = 'AW-18540345955/XIrxCOOG3KsdEOP03IhF'; WA = 'AW-18540345955/HsRYCKHHzKsdEOP03IhF'; CALL = 'AW-18540345955/eMUqCIyw8LAdEOP03IhF'
REAL_TEL, FWD_TEL, FWD_SHOWN = 'tel:+48516721072', 'tel:+48221002030', '+48 22 100 20 30'   # FWD: a made-up forwarding number from the stub
LABEL = {'tel': TEL, 'wa': WA}
GOOGLE = ('googletagmanager.com', 'googleadservices.com', 'doubleclick.net', 'google.com', 'google.pl', 'googlesyndication.com', 'google-analytics.com')
QS = 'utm_source=google&utm_medium=cpc&utm_campaign=wy_test&qa_ad=1'   # qa_ad=1: the stub answers the phone snippet like Google does after an ad click
CANARY = ('qakanarek', 'qaadres')            # typed into the job card; must never reach Google
STUB = r"""(function(){ window.__stubLoads = (window.__stubLoads||0) + 1;
 function handle(a){ if(!a || typeof a.length !== 'number') return;
   if(a[0]==='event' && a[1]==='conversion'){ var p = a[2].send_to.split('/'); var i = new Image(); i.src = 'https://www.googleadservices.com/pagead/conversion/' + p[0].slice(3) + '/?label=' + p[1] + '&url=' + encodeURIComponent(location.href); }
   if(a[0]==='config'){ var j = new Image(); j.src = 'https://googleads.g.doubleclick.net/pagead/viewthroughconversion/' + a[1].slice(3) + '/?stub=1&url=' + encodeURIComponent(location.href);
     var o = a[2]; if(o && typeof o.phone_conversion_callback === 'function' && /qa_ad=1/.test(location.search)) setTimeout(function(){ o.phone_conversion_callback('+48 22 100 20 30', '48221002030'); }, 50); } }
 var dl = window.dataLayer = window.dataLayer || []; for(var k=0;k<dl.length;k++) handle(dl[k]);
 var push = dl.push; dl.push = function(x){ handle(x); return push.apply(dl, arguments); }; })();"""
GIF = bytes.fromhex('47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b')
# the test's own listener runs last (window, bubble): it records every CTA click and whether the site blocked it,
# then cancels tel: navigation (headless Chromium has no phone app). WhatsApp links open their window as usual.
INIT = r"""window.__csp = []; document.addEventListener('securitypolicyviolation', e => window.__csp.push(e.violatedDirective + ' ' + (e.blockedURI||'inline')));
window.__hits = []; window.__blocked = [];
window.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[href]'); if(!a) return; const h = a.getAttribute('href')||'';
  const tel = /^tel:/i.test(h), wa = /^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(a.href); if(!tel && !wa) return;
  window.__hits.push(tel ? 'tel' : 'wa'); window.__blocked.push(e.defaultPrevented); if(tel) e.preventDefault(); }, false);"""
DL = """() => (window.dataLayer||[]).map(a => { try { const x = Array.prototype.slice.call(a); return JSON.stringify(x[0]==='js' ? ['js'] : x); } catch(e){ return JSON.stringify(a); } })"""
CONV = """() => (window.dataLayer||[]).filter(a => a[0]==='event' && a[1]==='conversion').map(a => a[2])"""
NUMBERS = r"""() => ({
  calls: [...document.querySelectorAll('a.js-call')].map(a => ({footer: !!a.closest('footer'), href: a.getAttribute('href'), text: (a.classList.contains('js-phone') ? a : a.querySelector('.js-phone') || {textContent: ''}).textContent.trim()})),
  wa: [...document.querySelectorAll('a[href]')].filter(a => /wa\.me|api\.whatsapp/.test(a.href)).map(a => a.href.split('?')[0]),
  other: [...document.querySelectorAll('.js-phone, .js-phone2')].filter(el => !el.closest('a.js-call')).map(el => el.textContent.trim()) })"""
CTAS = r"""() => { const out = [];
  document.querySelectorAll('a[href]').forEach((a, i) => { const h = a.getAttribute('href') || '';
    const kind = /^tel:/i.test(h) ? 'tel' : (/^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(a.href) ? 'wa' : null); if(!kind) return;
    const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
    const where = [['#karta','job card'],['.dock','dock'],['header','header'],['footer','footer'],['.side-card','side card'],['.final','final'],['.in-cta','in text'],['.call-line','call line'],['.hero,.sub-hero','hero']].find(w => a.closest(w[0]));
    a.setAttribute('data-qa', 'c' + i);
    out.push({sel: '[data-qa="c' + i + '"]', kind: kind, vis: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden', where: where ? where[1] : 'page'}); });
  return out; }"""
INTERNAL = r"""() => [...document.querySelectorAll('a[href]')].filter(a => { const h = a.getAttribute('href') || '';
  if(!h || h[0] === '#' || a.hasAttribute('download')) return false; let u; try { u = new URL(h, location.href); } catch(e){ return false; }
  return u.origin === location.origin && !/\.(pdf|png|jpe?g|svg|webp|ico|txt|xml|js|css)$/i.test(u.pathname); }).map(a => a.getAttribute('href'))"""

results = []
def check(name, ok, detail=''):
    results.append((bool(ok), name, detail))

def pages():
    out = []
    for root, _, files in os.walk(SITE_DIR):
        if 'index.html' not in files: continue
        if 'id="consent"' not in open(os.path.join(root, 'index.html'), encoding='utf-8').read(): continue
        rel = os.path.relpath(root, SITE_DIR).replace(os.sep, '/')
        out.append('' if rel == '.' else rel + '/')
    return sorted(out, key=lambda p: (p != '', p != 'en/', p))

def google(reqs): return [u for u in reqs if any(g in u for g in GOOGLE)]

async def new_page(b, mob, tag_mode='stub'):
    ctx = await b.new_context(viewport={'width': 390, 'height': 844} if mob else {'width': 1440, 'height': 900}, is_mobile=mob, has_touch=mob)
    await ctx.grant_permissions(['clipboard-read', 'clipboard-write'], origin=B.rstrip('/'))
    await ctx.add_init_script(INIT)
    reqs, popups = [], []
    async def gtm(r):
        if tag_mode == 'blocked': await r.abort(); return
        if tag_mode == 'slow': await asyncio.sleep(6)
        try: await r.fulfill(status=200, content_type='application/javascript', body=STUB)
        except Exception: pass
    async def pix(r): await r.fulfill(status=200, content_type='image/gif', body=GIF)
    async def wa(r): await r.fulfill(status=200, content_type='text/html', body='<p>WhatsApp</p>')
    await ctx.route('https://www.googletagmanager.com/**', gtm)
    for h in ('https://www.googleadservices.com/**', 'https://googleads.g.doubleclick.net/**', 'https://www.google.com/**', 'https://www.google.pl/**', 'https://*.doubleclick.net/**', 'https://pagead2.googlesyndication.com/**'):
        await ctx.route(h, pix)
    await ctx.route('https://wa.me/**', wa); await ctx.route('https://api.whatsapp.com/**', wa)
    ctx.on('page', lambda p: popups.append(p.url))
    ctx.on('request', lambda r: reqs.append(r.url) if any(g in r.url for g in GOOGLE) else None)
    pg = await ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    await pg.clock.install()           # lets the test skip the 3 s double-tap window instead of waiting for it
    return ctx, pg, reqs, popups, errs

async def goto(pg, url):
    await pg.goto(url, wait_until='load'); await pg.wait_for_timeout(400)

async def click(pg, sel, wait=150):
    """Real click (Playwright refuses if something covers the element). True if the CTA click reached the page."""
    await pg.evaluate(f"document.querySelector({json.dumps(sel)}).scrollIntoView({{block:'center'}})")
    n = await pg.evaluate('window.__hits.length')
    try: await pg.click(sel, timeout=4000)
    except Exception: return False
    await pg.wait_for_timeout(wait)
    return await pg.evaluate('window.__hits.length') == n + 1

async def visible_ctas(pg): return [c for c in await pg.evaluate(CTAS) if c['vis']]
async def first_cta(pg, kind): return next(c['sel'] for c in await visible_ctas(pg) if c['kind'] == kind)
async def wait_windows(popups, n, ms=1500):
    for _ in range(ms // 100):
        if len(popups) >= n: return
        await asyncio.sleep(0.1)

async def run(b, mob, path):
    tag = ('mobile' if mob else 'desktop') + ' /' + path
    url = B + path + '?' + QS
    home = path in ('', 'en/')

    # A. first visit, no decision -> then B. refusal
    ctx, pg, reqs, popups, errs = await new_page(b, mob)
    await goto(pg, url)
    check(f'{tag}: A banner shown on first visit', await pg.is_visible('#consent'))
    check(f'{tag}: A no Google request before a decision', not google(reqs), google(reqs))
    dl = await pg.evaluate(DL)
    check(f'{tag}: A consent default (4 x denied) queued first, no config/event', dl[:1] == ['["consent","default",{"ad_storage":"denied","ad_user_data":"denied","ad_personalization":"denied","analytics_storage":"denied"}]'] and not any('"config"' in x or '"event"' in x for x in dl), dl)
    nb = await pg.evaluate(NUMBERS)
    check(f'{tag}: A real phone number everywhere before a decision', all(c['href'] == REAL_TEL for c in nb['calls']), nb['calls'][:3])
    internal = await pg.evaluate(INTERNAL)
    check(f'{tag}: A ad-click parameters carried on every link to another page of the site', internal and all('utm_campaign=wy_test' in h for h in internal), [h for h in internal if 'utm_campaign=wy_test' not in h][:6])
    ctas = await visible_ctas(pg)
    check(f'{tag}: A page has visible call and WhatsApp CTAs', any(c['kind'] == 'tel' for c in ctas) and any(c['kind'] == 'wa' for c in ctas), ctas)
    p0 = len(popups); clicked = [(c['where'], c['kind'], await click(pg, c['sel'])) for c in ctas]
    await wait_windows(popups, p0 + sum(1 for x in clicked if x[1] == 'wa' and x[2]))
    check(f'{tag}: A every visible CTA clickable with the banner open', all(x[2] for x in clicked), [x for x in clicked if not x[2]])
    check(f'{tag}: A CTAs before a decision send nothing', not await pg.evaluate(CONV) and not google(reqs), google(reqs))
    check(f'{tag}: A each WhatsApp click opens exactly one window', len(popups) - p0 == sum(1 for x in clicked if x[1] == 'wa' and x[2]), (len(popups) - p0, clicked))
    await pg.click('#consent-no')
    check(f'{tag}: B refusal hides the banner and is stored', not await pg.is_visible('#consent') and (await pg.evaluate("JSON.parse(localStorage.getItem('wyniose-consent-v1')).ads")) == 'denied')
    for c in ctas: await click(pg, c['sel'], 60)
    if home:
        await pg.fill('#k-co', 'szafa'); await pg.dispatch_event('#k-co', 'input'); await click(pg, '#send')
    check(f'{tag}: B after refusal no conversion and no Google request', not await pg.evaluate(CONV) and not google(reqs), google(reqs))
    await goto(pg, url)
    check(f'{tag}: B after refusal + reload: no banner, no Google request', not await pg.is_visible('#consent') and not google(reqs), google(reqs))
    nb = await pg.evaluate(NUMBERS)
    check(f'{tag}: B after refusal the real phone number stays', all(c['href'] == REAL_TEL for c in nb['calls']), nb['calls'][:3])
    internal = await pg.evaluate(INTERNAL)
    check(f'{tag}: B after refusal ad-click parameters are not carried to other pages', not any('utm_campaign=wy_test' in h for h in internal if 'hreflang' not in h), [h for h in internal if 'utm_campaign' in h][:4])
    check(f'{tag}: B CTAs never blocked without consent', all(v is False for v in await pg.evaluate('window.__blocked')) or not await pg.evaluate('window.__blocked'))
    check(f'{tag}: B no CSP violations / errors', not await pg.evaluate('window.__csp') and not errs, (await pg.evaluate('window.__csp'), errs))
    await ctx.close()

    # C. consent
    ctx, pg, reqs, popups, errs = await new_page(b, mob)
    await goto(pg, url)
    ctas = await visible_ctas(pg)
    first_tel = next(c for c in ctas if c['kind'] == 'tel')
    await click(pg, first_tel['sel'])                  # made before consent: must not be replayed later
    await pg.click('#consent-yes'); await pg.wait_for_timeout(500)
    gtm = [u for u in reqs if 'googletagmanager.com' in u]
    check(f'{tag}: C Google tag requested exactly once after consent', len(gtm) == 1 and await pg.evaluate('document.querySelectorAll("script[src*=googletagmanager]").length') == 1 and 'id=AW-18540345955' in gtm[0], gtm)
    dl = await pg.evaluate(DL)
    upd = [x for x in dl if x.startswith('["consent","update"')]
    check(f'{tag}: C consent update grants only ad_storage + ad_user_data', upd == ['["consent","update",{"ad_storage":"granted","ad_user_data":"granted"}]'], upd)
    cfg = [x for x in dl if '"config"' in x]
    check(f'{tag}: C one tag config and one phone snippet config, after default and update', cfg == ['["config","AW-18540345955"]', '["config","' + CALL + '",{"phone_conversion_number":"+48 516 721 072"}]'] and dl.index(cfg[0]) > dl.index(upd[0]), cfg)
    await pg.wait_for_timeout(200); nb = await pg.evaluate(NUMBERS)
    calls_main, calls_foot = [c for c in nb['calls'] if not c['footer']], [c for c in nb['calls'] if c['footer']]
    check(f'{tag}: C calls from website: call buttons show and dial the forwarding number', calls_main and all(c['href'] == FWD_TEL and c['text'] in ('', FWD_SHOWN) for c in calls_main), calls_main)
    check(f'{tag}: C calls from website: footer, WhatsApp links and other number labels keep the real numbers', all(c['href'] == REAL_TEL and c['text'] == '+48 516 721 072' for c in calls_foot) and nb['wa'] and all(w == 'https://wa.me/48516721072' for w in nb['wa']) and all(t in ('+48 516 721 072', '+48 791 645 395') for t in nb['other']), nb)
    check(f'{tag}: C click made before consent not replayed', not await pg.evaluate(CONV))
    per = []
    for c in ctas:
        await pg.clock.fast_forward(3100)          # outside the double-tap window
        n0, p0 = len(await pg.evaluate(CONV)), len(popups)
        ok = await click(pg, c['sel'], 200)
        if c['kind'] == 'wa': await wait_windows(popups, p0 + 1)
        new = (await pg.evaluate(CONV))[n0:]
        per.append({'where': c['where'], 'kind': c['kind'], 'clicked': ok, 'events': new, 'windows': len(popups) - p0})
    bad = [p for p in per if not (p['clicked'] and p['events'] == [{'send_to': LABEL[p['kind']]}] and p['windows'] == (1 if p['kind'] == 'wa' else 0))]
    check(f'{tag}: C every visible CTA: exactly one conversion with its own label, one WhatsApp window', not bad, bad)
    await pg.clock.fast_forward(3100)
    n0 = len(await pg.evaluate(CONV)); await pg.dblclick(first_tel['sel']); await pg.wait_for_timeout(200)
    check(f'{tag}: C double tap = one event', len(await pg.evaluate(CONV)) - n0 == 1)
    if home:
        await pg.clock.fast_forward(3100)
        n0 = len(await pg.evaluate(CONV))
        await pg.evaluate("document.getElementById('karta').scrollIntoView()")
        await pg.click('label[for="o2"]'); await pg.click('label[for="f4"]'); await pg.click('label[for="l1"]')
        await pg.fill('#k-co', 'szafa, ' + CANARY[0]); await pg.fill('#k-area', CANARY[1] + ' 12'); await pg.wait_for_timeout(300)
        check(f'{tag}: C opening and filling the job card sends nothing', len(await pg.evaluate(CONV)) == n0)
        p0 = len(popups); ok = await click(pg, '#send', 300); await wait_windows(popups, p0 + 1); after = await pg.evaluate(CONV)
        check(f'{tag}: C "Wyślij na WhatsApp" = one WhatsApp conversion, one window', ok and after[n0:] == [{'send_to': WA}] and len(popups) - p0 == 1, (after[n0:], len(popups) - p0))
        href = await pg.get_attribute('#send', 'href')
        check(f'{tag}: C WhatsApp message carries the job card (items, object, floor, lift)', all(x in href for x in ((CANARY[0], 'dom', 'IV', 'bez%20windy') if not path else (CANARY[0], 'house', '4th', 'no%20lift'))), href[:160])
        hits = google(reqs)
        check(f'{tag}: C nothing from the job card, the WhatsApp link or a phone number in any Google request', not any(k in u for u in hits for k in CANARY + ('wa.me', 'text%3D', '516721072', 'szafa')), [u for u in hits if any(k in u for k in CANARY + ('wa.me', 'szafa'))][:2])
        n0 = len(await pg.evaluate(CONV)); await pg.click('#copy'); await pg.wait_for_timeout(400)
        check(f'{tag}: C copying the job card is not a conversion, only a local diagnostic note', len(await pg.evaluate(CONV)) == n0 and any(d['type'] == 'copy_job_card' for d in await pg.evaluate('window.__wyDiag')), await pg.evaluate('window.__wyDiag.map(d=>d.type)'))
    pix = [u for u in reqs if 'googleadservices.com/pagead/conversion' in u]
    check(f'{tag}: C conversion hits reach Google with the right labels', any('XIrxCOOG3KsdEOP03IhF' in u for u in pix) and any('HsRYCKHHzKsdEOP03IhF' in u for u in pix), pix[:2])
    check(f'{tag}: C ad-click parameters visible to the tag after consent', any('wy_test' in u for u in reqs if 'doubleclick' in u))
    # reload: stored consent, tag once, nothing replayed
    n0 = len(reqs); await goto(pg, url)
    gtm2 = [u for u in reqs[n0:] if 'googletagmanager.com' in u]
    check(f'{tag}: C reload with stored consent: no banner, tag once, nothing replayed', not await pg.is_visible('#consent') and len(gtm2) == 1 and not await pg.evaluate(CONV) and await pg.evaluate('document.querySelectorAll("script[src*=googletagmanager]").length') == 1)
    # move to another page of the site by a real click
    target = await pg.evaluate("""() => { const a = [...document.querySelectorAll('footer a[href], .side-links a[href], .crumbs a[href], .langs-nav a[href]')].find(a => { try { const u = new URL(a.href); return u.origin === location.origin && u.pathname !== location.pathname && !/polityka/.test(u.pathname) && a.getBoundingClientRect().width > 0; } catch(e){ return false; } }); if(!a) return null; a.setAttribute('data-qa', 'nav'); return a.getAttribute('href'); }""")
    if target:
        n0 = len(reqs)
        await pg.evaluate("document.querySelector('[data-qa=nav]').scrollIntoView({block:'center'})")
        async with pg.expect_navigation(): await pg.click('[data-qa=nav]')
        await pg.wait_for_timeout(400)
        gtm3 = [u for u in reqs[n0:] if 'googletagmanager.com' in u]
        nc = [c for c in await visible_ctas(pg) if c['kind'] == 'tel'][0]
        await pg.clock.fast_forward(3100); await click(pg, nc['sel'], 200)
        check(f'{tag}: C next page ({target.split("?")[0]}): no banner, tag once, one event per click', not await pg.is_visible('#consent') and len(gtm3) == 1 and await pg.evaluate(CONV) == [{'send_to': TEL}], (gtm3, await pg.evaluate(CONV)))
        check(f'{tag}: C next page keeps the ad-click parameters in its address', 'utm_campaign=wy_test' in pg.url, pg.url)
        await goto(pg, url)
    check(f'{tag}: C CTAs never blocked with consent', all(v is False for v in await pg.evaluate('window.__blocked')))
    check(f'{tag}: C no CSP violations / errors', not await pg.evaluate('window.__csp') and not errs, (await pg.evaluate('window.__csp'), errs))

    # D. withdrawal
    await pg.evaluate("document.cookie = '_gcl_au=1.1.test; path=/'; document.cookie = 'gwcc=%5B%22test%22%5D; path=/'")
    await pg.evaluate("""() => { sessionStorage.removeItem('qa_dl'); const dl = window.dataLayer, push = dl.push;
      dl.push = function(x){ try { const s = JSON.parse(sessionStorage.getItem('qa_dl') || '[]'); s.push(JSON.stringify(Array.prototype.slice.call(x))); sessionStorage.setItem('qa_dl', JSON.stringify(s)); } catch(e){} return push.apply(dl, arguments); }; }""")
    await pg.evaluate("document.getElementById('consent-open').scrollIntoView({block:'center'})")
    await pg.click('#consent-open'); await pg.wait_for_timeout(200)
    check(f'{tag}: D "Ustawienia cookie" reopens the banner', await pg.is_visible('#consent'))
    n0 = len(reqs); reloaded = True
    try:
        async with pg.expect_navigation(timeout=4000): await pg.click('#consent-no')
    except Exception: reloaded = False
    await pg.wait_for_timeout(500)
    pushed = json.loads(await pg.evaluate("sessionStorage.getItem('qa_dl') || '[]'"))
    check(f'{tag}: D withdrawal pushes consent update denied and removes _gcl cookies', '["consent","update",{"ad_storage":"denied","ad_user_data":"denied"}]' in pushed and '_gcl_au' not in await pg.evaluate('document.cookie'), pushed)
    check(f'{tag}: D withdrawal reloads the page, so the already loaded Google tag stops running', reloaded and not [u for u in reqs[n0:] if 'googletagmanager.com' in u] and await pg.evaluate('document.querySelectorAll("script[src*=googletagmanager]").length') == 0 and not any('"config"' in x for x in await pg.evaluate(DL)), (reloaded, [u for u in reqs[n0:] if 'googletagmanager' in u]))
    nb = await pg.evaluate(NUMBERS)
    check(f'{tag}: D after withdrawal the real phone number is back and the gwcc cookie is gone', all(c['href'] == REAL_TEL for c in nb['calls']) and 'gwcc' not in await pg.evaluate('document.cookie'), (nb['calls'][:2], await pg.evaluate('document.cookie')))
    check(f'{tag}: D after withdrawal: banner closed, refusal stored', not await pg.is_visible('#consent') and (await pg.evaluate("JSON.parse(localStorage.getItem('wyniose-consent-v1')).ads")) == 'denied')
    n0, c0 = len(reqs), len(await pg.evaluate(CONV))
    await pg.clock.fast_forward(3100); await click(pg, await first_cta(pg, 'tel'), 200)
    check(f'{tag}: D after withdrawal no conversion and no Google request', len(await pg.evaluate(CONV)) == c0 and not google(reqs[n0:]), google(reqs[n0:]))
    await pg.evaluate("document.getElementById('consent-open').scrollIntoView({block:'center'})")
    await pg.click('#consent-open'); await pg.click('#consent-yes'); await pg.wait_for_timeout(500)
    await pg.clock.fast_forward(3100); c0 = len(await pg.evaluate(CONV)); await click(pg, await first_cta(pg, 'tel'), 200)
    check(f'{tag}: D consenting again loads the tag once and measures again', len([u for u in reqs[n0:] if 'googletagmanager.com' in u]) == 1 and (await pg.evaluate(CONV))[c0:] == [{'send_to': TEL}])
    check(f'{tag}: D no CSP violations / errors', not await pg.evaluate('window.__csp') and not errs, (await pg.evaluate('window.__csp'), errs))
    await ctx.close()

    # E. tag blocked (ad blocker); F. Google slow
    for mode in ('blocked', 'slow'):
        ctx, pg, reqs, popups, errs = await new_page(b, mob, tag_mode=mode)
        await goto(pg, url)
        await pg.click('#consent-yes'); await pg.wait_for_timeout(300 if mode == 'slow' else 800)
        ctas = await visible_ctas(pg)
        t, w = next(c for c in ctas if c['kind'] == 'tel'), next(c for c in ctas if c['kind'] == 'wa')
        p0 = len(popups); ok = [await click(pg, t['sel']), await click(pg, w['sel'], 300)]; await wait_windows(popups, p0 + 1)
        st = await pg.evaluate('window.__consent.state()')
        real_errs = [e for e in errs if 'ERR_FAILED' not in e and 'Failed to load resource' not in e]
        name = 'E tag blocked' if mode == 'blocked' else 'F Google slow'
        check(f'{tag}: {name}: call and WhatsApp work at once, not blocked, no page errors', all(ok) and len(popups) - p0 == 1 and all(v is False for v in await pg.evaluate('window.__blocked')) and not real_errs and (st['failed'] if mode == 'blocked' else True), (ok, len(popups) - p0, st, real_errs))
        await ctx.close()

async def main():
    ps = pages()
    async with async_playwright() as pw:
        b = await pw.chromium.launch(**LAUNCH)
        sem = asyncio.Semaphore(int(os.environ.get('QA_PARALLEL', '4')))
        async def one(mob, p):
            async with sem:
                try: await run(b, mob, p)
                except Exception as e: check(f"{'mobile' if mob else 'desktop'} /{p}: scenario crashed", False, repr(e)[:300])
        await asyncio.gather(*[one(mob, p) for mob in (False, True) for p in ps])
        # anchors used by the ads
        pg = await b.new_page(); await pg.goto(B, wait_until='load')
        ids = await pg.evaluate("['uslugi','wycena','droga','faq'].map(i => [i, !!document.getElementById(i)])")
        check('ad anchors #uslugi #wycena #droga #faq exist', all(x[1] for x in ids), ids)
        await b.close()
    ok = sum(1 for r in results if r[0])
    print(f'pages: {len(ps)} x 2 viewports')
    print(f'PASSED {ok}/{len(results)}')
    for r in results:
        if not r[0]: print('FAIL', r[1], json.dumps(r[2], ensure_ascii=False, default=str)[:400])
    if os.environ.get('QA_JSON'):
        json.dump([{'ok': r[0], 'name': r[1], 'detail': json.dumps(r[2], ensure_ascii=False, default=str)[:600]} for r in results], open(os.environ['QA_JSON'], 'w'), ensure_ascii=False, indent=1)
    sys.exit(0 if ok == len(results) else 1)

asyncio.run(main())
