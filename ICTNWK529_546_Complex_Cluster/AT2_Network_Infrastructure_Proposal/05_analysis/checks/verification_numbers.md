# Verification of numbers and internal consistency: HelpYou AT2 draft report

Source: /scratchpad/extract/report.md. Every value recomputed from scratch by verify_numbers.py (run with python3 -I). Status: OK = draft matches recomputation; ERROR = wrong number or contradiction that must change text; WARNING = questionable but defensible; INFO = fine but worth a note.

Checks: 199 total; 190 OK, 0 ERROR, 5 WARNING, 4 INFO.

Recomputed totals: initial $286,999.46, contingency $28,699.95, recurring $34,902.40, first-year $350,601.81, remaining $149,398.19, five-year $498,211.41.

| # | Section | Item | Draft value | Recomputed value | Status |
|---|---|---|---|---|---|
| 1 | 1.1 | Original Brisbane headcount (5+5+5+10+10+3+2) | 40 | 40 | OK |
| 2 | ES/1.1 | Brisbane after expansion (40 + 30) | 70 | 70 | OK |
| 3 | ES/3 | Two floors x 35 staff | 70 | 70 | OK |
| 4 | 6.4/6.6 | Initial users (70 Brisbane + 8 Cairns) | 78 | 78 | OK |
| 5 | 6.9 | Five-year org users (108 Brisbane + 8 Cairns) | 116 | 116 | OK |
| 6 | 6.9 | Extra users (116 - 78) | 38 | 38 | OK |
| 7 | 7.1 table | Original dept sizes used as growth denominators (HR 3, Mkt 10, CS 5) | 3 / 10 / 5 | 3 / 10 / 5 | OK |
| 8 | 5 vs ES/1.2/4.1 | Sum of departmental VLAN requirements = 270 devices | 270 | 270 | OK |
| 9 | 6.9 initial | Core switches C1300-12XS: 2 x $3,036.73 | $6,073.46 | $6,073.46 | OK |
| 10 | 6.9 initial | HQ access C1300-48P-4X: 6 x $2,704.42 | $16,226.52 | $16,226.52 | OK |
| 11 | 6.9 initial | Cairns access C1300-24P-4X: 1 x $2,003.43 | $2,003.43 | $2,003.43 | OK |
| 12 | 6.9 initial | DMZ switch C1300-24T-4X: 1 x $1,750.00 | $1,750.00 | $1,750.00 | OK |
| 13 | 6.9 initial | FortiGate 70G + UTP, one per site: 2 x $2,250.00 | $4,500.00 | $4,500.00 | OK |
| 14 | 6.9 initial | Dell R360 hosts: 2 x $18,000.00 | $36,000.00 | $36,000.00 | OK |
| 15 | 6.9 initial | Windows Server 2025 Std 16-core packs: 6 x $1,744.45 | $10,466.70 | $10,466.70 | OK |
| 16 | 6.9 initial | Windows Server User CALs: 78 x $109.45 | $8,537.10 | $8,537.10 | OK |
| 17 | 6.9 initial | Synology RS2423RP+ diskless: 1 x $6,124.25 | $6,124.25 | $6,124.25 | OK |
| 18 | 6.9 initial | NAS drives, rails, media: 1 x $6,000.00 | $6,000.00 | $6,000.00 | OK |
| 19 | 6.9 initial | UPS / rack fit-out: 1 x $7,000.00 | $7,000.00 | $7,000.00 | OK |
| 20 | 6.9 initial | TP-Link EAP650 APs: 7 x $179.00 | $1,253.00 | $1,253.00 | OK |
| 21 | 6.9 initial | Grandstream UCM6302 PBX: 1 x $462.00 | $462.00 | $462.00 | OK |
| 22 | 6.9 initial | GRP2612P phones: 82 x $83.00 | $6,806.00 | $6,806.00 | OK |
| 23 | 6.9 initial | Logitech MeetUp 2: 3 x $1,599.00 | $4,797.00 | $4,797.00 | OK |
| 24 | 6.9 initial | Endpoint fund: 78 x $1,500.00 | $117,000.00 | $117,000.00 | OK |
| 25 | 6.9 initial | Optics / accessories: 1 x $6,500.00 | $6,500.00 | $6,500.00 | OK |
| 26 | 6.9 initial | Cabling certification / outlets: 1 x $6,000.00 | $6,000.00 | $6,000.00 | OK |
| 27 | 6.9 initial | HR DB compatibility fund: 1 x $8,000.00 | $8,000.00 | $8,000.00 | OK |
| 28 | 6.9 initial | Labour (hours): 160 x $150.00 | $24,000.00 | $24,000.00 | OK |
| 29 | 6.9 initial | Training / handover: 1 x $5,000.00 | $5,000.00 | $5,000.00 | OK |
| 30 | 6.9 initial | MFA licensing / enrolment: 1 x $2,500.00 | $2,500.00 | $2,500.00 | OK |
| 31 | 6.9 initial | Initial procurement and implementation total | $286,999.46 | $286,999.46 | OK |
| 32 | 6.9 initial | Contingency 10% of initial (note: exact 28699.9460) | $28,699.95 | $28,699.95 | OK |
| 33 | 6.4/6.9 | Defender for Business 78 users: 78 x 4.50 x 12 x 1.10 | $4,633.20 | $4,633.20 | OK |
| 34 | 6.4/6.9 | Defender server add-on 14 instances: 14 x 4.50 x 12 x 1.10 | $831.60 | $831.60 | OK |
| 35 | 6.4 | Defender combined annual (users + servers) | $5,464.80 | $5,464.80 | OK |
| 36 | 6.6/6.9 | Teams Essentials 78 users: 78 x 6.00 x 12 x 1.10 | $6,177.60 | $6,177.60 | OK |
| 37 | 6.9/6.10 | Brisbane ISP 160 x 12 | $1,920.00 | $1,920.00 | OK |
| 38 | 6.9/6.10 | Cairns ISP allowance 120 x 12 | $1,440.00 | $1,440.00 | OK |
| 39 | 6.6/6.9 | SIP/call allowance 600 x 12 | $7,200.00 | $7,200.00 | OK |
| 40 | 6.9 recurring | Year-one operating total | $34,902.40 | $34,902.40 | OK |
| 41 | ES/6.9/7.4 | First-year funding requirement | $350,601.81 | $350,601.81 | OK |
| 42 | 6.9 | Remaining against $500,000 | $149,398.19 | $149,398.19 | OK |
| 43 | 6.9 | Five-year estimate = initial + contingency + 5 x recurring + 4 x $2,000 firewall renewals | $498,211.41 | $498,211.41 | OK |
| 44 | 6.9 | 38 extra users: 38 x (4.50 + 6.00) x 12 x 1.10 | $5,266.80 | $5,266.80 | OK |
| 45 | 6.1 vs 6.9 | Core switch unit price | $3,036.73 | $3,036.73 | OK |
| 46 | 6.2 vs 6.9 | 48P unit price / 24P unit price | $2,704.42 / $2,003.43 | $2,704.42 / $2,003.43 | OK |
| 47 | 6.2 vs 6.9 | DMZ switch allowance (listing $1,578) | $1,750.00 | $1,750.00 | OK |
| 48 | 6.3 vs 6.9 | FortiGate allowance per site (listing $2,038) | $2,250.00 | $2,250.00 | OK |
| 49 | 6.3 vs 6.9 | MFA setup / annual | $2,500 / $500 | $2,500 / $500 | OK |
| 50 | 6.5 vs 6.9 | Host allowance / NAS price / NAS package / HR DB fund / HR maint | $18,000 / $6,124.25 / $6,000 / $8,000 / $2,000 | $18,000 / $6,124.25 / $6,000 / $8,000 / $2,000 | OK |
| 51 | 6.6 vs 6.9 | PBX $462, phones 82 x $83, MeetUp 3 x $1,599 | match | match | OK |
| 52 | 6.8 vs 6.9 | APs 7 x $179 | $1,253.00 | $1,253.00 | OK |
| 53 | 6.6 | Phones purchased = 78 deployed + 4 spare | 82 | 82 | OK |
| 54 | 6.5 | 6 Windows Server packs x $1,744.45 | $10,466.70 | $10,466.70 | OK |
| 55 | 6.5 | 78 User CALs x $109.45 | $8,537.10 | $8,537.10 | OK |
| 56 | 6.5 | VM RAM total | 70 GB | 70 GB | OK |
| 57 | 6.5 | Windows Server guests (DC1, DC2, WEB, HRDB, MKT-FS, CS-FS) | 6 | 6 | OK |
| 58 | 6.5 | 3 x 16-core Standard sets per host cover 6 guests (2 OSEs per set) | 6 | 6 | OK |
| 59 | 6.5 | Packs = 3 per host x 2 hosts | 6 | 6 | OK |
| 60 | 2.2/6.5 | VM count in 2.2 and 6.5 tables | 11 | 11 | OK |
| 61 | 6.4/6.9 | Defender 'protected server instances' vs VM list (note: At 13 instances the add-on is $772.20/yr (-$59.40); recurring $34,843.00, first-year $350,542.41, remaining $149,457.59, five-year $497,914.41. Alternatively keep 14 and state the 14th is a spare licence.) | 14 | 11 VMs + 2 Hyper-V hosts = 13 (NAS cannot run the Defender agent) | WARNING |
| 62 | 6.5 | RAID 10 of 4 x 3.84 TB | 7.68 TB | 7.68 TB | OK |
| 63 | 6.5 | RAID 6 of 6 x 8 TB | about 32 TB | 32 TB | OK |
| 64 | 6.5 | 70 GB VMs fit a surviving 128 GB host | yes | yes | OK |
| 65 | 4.1 | 6 x 48 access ports | 288 | 288 | OK |
| 66 | 4.1 | 270 devices + 6 APs | 276 | 276 | OK |
| 67 | 4.1 | Spare access ports 288 - 276 | 12 | 12 | OK |
| 68 | 4.1 | Existing runs 96 + 120 | 216 | 216 | OK |
| 69 | 4.1 | Extra runs for 276 wired connections | 60 | 60 | OK |
| 70 | 4.1 | Cairns 24 - (8 PCs + 8 phones + 1 AP) | 7 | 7 | OK |
| 71 | 4.1/6.2 | Three switches per floor x two floors | 6 | 6 | OK |
| 72 | 5.1/6.2/6.8 | Access switches 1-6 and APs 1-6 in static table match 6 switches / 6 APs | 6 / 6 | 6 / 6 | OK |
| 73 | 6.8/6.9 | APs: 6 Brisbane + 1 Cairns | 7 | 7 | OK |
| 74 | 6.1 | Core ports listed in 6.1: 6 uplinks + 2 hosts + 1 NAS + 2 interlinks | 11 | 11 | OK |
| 75 | 2/6.1 | Core ports incl. firewall transit link (omitted from 6.1 list) (note: Zero spare per core; text should mention the firewall link and that the cores are fully used (or that the firewall is single-homed to one core).) | 12 ports 'suits' the listed uses (11) | 12 of 12 used if FW-HQ connects to each core | WARNING |
| 76 | 2/6.2 | Access-switch uplinks: 6 switches x 2 (one per core) vs 4 x 10G SFP+ on C1300-48P-4X | 12 total, 2 per switch | 12 total, 2 per switch (<= 4 available) | OK |
| 77 | 2/6.2/6.5 | Host NIC count: section 2 and 6.5 say two 10 Gbps interfaces; 6.2 adds a dedicated DMZ host interface (note: HYP-02 also needs a DMZ port if the SMTP-GW replica is to be activated there.) | 2 x 10G | 2 x 10G to cores + 1 extra port for the DMZ segment (3 ports; R360 onboard 1GbE can serve) | WARNING |
| 78 | 2/6.2/6.6 | PC access 1 Gbps vs phone 100 Mbps ports (note: Each staff member therefore uses two access ports; 270-device forecast is assumed to cover phones (4.1 says so).) | 1 Gbps PCs; 100 Mbps phones on separate ports | consistent, not a contradiction | INFO |
| 79 | 5 | VLAN 10 Executives 192.168.10.0/26: usable hosts | 62 | 62 | OK |
| 80 | 5 | VLAN 10 Executives: requirement 30 <= usable 62 | fits | fits | OK |
| 81 | 5 | VLAN 10 gateway is first usable (192.168.10.1) | 192.168.10.1 | 192.168.10.1 | OK |
| 82 | 5 | VLAN 20 Managers 192.168.20.0/26: usable hosts | 62 | 62 | OK |
| 83 | 5 | VLAN 20 Managers: requirement 40 <= usable 62 | fits | fits | OK |
| 84 | 5 | VLAN 20 gateway is first usable (192.168.20.1) | 192.168.20.1 | 192.168.20.1 | OK |
| 85 | 5 | VLAN 30 Marketing 192.168.30.0/25: usable hosts | 126 | 126 | OK |
| 86 | 5 | VLAN 30 Marketing: requirement 50 <= usable 126 | fits | fits | OK |
| 87 | 5 | VLAN 30 gateway is first usable (192.168.30.1) | 192.168.30.1 | 192.168.30.1 | OK |
| 88 | 5 | VLAN 40 Customer Service 192.168.40.0/25: usable hosts | 126 | 126 | OK |
| 89 | 5 | VLAN 40 Customer Service: requirement 50 <= usable 126 | fits | fits | OK |
| 90 | 5 | VLAN 40 gateway is first usable (192.168.40.1) | 192.168.40.1 | 192.168.40.1 | OK |
| 91 | 5 | VLAN 50 Admin 192.168.50.0/26: usable hosts | 62 | 62 | OK |
| 92 | 5 | VLAN 50 Admin: requirement 40 <= usable 62 | fits | fits | OK |
| 93 | 5 | VLAN 50 gateway is first usable (192.168.50.1) | 192.168.50.1 | 192.168.50.1 | OK |
| 94 | 5 | VLAN 60 HR 192.168.60.0/27: usable hosts | 30 | 30 | OK |
| 95 | 5 | VLAN 60 HR: requirement 20 <= usable 30 | fits | fits | OK |
| 96 | 5 | VLAN 60 gateway is first usable (192.168.60.1) | 192.168.60.1 | 192.168.60.1 | OK |
| 97 | 5 | VLAN 70 IT user devices 192.168.70.0/26: usable hosts | 62 | 62 | OK |
| 98 | 5 | VLAN 70 IT user devices: requirement 40 <= usable 62 | fits | fits | OK |
| 99 | 5 | VLAN 70 gateway is first usable (192.168.70.1) | 192.168.70.1 | 192.168.70.1 | OK |
| 100 | 5 | VLAN 80 Brisbane voice 192.168.80.0/25: usable hosts | 126 | 126 | OK |
| 101 | 5 | VLAN 80 Brisbane voice: requirement 108 <= usable 126 | fits | fits | OK |
| 102 | 5 | VLAN 80 gateway is first usable (192.168.80.1) | 192.168.80.1 | 192.168.80.1 | OK |
| 103 | 5 | VLAN 90 Brisbane guests 192.168.90.0/24: usable hosts | 254 | 254 | OK |
| 104 | 5 | VLAN 90 Brisbane guests: requirement 100 <= usable 254 | fits | fits | OK |
| 105 | 5 | VLAN 90 gateway is first usable (192.168.90.1) | 192.168.90.1 | 192.168.90.1 | OK |
| 106 | 5 | VLAN 100 DMZ 192.168.100.0/27: usable hosts | 30 | 30 | OK |
| 107 | 5 | VLAN 100 DMZ: requirement 10 <= usable 30 | fits | fits | OK |
| 108 | 5 | VLAN 100 gateway is first usable (192.168.100.1) | 192.168.100.1 | 192.168.100.1 | OK |
| 109 | 5 | VLAN 110 Internal services 192.168.110.0/26: usable hosts | 62 | 62 | OK |
| 110 | 5 | VLAN 110 Internal services: requirement 30 <= usable 62 | fits | fits | OK |
| 111 | 5 | VLAN 110 gateway is first usable (192.168.110.1) | 192.168.110.1 | 192.168.110.1 | OK |
| 112 | 5 | VLAN 120 Device management 192.168.120.0/26: usable hosts | 62 | 62 | OK |
| 113 | 5 | VLAN 120 Device management: requirement 40 <= usable 62 | fits | fits | OK |
| 114 | 5 | VLAN 120 gateway is first usable (192.168.120.1) | 192.168.120.1 | 192.168.120.1 | OK |
| 115 | 5 | VLAN 130 Backup / replication 192.168.130.0/27: usable hosts | 30 | 30 | OK |
| 116 | 5 | VLAN 130 Backup / replication: requirement 10 <= usable 30 | fits | fits | OK |
| 117 | 5 | VLAN 140 Staff Wi-Fi 192.168.140.0/24: usable hosts | 254 | 254 | OK |
| 118 | 5 | VLAN 140 Staff Wi-Fi: requirement 150 <= usable 254 | fits | fits | OK |
| 119 | 5 | VLAN 140 gateway is first usable (192.168.140.1) | 192.168.140.1 | 192.168.140.1 | OK |
| 120 | 5 | VLAN 210 Cairns staff 10.20.10.0/26: usable hosts | 62 | 62 | OK |
| 121 | 5 | VLAN 210 Cairns staff: requirement 16 <= usable 62 | fits | fits | OK |
| 122 | 5 | VLAN 210 gateway is first usable (10.20.10.1) | 10.20.10.1 | 10.20.10.1 | OK |
| 123 | 5 | VLAN 220 Cairns management 10.20.20.0/27: usable hosts | 30 | 30 | OK |
| 124 | 5 | VLAN 220 Cairns management: requirement 10 <= usable 30 | fits | fits | OK |
| 125 | 5 | VLAN 220 gateway is first usable (10.20.20.1) | 10.20.20.1 | 10.20.20.1 | OK |
| 126 | 5 | VLAN 280 Cairns voice 10.20.80.0/27: usable hosts | 30 | 30 | OK |
| 127 | 5 | VLAN 280 Cairns voice: requirement 8 <= usable 30 | fits | fits | OK |
| 128 | 5 | VLAN 280 gateway is first usable (10.20.80.1) | 10.20.80.1 | 10.20.80.1 | OK |
| 129 | 5 | VLAN 900 Core / firewall transit 192.168.254.0/29: usable hosts | 6 | 6 | OK |
| 130 | 5 | VLAN 900 Core / firewall transit: requirement 2 <= usable 6 | fits | fits | OK |
| 131 | 5 | VLAN 900 gateway is first usable (192.168.254.1) | 192.168.254.1 | 192.168.254.1 | OK |
| 132 | 5 | No overlapping subnets | none | none | OK |
| 133 | 5 | Usable-range sentence (/26 .1-.62, /25 .1-.126, /27 .1-.30, /24 .1-.254, /29 .1-.6) | as stated | 62 / 126 / 30 / 254 / 6 -> correct | OK |
| 134 | 5.2 | /26 scope .10-.62 size (after reserving .1-.9) | fits 40 | 53 addresses >= 40 | OK |
| 135 | 5.2 | HR /27 scope .10-.30 client addresses | 21 | 21 | OK |
| 136 | 5.2 | HR scope 21 >= 20 required | yes | yes | OK |
| 137 | 5.2 | /25 scope .10-.126 size >= 50 | fits | 117 >= 50 | OK |
| 138 | 5.2 | Voice DHCP .20-.126 + reservations .11-.19 vs 108 phones (PBX on .10) | sufficient | 107 + 9 = 116 >= 108 (DHCP alone 107 < 108, so reservation block is needed) | OK |
| 139 | 5.2 | Staff Wi-Fi .10-.254 >= 150 | fits | 245 >= 150 | OK |
| 140 | 5.1 | VLAN 110 static addresses (7) inside subnet, unique | inside/unique | inside/unique | OK |
| 141 | 5.1 | VLAN 100 static addresses (1) inside subnet, unique | inside/unique | inside/unique | OK |
| 142 | 5.1 | VLAN 120 static addresses (21) inside subnet, unique | inside/unique | inside/unique | OK |
| 143 | 5.1 | VLAN 80 static addresses (1) inside subnet, unique | inside/unique | inside/unique | OK |
| 144 | 5.1 | VLAN 220 static addresses (2) inside subnet, unique | inside/unique | inside/unique | OK |
| 145 | 5.1 | VLAN 130 static addresses (3) inside subnet, unique | inside/unique | inside/unique | OK |
| 146 | 5.1 | VLAN 900 static addresses (2) inside subnet, unique | inside/unique | inside/unique | OK |
| 147 | 5.1 vs 5 | VLAN 120 addresses used (21) <= 40 allowed | <= 40 | 21 <= 40 | OK |
| 148 | 5.1 vs 5 | VLAN 110 addresses used (7) <= 30 allowed | <= 30 | 7 <= 30 | OK |
| 149 | 5 vs 5.1 | VLAN 130 has no gateway in both places | None / None | None / None | OK |
| 150 | 5 vs 5.1 | DMZ gateway on firewall = SMTP-GW default gateway | 192.168.100.1 | 192.168.100.1 | OK |
| 151 | 5 vs 5.1 | Transit: core .2, firewall .1, core default route via .1 | consistent | consistent | OK |
| 152 | 5.2 vs 5.1 | DHCP scopes start at .10 but PBX-01 is .10 in VLAN 80 (voice scope starts .20) | no clash | no clash | OK |
| 153 | 5.2 vs 5.1 | /26 scopes start at .10, but VLAN 110 and 120 statics use .10+ (110.10, 120.11...) (note: Defensible; the sentence 'Management, servers, backup and transit addresses above are excluded from DHCP' already covers it.) | servers/management 'excluded from DHCP' | VLAN 110/120 are not departmental, so no DHCP scope applies; fine as written | WARNING |
| 154 | 7.1 | Growth factor all staff 108/40 | 2.70 | 2.70 | OK |
| 155 | 7.1 | Growth factor HR 10/3 | 3.33 recurring | 3.3333 | OK |
| 156 | 7.1 | Growth factor Marketing 20/10 | 2.00 | 2.00 | OK |
| 157 | 7.1 | Growth factor CS 30/5 | 6.00 | 6.00 | OK |
| 158 | 7.2 | Web: 100 x 2.7000 x 1.10 = 297.00 -> next 10 | 300 | 300 | OK |
| 159 | 7.2 | HR-DB: 80 x 3.3333 x 1.10 = 293.33 -> next 10 | 300 | 300 | OK |
| 160 | 7.2 | Marketing FS: 100 x 2.0000 x 1.10 = 220.00 -> next 10 | 220 | 220 | OK |
| 161 | 7.2 | CS-FS: 60 x 6.0000 x 1.10 = 396.00 -> next 10 | 400 | 400 | OK |
| 162 | 7.2 | Email: 80 x 2.7000 x 1.10 = 237.60 -> next 10 | 240 | 240 | OK |
| 163 | 7.2 | DHCP: 50 x 2.7000 x 1.10 = 148.50 -> next 10 | 150 | 150 | OK |
| 164 | 7.2 | DC/DNS: 90 x 2.7000 x 1.10 = 267.30 -> next 10 | 270 | 270 | OK |
| 165 | 7.2 | Monitoring: 100 x 2.7000 x 1.10 = 297.00 -> next 10 | 300 | 300 | OK |
| 166 | 7.2 | Sum of 5-year peaks | 2180 | 2180 | OK |
| 167 | 7.2 | 10 Gbps / 2,180 Mbps | about 4.6 x | 4.59 x | OK |
| 168 | 7.2 | Busiest forecast is CS-FS 400 < 1,000 benchmark | yes | yes | OK |
| 169 | 7.2 | Worked example CS-FS 60 x 6 x 1.10 | 396 -> 400 | 396 -> 400 | OK |
| 170 | 7.2 | Worked example Web 100 x 2.7 x 1.10 | 297 -> 300 | 297 -> 300 | OK |
| 171 | 7.1 vs 7.2 | 7.1 prose peaks (Web 100, Mkt 100, HR-DB 80, CS-FS 60) match table | match | match | OK |
| 172 | 7.2 backup | 500 GB x 8,000 / 28,800 s | approx 139 Mbps | 138.9 Mbps | OK |
| 173 | 7.2 backup | +30% overhead | about 181 Mbps | 180.6 Mbps | OK |
| 174 | 7.2 WAN | 20 video x 4 Mbps | 80 Mbps | 80 Mbps | OK |
| 175 | 7.2 WAN | 10 calls x 0.1 Mbps | 1 Mbps | 1 Mbps | OK |
| 176 | 7.2 WAN vs 6.10 | WAN allowance total vs 1000/400 plan (busy 875/339) | not summed in draft | 181 down / 131 up Mbps -> fits comfortably | INFO |
| 177 | 6.6 vs 7.2 | Ten simultaneous external calls in both sections | 10 | 10 | OK |
| 178 | ES | 'section 6.9' = Total Costings | 6.9 | 6.9 Total Costings | OK |
| 179 | 2 | 'section 5' = IP Scheme | 5 | 5 IP Scheme | OK |
| 180 | 3 | 'section 6' = Investment quantities | 6 | 6 Investment of Hardware and Software | OK |
| 181 | 6.2 | 'section 4.1' = Port and outlet provision | 4.1 | 4.1 Port and outlet provision | OK |
| 182 | 6 intro | 'Section 6.9' = Total Costings | 6.9 | 6.9 Total Costings | OK |
| 183 | 3 | Figure 1 = Packet Tracer two-floor overlay (only figure in draft) | Figure 1 | Figure 1 | OK |
| 184 | 2/4 | INSERT placeholders -> Figure 2 (logical), Figure 3 (rack), Figure 4 (PT rack view) | INSERT: ... | to be introduced in prose per brief rule 8 | INFO |
| 185 | headings | Duplicate '(continued)' headings: '# 1. Gap Analysis (continued)', '# 2. ... (continued)', '# 5. ... (continued)', '## 6.9 ... (continued)', '# 7. ... (continued)', '## 7.3 ... (continued)' (note: Two '7.3' headings and the '7. Traffic Bandwidth Prediction (continued)' heading drops the 'and Expected Performance' title.) | 6 duplicate headings (docx page-break artefacts) | remove; keep one heading per section | WARNING |
| 186 | Contents vs body | Section titles in Contents match body headings (1-8, 6.1-6.10, 7.1-7.4) | match | match | OK |
| 187 | Bibliography | All [R1]-[R30] cited in body at least once; [P4] to be dropped per brief | 30 cited | 30 cited | OK |
| 188 | 5 | 'Earlier departmental VLAN numbers are retained' refers to a prior draft | sentence present | drop in rebuild | INFO |
| 189 | 2.2 vs 6.5 | SMTP-GW on HYP-01, SRV-MAIL on HYP-02 in both | HYP-02 / HYP-01 | HYP-02 / HYP-01 | OK |
| 190 | 4 vs 6.5 | HYP-01 floor 1, HYP-02 floor 2 = 'one host on each floor' | consistent | consistent | OK |
| 191 | 4 vs 6.2 | Rack table: floor-1 access switches + three floor-2 access switches = 6 | 6 | 6 | OK |
| 192 | ES vs 2 vs 6.1 | Two core links / two 10 Gbps interconnections / front-panel stack | consistent | consistent | OK |
| 193 | ES vs 6.10 vs 2 | One ISP per site; Brisbane 1000/400 | consistent | consistent | OK |
| 194 | 6.6 vs 6.9 | Teams Essentials annual in prose = table | $6,177.60 | $6,177.60 | OK |
| 195 | 6.4 vs 6.9 | Defender combined in prose = table rows sum | $5,464.80 | $5,464.80 | OK |
| 196 | ES vs 7.4 | First-year budget stated identically | $350,601.81 | $350,601.81 | OK |
| 197 | 6.9 | Firewall renewals $2,000/yr for 4 years in five-year estimate | $8,000.00 | $8,000.00 | OK |
| 198 | 6.5 | Storage: each host holds its own live VMs + replicas of the other (4 TB envelope) <= 7.68 TB | fits | 4 TB <= 7.68 TB | OK |
| 199 | 6.5 | Licensing minimum 16 cores/host with 8-core CPU | 16-core packs | 16-core packs (Microsoft minimum) | OK |
