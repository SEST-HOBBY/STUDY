#!/usr/bin/env python3
"""Figure 3 for the HelpYou Mortgage report: proposed rack layout.

Writes two files from one geometry:
  fig3_rack_diagram.svg  hand-built SVG markup (2400 x 1400 viewBox)
  fig3_rack_diagram.png  the same drawing rasterised with Pillow at 150 dpi
                         equivalent (scale 150/96), because ImageMagick in this
                         environment has no SVG delegate.

Rack contents follow the draft report's section 4 rack table and the
corrections file (device names match the static-IP register in section 5.1).
"""
import os
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SVG_PATH = os.path.join(OUT_DIR, "fig3_rack_diagram.svg")
PNG_PATH = os.path.join(OUT_DIR, "fig3_rack_diagram.png")

W, H = 2400, 1400          # viewBox units (CSS px)
SCALE = 150 / 96           # "convert -density 150" equivalent for a 96 dpi SVG

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FAMILY = "DejaVu Sans, Liberation Sans, Arial, sans-serif"

INK = "#1f1f1f"
MUTED = "#5a5a5a"
TICK = "#6b6b6b"
RACK_FILL = "#fbfbfb"
RACK_STROKE = "#3a3a3a"
RAIL = "#a8a8a8"
RAIL_HOLE = "#6f6f6f"
GRID = "#e4e4e4"

# Colour by device type: (fill, stroke)
TYPES = {
    "network":  ("#cfe2f3", "#2f5f8f"),
    "security": ("#f4cccc", "#a33a3a"),
    "server":   ("#d9ead3", "#3f7f3f"),
    "storage":  ("#d9d2e9", "#5e4b8b"),
    "power":    ("#dcdcdc", "#595959"),
    "patching": ("#efe3c8", "#8c7a4a"),
}

U = 24                     # px per rack unit
RAIL_W = 12
RACK_W = 400               # outer width of a rack frame
TICK_W = 40                # width reserved for U numbers to the left of a rack
COL_GAP = 28
COL_PITCH = TICK_W + RACK_W + COL_GAP
MARGIN_X = (W - (5 * COL_PITCH - COL_GAP)) / 2

FRAME_TOP = 196            # top of the 42U frames
BASE_Y = FRAME_TOP + RAIL_W + 42 * U      # bottom of U1 (common floor line)


# ---------------------------------------------------------------- canvas ----
class Canvas:
    """Draws the same primitives into SVG markup and a Pillow image."""

    def __init__(self):
        self.svg = []
        self.img = Image.new("RGB", (round(W * SCALE), round(H * SCALE)), "white")
        self.d = ImageDraw.Draw(self.img)
        self._fonts = {}

    def _font(self, size, bold, scaled=True):
        key = (size, bold, scaled)
        if key not in self._fonts:
            px = round(size * SCALE) if scaled else size
            self._fonts[key] = ImageFont.truetype(FONT_B if bold else FONT_R, px)
        return self._fonts[key]

    def measure(self, s, size=16, bold=False):
        return self._font(size, bold, scaled=False).getlength(s)

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=1.0, rx=0, dash=None):
        attrs = [f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"']
        attrs.append(f'fill="{fill}"' if fill else 'fill="none"')
        if stroke:
            attrs.append(f'stroke="{stroke}" stroke-width="{sw}"')
            if dash:
                attrs.append(f'stroke-dasharray="{dash[0]} {dash[1]}"')
        if rx:
            attrs.append(f'rx="{rx}"')
        self.svg.append(f"<rect {' '.join(attrs)}/>")
        k = SCALE
        box = (x * k, y * k, (x + w) * k, (y + h) * k)
        if dash and stroke:
            if fill:
                self.d.rounded_rectangle(box, radius=rx * k, fill=fill)
            self._dashed_poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                              stroke, sw, dash)
        else:
            self.d.rounded_rectangle(box, radius=rx * k, fill=fill,
                                     outline=stroke, width=max(1, round(sw * k)) if stroke else 0)

    def line(self, x1, y1, x2, y2, stroke, sw=1.0, dash=None):
        extra = f' stroke-dasharray="{dash[0]} {dash[1]}"' if dash else ""
        self.svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                        f'stroke="{stroke}" stroke-width="{sw}"{extra}/>')
        if dash:
            self._dashed_poly([(x1, y1), (x2, y2)], stroke, sw, dash)
        else:
            k = SCALE
            self.d.line([(x1 * k, y1 * k), (x2 * k, y2 * k)], fill=stroke,
                        width=max(1, round(sw * k)))

    def _dashed_poly(self, pts, stroke, sw, dash):
        k = SCALE
        on, off = dash
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if length == 0:
                continue
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            pos = 0.0
            while pos < length:
                seg = min(on, length - pos)
                sx, sy = x1 + ux * pos, y1 + uy * pos
                ex, ey = x1 + ux * (pos + seg), y1 + uy * (pos + seg)
                self.d.line([(sx * k, sy * k), (ex * k, ey * k)], fill=stroke,
                            width=max(1, round(sw * k)))
                pos += on + off

    def text(self, x, y, s, size=16, bold=False, anchor="start", fill=INK):
        """y is the text baseline. anchor: start | middle | end."""
        weight = ' font-weight="bold"' if bold else ""
        ta = "" if anchor == "start" else f' text-anchor="{anchor}"'
        self.svg.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY}" '
                        f'font-size="{size}"{weight}{ta} fill="{fill}">{escape(s)}</text>')
        pil_anchor = {"start": "ls", "middle": "ms", "end": "rs"}[anchor]
        self.d.text((x * SCALE, y * SCALE), s, font=self._font(size, bold),
                    fill=fill, anchor=pil_anchor)

    def save(self, title):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}">\n<title>{escape(title)}</title>\n'
                f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>\n')
        with open(SVG_PATH, "w", encoding="utf-8") as fh:
            fh.write(head + "\n".join(self.svg) + "\n</svg>\n")
        self.img.save(PNG_PATH, dpi=(150, 150))


