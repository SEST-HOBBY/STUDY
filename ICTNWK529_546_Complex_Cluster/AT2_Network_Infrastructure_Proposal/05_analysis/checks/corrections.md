# Corrections file: single source of truth for the HelpYou AT2 rebuild

Compiled 7 October 2026 (second pass, replacing the earlier version that adopted live prices) from verification_numbers.md, verification_refs_1_10.md, verification_refs_11_20.md, verification_refs_21_30.md, audit_voice_mc.md, inventory_topology.md and inventory_floorplan.md, against the draft at scratchpad/extract/report.md. Every section rewriter follows this file verbatim. Where the draft and this file disagree, this file wins. Where this file is silent, keep the draft's figure and substance (reworded under the brief's voice rules).

## Binding rules (student's instructions; these override every checker finding)

1. **Every price is exactly the draft's price.** No live price is adopted anywhere. The checkers' live findings (R3, R6, R13, R15, R30 moved; R7, R10, R18 unreadable) are recorded in section 1.1 for the orchestrator only and must NOT appear in the report. No "price as listed on", "live check", "currently reports no stock", "out of stock", "preorder" or similar stock or price-movement commentary anywhere in the body.
2. **Every URL is exactly the draft's URL.** No cited page was proved gone (no HTTP 404/410, no removed product). Pages that were merely blocked by the sandbox proxy, bot protection or a 503 (Dell R7 and R10, Video Conferencing Australia R18, Teams R17) are kept. Zero bibliography URL changes.
3. **One price-date sentence in 6.9 and one in the bibliography, nowhere else.** 6.9: "Lines marked P are the Australian retail listings I found on 7 October 2026; lines marked A are my allowances pending supplier quotes." Bibliography: "Vendor and retail pages were accessed on 7 October 2026; the prices in section 6 are the listings found on that date." Delete "Prices were researched on 7 October 2026" from the section 6 introduction and "Retail references are dated 7 October 2026" from the old 6.9 lead-in.
4. **Website links appear once, in the bibliography, as clickable hyperlinks.** In the body each product carries its price and its [R#] only. Every [R1]-[R30] bibliography entry is a clickable hyperlink (markdown `[url](url)`; the .docx builder must keep it as a Word hyperlink).
5. **Firewall placement.** The FortiGate 70G (FW-HQ) sits directly behind the ISP handoff and in front of the two core switches: ISP -> FW-HQ -> core stack. Say so in plain words in the gap analysis (its own row), in section 2's first paragraph and link table, and draw it that way in Figure 2.
6. **Gap analysis detail.** Eighteen rows, one per topic (section 2 of this file lists each row's numbers). Every row carries figures.
7. **Figures and totals: nothing changes.** The number verifier found 0 arithmetic errors (199 checks: 190 OK, 5 warnings, 4 info). The warnings are consistency gaps fixed by wording, not by numbers (section 1.3).

Arithmetic: /tmp/claude-0/-home-user-STUDY/f8a3790f-8c1d-5a3f-8f9c-d2abf23b0604/scratchpad/work/analysis/costing_final.py (run with `python3 -I`; it asserts that every total equals the draft). Section 1.2 below is its output, unedited (also saved as costing_final_output.md).

Formatting note for the .docx builder: if the markdown goes through pandoc, escape dollar signs (`\$`) as the draft did; no em dashes anywhere.

---

## 1. Final figures

### 1.1 Every price, reconfirmed as the draft's figure

| Ref | Product | FINAL figure in the report (= draft) | Checker's live finding, 7 Oct 2026 (orchestrator record only; NOT for the report) |
|---|---|---|---|
| R2 | Cisco C1300-12XS core switch | $3,036.73 each inc GST; 2 = $6,073.46 | Same price on the page. |
| R3 | Cisco C1300-48P-4X access switch | $2,704.42 each inc GST; 6 = $16,226.52 | Page now shows $2,880.62. Draft figure kept. |
| R4 | Cisco C1300-24P-4X Cairns switch | $2,003.43 inc GST | Same price on the page. |
| R30 | Cisco C1300-24T-4X DMZ switch | reference listing $1,578; allowance $1,750.00 used in 6.9 | Page now shows $1,632.00, preorder. Draft figures kept; allowance still covers it. |
| R6 | FortiGate FG-70G-BDL-950-12 (70G + 1 yr FortiCare Premium + FortiGuard UTP) | reference listing $2,038; allowance $2,250.00 per site; 2 = $4,500.00 | Page shows $3,028.00, out of stock. Draft figures kept. Do not mention stock. |
| R7 | Dell PowerEdge R360 host | Dell starting price $6,047.97 inc GST (as the draft); allowance $18,000.00 per configured host; 2 = $36,000.00 | Dell blocks automated reads; unverifiable. Draft figure kept, URL kept. |
| R8 | Windows Server 2025 Standard 16-core OEM pack EP2-25187 | $1,744.45 each; 6 = $10,466.70 | Same price on the page. |
| R9 | Microsoft Windows Server pricing page | no figure (licensing rules only: 16-core packs, CALs for every user or device) | Page shows "VARIABLE". Never attach a dollar figure to [R9]. |
| R10 | Windows Server User CAL (Dell R450 configurator) | $109.45 each; 78 = $8,537.10 | Dell blocks automated reads; unverifiable. Draft figure kept, URL kept. |
| R11 | Defender for Business and servers add-on | AU$4.50 per user or server per month ex GST; 78 users $4,633.20; 14 servers $831.60; combined $5,464.80 | Same price on the page. |
| R13 | Synology RS2423RP+ diskless NAS | $6,124.25 inc GST | Page shows $6,014.25. Draft figure kept. |
| R15 | Grandstream UCM6302 IP PBX | $462 inc GST | Page shows $605.00. Draft figure kept. |
| R16 | Grandstream GRP2612P phone | $83 each; 82 = $6,806.00 | Same price on the page. |
| R17 | Microsoft Teams Essentials | AU$6 per user per month ex GST; 78 users = $6,177.60 a year inc GST | Same price on the page. |
| R18 | Logitech MeetUp 2 | $1,599 each; 3 = $4,797.00 | Cited page blocked by bot protection; unverifiable. Draft figure kept, URL kept. |
| R20 | TP-Link EAP650 | $179 each; 7 = $1,253.00 | Same price on the page (retailer out of stock). Drop the draft's "cited retailer currently reports no stock" clause. |
| R24 | Aussie Broadband Business Assurance Ultrafast Plus 1000/400 | $160 a month = $1,920.00 a year; Cairns allowance $120 a month = $1,440.00 a year | Same price on the page; 875/339 Mbps typical busy-period, static IP, Gold eSLA, FTTP all confirmed. |
| R25 | SIP trunks (Aussie Broadband / Nexgen) | $600 a month allowance = $7,200.00 a year | Quote-based page, no price; allowance stands. |
| none | Firewall UTP renewals, years 2 to 5 | $2,000.00 a year (allowance) | n/a |
| none | All other allowances | NAS drives/rails/media $6,000; UPS and rack fit-out $7,000; endpoint fund 78 x $1,500 = $117,000; optics $6,500; cabling $6,000; HR application fund $8,000 and $2,000 a year; labour 160 h x $150 = $24,000; training $5,000; MFA $2,500 setup and $500 a year; off-site custody $1,200 a year; external support $9,000 a year | n/a |

### 1.2 Section 6.9 tables (verbatim output of costing_final.py)

### Table 6.9a Initial procurement and implementation (AUD including GST)

| Initial item | Qty | Unit budget | Line total | Basis |
|---|---|---|---|---|
| Core switches - Cisco C1300-12XS | 2 | $3,036.73 | $6,073.46 | P [R2] |
| Head-office access - Cisco C1300-48P-4X | 6 | $2,704.42 | $16,226.52 | P [R3] |
| Cairns access - Cisco C1300-24P-4X | 1 | $2,003.43 | $2,003.43 | P [R4] |
| DMZ switch - Cisco C1300-24T-4X | 1 | $1,750.00 | $1,750.00 | A [R30] |
| FortiGate 70G + year-one UTP, one per site | 2 | $2,250.00 | $4,500.00 | A [R6] |
| Dell R360 configured virtualisation hosts | 2 | $18,000.00 | $36,000.00 | A [R7] |
| Synology RS2423RP+ diskless NAS | 1 | $6,124.25 | $6,124.25 | P [R13] |
| NAS drives, rails and backup media package | 1 | $6,000.00 | $6,000.00 | A |
| Head-office and branch UPS / rack fit-out | 1 | $7,000.00 | $7,000.00 | A |
| TP-Link EAP650 access points | 7 | $179.00 | $1,253.00 | P [R20] |
| Grandstream UCM6302 IP PBX | 1 | $462.00 | $462.00 | P [R15] |
| GRP2612P phones (78 deployed, four spare) | 82 | $83.00 | $6,806.00 | P [R16] |
| Logitech MeetUp 2 (two Brisbane, one Cairns) | 3 | $1,599.00 | $4,797.00 | P [R18] |
| Endpoint replacement / OS / peripherals fund | 78 | $1,500.00 | $117,000.00 | A |
| Compatible optics and connection accessories | 1 | $6,500.00 | $6,500.00 | A |
| Hardware subtotal | | | $222,495.66 | Calculated |
| Windows Server 2025 Standard 16-core packs | 6 | $1,744.45 | $10,466.70 | P [R8] |
| Windows Server User CALs | 78 | $109.45 | $8,537.10 | P [R10] |
| HR database/application compatibility fund | 1 | $8,000.00 | $8,000.00 | A |
| Remote-access MFA licensing / enrolment fund | 1 | $2,500.00 | $2,500.00 | A |
| Software and licences subtotal | | | $29,503.80 | Calculated |
| Cabling certification and extra outlets | 1 | $6,000.00 | $6,000.00 | A |
| Design, installation and migration labour (hours) | 160 | $150.00 | $24,000.00 | A |
| Staff and IT training / handover | 1 | $5,000.00 | $5,000.00 | A |
| Services and labour subtotal | | | $35,000.00 | Calculated |
| Initial procurement and implementation | | | $286,999.46 | Calculated |
| Contingency: 10% of the above | | | $28,699.95 | Calculated |

P = published Australian retail listing (the figure found on 7 October 2026); A = allowance pending a supplier quote.

### Table 6.9b Recurring costs (annual, AUD including GST)

| Recurring item | Calculation | Annual cost | Basis |
|---|---|---|---|
| Defender for Business: 78 users | 78 x AU$4.50 x 12 x 1.10 | $4,633.20 | P [R11] |
| Defender for Business servers add-on: 14 instances | 14 x AU$4.50 x 12 x 1.10 | $831.60 | P [R11] |
| Teams Essentials: 78 users | 78 x AU$6.00 x 12 x 1.10 | $6,177.60 | P [R17] |
| Brisbane: Aussie Broadband Business Assurance Ultrafast Plus 1000/400 | 12 x $160 | $1,920.00 | P [R24] |
| Cairns internet service allowance | 12 x $120 | $1,440.00 | A [R24] |
| SIP trunk, numbers and call allowance | 12 x $600 | $7,200.00 | A [R25] |
| Off-site backup custody / media rotation | allowance | $1,200.00 | A |
| External support, patches and restore tests | allowance | $9,000.00 | A |
| Business application maintenance allowance | allowance | $2,000.00 | A |
| MFA subscription / token renewal fund | allowance | $500.00 | A |
| Zabbix, Wazuh and Ubuntu licence fees | self-hosted open source | $0.00 | [R22, R23, R29] |
| Year-one operating total | | $34,902.40 | Calculated |
| Firewall UTP renewals, years 2 to 5 | 2 sites, allowance | $2,000.00 | A; year 1 is inside the bundle |

### Table 6.9c Budget summary (AUD including GST)

| Budget summary | AUD including GST |
|---|---|
| Initial implementation | $286,999.46 |
| Implementation contingency (10%) | $28,699.95 |
| First-year recurring costs | $34,902.40 |
| First-year funding requirement | $350,601.81 |
| Remaining against the $500,000 budget | $149,398.19 |
| Five-year baseline ownership estimate | $498,211.41 |

Five-year estimate = initial implementation + contingency + 5 x year-one operating total + 4 x $2,000 firewall renewals.

### Supporting arithmetic (quoted in prose elsewhere in the report)

- Hardware subtotal $222,495.66; software and licences $29,503.80; services and labour $35,000.00; sum $286,999.46
- Contingency: 10% x $286,999.46 = $28,699.946, rounded to $28,699.95
- Defender combined annual (users + servers): $4,633.20 + $831.60 = $5,464.80
- Defender server instances: 11 virtual servers + 2 Hyper-V hosts + 1 spare licence = 14
- Teams Essentials annual: 78 x 6.00 x 12 x 1.10 = $6,177.60
- Extra 38 users (78 to 116): 38 x (4.50 + 6.00) x 12 x 1.10 = $5,266.80 per year
- First year: $286,999.46 + $28,699.95 + $34,902.40 = $350,601.81
- Remaining: $500,000.00 - $350,601.81 = $149,398.19
- Five-year components: $286,999.46 + $28,699.95 + 5 x $34,902.40 ($174,512.00) + 4 x $2,000.00 ($8,000.00) = $498,211.41

### Reconfirmation against the draft

All six headline figures equal the draft's figures (asserted in costing_final.py): initial $286,999.46; contingency $28,699.95; recurring $34,902.40; first year $350,601.81; remaining $149,398.19; five year $498,211.41. No price and no total changes.

Layout note: the three tables above carry exactly the draft's 22 initial lines, 11 recurring lines and 6 summary lines. The only changes are presentational: the initial table is grouped under Hardware / Software and licences / Services and labour with a subtotal for each (marking criterion 3.5 asks for hardware and software cost), and the recurring table gains a Calculation column. Row order inside the groups follows the draft.

### 1.3 Final non-price numbers (use these everywhere; CHANGED marks wording fixes for the verifier's warnings; no figure changes)

People and devices (case study and handout, unchanged):
- Original Brisbane office 40 staff: 5 executives, 5 managers, 5 customer service, 10 admin, 10 marketing, 3 HR, 2 IT. The expansion adds 30, giving 70 Brisbane staff, 35 per floor. Cairns 8 staff. Initial users 78 (70 + 8). Five-year planning: 108 Brisbane staff + 8 Cairns = 116 users, 38 more than today. Five-year department sizes used for growth: HR 10, Marketing 20, Customer Service 30.
- Five-year departmental end devices: 270 (Executives 30, Managers 40, Marketing 50, Customer Service 50, Admin 40, HR 20, IT 40). The forecast is taken to include each desk's phone.
- Department placement: Customer Service and IT on floor 1; Executives, Admin and HR on floor 2; Managers and Marketing on both floors.
- Existing cabling: 96 Cat 5e runs on floor 1 to the server-room patch panels; 120 Cat 6 runs on floor 2 plus two racks (one with patch panels, one empty); 216 runs in total. Timeframe four months. Budget $500,000.
- Existing equipment: two cross-linked 24-port Catalyst 2940 switches, 100 Mbps access ports, one 1 Gbps inter-switch uplink each; statically addressed PCs; analogue phones; 100BaseT PCs and servers; two extra Linux machines; one ADSL router; four servers (internal Web, HR-DB, Market-FS, CS-FS); Web server short of memory and disk; slow access to the other servers; no backups, redundancy or remote access; existing VLAN, firewall and RAID settings undocumented.

Ports and links:
- Brisbane access: 6 x C1300-48P-4X = 288 copper access ports, three per floor. 270 device ports + 6 AP ports = 276 used, 12 spare. Up to 60 extra horizontal runs (276 - 216). Each access switch has two 10 Gbps uplinks, one to each core (12 uplink links in total; each switch has four SFP+ slots, so two remain). PoE budgets: 48P-4X 375 W, 24P-4X 195 W.
- Cairns: 1 x C1300-24P-4X: 8 PCs + 8 phones + 1 AP = 17 ports used, 7 spare.
- CHANGED (wording, 4.1): each desk uses two access ports, PC on a 1 Gbps port and phone on its own PoE port; PCs are not daisy-chained through the phone's 100 Mbps passthrough port; the 270-device forecast already counts the phones, which is why 270 + 6 APs = 276 ports.
- CHANGED (wording, 6.1 core port allocation): each C1300-12XS has 12 usable 10 Gbps ports (10 SFP+ plus 2 combo copper/SFP+; the separate management port is not counted; the combo pairs share a port, so the count is 12, not 14). Per core: 6 access-switch uplinks + 2 host links (one from each host) + 1 NAS link + 2 core-to-core links + 1 firewall transit link = 12 of 12. Both cores are fully used; there is no spare core port. Any further 10 Gbps device uses the access switches' spare SFP+ slots or a third stack member.
- CHANGED (wording, state once in 6.5; sections 2 and 6.2 must match): each Dell R360 host has two 10 Gbps ports, one to each core, plus one onboard 1 GbE port to the DMZ switch. Both hosts get the DMZ port so the SMTP gateway replica can run on HYP-02.
- Firewall FW-HQ: directly behind the ISP handoff, in front of the core stack. One transit link to each core in VLAN 900 (192.168.254.0/29; firewall .1, core stack .2; the core default route points at .1). The DMZ switch hangs off FW-HQ (VLAN 100). Guest VLAN 90 and DMZ VLAN 100 gateways are on the firewall; every other Brisbane gateway is on the core stack. FW-BR at Cairns terminates the site-to-site VPN.
- Core interconnect: two 10 Gbps links between CORE 1 and CORE 2, run as a supported front-panel stack (same Family 2 PID), so the pair is one logical switch; department gateways on the stack.

Servers, storage and licences:
- 11 virtual machines: DC1, DC2, SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS, SRV-MAIL, SMTP-GW, SRV-MON, SRV-LOG, WLAN-CTRL. Six are Windows Server 2025 (DC1, DC2, SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS); five are Linux. Placement as the draft's 2.2 and 6.5 tables: DC1, SRV-WEB, SRV-HRDB, SMTP-GW on HYP-01; DC2, SRV-MKT-FS, SRV-CS-FS, SRV-MAIL, WLAN-CTRL on HYP-02; SRV-MON and SRV-LOG on opposite hosts. HYP-01 on floor 1, HYP-02 on floor 2.
- VM RAM: DC1 4, DC2 4, SRV-WEB 4, SRV-HRDB 16, SRV-MKT-FS 8, SRV-CS-FS 8, SRV-MAIL 8, SMTP-GW 2, SRV-MON 4, SRV-LOG 8, WLAN-CTRL 4 = 70 GB; fits one surviving 128 GB host.
- Hosts: eight-core processor, 128 GB ECC RAM, redundant power, separate resilient boot storage, 4 x 3.84 TB enterprise SSD in RAID 10 = 7.68 TB usable before filesystem overhead; 4 TB live-dataset planning envelope; each host holds its own live VMs plus replicas of the other host's. NAS: 6 x 8 TB in RAID 6, about 32 TB before overhead, plus four removable off-site targets; NAS is the backup target, never shared live-VM storage.
- Licensing: three 16-core Standard sets per host (each set covers two Windows guests) so either host can run all six Windows guests = 6 packs x $1,744.45 = $10,466.70; 78 User CALs x $109.45 = $8,537.10; physical host used only to run Hyper-V. One caveat sentence stays: OEM stacking entitlement and CAL type to be confirmed with the supplier before purchase.
- CHANGED (wording, 6.4): the 14 Defender servers add-on instances are the 11 virtual servers, the two Hyper-V hosts and one spare licence (the NAS cannot run the agent). 14 x 4.50 x 12 x 1.10 = $831.60. Combined Defender annual $4,633.20 + $831.60 = $5,464.80.
- Hyper-V Replica every 15 minutes; four-hour recovery-time target; manual, verified failover; application-consistent database backups still required; daily versioned NAS backups; encrypted off-site copies with a maximum one-business-day gap; quarterly restoration exercise; annual recovery rehearsal.

IP scheme (unchanged; all 18 VLAN rows verified, no overlaps, gateways on the first usable address, every static address inside its subnet and unique): VLAN 10 Executives 192.168.10.0/26 (30/62); 20 Managers 192.168.20.0/26 (40/62); 30 Marketing 192.168.30.0/25 (50/126); 40 Customer Service 192.168.40.0/25 (50/126); 50 Admin 192.168.50.0/26 (40/62); 60 HR 192.168.60.0/27 (20/30); 70 IT user devices 192.168.70.0/26 (40/62); 80 Brisbane voice 192.168.80.0/25 (108/126); 90 Brisbane guests 192.168.90.0/24 (100/254); 100 DMZ 192.168.100.0/27 (10/30); 110 Internal services 192.168.110.0/26 (30/62); 120 Device management 192.168.120.0/26 (40/62); 130 Backup/replication 192.168.130.0/27 (10/30, no gateway, non-routed); 140 Staff Wi-Fi 192.168.140.0/24 (150/254); 210 Cairns staff 10.20.10.0/26 (16/62); 220 Cairns management 10.20.20.0/27 (10/30); 280 Cairns voice 10.20.80.0/27 (8/30); 900 Core/firewall transit 192.168.254.0/29 (2/6). Usable hosts: /26 = 62, /25 = 126, /27 = 30, /24 = 254, /29 = 6. Static addresses exactly as the draft's 5.1 table (DC1 .110.10, DC2 .110.11, SRV-WEB .110.20, SRV-HRDB .110.21, SRV-MKT-FS .110.22, SRV-CS-FS .110.23, SRV-MAIL .110.24, SMTP-GW 192.168.100.10, SRV-MON .120.20, SRV-LOG .120.21, WLAN-CTRL .120.22, core SVI .120.1, FW-HQ management .120.4, HYP-01 .120.11, HYP-02 .120.12, NAS .120.30, PBX-01 192.168.80.10, access switches .120.41-.46, APs .120.51-.56, DMZ switch .120.47, Cairns switch/AP 10.20.20.2-.3, replication 192.168.130.11-.12, NAS backup 192.168.130.20, transit core .254.2 / firewall .254.1). DHCP as the draft's 5.2 (departmental /26 scopes .10-.62; HR .10-.30 = 21 addresses for 20 devices; /25 scopes .10-.126; voice .20-.126 plus reservations .11-.19 = 116 addresses for 108 phones; staff Wi-Fi .10-.254; guests from the firewall).

Bandwidth (unchanged): current average/peak Mbps: Web 60/100, HR-DB 40/80, Marketing FS 50/100, CS-FS 26/60, Email 25/80 (estimate), DHCP 20/50 (estimate), DC/DNS 40/90 (estimate), Monitoring 60/100 (estimate). Growth factors 108/40 = 2.70, HR 10/3 = 3.33 recurring, Marketing 20/10 = 2.00, Customer Service 30/5 = 6.00. Five-year peaks (peak x factor x 1.10, rounded up to the next 10 Mbps): Web 300, HR-DB 300, Marketing FS 220, CS-FS 400, Email 240, DHCP 150, DC/DNS 270, Monitoring 300; sum 2,180 Mbps; a 10 Gbps host path is about 4.6 times that; benchmark 1,000 Mbps per service (the 1 Gbps per-server allocation inside the 10 Gbps host uplink); busiest service CS-FS 400 Mbps. Worked examples: CS-FS 60 x 6.00 x 1.10 = 396 -> 400; Web 100 x 2.70 x 1.10 = 297 -> 300. Backup: 500 GB over 8 hours = 500 x 8,000 / 28,800 = about 139 Mbps, about 181 Mbps with 30% overhead. WAN allowance: 20 video sessions x 4 Mbps = 80 Mbps each way, 10 calls x 0.1 Mbps = 1 Mbps each way, plus 100 Mbps download / 50 Mbps upload other; CHANGED (addition): together about 181 Mbps download and 131 Mbps upload, inside the 1000/400 plan and its 875/339 Mbps typical busy-period speeds. Review triggers: interface 70%, CPU 70%, memory 80%, free storage 25%.

Budget headline numbers (unchanged from the draft): initial $286,999.46; contingency $28,699.95; first-year recurring $34,902.40; first-year funding requirement $350,601.81; remaining $149,398.19 of $500,000; five-year baseline $498,211.41; growth to 116 users adds $5,266.80 a year in Defender and Teams subscriptions. The $500,000 comparison is made for the first-year figure, as in the draft; do not write that the five-year figure is "within budget".

### 1.4 Cross-section statements that carry these numbers (each must read exactly as follows)

| Where | Final statement |
|---|---|
| Executive summary | "The first-year cost is $350,601.81, including a 10% implementation contingency and the first year of operating costs, which leaves $149,398.19 of the $500,000 budget." |
| 1 Gap analysis, people/time/budget row | "$350,601.81 in year one (initial $286,999.46 plus 10% contingency and $34,902.40 operating); $149,398.19 remains of $500,000." |
| 4.1 Port arithmetic | "6 x 48 = 288 ports; 270 devices + 6 APs = 276; 12 spare; 216 existing runs; up to 60 more runs; Cairns 24 ports, 17 used, 7 spare." |
| 6.1 | "$3,036.73 each including GST [R1, R2]"; port allocation sentence in section 2 of this file. |
| 6.2 | "$2,704.42 (C1300-48P-4X) and $2,003.43 (C1300-24P-4X), both including GST [R1, R3, R4]"; DMZ switch "listed at $1,578; I have allowed $1,750 [R30]". |
| 6.3 | "listed at $2,038 for the FG-70G-BDL-950-12 bundle; I have allowed $2,250 per site including GST, $4,500 for both [R5, R6]"; MFA "$2,500 setup and $500 a year". |
| 6.4 | "78 users at AU$4.50 = $4,633.20 a year; 14 server instances (the 11 virtual servers, the two Hyper-V hosts and one spare licence) = $831.60; $5,464.80 a year combined, including GST [R11]". |
| 6.5 hosts | "Dell lists the R360 from $6,047.97 including GST; I allow $18,000 per configured host including support [R7]"; "four 3.84 TB SSDs in RAID 10, about 7.68 TB". |
| 6.5 licensing | "six 16-core packs at $1,744.45 = $10,466.70 [R8, R9, R28]; 78 User CALs at $109.45 = $8,537.10 [R10]"; HR "$8,000 compatibility fund and $2,000 a year maintenance". |
| 6.5 backup storage | "RS2423RP+ diskless at $6,124.25 plus $6,000 for six 8 TB drives in RAID 6 (about 32 TB), rails and four removable off-site targets [R12, R13]". |
| 6.6 | "UCM6302 at $462 and 82 GRP2612P phones at $83 = $6,806 [R14, R15, R16]"; "Teams Essentials, 78 users at AU$6 per user per month excluding GST = $6,177.60 a year including GST [R17]"; "three MeetUp 2 at $1,599 = $4,797 [R18]"; "ten simultaneous external calls; $600 a month ($7,200 a year) allowance [P1, R25]". |
| 6.7 | "$0 licence [R21, R22, R29]; 90 days searchable, 12 months archived". |
| 6.8 | "seven EAP650 at $179 = $1,253 (six Brisbane, one Cairns) [R19, R20]". |
| 6.9 | Tables in 1.2; closing sentence "$5,266.80 a year" for 38 extra users. |
| 6.10 | "Business Assurance Ultrafast Plus 1000/400 at $160 a month ($1,920 a year); typical busy-period 875/339 Mbps; static IP; nbn Gold eSLA; FTTP [R24]"; "Cairns $120 a month ($1,440 a year) allowance". |
| 7.2 table | Values in 1.3 (unchanged); add the WAN total sentence. |
| 7.4 Conclusion | "The first-year cost of $350,601.81 sits within the $500,000 ceiling, with a four-month delivery schedule." |

---

## 2. Text changes by section

Each entry: what changes and the final wording of any number. Items not listed keep the draft's substance, reworded under the brief's voice rules (first person, no "X, not Y" disclaimers, no em dashes, no "proposal allowance").

**Cover and header**
- Add a title line: "Network Infrastructure Proposal for HelpYou Mortgage". Keep "Prepared by Roly Lobley", "Submitted to the Chief Information Officer, HelpYou Mortgage", "Date: 7 October 2026". Cover blanks: "Student number: ________" and "Assessment due date: ________". Running page header: name and title only.
- Delete the unnumbered "Proposal basis" section; one sentence in the executive summary covers the sources ([P1] case study, [P2] interview handout, [R1]-[R30] vendor and retail pages).

**Executive summary**
- First-year sentence as in 1.4. Everything else numeric unchanged (40 to 70 staff, 35 per floor, 8 Cairns, 108 staff and 270 devices over five years, four months, one ISP per site, two core links, firewall behind the ISP handoff).

**Contents**
- Regenerate; drop the page numbers copied from the .docx.

**Section 1 Gap Analysis**
- Delete the duplicate heading "# 1. Gap Analysis (continued)" (draft L92). ONE three-column organiser. Column headings: "Current infrastructure" / "Changes required" / "Future infrastructure HelpYou needs". One introductory sentence says the organiser covers both quantitative and qualitative differences.
- Keep 1.1 current conditions (numbers in 1.3) and drop its disclaimers.
- Eighteen rows, in this order, each carrying these figures (write them in first person; current column cites [P1]/[P2], changes column cites the [R#] shown):
  1. Firewall and perimeter security. Current: the case study lists one ADSL router and no firewall, IPS or DMZ; the Web, HR-DB, Market-FS and CS-FS servers share the same flat switches as every PC; existing firewall settings are undocumented [P1]. Changes: install a FortiGate 70G (FW-HQ) directly behind the Brisbane nbn handoff and in front of the two core switches, so every internet flow passes ISP -> firewall -> core stack; enable the FortiGuard UTP bundle (IPS/IDS, web filtering, antivirus) at the perimeter; create a DMZ zone (VLAN 100, 192.168.100.0/27) on a separate Cisco C1300-24T-4X switch for the SMTP gateway; terminate the guest VLAN 90 and the DMZ on the firewall; connect the core stack through the VLAN 900 transit (192.168.254.0/29); install a second FortiGate 70G (FW-BR) at Cairns for the site-to-site VPN; $2,250 per site in year one ($4,500) and $2,000 a year UTP renewals from year two [R5, R6]. Future: one inspected, logged boundary at each site; the mail relay isolated in the DMZ; guests and branch traffic reach only what the policy permits; the single firewall per site is an accepted residual risk.
  2. Switching (core and access). Current: two cross-linked 24-port Catalyst 2940 switches (48 ports) with 100 Mbps access ports and one 1 Gbps uplink each serve 40 PCs and four servers; staff report slow access [P1]. Changes: two Cisco C1300-12XS 10 Gbps core switches stacked over two interconnects ($6,073.46); six C1300-48P-4X PoE+ access switches, three per floor, 288 ports, two 10 Gbps uplinks each ($16,226.52); one C1300-24P-4X at Cairns ($2,003.43); 1 Gbps to every PC, PoE to every phone and AP [R1-R4]. Future: 288 Brisbane ports for 276 planned connections (270 devices plus 6 APs, 12 spare), 10 Gbps server and uplink paths, no single switch or uplink failure isolates a floor.
  3. Servers and virtualisation. Current: four physical servers (internal Web, HR-DB, Market-FS, CS-FS) on 100BaseT; the Web server is short of memory and disk and the others are slow; the handout's servers run Windows 2012 or Linux; two further Linux machines [P1, P2]. Changes: two Dell PowerEdge R360 hosts (eight cores, 128 GB RAM, four 3.84 TB SSDs in RAID 10 = 7.68 TB, two 10 Gbps ports), one per floor, running 11 virtual servers (70 GB RAM in total) with Hyper-V Replica every 15 minutes; $18,000 allowance per host [R7, R26]. Future: every service has sized CPU, memory and storage; either host can carry all services if the other fails; four-hour recovery target.
  4. Identity, DHCP and DNS. Current: every PC carries a static address; no domain, DHCP or DNS service is documented; HelpYou asks for centralised DHCP and DNS [P1, P2]. Changes: DC1 on HYP-01 (192.168.110.10) and DC2 on HYP-02 (192.168.110.11) running Windows Server 2025 AD DS, DNS and DHCP with replication and DHCP failover; one DHCP scope per VLAN with reservations for printers and phones; AD group permissions; 78 User CALs [R8-R10, R28]. Future: one login per person, central password and permission control, automatic addressing with no conflicts, domain services that survive the loss of one host.
  5. Monitoring and logging. Current: no monitoring; HelpYou asks for a dedicated management server and activity logs [P1, P2]. Changes: Zabbix on SRV-MON (192.168.120.20) polling every switch, firewall, host and server over SNMPv3 with thresholds (70% interface, 70% CPU, 80% memory, 25% free storage); Wazuh on SRV-LOG (192.168.120.21) collecting security events; 90 days searchable, 12 months archived; $0 licence [R21, R22, R29]. Future: faults and misuse detected before staff report them; an auditable record of who accessed what.
  6. Anti-virus and endpoint protection. Current: no managed endpoint protection is documented; desktops run mixed Windows versions [P1]. Changes: Microsoft Defender for Business for 78 users ($4,633.20 a year) and the servers add-on for 14 server instances ($831.60 a year), $5,464.80 combined; central alerts, tamper protection, scheduled patching; ASD Essential Eight as the baseline [R11, R27]. Future: every PC and server protected and patched under one console.
  7. Backup and recovery. Current: no backups and no redundancy of any kind [P1]. Changes: Synology RS2423RP+ NAS ($6,124.25) with six 8 TB drives in RAID 6 (about 32 TB) on the isolated backup VLAN 130; daily versioned backups; four removable encrypted off-site targets rotated weekly ($1,200 a year custody); quarterly restore tests; RAID 10 on the hosts and Hyper-V Replica between them [R12, R13, R26]. Future: deleted files, failed servers and whole-site loss are recoverable; off-site gap no more than one business day.
  8. Internet service. Current: one ADSL service with recurring disconnections [P1]. Changes: Aussie Broadband Business Assurance Ultrafast Plus 1000/400 (875/339 Mbps typical busy period), static IP, nbn Gold eSLA, $160 a month at Brisbane; $120 a month business plan allowance at Cairns [R24]. Future: stable internet for cloud services, Teams, VPN and email; one service per site, so an outage is an accepted residual risk.
  9. VPN and remote access. Current: no remote access for staff and no link to Cairns [P1]. Changes: site-to-site IPsec VPN between FW-BR and FW-HQ carrying only the permitted branch-to-server flows; remote-access VPN on FW-HQ with MFA ($2,500 setup, $500 a year) and role-based rules [R5]. Future: Cairns staff and authorised remote staff reach approved resources only.
  10. VLANs and segmentation. Current: one flat network with no VLANs documented; every PC can reach every server [P1]. Changes: 18 VLANs (departmental 10 to 70, voice 80, guest 90, DMZ 100, services 110, management 120, backup 130, staff Wi-Fi 140, Cairns 210/220/280, transit 900) with inter-VLAN rules on the core stack and firewall; subnets sized from the handout (for example Customer Service 50 devices in a /25). Future: HR data reachable only by HR and administrators; guests internet-only; management interfaces reachable only from IT devices.
  11. Wireless. Current: wireless for IT staff only; visitors cannot connect reliably [P1]. Changes: seven TP-Link EAP650 Wi-Fi 6 access points (six Brisbane, one Cairns; 7 x $179 = $1,253), WPA3-Enterprise/802.1X staff SSID on VLAN 140, isolated guest SSID on VLAN 90, controller on WLAN-CTRL, coverage survey before final positions [R19, R20]. Future: staff mobility on both floors; guest access that never touches company data.
  12. Voice and video. Current: analogue phones, expensive international calls, no videoconferencing [P1]. Changes: Grandstream UCM6302 PBX ($462) and 82 GRP2612P PoE phones ($6,806; 78 deployed, four spare) on voice VLANs 80 and 280; SIP trunk for ten simultaneous calls ($600 a month allowance); Teams Essentials for 78 users ($6,177.60 a year); three Logitech MeetUp 2 video bars ($4,797), two Brisbane rooms and one Cairns [R14-R18, R25]. Future: internal and branch calls over the LAN and VPN, cheaper external calls, meeting rooms with video.
  13. Email. Current: no email server among the four existing servers; HelpYou asks for one on its own infrastructure [P1]. Changes: SRV-MAIL (Ubuntu Server LTS, Postfix/Dovecot, 8 GB) in the services VLAN 110 and the SMTP-GW relay/filter (2 GB) in DMZ VLAN 100; mailboxes backed up to the NAS [R23]. Future: company-hosted email with filtering and recovery.
  14. File sharing. Current: staff keep files on their own PCs, so nothing is shared, protected or backed up; Linux machines need access too [P1]. Changes: SRV-MKT-FS and SRV-CS-FS (8 GB each) with SMB shares, AD group permissions and auditing; HR-DB kept separate (16 GB) with HR-only access; access from Windows and Linux clients [P1]. Future: central, backed-up files with need-to-know access from both platforms.
  15. Cabling and racks. Current: 96 Cat 5e runs on floor 1 to the server-room patch panels; 120 Cat 6 runs and two racks (one with patch panels, one empty) on floor 2; 216 runs in total [P1]. Changes: test and certify the 216 runs, relabel the patching, add up to 60 runs to reach 276 connections; floor-1 network rack (cores, FW-HQ, DMZ switch, PBX, three access switches, UPS) and server space (HYP-01); floor-2 racks (three access switches, HYP-02, NAS); Cairns cabinet; $6,000 cabling, $7,000 UPS and rack fit-out, $6,500 optics and accessories. Future: a documented, labelled two-floor layout with spare capacity.
  16. Capacity and growth. Current: 40 staff growing to 70 now (35 per floor) plus 8 at Cairns; servers already peak at their 100 Mbps interfaces (Web 100, Marketing 100, HR-DB 80, CS-FS 60 Mbps) [P1, P2]. Changes: size for 108 Brisbane staff and 270 devices over five years; five-year peaks Web 300, HR-DB 300, Marketing 220, CS-FS 400 Mbps against a 1 Gbps benchmark per service and 10 Gbps host paths; monthly capacity review with 70%/70%/80%/25% triggers. Future: five years of growth without re-cabling or replacing switches.
  17. Operating systems and licensing. Current: mixed Windows desktop versions, Linux machines and servers on Windows 2012 or Linux; licensing undocumented [P1, P2]. Changes: Windows Server 2025 Standard, six 16-core packs ($10,466.70) covering the six Windows guests on either host; 78 User CALs ($8,537.10); Ubuntu Server LTS for mail, monitoring and the wireless controller; endpoint fund 78 x $1,500 = $117,000 for standardised desktops; $8,000 HR application compatibility fund [R8-R10, R28]. Future: supported, licensed, patchable builds on every desktop and server.
  18. People, time and budget. Current: staff need account-software training; four months; $500,000 [P1]. Changes: four stages (discovery month 1, build and pilot month 2, migration month 3, acceptance month 4); 160 hours of labour ($24,000); $5,000 training and handover; first-year cost $350,601.81 including 10% contingency; $149,398.19 remains. Future: delivered within time and budget, with trained staff and CIO sign-off.
- Delete the sentence under the table ("Middle-column actions are proposed responses...").

**Section 2 Logical Topology**
- Delete the duplicate heading "# 2. Logical Topology (continued)" (L132).
- First paragraph must state the firewall placement plainly: "The Brisbane nbn handoff terminates on FW-HQ, a FortiGate 70G, which sits directly behind the ISP and in front of the two core switches; every flow to or from the internet, the DMZ, the guest network and Cairns passes through it before it reaches the core stack."
- Replace the INSERT paragraph (L130) with prose introducing Figure 2 (drawn logical topology diagram) and what it shows: ISP -> FW-HQ (IPS/IDS, VPN) -> core stack; the VLAN IDs and subnets from section 5; link speeds; the DMZ with SMTP-GW; DC1/DC2; SRV-MON (Zabbix SNMPv3); the two core links; the two hosts and the NAS; Cairns via VPN.
- Link table final wording:
  - "Brisbane ISP handoff -> FW-HQ": "One 1000/400 Mbps business nbn service; FW-HQ is the WAN, IPS/IDS and VPN boundary."
  - "FW-HQ -> core pair" (new row): "One 1 GbE transit link to each core in VLAN 900 (192.168.254.0/29); the core stack's default route points at 192.168.254.1."
  - "CORE 1 <-> CORE 2": "Two 10 Gbps links, run as a supported stack so the pair is one logical switch."
  - "Each access switch -> core pair": "Two 10 Gbps uplinks per switch, one to each core; 1 Gbps PC access ports; PoE ports for phones and APs."
  - "HYP-01 / HYP-02 -> core pair": "Two 10 Gbps links per host, one to each core, carrying the service, management and backup VLANs; a separate 1 GbE link from each host to the DMZ switch for the SMTP gateway."
  - "FW-HQ -> DMZ switch -> SMTP-GW": "Separate firewall zone (VLAN 100) for the mail relay."
  - "Cairns LAN -> FW-BR -> VPN -> FW-HQ": "One branch internet service and a site-to-site VPN; only the required branch-to-server flows are permitted."
- 2.1: keep the IPS/IDS at the perimeter statement positively; delete the "does not claim inspection of every internal LAN flow" clause.
- Packet Tracer truthfulness (section 4 of this file): the design has two core links and the firewall cabled to the cores; the topology file today draws one core link and the firewall cabled only to the ISP cloud. Either the student adds the cables before submission or the text says Figure 2 shows the design and the Packet Tracer file shows the devices and the first core link. Never write that the .pkt shows two core links or the firewall-to-core links.
- 2.2 table and Hyper-V Replica paragraph: numbers unchanged (15-minute interval, four-hour recovery target, quarterly restoration test, one-business-day off-site gap).
- 2.3: two plain sentences of residual risk (single firewall, ISP and PBX per site; two core links do not remove those).

**Section 3 Physical Topology**
- Figure 1 = the student's Packet Tracer floor-plan drawing from FLOOR_PLAN_FINAL.pkt (facts in section 4.1). Caption: "Figure 1. My Packet Tracer physical layout of the two Brisbane floors (first floor top, second floor bottom). Cisco 2960 icons stand in for the proposed Catalyst 1300 switches and the ASA icon for the FortiGate 70G." Drop [P4].
- Prose describes what the drawing shows (section 4.3 "May say") and the department placement from the handout (1.3).

**Section 4 Racks Diagram**
- Rack table unchanged (floor-1 network rack: patch panels, CORE 1, CORE 2, FW-HQ on a shelf, DMZ switch, PBX on a shelf, three floor-1 access switches, UPS; floor-1 server space: HYP-01; floor-2 patch-panel rack; floor-2 equipment rack: three access switches, HYP-02, NAS, UPS; Cairns cabinet: ISP handoff, FW-BR, access switch, UPS).
- Replace the INSERT paragraph (L179) with prose introducing Figure 3 (drawn rack elevation). Figure 4 (Packet Tracer rack view) only with the truthful caption in section 4.4; otherwise omit Figure 4.

**Section 4.1 Port and outlet provision**
- Numbers unchanged (1.4). Add: "Each desk uses two access ports, one for the PC and one for its phone; the 270-device forecast already counts the phones, which is why 270 devices plus six access points come to 276 ports."
- Citation plain "[P1, P2]". Delete the Cairns growth disclaimer sentence.

**Section 5 IP Scheme**
- Delete "Earlier departmental VLAN numbers are retained." Optional replacement: "VLAN numbers follow the department order 10 to 70, then 80 voice, 90 guest, 100 to 140 services, 210 to 280 Cairns and 900 transit."
- Delete the duplicate heading "# 5. IP Scheme (continued)" (L216).
- VLAN table, usable-range sentence, 5.1 static table and 5.2 DHCP text: unchanged (1.3).
- 5.1 gateway cells: core SVI row = "n/a (core SVI; default route via 192.168.254.1)"; FW-HQ management row = "n/a (firewall interface)".
- Delete the double-count sentence (L212) and the "not invented" clause (L214): "Public addresses come from the ISP."

**Section 6 introduction**
- One sentence: "Section 6.9 marks each line P (published retail price) or A (allowance), and the bibliography carries the link for every product." No date here (rule 3).

**6.1 Core Layer Switches**
- Price: "$3,036.73 each including GST [R1, R2]".
- Port sentence (final): "Each C1300-12XS has twelve usable 10 Gbps ports (ten SFP+ and two combo copper/SFP+ ports; each combo pair shares a port, so the count is twelve, not fourteen). On each core I allocate six access-switch uplinks, two host links, one NAS link, two core-to-core links and one firewall transit link, which uses all twelve ports. Any further 10 Gbps device would use the access switches' spare SFP+ slots or a third stack member."
- Keep: front-panel stacking (same Family 2 PID), one logical routing system, department gateways on the stack.

**6.2 Access Layer Switches**
- "$2,704.42 for the C1300-48P-4X and $2,003.43 for the C1300-24P-4X, both including GST [R1, R3, R4]."
- PoE: 48P-4X 375 W budget, 24P-4X 195 W, four 10G SFP+ uplinks each; PoE load assessed from the connected phones and APs.
- Delete the paragraph about Packet Tracer 2960 icons (L267); the substitution clause now lives in the Figure 1 caption.
- DMZ switch (final): "For the DMZ I propose a Cisco C1300-24T-4X, listed at $1,578; I have allowed $1,750 to cover shipping and quote variation [R30]. Each host's onboard 1 GbE port connects to this switch, so the SMTP gateway and its replica reach the DMZ through a dedicated virtual switch; the DMZ switch's management address sits in VLAN 120."

**6.3 Firewall**
- Final: "I propose one FortiGate 70G at each site with the UTP subscription and support. FW-HQ sits directly behind the Brisbane nbn handoff and in front of the core stack, and provides internet security, IPS/IDS, DMZ separation and VPN termination; FW-BR secures the branch and terminates its VPN. The FG-70G-BDL-950-12 bundle is listed at $2,038; I have allowed $2,250 per site including GST, $4,500 for both, pending configuration and quote [R5, R6]." No stock commentary.
- MFA: "$2,500 setup and $500 a year" unchanged. Keep: throughput to be checked with IPS/UTP inspection enabled; no separate router where the ISP presents an Ethernet handoff.

**6.4 Anti-Virus**
- Final: "Microsoft Defender for Business for the 78 users and the servers add-on for 14 server instances: the 11 virtual servers, the two Hyper-V hosts and one spare licence for a server added during the five-year period. At AU$4.50 per user or server per month excluding GST, that is $4,633.20 for users and $831.60 for servers, $5,464.80 a year including GST [R11]."
- Essential Eight: one positive sentence "I have used the ASD Essential Eight as the baseline for these controls [R27]."

**6.5 Servers**
- Hosts (final): "Two Dell PowerEdge R360 hosts, each with an eight-core processor, 128 GB ECC RAM, redundant power, separate resilient boot storage, four 3.84 TB enterprise SSDs in RAID 10 (about 7.68 TB before filesystem overhead), two 10 Gbps ports to the core pair and one onboard 1 GbE port to the DMZ switch. Dell lists the R360 from $6,047.97 including GST; I allow $18,000 per configured host including support, to be confirmed by quotation [R7]."
- One host per floor; 4 TB live-dataset envelope; a host holds its own live VMs plus replicas of the other host's; VM table and 70 GB total unchanged.
- Licensing (final): "The design has six Windows Server guests. I budget three 16-core Standard licence sets per host so either host can run all six during recovery: six packs at $1,744.45 = $10,466.70 [R8, R9, R28]. The 78 User CALs at $109.45 each total $8,537.10 [R10]. OEM stacking entitlement and CAL type are confirmed with the supplier before purchase."
- HR database: $8,000 compatibility/licence allowance and $2,000 a year maintenance, unchanged.
- Backup storage (final): "Synology RS2423RP+ 12-bay rackmount NAS with redundant power, diskless at $6,124.25 including GST, plus $6,000 for six 8 TB drives in RAID 6 (about 32 TB before overhead), rails and four removable off-site targets [R12, R13]."

**6.6 VoIP and Videoconferencing**
- Final: "One Grandstream UCM6302 IP PBX at $462 including GST and 82 GRP2612P phones at $83 each, $6,806 in total: 78 for current staff and four spares [R14, R15, R16]." Keep: phones have 100 Mbps ports so PCs use their own gigabit switch ports; PoE powers the phones.
- Teams: "Teams Essentials for 78 users at AU$6 per user per month excluding GST is $6,177.60 a year including GST [R17]."
- Video: "Three Logitech MeetUp 2 USB video bars at $1,599 each, $4,797 in total, two for Brisbane and one for Cairns [R18]."
- SIP: ten simultaneous external calls, $600 a month ($7,200 a year) allowance pending a Nexgen/Aussie Broadband quote [P1, R25].

**6.7 Network Monitoring**
- Unchanged: Zabbix on SRV-MON (SNMPv3, thresholds, alerts), Wazuh on SRV-LOG, $0 licence, 90 days searchable and 12 months archive [R21, R22, R29].

**6.8 Cross-Platform File Sharing and managed wireless**
- Unchanged: seven EAP650 (six Brisbane, one Cairns), 7 x $179 = $1,253 [R19, R20]; delete "the cited retailer currently reports no stock"; Ubuntu Server LTS with Postfix/Dovecot [R23]; one mention of the coverage survey.

**6.9 Total Costings**
- Use the three tables in 1.2 exactly. Delete the duplicate heading "## 6.9 Total Costings (continued)" (L367).
- Lead-in (final): "Amounts are AUD including GST. Lines marked P are the Australian retail listings I found on 7 October 2026; lines marked A are my allowances pending supplier quotes. Subscriptions published excluding GST are multiplied by 1.10. The ISP tariff is treated as GST-inclusive until the service summary confirms it."
- Endpoint-fund paragraph: keep the substance (ceiling for replacing or upgrading 78 workstations and room peripherals; reuse compatible equipment).
- Closing paragraph: "Five-year estimate = initial implementation + contingency + five years of the 78-user operating budget + four years of firewall renewals; it excludes inflation, electricity, extra staff, storage growth beyond the allowances and replacement equipment. Growing from 78 to 116 users (108 Brisbane plus 8 Cairns) adds 38 Defender and Teams subscriptions, $5,266.80 a year at these prices, plus devices."

**6.10 ISP Plan**
- Unchanged figures (1.4). One ISP per site; no mobile backup counted; one caveat that the page does not state the GST basis.

**Section 7**
- Delete the duplicate headings "# 7. Traffic Bandwidth Prediction (continued)" (L436) and "## 7.3 Five-year capacity (continued)" (L461). Section 7 title stays "Traffic Bandwidth Prediction and Expected Performance"; 7.3 stays "Five-year capacity and implementation".
- 7.1 and 7.2 tables unchanged (1.3). Citations plain "[P2]". Explain once that the 1,000 Mbps benchmark is the 1 Gbps per-server allocation inside the 10 Gbps host uplink.
- 7.2 add after the WAN allowances: "Together these come to about 181 Mbps download and 131 Mbps upload, well inside the 1000/400 Mbps plan and its 875/339 Mbps typical busy-period speeds."
- 7.3 four-stage table, review triggers and schedules unchanged. Delete L459.
- 7.4 Conclusion sentence as in 1.4.

**Section 8 Bibliography**
- Apply section 3. Preamble (one line): "Vendor and retail pages were accessed on 7 October 2026; the prices in section 6 are the listings found on that date. [P#] are the supplied assessment documents; [R#] are external sources."

---

## 3. Bibliography updates

Zero URL changes. Drop [P4]. Every [R#] entry is a clickable hyperlink. Titles stay as the draft wrote them (listed here so the rewriter does not retitle anything). Final list:

- [P1] TAFE Queensland. ICTNWK529_546_AT2_PE_TQM_v2: Portfolio of Evidence. HelpYou case study and task instructions. Supplied assessment document.
- [P2] TAFE Queensland. ICTNWK529_546_AT2_Student Handout 2_TQB_v1: HelpYou Mortgage Customer Interview Answers. Supplied assessment document.
- [P3] TAFE Queensland. ICTNWK529_546_AT2_MC_TQM_v2: Assessment Marking Criteria; and ICTNWK529_546_AT2_Template_SH_TQM_v2. Supplied assessment documents.
- [R1] Cisco. Catalyst 1300 and 1300X Series Switches: data sheet. https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-1300-series-switches/nb-06-cat1300-ser-data-sheet-cte-en.html
- [R2] The Telecom Shop. Cisco Catalyst C1300-12XS: Australian retail listing. https://www.thetelecomshop.com/au/cisco-catalyst-1300-12-port-sfp-2x10ge-shared-c1300-12xs
- [R3] PB Tech Australia. Cisco C1300-48P-4X: Australian retail listing. https://www.pbtech.com/au/product/SWHCIS0185/Cisco-Catalyst-1300-Switch-48-port-GE-PoE-4x10G-SF
- [R4] The Telecom Shop. Cisco C1300-24P-4X: Australian retail listing. https://www.thetelecomshop.com/au/cisco-catalyst-1300-24-port-ge-poe-managed-network-switch-c1300-24p-4x
- [R5] Fortinet. Next-Generation Firewall product information. https://www.fortinet.com/products/next-generation-firewall
- [R6] Technology Centre. FG-70G-BDL-950-12 hardware and one-year UTP bundle: reference listing. https://www.technologycentre.com.au/products/fortinet-fortigate-70g-hardware-plus-1-year-forticare-premium-and-fortiguard-unified-threat-protection-utp-2530043
- [R7] Dell Australia. PowerEdge R360 configuration and starting price. https://www.dell.com/en-au/shop/ipovw/poweredge-r360
- [R8] Techbuy. Windows Server 2025 Standard 16-core OEM pack EP2-25187: reference price. https://www.techbuy.com.au/p/553348/OPERATING_SYSTEMS_LICENCES/Microsoft/EP2-25187.asp
- [R9] Microsoft. Windows Server 2025 licensing and pricing. https://www.microsoft.com/en-au/windows-server/pricing
- [R10] Dell Australia. PowerEdge R450 configurator: Windows Server User CAL reference price. https://www.dell.com/en-au/shop/servers-storage-and-networking/poweredge-r450-rack-server/spd/poweredge-r450/per45020a
- [R11] Microsoft. Small and medium business security solutions pricing: Defender for Business and server add-on. https://www.microsoft.com/en-au/security/small-medium-business/pricing
- [R12] Synology. RackStation RS2423+ / RS2423RP+ product information. https://www.synology.com/en-global/products/RS2423%2B
- [R13] Techbuy. Synology RS2423RP+ diskless NAS: Australian retail listing. https://www.techbuy.com.au/p/529889/HARD_DRIVE_-_EXTERNAL_NAS_DRIVES/Synology/RS2423RP_.asp
- [R14] Grandstream. UCM6300 Series IP PBX product information. https://www.grandstream.com/products/ip-pbxs/ucm-series-ip-pbxs/product/ucm6300-series-ip-pbx
- [R15] Telrex. Grandstream UCM6302 IP PBX: Australian retail listing. https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users
- [R16] MyITHub. Grandstream GRP2612P IP phone: Australian retail listing. https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone
- [R17] Microsoft. Teams Essentials for Small Businesses: Australian pricing. https://www.microsoft.com/en-au/microsoft-teams/essentials
- [R18] Video Conferencing Australia. Logitech MeetUp 2: Australian retail listing. https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/
- [R19] TP-Link Australia. EAP650 V1.30 specifications. https://www.tp-link.com/au/business-networking/omada-wifi-ceiling-mount/eap650/v1.30/
- [R20] Umart. EAP650 access point: Australian retail listing. https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658
- [R21] Zabbix. On-premise platform and network monitoring. https://www.zabbix.com/network_monitoring
- [R22] Wazuh. Getting started: platform documentation. https://documentation.wazuh.com/current/getting-started/index.html
- [R23] Canonical. Ubuntu Server documentation: Mail services. https://ubuntu.com/server/docs/how-to/mail-services/
- [R24] Aussie Broadband. Business nbn plans, including Business Assurance Ultrafast Plus 1000/400. https://www.aussiebroadband.com.au/business/internet/nbn-plans/
- [R25] Aussie Broadband / Nexgen. SIP Trunks: quotation and service information. https://www.aussiebroadband.com.au/business/voice/sip-trunks/
- [R26] Microsoft Learn. Hyper-V Replica overview. https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-overview
- [R27] Australian Signals Directorate. Essential Eight maturity model. https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model
- [R28] Microsoft. Windows Server 2025 Licensing Guide. https://www.microsoft.com/licensing/docs/documents/download/Licensing_guide_PLT_Windows_Server_2025.pdf
- [R29] Zabbix. On-premise open-source deployment and licence-fee information. https://www.zabbix.com/
- [R30] i-Tech. Cisco C1300-24T-4X: reference listing for the DMZ switch. https://www.i-tech.com.au/c1300-24t-4x-cisco-c1300-24t-4x-catalyst-1300-24-port-ge-419371.html

Citation hygiene: every [R#] is cited at least once in the body (R1-R4 in 6.1/6.2 and the gap analysis; R5/R6 in 6.3 and the gap analysis; R7 in 6.5; R8-R10 and R28 in 6.5 licensing; R11 in 6.4; R12/R13 in 6.5 backup; R14-R16 in 6.6; R17/R18 in 6.6; R19/R20 in 6.8; R21/R22/R29 in 6.7; R23 in 6.8; R24 in 6.10; R25 in 6.6; R26 in 2.2; R27 in 6.4 and 7.3; R30 in 6.2). Normalise the annotated brackets to plain citations: "[P1, P2]" (4.1), "[R7]" (6.5), "[P2]" (7.2), "[R27]" (7.3). [R9] and [R28] are cited for licensing rules only.

---

## 4. Facts from the Packet Tracer files

Both files were decrypted and read from their XML (inventory_floorplan.md, inventory_topology.md). Sections 2 to 4 may use only what is listed here when describing the Packet Tracer work. Neither file contains any VLAN, IP address, hostname or firewall configuration entered by the student; both are connectivity drawings, which matches the agreed design-only scope. The IP scheme therefore rests on the report's own tables, never on the .pkt files.

### 4.1 FLOOR_PLAN_FINAL.pkt (Packet Tracer 8.2.1): the source of Figure 1

- The floor plan is the background image of Packet Tracer's Logical workspace (a 604 x 813 px JPEG, "BACKGROUND FOR FLOOR PLAN.png", embedded in the file). It is one floor plan duplicated vertically with different room labels: the top half is the first floor (Executive Room 1 and 2, Server Room) and the bottom half is the second floor (Meeting Room 1 and 2, Server Room). The student's screenshot (496 x 651 px, Figure 1) is this workspace at 0.75 scale. Call it "my Packet Tracer physical layout" or "physical view"; do not call it the Physical Workspace, and do not say cable lengths were measured.
- 31 devices on the plan (plus two off-plan power-distribution units that Packet Tracer auto-creates): four Cisco 2960-24TT switches (Switch0 and Switch1 in the second-floor Server Room; Switch2 and Switch3 in the first-floor Server Room), one Cisco ASA 5506-X named ASA0 (the firewall), one cloud named Cloud0 (the ISP), six Server-PT servers (WEB SERVER, DHCP + DNS, NET MONITOR SERVER, APP SERVER, Server0, Server2), 15 PCs (first floor: IT-1, IT-2, CUST-1, CUST-2, MGMT-2, MRKT-2; second floor: HR-1, HR-2, HR 1, ADMIN-1, ADMIN-2, EXEC-1, EXEC-2, MGMT-1, MRKT-1), two Home-VoIP phones (VoIP-2 first floor, VoIP-1 second floor), one laptop (Laptop0, first floor near the entry) and one lightweight access point named "Guest WiFi" (first-floor corridor).
- Department placement in the drawing matches the handout: IT and Customer Service on floor 1; HR, Admin and Executives on floor 2; Managers and Marketing on both floors (MGMT-2 and MRKT-2 on floor 1, MGMT-1 and MRKT-1 on floor 2). Each department is drawn as a sample of one or two PCs, not the full headcount.
- 32 copper links, all at Packet Tracer's default length. Eight are switch-to-switch: the two switches on each floor are cross-connected to the two on the other floor on all four Gigabit ports (Switch0 Gi0/1-Switch2 Gi0/1, Switch0 Gi0/2-Switch3 Gi0/1, Switch1 Gi0/1-Switch2 Gi0/2, Switch1 Gi0/2-Switch3 Gi0/2); two of those pairs are doubled on Fa0/24 (Switch0-Switch2, Switch1-Switch3); each floor pair has one horizontal link (Switch1 Fa0/5-Switch0 Fa0/1; Switch3 Fa0/3-Switch2 Fa0/2). This is a representative "two switches per floor, every switch reaches the other floor" drawing, not the final design's exact 2 core + 6 access layout.
- Firewall placement in this file: Cloud0 Ethernet6 connects to ASA0 Gi1/2 and ASA0 Gi1/1 connects to Switch1 Fa0/1, so the firewall sits between the ISP cloud and the second-floor switch (ISP -> firewall -> switch). This is the one place the Packet Tracer work already draws the firewall behind the ISP and in front of the switching.
- Servers: Server0, DHCP + DNS, APP SERVER and Server2 cable to Switch1 (second floor); WEB SERVER and NET MONITOR SERVER cable to Switch3 (first floor).
- Eleven of the sixteen PC/phone cables run to the switch on the other floor; five stay on their own floor. Treat this as "every desk patches back to a switch", not a cabling plan.
- Not cabled: Laptop0, Guest WiFi (no Ethernet link and no wireless clients), MRKT-1, and the two power-distribution units. HR 1 and HR-1 are two separate PCs almost on top of each other in the second-floor HR cubicle (a leftover duplicate).
- Five devices sit outside the floor-plan image (WEB SERVER and Server2 to the right, DHCP + DNS and NET MONITOR SERVER below, ASA0 at the bottom-right corner), which is the white space at the bottom right of the screenshot.
- Nothing is configured: every PC and server port is 0.0.0.0, the phones show self-assigned 169.254.x.x addresses, the switches and ASA carry factory configurations, VLAN 1 only, and the server "services" are Packet Tracer defaults (the DHCP and DNS services on the "DHCP + DNS" server are switched off). Device display names are the only labelling.
- Physical workspace: untouched Packet Tracer default (Intercity > Home City > Corporate Office > Main Wiring Closet). Packet Tracer auto-racked the switches, servers, ASA, cloud and AP into two default racks in creation order; no building, floor, rack or Cairns site was created. A rack-view screenshot from this file would show only that auto-filled default rack.
- A clean re-render of this file at 2475 x 3407 px exists at work/figures/fig1b_physical_layout_render.png (drawn from the .pkt coordinates, solid lines for straight-through cables and dashed for crossover). If it is used instead of the screenshot it must be captioned as redrawn from the Packet Tracer file.

### 4.2 Helpyou_Network_Topology.pkt (Packet Tracer 8.2.1): the logical topology drawing

- 31 devices: two Cisco 2960-24TT switches named CORE 1 and CORE 2; a generic six-port Packet Tracer switch named DMZ Switch; a Cisco ASA 5505 icon named "Firewall - FortiGate" (the file name uses an en dash; it is an ASA icon labelled as the FortiGate); a cloud named ISP-1 Cloud; four servers named for the existing roles (SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS); 21 PCs; one power-distribution unit.
- The PCs are samples of the original 40-staff office, named by department with ". . ." notes between them: Executive 5 (spelled "Excutive" in the file), Admin 4 (Admin-1, -5, -6, -10), Marketing 4 (Marketing-1, -5, -6, -10), Customer Service 2 (CS-1, CS-5), Managers 2 (Manager-1, -5), HR 2 (HR-1, HR-3), IT 2 (IT-1, IT-2). Coloured, labelled boxes group them: Executive Room 1 and 2, CS-Cube, Manager-Cube, Admin-Cube-1 and -2, HR-Cube, IT-Cube, Marketing-Cube-1 and -2, and a Server Room box around the four servers.
- 27 copper links. Exactly ONE core-to-core link (CORE 1 Gi0/1 to CORE 2 Gi0/1, crossover); Gi0/2 is free on both cores. The design calls for two core links: the report must not say the file shows two. SRV-WEB and SRV-HRDB cable to CORE 1 (Fa0/24, Fa0/23); SRV-MKT-FS and SRV-CS-FS to CORE 2 (Fa0/24, Fa0/23); ten PCs on CORE 1 and eleven on CORE 2, all on 100 Mbps FastEthernet ports.
- The firewall's only cable goes to ISP-1 Cloud (Ethernet6 to Ethernet0/0, the ASA's outside port). It is not cabled to either core, so this file does not yet draw ISP -> firewall -> core. The DMZ Switch has no cables at all. There are no access switches, domain controllers, hypervisors, PBX, access points, Cairns site or VPN in this file.
- Nothing is configured: no IP addresses (the only one present is the ASA 5505 factory default 192.168.1.1/24), VLAN 1 only, hostnames "Switch" and "ciscoasa".
- Physical workspace: default hierarchy only; one default rack holding, top to bottom, the power-distribution unit, CORE 1, CORE 2, DMZ Switch, SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS, the firewall and the ISP cloud (the cloud is racked as if it were equipment). The 21 PCs sit on the Corporate Office floor; Packet Tracer derived the 31 to 45 m cable lengths from those auto positions. No second floor, no Cairns.
- Recommended before submission (student's action, not the rewriters'): add the second core link (CORE 1 Gi0/2 to CORE 2 Gi0/2), cable the firewall's inside port to CORE 1 and CORE 2, and cable the DMZ Switch to the firewall, so the file matches Figure 2. Until that is done the text describes the file as it is.

### 4.3 What sections 2 to 4 may and may not say

May say:
- "My Packet Tracer physical layout (Figure 1) places two switches in each floor's server room, the firewall between the ISP cloud and the second-floor switches, the servers in the second-floor server room, sample PCs in each department's cubicles, a phone on each floor and the guest access point in the first-floor corridor."
- "My Packet Tracer topology file draws the two core switches with their first interconnect, the four existing servers, sample PCs for each of the seven departments, the DMZ switch, the firewall and the ISP cloud."
- "Cisco 2960 icons stand in for the Catalyst 1300 models and the ASA icon for the FortiGate 70G; the drawings show what connects to what, with copper cabling, and carry no configuration."

Must not say:
- that either file contains VLANs, subnets, IP addresses, trunks, routing, firewall rules, DHCP scopes or any CLI configuration;
- that the topology file shows two core-to-core links, the firewall cabled to the cores, or anything on the DMZ switch;
- that Figure 1 is a measured cable-route drawing, shows the Cairns site, shows six access switches, or was produced in the Physical Workspace;
- that a Packet Tracer rack view shows the proposed rack layout (the only rack views are Packet Tracer's auto-filled default racks).

### 4.4 Figure guidance

- Figure 1 (section 3): the student's screenshot, captioned "Figure 1. My Packet Tracer physical layout of the two Brisbane floors (first floor top, second floor bottom). Cisco 2960 icons stand in for the proposed Catalyst 1300 switches and the ASA icon for the FortiGate 70G."
- Figure 2 (section 2): drawn logical topology diagram showing, left to right or top to bottom, the ISP handoff (1000/400) -> FW-HQ (IPS/IDS, VPN) -> the VLAN 900 transit to the core stack; CORE 1 and CORE 2 with two 10 Gbps links; six access switches each with two 10 Gbps uplinks; HYP-01 and HYP-02 with two 10 Gbps links each and a 1 GbE link to the DMZ switch; the NAS; the DMZ switch with SMTP-GW (VLAN 100) hanging off FW-HQ; DC1/DC2; SRV-MON (Zabbix SNMPv3); the VLAN IDs and subnets from section 5; and Cairns (FW-BR, access switch, AP) over the site-to-site VPN. The firewall must be drawn between the ISP and the cores, never beside or below them.
- Figure 3 (section 4): drawn rack elevations matching the rack table (floor-1 network rack; floor-1 server space; floor-2 patch-panel rack; floor-2 equipment rack; Cairns cabinet).
- Figure 4 (section 4, optional): if a Packet Tracer rack view is included it must be the default rack from Helpyou_Network_Topology.pkt and captioned "Figure 4. Packet Tracer's default rack view of my topology file (CORE 1, CORE 2, DMZ switch, the four existing servers and the firewall); the proposed arrangement is Figure 3." Otherwise omit Figure 4.
