"""Render Packet Tracer files in Packet Tracer's own visual style (Pillow only).

  python3 -I pt_render.py logical  design.xml           out.png
  python3 -I pt_render.py racks    design.xml           out.png
  python3 -I pt_render.py floor    floor.xml  bg.jpg    out.png

Geometry comes straight from the decrypted .pkt XML: each device's <WORKSPACE><LOGICAL>
X/Y is the centre of its icon, cables run centre to centre (straight-through solid,
crossover dashed), notes and rectangles use their stored coordinates, and racks list
their devices in the order of their stored rack offsets. Icon colours were sampled from
a Packet Tracer 8.2 screenshot (teal 82,152,174; link-light green 108,192,74).
"""
import math, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
FONT_B = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
TOP, FRONT, SIDE, EDGE = (150, 201, 216), (82, 152, 174), (24, 112, 138), (16, 84, 104)
LIGHT, SCREEN = (113, 172, 190), (214, 236, 243)
GREEN, LABEL, INK = (108, 192, 74), (38, 72, 160), (20, 20, 20)
RED_F, RED_T, RED_S = (168, 40, 36), (210, 92, 80), (118, 26, 24)


def font(px, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, max(6, int(px)))


# ------------------------------------------------------------------ icons
def box(d, x0, y0, w, h, dep, top=TOP, front=FRONT, side=SIDE, edge=EDGE, lw=1):
    dx, dy = dep * 0.85, -dep * 0.55
    d.polygon([(x0, y0), (x0 + dx, y0 + dy), (x0 + w + dx, y0 + dy), (x0 + w, y0)], fill=top, outline=edge, width=lw)
    d.polygon([(x0 + w, y0), (x0 + w + dx, y0 + dy), (x0 + w + dx, y0 + h + dy), (x0 + w, y0 + h)], fill=side, outline=edge, width=lw)
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=front, outline=edge, width=lw)
    return dx, dy


def arrow(d, x1, y1, x2, y2, col, lw):
    d.line((x1, y1, x2, y2), fill=col, width=lw)
    a = math.atan2(y2 - y1, x2 - x1); L = lw * 3.2
    for s in (-1, 1):
        d.line((x2, y2, x2 - L * math.cos(a + s * 0.5), y2 - L * math.sin(a + s * 0.5)), fill=col, width=lw)


