#!/usr/bin/env python3
"""Final section 6.9 costing for the HelpYou AT2 report rebuild.

Rule (student's instruction, binding): every price is EXACTLY the figure in the
draft report (scratchpad/extract/report.md, section 6.9). No live price is
adopted. This script only reconfirms the draft's arithmetic and prints the three
6.9 tables in the layout the rebuilt report must carry (hardware / software and
licences / services and labour sub-totals added for marking criterion 3.5; no
figure changes).

The number verifier (verification_numbers.md) found 0 arithmetic errors, so the
totals printed here equal the draft's totals. The script asserts that.

Defender servers add-on: the draft's 14 instances are KEPT (11 virtual servers
+ 2 Hyper-V hosts + 1 spare licence); the text in 6.4 now says what the 14 are.

Run:  python3 -I costing_final.py
The markdown it prints is pasted verbatim into corrections.md section 1.2.
"""
from decimal import Decimal, ROUND_HALF_UP

D = Decimal
CENT = D("0.01")
GST = D("1.10")


def q(x: Decimal) -> Decimal:
    return x.quantize(CENT, rounding=ROUND_HALF_UP)


def money(x: Decimal) -> str:
    return "${:,.2f}".format(q(x))


# ---------------------------------------------------------------------------
# Initial procurement and implementation (AUD inc GST), draft figures verbatim
# (group, item, qty, unit, basis)
# ---------------------------------------------------------------------------
initial = [
    ("Hardware", "Core switches - Cisco C1300-12XS", 2, D("3036.73"), "P [R2]"),
    ("Hardware", "Head-office access - Cisco C1300-48P-4X", 6, D("2704.42"), "P [R3]"),
    ("Hardware", "Cairns access - Cisco C1300-24P-4X", 1, D("2003.43"), "P [R4]"),
    ("Hardware", "DMZ switch - Cisco C1300-24T-4X", 1, D("1750.00"), "A [R30]"),
    ("Hardware", "FortiGate 70G + year-one UTP, one per site", 2, D("2250.00"), "A [R6]"),
    ("Hardware", "Dell R360 configured virtualisation hosts", 2, D("18000.00"), "A [R7]"),
    ("Hardware", "Synology RS2423RP+ diskless NAS", 1, D("6124.25"), "P [R13]"),
    ("Hardware", "NAS drives, rails and backup media package", 1, D("6000.00"), "A"),
    ("Hardware", "Head-office and branch UPS / rack fit-out", 1, D("7000.00"), "A"),
    ("Hardware", "TP-Link EAP650 access points", 7, D("179.00"), "P [R20]"),
    ("Hardware", "Grandstream UCM6302 IP PBX", 1, D("462.00"), "P [R15]"),
    ("Hardware", "GRP2612P phones (78 deployed, four spare)", 82, D("83.00"), "P [R16]"),
    ("Hardware", "Logitech MeetUp 2 (two Brisbane, one Cairns)", 3, D("1599.00"), "P [R18]"),
    ("Hardware", "Endpoint replacement / OS / peripherals fund", 78, D("1500.00"), "A"),
    ("Hardware", "Compatible optics and connection accessories", 1, D("6500.00"), "A"),
    ("Software and licences", "Windows Server 2025 Standard 16-core packs", 6, D("1744.45"), "P [R8]"),
    ("Software and licences", "Windows Server User CALs", 78, D("109.45"), "P [R10]"),
    ("Software and licences", "HR database/application compatibility fund", 1, D("8000.00"), "A"),
    ("Software and licences", "Remote-access MFA licensing / enrolment fund", 1, D("2500.00"), "A"),
    ("Services and labour", "Cabling certification and extra outlets", 1, D("6000.00"), "A"),
    ("Services and labour", "Design, installation and migration labour (hours)", 160, D("150.00"), "A"),
    ("Services and labour", "Staff and IT training / handover", 1, D("5000.00"), "A"),
]
GROUPS = ("Hardware", "Software and licences", "Services and labour")

# ---------------------------------------------------------------------------
# Recurring (annual, AUD inc GST), draft figures verbatim
# ---------------------------------------------------------------------------
users = 78
server_instances = 14  # 11 VMs + 2 Hyper-V hosts + 1 spare licence (draft figure kept)
defender_user = q(D(users) * D("4.50") * 12 * GST)
defender_server = q(D(server_instances) * D("4.50") * 12 * GST)
teams = q(D(users) * D("6.00") * 12 * GST)
isp_bne = q(D("160") * 12)
isp_cns = q(D("120") * 12)
sip = q(D("600") * 12)

recurring = [
    ("Defender for Business: 78 users", "78 x AU$4.50 x 12 x 1.10", defender_user, "P [R11]"),
    ("Defender for Business servers add-on: 14 instances", "14 x AU$4.50 x 12 x 1.10", defender_server, "P [R11]"),
    ("Teams Essentials: 78 users", "78 x AU$6.00 x 12 x 1.10", teams, "P [R17]"),
    ("Brisbane: Aussie Broadband Business Assurance Ultrafast Plus 1000/400", "12 x $160", isp_bne, "P [R24]"),
    ("Cairns internet service allowance", "12 x $120", isp_cns, "A [R24]"),
    ("SIP trunk, numbers and call allowance", "12 x $600", sip, "A [R25]"),
    ("Off-site backup custody / media rotation", "allowance", D("1200.00"), "A"),
    ("External support, patches and restore tests", "allowance", D("9000.00"), "A"),
    ("Business application maintenance allowance", "allowance", D("2000.00"), "A"),
    ("MFA subscription / token renewal fund", "allowance", D("500.00"), "A"),
    ("Zabbix, Wazuh and Ubuntu licence fees", "self-hosted open source", D("0.00"), "[R22, R23, R29]"),
]
firewall_renewal = D("2000.00")  # per year, years 2 to 5 (allowance)
budget = D("500000.00")

