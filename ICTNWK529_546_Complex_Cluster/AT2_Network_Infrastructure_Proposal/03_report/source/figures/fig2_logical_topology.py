#!/usr/bin/env python3
"""Figure 2 for the HelpYou Mortgage report: proposed logical topology.

Writes fig2_logical_topology.svg (hand-laid-out SVG markup, 2400 x 1500
viewBox, presentation attributes only so any renderer handles it) and
rasterises it to fig2_logical_topology.png with cairosvg at 150 dpi
(ImageMagick in this environment has no SVG delegate).

Every label is measured with the real Liberation Sans font files so that no
text runs past its box; the script prints a warning for anything that would.
Content follows the draft report sections 2, 5, 6.1-6.3 and 6.10 with the
corrections file applied (ISP -> FW-HQ -> transit VLAN 900 -> core stack,
two core links, 1 GbE transit per core, hosts dual-homed plus a 1 GbE DMZ
link each, NAS on the isolated VLAN 130, Cairns over a site-to-site VPN).
"""
import os
from xml.sax.saxutils import escape

from PIL import ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SVG_PATH = os.path.join(OUT_DIR, "fig2_logical_topology.svg")
PNG_PATH = os.path.join(OUT_DIR, "fig2_logical_topology.png")

W, H = 2400, 1500
FAMILY = "Liberation Sans, DejaVu Sans, Arial, Helvetica, sans-serif"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# ---------------------------------------------------------------- palette --
INK = "#1e1e1e"
MUTED = "#555555"
FW_FILL, FW_STROKE = "#f9d9d6", "#b03a2e"        # firewall: red
SW_FILL, SW_STROKE = "#d7e6f6", "#2c5f8f"        # switches: blue
SRV_FILL, SRV_STROKE = "#dcefd6", "#3a7d3a"      # servers / hosts / NAS: green
SRV_PANEL = "#eef7ea"
AP_FILL, AP_STROKE = "#ffe2bf", "#d9731a"        # Wi-Fi: orange
DMZ_FILL, DMZ_STROKE = "#fff6c4", "#c8a200"      # DMZ zone: yellow
VPN = "#7d3c98"                                  # VPN: dashed purple
ISP_FILL, ISP_STROKE = "#ececec", "#6f6f6f"
END_FILL, END_STROKE = "#f0f0f0", "#5a5a5a"
SITE_FILL, SITE_STROKE = "#fbfbfb", "#9a9a9a"
ZONE_STROKE = "#a0a0a0"
L10 = "#2f3e4e"      # 10 Gbps links
L1 = "#6a6a6a"       # 1 GbE links
WAN = "#7a7a7a"

_fonts = {}


def measure(text, size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_B if bold else FONT_R, size)
    return _fonts[key].getlength(text)


WARNINGS = []
out = []


def emit(s):
    out.append(s)


def text(x, y, s, size=16, bold=False, anchor="middle", fill=INK, maxw=None, extra=""):
    """Emit a text element; warn if wider than maxw."""
    if maxw is not None:
        w = measure(s, size, bold)
        if w > maxw:
            WARNINGS.append(f"text too wide ({w:.0f} > {maxw}): {s!r} @ {size}px")
    weight = ' font-weight="bold"' if bold else ""
    emit(f'  <text x="{x:.0f}" y="{y:.0f}" font-size="{size}"{weight} '
         f'text-anchor="{anchor}" fill="{fill}"{extra}>{escape(s)}</text>')


def rect(x, y, w, h, fill, stroke, sw=2, rx=8, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'  <rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{extra}/>')


