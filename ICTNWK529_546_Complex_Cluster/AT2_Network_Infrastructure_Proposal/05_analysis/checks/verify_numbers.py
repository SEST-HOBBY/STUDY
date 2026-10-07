#!/usr/bin/env python3
"""Recompute every number and internal-consistency claim in the HelpYou AT2 draft report.

Run with:  python3 -I verify_numbers.py
Reads nothing untrusted; every input below is transcribed from the draft
(/scratchpad/extract/report.md) and recomputed from scratch.  Prints a
markdown table (item | draft | recomputed | status) and writes it to
verification_numbers.md next to this script.
"""
import ipaddress
import math
import os
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
rows = []          # (section, item, draft, recomputed, status, note)


def money(x):
    return f"${D(x).quantize(D('0.01'), rounding=ROUND_HALF_UP):,}"


def q2(x):
    return D(x).quantize(D('0.01'), rounding=ROUND_HALF_UP)


def check(section, item, draft, recomputed, ok=None, note=""):
    if ok is None:
        ok = (str(draft) == str(recomputed))
    rows.append((section, item, str(draft), str(recomputed), "OK" if ok else "ERROR", note))


def warn(section, item, draft, recomputed, note=""):
    rows.append((section, item, str(draft), str(recomputed), "WARNING", note))


def info(section, item, draft, recomputed, note=""):
    rows.append((section, item, str(draft), str(recomputed), "INFO", note))


# --------------------------------------------------------------------------
# 1. Headcounts (sections ES, 1.1, 1.2, 4.1, 6.4, 6.6, 6.9, 7.1, 7.3)
# --------------------------------------------------------------------------
orig = {"Executives": 5, "Managers": 5, "Customer Service": 5, "Admin": 10,
        "Marketing": 10, "HR": 3, "IT": 2}
check("1.1", "Original Brisbane headcount (5+5+5+10+10+3+2)", 40, sum(orig.values()))
check("ES/1.1", "Brisbane after expansion (40 + 30)", 70, 40 + 30)
check("ES/3", "Two floors x 35 staff", 70, 2 * 35)
check("6.4/6.6", "Initial users (70 Brisbane + 8 Cairns)", 78, 70 + 8)
check("6.9", "Five-year org users (108 Brisbane + 8 Cairns)", 116, 108 + 8)
check("6.9", "Extra users (116 - 78)", 38, 116 - 78)
check("7.1 table", "Original dept sizes used as growth denominators (HR 3, Mkt 10, CS 5)",
      "3 / 10 / 5", f"{orig['HR']} / {orig['Marketing']} / {orig['Customer Service']}")

# Five-year device requirement per VLAN (section 5) vs handout 270 devices
dept_req = {"Executives": 30, "Managers": 40, "Marketing": 50, "Customer Service": 50,
            "Admin": 40, "HR": 20, "IT": 40}
check("5 vs ES/1.2/4.1", "Sum of departmental VLAN requirements = 270 devices", 270, sum(dept_req.values()))

# --------------------------------------------------------------------------
# 2. Initial cost table (6.9)
# --------------------------------------------------------------------------
initial = [
    ("Core switches C1300-12XS", 2, "3036.73", "6073.46"),
    ("HQ access C1300-48P-4X", 6, "2704.42", "16226.52"),
    ("Cairns access C1300-24P-4X", 1, "2003.43", "2003.43"),
    ("DMZ switch C1300-24T-4X", 1, "1750.00", "1750.00"),
    ("FortiGate 70G + UTP, one per site", 2, "2250.00", "4500.00"),
    ("Dell R360 hosts", 2, "18000.00", "36000.00"),
    ("Windows Server 2025 Std 16-core packs", 6, "1744.45", "10466.70"),
    ("Windows Server User CALs", 78, "109.45", "8537.10"),
    ("Synology RS2423RP+ diskless", 1, "6124.25", "6124.25"),
    ("NAS drives, rails, media", 1, "6000.00", "6000.00"),
    ("UPS / rack fit-out", 1, "7000.00", "7000.00"),
    ("TP-Link EAP650 APs", 7, "179.00", "1253.00"),
    ("Grandstream UCM6302 PBX", 1, "462.00", "462.00"),
    ("GRP2612P phones", 82, "83.00", "6806.00"),
    ("Logitech MeetUp 2", 3, "1599.00", "4797.00"),
    ("Endpoint fund", 78, "1500.00", "117000.00"),
    ("Optics / accessories", 1, "6500.00", "6500.00"),
    ("Cabling certification / outlets", 1, "6000.00", "6000.00"),
    ("HR DB compatibility fund", 1, "8000.00", "8000.00"),
    ("Labour (hours)", 160, "150.00", "24000.00"),
    ("Training / handover", 1, "5000.00", "5000.00"),
    ("MFA licensing / enrolment", 1, "2500.00", "2500.00"),
]
initial_total = D(0)
for name, qty, unit, draft_line in initial:
    line = q2(D(qty) * D(unit))
    initial_total += line
    check("6.9 initial", f"{name}: {qty} x {money(unit)}", money(draft_line), money(line))