# ---------------------------------------------------------------------------
# Totals
# ---------------------------------------------------------------------------
lines = [(g, i, n, u, q(D(n) * u), b) for (g, i, n, u, b) in initial]
group_sub = {g: sum(lt for gg, _, _, _, lt, _ in lines if gg == g) for g in GROUPS}
initial_total = sum(lt for *_, lt, _b in lines)
contingency = q(initial_total * D("0.10"))
recurring_total = sum(a for _, _, a, _ in recurring)
first_year = q(initial_total + contingency + recurring_total)
remaining = q(budget - first_year)
five_year = q(initial_total + contingency + 5 * recurring_total + 4 * firewall_renewal)
defender_combined = q(defender_user + defender_server)
extra_users = 116 - 78
extra_subs = q(D(extra_users) * (D("4.50") + D("6.00")) * 12 * GST)

# Reconfirmation: every total must equal the draft (no arithmetic errors found)
DRAFT = {
    "initial": D("286999.46"), "contingency": D("28699.95"), "recurring": D("34902.40"),
    "first_year": D("350601.81"), "remaining": D("149398.19"), "five_year": D("498211.41"),
    "defender_combined": D("5464.80"), "extra_subs": D("5266.80"),
}
assert initial_total == DRAFT["initial"], initial_total
assert contingency == DRAFT["contingency"], contingency
assert recurring_total == DRAFT["recurring"], recurring_total
assert first_year == DRAFT["first_year"], first_year
assert remaining == DRAFT["remaining"], remaining
assert five_year == DRAFT["five_year"], five_year
assert defender_combined == DRAFT["defender_combined"], defender_combined
assert extra_subs == DRAFT["extra_subs"], extra_subs

# ---------------------------------------------------------------------------
# Print the three tables exactly as the report must carry them
# ---------------------------------------------------------------------------
print("### Table 6.9a Initial procurement and implementation (AUD including GST)")
print()
print("| Initial item | Qty | Unit budget | Line total | Basis |")
print("|---|---|---|---|---|")
for group in GROUPS:
    for g, i, n, u, lt, b in lines:
        if g == group:
            print(f"| {i} | {n} | {money(u)} | {money(lt)} | {b} |")
    print(f"| {group} subtotal | | | {money(group_sub[group])} | Calculated |")
print(f"| Initial procurement and implementation | | | {money(initial_total)} | Calculated |")
print(f"| Contingency: 10% of the above | | | {money(contingency)} | Calculated |")
print()
print("P = published Australian retail listing (the figure found on 7 October 2026); A = allowance pending a supplier quote.")
print()
print("### Table 6.9b Recurring costs (annual, AUD including GST)")
print()
print("| Recurring item | Calculation | Annual cost | Basis |")
print("|---|---|---|---|")
for i, c, a, b in recurring:
    print(f"| {i} | {c} | {money(a)} | {b} |")
print(f"| Year-one operating total | | {money(recurring_total)} | Calculated |")
print(f"| Firewall UTP renewals, years 2 to 5 | 2 sites, allowance | {money(firewall_renewal)} | A; year 1 is inside the bundle |")
print()
print("### Table 6.9c Budget summary (AUD including GST)")
print()
print("| Budget summary | AUD including GST |")
print("|---|---|")
print(f"| Initial implementation | {money(initial_total)} |")
print(f"| Implementation contingency (10%) | {money(contingency)} |")
print(f"| First-year recurring costs | {money(recurring_total)} |")
print(f"| First-year funding requirement | {money(first_year)} |")
print(f"| Remaining against the $500,000 budget | {money(remaining)} |")
print(f"| Five-year baseline ownership estimate | {money(five_year)} |")
print()
print("Five-year estimate = initial implementation + contingency + 5 x year-one operating total + 4 x $2,000 firewall renewals.")
print()
print("### Supporting arithmetic (quoted in prose elsewhere in the report)")
print()
print(f"- Hardware subtotal {money(group_sub['Hardware'])}; software and licences {money(group_sub['Software and licences'])}; services and labour {money(group_sub['Services and labour'])}; sum {money(initial_total)}")
print(f"- Contingency: 10% x {money(initial_total)} = $28,699.946, rounded to {money(contingency)}")
print(f"- Defender combined annual (users + servers): {money(defender_user)} + {money(defender_server)} = {money(defender_combined)}")
print(f"- Defender server instances: 11 virtual servers + 2 Hyper-V hosts + 1 spare licence = {server_instances}")
print(f"- Teams Essentials annual: 78 x 6.00 x 12 x 1.10 = {money(teams)}")
print(f"- Extra 38 users (78 to 116): 38 x (4.50 + 6.00) x 12 x 1.10 = {money(extra_subs)} per year")
print(f"- First year: {money(initial_total)} + {money(contingency)} + {money(recurring_total)} = {money(first_year)}")
print(f"- Remaining: $500,000.00 - {money(first_year)} = {money(remaining)}")
print(f"- Five-year components: {money(initial_total)} + {money(contingency)} + 5 x {money(recurring_total)} ({money(5 * recurring_total)}) + 4 x $2,000.00 ($8,000.00) = {money(five_year)}")
print()
print("### Reconfirmation against the draft")
print()
print("All six headline figures equal the draft's figures (asserted in costing_final.py): initial $286,999.46; contingency $28,699.95; recurring $34,902.40; first year $350,601.81; remaining $149,398.19; five year $498,211.41. No price and no total changes.")
