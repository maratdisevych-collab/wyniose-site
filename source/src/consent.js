/* Google Ads with Consent Mode v2, basic implementation
   (developers.google.com/tag-platform/security/guides/consent?consentmode=basic).
   - Nothing from Google is requested until the visitor agrees. After a refusal nothing is requested at all.
   - Consent defaults (all denied) are queued before any config or event; on consent only the granted
     categories are updated (ad_storage, ad_user_data). ad_personalization and analytics_storage stay denied.
   - Withdrawal ("Ustawienia cookie" -> "Nie zgadzam się") after the tag was loaded: consent update denied, _gcl cookies
     removed, then the page reloads, so no Google code keeps running on it.
   - Conversions, secondary actions in Google Ads, one per click, no value, nothing personal attached:
       Telefon  = a real click on any tel: link (header, hero, cards, final CTA, mobile dock, footer)
       WhatsApp = a real click on any wa.me link (header, hero, cards, dock, "Wyślij na WhatsApp" in the job card)
     Clicks made before consent are never replayed. Navigation is never delayed or blocked.
   - Calls from website (optional ads.call): the phone snippet runs in the same tag after consent; see callNumber().
   - Copying the job card is a local diagnostic event only (window.__wyDiag), never sent to Google.
   - The primary goal, calls from ads of 60 s or more, is measured inside Google Ads; nothing here.
   Config: window.SITE.ads = {id: "AW-…", tel: "AW-…/label", wa: "AW-…/label", call: "AW-…/label" (optional)}. */