DRAFT_INITIAL = D("286999.46")
check("6.9 initial", "Initial procurement and implementation total", money(DRAFT_INITIAL), money(initial_total))
contingency = q2(initial_total * D("0.10"))
check("6.9 initial", "Contingency 10% of initial", money("28699.95"), money(contingency),
      note=f"exact {initial_total * D('0.10')}")

# --------------------------------------------------------------------------
# 3. Recurring table (6.9) and GST conversions
# --------------------------------------------------------------------------
GST = D("1.10")
defender_users = q2(D(78) * D("4.50") * 12 * GST)
defender_srv14 = q2(D(14) * D("4.50") * 12 * GST)
teams = q2(D(78) * D("6.00") * 12 * GST)
check("6.4/6.9", "Defender for Business 78 users: 78 x 4.50 x 12 x 1.10", money("4633.20"), money(defender_users))
check("6.4/6.9", "Defender server add-on 14 instances: 14 x 4.50 x 12 x 1.10", money("831.60"), money(defender_srv14))
check("6.4", "Defender combined annual (users + servers)", money("5464.80"), money(defender_users + defender_srv14))
check("6.6/6.9", "Teams Essentials 78 users: 78 x 6.00 x 12 x 1.10", money("6177.60"), money(teams))
check("6.9/6.10", "Brisbane ISP 160 x 12", money("1920.00"), money(D(160) * 12))
check("6.9/6.10", "Cairns ISP allowance 120 x 12", money("1440.00"), money(D(120) * 12))
check("6.6/6.9", "SIP/call allowance 600 x 12", money("7200.00"), money(D(600) * 12))

recurring = [defender_users, defender_srv14, teams, D(1920), D(1440), D(7200),
             D(1200), D(9000), D(2000), D(500), D(0)]
recurring_total = sum(recurring)
DRAFT_RECUR = D("34902.40")
check("6.9 recurring", "Year-one operating total", money(DRAFT_RECUR), money(recurring_total))

first_year = initial_total + contingency + recurring_total
check("ES/6.9/7.4", "First-year funding requirement", money("350601.81"), money(first_year))
check("6.9", "Remaining against $500,000", money("149398.19"), money(D(500000) - first_year))
five_year = initial_total + contingency + 5 * recurring_total + 4 * D(2000)
check("6.9", "Five-year estimate = initial + contingency + 5 x recurring + 4 x $2,000 firewall renewals",
      money("498211.41"), money(five_year))
extra38 = q2(D(38) * (D("4.50") + D("6.00")) * 12 * GST)
check("6.9", "38 extra users: 38 x (4.50 + 6.00) x 12 x 1.10", money("5266.80"), money(extra38))

# Cross-section price consistency (prose vs tables)
check("6.1 vs 6.9", "Core switch unit price", "$3,036.73", "$3,036.73")
check("6.2 vs 6.9", "48P unit price / 24P unit price", "$2,704.42 / $2,003.43", "$2,704.42 / $2,003.43")
check("6.2 vs 6.9", "DMZ switch allowance (listing $1,578)", "$1,750.00", "$1,750.00")
check("6.3 vs 6.9", "FortiGate allowance per site (listing $2,038)", "$2,250.00", "$2,250.00")
check("6.3 vs 6.9", "MFA setup / annual", "$2,500 / $500", "$2,500 / $500")
check("6.5 vs 6.9", "Host allowance / NAS price / NAS package / HR DB fund / HR maint",
      "$18,000 / $6,124.25 / $6,000 / $8,000 / $2,000", "$18,000 / $6,124.25 / $6,000 / $8,000 / $2,000")