# ------------------------------------------------------------ rack data -----
def dev(name, model, typ, units=1, ports=False):
    return {"kind": "device", "name": name, "model": model, "type": typ,
            "units": units, "ports": ports}


def shelf(*devices):
    """A 1U shelf carrying desktop units: (name, model, type, width fraction)."""
    return {"kind": "shelf", "units": 1, "devices": list(devices)}


def spare(units):
    return {"kind": "spare", "units": units}


CM = dev("Cable manager", "horizontal, 1U", "patching")

RACKS = [
    {
        "title": "Floor 1 network rack (42U)",
        "sub": "Server room, head office",
        "units": 42,
        "items": [
            dev("F1-P1", "24-port panel, runs 1-24", "patching", ports=True),
            dev("F1-P2", "24-port panel, runs 25-48", "patching", ports=True),
            dev("F1-P3", "24-port panel, runs 49-72", "patching", ports=True),
            dev("F1-P4", "24-port panel, runs 73-96", "patching", ports=True),
            CM,
            dev("CORE 1", "Cisco C1300-12XS", "network", ports=True),
            dev("CORE 2", "Cisco C1300-12XS", "network", ports=True),
            shelf(("nbn NTD", "", "network", 0.30),
                  ("FW-HQ", "FortiGate 70G", "security", 0.64)),
            dev("DMZ switch", "Cisco C1300-24T-4X", "network", ports=True),
            shelf(("PBX-01", "Grandstream UCM6302", "network", 0.80)),
            dev("ASW-1", "Cisco C1300-48P-4X", "network", ports=True),
            dev("ASW-2", "Cisco C1300-48P-4X", "network", ports=True),
            dev("ASW-3", "Cisco C1300-48P-4X", "network", ports=True),
            spare(27),
            dev("UPS", "2U rack-mount UPS", "power", units=2),
        ],
    },
    {
        "title": "Floor 1 server space (42U)",
        "sub": "Server room, head office",
        "units": 42,
        "items": [
            dev("HYP-01", "Dell PowerEdge R360", "server"),
            dev("KVM console", "1U drawer / shelf", "patching"),
            spare(38),
            dev("UPS", "2U rack-mount UPS", "power", units=2),
        ],
    },
    {
        "title": "Floor 2 patch-panel rack (42U)",
        "sub": "Existing rack, 120 Cat 6 runs",
        "units": 42,
        "items": [
            dev("F2-P1", "24-port panel, runs 1-24", "patching", ports=True),
            CM,
            dev("F2-P2", "24-port panel, runs 25-48", "patching", ports=True),
            CM,
            dev("F2-P3", "24-port panel, runs 49-72", "patching", ports=True),
            CM,
            dev("F2-P4", "24-port panel, runs 73-96", "patching", ports=True),
            CM,
            dev("F2-P5", "24-port panel, runs 97-120", "patching", ports=True),
            spare(33),
        ],
    },
    {
        "title": "Floor 2 equipment rack (42U)",
        "sub": "Existing rack, currently empty",
        "units": 42,
        "items": [
            dev("ASW-4", "Cisco C1300-48P-4X", "network", ports=True),
            dev("ASW-5", "Cisco C1300-48P-4X", "network", ports=True),
            dev("ASW-6", "Cisco C1300-48P-4X", "network", ports=True),
            dev("HYP-02", "Dell PowerEdge R360", "server"),
            dev("NAS-BACKUP", "Synology RS2423RP+ 12-bay NAS", "storage", units=2),
            spare(34),
            dev("UPS", "2U rack-mount UPS", "power", units=2),
        ],
    },
    {
        "title": "Cairns branch cabinet (12U)",
        "sub": "Secured wall cabinet",
        "units": 12,
        "items": [
            shelf(("nbn NTD", "ISP handoff", "network", 0.62)),
            shelf(("FW-BR", "FortiGate 70G", "security", 0.62)),
            dev("Cairns switch", "Cisco C1300-24P-4X", "network", ports=True),
            dev("Patch panel", "24-port, branch outlets", "patching", ports=True),
            spare(6),
            dev("UPS", "2U rack-mount UPS", "power", units=2),
        ],
    },
]

