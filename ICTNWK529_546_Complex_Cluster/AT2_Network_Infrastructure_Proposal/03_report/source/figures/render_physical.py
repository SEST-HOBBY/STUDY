#!/usr/bin/env python3
"""Render the student's FLOOR_PLAN_FINAL.pkt (Packet Tracer 8.2.1) floor-plan view at
high resolution (Figure 1b of the report).

Source of geometry: work/analysis/inventory_floorplan.json (extracted from the decrypted
.pkt XML by extract_inventory.py). Coordinate model, verified against the student's own
screenshot by FFT cross-correlation (screenshot = workspace * 0.75 + (1, 1) px, peak 0.63):
  * the floor-plan JPEG is the ROOTCLUSTER background (CLUSTER_EMBEDDED_BG_IMAGE,
    TILED_BG=false) drawn at the logical-workspace origin at its native 604 x 813 px;
  * each device's <WORKSPACE><LOGICAL><X>/<Y> is the CENTRE of its icon in that pixel space;
  * links run centre to centre; PT draws straight-through cables solid, crossover dashed.
Run with:  python3 -I render_physical.py
Only Pillow is used (no matplotlib).
"""
import json
import math

from PIL import Image, ImageDraw, ImageFont

BASE = "/tmp/claude-0/-home-user-STUDY/f8a3790f-8c1d-5a3f-8f9c-d2abf23b0604/scratchpad/"
INV = BASE + "work/analysis/inventory_floorplan.json"
BG = BASE + "pkt/floor_bg_0_IMAGE_CONTENT.jpg"
OUT = BASE + "work/figures/fig1b_physical_layout_render.png"
TMP = BASE + "work/figures/tmp/"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

K = 3.75                       # workspace px -> output px (604 px background -> 2265 px)
CANVAS_W_N, CANVAS_H_N = 660, 858   # workspace-unit canvas; bg is 604 x 813, cluster spills right/below
LEGEND_H = 190                 # px strip under the plan for the legend
LINK_W = 3                     # px; 2 px was near-invisible against the plan's own linework at 2475 px wide
LABEL_PX = 34                  # label font size in px
INK = (28, 28, 32)
HALO = (255, 255, 255)

COLOURS = {  # fill, outline
    "Pc": ((47, 111, 181), (20, 55, 100)),
    "Laptop": ((42, 157, 143), (18, 85, 78)),
    "HomeVoip": ((123, 79, 163), (70, 40, 100)),
    "LightWeightAccessPoint": ((232, 135, 43), (140, 75, 15)),
    "Switch": ((58, 158, 75), (25, 85, 38)),
    "Server": ((92, 99, 112), (40, 45, 55)),
    "ASA": ((192, 57, 43), (110, 25, 18)),
    "Cloud": ((205, 214, 224), (92, 99, 112)),
}
LEGEND_NAMES = [
    ("Pc", "PC"), ("Laptop", "Laptop"), ("HomeVoip", "VoIP phone"),
    ("LightWeightAccessPoint", "Wireless AP"), ("Switch", "Switch (2960)"),
    ("Server", "Server"), ("ASA", "ASA firewall"), ("Cloud", "ISP cloud"),
]


def P(x, y):
    """workspace units -> output px"""
    return x * K, y * K