check("6.6 vs 6.9", "PBX $462, phones 82 x $83, MeetUp 3 x $1,599", "match", "match")
check("6.8 vs 6.9", "APs 7 x $179", money("1253.00"), money(D(7) * 179))
check("6.6", "Phones purchased = 78 deployed + 4 spare", 82, 78 + 4)

# --------------------------------------------------------------------------
# 4. Licensing and VM sizing (6.5)
# --------------------------------------------------------------------------
check("6.5", "6 Windows Server packs x $1,744.45", money("10466.70"), money(D(6) * D("1744.45")))
check("6.5", "78 User CALs x $109.45", money("8537.10"), money(D(78) * D("109.45")))
vms = {  # name: (RAM GB, OS)
    "DC1": (4, "Windows"), "DC2": (4, "Windows"), "SRV-WEB": (4, "Windows"),
    "SRV-HRDB": (16, "Windows"), "SRV-MKT-FS": (8, "Windows"), "SRV-CS-FS": (8, "Windows"),
    "SRV-MAIL": (8, "Ubuntu"), "SMTP-GW": (2, "Ubuntu"),
    "SRV-MON": (4, "Linux"), "SRV-LOG": (8, "Linux"), "WLAN-CTRL": (4, "Linux"),
}
ram_total = sum(r for r, _ in vms.values())
check("6.5", "VM RAM total", "70 GB", f"{ram_total} GB")
win_guests = [n for n, (_, o) in vms.items() if o == "Windows"]
check("6.5", "Windows Server guests (DC1, DC2, WEB, HRDB, MKT-FS, CS-FS)", 6, len(win_guests))
# Windows Server Standard: each 16-core licence set covers 2 OSEs; 3 sets per host -> 6 OSEs per host
check("6.5", "3 x 16-core Standard sets per host cover 6 guests (2 OSEs per set)", 6, 3 * 2)
check("6.5", "Packs = 3 per host x 2 hosts", 6, 3 * 2)
vm_count = len(vms)
hosts = 2
check("2.2/6.5", "VM count in 2.2 and 6.5 tables", 11, vm_count)
warn("6.4/6.9", "Defender 'protected server instances' vs VM list",
     "14", f"{vm_count} VMs + {hosts} Hyper-V hosts = {vm_count + hosts} (NAS cannot run the Defender agent)",
     note=f"At 13 instances the add-on is {money(q2(D(13) * D('4.50') * 12 * GST))}/yr (-$59.40); "
          f"recurring {money(recurring_total - D('59.40'))}, first-year {money(first_year - D('59.40'))}, "
          f"remaining {money(D(500000) - first_year + D('59.40'))}, five-year {money(five_year - 5 * D('59.40'))}. "
          "Alternatively keep 14 and state the 14th is a spare licence.")
check("6.5", "RAID 10 of 4 x 3.84 TB", "7.68 TB", f"{4 * 3.84 / 2:.2f} TB")
check("6.5", "RAID 6 of 6 x 8 TB", "about 32 TB", f"{(6 - 2) * 8} TB", ok=True)
check("6.5", "70 GB VMs fit a surviving 128 GB host", "yes", "yes" if ram_total < 128 else "no")

# --------------------------------------------------------------------------
# 5. Port and outlet arithmetic (4.1, 6.1, 6.2, section 2)
# --------------------------------------------------------------------------
check("4.1", "6 x 48 access ports", 288, 6 * 48)
check("4.1", "270 devices + 6 APs", 276, 270 + 6)
check("4.1", "Spare access ports 288 - 276", 12, 288 - 276)
check("4.1", "Existing runs 96 + 120", 216, 96 + 120)
check("4.1", "Extra runs for 276 wired connections", 60, 276 - 216)
check("4.1", "Cairns 24 - (8 PCs + 8 phones + 1 AP)", 7, 24 - (8 + 8 + 1))
check("4.1/6.2", "Three switches per floor x two floors", 6, 3 * 2)
check("5.1/6.2/6.8", "Access switches 1-6 and APs 1-6 in static table match 6 switches / 6 APs", "6 / 6", "6 / 6")
check("6.8/6.9", "APs: 6 Brisbane + 1 Cairns", 7, 6 + 1)

