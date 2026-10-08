## 6.6 VoIP and Videoconferencing

The design uses one Grandstream UCM6302 IP PBX for the whole company. It sits on a shelf in the floor-1 network rack with a static address in the Brisbane voice VLAN (192.168.80.10), and it is priced at $462 including GST ([Telrex](https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users)) [R14, R15]. The desks get 82 Grandstream GRP2612P phones at $83 each ([MyITHub](https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone)), $6,806 in total: 78 for the current staff across both sites and four spares [R16]. Brisbane phones live in VLAN 80 and Cairns phones in VLAN 280, and the branch phones register to the Brisbane PBX across the site-to-site VPN, so a call between the two offices stays on HelpYou's own network.

Each phone draws PoE from its access switch, so each desk needs only the one cable and the UPS in each rack keeps the phones up through a power cut. The GRP2612P has a 100 Mbps port, which is ample for a voice call, so every PC keeps its own gigabit port on the access switch and the phone has its own PoE port beside it. A single on-premises SIP PBX with PoE handsets is the standard replacement for an analogue phone system in a two-site business of this size. The UCM6302 is sized for far more users than HelpYou will have in five years and carries two FXO ports, so an analogue line can stay in place for emergency calls if HelpYou wants one [R14].

For meetings, this proposal recommends Microsoft Teams Essentials for 78 users at AU$6 per user per month excluding GST ([Microsoft](https://www.microsoft.com/en-au/microsoft-teams/essentials)), which is $6,177.60 a year including GST [R17]. The meeting rooms get three Logitech MeetUp 2 USB video bars at $1,599 each ([Video Conferencing Australia](https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/)), $4,797 in total, two for the Brisbane meeting rooms and one for Cairns [R18]. Each MeetUp 2 plugs into a laptop or a small room PC over USB, so the rooms run as BYOD Teams rooms on whatever laptop staff bring in, and the endpoint and peripherals fund in section 6.9 covers a room display or PC where one is needed. A cloud meeting service with a USB room camera is the lowest-cost way to give a business of this size video that works with the outside world, because the people HelpYou meets already have a Teams or browser link and the service runs in Microsoft's cloud rather than on HelpYou's servers. Teams Essentials covers meetings, screen sharing and chat; external phone calls go through the PBX and the SIP trunk below.

For external calls, the budget allows for ten simultaneous calls on a SIP trunk, at $600 a month ($7,200 a year) for the trunk, the numbers and call charges ([Aussie Broadband](https://www.aussiebroadband.com.au/business/voice/sip-trunks/)), pending a quote from Aussie Broadband (Nexgen) and a review of HelpYou's recent call records [P1, R25]. Domestic and international rates, number porting and the emergency-calling arrangement are settled in that quote. The client brief names expensive international calls as a problem, and comparing the SIP rates against the current bills will put a figure on the saving before HelpYou signs.

## 6.7 Network Monitoring

The design uses Zabbix on SRV-MON (192.168.120.20) as the monitoring platform ([Zabbix](https://www.zabbix.com/network_monitoring)) [R21]. It polls every Catalyst 1300, both FortiGates, the two hosts, the NAS and every virtual server over SNMPv3 and its own agent, tracks service availability and resource use against thresholds, and alerts the IT team. Alongside it, Wazuh on SRV-LOG (192.168.120.21) collects security events from the firewalls, servers and endpoints and lets the IT team search and investigate them ([Wazuh](https://documentation.wazuh.com/current/getting-started/index.html)) [R22]. The two have different jobs: Zabbix answers whether a device is up and how busy it is, and Wazuh answers who did what and whether it was allowed. Both are open source and self-hosted, so their licence line in the budget is $0 ([Zabbix](https://www.zabbix.com/)) [R29]; the IT time, storage and external support behind them are budgeted separately in section 6.9.

Both servers sit in the management VLAN 120 and run on opposite hosts, so a host failure takes down at most one of them. HelpYou asked for a dedicated management server and activity logs, and this pair delivers both [P1, P2]. Industry practice is to poll with SNMPv3 rather than the older community-string versions, because version 3 authenticates and encrypts the polling traffic. The design enables it on every switch, firewall, host and the NAS, and only IT devices can reach the management VLAN.

The monitoring checks cover interface load and errors on every uplink and server port, CPU and memory on the hosts and virtual servers, free space and latency on the host SSDs and the NAS, backup-job and replication status, VPN reachability to Cairns, failed logons and firewall events. The alert thresholds match the review triggers in section 7.3: 70% sustained interface use, 70% CPU, 80% memory and less than 25% free storage. Every device takes its time from the domain controllers so the logs line up, log administration is limited to the IT staff, and high-priority alerts are reviewed each morning. This proposal recommends keeping 90 days of events readily searchable and 12 months in a protected archive, with the CIO to confirm those periods once the first month of measured event volume is in.

## 6.8 Cross-Platform File Sharing

The client brief asks for files that Windows and Linux users can share under need-to-know access. The two departmental file services stay as Windows servers, SRV-MKT-FS and SRV-CS-FS on HYP-02, each with 8 GB of memory and its own SMB shares. Windows PCs connect natively, and the Linux machines connect to the same shares over SMB with their domain credentials, so both platforms see one set of files under one set of permissions. SRV-HRDB stays on HYP-01 as a separate server, so the HR data keeps its own server, its own share and its own permission group, apart from the general business files. [P1]

Access follows job role through AD groups: a Marketing group on the Marketing shares, a Customer Service group on theirs, an HR-only group on the HR application, and IT administrators using separate admin accounts for administrative work. Changes to sensitive folders are audited to SRV-LOG, and this proposal recommends a permission review with each department manager every quarter. This is the standard way to deliver need-to-know access on a Windows domain, and it moves every business file off the staff PCs and onto servers that are backed up to the NAS each night.

### Company email

HelpYou asked for an email server inside its own infrastructure, so the design adds SRV-MAIL, an Ubuntu Server LTS virtual machine on HYP-02 running Postfix and Dovecot for the mailboxes, and SMTP-GW, a second Ubuntu VM on HYP-01 in the DMZ that relays and filters all inbound and outbound mail. Only SMTP-GW is reachable from the internet, and only on the mail ports the firewall policy opens; the mailbox server sits in the services VLAN behind it. The build follows Canonical's mail-services documentation ([Canonical](https://ubuntu.com/server/docs/how-to/mail-services/)), and Ubuntu Server is free to use [R23]. The month-2 pilot validates domain-account integration, anti-spam filtering, certificates, a mailbox restore from the NAS backup and the staff mail clients on Windows and Linux before any mailbox moves. This keeps HelpYou's email on HelpYou's own servers, as the business requested, with Teams used for meetings only.

### Managed wireless

The wireless design uses seven TP-Link EAP650 Wi-Fi 6 ceiling-mount access points, six across the two Brisbane floors and one at Cairns, at $179 each ([Umart](https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658)), $1,253 for the seven [R19, R20]. The EAP650 supports WPA3-Enterprise authentication against the domain, maps each SSID to its own VLAN and isolates guest clients from one another ([TP-Link](https://www.tp-link.com/au/business-networking/omada-wifi-ceiling-mount/eap650/v1.30/)) [R19]. Each AP takes PoE from its access switch and has a management address in VLAN 120.

The staff SSID authenticates each person with 802.1X against AD and lands on the staff Wi-Fi VLAN 140; the guest SSID lands on VLAN 90, whose gateway is the firewall, so visitors get rate-limited internet access only. WLAN-CTRL, the Omada software controller on HYP-02, manages all seven APs from one console. Wi-Fi 6 with WPA3-Enterprise and VLAN-mapped SSIDs is the current standard for office wireless, and it answers the two complaints in the client brief: wireless limited to IT staff, and visitors who struggled to connect. A coverage survey of both floors fixes the final AP positions before the cable runs are terminated.

## 6.9 Total Costings

Amounts are AUD including GST. Lines marked P are the Australian retail listings checked on 7 October 2026; lines marked A are allowances in this proposal pending supplier quotes. Each priced item name links to the retailer or vendor page the price came from, and section 8.1 lists the same pages. Subscriptions published excluding GST are multiplied by 1.10. The ISP tariff is treated as GST-inclusive until the service summary confirms it.

Table 8 lists every initial purchase and implementation cost, grouped into hardware, software and licences, and services and labour, with a subtotal for each group and a 10% contingency on the total.

| Initial item | Qty | Unit budget | Line total | Basis |
|---|---|---|---|---|
| [Core switches - Cisco C1300-12XS](https://www.thetelecomshop.com/au/cisco-catalyst-1300-12-port-sfp-2x10ge-shared-c1300-12xs) | 2 | $3,036.73 | $6,073.46 | P [R2] |
| [Head-office access - Cisco C1300-48P-4X](https://www.pbtech.com/au/product/SWHCIS0185/Cisco-Catalyst-1300-Switch-48-port-GE-PoE-4x10G-SF) | 6 | $2,704.42 | $16,226.52 | P [R3] |
| [Cairns access - Cisco C1300-24P-4X](https://www.thetelecomshop.com/au/cisco-catalyst-1300-24-port-ge-poe-managed-network-switch-c1300-24p-4x) | 1 | $2,003.43 | $2,003.43 | P [R4] |
| [DMZ switch - Cisco C1300-24T-4X](https://www.i-tech.com.au/c1300-24t-4x-cisco-c1300-24t-4x-catalyst-1300-24-port-ge-419371.html) | 1 | $1,750.00 | $1,750.00 | A [R30] |
| [FortiGate 70G + year-one UTP, one per site](https://www.technologycentre.com.au/products/fortinet-fortigate-70g-hardware-plus-1-year-forticare-premium-and-fortiguard-unified-threat-protection-utp-2530043) | 2 | $2,250.00 | $4,500.00 | A [R6] |
| [Dell R360 configured virtualisation hosts](https://www.dell.com/en-au/shop/ipovw/poweredge-r360) | 2 | $18,000.00 | $36,000.00 | A [R7] |
| [Synology RS2423RP+ diskless NAS](https://www.techbuy.com.au/p/529889/HARD_DRIVE_-_EXTERNAL_NAS_DRIVES/Synology/RS2423RP_.asp) | 1 | $6,124.25 | $6,124.25 | P [R13] |
| NAS drives, rails and backup media package | 1 | $6,000.00 | $6,000.00 | A |
| Head-office and branch UPS / rack fit-out | 1 | $7,000.00 | $7,000.00 | A |
| [TP-Link EAP650 access points](https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658) | 7 | $179.00 | $1,253.00 | P [R20] |
| [Grandstream UCM6302 IP PBX](https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users) | 1 | $462.00 | $462.00 | P [R15] |
| [GRP2612P phones (78 deployed, four spare)](https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone) | 82 | $83.00 | $6,806.00 | P [R16] |
| [Logitech MeetUp 2 (two Brisbane, one Cairns)](https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/) | 3 | $1,599.00 | $4,797.00 | P [R18] |
| Endpoint replacement / OS / peripherals fund | 78 | $1,500.00 | $117,000.00 | A |
| Compatible optics and connection accessories | 1 | $6,500.00 | $6,500.00 | A |
| Hardware subtotal | | | $222,495.66 | Calculated |
| [Windows Server 2025 Standard 16-core packs](https://www.techbuy.com.au/p/553348/OPERATING_SYSTEMS_LICENCES/Microsoft/EP2-25187.asp) | 6 | $1,744.45 | $10,466.70 | P [R8] |
| [Windows Server User CALs](https://www.dell.com/en-au/shop/servers-storage-and-networking/poweredge-r450-rack-server/spd/poweredge-r450/per45020a) | 78 | $109.45 | $8,537.10 | P [R10] |
| HR database/application compatibility fund | 1 | $8,000.00 | $8,000.00 | A |
| Remote-access MFA licensing / enrolment fund | 1 | $2,500.00 | $2,500.00 | A |
| Software and licences subtotal | | | $29,503.80 | Calculated |
| Cabling certification and extra outlets | 1 | $6,000.00 | $6,000.00 | A |
| Design, installation and migration labour (hours) | 160 | $150.00 | $24,000.00 | A |
| Staff and IT training / handover | 1 | $5,000.00 | $5,000.00 | A |
| Services and labour subtotal | | | $35,000.00 | Calculated |
| Initial procurement and implementation | | | $286,999.46 | Calculated |
| Contingency: 10% of the above | | | $28,699.95 | Calculated |

*Table 8. Initial procurement and implementation costs (AUD including GST).*

The endpoint fund is a ceiling for replacing or upgrading the 78 current user workstations and the meeting-room peripherals at $1,500 each; where a current PC meets the standard build it stays in service and that money stays unspent. The NAS drive package, the UPS and rack fit-out, the optics, the extra outlets and the HR application fund need site-specific quotes, so the budget carries them as allowances rather than leaving them out and understating the total.

Table 9 lists the recurring costs for the first year, with the calculation behind each subscription.

| Recurring item | Calculation | Annual cost | Basis |
|---|---|---|---|
| [Defender for Business: 78 users](https://www.microsoft.com/en-au/security/small-medium-business/pricing) | 78 x AU$4.50 x 12 x 1.10 | $4,633.20 | P [R11] |
| [Defender for Business servers add-on: 14 instances](https://www.microsoft.com/en-au/security/small-medium-business/pricing) | 14 x AU$4.50 x 12 x 1.10 | $831.60 | P [R11] |
| [Teams Essentials: 78 users](https://www.microsoft.com/en-au/microsoft-teams/essentials) | 78 x AU$6.00 x 12 x 1.10 | $6,177.60 | P [R17] |
| [Brisbane: Aussie Broadband Business Assurance Ultrafast Plus 1000/400](https://www.aussiebroadband.com.au/business/internet/nbn-plans/) | 12 x $160 | $1,920.00 | P [R24] |
| [Cairns internet service allowance](https://www.aussiebroadband.com.au/business/internet/nbn-plans/) | 12 x $120 | $1,440.00 | A [R24] |
| [SIP trunk, numbers and call allowance](https://www.aussiebroadband.com.au/business/voice/sip-trunks/) | 12 x $600 | $7,200.00 | A [R25] |
| Off-site backup custody / media rotation | allowance | $1,200.00 | A |
| External support, patches and restore tests | allowance | $9,000.00 | A |
| Business application maintenance allowance | allowance | $2,000.00 | A |
| MFA subscription / token renewal fund | allowance | $500.00 | A |
| [Zabbix](https://www.zabbix.com/), [Wazuh](https://documentation.wazuh.com/current/getting-started/index.html) and [Ubuntu](https://ubuntu.com/server/docs/how-to/mail-services/) licence fees | self-hosted open source | $0.00 | [R22], [R23], [R29] |
| Year-one operating total | | $34,902.40 | Calculated |
| Firewall UTP renewals, years 2 to 5 | 2 sites, allowance | $2,000.00 | A; year 1 is inside the bundle |

*Table 9. Recurring costs (annual, AUD including GST).*

Table 10 brings the two together against the $500,000 budget.

| Budget summary | AUD including GST |
|---|---|
| Initial implementation | $286,999.46 |
| Implementation contingency (10%) | $28,699.95 |
| First-year recurring costs | $34,902.40 |
| First-year funding requirement | $350,601.81 |
| Remaining against the $500,000 budget | $149,398.19 |
| Five-year baseline ownership estimate | $498,211.41 |

*Table 10. Budget summary (AUD including GST).*

The first-year requirement of $350,601.81 leaves $149,398.19 of the $500,000 HelpYou has set aside. The five-year estimate is the initial implementation plus contingency, five years of the 78-user operating budget and four years of firewall renewals; it excludes inflation, electricity, extra staff, storage growth beyond the allowances and replacement equipment. Growing from 78 to 116 users (108 Brisbane plus 8 Cairns) adds 38 Defender and Teams subscriptions, $5,266.80 a year at these prices, plus their devices.

## 6.10 ISP Plan

For Brisbane, this proposal recommends the Aussie Broadband Business Assurance Ultrafast Plus 1000/400 plan at $160 a month ([Aussie Broadband](https://www.aussiebroadband.com.au/business/internet/nbn-plans/)), $1,920 a year, with a static IP address and the nbn Gold eSLA for priority fault restoration [R24]. It is a 1000 Mbps download / 400 Mbps upload business nbn tier with typical busy-period speeds of 875/339 Mbps, and it needs FTTP at the address [R24]. The service hands off on Ethernet straight to FW-HQ in the floor-1 network rack. Section 7.2 puts HelpYou's WAN demand at about 181 Mbps down and 131 Mbps up, so the plan carries Teams, the Cairns VPN, email and cloud services with room to grow.

A business nbn tier of this kind, with a static IP and a service-level agreement on restoration, is the usual choice for an office of 70 people; it replaces the ADSL service that keeps dropping out and costs far less than dedicated symmetric fibre. Before ordering, the project team will confirm FTTP eligibility at the Brisbane address, the static-IP and reverse-DNS arrangement for the mail gateway, and the provider's policy on inbound mail. The plan page is silent on GST, so the budget treats the $160 as GST-inclusive until the service summary confirms it.

At Cairns, the budget allows $120 a month ($1,440 a year) for one business nbn service, to be chosen once the branch address is qualified. FW-BR terminates it in the Cairns cabinet and carries the site-to-site VPN to Brisbane. The design keeps one internet service at each site and leaves a second provider or mobile backup out, which is the trade-off set out in section 2.3: if the Brisbane service fails, Teams calls, the VPN and email wait until Aussie Broadband restores it, and the Gold eSLA is what keeps that wait short. If a chosen plan happens to include a mobile backup feature, it counts as a bonus rather than a designed second path.