# ---------------------------------------------------------------- icon drawing
def draw_icon(d, kind, cx, cy, k):
    """Draw a device glyph centred on (cx, cy) px; k is the px-per-workspace-unit scale."""
    fill, line = COLOURS.get(kind, ((150, 150, 150), (60, 60, 60)))
    w = max(2, int(round(k * 0.6)))  # outline width
    if kind == "Pc":
        mw, mh = 30 * k, 22 * k
        d.rounded_rectangle((cx - mw / 2, cy - mh / 2 - 3 * k, cx + mw / 2, cy + mh / 2 - 3 * k),
                            radius=3 * k, fill=fill, outline=line, width=w)
        d.rectangle((cx - mw / 2 + 4 * k, cy - mh / 2 + 1 * k, cx + mw / 2 - 4 * k, cy + mh / 2 - 6 * k),
                    fill=(215, 230, 245))
        d.rectangle((cx - 3 * k, cy + mh / 2 - 3 * k, cx + 3 * k, cy + mh / 2 + 1 * k), fill=line)
        d.rectangle((cx - 10 * k, cy + mh / 2 + 1 * k, cx + 10 * k, cy + mh / 2 + 4 * k), fill=line)
    elif kind == "Laptop":
        d.polygon([(cx - 13 * k, cy - 9 * k), (cx + 11 * k, cy - 9 * k), (cx + 13 * k, cy + 4 * k), (cx - 15 * k, cy + 4 * k)],
                  fill=fill, outline=line, width=w)
        d.rectangle((cx - 10 * k, cy - 7 * k, cx + 9 * k, cy + 2 * k), fill=(215, 240, 236))
        d.rectangle((cx - 17 * k, cy + 4 * k, cx + 15 * k, cy + 8 * k), fill=line)
    elif kind == "HomeVoip":
        d.rounded_rectangle((cx - 15 * k, cy - 9 * k, cx + 15 * k, cy + 10 * k), radius=3 * k, fill=fill, outline=line, width=w)
        d.rectangle((cx - 1 * k, cy - 6 * k, cx + 12 * k, cy + 2 * k), fill=(235, 225, 245))
        d.rounded_rectangle((cx - 13 * k, cy - 7 * k, cx - 7 * k, cy + 8 * k), radius=2 * k, fill=(235, 225, 245))
    elif kind == "LightWeightAccessPoint":
        r = 13 * k
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=line, width=w)
        for rr in (4 * k, 8 * k):
            d.arc((cx - rr, cy - rr - 1 * k, cx + rr, cy + rr - 1 * k), start=200, end=340, fill=(255, 255, 255), width=w)
        d.ellipse((cx - 2 * k, cy + 2 * k, cx + 2 * k, cy + 6 * k), fill=(255, 255, 255))
    elif kind == "Switch":
        sw, sh = 44 * k, 16 * k
        d.rounded_rectangle((cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2), radius=2 * k, fill=fill, outline=line, width=w)
        for i in range(6):  # port dots
            px = cx - sw / 2 + 5 * k + i * 6 * k
            d.rectangle((px, cy + 2 * k, px + 3 * k, cy + 5 * k), fill=(200, 240, 205))
        d.line((cx - 16 * k, cy - 3 * k, cx + 16 * k, cy - 3 * k), fill=(200, 240, 205), width=w)
    elif kind == "Server":
        sw, sh = 22 * k, 36 * k
        d.rounded_rectangle((cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2), radius=2 * k, fill=fill, outline=line, width=w)
        for i in range(4):
            yy = cy - sh / 2 + 5 * k + i * 7 * k
            d.rectangle((cx - sw / 2 + 4 * k, yy, cx + sw / 2 - 4 * k, yy + 3 * k), fill=(190, 196, 206))
            d.ellipse((cx + sw / 2 - 8 * k, yy + 0.5 * k, cx + sw / 2 - 6 * k, yy + 2.5 * k), fill=(120, 220, 140))
    elif kind == "ASA":
        sw, sh = 38 * k, 24 * k
        d.rectangle((cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2), fill=fill, outline=line, width=w)
        for r_i in range(3):  # brick courses
            yy = cy - sh / 2 + (r_i + 1) * sh / 4
            d.line((cx - sw / 2, yy, cx + sw / 2, yy), fill=(245, 225, 220), width=w)
            off = (sw / 6) if r_i % 2 else 0
            for b in range(4):
                xx = cx - sw / 2 + off + b * sw / 3
                if cx - sw / 2 < xx < cx + sw / 2:
                    d.line((xx, yy - sh / 4, xx, yy), fill=(245, 225, 220), width=w)
    elif kind == "Cloud":
        for (ox, oy, r) in ((-12, 2, 9), (-4, -6, 11), (7, -3, 10), (13, 4, 8), (0, 5, 9)):
            d.ellipse((cx + (ox - r) * k, cy + (oy - r) * k, cx + (ox + r) * k, cy + (oy + r) * k), fill=fill, outline=line, width=w)
        for (ox, oy, r) in ((-12, 2, 9), (-4, -6, 11), (7, -3, 10), (13, 4, 8), (0, 5, 9)):
            d.ellipse((cx + (ox - r) * k + w, cy + (oy - r) * k + w, cx + (ox + r) * k - w, cy + (oy + r) * k - w), fill=fill)
    else:
        d.rectangle((cx - 12 * k, cy - 12 * k, cx + 12 * k, cy + 12 * k), fill=fill, outline=line, width=w)