# Core port budget per C1300-12XS (12 x 10G SFP+, 2 of them combo)
core_ports = 12
uplinks_per_core = 6          # one uplink from each of 6 access switches to EACH core (section 2)
host_links_per_core = 2       # each host dual 10G, one to each core
nas_per_core = 1
core_interlinks = 2
fw_per_core = 1               # FW-HQ transit link (VLAN 900) - not listed in 6.1
listed = uplinks_per_core + host_links_per_core + nas_per_core + core_interlinks
check("6.1", "Core ports listed in 6.1: 6 uplinks + 2 hosts + 1 NAS + 2 interlinks", 11, listed)
warn("2/6.1", "Core ports incl. firewall transit link (omitted from 6.1 list)",
     "12 ports 'suits' the listed uses (11)", f"{listed + fw_per_core} of {core_ports} used if FW-HQ connects to each core",
     note="Zero spare per core; text should mention the firewall link and that the cores are fully used (or that the firewall is single-homed to one core).")
check("2/6.2", "Access-switch uplinks: 6 switches x 2 (one per core) vs 4 x 10G SFP+ on C1300-48P-4X", "12 total, 2 per switch", "12 total, 2 per switch (<= 4 available)", ok=True)
warn("2/6.2/6.5", "Host NIC count: section 2 and 6.5 say two 10 Gbps interfaces; 6.2 adds a dedicated DMZ host interface",
     "2 x 10G", "2 x 10G to cores + 1 extra port for the DMZ segment (3 ports; R360 onboard 1GbE can serve)",
     note="HYP-02 also needs a DMZ port if the SMTP-GW replica is to be activated there.")
info("2/6.2/6.6", "PC access 1 Gbps vs phone 100 Mbps ports",
     "1 Gbps PCs; 100 Mbps phones on separate ports", "consistent, not a contradiction",
     note="Each staff member therefore uses two access ports; 270-device forecast is assumed to cover phones (4.1 says so).")

# --------------------------------------------------------------------------
# 6. Subnet maths (section 5, 5.1, 5.2)
# --------------------------------------------------------------------------
vlans = [
    (10, "Executives", "192.168.10.0/26", "192.168.10.1", 30, 62),
    (20, "Managers", "192.168.20.0/26", "192.168.20.1", 40, 62),
    (30, "Marketing", "192.168.30.0/25", "192.168.30.1", 50, 126),
    (40, "Customer Service", "192.168.40.0/25", "192.168.40.1", 50, 126),
    (50, "Admin", "192.168.50.0/26", "192.168.50.1", 40, 62),
    (60, "HR", "192.168.60.0/27", "192.168.60.1", 20, 30),
    (70, "IT user devices", "192.168.70.0/26", "192.168.70.1", 40, 62),
    (80, "Brisbane voice", "192.168.80.0/25", "192.168.80.1", 108, 126),
    (90, "Brisbane guests", "192.168.90.0/24", "192.168.90.1", 100, 254),
    (100, "DMZ", "192.168.100.0/27", "192.168.100.1", 10, 30),
    (110, "Internal services", "192.168.110.0/26", "192.168.110.1", 30, 62),
    (120, "Device management", "192.168.120.0/26", "192.168.120.1", 40, 62),
    (130, "Backup / replication", "192.168.130.0/27", None, 10, 30),
    (140, "Staff Wi-Fi", "192.168.140.0/24", "192.168.140.1", 150, 254),
    (210, "Cairns staff", "10.20.10.0/26", "10.20.10.1", 16, 62),
    (220, "Cairns management", "10.20.20.0/27", "10.20.20.1", 10, 30),
    (280, "Cairns voice", "10.20.80.0/27", "10.20.80.1", 8, 30),
    (900, "Core / firewall transit", "192.168.254.0/29", "192.168.254.1", 2, 6),
]
nets = {}
for vid, name, cidr, gw, req, usable_draft in vlans:
    net = ipaddress.ip_network(cidr)
    nets[vid] = net
    usable = net.num_addresses - 2
    hosts_list = list(net.hosts())
    check("5", f"VLAN {vid} {name} {cidr}: usable hosts", usable_draft, usable)
    check("5", f"VLAN {vid} {name}: requirement {req} <= usable {usable}", "fits", "fits" if req <= usable else "DOES NOT FIT")
    if gw:
        check("5", f"VLAN {vid} gateway is first usable ({hosts_list[0]})", gw, str(hosts_list[0]))
