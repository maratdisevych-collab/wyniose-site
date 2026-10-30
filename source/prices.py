# -*- coding: utf-8 -*-
"""Published prices, one place for the whole site (home page in PL and EN, the price list page, service pages).
Source: the owner's pricing model of 29.10.2026 (document "Wyniosę: ценообразование"), rounded to round numbers.
All prices are "from" prices in PLN, invoice without VAT, for Wrocław, ready items, ground floor or a lift.
Change a number here only with the owner's explicit "да" (see CLAUDE.md)."""

def zl(n):
    """190 -> '190 zł', 1600 -> '1600 zł', 10500 -> '10 500 zł' (Polish style: 4-digit numbers unspaced), no-break spaces."""
    s = str(n) if n < 10000 else f'{n:,}'.replace(',', '\u00a0')
    return s + '\u00a0zł'

# home page cards and the top of the price list: key, from-price
FROM = dict(
    item=190,        # one small item on a shared route: armchair, mattress, cabinet, rug
    appliance=210,   # fridge, washing machine, cooker
    furniture=270,   # sofa, bed, wardrobe in one piece, table
    room=700,        # about a quarter of the van, ~4 m3
    cellar=750,      # basement or storage room, ~3 m3
    garage=800,      # garage, ~5 m3
    studio=1600,     # studio flat, ~8 m3
    flat=2900,       # 2-room flat, ~14 m3, two trips
    flat3=4200,      # 3-room flat, ~22 m3
    house=6900,      # house, ~35 m3
    office=1900,     # office, half a van, paid disposal (company waste cannot go to PSZOK)
    solo=450,        # a separate trip for one item on a day the client picks
)

# price list page: volume in parts of the van (16 m3, 1.2 t)
VAN = [('Do 1 m³ (minimalny osobny przyjazd)', 450), ('¼ busa, ok. 4 m³', 700), ('½ busa, ok. 8 m³', 1050),
       ('¾ busa, ok. 12 m³', 1400), ('Cały bus, ok. 16 m³', 1800)]

# extras
EXTRA = dict(next_item=100, floor_item=20, dismantle=100, pack_m3=130, second_trip=330,
             hour_first=290, hour_next=240, rubble_10=420, rubble_bag=10, evening_pct=20)
FLOOR_VAN = [('¼ busa', 40), ('½ busa', 70), ('¾ busa', 100), ('cały bus', 130)]
ZONES = [(10, 100), (25, 250), (40, 400), (55, 550), (70, 700)]