def icon_bbox(kind, cx, cy, k):
    half = {"Pc": (15, 15), "Laptop": (17, 10), "HomeVoip": (15, 10), "LightWeightAccessPoint": (13, 13),
            "Switch": (22, 8), "Server": (11, 18), "ASA": (19, 12), "Cloud": (22, 16)}.get(kind, (12, 12))
    return (cx - half[0] * k, cy - half[1] * k, cx + half[0] * k, cy + half[1] * k)


# ---------------------------------------------------------------- helpers
def dashed_line(d, p0, p1, fill, width, dash=22, gap=12):
    x0, y0 = p0
    x1, y1 = p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L == 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    t = 0.0
    while t < L:
        e = min(t + dash, L)
        d.line((x0 + ux * t, y0 + uy * t, x0 + ux * e, y0 + uy * e), fill=fill, width=width)
        t += dash + gap


def overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if (w > 0 and h > 0) else 0.0


def wrap_label(name, font, max_w):
    if font.getlength(name) <= max_w or " " not in name:
        return name
    words = name.split(" ")
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wdt = max(font.getlength(a), font.getlength(b))
        if best is None or wdt < best[0]:
            best = (wdt, a + "\n" + b)
    return best[1]


# ---------------------------------------------------------------- main
def main():
    inv = json.load(open(INV))
    devs = [v for v in inv["devices"] if v["x"] < 3000]   # the two Power Distribution Devices sit at (3900, 3900), off-plan
    by_name = {v["name"]: v for v in devs}
    links = [l for l in inv["links"] if l["from_device"] in by_name and l["to_device"] in by_name]

    W, H = int(CANVAS_W_N * K), int(CANVAS_H_N * K)
    img = Image.new("RGB", (W, H + LEGEND_H), (255, 255, 255))
    bg = Image.open(BG).convert("RGB")
    bgs = bg.resize((int(round(bg.width * K)), int(round(bg.height * K))), Image.LANCZOS)
    img.paste(bgs, (0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, LABEL_PX)
    font_small = ImageFont.truetype(FONT, 28)
    font_tag = ImageFont.truetype(FONT_B, 36)

    # floor tags in the white margin right of the plan
    bx = bgs.width + 18
    for txt, yy in (("1st floor", 14), ("2nd floor", bgs.height / 2 + 14)):
        d.text((bx, yy), txt, font=font_tag, fill=(70, 70, 75))

    # links: centre to centre, under the icons; crossover dashed like PT
    for l in links:
        a, b = by_name[l["from_device"]], by_name[l["to_device"]]
        p0, p1 = P(a["x"], a["y"]), P(b["x"], b["y"])
        if l["cable_type"] == "eCrossOver":
            dashed_line(d, p0, p1, INK, LINK_W)
        else:
            d.line((p0, p1), fill=INK, width=LINK_W)

    # icons
    boxes = {}
    for v in devs:
        cx, cy = P(v["x"], v["y"])
        draw_icon(d, v["pt_type"], cx, cy, K)
        boxes[v["name"]] = icon_bbox(v["pt_type"], cx, cy, K)

    # labels: greedy placement, crowded devices first
    def crowd(v):
        return sum(1 for u in devs if u is not v and abs(u["x"] - v["x"]) < 90 and abs(u["y"] - v["y"]) < 90)
    order = sorted(devs, key=lambda v: (-crowd(v), v["y"], v["x"]))
    placed = []     # label rects
    sw = 3          # halo stroke
    gap = 8
    for v in order:
        text = wrap_label(v["name"], font, 300)
        bb = d.multiline_textbbox((0, 0), text, font=font, stroke_width=sw, align="center")
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x0, y0, x1, y1 = boxes[v["name"]]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        near = [  # (left, top)
            (cx - tw / 2, y1 + gap), (cx - tw / 2, y0 - gap - th),
            (x1 + gap, cy - th / 2), (x0 - gap - tw, cy - th / 2),
            (x1 + gap, y1 + gap), (x0 - gap - tw, y1 + gap),
            (x1 + gap, y0 - gap - th), (x0 - gap - tw, y0 - gap - th),
        ]
        far = []
        for R in (70, 110, 150, 190):
            for ang in range(0, 360, 30):
                a = math.radians(ang)
                far.append((cx + R * math.cos(a) - tw / 2, cy + R * math.sin(a) - th / 2))
        cands = near + far
        best = None
        for i, (lx, ly) in enumerate(cands):
            rect = (lx - 4, ly - 4, lx + tw + 4, ly + th + 4)
            score = i * 40.0
            for r in placed:
                score += 3.0 * overlap(rect, r)
            for n2, r in boxes.items():
                score += (6.0 if n2 != v["name"] else 20.0) * overlap(rect, r)
            if rect[0] < 4 or rect[1] < 4 or rect[2] > W - 4 or rect[3] > H - 4:
                score += 1e6
            if best is None or score < best[0]:
                best = (score, i, lx, ly, rect)
        score, i, lx, ly, rect = best
        placed.append(rect)
        if i >= len(near):  # leader line from icon edge toward label
            lcx, lcy = (rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2
            # point on label rect nearest the icon centre
            px = min(max(cx, rect[0]), rect[2])
            py = min(max(cy, rect[1]), rect[3])
            # point on icon box edge toward the label
            qx = min(max(lcx, x0), x1)
            qy = min(max(lcy, y0), y1)
            d.line((qx, qy, px, py), fill=(110, 110, 120), width=2)
            d.ellipse((px - 4, py - 4, px + 4, py + 4), fill=(110, 110, 120))
        d.multiline_text((lx, ly), text, font=font, fill=INK, stroke_width=sw, stroke_fill=HALO, align="center")

    # legend strip: row 1 device glyphs, row 2 cable styles
    ly0 = H
    d.rectangle((0, ly0, W, ly0 + LEGEND_H), fill=(246, 247, 249))
    d.line((0, ly0, W, ly0), fill=(190, 190, 195), width=2)
    k2 = K * 0.5
    x = 40
    cy = ly0 + 62
    for kind, label in LEGEND_NAMES:
        draw_icon(d, kind, x + 22 * k2, cy, k2)
        d.text((x + 46 * k2, cy - 16), label, font=font_small, fill=INK)
        x += 46 * k2 + font_small.getlength(label) + 60
    cy = ly0 + 142
    x = 40
    d.line((x, cy, x + 110, cy), fill=INK, width=LINK_W)
    t = "solid: straight-through copper (host or server to switch, cloud to firewall)"
    d.text((x + 125, cy - 16), t, font=font_small, fill=INK)
    x += 125 + font_small.getlength(t) + 80
    dashed_line(d, (x, cy), (x + 110, cy), INK, LINK_W)
    d.text((x + 125, cy - 16), "dashed: crossover copper (switch to switch)", font=font_small, fill=INK)

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)

    # review crops at 100 %
    img.crop((int(430 * K), int(660 * K), W, H)).save(TMP + "crop_cluster.png")
    img.crop((0, 0, int(360 * K), int(260 * K))).save(TMP + "crop_topleft.png")
    img.crop((int(120 * K), int(440 * K), int(620 * K), int(680 * K))).save(TMP + "crop_mid.png")


if __name__ == "__main__":
    main()