def line(x1, y1, x2, y2, stroke=L1, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    emit(f'  <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
         f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>')


def polyline(pts, stroke=L1, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    emit(f'  <polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
         f'stroke-linejoin="round" stroke-linecap="round"{d}/>')


def box(x, y, w, h, fill, stroke, lines, sw=2.5, rx=10, pad_top=None, pitch=None):
    """Rounded box with centred text lines: [(text, size, bold), ...]."""
    rect(x, y, w, h, fill, stroke, sw, rx)
    n = len(lines)
    if pitch is None:
        pitch = 23
    total = sum(l[1] for l in lines) + (n - 1) * (pitch - 16)
    # first baseline: vertically centre the block
    y0 = y + (h - total) / 2 + lines[0][1] * 0.78
    cx = x + w / 2
    yy = y0
    for i, (s, size, bold) in enumerate(lines):
        text(cx, yy, s, size, bold, "middle", INK, maxw=w - 14)
        if i + 1 < n:
            yy += (size + lines[i + 1][1]) / 2 + (pitch - 16)


def cloud(cx, cy, w, h, lines, n=9):
    """ISP cloud: one closed path of outward arcs around an ellipse (no inner strokes)."""
    import math
    rx, ry = w / 2 - 16, h / 2 - 12
    pts = [(cx + rx * math.cos(2 * math.pi * i / n - math.pi / 2),
            cy + ry * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        r = math.hypot(x2 - x1, y2 - y1) * 0.56
        d += f" A {r:.1f} {r:.1f} 0 0 1 {x2:.1f} {y2:.1f}"
    d += " Z"
    emit(f'  <path d="{d}" fill="{ISP_FILL}" stroke="{ISP_STROKE}" stroke-width="2.5" '
         f'stroke-linejoin="round"/>')
    m = len(lines)
    pitch = 21
    y0 = cy - (m - 1) * pitch / 2 + 6
    for i, (s, size, bold) in enumerate(lines):
        text(cx, y0 + i * pitch, s, size, bold, maxw=w * 0.8)


# ------------------------------------------------------------------ icons --
def icon_pc(cx, cy):
    rect(cx - 24, cy - 20, 48, 32, END_FILL, END_STROKE, 2, 4)
    rect(cx - 18, cy - 15, 36, 22, "#ffffff", END_STROKE, 1.5, 2)
    line(cx, cy + 12, cx, cy + 20, END_STROKE, 2.5)
    line(cx - 14, cy + 21, cx + 14, cy + 21, END_STROKE, 2.5)


def icon_phone(cx, cy):
    rect(cx - 26, cy - 14, 52, 34, END_FILL, END_STROKE, 2, 5)
    rect(cx - 18, cy - 8, 20, 12, "#ffffff", END_STROKE, 1.5, 2)
    emit(f'  <rect x="{cx - 30:.0f}" y="{cy - 22:.0f}" width="22" height="10" rx="5" '
         f'fill="{END_STROKE}"/>')
    for dx in (6, 13, 20):
        for dy in (0, 7):
            emit(f'  <rect x="{cx + dx:.0f}" y="{cy - 8 + dy:.0f}" width="5" height="5" '
                 f'fill="{END_STROKE}"/>')


def icon_ap(cx, cy):
    emit(f'  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="21" fill="{AP_FILL}" '
         f'stroke="{AP_STROKE}" stroke-width="2.5"/>')
    emit(f'  <circle cx="{cx:.0f}" cy="{cy + 4:.0f}" r="3.5" fill="{AP_STROKE}"/>')
    for r in (9, 15):
        emit(f'  <path d="M {cx - r:.0f} {cy + 4 - 0:.0f} A {r} {r} 0 0 1 {cx + r:.0f} {cy + 4:.0f}" '
             f'fill="none" stroke="{AP_STROKE}" stroke-width="2.5"/>')


def icon_appliance(cx, cy, label):
    rect(cx - 30, cy - 16, 60, 32, END_FILL, END_STROKE, 2, 4)
    for i in range(3):
        emit(f'  <circle cx="{cx - 18 + i * 9:.0f}" cy="{cy + 8:.0f}" r="2.5" fill="{END_STROKE}"/>')
    text(cx, cy - 2, label, 13, True, maxw=56)


def caption(cx, y, lines, size=16, maxw=112):
    for i, s in enumerate(lines):
        text(cx, y + i * 19, s, size, i == 0, maxw=maxw)


# ================================================================= drawing ==
emit(f'<?xml version="1.0" encoding="UTF-8"?>')
emit(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
     f'font-family="{FAMILY}">')
emit(f'  <title>HelpYou Mortgage proposed logical topology</title>')
emit(f'  <rect width="{W}" height="{H}" fill="#ffffff"/>')

# ---- title ---------------------------------------------------------------
emit('  <!-- title -->')
text(W / 2, 54, "HelpYou Mortgage proposed logical topology", 34, True)
text(W / 2, 86, "Brisbane head office (two floors) and Cairns branch. VLAN IDs and subnets "
     "follow section 5; link speeds are the design targets from section 6.", 17, fill=MUTED)

# ---- site boundaries -----------------------------------------------------
BX, BY, BW, BH = 20, 108, 1780, 1255        # Brisbane
CX, CY, CW, CH = 1830, 108, 550, 1255       # Cairns
emit('  <!-- site boundaries -->')
rect(BX, BY, BW, BH, SITE_FILL, SITE_STROKE, 2, 14)
rect(CX, CY, CW, CH, SITE_FILL, SITE_STROKE, 2, 14)
text(BX + 20, BY + 32, "Brisbane head office", 20, True, "start")
text(CX + 20, CY + 32, "Cairns branch", 20, True, "start")

# ---- Brisbane internet edge ---------------------------------------------
emit('  <!-- Brisbane ISP and FW-HQ -->')
cloud(900, 175, 370, 96, [("Brisbane ISP", 18, True),
                           ("business nbn 1000/400 Mbps", 16, False),
                           ("single service, static IP", 16, False)])
line(900, 222, 900, 265, WAN, 2.5)
text(915, 258, "nbn handoff", 15, False, "start", MUTED)

FWX, FWY, FWW, FWH = 700, 265, 400, 120
box(FWX, FWY, FWW, FWH, FW_FILL, FW_STROKE, [
    ("FW-HQ   FortiGate 70G", 18, True),
    ("IPS/IDS, UTP inspection, VPN termination", 16, False),
    ("Gateways: guest VLAN 90, DMZ VLAN 100", 16, False),
    ("mgmt 192.168.120.4", 16, False)])

# ---- DMZ zone --------------------------------------------------------------
emit('  <!-- DMZ zone (hangs off FW-HQ) -->')
DZX, DZY, DZW, DZH = 62, 258, 518, 146
rect(DZX, DZY, DZW, DZH, DMZ_FILL, DMZ_STROKE, 2.5, 12)
text(DZX + 10, DZY + 22, "DMZ zone   VLAN 100   192.168.100.0/27   (gateway .1 on FW-HQ)",
     16, True, "start", maxw=DZW - 20)
box(76, 294, 220, 100, SRV_FILL, SRV_STROKE, [
    ("SMTP-GW", 17, True),
    ("mail relay / filter", 16, False),
    ("192.168.100.10/27", 16, False),
    ("VM on HYP-01, DMZ NIC", 16, False)], pitch=21)
box(336, 294, 232, 100, SW_FILL, SW_STROKE, [
    ("DMZ switch", 17, True),
    ("Cisco C1300-24T-4X", 16, False),
    ("24 x 1 GbE ports", 16, False),
    ("mgmt 192.168.120.47", 16, False)], pitch=21)
line(296, 344, 336, 344, L1, 2)                       # SMTP-GW <-> DMZ switch
line(568, 325, FWX, 325, L1, 2)                       # DMZ switch -> FW-HQ
text(634, 316, "1 GbE", 15, False, "middle", MUTED)
text(634, 343, "VLAN 100", 15, False, "middle", MUTED)

# ---- transit to the core stack ----------------------------------------------
emit('  <!-- VLAN 900 transit: one 1 GbE link to each core -->')
line(860, FWY + FWH, 800, 470, L1, 2.5)
line(940, FWY + FWH, 1000, 470, L1, 2.5)
text(1015, 416, "VLAN 900 transit   192.168.254.0/29", 16, True, "start")
text(1015, 441, "1 GbE to each core; FW-HQ .1, core stack .2", 16, False, "start")
text(785, 416, "1 GbE", 15, False, "end", MUTED)

# ---- core stack ----------------------------------------------------------------
emit('  <!-- core stack: CORE 1 + CORE 2 with two 10 Gbps stack links -->')
C1X, C2X, CY0, CWD, CHT = 590, 970, 470, 240, 90
box(C1X, CY0, CWD, CHT, SW_FILL, SW_STROKE, [
    ("CORE 1", 18, True), ("Cisco C1300-12XS", 16, False), ("12 x 10 Gbps SFP+", 16, False)])
box(C2X, CY0, CWD, CHT, SW_FILL, SW_STROKE, [
    ("CORE 2", 18, True), ("Cisco C1300-12XS", 16, False), ("12 x 10 Gbps SFP+", 16, False)])
line(C1X + CWD, 500, C2X, 500, L10, 4)
line(C1X + CWD, 535, C2X, 535, L10, 4)
text(900, 490, "2 x 10 Gbps", 16, True, "middle", maxw=136)
text(900, 557, "stack links", 16, False, "middle", maxw=136)
text(1235, 492, "Core stack = one logical switch (front-panel stack)", 16, True, "start",
     maxw=540)
text(1235, 517, "VLAN gateways (.1 of each subnet) on the stack; mgmt SVI 192.168.120.1",
     15, False, "start", maxw=540)
text(1235, 541, "Default route to FW-HQ via 192.168.254.1", 16, False, "start", maxw=540)

# ---- fan row: hosts, NAS and six access switches, all dual-homed -----------
emit('  <!-- downstream devices: each has one 10 Gbps link to each core -->')
ROW_Y, ROW_H = 730, 85
HOST_W, NAS_W, ASW_W, GAP, FLOOR_GAP = 290, 170, 138, 14, 30
x = 62
cols = {}
cols["HYP-01"] = x; x += HOST_W + GAP
cols["HYP-02"] = x; x += HOST_W + GAP
cols["NAS"] = x; x += NAS_W + GAP
for i in range(1, 7):
    cols[f"ASW-{i}"] = x
    x += ASW_W + (FLOOR_GAP if i == 3 else GAP)
widths = {"HYP-01": HOST_W, "HYP-02": HOST_W, "NAS": NAS_W}
widths.update({f"ASW-{i}": ASW_W for i in range(1, 7)})
order = ["HYP-01", "HYP-02", "NAS"] + [f"ASW-{i}" for i in range(1, 7)]
centres = {k: cols[k] + widths[k] / 2 for k in order}

# fan lines first so boxes sit on top of them
n = len(order)
for i, k in enumerate(order):
    cx = centres[k]
    a1 = C1X + 16 + i * (CWD - 32) / (n - 1)
    a2 = C2X + 16 + i * (CWD - 32) / (n - 1)
    line(cx - 14, ROW_Y, a1, CY0 + CHT, L10, 3.5)
    line(cx + 14, ROW_Y, a2, CY0 + CHT, L10, 3.5)

text(62, ROW_Y - 16, "10 Gbps each", 15, False, "start", MUTED)
text(cols["ASW-6"] + ASW_W, ROW_Y - 16, "10 Gbps each", 15, False, "end", MUTED)

PANEL_Y, PANEL_H = ROW_Y + ROW_H, 215

# hosts
for name, floor, mg, rp, vms in [
    ("HYP-01", "Floor 1 server space", ".120.11", ".130.11", [
        "DC1 / DNS / DHCP   .110.10",
        "SRV-WEB (intranet)   .110.20",
        "SRV-HRDB   .110.21",
        "SMTP-GW   .100.10 (DMZ NIC)",
        "SRV-LOG (Wazuh)   .120.21",
        "+ replicas of HYP-02 VMs"]),
    ("HYP-02", "Floor 2 equipment rack", ".120.12", ".130.12", [
        "DC2 / DNS / DHCP   .110.11",
        "SRV-MKT-FS   .110.22",
        "SRV-CS-FS   .110.23",
        "SRV-MAIL   .110.24",
        "SRV-MON Zabbix/SNMPv3   .120.20",
        "WLAN-CTRL   .120.22",
        "+ replicas of HYP-01 VMs"]),
]:
    hx = cols[name]
    rect(hx, PANEL_Y - 10, HOST_W, PANEL_H + 10, SRV_PANEL, SRV_STROKE, 2, 10)
    box(hx, ROW_Y, HOST_W, ROW_H, SRV_FILL, SRV_STROKE, [
        (f"{name}   Dell PowerEdge R360", 18, True),
        (floor, 16, False),
        ("2 x 10 Gbps to cores + 1 GbE to DMZ", 16, False)], pitch=21)
    yy = PANEL_Y + 22
    text(hx + 12, yy, "Virtual machines (Hyper-V):", 16, True, "start", maxw=HOST_W - 20)
    for v in vms:
        yy += 21
        text(hx + 12, yy, v, 16, False, "start", maxw=HOST_W - 20)
    yy += 24
    text(hx + 12, yy, f"mgmt {mg}   replication {rp}", 16, False, "start", MUTED,
         maxw=HOST_W - 20)

# NAS
nx = cols["NAS"]
rect(nx, PANEL_Y - 10, NAS_W, PANEL_H + 10, SRV_PANEL, SRV_STROKE, 2, 10)
box(nx, ROW_Y, NAS_W, ROW_H, SRV_FILL, SRV_STROKE, [
    ("NAS-BACKUP", 17, True), ("Synology RS2423RP+", 15, False),
    ("2 x 10 Gbps to cores", 15, False)], pitch=21)
for i, s in enumerate(["VLAN 130 backup", "192.168.130.20/27", "no gateway", "(non-routed)",
                       "mgmt .120.30", "daily versioned", "backups, off-site", "rotation"]):
    text(nx + NAS_W / 2, PANEL_Y + 22 + i * 21, s, 16, i == 0, maxw=NAS_W - 16)

# access switches
for i in range(1, 7):
    k = f"ASW-{i}"
    box(cols[k], ROW_Y, ASW_W, ROW_H, SW_FILL, SW_STROKE, [
        (k, 18, True), ("C1300-48P-4X", 16, False), ("2 x 10G uplinks", 16, False)], pitch=21)

# server VLAN note under the hosts
emit('  <!-- server VLAN note and design notes -->')
NY = PANEL_Y + PANEL_H + 46
text(62, NY, "Server VLANs (gateways .1 on the core stack):", 16, True, "start")
text(62, NY + 24, "110 services: 192.168.110.0/26", 16, False, "start")
text(62, NY + 46, "120 management: 192.168.120.0/26", 16, False, "start")
text(62, NY + 68, "130 replication / backup: 192.168.130.0/27 (no gateway, non-routed)", 15,
     False, "start")
text(62, NY + 108, "Design notes", 16, True, "start")
notes = [
    "Each core uses all 12 ports: 6 access uplinks, 2 host links, 1 NAS link,",
    "2 stack links and 1 firewall transit link.",
    "Hyper-V Replica copies VMs between the hosts every 15 minutes; the NAS is",
    "the backup target only. Both hosts carry a 1 GbE port to the DMZ switch.",
    "Remote-access VPN with MFA also terminates on FW-HQ.",
]
for i, s in enumerate(notes):
    text(62, NY + 132 + i * 22, s, 16, False, "start", maxw=760)

# host DMZ links (1 GbE each) routed along the left margin to the DMZ switch
emit('  <!-- 1 GbE host links to the DMZ switch -->')
polyline([(cols["HYP-01"], 772), (36, 772), (36, 424), (430, 424), (430, 394)], L1, 2)
polyline([(cols["HYP-02"] + 60, PANEL_Y + PANEL_H), (cols["HYP-02"] + 60, PANEL_Y + PANEL_H + 14),
          (48, PANEL_Y + PANEL_H + 14), (48, 442), (470, 442), (470, 394)], L1, 2)
text(70, 414, "1 GbE from each host (SMTP-GW virtual switch)", 15, False, "start", MUTED,
     maxw=350)

# ---- floor zones ------------------------------------------------------------
emit('  <!-- floor zones: endpoints and the VLANs served -->')
ZY, ZH = ROW_Y + ROW_H + 25, 500
floors = [
    ("Floor 1", ["ASW-1", "ASW-2", "ASW-3"], True, [
        ("IT", "VLAN 70", "192.168.70.0/26"),
        ("Customer Service", "VLAN 40", "192.168.40.0/25"),
        ("Managers", "VLAN 20", "192.168.20.0/26"),
        ("Marketing", "VLAN 30", "192.168.30.0/25"),
        ("Voice", "VLAN 80", "192.168.80.0/25"),
        ("Staff Wi-Fi", "VLAN 140", "192.168.140.0/24"),
        ("Guest Wi-Fi", "VLAN 90", "192.168.90.0/24 *")]),
    ("Floor 2", ["ASW-4", "ASW-5", "ASW-6"], False, [
        ("Executives", "VLAN 10", "192.168.10.0/26"),
        ("Admin", "VLAN 50", "192.168.50.0/26"),
        ("HR", "VLAN 60", "192.168.60.0/27"),
        ("Managers", "VLAN 20", "192.168.20.0/26"),
        ("Marketing", "VLAN 30", "192.168.30.0/25"),
        ("Voice", "VLAN 80", "192.168.80.0/25"),
        ("Staff Wi-Fi", "VLAN 140", "192.168.140.0/24"),
        ("Guest Wi-Fi", "VLAN 90", "192.168.90.0/24 *")]),
]
for fname, sws, has_pbx, vlans in floors:
    zx = cols[sws[0]] - 10
    zw = cols[sws[-1]] + ASW_W + 10 - zx
    rect(zx, ZY, zw, ZH, "#ffffff", ZONE_STROKE, 2, 10, dash="10 6")
    bus_y = ZY + 22
    for s in sws:
        line(centres[s], ROW_Y + ROW_H, centres[s], bus_y, L1, 2)
    # endpoint icons
    items = [("pc", ["PCs on desks", "1 Gbps"]),
             ("phone", ["IP phones", "PoE, VLAN 80"]),
             ("ap", ["3 EAP650 APs", "PoE", "VLANs 140 / 90"])]
    if has_pbx:
        items.append(("pbx", ["PBX-01", "UCM6302, PoE", "VLAN 80 .80.10"]))
    slot = zw / len(items)
    ixs = [zx + slot * (i + 0.5) for i in range(len(items))]
    line(min(ixs[0], centres[sws[0]]), bus_y, max(ixs[-1], centres[sws[-1]]), bus_y, L1, 2)
    icon_y = bus_y + 52
    for (kind, cap), ix in zip(items, ixs):
        line(ix, bus_y, ix, icon_y - 24, L1, 2)
        if kind == "pc":
            icon_pc(ix, icon_y)
        elif kind == "phone":
            icon_phone(ix, icon_y)
        elif kind == "ap":
            icon_ap(ix, icon_y)
        else:
            icon_appliance(ix, icon_y, "PBX")
        caption(ix, icon_y + 44, cap, 15, maxw=slot - 6)
    # VLAN list
    ly = icon_y + 122
    text(zx + 14, ly, f"{fname}: {sws[0]} to {sws[-1]}, 144 x 1 Gbps PoE+ ports",
         16, True, "start", maxw=zw - 24)
    text(zx + 14, ly + 23, "VLANs served (gateways .1 on the core stack unless noted):",
         15, False, "start", maxw=zw - 24)
    dept_w = max(measure(d, 16, True) for d, _, _ in vlans) + 16
    vid_w = max(measure(v, 16) for _, v, _ in vlans) + 16
    for i, (dept, vid, net) in enumerate(vlans):
        yy = ly + 50 + i * 23
        text(zx + 22, yy, dept, 16, True, "start")
        text(zx + 22 + dept_w, yy, vid, 16, False, "start")
        text(zx + 22 + dept_w + vid_w, yy, net, 16, False, "start",
             maxw=zw - 22 - dept_w - vid_w - 8)
    yy = ly + 50 + len(vlans) * 23 + 6
    text(zx + 14, yy, "* guest gateway on FW-HQ; guests are internet-only.", 15,
         False, "start", MUTED, maxw=zw - 24)
    text(zx + 14, yy + 21, "35 desks: PC on a 1 Gbps port, phone on its own PoE port.", 15,
         False, "start", MUTED, maxw=zw - 24)
    text(zx + 14, yy + 42, "Access ports 1 Gbps; uplinks 2 x 10 Gbps per switch.", 15,
         False, "start", MUTED, maxw=zw - 24)

# ---- site-to-site VPN -------------------------------------------------------
emit('  <!-- site-to-site VPN between the two firewalls -->')
FBX, FBY, FBW, FBH = 1950, 265, 310, 120
line(FWX + FWW, 325, FBX, 325, VPN, 3.5, dash="16 10")
text((FWX + FWW + FBX) / 2, 308, "Site-to-site IPsec VPN", 17, True, "middle", VPN)
text((FWX + FWW + FBX) / 2, 350, "FW-HQ to FW-BR over both ISP services; only permitted "
     "branch-to-server flows", 16, False, "middle", MUTED)

# ---- Cairns ------------------------------------------------------------------
emit('  <!-- Cairns branch -->')
CCX = CX + CW / 2
cloud(CCX, 175, 300, 96, [("Cairns ISP", 18, True), ("business nbn service", 16, False),
                           ("single service", 16, False)])
line(CCX, 222, CCX, 265, WAN, 2.5)
box(FBX, FBY, FBW, FBH, FW_FILL, FW_STROKE, [
    ("FW-BR   FortiGate 70G", 18, True),
    ("UTP, IPS/IDS", 16, False),
    ("site-to-site VPN termination", 16, False),
    ("gateways for VLANs 210 / 220 / 280", 16, False)])
line(CCX, FBY + FBH, CCX, 470, L1, 2.5)
text(CCX + 12, 420, "1 GbE trunk", 16, False, "start", MUTED)
text(CCX + 12, 441, "VLANs 210 / 220 / 280", 16, False, "start", MUTED)
box(FBX, 470, FBW, 90, SW_FILL, SW_STROKE, [
    ("Cairns switch", 18, True), ("Cisco C1300-24P-4X", 16, False),
    ("24 x 1 Gbps PoE+; mgmt 10.20.20.2", 16, False)])
c_items = [("pc", ["8 x PC", "1 Gbps"]), ("phone", ["8 x IP phone", "PoE, VLAN 280"]),
           ("ap", ["1 x EAP650 AP", "PoE, 10.20.20.3"])]
c_slot = CW / 3
c_ix = [CX + c_slot * (i + 0.5) for i in range(3)]
c_icon_y = 700
for (kind, cap), ix in zip(c_items, c_ix):
    line(CCX, 560, ix, c_icon_y - 26, L1, 2)
    {"pc": icon_pc, "phone": icon_phone, "ap": icon_ap}[kind](ix, c_icon_y)
    caption(ix, c_icon_y + 44, cap, 16, maxw=c_slot - 10)
ly = 830
text(CX + 20, ly, "Cairns VLANs (gateways .1 on FW-BR):", 16, True, "start", maxw=CW - 40)
for i, (dept, vid, net) in enumerate([("Staff", "VLAN 210", "10.20.10.0/26"),
                                      ("Management", "VLAN 220", "10.20.20.0/27"),
                                      ("Voice", "VLAN 280", "10.20.80.0/27")]):
    yy = ly + 30 + i * 24
    text(CX + 28, yy, dept, 16, True, "start")
    text(CX + 150, yy, vid, 16, False, "start")
    text(CX + 240, yy, net, 16, False, "start")
cn = ["8 staff; one access switch, one AP and",
      "one MeetUp 2 video bar.",
      "Branch traffic reaches HelpYou servers",
      "only through the VPN policy on FW-HQ.",
      "Single ISP service and single firewall",
      "per site are accepted residual risks."]
for i, s in enumerate(cn):
    text(CX + 20, ly + 130 + i * 22, s, 16, False, "start", MUTED, maxw=CW - 40)

# ---- legend ---------------------------------------------------------------------
emit('  <!-- legend -->')
LY = 1388
rect(20, LY, 2360, 96, "#ffffff", "#bbbbbb", 2, 10)
text(40, LY + 36, "Legend", 18, True, "start")
lx = 150
items = [
    ("box", FW_FILL, FW_STROKE, "Firewall (FortiGate 70G)"),
    ("box", SW_FILL, SW_STROKE, "Switch (Cisco Catalyst 1300)"),
    ("box", SRV_FILL, SRV_STROKE, "Server host / VM / NAS"),
    ("ap", AP_FILL, AP_STROKE, "Wireless access point"),
    ("box", DMZ_FILL, DMZ_STROKE, "DMZ zone"),
    ("box", ISP_FILL, ISP_STROKE, "ISP / endpoint"),
    ("l10", None, None, "10 Gbps link"),
    ("l1", None, None, "1 Gbps / 1 GbE link"),
    ("vpn", None, None, "Site-to-site VPN"),
    ("zone", None, None, "Floor / site boundary"),
]
ly1 = LY + 30
for kind, f, s, label in items:
    if kind == "box":
        rect(lx, ly1, 34, 26, f, s, 2, 5)
    elif kind == "ap":
        emit(f'  <circle cx="{lx + 17}" cy="{ly1 + 13}" r="13" fill="{f}" stroke="{s}" stroke-width="2.5"/>')
    elif kind == "l10":
        line(lx, ly1 + 13, lx + 34, ly1 + 13, L10, 4)
    elif kind == "l1":
        line(lx, ly1 + 13, lx + 34, ly1 + 13, L1, 2)
    elif kind == "vpn":
        line(lx, ly1 + 13, lx + 34, ly1 + 13, VPN, 3.5, dash="10 6")
    elif kind == "zone":
        rect(lx, ly1, 34, 26, "#ffffff", ZONE_STROKE, 2, 5, dash="6 4")
    text(lx + 44, ly1 + 19, label, 16, False, "start")
    lx += 44 + measure(label, 16) + 36
text(40, LY + 78, "Every access switch, host and the NAS has one 10 Gbps link to CORE 1 and one to "
     "CORE 2. Addresses written .x.y are inside 192.168.x.0 (Brisbane).", 16, False, "start", MUTED)

emit('</svg>')

with open(SVG_PATH, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print("wrote", SVG_PATH, f"({len(out)} elements)")
for w in WARNINGS:
    print("WARNING:", w)

import cairosvg  # noqa: E402

cairosvg.svg2png(url=SVG_PATH, write_to=PNG_PATH, scale=150 / 96, background_color="white")
print("wrote", PNG_PATH)