def icon(d, kind, cx, cy, s):
    """Draw a device icon centred on (cx, cy); s = half-width in px. Returns icon half-height."""
    lw = max(1, int(s / 14))
    if kind == 'Server':
        w, h, dep = 0.95 * s, 1.85 * s, 0.6 * s
        x0, y0 = cx - w / 2 - dep * 0.4, cy - h / 2 + dep * 0.25
        box(d, x0, y0, w, h, dep, lw=lw)
        d.rectangle((x0 + w * 0.12, y0 + h * 0.08, x0 + w * 0.88, y0 + h * 0.2), fill=LIGHT)
        for k in range(3):
            yy = y0 + h * (0.3 + 0.06 * k); d.line((x0 + w * 0.15, yy, x0 + w * 0.85, yy), fill=LIGHT, width=lw)
        return h / 2
    if kind == 'Switch':
        w, h, dep = 2.0 * s, 0.42 * s, 1.0 * s
        x0, y0 = cx - w / 2 - dep * 0.42, cy + 0.05 * s
        dx, dy = box(d, x0, y0, w, h, dep, lw=lw)
        # Cisco workgroup-switch arrows on the top face
        ty = y0 + dy / 2; tx = x0 + dx / 2
        for k, (a, b) in enumerate(((0.18, 0.46), (0.54, 0.82))):
            yy = ty + (k - 0.5) * abs(dy) * 0.42
            if k == 0: arrow(d, tx + w * a, yy, tx + w * b, yy, (255, 255, 255), lw + 1)
            else: arrow(d, tx + w * b, yy, tx + w * a, yy, (255, 255, 255), lw + 1)
        for k in range(8):
            px = x0 + w * (0.1 + 0.1 * k); d.rectangle((px, y0 + h * 0.35, px + w * 0.05, y0 + h * 0.7), fill=LIGHT)
        return 0.7 * s
    if kind in ('Pc', 'Laptop'):
        w, h, dep = 1.35 * s, 0.98 * s, 0.22 * s
        x0, y0 = cx - w / 2, cy - h * 0.62
        box(d, x0, y0, w, h, dep, lw=lw)
        d.rectangle((x0 + w * 0.09, y0 + h * 0.1, x0 + w * 0.91, y0 + h * 0.86), fill=SCREEN, outline=EDGE, width=lw)
        d.rectangle((cx - w * 0.08, y0 + h, cx + w * 0.08, y0 + h * 1.12), fill=SIDE)
        box(d, cx - w * 0.6, y0 + h * 1.14, w * 1.1, h * 0.13, 0.5 * s, lw=lw)
        return 0.75 * s
    if kind == 'Cloud':
        pts = [(-0.62, 0.1, 0.42), (-0.2, -0.22, 0.5), (0.3, -0.12, 0.48), (0.7, 0.14, 0.36), (0.05, 0.22, 0.5), (-0.4, 0.3, 0.34)]
        for ox, oy, r in pts:
            d.ellipse((cx + (ox - r) * s * 1.3, cy + (oy - r) * s * 1.05, cx + (ox + r) * s * 1.3, cy + (oy + r) * s * 1.05), fill=EDGE)
        for ox, oy, r in pts:
            r2 = r - 0.06
            d.ellipse((cx + (ox - r2) * s * 1.3, cy + (oy - r2) * s * 1.05, cx + (ox + r2) * s * 1.3, cy + (oy + r2) * s * 1.05), fill=(126, 178, 196))
        for ox, oy, r in pts[:3]:
            r2 = r * 0.55
            d.ellipse((cx + (ox - r2) * s * 1.3, cy + (oy - r2 - 0.12) * s * 1.05, cx + (ox + r2) * s * 1.3, cy + (oy + r2 - 0.12) * s * 1.05), fill=(168, 210, 222))
        return 0.65 * s
    if kind == 'ASA':
        w, h, dep = 1.15 * s, 0.6 * s, 0.5 * s
        x0, y0 = cx - w / 2 - dep * 0.4, cy + 0.15 * s
        box(d, x0, y0, w, h, dep, top=RED_T, front=RED_F, side=RED_S, edge=(90, 20, 18), lw=lw)
        for r in range(3):
            yy = y0 + h * (r + 1) / 3.2; d.line((x0, yy, x0 + w, yy), fill=(230, 150, 140), width=lw)
            for c in range(4):
                xx = x0 + w * (c + (0.5 if r % 2 else 0)) / 4
                if x0 < xx < x0 + w: d.line((xx, yy - h / 3.2, xx, yy), fill=(230, 150, 140), width=lw)
        bw, bh = 0.95 * s, 0.75 * s
        bx, by = cx - bw / 2 - dep * 0.3, y0 - bh - dep * 0.1
        box(d, bx, by, bw, bh, dep * 0.8, lw=lw)
        r = 0.27 * s; mx, my = bx + bw * 0.5, by + bh * 0.45
        d.line((mx + r * 0.6, my + r * 0.6, mx + r * 1.4, my + r * 1.4), fill=(240, 240, 240), width=lw * 3)
        d.ellipse((mx - r, my - r, mx + r, my + r), fill=(235, 245, 248), outline=(240, 240, 240), width=lw * 2)
        return 0.9 * s
    if kind == 'LightWeightAccessPoint':
        w, h, dep = 1.6 * s, 0.38 * s, 0.75 * s
        x0, y0 = cx - w / 2 - dep * 0.4, cy
        box(d, x0, y0, w, h, dep, lw=lw)
        for k in range(10):
            px = x0 + w * (0.08 + 0.085 * k); d.ellipse((px, y0 + h * 0.4, px + w * 0.035, y0 + h * 0.65), fill=LIGHT)
        return 0.55 * s
    if kind == 'HomeVoip':
        w, h, dep = 1.55 * s, 0.4 * s, 0.8 * s
        x0, y0 = cx - w / 2 - dep * 0.4, cy + 0.1 * s
        dx, dy = box(d, x0, y0, w, h, dep, lw=lw)
        d.rounded_rectangle((x0 + dx * 0.25, y0 + dy * 0.85, x0 + w * 0.42 + dx * 0.25, y0 + dy * 0.35), radius=s * 0.12, fill=EDGE)
        for k in range(4):
            px = x0 + w * (0.55 + 0.1 * k); d.ellipse((px, y0 + h * 0.4, px + w * 0.04, y0 + h * 0.65), fill=LIGHT)
        return 0.6 * s
    d.rectangle((cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), fill=FRONT, outline=EDGE)
    return s / 2


def link_light(d, x, y, sz, col=GREEN):
    d.polygon([(x, y - sz * 0.6), (x - sz * 0.6, y + sz * 0.45), (x + sz * 0.6, y + sz * 0.45)], fill=col)