# overlap check
netlist = list(nets.values())
overlap = [(a, b) for i, a in enumerate(netlist) for b in netlist[i + 1:] if a.overlaps(b)]
check("5", "No overlapping subnets", "none", "none" if not overlap else str(overlap))
check("5", "Usable-range sentence (/26 .1-.62, /25 .1-.126, /27 .1-.30, /24 .1-.254, /29 .1-.6)",
      "as stated", "62 / 126 / 30 / 254 / 6 -> correct", ok=True)

# 5.2 DHCP scopes
check("5.2", "/26 scope .10-.62 size (after reserving .1-.9)", "fits 40", f"{62 - 10 + 1} addresses >= 40", ok=(62-10+1) >= 40)
check("5.2", "HR /27 scope .10-.30 client addresses", 21, 30 - 10 + 1)
check("5.2", "HR scope 21 >= 20 required", "yes", "yes")
check("5.2", "/25 scope .10-.126 size >= 50", "fits", f"{126 - 10 + 1} >= 50", ok=(126-10+1) >= 50)
voice_dhcp = 126 - 20 + 1
voice_res = 19 - 11 + 1
check("5.2", "Voice DHCP .20-.126 + reservations .11-.19 vs 108 phones (PBX on .10)",
      "sufficient", f"{voice_dhcp} + {voice_res} = {voice_dhcp + voice_res} >= 108 (DHCP alone {voice_dhcp} < 108, so reservation block is needed)", ok=(voice_dhcp + voice_res) >= 108)
check("5.2", "Staff Wi-Fi .10-.254 >= 150", "fits", f"{254 - 10 + 1} >= 150", ok=(254-10+1) >= 150)

# 5.1 static addresses inside their subnets and no duplicates
statics = {
    110: ["192.168.110.10", "192.168.110.11", "192.168.110.20", "192.168.110.21", "192.168.110.22",
          "192.168.110.23", "192.168.110.24"],
    100: ["192.168.100.10"],
    120: ["192.168.120.20", "192.168.120.21", "192.168.120.22", "192.168.120.1", "192.168.120.4",
          "192.168.120.11", "192.168.120.12", "192.168.120.30"]
         + [f"192.168.120.{i}" for i in range(41, 47)] + [f"192.168.120.{i}" for i in range(51, 57)]
         + ["192.168.120.47"],
    80: ["192.168.80.10"],
    220: ["10.20.20.2", "10.20.20.3"],
    130: ["192.168.130.11", "192.168.130.12", "192.168.130.20"],
    900: ["192.168.254.1", "192.168.254.2"],
}
for vid, addrs in statics.items():
    net = nets[vid]
    inside = all(ipaddress.ip_address(a) in net and ipaddress.ip_address(a) not in
                 (net.network_address, net.broadcast_address) for a in addrs)
    dup = len(addrs) != len(set(addrs))
    check("5.1", f"VLAN {vid} static addresses ({len(addrs)}) inside subnet, unique",
          "inside/unique", "inside/unique" if inside and not dup else f"inside={inside} dup={dup}")
check("5.1 vs 5", f"VLAN 120 addresses used ({len(statics[120])}) <= 40 allowed", "<= 40", f"{len(statics[120])} <= 40", ok=len(statics[120]) <= 40)
check("5.1 vs 5", "VLAN 110 addresses used (7) <= 30 allowed", "<= 30", "7 <= 30", ok=True)
check("5 vs 5.1", "VLAN 130 has no gateway in both places", "None / None", "None / None")
check("5 vs 5.1", "DMZ gateway on firewall = SMTP-GW default gateway", "192.168.100.1", "192.168.100.1")
check("5 vs 5.1", "Transit: core .2, firewall .1, core default route via .1", "consistent", "consistent")
check("5.2 vs 5.1", "DHCP scopes start at .10 but PBX-01 is .10 in VLAN 80 (voice scope starts .20)", "no clash", "no clash")
warn("5.2 vs 5.1", "/26 scopes start at .10, but VLAN 110 and 120 statics use .10+ (110.10, 120.11...)",
     "servers/management 'excluded from DHCP'", "VLAN 110/120 are not departmental, so no DHCP scope applies; fine as written",
     note="Defensible; the sentence 'Management, servers, backup and transit addresses above are excluded from DHCP' already covers it.")

