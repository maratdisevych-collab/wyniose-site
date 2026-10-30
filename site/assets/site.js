(function(){
  var L = window.L || {}, SITE = window.SITE || {};
  var $ = function(id){ return document.getElementById(id); };
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var header = $('top');
  function setHH(){ if(header) document.documentElement.style.setProperty('--hh', header.offsetHeight + 'px'); }
  setHH(); addEventListener('resize', setHH);
  var digits = function(s){ return String(s || '').replace(/[^\d+]/g, ''); };
  var phone = digits(SITE.phone), wa = digits(SITE.whatsapp || SITE.phone).replace(/^\+/, '');
  var phoneText = SITE.phone ? String(SITE.phone) : '+48 ··· ··· ···';
  Array.prototype.forEach.call(document.querySelectorAll('.js-phone'), function(el){ el.textContent = phoneText; });
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
(function(){
  var sec = document.getElementById('droga'); if(!sec) return;
  var svg = document.getElementById('scene'); if(!svg || !svg.setAttribute) return;
  var G; try { G = JSON.parse(svg.getAttribute('data-geo')); } catch(e){ return; }
  var view = sec.querySelector('.view'), track = sec.querySelector('.track');
  var L = window.L || {}, de = document.documentElement;
  var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var canScroll = (Math.max(de.scrollHeight, document.body.scrollHeight) - window.innerHeight) > window.innerHeight*1.5;
  function mq(q){ return !!(window.matchMedia && matchMedia(q).matches); }
  var small = mq('(max-width: 960px)') || window.innerWidth <= 960, touch = mq('(pointer: coarse)');
  var mode = canScroll && !small && !touch ? 'scroll' : 'auto';
  sec.classList.add('anim'); if(mode === 'scroll') sec.classList.add('scroll');
  sec.setAttribute('data-mode', mode);
  svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
  var phases = [].slice.call(sec.querySelectorAll('.phase')), rails = [].slice.call(sec.querySelectorAll('.rail li')), railBtns = [].slice.call(sec.querySelectorAll('.rail button'));
  var hint = sec.querySelector('.hint'), player = sec.querySelector('.player'), pbtn = player && player.querySelector('button'), scrub = player && player.querySelector('input');
  function $(id){ return document.getElementById(id); }
  var box = $('sc-box'), leaf = $('sc-leaf'), exitLeaf = $('sc-exit'), day = $('sc-daylight'), van = $('sc-van'), rear = $('sc-rear');
  var spins = [].slice.call(svg.querySelectorAll('.sc-spin')), wheels = [].slice.call(svg.querySelectorAll('.sc-wheel'));
  var slots = {back: $('sc-slot-back'), front: $('sc-slot-front'), van: $('sc-slot-van'), skip: $('sc-slot-skip'), out: $('sc-slot-out')};
  var SH = G.SH, NF = G.NF, GR = G.G, FR = G.FR, HL1 = G.HL1, NS = G.NS, TW = G.TW, RS = G.RS;
  var DOORX = G.DB + G.DW/2, HINGE = G.DB + G.DW, VX = G.VX, VL = G.VL, VDX = G.VDX, SKX = G.SK + G.SKW/2;
  var BMIN = 225, BMAX = 1275, BC = (BMIN + BMAX)/2;
  function Fk(k){ return GR - SH*k; }
  var P_IN = 0.06, P_DN = 0.64, P_VAN = 0.735, P_LOAD = 0.775, P_DRIVE = 0.885, P_DROP = 0.955;
  function clamp(x,a,b){ return x < a ? a : x > b ? b : x; }
  function seg(p,a,b){ return clamp((p - a)/(b - a), 0, 1); }
  function ease(x){ return x*x*(3 - 2*x); }
  function lerp(a,b,t){ return a + (b - a)*t; }
  function steps(q, dir, x0, y0){
    var i = Math.min(NS - 1, Math.floor(q)), fr = q - i, d = clamp(fr/0.34, 0, 1);
    return {x: x0 + dir*TW*q, y: y0 + RS*(i + ease(d)), rot: dir*7*Math.sin(Math.PI*d), lin: y0 + RS*q};
  }
  function boxAt(p){
    var b = {x: 0, y: 0, rot: 0, sx: 1, sc: 1, op: 1, slot: 'front', lin: 0, door: 0, exit: 0, rear: 1, dx: 0};
    b.door = ease(seg(p, 0, 0.022));
    if(p < P_IN){
      var e = ease(seg(p, 0.016, P_IN));
      b.x = lerp(DOORX, FR + 6, e); b.y = b.lin = Fk(NF); b.sc = lerp(0.84, 1, Math.min(1, e*2.5)); b.op = Math.min(1, e*6 + 0.0001);
      return b;
    }
    if(p < P_DN){
      var u = 4*seg(p, P_IN, P_DN), j = Math.min(3, Math.floor(u)), a = u - j, F0 = Fk(NF - j), s, t;
      if(a < 0.40){ t = a/0.40; s = steps(t*NS, -1, FR, F0); b.x = s.x; b.y = s.y; b.rot = s.rot; b.lin = s.lin; }
      else if(a < 0.52){ t = (a - 0.40)/0.12; b.x = HL1 - 95*Math.sin(Math.PI*t); b.y = b.lin = F0 + SH/2; b.sx = Math.cos(Math.PI*t); }
      else if(a < 0.92){ t = (a - 0.52)/0.40; s = steps(t*NS, 1, HL1, F0 + SH/2); b.x = s.x; b.y = s.y; b.rot = s.rot; b.lin = s.lin; b.sx = -1; b.slot = 'back'; }
      else { t = (a - 0.92)/0.08; b.y = b.lin = F0 + SH;
        if(j < 3){ b.x = FR + 70*Math.sin(Math.PI*t); b.sx = -Math.cos(Math.PI*t); }
        else { b.x = FR + 40*t; b.sx = -1; } }
      return b;
    }
    b.sx = -1; b.y = b.lin = GR; b.exit = ease(seg(p, P_DN - 0.03, P_DN + 0.02));
    if(p < P_VAN){ b.x = lerp(FR + 40, VX - 46, ease(seg(p, P_DN, P_VAN))); b.slot = b.x > G.WR0 - 20 ? 'out' : 'front'; return b; }
    if(p < P_LOAD){ var lt = seg(p, P_VAN, P_LOAD - 0.012); b.x = lerp(VX - 46, VX + 90, ease(clamp((lt - 0.25)/0.75, 0, 1))); b.y = GR - 44*ease(clamp(lt/0.3, 0, 1)); b.rot = -6*Math.sin(Math.PI*clamp(lt/0.3, 0, 1)); b.slot = 'van'; b.rear = 1 - ease(seg(p, P_LOAD - 0.014, P_LOAD)); return b; }
    b.dx = VDX*ease(seg(p, P_LOAD + 0.004, P_DRIVE - 0.004));
    if(p < P_DRIVE){ b.rear = 0; b.op = 0; b.x = VX + 90 + b.dx; b.slot = 'van'; return b; }
    b.rear = ease(seg(p, P_DRIVE, P_DRIVE + 0.014));
    var vr = VX + VDX;
    var o = ease(seg(p, P_DRIVE + 0.01, P_DRIVE + 0.03)), f = seg(p, P_DRIVE + 0.03, P_DROP);
    if(f <= 0){ b.x = lerp(vr + 60, vr - 40, o); b.y = GR - 44; b.slot = 'van'; return b; }
    var fe = ease(f);
    b.x = lerp(vr - 40, SKX, fe); b.y = lerp(GR - 44, GR - 78, fe) - Math.sin(Math.PI*f)*230; b.rot = -200*fe; b.sc = lerp(1, 0.92, fe);
    b.slot = f > 0.6 ? 'skip' : 'out';
    return b;
  }
  var W = 1, H = 1, s0 = 1, fx = 0, fy = 0, lo = 0, hi = 0, gy = 0, ready = false;
  function size(){
    var r = view.getBoundingClientRect(); if(r.width < 2 || r.height < 2){ ready = false; return; }
    W = r.width; H = r.height;
    var lp, rp, aw;
    if(W > 960){ lp = Math.min(470, W*0.35); rp = 96; aw = W - lp - rp; fx = lp + aw/2; fy = H*0.5; s0 = Math.min(aw/1060, H/600); gy = H*0.8; }
    else {
      var top = 56, bot = 14;
      if(mode === 'scroll'){ var ph = 0; phases.forEach(function(el){ ph = Math.max(ph, el.offsetHeight || 0); }); bot = 92 + (ph || 190) + 14; }
      var ah = Math.max(160, H - top - bot);
      lp = rp = 10; aw = W - 20; fx = W/2; fy = top + ah*0.5; s0 = Math.max(0.5, Math.min(aw/1060, ah/500)); gy = top + ah*0.92;
    }
    lo = BMIN + (fx - lp)/s0; hi = BMAX - (W - rp - fx)/s0;
    ready = true;
  }
  function camX(x){ return lo >= hi ? BC : clamp(x, lo, hi); }
  function camAt(p, b){
    var stairsY = function(bb){ return bb.lin - 60; };
    var cS = {x: camX(b.x), y: stairsY(b), s: s0, ym: GR + 80};
    var sOut = s0*0.74, oy = GR - (gy - fy)/sOut;
    var yard = {x: VX + 60, y: oy, s: sOut, ym: GR + 740};
    if(p < P_DN - 0.02) return cS;
    if(p < P_VAN){
      var bb = boxAt(P_DN - 0.02), a = {x: camX(bb.x), y: stairsY(bb), s: s0, ym: GR + 80}, t = ease(seg(p, P_DN - 0.02, P_VAN));
      return {x: lerp(a.x, yard.x, t), y: lerp(a.y, yard.y, t), s: lerp(a.s, yard.s, t), ym: lerp(a.ym, yard.ym, t)};
    }
    return {x: lerp(VX + 60, VX + VDX - 120, b.dx/VDX), y: oy, s: sOut, ym: GR + 740};
  }
  var lastVB = '';
  function setVB(c){
    var vw = W/c.s, vh = H/c.s, x = c.x - fx/c.s, y = c.y - fy/c.s;
    y = Math.max(-560, Math.min(y, (c.ym || GR + 740) - vh));
    var v = x.toFixed(1) + ' ' + y.toFixed(1) + ' ' + vw.toFixed(1) + ' ' + vh.toFixed(1);
    if(v !== lastVB){ svg.setAttribute('viewBox', v); lastVB = v; }
  }
  var curSlot = '', cache = {};
  function attr(el, k, v){ if(!el) return; var key = (el.id || '') + k; if(cache[key] === v) return; cache[key] = v; el.setAttribute(k, v); }
  function frame(p){
    var b = boxAt(p);
    if(b.slot !== curSlot && slots[b.slot]){ slots[b.slot].appendChild(box); curSlot = b.slot; }
    var vx = VX + b.dx, bx = b.slot === 'van' ? b.x - vx : b.x;
    attr(box, 'transform', 'translate(' + bx.toFixed(1) + ' ' + b.y.toFixed(1) + ') rotate(' + b.rot.toFixed(1) + ' 0 ' + (-G.BH/2) + ') scale(' + (b.sx*b.sc).toFixed(3) + ' ' + b.sc.toFixed(3) + ')');
    attr(box, 'opacity', b.op.toFixed(2));
    attr(leaf, 'transform', 'translate(' + HINGE + ' 0) scale(' + (1 - 0.82*b.door).toFixed(3) + ' 1) translate(' + (-HINGE) + ' 0)');
    attr(exitLeaf, 'transform', 'translate(' + G.WR1 + ' 0) scale(' + b.exit.toFixed(3) + ' 1) translate(' + (-G.WR1) + ' 0)');
    attr(day, 'opacity', (b.exit*0.45).toFixed(2));
    attr(van, 'transform', 'translate(' + vx.toFixed(1) + ' 0)');
    attr(rear, 'transform', 'scale(' + Math.max(0.001, b.rear).toFixed(3) + ' 1)');
    var ang = (b.dx/40)*57.2958;
    for(var i = 0; i < spins.length; i++){ var wx = wheels[i].getAttribute('data-x'); attr(spins[i], 'transform', 'rotate(' + ang.toFixed(1) + ' ' + wx + ' ' + (GR - 34) + ')'); }
    setVB(camAt(p, b));
  }
  var current = -1;
  function phaseOf(p){
    if(p < P_DN) return Math.min(4, Math.round(4*seg(p, P_IN, P_DN)));
    if(p < P_VAN - 0.012) return 4;
    return p < P_DRIVE - 0.02 ? 5 : 6;
  }
  function setPhase(p){
    if(hint) hint.classList.toggle('gone', p > 0.03);
    var i = phaseOf(p); if(i === current) return; current = i;
    phases.forEach(function(el, k){ el.classList.toggle('on', k === i); });
    rails.forEach(function(el, k){ el.classList.toggle('on', k === i); });
  }
  var curP = 0, drawnP = -1;
  function draw(p){ if(!ready) size(); curP = p; if(Math.abs(p - drawnP) < 0.0002) return; drawnP = p; frame(p); setPhase(p); if(scrub) scrub.value = Math.round(p*1000); }
  function hh(){ return parseFloat(getComputedStyle(de).getPropertyValue('--hh')) || 0; }
  function progress(){ var r = track.getBoundingClientRect(), top = hh(), total = r.height - (window.innerHeight - top); return clamp((top - r.top)/Math.max(1, total), 0, 1); }
  var visible = false, ticking = false;
  function onScroll(){ if(!ticking && visible){ ticking = true; requestAnimationFrame(function(){ ticking = false; draw(progress()); }); } }
  var playing = false, t0 = 0, pStart = 0, DUR = small ? 13000 : 17000, raf = 0, autoplayed = false, autoPaused = false;
  var ICON = {play:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>', pause:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg>', replay:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a5 5 0 1 1-5 5H5a7 7 0 1 0 7-7z" fill="currentColor"/></svg>'};
  function setBtn(k){ if(!pbtn) return; pbtn.innerHTML = ICON[k]; pbtn.setAttribute('aria-label', (L.player && L.player[k]) || k); }
  var lastT = 0, lastDraw = 0, slow = 0, cap = 0;
  function tick(now){
    if(!playing) return;
    if(lastT){ var dt = now - lastT; slow = dt > 24 ? slow + 1 : Math.max(0, slow - 1); if(slow > 8) cap = 32; }
    lastT = now;
    var p = pStart + (now - t0)/DUR; if(p >= 1){ p = 1; playing = false; setBtn('replay'); }
    if(!cap || now - lastDraw >= cap - 2 || p >= 1){ lastDraw = now; draw(p); }
    if(playing) raf = requestAnimationFrame(tick);
  }
  function play(){ if(curP >= 0.999) curP = 0; pStart = curP; t0 = performance.now(); lastT = 0; playing = true; setBtn('pause'); raf = requestAnimationFrame(tick); }
  function pause(){ playing = false; cancelAnimationFrame(raf); setBtn(curP >= 0.999 ? 'replay' : 'play'); }
  if(player && mode !== 'scroll'){
    player.hidden = false; setBtn('play');
    pbtn.addEventListener('click', function(){ autoPaused = false; playing ? pause() : play(); });
    scrub.addEventListener('input', function(){ autoPaused = false; if(playing) pause(); drawnP = -1; draw(scrub.value/1000); });
  }
  var STAGE_P = [0, P_IN + (P_DN - P_IN)*0.875/4, P_IN + (P_DN - P_IN)*1.875/4, P_IN + (P_DN - P_IN)*2.875/4, P_IN + (P_DN - P_IN)*3.875/4, P_VAN - 0.008, P_DRIVE - 0.018];
  railBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      var p = STAGE_P[+btn.getAttribute('data-i')] || 0;
      if(mode === 'scroll'){
        var r = track.getBoundingClientRect(), top = hh(), total = r.height - (window.innerHeight - top);
        window.scrollTo({top: r.top + window.pageYOffset - top + total*p + 2, behavior: reduce ? 'auto' : 'smooth'});
        return;
      }
      autoPaused = false; var was = playing; if(playing) pause();
      drawnP = -1; draw(p); if(was) play(); else setBtn('play');
    });
  });
  size(); draw(curP);
  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      var e = es[0]; visible = e.isIntersecting;
      if(mode === 'scroll' && visible) onScroll();
      if(mode === 'auto'){
        var ra = e.intersectionRatio;
        if(ra >= 0.5){ if(!autoplayed){ autoplayed = true; play(); } else if(autoPaused){ autoPaused = false; play(); } }
        else if(ra < 0.2 && playing){ pause(); autoPaused = true; }
      }
    }, {rootMargin: mode === 'scroll' ? '200px 0px' : '0px', threshold: [0, 0.2, 0.5, 0.8]}).observe(mode === 'scroll' ? sec : view);
  } else { visible = true; }
  if(mode === 'scroll'){ addEventListener('scroll', onScroll, {passive: true}); onScroll(); }
  function resized(){ size(); drawnP = -1; draw(mode === 'scroll' ? progress() : curP); }
  var rt; addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(resized, 120); });
  if('ResizeObserver' in window) new ResizeObserver(function(){ if(Math.abs(view.clientWidth - W) > 1 || Math.abs(view.clientHeight - H) > 1) resized(); }).observe(view);
  addEventListener('orientationchange', function(){ setTimeout(resized, 300); });
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(resized);
  window.__stair = {mode: mode, draw: function(p){ drawnP = -1; draw(p); }, state: function(){ return {p: curP, playing: playing}; }, stop: function(){ autoPaused = false; pause(); }};
})();
(function(){
  var SITE = window.SITE || {}, A = SITE.ads || {};
  var ID_OK = /^AW-\d{6,}$/, SEND_OK = /^AW-\d{6,}\/[A-Za-z0-9_-]+$/;
  var enabled = ID_OK.test(A.id || '') && SEND_OK.test(A.tel || '') && SEND_OK.test(A.wa || '') && A.tel !== A.wa;
  var banner = document.getElementById('consent'), openBtn = document.getElementById('consent-open');
  var diag = window.__wyDiag = window.__wyDiag || [];
  function note(type, extra){ var d = {type: type, t: Date.now()}; for(var k in extra) d[k] = extra[k]; diag.push(d); }
  var AD_PARAMS = /^(gclid|gbraid|wbraid|gad_source|gad_campaignid|utm_[a-z]+)$/;
  function adQuery(){
    try { var q = new URLSearchParams(location.search), keep = new URLSearchParams();
      q.forEach(function(v, k){ if(AD_PARAMS.test(k)) keep.append(k, v); }); var s = keep.toString(); return s ? '?' + s : ''; } catch(e){ return ''; }
  }
  var aq = adQuery();
  if(aq) [].forEach.call(document.querySelectorAll('.langs-nav a'), function(a){ var h = a.getAttribute('href') || ''; if(h.indexOf('?') < 0) a.setAttribute('href', h.replace(/(#.*)?$/, aq + '$1')); });
  window.addEventListener('wyniose:copied', function(){ note('copy_job_card'); });
  if(!enabled){ if(banner) banner.hidden = true; if(openBtn) openBtn.hidden = true; window.__consent = {enabled: false}; return; }
  var KEY = 'wyniose-consent-v1', MAX_AGE = 365*24*3600*1000;
  function read(){
    try { var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if(v && (v.ads === 'granted' || v.ads === 'denied') && Date.now() - (v.t || 0) < MAX_AGE) return v.ads; } catch(e){}
    return null;
  }
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
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(A.id);
    s.onerror = function(){ failed = true; note('tag_blocked'); };
    document.head.appendChild(s);
  }
  function clearAdCookies(){
    var host = location.hostname, base = host.replace(/^www\./, '');
    document.cookie.split(';').forEach(function(c){
      var n = c.split('=')[0].trim(); if(!/^(_gcl_|_gac_|FPGCL)/.test(n)) return;
      ['', '; domain=' + host, '; domain=.' + base].forEach(function(d){ document.cookie = n + '=; Max-Age=0; path=/' + d; });
    });
  }
  function decide(state, fromUser){
    var was = granted;
    granted = state === 'granted';
    if(fromUser) save(state);
    if(granted){ if(!was) gtag('consent', 'update', {ad_storage: 'granted', ad_user_data: 'granted'}); load(); }
    else { if(was || loaded) gtag('consent', 'update', {ad_storage: 'denied', ad_user_data: 'denied'}); clearAdCookies(); }
    note('consent', {state: state, by: fromUser ? 'visitor' : 'stored'});
    if(banner) banner.hidden = true;
    document.documentElement.classList.remove('consent-open');
  }
  function ask(focus){
    if(!banner) return;
    banner.hidden = false; document.documentElement.classList.add('consent-open');
    var b = focus && banner.querySelector('button'); if(b) try { b.focus({preventScroll: true}); } catch(e){}
  }
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