LEGEND = [
    ("network", "Network: switches, PBX, nbn NTD"),
    ("security", "Security: FortiGate 70G firewalls"),
    ("server", "Servers: Dell R360 Hyper-V hosts"),
    ("storage", "Storage: Synology backup NAS"),
    ("power", "Power: rack-mount UPS"),
    ("patching", "Patching: panels, cable managers, shelves"),
]

NOTES = [
    "Rack units are counted from the base (U1). Floor 2 racks and the floor 1 server space are drawn as standard 42U frames; usable height is confirmed on site before positions are fixed.",
    "Patching: four 24-port panels terminate the 96 existing floor 1 Cat 5e runs and five 24-port panels terminate the 120 existing floor 2 Cat 6 runs; spare space takes panels for up to 60 extra runs.",
    "Internet path: the nbn NTD hands off to FW-HQ, which sits in front of CORE 1 and CORE 2 (ISP, then firewall, then core stack). FW-BR does the same job at Cairns. Shelf items are desktop units.",
]

WARNINGS = []


# -------------------------------------------------------------- drawing -----
def draw_label(c, x, cy, name, model, box_w, name_fill=INK):
    """Bold name then regular model on one baseline; returns the text width."""
    size = 16
    base = cy + 6                      # visually centres 16 px caps in the band
    nw = c.measure(name, size, True)
    c.text(x, base, name, size, True, fill=name_fill)
    total = nw
    if model:
        c.text(x + nw + 10, base, model, size, False, fill=INK)
        total += 10 + c.measure(model, size, False)
    if total > box_w - 16:
        WARNINGS.append(f"label overflow: '{name} {model}' needs {total:.0f} px, box {box_w:.0f}")
    return total


