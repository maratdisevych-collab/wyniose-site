# -*- coding: utf-8 -*-
"""The stairwell scene as one SVG world (units = cm). A cut-away of a Wrocław tenement:
floors IV..P stacked, dog-leg stairs (front flight cut in ink, back flight seen behind), doors and floor plates on the
back wall, lamperia following the stairs; outside: the courtyard, the van, the street, PSZOK.
stair.js only moves the camera (viewBox), the box, two doors and the van."""
import json

SH = 300            # storey height
NF = 4              # IV
def F(k): return 1600 - SH * k          # floor surface of level k (0 = P ... 4 = IV); F(5) = attic floor
T = 24              # slab
WL0, WL1 = 240, 300 # left wall
WR0, WR1 = 1200, 1260
HL1 = 540           # half landing 300..540
FR = 860            # flights run between HL1 and FR
NS, TW, RS = 8, 40, 150 / 8
DW, DH = 90, 210
DA, DB = 885, 1085  # door x (left edge)
BW, BH = 74, 60     # box
VAN_X, VAN_L, VAN_DX = 1420, 520, 1680
SKIPS = [(2560, 'ELEKTRO', '#C2412B'), (2730, 'PAPIER', '#1E4FAE'), (2900, 'GABARYTY', '#226B4C')]
SKW, SKH = 140, 110
GROUND = F(0)

C = dict(ink='#111A16', ink2='#26332D', plaster='#E6E9DE', plaster2='#D9DDD2', lamp='#226B4C', lamp2='#1B5A40',
         wood='#93603A', wood2='#6E4527', brass='#B98B3A', brassD='#7B5A1F', enamel='#1E4FAE', signal='#FFD02A',
         back='#5E6B64', backTop='#7C877F', sky='#DCE8EE', warm='#F6D9A0', kraft='#C29A63', tape='#E8D3A8')

def r(n): return ('%.1f' % n).rstrip('0').rstrip('.')

def path(d, fill=None, stroke=None, sw=None, extra=''):
    a = f'<path d="{d}"'
    if fill: a += f' fill="{fill}"'
    if stroke: a += f' stroke="{stroke}"'
    if sw: a += f' stroke-width="{sw}"'
    return a + extra + '/>'

def rect(x, y, w, h, fill, extra=''):
    return f'<rect x="{r(x)}" y="{r(y)}" width="{r(w)}" height="{r(h)}" fill="{fill}"{extra}/>'

def text(x, y, s, size, fill, extra=''):
    return f'<text x="{r(x)}" y="{r(y)}" font-size="{size}" fill="{fill}" text-anchor="middle"{extra}>{s}</text>'

def flight_poly(x0, y0, dirx):
    """steps going down from (x0,y0) in direction dirx (-1 left, +1 right); returns outline path and nosing path."""
    pts = [(x0, y0)]
    nos = []
    for i in range(NS):
        xa = x0 + dirx * TW * i
        y = y0 + RS * (i + 1)
        pts.append((xa, y))                   # riser down
        xb = xa + dirx * TW
        pts.append((xb, y))                   # tread
        nos.append((xa + (0 if dirx > 0 else -12), y, 12))
    xe, ye = pts[-1]
    # soffit: straight, parallel to the pitch, T below the nosing line
    soff = [(xe, ye + T + 4), (x0, y0 + T)]
    d = 'M' + ' L'.join(f'{r(a)} {r(b)}' for a, b in pts + soff) + 'Z'
    nd = ''.join(f'M{r(a)} {r(b)}h{r(w)}v4h{r(-w)}Z' for a, b, w in nos)
    return d, nd

