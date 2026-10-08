# 6. Investment of Hardware and Software

Each product below is listed with its make and model, its place in the design, the reason for its selection against industry practice, its price and a link to the retailer page. Section 6.9 marks each line P (published retail price) or A (allowance), and the bibliography lists every link again. The prices are current Australian retail listings, so each one will need a formal quote before HelpYou places an order.

## 6.1 Core Layer Switches

Two Cisco Catalyst C1300-12XS switches form the Brisbane core. They mount at the top of the floor-1 network rack, directly below the patch panels, with FW-HQ on the shelf beneath them. The price is $3,036.73 each including GST ([The Telecom Shop](https://www.thetelecomshop.com/au/cisco-catalyst-1300-12-port-sfp-2x10ge-shared-c1300-12xs)) [R1, R2].

Each C1300-12XS has twelve usable 10 Gbps ports (ten SFP+ and two combo copper/SFP+ ports; each combo pair shares a port, so the count is twelve rather than fourteen). Each core carries six access-switch uplinks, two host links, one NAS link, two core-to-core links and one firewall transit link, which uses all twelve ports. Any further 10 Gbps device would use the access switches' spare SFP+ slots or a third stack member.

Industry practice for an office of this size is a hierarchical design: a small, fast core that routes between VLANs, and a separate access layer that connects the desks. The C1300-12XS delivers that core at 10 Gbps for the price of a mid-range access switch. The two units stack over their front-panel ports, since both carry the same Catalyst 1300 Family 2 product ID, so the pair behaves as one logical switch and one routing system. Every departmental gateway is an interface on the stack, the inter-VLAN access rules are applied there, and administration is limited to the management VLAN. Keeping both cores in one rack is what allows the supported two-link stack; the loss of the whole stack or its rack is the residual risk accepted in section 2.3. [R1]

## 6.2 Access Layer Switches

The access layer uses six Cisco Catalyst C1300-48P-4X switches at Brisbane, three in the floor-1 network rack and three in the floor-2 equipment rack, and one C1300-24P-4X in the Cairns cabinet. The prices are $2,704.42 for the C1300-48P-4X ([PB Tech Australia](https://www.pbtech.com/au/product/SWHCIS0185/Cisco-Catalyst-1300-Switch-48-port-GE-PoE-4x10G-SF)) and $2,003.43 for the C1300-24P-4X ([The Telecom Shop](https://www.thetelecomshop.com/au/cisco-catalyst-1300-24-port-ge-poe-managed-network-switch-c1300-24p-4x)), both including GST [R1, R3, R4].

Each 48-port switch gives 1 Gbps to every desk and PoE+ to the phones and access points from a 375 W budget; the 24-port Cairns unit has a 195 W budget. All four SFP+ slots run at 10 Gbps. Two per switch carry the uplinks, one to each core, which leaves two spare. Three switches per floor give 288 Brisbane ports for the 276 connections in section 4.1, with 12 spare, and the Cairns switch has 17 of its 24 ports in use. The PoE assessment counts the phones and access points that are actually connected, since the raw port count would overstate the load.

This is the standard access-layer pattern: gigabit PoE at the desk, separate 10 Gbps uplinks to the core, and every desk two cable hops from any server. It retires the old 100 Mbps Catalyst 2940 ports from the production network. Staying in the same Catalyst 1300 family as the cores also gives the IT team one management interface and one firmware stream across every switch.

The DMZ uses a Cisco C1300-24T-4X, listed at $1,578 ([i-Tech](https://www.i-tech.com.au/c1300-24t-4x-cisco-c1300-24t-4x-catalyst-1300-24-port-ge-419371.html)); an allowance of $1,750 covers shipping and quote variation [R30]. It mounts in the floor-1 network rack beneath FW-HQ and connects to the firewall's DMZ interface, so the mail relay sits on its own physical switch and only the firewall policy decides what can reach it. Each host's onboard 1 GbE port connects to this switch, so the SMTP gateway and its replica reach the DMZ through a dedicated virtual switch; the DMZ switch's management address sits in VLAN 120.

## 6.3 Firewall

Each site receives one FortiGate 70G with the UTP subscription and support. FW-HQ sits directly behind the Brisbane nbn handoff and in front of the core stack, on a shelf in the floor-1 network rack, and provides internet security, IPS/IDS, DMZ separation and VPN termination; FW-BR sits in the Cairns cabinet, secures the branch and terminates its VPN. The FG-70G-BDL-950-12 bundle is listed at $2,038 ([Technology Centre](https://www.technologycentre.com.au/products/fortinet-fortigate-70g-hardware-plus-1-year-forticare-premium-and-fortiguard-unified-threat-protection-utp-2530043)); the budget allows $2,250 per site including GST, $4,500 for both, pending configuration and quote [R5, R6].

A next-generation firewall with intrusion prevention at the perimeter is the baseline control for any business on the internet, and the FortiGuard UTP bundle adds web filtering and antivirus to the IPS. Placing it between the ISP and the cores means every flow to or from the internet, the DMZ, the guest network and Cairns is inspected and logged before it touches the core stack, which is how the gap analysis and section 2 describe it. The 70G has enough interfaces for the WAN, the two transit links to the cores and the DMZ. Its throughput will be checked with IPS and UTP inspection enabled, because the headline forwarding figure drops once inspection is switched on. [R5]

Where Aussie Broadband presents an Ethernet handoff, the firewall terminates the service itself, so the design leaves out a separate router and the provider's termination equipment stays on the ISP side of FW-HQ. Remote access carries an allowance of $2,500 for setup and $500 a year for the MFA service, to be confirmed against the final user count and supplier. Every VPN logon is then a password plus a second factor, which is standard practice for remote access.

## 6.4 Anti-Virus

Microsoft Defender for Business covers the 78 users, and the servers add-on covers 14 server instances: the 11 virtual servers, the two Hyper-V hosts and one spare licence for a server added during the five-year period. At AU$4.50 per user or server per month excluding GST ([Microsoft](https://www.microsoft.com/en-au/security/small-medium-business/pricing)), that is $4,633.20 for users and $831.60 for servers, $5,464.80 a year including GST [R11].

The agent runs on every Brisbane and Cairns PC and on every Windows and Linux server, reporting to one console that the two IT staff manage. Defender for Business provides central alerts, tamper protection, automated investigation and scheduled patching from that console, which turns antivirus from a per-PC product into a managed service. Device eligibility is confirmed before deployment.

The ASD Essential Eight forms the baseline for these controls [R27]. Endpoint protection is one layer of it; least-privilege administration, controlled application settings, regular backups and MFA on remote access make up the rest, and each of those appears elsewhere in this design.

## 6.5 Servers

The server platform is two Dell PowerEdge R360 hosts, each with an eight-core processor, 128 GB ECC RAM, redundant power, separate resilient boot storage, four 3.84 TB enterprise SSDs in RAID 10 (about 7.68 TB before filesystem overhead), two 10 Gbps ports to the core pair and one onboard 1 GbE port to the DMZ switch. Dell lists the R360 from $6,047.97 including GST ([Dell Australia](https://www.dell.com/en-au/shop/ipovw/poweredge-r360)); the budget allows $18,000 per configured host including support, to be confirmed by quotation [R7].

HYP-01 sits in the floor-1 server rack beside the network rack and HYP-02 in the floor-2 equipment rack, so a fault that takes out one floor's rack leaves the other host running. Each host runs its own live VMs from its local RAID 10 SSDs and holds Hyper-V replicas of the other host's VMs, refreshed every 15 minutes [R26]. The planning envelope for the whole live dataset, mail and business files included, is 4 TB until the month-1 data inventory gives a measured figure. That leaves room on each host for its own VMs, the replicas and growth, and the monthly capacity review in section 7.3 triggers an upgrade before the tested storage or CPU envelope is reached.

Two virtualisation hosts with replicas is the usual way a business of this size gets server redundancy without a shared storage array or a cluster. It replaces four ageing physical servers on 100BaseT with 11 virtual servers on 10 Gbps paths, puts the second domain controller on its own hardware, and allows the IT team to rebuild or restore any one service without touching the others. The table below lists each virtual server, its memory and where it runs.

| Virtual service | Runs on | Initial RAM allowance | Operating system and purpose |
|---|---|---|---|
| DC1 and DC2 | HYP-01 / HYP-02 | 4 GB each | Windows Server 2025: AD DS, DNS, DHCP. |
| SRV-WEB | HYP-01 | 4 GB | Windows Server: existing internal web application, subject to compatibility. |
| SRV-HRDB | HYP-01 | 16 GB | Windows Server: existing HR database and application; database engine subject to vendor confirmation. |
| SRV-MKT-FS and SRV-CS-FS | HYP-02 | 8 GB each | Windows Server: department file services. |
| SRV-MAIL / SMTP-GW | HYP-02 / HYP-01 | 8 GB / 2 GB | Ubuntu Server LTS: Postfix/Dovecot mailbox service and the separate DMZ mail relay and filter. |
| SRV-MON / SRV-LOG / WLAN-CTRL | Opposite hosts / HYP-02 | 4 GB / 8 GB / 4 GB | Linux: monitoring, security events and the access-point controller. |

*Table 7. Virtual servers, memory allowances and host placement.*

The VM memory total is 70 GB. A surviving 128 GB host carries that allocation with room for the hypervisor, so either host can run all 11 services alone. CPU, storage latency and the HR application must still pass a degraded-operation test on one host before the build is signed off.

### Operating-system and application licensing

The design has six Windows Server guests: DC1, DC2, SRV-WEB, SRV-HRDB, SRV-MKT-FS and SRV-CS-FS. Each 16-core Standard licence set covers two Windows guests on a licensed host, and the physical host runs only Hyper-V, which is how Microsoft's licensing guide counts virtual machines. The budget includes three sets per host so either host can run all six during recovery: six packs at $1,744.45 ([Techbuy](https://www.techbuy.com.au/p/553348/OPERATING_SYSTEMS_LICENCES/Microsoft/EP2-25187.asp)) = $10,466.70 [R8, R9, R28].

The 78 User CALs at $109.45 each ([Dell Australia](https://www.dell.com/en-au/shop/servers-storage-and-networking/poweredge-r450-rack-server/spd/poweredge-r450/per45020a)) total $8,537.10 [R10]. A User CAL follows the person rather than the device, which suits staff who use a PC, a phone and Wi-Fi. OEM stacking entitlement and CAL type are confirmed with the supplier before purchase.

The client brief leaves the HR database engine and application licence unnamed, so the budget includes an $8,000 compatibility and licence fund and $2,000 a year for maintenance. The month-2 pilot confirms the engine and version with the vendor before any HR data moves.

### Backup storage

A Synology RS2423RP+ 12-bay rackmount NAS with redundant power serves as the backup target, priced diskless at $6,124.25 including GST ([Techbuy](https://www.techbuy.com.au/p/529889/HARD_DRIVE_-_EXTERNAL_NAS_DRIVES/Synology/RS2423RP_.asp)), plus $6,000 for six 8 TB drives in RAID 6 (about 32 TB before overhead), rails and four removable off-site targets [R12, R13]. It mounts in the floor-2 equipment rack beneath HYP-02 and connects to both cores, with its management address in VLAN 120 and its backup-data interface on the isolated backup VLAN 130.

This follows the 3-2-1 rule: at least three copies of the data (the live VM on its host, its replica on the other host and the NAS backup), on two kinds of storage (the hosts' SSDs and the NAS disk array), with one copy off site on the removable targets, which rotate weekly and stay encrypted. RAID 6 lets the array survive two failed drives, and the NAS holds backups only, while live VMs stay on each host's RAID 10 SSDs. NAS snapshots give a quick roll-back of a damaged file, the daily versioned backups give point-in-time restores, and the off-site copies cover the loss of the building. The selected drives are checked against Synology's compatibility list before ordering.