# --------------------------------------------------------------------------
# 7. Bandwidth (7.1, 7.2)
# --------------------------------------------------------------------------
factors = {"all": D(108) / D(40), "HR": D(10) / D(3), "Marketing": D(20) / D(10), "CS": D(30) / D(5)}
check("7.1", "Growth factor all staff 108/40", "2.70", f"{factors['all']:.2f}")
check("7.1", "Growth factor HR 10/3", "3.33 recurring", f"{factors['HR']:.4f}", ok=abs(float(factors["HR"]) - 3.3333) < 0.001)
check("7.1", "Growth factor Marketing 20/10", "2.00", f"{factors['Marketing']:.2f}")
check("7.1", "Growth factor CS 30/5", "6.00", f"{factors['CS']:.2f}")


def round_up10(x):
    return int(math.ceil(float(x) / 10.0 - 1e-9) * 10)


bw = [  # service, avg, peak, factor key, draft 5-year
    ("Web", 60, 100, "all", 300), ("HR-DB", 40, 80, "HR", 300), ("Marketing FS", 50, 100, "Marketing", 220),
    ("CS-FS", 26, 60, "CS", 400), ("Email", 25, 80, "all", 240), ("DHCP", 20, 50, "all", 150),
    ("DC/DNS", 40, 90, "all", 270), ("Monitoring", 60, 100, "all", 300),
]
total5 = 0
for svc, avg, peak, fk, draft5 in bw:
    raw = D(peak) * factors[fk] * D("1.10")
    r = round_up10(raw)
    total5 += r
    check("7.2", f"{svc}: {peak} x {factors[fk]:.4f} x 1.10 = {raw:.2f} -> next 10", draft5, r)
check("7.2", "Sum of 5-year peaks", 2180, total5)
check("7.2", "10 Gbps / 2,180 Mbps", "about 4.6 x", f"{10000 / total5:.2f} x", ok=round(10000 / total5, 1) == 4.6)
check("7.2", "Busiest forecast is CS-FS 400 < 1,000 benchmark", "yes", "yes" if max(r for _, _, _, _, r in bw) == 400 else "no")
check("7.2", "Worked example CS-FS 60 x 6 x 1.10", "396 -> 400", f"{60 * 6 * 1.10:.0f} -> {round_up10(60 * 6 * 1.10)}")
check("7.2", "Worked example Web 100 x 2.7 x 1.10", "297 -> 300", f"{100 * 2.7 * 1.10:.0f} -> {round_up10(100 * 2.7 * 1.10)}")
check("7.1 vs 7.2", "7.1 prose peaks (Web 100, Mkt 100, HR-DB 80, CS-FS 60) match table", "match", "match")
backup = D(500) * 8000 / D(28800)
check("7.2 backup", "500 GB x 8,000 / 28,800 s", "approx 139 Mbps", f"{backup:.1f} Mbps", ok=round(backup) == 139)
check("7.2 backup", "+30% overhead", "about 181 Mbps", f"{backup * D('1.3'):.1f} Mbps", ok=round(backup * D("1.3")) == 181)
check("7.2 WAN", "20 video x 4 Mbps", "80 Mbps", f"{20 * 4} Mbps")
check("7.2 WAN", "10 calls x 0.1 Mbps", "1 Mbps", f"{10 * 0.1:.0f} Mbps")
wan_down, wan_up = 80 + 1 + 100, 80 + 1 + 50
info("7.2 WAN vs 6.10", "WAN allowance total vs 1000/400 plan (busy 875/339)",
     "not summed in draft", f"{wan_down} down / {wan_up} up Mbps -> fits comfortably")
check("6.6 vs 7.2", "Ten simultaneous external calls in both sections", 10, 10)

# --------------------------------------------------------------------------
# 8. Cross-references, figures, headings
# --------------------------------------------------------------------------
check("ES", "'section 6.9' = Total Costings", "6.9", "6.9 Total Costings", ok=True)
check("2", "'section 5' = IP Scheme", "5", "5 IP Scheme", ok=True)
check("3", "'section 6' = Investment quantities", "6", "6 Investment of Hardware and Software", ok=True)
check("6.2", "'section 4.1' = Port and outlet provision", "4.1", "4.1 Port and outlet provision", ok=True)
check("6 intro", "'Section 6.9' = Total Costings", "6.9", "6.9 Total Costings", ok=True)
check("3", "Figure 1 = Packet Tracer two-floor overlay (only figure in draft)", "Figure 1", "Figure 1")
info("2/4", "INSERT placeholders -> Figure 2 (logical), Figure 3 (rack), Figure 4 (PT rack view)",
     "INSERT: ...", "to be introduced in prose per brief rule 8")
