/* Page behaviour: contact config, the pen, the job card. Strings come from window.L, contact data from window.SITE. */
(function(){
  var L = window.L || {}, SITE = window.SITE || {};
  var $ = function(id){ return document.getElementById(id); };
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var header = $('top');
  function setHH(){ if(header) document.documentElement.style.setProperty('--hh', header.offsetHeight + 'px'); }
  setHH(); addEventListener('resize', setHH);

  /* contact data: filled in config, otherwise placeholders stay */
  var digits = function(s){ return String(s || '').replace(/[^\d+]/g, ''); };
  var phone = digits(SITE.phone), wa = digits(SITE.whatsapp || SITE.phone).replace(/^\+/, '');
  var phoneText = SITE.phone ? String(SITE.phone) : '+48 ··· ··· ···';
  Array.prototype.forEach.call(document.querySelectorAll('.js-phone'), function(el){ el.textContent = phoneText; });
  /* every WhatsApp button opens the chat with a short greeting; without a number it stays a link to the job card */
  if(wa){
    var waHref = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(L.waText || '');
    Array.prototype.forEach.call(document.querySelectorAll('.js-wa'), function(a){ a.setAttribute('href', waHref); a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener'); });
  }
  if(phone){
    Array.prototype.forEach.call(document.querySelectorAll('.js-call'), function(a){ a.setAttribute('href', 'tel:' + phone); });
    Array.prototype.forEach.call(document.querySelectorAll('.ph-phone'), function(el){ el.hidden = true; });
  }
  if(SITE.email){ Array.prototype.forEach.call(document.querySelectorAll('.js-email'), function(el){ el.innerHTML = ''; var a = document.createElement('a'); a.href = 'mailto:' + SITE.email; a.textContent = SITE.email; el.appendChild(a); }); }
  var co = SITE.company;
  if(co && typeof co === 'object') co = [co.name, co.address, co.nip ? 'NIP ' + co.nip : '', co.regon ? 'REGON ' + co.regon : ''].filter(Boolean).join(', ');
  if(co){ Array.prototype.forEach.call(document.querySelectorAll('.js-company'), function(el){ el.textContent = co; }); }
  if(SITE.phone2){
    Array.prototype.forEach.call(document.querySelectorAll('.js-phone2'), function(a){ a.textContent = SITE.phone2; a.setAttribute('href', 'tel:' + digits(SITE.phone2)); });
    Array.prototype.forEach.call(document.querySelectorAll('.js-phone2-row'), function(el){ el.hidden = false; });
  }
  function safeUrl(u){ return /^(\/(?!\/)|https:\/\/)/.test(String(u || '')); }
  if(SITE.privacyUrl && safeUrl(SITE.privacyUrl)){ Array.prototype.forEach.call(document.querySelectorAll('.js-privacy'), function(el){ el.innerHTML = ''; var a = document.createElement('a'); a.href = SITE.privacyUrl; a.textContent = L.privacyLink || 'PDF'; el.appendChild(a); }); }

  /* the pen crosses out "someday" */
  var ill = $('ill'); if(ill) ill.classList.add('drawn');
  var hook = $('hook'), lines = L.hook || [], word = L.hookWord || '', q1 = L.q1 || '„', q2 = L.q2 || '”';
  function len(p){ try { return p.getTotalLength(); } catch(e){ return 120; } }
  function show(i){
    var j = function(a){ return (a + Math.random()*4).toFixed(1); };
    hook.innerHTML = '<span class="line">' + q1 + '<span class="k">' + word + '<svg viewBox="0 0 100 40" preserveAspectRatio="none" aria-hidden="true"><path d="M2 ' + j(22) + ' C 20 ' + j(17) + ', 38 ' + j(25) + ', 55 21 S 86 ' + j(16) + ', 98 22"/></svg></span> ' + lines[i] + q2 + '</span>';
    var line = hook.firstChild, p = hook.querySelector('path'), Lp = len(p);
    p.style.strokeDasharray = Lp; p.style.strokeDashoffset = Lp;
    line.animate(reduce ? [{opacity:0},{opacity:1}] : [{opacity:0, transform:'translateY(10px)'},{opacity:1, transform:'none'}], {duration:450, easing:'cubic-bezier(.2,.7,.2,1)', fill:'both'});
    setTimeout(function(){ p.animate([{strokeDashoffset:Lp},{strokeDashoffset:0}], {duration:600, easing:'cubic-bezier(.7,0,.3,1)', fill:'forwards'}); }, 800);
    setTimeout(function(){ line.animate(reduce ? [{opacity:1},{opacity:0}] : [{opacity:1},{opacity:0, transform:'translateX(-16px)'}], {duration:380, easing:'ease-in', fill:'forwards'}); }, 3500);
  }
  if(hook && lines.length && hook.animate){ var hi = 0; show(0); setInterval(function(){ if(document.hidden) return; hi = (hi + 1) % lines.length; show(hi); }, 3900); }

  /* job card */
  var F = $('karta'); if(!F) return;
  var co = $('k-co'), area = $('k-area'), dt = $('k-date'), kpath = $('kpath'), whenEl = $('when'), itemsEl = $('items'), stamp = $('stamp'), msg = $('msg'), tip = $('tip'), status = $('status');
  var M = L.msg || {}, struck = false, sendA = $('send');
  try { var td = new Date(); dt.min = new Date(td.getTime() - td.getTimezoneOffset()*60000).toISOString().slice(0, 10); } catch(e){}
  function v(nm){ var r = F.querySelector('input[name="' + nm + '"]:checked'); return r ? r.value : ''; }
  function list(){ return co.value.split(/[\n,;]+/).map(function(s){ return s.trim(); }).filter(Boolean); }
  function fmtDate(s){ if(!s) return ''; var p = s.split('-'); return p.length === 3 ? p[2] + '.' + p[1] : s; }
  function when(){ var r = F.querySelector('input[name="kiedy"]:checked'); if(!r) return ''; if(r.value === 'day') return dt.value ? (r.getAttribute('data-on') || '{d}').replace('{d}', fmtDate(dt.value)) : r.getAttribute('data-any'); return r.getAttribute('data-when') || r.value; }
  function strike(on){
    if(on === struck) return; struck = on;
    if(kpath.getAnimations) kpath.getAnimations().forEach(function(a){ a.cancel(); });
    if(on){ if(!kpath.animate) kpath.style.strokeDashoffset = 0; else kpath.animate([{strokeDashoffset:100},{strokeDashoffset:0}], {duration:520, easing:'cubic-bezier(.7,0,.3,1)', fill:'forwards'}); }
    else kpath.style.strokeDashoffset = 100;
  }
  var text = '';
  function update(){
    var it = list(), w = when();
    dt.hidden = v('kiedy') !== 'day';
    itemsEl.innerHTML = '';
    if(!it.length){ var e = document.createElement('li'); e.className = 'empty'; e.style.listStyle = 'none'; e.style.marginLeft = '-20px'; e.textContent = L.noteEmpty || ''; itemsEl.appendChild(e); }
    it.forEach(function(s){ var li = document.createElement('li'); li.textContent = s; itemsEl.appendChild(li); });
    whenEl.textContent = w; strike(!!w);
    stamp.classList.toggle('on', !!(w && it.length));
    var fl = v('fl'), lift = v('lift'), dem = v('dem'), cl = v('clean'), a = area.value.trim(), tbd = M.tbd || '';
    text = M.greet + '\n' + M.obj + ': ' + v('obj') + (a ? ', ' + a : '') +
      '\n' + M.floor + ': ' + (fl || '…') + (lift ? ', ' + lift : '') +
      '\n' + M.items + ': ' + (it.length ? it.join(', ') : '…') +
      '\n' + M.dem + ': ' + (dem || tbd) + ' · ' + M.clean + ': ' + (cl || tbd) +
      '\n' + M.when + ': ' + (w || tbd) + '\n' + M.photos;
    msg.textContent = text;
    if(wa) sendA.href = 'https://wa.me/' + wa + '?text=' + encodeURIComponent(text);
    var t = [], high = F.querySelector('input[name="fl"]:checked'), noLift = F.querySelector('input[name="lift"]:checked');
    if(high && high.hasAttribute('data-high') && noLift && noLift.hasAttribute('data-none')) t.push(L.tipHigh);
    if(dem && F.querySelector('input[name="dem"]:checked').hasAttribute('data-yes')) t.push(L.tipDem);
    var ob = F.querySelector('input[name="obj"]:checked'); if(ob && ob.hasAttribute('data-office')) t.push(L.tipOffice);
    tip.textContent = t.join(' ');
  }
  F.addEventListener('input', update); F.addEventListener('change', update); F.addEventListener('submit', function(e){ e.preventDefault(); });
  Array.prototype.forEach.call(F.querySelectorAll('[data-add]'), function(b){ b.addEventListener('click', function(){ var cur = co.value.trim(); co.value = cur ? cur.replace(/[,\s]+$/, '') + ', ' + b.getAttribute('data-add') : b.getAttribute('data-add'); update(); }); });
  update();
  sendA.addEventListener('click', function(){ if(wa) status.textContent = L.opening || ''; });
  $('copy').addEventListener('click', function(){
    function sel(){ var r = document.createRange(); r.selectNodeContents(msg); var s = getSelection(); s.removeAllRanges(); s.addRange(r); status.textContent = L.select || ''; }
    if(navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function(){ status.textContent = L.copied || ''; try { window.dispatchEvent(new CustomEvent('wyniose:copied')); } catch(e){} }, sel); else sel();
  });
})();