(function(){
  var SITE = window.SITE || {}, A = SITE.ads || {};
  var ID_OK = /^AW-\d{6,}$/, SEND_OK = /^AW-\d{6,}\/[A-Za-z0-9_-]+$/;
  var enabled = ID_OK.test(A.id || '') && SEND_OK.test(A.tel || '') && SEND_OK.test(A.wa || '') && A.tel !== A.wa;
  var CALL = enabled && SEND_OK.test(A.call || '') && A.call !== A.tel && A.call !== A.wa && !!SITE.phone;
  var banner = document.getElementById('consent'), openBtn = document.getElementById('consent-open');
  var diag = window.__wyDiag = window.__wyDiag || [];
  function note(type, extra){ var d = {type: type, t: Date.now()}; for(var k in extra) d[k] = extra[k]; diag.push(d); }

  /* keep ad-click parameters (gclid, gbraid, wbraid, gad_*, utm_*) on links to the site's other pages (language switch,
     menu, service pages), without storing them anywhere, so the tag can still read them from the address if consent is
     given on a later page. Not done once the visitor has refused. */
  var AD_PARAMS = /^(gclid|gbraid|wbraid|gad_source|gad_campaignid|utm_[a-z]+)$/;
  function adQuery(){
    try { var q = new URLSearchParams(location.search), keep = new URLSearchParams();
      q.forEach(function(v, k){ if(AD_PARAMS.test(k)) keep.append(k, v); }); var s = keep.toString(); return s ? '?' + s : ''; } catch(e){ return ''; }
  }
  var aq = adQuery();
  function carryAdParams(){
    if(!aq) return;
    [].forEach.call(document.querySelectorAll('a[href]'), function(a){
      var h = a.getAttribute('href') || '', u;
      if(!h || h.charAt(0) === '#' || h.indexOf('?') >= 0 || a.hasAttribute('download')) return;
      try { u = new URL(h, location.href); } catch(e){ return; }
      if(u.origin !== location.origin || /\.(pdf|png|jpe?g|svg|webp|ico|txt|xml|js|css)$/i.test(u.pathname)) return;
      a.setAttribute('href', h.replace(/(#.*)?$/, aq + '$1'));
    });
  }

  window.addEventListener('wyniose:copied', function(){ note('copy_job_card'); });   // diagnostic only

  var KEY = 'wyniose-consent-v1', MAX_AGE = 365*24*3600*1000;
  function read(){
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if(v && (v.ads === 'granted' || v.ads === 'denied') && Date.now() - (v.t || 0) < MAX_AGE) return v.ads; } catch(e){}
    return null;
  }
  if(!enabled || read() !== 'denied') carryAdParams();

  if(!enabled){ if(banner) banner.hidden = true; if(openBtn) openBtn.hidden = true; window.__consent = {enabled: false}; return; }
  function save(state){ try { localStorage.setItem(KEY, JSON.stringify({ads: state, t: Date.now()})); } catch(e){} }

  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('consent', 'default', {ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'denied'});
  gtag('set', 'ads_data_redaction', true);

  var loaded = false, granted = false, failed = false;
  function load(){
    if(loaded) return; loaded = true;
    gtag('js', new Date());
    gtag('config', A.id);
    if(CALL) gtag('config', A.call, {phone_conversion_number: String(SITE.phone), phone_conversion_callback: callNumber});
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(A.id);
    s.onerror = function(){ failed = true; note('tag_blocked'); };   // ad blocker or network: the buttons keep working
    document.head.appendChild(s);
  }
  /* Calls from website: Google answers the config above with a forwarding number only for visitors who came from an ad
     (support.google.com/google-ads/answer/6095883, callback variant, so the shown and the dialled number change together).
     Only the call buttons change. The footer ("Telefon / WhatsApp"), the WhatsApp label in the drawing and every wa.me
     link keep the real number. Google measures the call itself; nothing is timed or sent from here. */
  function callNumber(formatted, mobile){
    if(!granted) return;
    var shown = String(formatted || '').trim(), d = String(mobile || '').replace(/\D/g, ''), dial;
    if(/^\+/.test(shown)) dial = '+' + shown.replace(/\D/g, '');
    else if(d.length === 11 && d.indexOf('48') === 0) dial = '+' + d;
    else if(d.length === 9) dial = '+48' + d;
    else dial = d;
    if(!shown || !/^\+?\d{6,15}$/.test(dial)) return;
    [].forEach.call(document.querySelectorAll('a.js-call'), function(a){
      if(a.closest('footer')) return;
      a.setAttribute('href', 'tel:' + dial);
      if(a.classList.contains('js-phone')) a.textContent = shown;
      [].forEach.call(a.querySelectorAll('.js-phone'), function(el){ el.textContent = shown; });
    });
    note('call_number', {swapped: true});
  }
  function clearAdCookies(){
    var host = location.hostname, base = host.replace(/^www\./, '');
    document.cookie.split(';').forEach(function(c){
      var n = c.split('=')[0].trim(); if(!/^(_gcl_|_gac_|FPGCL|gwcc)/.test(n)) return;
      ['', '; domain=' + host, '; domain=.' + base].forEach(function(d){ document.cookie = n + '=; Max-Age=0; path=/' + d; });
    });
  }
  function decide(state, fromUser){
    var was = granted;
    granted = state === 'granted';
    if(fromUser) save(state);
    if(granted){ if(!was) gtag('consent', 'update', {ad_storage: 'granted', ad_user_data: 'granted'}); load(); }
    else {
      if(was || loaded) gtag('consent', 'update', {ad_storage: 'denied', ad_user_data: 'denied'});
      clearAdCookies();
      /* withdrawal after the tag was loaded on this page: a loaded Google tag keeps its own listeners (automatic events)
         and would go on sending cookieless pings, which basic mode does not allow; reloading removes it from the page */
      if(loaded && fromUser){ note('consent', {state: state, by: 'visitor', reload: true}); if(banner) banner.hidden = true; try { location.reload(); } catch(e){} return; }
    }
    note('consent', {state: state, by: fromUser ? 'visitor' : 'stored'});
    if(banner) banner.hidden = true;
    document.documentElement.classList.remove('consent-open');
  }
  function ask(focus){
    if(!banner) return;
    banner.hidden = false; document.documentElement.classList.add('consent-open');
    var b = focus && banner.querySelector('button'); if(b) try { b.focus({preventScroll: true}); } catch(e){}
  }

  /* one listener for the whole page, one event per click; a second tap on the same action within 3 s is ignored */
  var last = {};
  function conversion(kind){
    if(!granted || !loaded) return false;
    var now = Date.now(); if(last[kind] && now - last[kind] < 3000) return false;
    last[kind] = now;
    gtag('event', 'conversion', {send_to: A[kind]});
    note('conversion', {kind: kind});
    return true;
  }
  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null; if(!a) return;
    var href = a.getAttribute('href') || '';
    if(/^tel:/i.test(href)) conversion('tel');
    else if(/^https:\/\/(wa\.me|api\.whatsapp\.com)\//i.test(a.href)) conversion('wa');
  }, true);

  if(banner){
    var yes = document.getElementById('consent-yes'), no = document.getElementById('consent-no');
    if(yes) yes.addEventListener('click', function(){ decide('granted', true); });
    if(no) no.addEventListener('click', function(){ decide('denied', true); });
  }
  if(openBtn){ openBtn.hidden = false; openBtn.addEventListener('click', function(){ ask(true); }); }

  var stored = read();
  if(stored) decide(stored, false); else ask(false);

  window.__consent = {enabled: true, state: function(){ return {granted: granted, loaded: loaded, failed: failed, stored: read()}; }};
})();