def build():
    o = []
    # no gradients or patterns: flat fills keep every frame cheap to draw on phones
    # ---------- sky, town behind, ground ----------
    o.append(rect(-3000, -1200, 9000, GROUND + 1200, '#D3E2E8') + rect(-3000, GROUND - 700, 9000, 700, '#E2EBEA'))
    # town behind the courtyard: colours pre-mixed with the sky (no group opacity, so nothing is composited per frame)
    def fade(c, a=0.75, bg=(0xDD, 0xE6, 0xE8)):
        v = [int(c[k:k + 2], 16) for k in (1, 3, 5)]
        return '#%02X%02X%02X' % tuple(round(v[n] * a + bg[n] * (1 - a)) for n in range(3))
    town, wins, roofs = [], [], []
    x = 1300; i = 0
    heights = [760, 640, 820, 700, 880, 660, 780, 720, 840, 690, 760, 800, 650, 870]
    cols = ['#D5D9CD', '#CDD3C6', '#D9D4C6', '#CFD6CC', '#D3CFC2']
    while x < 4600:
        w = 300 + (i * 70) % 160; h = heights[i % len(heights)]
        top = GROUND - h
        town.append(rect(x, top, w, h, fade(cols[i % len(cols)])))
        roofs.append(f'M{x - 10} {top}L{x + w / 2} {top - 70}L{x + w + 10} {top}Z')
        for wy in range(int(top + 60), GROUND - 120, 150):
            for wx in range(int(x + 40), int(x + w - 60), 90):
                wins.append(f'M{wx} {wy}h44v70h-44Z')
        x += w + 20; i += 1
    o.append(''.join(town) + path(''.join(roofs), fill=fade('#B8B2A3')) + path(''.join(wins), fill=fade('#BCC6C4')))
    # trees in the courtyard / street
    for tx, ts in [(1330, 1.0), (2280, 1.25), (3420, 1.1), (4100, 0.9)]:
        o.append(rect(tx - 9 * ts, GROUND - 200 * ts, 18 * ts, 200 * ts, '#6E5442'))
        o.append(f'<circle cx="{r(tx)}" cy="{r(GROUND - 250 * ts)}" r="{r(95 * ts)}" fill="#5E8C55"/><circle cx="{r(tx - 50 * ts)}" cy="{r(GROUND - 215 * ts)}" r="{r(62 * ts)}" fill="#6E9B63"/><circle cx="{r(tx + 55 * ts)}" cy="{r(GROUND - 205 * ts)}" r="{r(58 * ts)}" fill="#4F7A48"/>')
    # ground: courtyard cobbles, kerb, street
    o.append(rect(WR1, GROUND, 6000, 30, '#B4A991') + rect(WR1, GROUND, 6000, 4, '#CDC3AC'))
    o.append(rect(WR1, GROUND + 30, 6000, 12, '#E4E8DD'))
    o.append(rect(-3000, GROUND + 42, 9000, 700, '#39403C'))
    o.append(path(''.join(f'M{x} {GROUND + 120}h70v6h-70Z' for x in range(1300, 5200, 150)), fill='#EEF0E8', extra=' opacity=".7"'))
    o.append(rect(-3000, GROUND + 24, WR1 + 3000, 700, '#4A3B2E'))   # basement / earth under the building
    o.append(rect(-3000, GROUND + 24, WR1 + 3000, 6, '#3A2E24'))
    # ---------- neighbour (left) ----------
    o.append(rect(-3000, F(5) - 200, 3000 + WL0, GROUND - F(5) + 242, '#2E3A35'))
    for k in range(5):
        for wx in (-260, -60):
            o.append(rect(WL0 + wx - 120, F(k) - 230, 90, 150, '#3E4A44'))
    # ---------- the building ----------
    # back wall plaster
    o.append(rect(WL1, F(5) + T, WR0 - WL1, GROUND - F(5) - T, C['plaster']))
    # per storey: lamperia band, windows, doors, plates, lamps
    for k in range(NF + 1):
        f = F(k)
        hl = f + SH / 2 - SH       # half landing above this floor belongs to storey k+1 ... keep per-flight below
        # landing band (right) and lamp
        o.append(rect(FR, f - 150, WR0 - FR, 150, C['lamp']))
        o.append(rect(FR, f - 154, WR0 - FR, 4, C['ink2']))
        o.append(f'<circle cx="1030" cy="{r(f - 250)}" r="150" fill="#FFE9B0" fill-opacity=".16"/><circle cx="1030" cy="{r(f - 250)}" r="80" fill="#FFE9B0" fill-opacity=".22"/>')
        o.append(rect(1018, f - 276, 24, 8, C['ink2']) + f'<ellipse cx="1030" cy="{r(f - 262)}" rx="16" ry="9" fill="#FFF1C2"/>')
        # doors
        nums = {4: (11, 12), 3: (8, 9), 2: (5, 6), 1: (2, 3), 0: (1, None)}[k]
        for j, dx in enumerate((DA, DB)):
            n = nums[j]
            if n is None:
                # ground floor: letterboxes instead of a door
                o.append(rect(dx, f - 170, DW, 80, '#5D6B62') + path(''.join(f'M{dx + 6 + c * 28} {f - 164 + rr * 24}h22v18h-22Z' for c in range(3) for rr in range(3)), fill='#7C8A82'))
                continue
            g = [rect(dx - 8, f - DH - 8, DW + 16, DH + 8, C['wood2'])]
            if k == NF and j == 1:
                # flat 12: the warm doorway and a leaf that swings toward us (scaled by JS)
                g.append(rect(dx, f - DH, DW, DH, C['warm']))
                g.append(rect(dx, f - 26, DW, 26, '#E8C688'))
                g.append(f'<g id="sc-door"><g id="sc-leaf">' + rect(dx, f - DH, DW, DH, C['wood']) + rect(dx + 10, f - DH + 14, DW - 20, 80, 'none', ' stroke="#6E4527" stroke-width="3"') + rect(dx + 10, f - 110, DW - 20, 90, 'none', ' stroke="#6E4527" stroke-width="3"') + rect(dx + 8, f - 112, 6, 22, C['brass']) + '</g></g>')
            else:
                g.append(rect(dx, f - DH, DW, DH, C['wood']))
                g.append(rect(dx + 10, f - DH + 14, DW - 20, 80, 'none', ' stroke="#6E4527" stroke-width="3"'))
                g.append(rect(dx + 10, f - 110, DW - 20, 90, 'none', ' stroke="#6E4527" stroke-width="3"'))
                g.append(rect(dx + DW - 14, f - 112, 6, 22, C['brass']))
            g.append(f'<ellipse cx="{r(dx + DW / 2)}" cy="{r(f - DH + 52)}" rx="17" ry="12" fill="{C["brass"]}"/>')
            g.append(text(dx + DW / 2, f - DH + 59, n, 19, '#2B1F07', ' class="sc-n"'))
            g.append(rect(dx + 6, f - 6, DW - 12, 6, '#4E3B2E'))
            o.append(''.join(g))
        # enamel floor plate
        lbl = ['P', 'I', 'II', 'III', 'IV'][k]
        o.append(f'<g><rect x="997" y="{r(f - 190)}" width="66" height="44" rx="6" fill="{C["enamel"]}"/><rect x="1001" y="{r(f - 186)}" width="58" height="36" rx="4" fill="none" stroke="#fff" stroke-width="2.5"/>' + text(1030, f - 158, lbl, 27, '#fff', ' class="sc-n"') + '</g>')
    # roof + attic
    o.append(path(f'M{WL0 - 60} {F(5)}L{WL0 + 120} {F(5) - 230}L{WR1 - 120} {F(5) - 230}L{WR1 + 60} {F(5)}Z', fill='#A35F44'))
    o.append(path(''.join(f'M{x} {F(5) - 230}L{x - 40 if x < 750 else x + 40} {F(5)}' for x in range(WL0 + 160, WR1 - 100, 90)), stroke='#8A4E37', sw=4, fill='none'))
    o.append(rect(980, F(5) - 330, 70, 120, '#8A4E37'))
    o.append(rect(970, F(5) - 340, 90, 18, '#5E3526'))
    o.append(rect(WL0 - 60, F(5), WR1 - WL0 + 120, T, C['ink']))
    # half landings, windows, back flights (seen behind the front ones)
    backs = []
    for k in range(NF, 0, -1):
        f = F(k); h = f + SH / 2
        # lamperia on the half landing and along the back flight
        o.append(rect(WL1, h - 150, HL1 - WL1, 150, C['lamp']))
        o.append(rect(WL1, h - 154, HL1 - WL1, 4, C['ink2']))
        o.append(path(f'M{HL1} {h - 150}L{FR} {f + SH - 150}L{FR} {f + SH}L{HL1} {h}Z', fill=C['lamp']))
        o.append(path(f'M{HL1} {h - 154}L{FR} {f + SH - 154}L{FR} {f + SH - 150}L{HL1} {h - 150}Z', fill=C['ink2']))
        # window to the courtyard behind the half landing
        o.append(rect(340, h - 250, 150, 170, '#F4F6F0') + rect(350, h - 240, 130, 150, '#BFD6E2') + rect(412, h - 240, 6, 150, '#F4F6F0') + rect(350, h - 175, 130, 6, '#F4F6F0'))
        # radiator
        o.append(rect(360, h - 66, 110, 46, '#C9CFC4') + path(''.join(f'M{366 + 14 * q} {h - 62}h7v38h-7Z' for q in range(7)), fill='#AEB5A9'))
        # back flight: from the half landing down to the floor below, going right
        d, nd = flight_poly(HL1, h, +1)
        backs.append(path(d, fill=C['back']) + path(nd, fill='#B5A85E'))
        # back railing
        rail = ''.join(f'M{r(HL1 + TW * i + 20)} {r(h + RS * (i + 1))}v-88' for i in range(NS))
        backs.append(path(rail, stroke='#56615B', sw=3, fill='none'))
        backs.append(path(f'M{HL1} {h - 92}L{FR} {f + SH - 92}', stroke='#8E7A4F', sw=6, fill='none', extra=' stroke-linecap="round"'))
    o.append('<g id="sc-backs">' + ''.join(backs) + '</g>')
    o.append('<g id="sc-slot-back"></g>')
    # ---------- the cut (front): slabs, front flights, walls ----------
    cut = []
    for k in range(NF, 0, -1):
        f = F(k); h = f + SH / 2
        cut.append(rect(FR, f, WR0 - FR, T, C['ink']))                       # floor landing slab
        cut.append(rect(WL1, h, HL1 - WL1, T, C['ink']))                      # half landing slab
        d, nd = flight_poly(FR, f, -1)
        cut.append(path(d, fill=C['ink']) + path(nd, fill=C['signal']))
        # landing slab edge nosing
        cut.append(rect(FR, f, 14, 4, C['signal']))
    cut.append(rect(WL1, GROUND, WR0 - WL1, T, C['ink']))                     # ground floor
    cut.append(rect(WL0, F(5), WL1 - WL0, GROUND - F(5) + T, C['ink']))      # left wall
    # right wall with the street door opening at P
    cut.append(rect(WR0, F(5), WR1 - WR0, GROUND - 236 - F(5), C['ink']))
    cut.append(rect(WR0, GROUND, WR1 - WR0, T, C['ink']))
    o.append('<g id="sc-cut">' + ''.join(cut) + '</g>')
    o.append('<g id="sc-slot-front"></g>')
    # front railings (always in front of the box)
    rails = []
    for k in range(NF, 0, -1):
        f = F(k)
        rail = ''.join(f'M{r(FR - TW * i - 20)} {r(f + RS * (i + 1))}v-88' for i in range(NS))
        rails.append(path(rail, stroke=C['ink'], sw=3.5, fill='none'))
        rails.append(path(f'M{FR + 30} {f - 92}L{FR} {f - 92}L{HL1} {f + SH / 2 - 92}L{WL1 + 20} {f + SH / 2 - 92}', stroke=C['brass'], sw=7, fill='none', extra=' stroke-linecap="round" stroke-linejoin="round"'))
        rails.append(path(f'M{FR + 28} {f}v-92M{WL1 + 24} {f + SH / 2}v-92', stroke=C['ink'], sw=5, fill='none'))
    o.append('<g id="sc-rails">' + ''.join(rails) + '</g>')
    # street door: daylight on the floor + leaf that opens outward (scaled by JS)
    o.append(path(f'M{WR0} {GROUND - 230}L{WR0} {GROUND}L{WR0 - 260} {GROUND}Z', fill='#FFF1C2', extra=' id="sc-daylight" opacity="0"'))
    o.append(f'<g id="sc-exit">' + rect(WR1, GROUND - 230, 100, 230, C['wood']) + rect(WR1 + 12, GROUND - 216, 76, 96, 'none', ' stroke="#6E4527" stroke-width="3"') + rect(WR1 + 12, GROUND - 108, 76, 92, 'none', ' stroke="#6E4527" stroke-width="3"') + '</g>')
    o.append(f'<g>' + rect(WR1, GROUND - 300, 70, 46, C['enamel'], ' rx="6"') + text(WR1 + 35, GROUND - 268, '7', 28, '#fff', ' class="sc-n"') + '</g>')
    # ---------- PSZOK ----------
    o.append('<g id="sc-slot-skip"></g>')
    psz = []
    x0 = SKIPS[0][0] - 60; x1 = SKIPS[-1][0] + SKW + 60
    psz.append(path(''.join(f'M{x} {GROUND}v-150' for x in range(int(x0) - 200, int(x0) - 20, 22)), stroke='#7C877F', sw=3, fill='none'))
    psz.append(rect(x0 - 200, GROUND - 150, 180, 4, '#7C877F'))
    psz.append(rect(x0 + 40, GROUND - 330, 8, 330, '#5D6B62') + rect(x1 - 48, GROUND - 330, 8, 330, '#5D6B62'))
    psz.append(rect(x0 + 10, GROUND - 400, x1 - x0 - 20, 82, C['signal'], ' rx="8" stroke="#111A16" stroke-width="4"'))
    psz.append(text((x0 + x1) / 2, GROUND - 341, 'PSZOK', 58, C['ink'], ' class="sc-n"'))
    for sx, lbl, col in SKIPS:
        psz.append(path(f'M{sx} {GROUND - SKH}h{SKW}l-16 {SKH}h{-(SKW - 32)}Z', fill=col))
        psz.append(rect(sx - 6, GROUND - SKH - 8, SKW + 12, 12, C['ink2'], ' rx="3"'))
        psz.append(text(sx + SKW / 2, GROUND - SKH / 2 + 6, lbl, 21 if len(lbl) > 6 else 24, '#fff', ' class="sc-n"'))
    o.append('<g>' + ''.join(psz) + '</g>')
    # ---------- the van (moved by JS) ----------
    L = VAN_L
    v = [f'<g id="sc-van" transform="translate({VAN_X} 0)">']
    v.append(f'<ellipse cx="{L / 2}" cy="{GROUND + 10}" rx="{L * 0.55}" ry="14" fill="#000" opacity=".22"/>')
    v.append(f'<g id="sc-rear">' + rect(-96, GROUND - 236, 96, 196, '#174A35') + rect(-86, GROUND - 222, 76, 70, '#17302A') + '</g>')
    v.append(rect(-4, GROUND - 236, 8, 196, '#0B1310'))
    v.append('<g id="sc-slot-van"></g>')
    v.append(path(f'M0 {GROUND - 40}V{GROUND - 236}Q0 {GROUND - 250} 14 {GROUND - 250}H{L - 150}Q{L - 112} {GROUND - 250} {L - 92} {GROUND - 210}L{L - 46} {GROUND - 130}Q{L} {GROUND - 118} {L} {GROUND - 84}V{GROUND - 40}Z', fill=C['lamp']))
    v.append(path(f'M{L - 140} {GROUND - 236}H{L - 104}Q{L - 94} {GROUND - 234} {L - 86} {GROUND - 218}L{L - 58} {GROUND - 150}H{L - 140}Z', fill='#17302A'))
    v.append(rect(L - 150, GROUND - 244, 4, 204, '#174A35'))
    v.append(rect(0, GROUND - 96, L, 26, C['signal']))
    v.append(path(''.join(f'M{x} {GROUND - 96}l26 0l-26 26Z' for x in range(0, 100, 26)), fill=C['ink']))
    v.append(f'<image href="/logo-light.svg" x="{r((L - 150) / 2 + 4 - 140)}" y="{r(GROUND - 206)}" width="280" height="68"/>')
    v.append(rect(L - 26, GROUND - 120, 22, 18, '#FFF1C2', ' rx="4"'))
    for wx in (110, L - 110):
        v.append(f'<g class="sc-wheel" data-x="{wx}"><circle cx="{wx}" cy="{GROUND - 34}" r="40" fill="#EEF0E8"/><circle cx="{wx}" cy="{GROUND - 34}" r="33" fill="#111A16"/><g class="sc-spin"><circle cx="{wx}" cy="{GROUND - 34}" r="14" fill="#9AA59E"/><rect x="{wx - 3}" y="{GROUND - 52}" width="6" height="36" fill="#5D6B62"/></g></g>')
    v.append('</g>')
    o.append(''.join(v))
    o.append('<g id="sc-slot-out"></g>')
    # ---------- the box (moved between slots by JS) ----------
    box = (f'<g id="sc-box"><g id="sc-boxi">'
           f'<ellipse cx="0" cy="2" rx="{BW * 0.55}" ry="5" fill="#000" opacity=".22"/>'
           + rect(-BW / 2, -BH, BW, BH, C['kraft']) + rect(-BW / 2, -BH, BW, 9, '#D2AE78') + rect(-7, -BH, 14, BH, C['tape'])
           + rect(-BW / 2, -BH, 5, BH, '#000', ' opacity=".08"')
           + '</g></g>')
    o.append(f'<g id="sc-boxhome" transform="translate({FR - TW * 3.5} {F(NF) + RS * 4})">{box}</g>')
    return ''.join(o)

GEO = dict(SH=SH, NF=NF, G=GROUND, T=T, FR=FR, HL1=HL1, WL1=WL1, WR0=WR0, WR1=WR1, NS=NS, TW=TW, RS=RS, DB=DB, DW=DW, DH=DH,
           BW=BW, BH=BH, VX=VAN_X, VL=VAN_L, VDX=VAN_DX, SK=SKIPS[-1][0], SKW=SKW, SKH=SKH)
OVERVIEW = '60 -260 2100 1960'

def svg(title):
    return (f'<svg class="scene" id="scene" viewBox="{OVERVIEW}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="{title}" '
            f'data-geo=\'{json.dumps(GEO)}\'>' + build() + '</svg>')

if __name__ == '__main__':
    s = svg('test')
    open('scene-test.svg', 'w').write(s.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
    print(len(s))