def draw_ports(c, x_right, cy, count, stroke, text_right):
    """Row of small port squares at the right end of a switch or patch panel."""
    pitch, side = 10, 6
    n = min(count, int((x_right - 14 - text_right - 24) // pitch))
    if n < 4:
        return
    x = x_right - 10 - n * pitch
    for i in range(n):
        c.rect(x + i * pitch, cy - side / 2, side, side, fill="#ffffff", stroke=stroke, sw=1)


def draw_device(c, x, y, w, h, name, model, typ, ports=False):
    fill, stroke = TYPES[typ]
    c.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=3)
    if h >= 2 * U - 2:                 # two-line label for 2U and taller
        c.text(x + 12, y + h / 2 - 3, name, 16, True)
        c.text(x + 12, y + h / 2 + 17, model, 16, False)
        if c.measure(model, 16) > w - 24 or c.measure(name, 16, True) > w - 24:
            WARNINGS.append(f"label overflow (2-line): '{name} / {model}' in box {w:.0f}")
        return
    tw = draw_label(c, x + 12, y + h / 2, name, model, w)
    if ports:
        draw_ports(c, x + w, y + h / 2, 12, stroke, x + 12 + tw)


def draw_rack(c, col, rack):
    units = rack["units"]
    x_rack = MARGIN_X + col * COL_PITCH + TICK_W
    height = units * U
    top_u = BASE_Y - height                 # top of the highest U
    frame_top = top_u - RAIL_W
    frame_bot = BASE_Y + RAIL_W
    inner_x = x_rack + RAIL_W
    inner_w = RACK_W - 2 * RAIL_W

    # Header
    cx = x_rack + RACK_W / 2
    c.text(cx, frame_top - 34, rack["title"], 20, True, "middle")
    c.text(cx, frame_top - 12, rack["sub"], 16, False, "middle", fill=MUTED)

    # Frame, rails, mounting holes, U grid
    c.rect(x_rack, frame_top, RACK_W, frame_bot - frame_top, fill=RACK_FILL,
           stroke=RACK_STROKE, sw=2, rx=4)
    for rx in (x_rack, x_rack + RACK_W - RAIL_W):
        c.rect(rx, top_u, RAIL_W, height, fill=RAIL)
        hx = rx + RAIL_W / 2
        # three holes per U: 4 px hole, 4 px gap, starting 2 px into each U
        c.line(hx, top_u + 2, hx, BASE_Y - 2, RAIL_HOLE, 4, dash=(4, 4))
    for i in range(units + 1):
        y = top_u + i * U
        if 0 < i < units:
            c.line(inner_x, y, inner_x + inner_w, y, GRID, 1)
        c.line(x_rack - 6, y, x_rack, y, TICK, 1)
    for u in range(1, units + 1):
        cy = BASE_Y - (u - 0.5) * U
        c.text(x_rack - 9, cy + 6, str(u), 16, False, "end", fill=TICK)

    # Items, top to bottom
    y = top_u
    used = 0
    for it in rack["items"]:
        h = it["units"] * U
        used += it["units"]
        if it["kind"] == "device":
            draw_device(c, inner_x + 3, y + 1, inner_w - 6, h - 2,
                        it["name"], it["model"], it["type"], it["ports"])
        elif it["kind"] == "shelf":
            sfill, sstroke = TYPES["patching"]
            # thin shelf bar along the bottom of the U; desktop units sit on it
            c.rect(inner_x + 3, y + h - 4, inner_w - 6, 3, fill=sfill, stroke=sstroke, sw=1)
            dx = inner_x + 8
            bh = h - 5
            for name, model, typ, frac in it["devices"]:
                bw = (inner_w - 16) * frac
                fill, stroke = TYPES[typ]
                c.rect(dx, y + 1, bw, bh, fill=fill, stroke=stroke, sw=1.5, rx=3)
                draw_label(c, dx + 10, y + 1 + bh / 2, name, model, bw + 4)
                dx += bw + 8
        else:  # spare
            c.rect(inner_x + 3, y + 3, inner_w - 6, h - 6, fill=None, stroke="#b5b5b5",
                   sw=1.2, rx=3, dash=(8, 6))
            c.text(inner_x + inner_w / 2, y + h / 2 + 6, f"Spare {it['units']}U",
                   16, False, "middle", fill=MUTED)
        y += h
    if used != units:
        WARNINGS.append(f"rack '{rack['title']}' uses {used}U of {units}U")
    return x_rack, frame_top, frame_bot


def draw_legend(c, x, y, w):
    c.rect(x, y, w, 56 + 40 * len(LEGEND), fill="#ffffff", stroke="#8a8a8a", sw=1.2, rx=4)
    c.text(x + 16, y + 32, "Legend (colour by equipment type)", 18, True)
    yy = y + 56
    for typ, label in LEGEND:
        fill, stroke = TYPES[typ]
        c.rect(x + 16, yy + 6, 34, 22, fill=fill, stroke=stroke, sw=1.5, rx=3)
        c.text(x + 62, yy + 23, label, 16)
        if c.measure(label, 16) > w - 78:
            WARNINGS.append(f"legend overflow: '{label}'")
        yy += 40


def main():
    c = Canvas()
    title = "HelpYou Mortgage proposed rack layout"
    c.text(W / 2, 54, title, 36, True, "middle")
    c.text(W / 2, 86, "Front elevations of the proposed racks and cabinet, drawn to a common "
           "rack-unit scale; each device is labelled with its name and model.",
           18, False, "middle", fill=MUTED)

    frames = [draw_rack(c, i, r) for i, r in enumerate(RACKS)]

    # Site bracket over the four Brisbane racks
    x_left = frames[0][0]
    x_right = frames[3][0] + RACK_W
    yb = FRAME_TOP - 62
    c.text((x_left + x_right) / 2, yb - 10, "Brisbane head office", 20, True, "middle")
    c.line(x_left, yb, x_right, yb, RACK_STROKE, 1.5)
    c.line(x_left, yb, x_left, yb + 8, RACK_STROKE, 1.5)
    c.line(x_right, yb, x_right, yb + 8, RACK_STROKE, 1.5)

    # Legend in the space above the 12U Cairns cabinet
    x_c = frames[4][0]
    draw_legend(c, x_c - TICK_W + 4, FRAME_TOP - 44, RACK_W + TICK_W - 4)

    # Notes under the floor line
    ny = BASE_Y + RAIL_W + 44
    for line in NOTES:
        c.text(MARGIN_X + TICK_W, ny, line, 16)
        if c.measure(line, 16) > W - 2 * MARGIN_X - TICK_W:
            WARNINGS.append(f"note overflow: '{line[:40]}...'")
        ny += 26

    c.save(title)
    for wmsg in WARNINGS:
        print("WARNING:", wmsg)
    print("wrote", SVG_PATH, "and", PNG_PATH, c.img.size)


if __name__ == "__main__":
    main()