def dashed(d, p, q, col, lw, dash, gap):
    L = math.dist(p, q); n = int(L // (dash + gap)) + 1
    for k in range(n):
        a = k * (dash + gap) / L; b = min(1, (k * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line((p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a, p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b), fill=col, width=lw)


def centred(d, x, y, text, f, col, halo=0):
    w = d.textlength(text, font=f)
    d.text((x - w / 2, y), text, font=f, fill=col, stroke_width=halo, stroke_fill=(255, 255, 255))


# ------------------------------------------------------------------ helpers
def load(path):
    r = ET.parse(path).getroot()
    devs = []
    for dv in r.find('NETWORK/DEVICES').findall('DEVICE'):
        e = dv.find('ENGINE'); lg = dv.find('WORKSPACE/LOGICAL')
        devs.append({'name': e.findtext('NAME'), 'type': e.findtext('TYPE'), 'ref': e.findtext('SAVE_REF_ID'),
                     'x': float(lg.findtext('X')), 'y': float(lg.findtext('Y'))})
    by = {d['ref']: d for d in devs}
    links = []
    for l in r.find('NETWORK/LINKS').findall('LINK'):
        c = l.find('CABLE')
        links.append((by[c.findtext('FROM')], by[c.findtext('TO')], c.findtext('TYPE') == 'eCrossOver'))
    return r, devs, links


def draw_links(d, links, P, K, s_units, lw, light_sz, dash=(9, 6)):
    for a, b, xo in links:
        p, q = P(a['x'], a['y']), P(b['x'], b['y'])
        if xo: dashed(d, p, q, INK, lw, dash[0] * K, dash[1] * K)
        else: d.line((*p, *q), fill=INK, width=lw)
    for a, b, xo in links:
        p, q = P(a['x'], a['y']), P(b['x'], b['y'])
        L = math.dist(p, q)
        if L < 1: continue
        off = min(0.42 * L, s_units * K * 1.45)
        for (x0, y0), (x1, y1) in ((p, q), (q, p)):
            t = off / L
            link_light(d, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, light_sz)


def draw_devices(d, devs, P, K, s_units, label_px):
    f = font(label_px)
    for dv in devs:
        if dv['type'] == 'Power Distribution Device' or dv['x'] > 3000: continue
        cx, cy = P(dv['x'], dv['y'])
        hh = icon(d, dv['type'], cx, cy, s_units * K)
        centred(d, cx, cy + hh + 0.15 * s_units * K, dv['name'], f, LABEL, halo=max(1, int(label_px / 9)))


# ------------------------------------------------------------------ logical view
def render_logical(xml, out):
    r, devs, links = load(xml)
    K = 1.7; S = 21
    pw = r.find('PHYSICALWORKSPACE')
    notes = [(float(n.findtext('X')), float(n.findtext('Y')), n.findtext('TEXT') or '') for n in pw.find('NOTES').findall('NOTE') if (n.findtext('TEXT') or '').strip()]
    rects = []
    for rc in r.find('RECTANGLES').findall('RECTANGLE'):
        col = tuple(int(rc.find('Color').findtext(c)) for c in ('Red', 'Green', 'Blue'))
        rects.append((float(rc.findtext('TopLeftX')), float(rc.findtext('TopLeftY')), float(rc.findtext('BottomRightX')), float(rc.findtext('BottomRightY')), col))
    xs = [dv['x'] for dv in devs if dv['x'] < 3000] + [x for x, _, _ in notes] + [r_[2] for r_ in rects]
    ys = [dv['y'] for dv in devs if dv['y'] < 3000] + [y for _, y, _ in notes] + [r_[3] for r_ in rects]
    X0, Y0 = 10, 10
    W = int((max(xs) + 20 - X0) * K); H = int((max(ys) + 75 - Y0) * K)
    img = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(img)
    P = lambda x, y: ((x - X0) * K, (y - Y0) * K)
    for x1, y1, x2, y2, col in rects:
        d.rectangle((*P(x1, y1), *P(x2, y2)), fill=col, outline=(0, 0, 0), width=2)
    draw_links(d, links, P, K, S, max(2, int(1.3 * K)), 7.5 * K)
    nf = font(15 * K)
    for x, y, t in notes:
        d.multiline_text(P(x, y), t, font=nf, fill=INK, spacing=int(2 * K), stroke_width=3, stroke_fill=(255, 255, 255))
    draw_devices(d, devs, P, K, S, 16 * K)
    img.save(out)
    print('logical', img.size)


# ------------------------------------------------------------------ rack view
RU = {'Switch': 1, 'ASA': 1, 'Server': 2, 'Cloud': 1, 'Power Distribution Device': 1}


def faceplate(d, kind, name, x0, y0, w, uh):
    h = RU.get(kind, 1) * uh
    if kind == 'Switch':
        d.rectangle((x0, y0, x0 + w, y0 + h - 2), fill=(62, 68, 74), outline=(25, 25, 28), width=2)
        d.rectangle((x0 + 6, y0 + 6, x0 + w * 0.14, y0 + h - 8), fill=(30, 110, 160))
        for row in range(2):
            for k in range(12):
                px = x0 + w * 0.2 + k * w * 0.042; py = y0 + 7 + row * (h - 16) / 2
                d.rectangle((px, py, px + w * 0.032, py + (h - 20) / 2), fill=(18, 18, 20), outline=(150, 150, 150))
        for k in range(2):
            px = x0 + w * 0.76 + k * w * 0.06; d.rectangle((px, y0 + 9, px + w * 0.045, y0 + h - 11), fill=(18, 18, 20), outline=(190, 190, 190))
        for k in range(3): d.ellipse((x0 + w * 0.9 + k * 9, y0 + h / 2 - 3, x0 + w * 0.9 + k * 9 + 6, y0 + h / 2 + 3), fill=(90, 210, 90))
    elif kind == 'ASA':
        d.rectangle((x0, y0 + h - 5, x0 + w, y0 + h - 1), fill=(120, 120, 125))  # shelf
        bw = w * 0.5
        d.rectangle((x0 + 8, y0 + 4, x0 + 8 + bw, y0 + h - 6), fill=(40, 40, 44), outline=(10, 10, 10), width=2)
        for k in range(8):
            px = x0 + 8 + bw * (0.3 + 0.08 * k); d.rectangle((px, y0 + 9, px + bw * 0.06, y0 + h - 12), fill=(15, 15, 15), outline=(160, 160, 160))
        d.ellipse((x0 + 16, y0 + h / 2 - 4, x0 + 24, y0 + h / 2 + 4), fill=(90, 210, 90))
    elif kind == 'Server':
        d.rectangle((x0, y0, x0 + w, y0 + h - 2), fill=(205, 208, 212), outline=(60, 60, 64), width=2)
        for row in range(2):
            for k in range(6):
                px = x0 + w * 0.08 + k * w * 0.11; py = y0 + 7 + row * (h - 14) / 2
                d.rectangle((px, py, px + w * 0.095, py + (h - 22) / 2), fill=(150, 154, 160), outline=(80, 80, 84))
        d.rectangle((x0 + w * 0.78, y0 + 8, x0 + w * 0.94, y0 + h - 10), fill=(45, 48, 52))
        d.ellipse((x0 + w * 0.82, y0 + h / 2 - 5, x0 + w * 0.82 + 10, y0 + h / 2 + 5), fill=(90, 210, 90))
    elif kind == 'Cloud':
        d.rectangle((x0, y0 + h - 5, x0 + w, y0 + h - 1), fill=(120, 120, 125))
        d.rectangle((x0 + 8, y0 + 5, x0 + w * 0.35, y0 + h - 6), fill=(245, 245, 245), outline=(80, 80, 80), width=2)
        d.ellipse((x0 + 16, y0 + h / 2 - 4, x0 + 24, y0 + h / 2 + 4), fill=(90, 210, 90))
    else:  # PDU
        d.rectangle((x0, y0 + 3, x0 + w, y0 + h - 4), fill=(28, 28, 30), outline=(10, 10, 10), width=2)
        for k in range(10):
            px = x0 + w * (0.08 + 0.085 * k); d.rectangle((px, y0 + 8, px + w * 0.045, y0 + h - 9), fill=(70, 70, 74))
    return h


MODELS = [('CORE', 'Cisco C1300-12XS'), ('ASW', 'Cisco C1300-48P-4X'), ('CAIRNS-SW', 'Cisco C1300-24P-4X'),
          ('DMZ-SW', 'Cisco C1300-24T-4X'), ('FW-', 'FortiGate 70G (shelf)'), ('HYP', 'Dell PowerEdge R360'),
          ('NAS', 'Synology RS2423RP+'), ('PBX', 'Grandstream UCM6302 (shelf)'), ('PDU', 'rack PDU'),
          ('Brisbane ISP', 'nbn NTD (shelf)'), ('Cairns ISP', 'nbn NTD (shelf)')]


def model_of(n):
    for k, m in MODELS:
        if n.startswith(k): return m
    return ''


def render_racks(xml, out):
    r, devs, _ = load(xml)
    types = {dv['name']: dv['type'] for dv in devs}
    pw = r.find('PHYSICALWORKSPACE')
    racks = []
    for room in pw.iter('NODE'):
        if room.findtext('TYPE') != '3': continue
        for rk in room.find('CHILDREN').findall('NODE'):
            if rk.findtext('TYPE') != '4': continue
            kids = sorted(((float(c.findtext('X')), c.findtext('NAME')) for c in rk.find('CHILDREN').findall('NODE') if c.findtext('TYPE') == '6'))
            racks.append((room.findtext('NAME'), rk.findtext('NAME'), [n for _, n in kids]))
    UH, RW, GAP, LABW, TOPM = 25, 290, 40, 330, 150
    NU_MAX = 42
    W = len(racks) * (RW + 60 + LABW) + GAP * (len(racks) + 1)
    H = TOPM + NU_MAX * UH + 70
    img = Image.new('RGB', (W, H), (236, 238, 240)); d = ImageDraw.Draw(img)
    ft, fr, fl, fm, fs = font(34, True), font(27, True), font(29), font(22), font(17)
    x = GAP
    for room, rack, kids in racks:
        NU = 12 if 'Cairns' in rack else 42
        rx0 = x; ry0 = TOPM + (NU_MAX - NU) * UH
        centred(d, rx0 + (RW + 60) / 2, ry0 - 115, room, fr, (70, 70, 70))
        centred(d, rx0 + (RW + 60) / 2, ry0 - 78, f'{rack} ({NU}U)', ft, (20, 20, 20))
        d.rectangle((rx0, ry0 - 16, rx0 + RW + 60, ry0 + NU * UH + 16), fill=(34, 34, 38), outline=(10, 10, 10), width=3)
        for side in (rx0 + 8, rx0 + RW + 32):
            d.rectangle((side, ry0, side + 20, ry0 + NU * UH), fill=(150, 152, 156))
            for u in range(NU * 3):
                hy = ry0 + u * UH / 3 + 3; d.rectangle((side + 7, hy, side + 13, hy + 4), fill=(40, 40, 44))
        d.rectangle((rx0 + 30, ry0, rx0 + RW + 30, ry0 + NU * UH), fill=(52, 52, 56))
        for u in range(0, NU, 2):
            centred(d, rx0 - 20, ry0 + u * UH + 3, str(NU - u), fs, (90, 90, 90))
        y = ry0 + 3
        for n in kids:
            t = types.get(n, '')
            h = faceplate(d, t, n, rx0 + 30, y, RW, UH)
            ly = y + h / 2 - 17
            d.text((rx0 + RW + 72, ly), n, font=fl, fill=LABEL)
            d.text((rx0 + RW + 72 + d.textlength(n, font=fl) + 10, ly + 6), model_of(n), font=fm, fill=(95, 95, 95))
            y += h + 2
        if not kids:
            centred(d, rx0 + 30 + RW / 2, ry0 + 40, 'patch panels and', fm, (200, 200, 200))
            centred(d, rx0 + 30 + RW / 2, ry0 + 68, 'cable management', fm, (200, 200, 200))
        x += RW + 60 + LABW + GAP
    img.save(out)
    print('racks', img.size, [(a, b, len(c)) for a, b, c in racks])


# ------------------------------------------------------------------ floor-plan view
def render_floor(xml, bg, out):
    r, devs, links = load(xml)
    K, S = 3.75, 23
    bgi = Image.open(bg).convert('RGB')
    xs = [dv['x'] for dv in devs if dv['x'] < 3000]; ys = [dv['y'] for dv in devs if dv['y'] < 3000]
    W = int(max(bgi.width, max(xs) + 45) * K); H = int(max(bgi.height, max(ys) + 45) * K)
    img = Image.new('RGB', (W, H), (255, 255, 255))
    img.paste(bgi.resize((int(bgi.width * K), int(bgi.height * K)), Image.LANCZOS), (0, 0))
    d = ImageDraw.Draw(img)
    P = lambda x, y: (x * K, y * K)
    draw_links(d, links, P, K, S, max(3, int(2.6 * K)), 10 * K, dash=(11, 7))
    draw_devices(d, devs, P, K, S, 11.5 * K)
    img.save(out)
    print('floor', img.size)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'logical': render_logical(sys.argv[2], sys.argv[3])
    elif mode == 'racks': render_racks(sys.argv[2], sys.argv[3])
    elif mode == 'floor': render_floor(sys.argv[2], sys.argv[3], sys.argv[4])