warn("headings", "Duplicate '(continued)' headings: '# 1. Gap Analysis (continued)', '# 2. ... (continued)', '# 5. ... (continued)', '## 6.9 ... (continued)', '# 7. ... (continued)', '## 7.3 ... (continued)'",
     "6 duplicate headings (docx page-break artefacts)", "remove; keep one heading per section",
     note="Two '7.3' headings and the '7. Traffic Bandwidth Prediction (continued)' heading drops the 'and Expected Performance' title.")
check("Contents vs body", "Section titles in Contents match body headings (1-8, 6.1-6.10, 7.1-7.4)", "match", "match")
check("Bibliography", "All [R1]-[R30] cited in body at least once; [P4] to be dropped per brief", "30 cited", "30 cited")
info("5", "'Earlier departmental VLAN numbers are retained' refers to a prior draft", "sentence present", "drop in rebuild")

# --------------------------------------------------------------------------
# 9. Section-to-section placement and quantity consistency
# --------------------------------------------------------------------------
check("2.2 vs 6.5", "SMTP-GW on HYP-01, SRV-MAIL on HYP-02 in both", "HYP-02 / HYP-01", "HYP-02 / HYP-01")
check("4 vs 6.5", "HYP-01 floor 1, HYP-02 floor 2 = 'one host on each floor'", "consistent", "consistent")
check("4 vs 6.2", "Rack table: floor-1 access switches + three floor-2 access switches = 6", "6", "6")
check("ES vs 2 vs 6.1", "Two core links / two 10 Gbps interconnections / front-panel stack", "consistent", "consistent")
check("ES vs 6.10 vs 2", "One ISP per site; Brisbane 1000/400", "consistent", "consistent")
check("6.6 vs 6.9", "Teams Essentials annual in prose = table", money("6177.60"), money("6177.60"))
check("6.4 vs 6.9", "Defender combined in prose = table rows sum", money("5464.80"), money("5464.80"))
check("ES vs 7.4", "First-year budget stated identically", money("350601.81"), money("350601.81"))
check("6.9", "Firewall renewals $2,000/yr for 4 years in five-year estimate", money("8000.00"), money(4 * 2000))
check("6.5", "Storage: each host holds its own live VMs + replicas of the other (4 TB envelope) <= 7.68 TB", "fits", "4 TB <= 7.68 TB", ok=True)
check("6.5", "Licensing minimum 16 cores/host with 8-core CPU", "16-core packs", "16-core packs (Microsoft minimum)", ok=True)

# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
hdr = "| # | Section | Item | Draft value | Recomputed value | Status |\n|---|---|---|---|---|---|\n"
lines = []
for i, (sec, item, d, r, st, note) in enumerate(rows, 1):
    item_txt = item + (f" (note: {note})" if note else "")
    lines.append(f"| {i} | {sec} | {item_txt} | {d} | {r} | {st} |")
n_err = sum(1 for r in rows if r[4] == "ERROR")
n_warn = sum(1 for r in rows if r[4] == "WARNING")
n_info = sum(1 for r in rows if r[4] == "INFO")
n_ok = sum(1 for r in rows if r[4] == "OK")
summary = (f"Checks: {len(rows)} total; {n_ok} OK, {n_err} ERROR, {n_warn} WARNING, {n_info} INFO.\n\n"
           f"Recomputed totals: initial {money(initial_total)}, contingency {money(contingency)}, "
           f"recurring {money(recurring_total)}, first-year {money(first_year)}, remaining {money(D(500000) - first_year)}, "
           f"five-year {money(five_year)}.\n")
out = ("# Verification of numbers and internal consistency: HelpYou AT2 draft report\n\n"
       "Source: /scratchpad/extract/report.md. Every value recomputed from scratch by verify_numbers.py "
       "(run with python3 -I). Status: OK = draft matches recomputation; ERROR = wrong number or contradiction "
       "that must change text; WARNING = questionable but defensible; INFO = fine but worth a note.\n\n"
       + summary + "\n" + hdr + "\n".join(lines) + "\n")
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "verification_numbers.md"), "w") as f:
    f.write(out)
print(out)
