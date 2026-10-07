ICTNWK529 - Install and manage complex ICT networks  
ICTNWK546 - Manage network security  
Complex Cluster \| Assessment Task 2 of 3

Prepared by Roly Lobley  
Submitted to the Chief Information Officer, HelpYou Mortgage  
Date: 7 October 2026

Student number: \[insert\] Assessment due date: \[insert\]

# Executive summary

HelpYou requires a secure network for its Brisbane expansion from 40 to 70 staff, with 35 people on each floor, and connectivity for eight Cairns staff. The five-year departmental estimates total 108 head-office staff and 270 end devices. This proposal replaces the capacity-limited network with segmented access, two core switches, centralised services, protected backups and managed communications. The implementation is staged over four months. \[P1, P2\]

The design retains one internet service at each site, rather than dual internet providers. Brisbane uses two links between its core switches. Separate domain controllers provide service redundancy; two virtualisation hosts and recoverable replicas protect the business applications. A single firewall and internet service remain recognised points of failure at each site. These are design choices, not claims of continuous availability.

The first-year budget is \$350,601.81, including a 10% implementation contingency and operating costs, against the case-study ceiling of \$500,000. Published reference prices and proposal allowances are separated in section 6.9; supplier configuration and availability must be confirmed before purchase. \[P1\]

The following report contains the proposed design and calculations. It does not claim that the network has been configured, tested or installed.

# Contents

1\. Gap Analysis 3

2\. Logical Topology 5

3\. Physical Topology 7

4\. Racks Diagram 8

5\. IP Scheme 9

6\. Investment of Hardware and Software 11

6.1 Core Layer Switches 11

6.2 Access Layer Switches 11

6.3 Firewall 11

6.4 Anti-Virus 11

6.5 Servers 12

6.6 VoIP and Videoconferencing 13

6.7 Network Monitoring 13

6.8 Cross-Platform File Sharing 13

6.9 Total Costings 14

6.10 ISP Plan 15

7\. Traffic Bandwidth Prediction and Expected Performance 16

7.1 Existing performance and prediction method 16

7.2 Bandwidth calculations 16

7.3 Five-year capacity and implementation 17

7.4 Conclusion 18

8\. Bibliography 19

## Proposal basis

Existing conditions and business requirements are drawn from the HelpYou case study \[P1\]. Departmental location, headcount and bandwidth inputs come from the customer interview handout \[P2\]. Equipment selections, recovery targets, subnet allocations and workload forecasts are proposed engineering decisions. They are not reported measurements or additional customer instructions. Vendor sources \[R1-R30\] support the selected capabilities and reference prices.

# 1. Gap Analysis

## 1.1 Current conditions

The original Brisbane office accommodated 40 staff: five executives, five managers, five customer-service staff, ten administrative staff, ten marketing staff, three HR staff and two IT staff. The case study then adds 30 Brisbane staff, giving 70 across two floors; Cairns has eight. These are separate stages, not competing totals. \[P1\]

The existing equipment is described as two cross-linked, 24-port Catalyst 2940 switches with 100 Mbps access ports and one 1 Gbps inter-switch uplink each. Each staff member has a statically addressed PC and an analogue phone. PCs and servers have 100BaseT interfaces; two additional Linux machines are present. There is an ADSL router and four service servers: internal Web, HR-DB, Market-FS and CS-FS. \[P1\]

The first floor already has 96 Cat 5e runs to its server-room patch panels. The new floor has 120 Cat 6 runs and two racks, one containing patch panels and one empty. These existing assets should be assessed for reuse rather than described as absent. The Web server reports insufficient memory and disk space; users report slow access to other servers. Backups, redundancy and remote access are expressly absent. The precise existing VLAN, firewall and disk-RAID configurations are not documented. \[P1\]

## 1.2 Current system -\> changes -\> required future state

| **Current system - left**                                                                             | **Changes required - middle**                                                                                                   | **Business need / proposed system - right**                                                                            |
|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| Capacity: 40 original Brisbane users, expanding to 70, plus eight Cairns users.                       | Size the design for 108 Brisbane staff and 270 departmental devices over five years; retain separate branch capacity.           | An expandable network supporting the immediate two-floor move and the documented five-year demand. \[P1, P2\]          |
| Access network: 100 Mbps interfaces and two 24-port switches. Staff report slow responses.            | Replace access switching; provide 1 Gbps PC access and higher-capacity core/server connections.                                 | Enough LAN capacity for shared files, applications and communication without relying on the old 100 Mbps paths.        |
| Cabling and space: 96 existing first-floor runs; 120 on the upper floor; upper-floor racks available. | Certify existing runs, relabel patching, reuse compliant infrastructure and add outlets only where the port plan requires them. | A documented two-floor physical layout that uses existing facilities and leaves expansion space.                       |
| Internet: one unreliable ADSL service, with recurring disconnections.                                 | Replace ADSL with a business service, static addressing and a stated support/restoration arrangement.                           | Stable access to cloud services and branch resources; the residual risk of one service remains explicit.               |
| Remote access: no facility for remote staff or convenient branch access.                              | Provide a Cairns site-to-site VPN and authenticated remote access with MFA and role-based access limits.                        | Authorised staff can reach approved resources from other locations without exposing the whole LAN.                     |
| Segmentation: existing security boundaries are not established in the case study.                     | Create departmental, voice, guest, service, management, backup and DMZ zones with an explicit access policy.                    | Need-to-know access and controlled visitor internet use, rather than unrestricted movement between users and services. |

# 1. Gap Analysis (continued)

| **Current system - left**                                                                                               | **Changes required - middle**                                                                                                   | **Business need / proposed system - right**                                                                  |
|-------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Servers: four named services; Web reports memory/disk shortages and other services are slow.                            | Migrate services to two sized virtualisation hosts, retaining distinct service roles and monitoring resource demand.            | Adequate processing, memory and storage, with resource expansion and recoverable server services.            |
| Identity/addressing: user PCs have static IPs. Centralised DHCP/DNS is requested.                                       | Introduce two AD DS/DNS instances, managed DHCP scopes, reservations and group-based permissions.                               | Consistent identity administration, fewer address conflicts and central access control.                      |
| Recovery: no backup or redundancy is in place.                                                                          | Use two core links, two service hosts, domain-service redundancy, versioned NAS backups and encrypted off-site copies.          | Recoverability from equipment failure or data loss; defined recovery targets and regular restoration tests.  |
| Storage: staff save files locally, preventing sharing and exposing data to loss or misuse.                              | Move business files to centrally controlled shares; back them up and apply departmental permissions.                            | Accessible, protected files across Windows and Linux clients, with traceable authorised access.              |
| Operating systems: mixed Windows desktop versions and Linux machines; handout servers use Windows 2012 or Linux.        | Inventory compatibility, standardise supported desktop/server builds and retain Linux where appropriate.                        | Maintainable systems with a documented patch cycle, licensed software and consistent support.                |
| Security/monitoring: a dedicated management server and activity logs are requested; existing coverage is not specified. | Deploy NGFW inspection, managed endpoint protection, SNMPv3 monitoring, central event collection and restricted administration. | Earlier detection of faults and misuse, auditable staff access and a maintained security baseline.           |
| Communications: analogue phones and expensive international calls; videoconferencing is needed.                         | Install an IP PBX, SIP service and phones; provide meeting software and room video equipment.                                   | Improved staff/branch communication and a costed alternative to the existing telephone service.              |
| Wireless: network wireless access is available only to IT; visitors have connection difficulties.                       | Deploy managed access points with authenticated staff access and an isolated, controlled guest service.                         | Staff mobility and visitor internet access without granting visitors access to client or HR information.     |
| Email: the business asks for an email server within company infrastructure.                                             | Deploy an internal mail service with controlled mail ingress/egress, filtering and backup.                                      | Company-hosted email with security and recovery arrangements; cloud video does not replace this requirement. |
| People, time and governance: staff need account-software training; the project has four months and a \$500,000 budget.  | Stage discovery, procurement, migration and handover; train staff; seek CIO acceptance and record expenditure.                  | A usable upgrade within the agreed time and budget, respecting privacy, IP and organisational procedures.    |

Source: case study and interview \[P1, P2\]. Middle-column actions are proposed responses, not claims that these controls already exist.

# 2. Logical Topology

The proposed logical design uses one Brisbane ISP handoff, a perimeter firewall, two core switches and floor-based access switches. The cores have two direct interconnections. Access switches serve multiple departmental VLANs; a separate switch per department is not necessary. IP addresses in section 5 are proposed labels and documentation, not Packet Tracer configuration.

| **Connection**                               | **Purpose / proposed capacity**                                                                             |
|----------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Brisbane ISP handoff -\> FW-HQ -\> core pair | Single 1000/400 Mbps internet service; firewall is the WAN and VPN boundary.                                |
| CORE 1 \<-\> CORE 2: two separate links      | Two proposed 10 Gbps core interconnections; implement as the supported stack design, not an unmanaged loop. |
| Each floor access switch -\> core pair       | One uplink to each core in the production design; 10 Gbps target per uplink. PC access target: 1 Gbps.      |
| HYP-01 / HYP-02 -\> core pair                | Two 10 Gbps host interfaces, with resilience and separate service/backup VLANs.                             |
| FW-HQ -\> DMZ switch -\> SMTP gateway        | Separate firewall zone; the DMZ is not an unfiltered extension of the internal network.                     |
| Cairns LAN -\> FW-BR -\> VPN -\> FW-HQ       | One branch internet service, not a second Brisbane ISP. Only required branch-to-server flows are permitted. |

## 2.1 Security zones and service access

Departmental VLANs permit access to the required internal services, not to every other department. HR database access is limited to the HR group and authorised administrators; Marketing and Customer Service have separate file permissions. Domain authentication, DNS and DHCP must remain available to authorised clients even though administration of those services is restricted to IT. \[P1, P2\]

The existing Web role remains an internal intranet, as specified in the case study. An SMTP relay/filter is proposed for the DMZ; the internal mailbox service remains in the server VLAN. Guest traffic is internet-only, isolated from company subnets and other guests. Management interfaces are reachable only from approved IT administrative devices. The firewall provides IPS/IDS functionality at the perimeter; this does not claim inspection of every internal LAN flow. \[P1, R5\]

The chosen Cisco core pair supports a managed stack, providing one logical routing system. Department gateways are stack interfaces. The production implementation must validate supported dual-link stacking and loop prevention. A drawing of two cables alone is not an operational failover test. \[R1\]

INSERT: your final Packet Tracer Logical View screenshot. Include VLANs/subnets, link-capacity notes, firewall/IPS, DMZ, domain controllers, monitoring and the two core links. Use the service roles below as the diagram labels. No CLI configuration is required for this design-only submission.

# 2. Logical Topology (continued)

## 2.2 Server services and redundancy

| **Service / device**        | **Normal placement**  | **Resilience / security treatment**                                                     |
|-----------------------------|-----------------------|-----------------------------------------------------------------------------------------|
| DC1 + DNS + DHCP            | HYP-01                | DC2 on the other host; AD/DNS replication and DHCP failover are proposed.               |
| DC2 + DNS + DHCP            | HYP-02                | Independently running second domain-service instance, not only a stopped VM copy.       |
| SRV-WEB - internal intranet | HYP-01                | Internal server zone; replica on HYP-02 and application-consistent backup.              |
| SRV-HRDB                    | HYP-01                | HR-only application access; replica plus vendor-supported database backup.              |
| SRV-MKT-FS / SRV-CS-FS      | HYP-02                | Separate shares and permissions; replicas on HYP-01 and versioned backup.               |
| SRV-MAIL / SMTP-GW          | HYP-02 / HYP-01       | Mailbox server internal; relay/filter in DMZ; controlled SMTP path and replicas.        |
| SRV-MON / SRV-LOG           | Opposite hosts        | Zabbix for availability/capacity; Wazuh for central security events; protected backups. |
| WLAN-CTRL / NAS-BACKUP      | HYP-02 / physical NAS | Controller backup; NAS is a backup target, not single shared storage for live VMs.      |

Hyper-V Replica is proposed for recoverable copies of application VMs, with a 15-minute replication interval and a provisional four-hour recovery-time target. Recovery requires controlled activation and verification; it is not automatic clustered failover. Application-consistent database backups remain necessary. Both hosts are sized to run the essential services after one host fails, subject to workload acceptance tests. \[R26\]

RAID protects against some disk failures but is not the backup strategy. Daily versioned NAS backups and encrypted, offline/off-site copies protect against deletion, corruption and site loss. Proposed targets are a maximum one-business-day off-site data gap and a documented restoration exercise every quarter. Final retention and recovery targets require CIO approval. \[R27\]

## 2.3 Limits of the simplified design

A single head-office firewall, ISP service and PBX remain single points of failure. Two core links do not remove those risks, and the two-floor building remains a shared site risk. The proposal includes saved device configurations, supplier replacement arrangements, tested recovery and off-site copies rather than claiming zero downtime. A future requirement for uninterrupted internet or telephony would require further investment.

# 3. Physical Topology

The existing student-created overlay is retained below. It presents the two floors and representative device connections; it is not a measured cable-route drawing. The first-floor area is the upper image and the second-floor area is the lower image. The final logical diagram and quantities in section 6 provide the detailed proposed deployment. \[P4\]

<img src="media/image1.png" style="width:5.33933in;height:7.00787in" alt="Student-created HelpYou floor plan, duplicated vertically for two floors, with representative Packet Tracer devices and visible connections." />

Figure 1. Existing two-floor Packet Tracer overlay supplied by Roly Lobley. \[P4\]

Department placement follows the handout: Customer Service and IT on floor 1; Executives, Admin and HR on floor 2; Managers and Marketing on both floors. The business requires 35 Brisbane staff on each floor initially. Existing room labels on a reused background do not override this departmental allocation. \[P1, P2\]

# 4. Racks Diagram

The proposed arrangement uses the existing server-room rack space, with network equipment grouped above heavier equipment and patching separated from server access. The upper floor already has a patch-panel rack and an empty equipment rack. Final rack-unit positions depend on the measured dimensions and usable height; the table is a placement design, not an assertion about existing rack dimensions. \[P1\]

| **Location / rack area**            | **Top-to-bottom equipment arrangement**                                                                                                | **Function**                                                                     |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Floor 1 - network rack              | Patch panels and cable management; CORE 1; CORE 2; FW-HQ on a shelf; DMZ switch; PBX on a shelf; floor-1 access switches; UPS at base. | WAN security, the dual core interconnection, local access and telephone control. |
| Floor 1 - server space              | HYP-01; labelled service/management connections; spare expansion space; UPS-backed power.                                              | First domain controller and application-host workload.                           |
| Floor 2 - existing patch-panel rack | Retained patch panels; labelled outlets and cable management.                                                                          | Terminate the existing upper-floor horizontal cabling.                           |
| Floor 2 - existing equipment rack   | Three floor-2 access switches; HYP-02; NAS-BACKUP; spare space; UPS at base.                                                           | Second domain controller, recovery host and separate backup appliance.           |
| Cairns - small secured cabinet      | ISP handoff, FW-BR, branch access switch and UPS; local patch termination.                                                             | Branch VPN, workstation/phone access and controlled management.                  |

Rack access is restricted to authorised IT staff. Patch labels identify floor, panel and outlet, and device labels match the logical diagram and static-IP register. Power loading, earthing, ventilation and UPS runtime are verified during installation. Locating the hosts on different floors reduces some localised risks but does not create a second disaster-recovery site.

INSERT: Packet Tracer Physical View rack screenshot(s), showing the actual equipment arrangement and visible connections. Use normal device names; do not relabel an unrelated server icon as a working UPS. Rack tables above remain as the written arrangement explanation.

## 4.1 Port and outlet provision

Six 48-port access switches provide 288 Brisbane copper access ports, arranged as three switches per floor. The forecast is 270 departmental end devices; it is not automatically 270 PCs plus another 108 phones. For a conservative wired provision, 270 device ports and six AP ports leave 12 spare ports. Uplinks use separate uplink ports. The existing 216 horizontal runs must therefore be supplemented where the final wired-device count exceeds them; up to 60 further runs would be needed for 276 wired connections. \[P1, P2; proposed port arithmetic\]

A 24-port Cairns switch provides room for eight PCs, eight phones and one AP, with seven spare ports. Branch growth beyond the stated eight staff is not supplied in the case study and is not represented as a confirmed requirement.

# 5. IP Scheme

The following are proposed private IPv4 subnets. Earlier departmental VLAN numbers are retained. Each routed subnet uses its first usable address as the gateway; the /prefix determines its usable capacity. Departmental host requirements come from the interview; supporting-zone sizes are design allowances. \[P2\]

| **VLAN** | **Name**                | **Network / prefix** | **Gateway**     | **Requirement / usable** |
|----------|-------------------------|----------------------|-----------------|--------------------------|
| 10       | Executives              | 192.168.10.0/26      | 192.168.10.1    | 30 / 62                  |
| 20       | Managers                | 192.168.20.0/26      | 192.168.20.1    | 40 / 62                  |
| 30       | Marketing               | 192.168.30.0/25      | 192.168.30.1    | 50 / 126                 |
| 40       | Customer Service        | 192.168.40.0/25      | 192.168.40.1    | 50 / 126                 |
| 50       | Admin                   | 192.168.50.0/26      | 192.168.50.1    | 40 / 62                  |
| 60       | HR                      | 192.168.60.0/27      | 192.168.60.1    | 20 / 30                  |
| 70       | IT user devices         | 192.168.70.0/26      | 192.168.70.1    | 40 / 62                  |
| 80       | Brisbane voice          | 192.168.80.0/25      | 192.168.80.1    | 108 assumed / 126        |
| 90       | Brisbane guests         | 192.168.90.0/24      | 192.168.90.1    | 100 assumed / 254        |
| 100      | DMZ                     | 192.168.100.0/27     | 192.168.100.1   | 10 allowed / 30          |
| 110      | Internal services       | 192.168.110.0/26     | 192.168.110.1   | 30 allowed / 62          |
| 120      | Device management       | 192.168.120.0/26     | 192.168.120.1   | 40 allowed / 62          |
| 130      | Backup / replication    | 192.168.130.0/27     | None - isolated | 10 allowed / 30          |
| 140      | Staff Wi-Fi             | 192.168.140.0/24     | 192.168.140.1   | 150 allowed / 254        |
| 210      | Cairns staff            | 10.20.10.0/26        | 10.20.10.1      | 16 allowed / 62          |
| 220      | Cairns management       | 10.20.20.0/27        | 10.20.20.1      | 10 allowed / 30          |
| 280      | Cairns voice            | 10.20.80.0/27        | 10.20.80.1      | 8 required / 30          |
| 900      | Core / firewall transit | 192.168.254.0/29     | 192.168.254.1   | 2 used / 6               |

Usable ranges are .1-.62 for each /26, .1-.126 for each /25, .1-.30 for each /27, .1-.254 for each /24, and .1-.6 for the /29 transit. Network and broadcast addresses are not allocated. The gateway consumes one usable address. Voice and Wi-Fi capacity are supporting address pools; adding their pool sizes to 270 would double-count devices that move from departmental addressing to those services.

VLAN 130 is a non-routed replication/backup network with no default gateway on its secondary interfaces. The guest and DMZ gateways terminate at the firewall; other Brisbane gateways are on the core stack. The core default route uses firewall transit address 192.168.254.1. Public addressing is assigned by the ISP, not invented for this proposal.

# 5. IP Scheme (continued)

## 5.1 Static server and infrastructure addresses

| **Device / role**              | **VLAN** | **Static IP / prefix** | **Default gateway** |
|--------------------------------|----------|------------------------|---------------------|
| DC1 / DNS / DHCP               | 110      | 192.168.110.10/26      | 192.168.110.1       |
| DC2 / DNS / DHCP               | 110      | 192.168.110.11/26      | 192.168.110.1       |
| SRV-WEB (internal)             | 110      | 192.168.110.20/26      | 192.168.110.1       |
| SRV-HRDB                       | 110      | 192.168.110.21/26      | 192.168.110.1       |
| SRV-MKT-FS                     | 110      | 192.168.110.22/26      | 192.168.110.1       |
| SRV-CS-FS                      | 110      | 192.168.110.23/26      | 192.168.110.1       |
| SRV-MAIL                       | 110      | 192.168.110.24/26      | 192.168.110.1       |
| SMTP-GW (DMZ)                  | 100      | 192.168.100.10/27      | 192.168.100.1       |
| SRV-MON / Zabbix               | 120      | 192.168.120.20/26      | 192.168.120.1       |
| SRV-LOG / Wazuh                | 120      | 192.168.120.21/26      | 192.168.120.1       |
| WLAN-CTRL                      | 120      | 192.168.120.22/26      | 192.168.120.1       |
| Core stack management / SVI    | 120      | 192.168.120.1/26       | Uses transit route  |
| FW-HQ management               | 120      | 192.168.120.4/26       | Not a host gateway  |
| HYP-01 management              | 120      | 192.168.120.11/26      | 192.168.120.1       |
| HYP-02 management              | 120      | 192.168.120.12/26      | 192.168.120.1       |
| NAS management                 | 120      | 192.168.120.30/26      | 192.168.120.1       |
| PBX-01                         | 80       | 192.168.80.10/25       | 192.168.80.1        |
| Brisbane access switches 1-6   | 120      | 192.168.120.41-.46/26  | 192.168.120.1       |
| Brisbane APs 1-6               | 120      | 192.168.120.51-.56/26  | 192.168.120.1       |
| DMZ switch management          | 120      | 192.168.120.47/26      | 192.168.120.1       |
| Cairns switch / AP             | 220      | 10.20.20.2-.3/27       | 10.20.20.1          |
| HYP-01 / HYP-02 replication    | 130      | 192.168.130.11-.12/27  | None                |
| NAS backup-data interface      | 130      | 192.168.130.20/27      | None                |
| Core transit / firewall inside | 900      | 192.168.254.2 / .1 /29 | Core next hop: .1   |

## 5.2 DHCP and reservations

For departmental /26 networks, reserve .1-.9 and use .10-.62 as the initial DHCP scope. In HR /27, use .10-.30, giving 21 client addresses for the 20-device requirement. In Marketing and CS /25, use .10-.126. Voice uses .20-.126 for DHCP plus a reservation from .11-.19 if 108 phones are eventually required. Staff Wi-Fi uses .10-.254; guest addresses are supplied by the firewall. Management, servers, backup and transit addresses above are excluded from DHCP.

Use departmental DHCP reservations for printers once the inventory is confirmed; record MAC addresses and locations. Corporate clients use both DC/DNS servers. Guest clients use the approved external resolver, without internal-network access.

# 6. Investment of Hardware and Software

All recommendations below are proposed selections, not existing case-study assets. Prices were researched on 7 October 2026. Section 6.9 distinguishes published reference prices from configured-system and service allowances. Price-source references link to the specific product or service in the bibliography.

## 6.1 Core Layer Switches

Select two Cisco Catalyst C1300-12XS switches for the Brisbane core. Each provides twelve 10 Gbps-capable ports, including shared combo-port options, and the pair supports front-panel stacking. This suits the six access-switch uplinks, two host connections per core, NAS connectivity and two core interconnections. Twelve physical ports must not be counted as fourteen because combo connectors share ports. Published reference price: \$3,036.73 each including GST. \[R1, R2\]

The design uses a layered access/core structure, separates administration and applies inter-VLAN access controls. Keeping the two cores together permits the supported dual-link stack design without adding a second ISP. Failure of the entire stack or its shared environment remains a residual risk.

## 6.2 Access Layer Switches

Select six Cisco C1300-48P-4X switches at Brisbane, three per floor, and one C1300-24P-4X at Cairns. Reference prices are \$2,704.42 and \$2,003.43 respectively including GST. PoE supports phones/APs; gigabit access and separate high-speed uplinks avoid using the old 100 Mbps access hardware for the production design. Port arithmetic is in section 4.1. PoE load is assessed from the actual connected devices, not merely the total number of ports. \[R1, R3, R4\]

Packet Tracer 2960 icons may represent the proposed switches in a design-only drawing, but their simulated interfaces are not evidence of the commercial models or the proposed speeds. The diagram needs a short model-substitution note.

A Cisco C1300-24T-4X is proposed as the separate DMZ switch. Its reference listing is \$1,578; allow \$1,750 pending tax, shipping and quote confirmation. The SMTP gateway uses a dedicated host interface and virtual switch for this segment; the management VLAN is restricted separately. \[R30\]

## 6.3 Firewall

Select one FortiGate 70G at each site, with UTP subscription and support. FW-HQ provides internet security, IPS, DMZ separation and VPN termination; FW-BR secures the branch and terminates its VPN. The reference FG-70G-BDL-950-12 listing shows \$2,038 and is out of stock. The budget uses \$2,250 per site as a GST-inclusive procurement allowance, pending tax, stock and configuration confirmation. \[R5, R6\]

No separate enterprise router is required where the provider presents an Ethernet handoff supported by the firewall. Provider termination equipment remains outside the firewall. A \$2,500 setup and \$500 annual MFA allowance covers the remote-access authentication solution, subject to the final user count and supplier selection. Required throughput must be checked with the selected security inspection enabled, not by the headline basic-firewall forwarding figure alone.

## 6.4 Anti-Virus

Select Microsoft Defender for Business for 78 initial users and the server add-on for 14 protected server instances. At AU\$4.50 per user or server per month excluding GST, the combined GST-inclusive annual allocation is \$5,464.80. This separates desktop entitlement from server protection. Propose central alerts, tamper protection, automatic investigation and scheduled patching, with device eligibility confirmed before deployment. \[R11\]

Least-privilege administration, managed application settings, regular backups and MFA complement endpoint software. Purchasing antivirus alone does not establish compliance with an industry framework. ASD Essential Eight is used as a baseline for those controls, not as a certification claim. \[R27\]

## 6.5 Servers

Select two Dell PowerEdge R360 hosts with an eight-core processor, 128 GB ECC RAM, redundant power, separate resilient boot storage, four 3.84 TB enterprise SSDs in RAID 10 and dual 10 Gbps networking. This is a proposed configured specification, not the basic web-store configuration. Dell displays a starting price of \$6,047.97 including GST; allow \$18,000 per configured host including support, subject to quotation. Four 3.84 TB data SSDs provide approximately 7.68 TB before filesystem overhead. \[R7; proposed configuration\]

One host is positioned on each floor. The initial storage planning envelope is 4 TB for the total live service dataset, including mail and business files; this is an allowance until a data inventory is taken. A host stores its local live VMs and replicas of the other host's workload. It does not require twice the complete live dataset. Growth beyond the tested storage/CPU envelope triggers an upgrade rather than an unconditional five-year capacity claim.

| **Virtual service**           | **Initial RAM allowance** | **Operating system / purpose**                                                                    |
|-------------------------------|---------------------------|---------------------------------------------------------------------------------------------------|
| DC1 and DC2                   | 4 GB each                 | Windows Server 2025: AD DS, DNS, DHCP.                                                            |
| SRV-WEB                       | 4 GB                      | Windows Server: existing internal web application, subject to compatibility.                      |
| SRV-HRDB                      | 16 GB                     | Windows Server: existing HR database/application; database engine subject to vendor confirmation. |
| SRV-MKT-FS and SRV-CS-FS      | 8 GB each                 | Windows Server: department file services.                                                         |
| SRV-MAIL / SMTP-GW            | 8 GB / 2 GB               | Ubuntu Server LTS: Postfix/Dovecot mailbox service and separate DMZ mail relay/filter.            |
| SRV-MON / SRV-LOG / WLAN-CTRL | 4 GB / 8 GB / 4 GB        | Linux: monitoring, security events and access-point controller.                                   |

The proposed VM memory total is 70 GB. A surviving 128 GB host has room for this allocation and hypervisor overhead, but CPU, storage latency and the HR application must still pass a degraded-operation test. Virtualisation does not itself fix poorly performing application queries.

### Operating-system and application licensing

The design has six Windows Server guests. Each host is budgeted for three complete 16-core Standard licence sets so that either can run all six guests during recovery; the physical host is reserved for virtualisation management. Six packs at \$1,744.45 cost \$10,466.70. Add 78 User CALs at the \$109.45 reference price, totalling \$8,537.10. OEM/stacking entitlement, CAL type and replica use must be confirmed in the supplier licence statement before purchase. \[R8-R10, R28\]

The HR database engine and application licence are not identified in the case study. An \$8,000 compatibility/licence allowance and \$2,000 annual maintenance allowance are included, rather than claiming that a particular database edition is sufficient or free.

### Backup storage

Select a Synology RS2423RP+ NAS as a separate backup target. The diskless reference price is \$6,124.25. Allow another \$6,000 for compatible disks, rails and removable off-site media: the planning configuration is six 8 TB disks in RAID 6 (about 32 TB before overhead) and four removable backup targets. Validate the selected disks against the NAS compatibility list. NAS snapshots, versioned backups and offline copies have different purposes. \[R12, R13\]

## 6.6 VoIP and Videoconferencing

Select one Grandstream UCM6302 IP PBX at \$462 including GST and 82 GRP2612P phones at \$83 each: 78 deployed for current staff and four spare. Brisbane and Cairns share the PBX over the VPN. The selected phones have 100 Mbps ports, so PCs use separate gigabit switch connections rather than being placed behind the phone's Ethernet passthrough. Phones do not need gigabit throughput to carry voice. \[R14-R16\]

Provide Microsoft Teams Essentials for 78 users at AU\$6 per user per month excluding GST, or \$6,177.60 annually including GST. Add three Logitech MeetUp 2 USB video bars at \$1,599 each, two at Brisbane and one at Cairns. These are USB/BYOD meeting rooms, not a separately licensed Teams Rooms deployment. The endpoint/peripheral allowance covers any required meeting display or compatible computer. Teams Essentials is for meetings and does not include the external PSTN service in this proposal. \[R17, R18\]

Allow ten simultaneous external calls initially, with a \$600 monthly SIP/number/call budget pending a Nexgen/Aussie Broadband quote and review of actual call records. Domestic/international rates, number porting and emergency-calling arrangements must be confirmed. Lower bills are an objective, not a quantified saving: no existing call-cost baseline was supplied. \[P1, R25\]

## 6.7 Network Monitoring

Use Zabbix on SRV-MON for SNMPv3 device monitoring, service availability, resource thresholds and alerts. Use Wazuh on SRV-LOG for collected security events and investigation. These have separate operational roles; a bandwidth monitor is not assumed to be a full security-event platform. The self-hosted software licence allocation is \$0; administration, storage and support are budgeted separately. \[R21, R22, R29\]

Proposed checks include interface utilisation and errors, server CPU/RAM, storage free space and latency, backup-job status, VPN reachability, authentication failures and firewall events. Synchronise device time, restrict log administration and review high-priority alerts daily. Propose 90 days of readily searchable events and 12 months of protected archive, subject to CIO approval and measured event volume.

## 6.8 Cross-Platform File Sharing

Retain Windows file services for Market-FS and CS-FS and provide authenticated SMB access to approved Windows and Linux clients. Keep HR-DB separate from general file shares. User access follows job role and AD groups, with separate administrator accounts, auditing of sensitive changes and a controlled permission-review process. This is the proposed implementation of the client's need-to-know and cross-platform requirements. \[P1\]

Use Ubuntu Server LTS with Postfix/Dovecot for the proposed internal mail role and the separate SMTP relay, following the vendor mail-services documentation. Validate account integration, anti-spam filtering, certificate management, mail recovery and client compatibility in the pilot. This retains company-hosted email rather than silently replacing it with a hosted mailbox subscription. \[R23\]

### Managed wireless

Provide six TP-Link EAP650 APs at Brisbane and one at Cairns, subject to a coverage survey. The \$179 reference price gives \$1,253 for seven units; the cited retailer currently reports no stock. EAP650 supports enterprise wireless authentication, SSID/VLAN mapping and guest isolation. Use a local controller, separate staff and guest services, and rate-limit visitor access. A coverage survey, rather than the floor-plan picture alone, determines final AP positions. \[R19, R20\]

## 6.9 Total Costings

Amounts below are AUD, budgeted inclusive of GST. P = published reference price; A = proposal allowance, not a supplier quotation. Retail references are dated 7 October 2026; delivery, stock, licensing channel and final tax treatment are confirmed at procurement. Software subscriptions published ex-GST are multiplied by 1.10. The listed ISP tariff is provisionally treated as GST-inclusive until its service summary confirms the tax basis.

| **Initial item**                             | **Qty** | **Unit budget** | **Line total** | **Basis**  |
|----------------------------------------------|---------|-----------------|----------------|------------|
| Core switches - Cisco C1300-12XS             | 2       | \$3,036.73      | \$6,073.46     | P \[R2\]   |
| Head-office access - Cisco C1300-48P-4X      | 6       | \$2,704.42      | \$16,226.52    | P \[R3\]   |
| Cairns access - Cisco C1300-24P-4X           | 1       | \$2,003.43      | \$2,003.43     | P \[R4\]   |
| DMZ switch - Cisco C1300-24T-4X              | 1       | \$1,750.00      | \$1,750.00     | A \[R30\]  |
| FortiGate 70G + year-one UTP, one per site   | 2       | \$2,250.00      | \$4,500.00     | A \[R6\]   |
| Dell R360 configured virtualisation hosts    | 2       | \$18,000.00     | \$36,000.00    | A \[R7\]   |
| Windows Server 2025 Standard 16-core packs   | 6       | \$1,744.45      | \$10,466.70    | P \[R8\]   |
| Windows Server User CALs                     | 78      | \$109.45        | \$8,537.10     | P \[R10\]  |
| Synology RS2423RP+ diskless NAS              | 1       | \$6,124.25      | \$6,124.25     | P \[R13\]  |
| NAS drives, rails and backup media package   | 1       | \$6,000.00      | \$6,000.00     | A          |
| Head-office and branch UPS / rack fit-out    | 1       | \$7,000.00      | \$7,000.00     | A          |
| TP-Link EAP650 access points                 | 7       | \$179.00        | \$1,253.00     | P \[R20\]  |
| Grandstream UCM6302 IP PBX                   | 1       | \$462.00        | \$462.00       | P \[R15\]  |
| GRP2612P phones (78 deployed, four spare)    | 82      | \$83.00         | \$6,806.00     | P \[R16\]  |
| Logitech MeetUp 2 (two Brisbane, one Cairns) | 3       | \$1,599.00      | \$4,797.00     | P \[R18\]  |
| Endpoint replacement / OS / peripherals fund | 78      | \$1,500.00      | \$117,000.00   | A          |
| Compatible optics and connection accessories | 1       | \$6,500.00      | \$6,500.00     | A          |
| Cabling certification and extra outlets      | 1       | \$6,000.00      | \$6,000.00     | A          |
| HR database/application compatibility fund   | 1       | \$8,000.00      | \$8,000.00     | A          |
| Design, installation and migration labour    | 160     | \$150.00        | \$24,000.00    | A          |
| Staff and IT training / handover             | 1       | \$5,000.00      | \$5,000.00     | A          |
| Remote-access MFA licensing / enrolment fund | 1       | \$2,500.00      | \$2,500.00     | A          |
| Initial procurement and implementation       |         |                 | \$286,999.46   |            |
| Contingency: 10% of the above                |         |                 | \$28,699.95    | Calculated |

The endpoint fund is a ceiling for replacing or upgrading the 78 current user workstations and necessary room peripherals; it is not a verified quotation for 78 identical PCs. Retain compatible equipment where practical. The NAS package, UPS/rack work, optics, extra outlets and application funds require site-specific quotes. These allowances prevent mandatory supporting costs from being omitted or hidden in an unsupported round total.

## 6.9 Total Costings (continued)

| **Recurring item**                          | **Annual cost** | **Basis**                                     |
|---------------------------------------------|-----------------|-----------------------------------------------|
| Defender for Business: 78 users             | \$4,633.20      | \[R11\]                                       |
| Defender server add-on: 14 instances        | \$831.60        | \[R11\]                                       |
| Teams Essentials: 78 users                  | \$6,177.60      | \[R17\]                                       |
| Brisbane Business Assurance 1000/400        | \$1,920.00      | \[R24\]                                       |
| Cairns internet service allowance           | \$1,440.00      | A \[R24\]                                     |
| SIP trunk, numbers and call allowance       | \$7,200.00      | A \[R25\]                                     |
| Off-site backup custody / media rotation    | \$1,200.00      | A                                             |
| External support, patches and restore tests | \$9,000.00      | A                                             |
| Business application maintenance allowance  | \$2,000.00      | A                                             |
| MFA subscription / token renewal fund       | \$500.00        | A                                             |
| Zabbix, Wazuh and Ubuntu licence fees       | \$0.00          | \[R22, R23, R29\]                             |
| Year-one operating total                    | \$34,902.40     | Calculated                                    |
| Firewall renewals - years 2 onward          | \$2,000.00      | Annual allowance; not charged twice in year 1 |

| **Budget summary**                                | **AUD including GST** |
|---------------------------------------------------|-----------------------|
| Initial implementation                            | \$286,999.46          |
| Implementation contingency                        | \$28,699.95           |
| First-year recurring costs                        | \$34,902.40           |
| First-year funding requirement                    | \$350,601.81          |
| Remaining against the \$500,000 case-study budget | \$149,398.19          |
| Five-year baseline ownership estimate             | \$498,211.41          |

Five-year estimate = initial implementation + contingency + five years of the current 78-user operating budget + four years of firewall renewals. It is a baseline, not a fixed-price guarantee: it excludes inflation, electricity, additional future employees, storage growth beyond the allowances and replacement equipment. Increasing from 78 organisation-wide users to 116 (108 Brisbane plus eight Cairns) would add 38 user licences and any required devices; at the displayed Defender and Teams prices, those extra subscriptions alone add \$5,266.80 annually.

## 6.10 ISP Plan

For Brisbane, select Aussie Broadband Business Assurance Ultrafast Plus 1000/400 at the displayed \$160 monthly rate, with a static IP and Gold eSLA priority restoration. This is a 1000 Mbps download / 400 Mbps upload access tier, not symmetric 1 Gbps dedicated fibre. The provider lists typical busy-period speeds of 875/339 Mbps and requires FTTP eligibility. Check the site address, inbound mail policy, reverse DNS and static addressing before ordering. \[R24\]

Cairns retains one business internet service, with a \$120 monthly service allowance pending an address-qualified plan. There are no dual Brisbane ISPs and no mobile backup counted in the design. An included backup feature in a provider plan is not treated as a deployed second path. If either site's single service fails, internet-dependent calls and branch access may be interrupted until restoration.

# 7. Traffic Bandwidth Prediction and Expected Performance

## 7.1 Existing performance and prediction method

The existing 100 Mbps network interfaces leave little headroom for Web and Marketing traffic, both listed at a 100 Mbps peak in the interview. HR-DB peaks at 80 Mbps and CS-FS at 60 Mbps. The Web server also reports memory and disk-space faults, so bandwidth is only one contributing constraint. The case study does not provide measured CPU load, disk latency or application response times. \[P1, P2\]

The interview explicitly labels the new Email, DHCP, DC/DNS and Monitoring values as estimates. Those values are retained as planning baselines, not represented as measurements from installed servers. Although the handout lists IT Admin only for certain infrastructure roles, normal clients still require their authorised DHCP/DNS/domain functions; administrative control and service consumption are different permissions. \[P2\]

Forecast formula: predicted peak = supplied peak x relevant five-year staff-growth factor x 1.10 workload allowance, rounded upward to the next 10 Mbps. The 10% factor and rounding are proposal assumptions. The source documents do not prescribe a single mandatory multiplier.

| **Service audience**                          | **Growth calculation**                 | **Factor**     |
|-----------------------------------------------|----------------------------------------|----------------|
| All head-office staff / shared infrastructure | 108 forecast staff / 40 original staff | 2.70           |
| HR                                            | 10 forecast / 3 original               | 3.33 recurring |
| Marketing                                     | 20 forecast / 10 original              | 2.00           |
| Customer Service                              | 30 forecast / 5 original               | 6.00           |

The comparison uses the original 40-staff baseline because the interview does not date its traffic estimates relative to the 70-staff expansion. Shared infrastructure uses staff growth as a workload proxy, not as an asserted packet-rate relationship. If a measured 70-staff baseline becomes available, recalculate from that baseline. Cairns access and changes in application behaviour are then validated in the pilot rather than silently added to head-office demand.

## 7.2 Bandwidth calculations

| **Service**  | **Current average** | **Current peak** | **Growth + allowance** | **5-year peak** | **Service benchmark** |
|--------------|---------------------|------------------|------------------------|-----------------|-----------------------|
| Web          | 60                  | 100              | 2.70 x 1.10            | 300             | 1,000                 |
| HR-DB        | 40                  | 80               | 3.33 x 1.10            | 300             | 1,000                 |
| Marketing FS | 50                  | 100              | 2.00 x 1.10            | 220             | 1,000                 |
| CS-FS        | 26                  | 60               | 6.00 x 1.10            | 400             | 1,000                 |
| Email\*      | 25                  | 80               | 2.70 x 1.10            | 240             | 1,000                 |
| DHCP\*       | 20                  | 50               | 2.70 x 1.10            | 150             | 1,000                 |
| DC / DNS\*   | 40                  | 90               | 2.70 x 1.10            | 270             | 1,000                 |
| Monitoring\* | 60                  | 100              | 2.70 x 1.10            | 300             | 1,000                 |

All traffic values are Mbps. \*The supplied handout identifies these baselines as estimated. A 1,000 Mbps service benchmark is a proposed throughput-capacity target, not a configured speed limit or dedicated bandwidth reservation. \[P2; calculations above\]

# 7. Traffic Bandwidth Prediction (continued)

The sum of predicted service peaks is 2,180 Mbps (2.18 Gbps). This deliberately assumes that all listed services could peak together; it is a conservative LAN planning envelope, not measured simultaneous utilisation. A surviving 10 Gbps host path has about 4.6 times this calculated capacity before overhead and competing backup/replication traffic. The busiest individual forecast, CS-FS at 400 Mbps, is below the 1 Gbps service benchmark.

For example, CS-FS = 60 x (30 / 5) x 1.10 = 396 Mbps, rounded up to 400 Mbps. Web = 100 x (108 / 40) x 1.10 = 297 Mbps, rounded up to 300 Mbps. Department-specific growth avoids understating the six-fold growth in Customer Service while applying the same arbitrary multiplier to every service.

### Backup, voice and video allowances

Backup traffic is additional to the eight interview rows. Moving 500 GB of changed data over an eight-hour window needs approximately 139 Mbps before protocol overhead (500 x 8,000 / 28,800); adding 30% overhead gives about 181 Mbps. This is an example workload assumption, not a measured daily change rate. Schedule backups and VM replication so they do not displace interactive application traffic, and size off-site media from the actual dataset.

For WAN planning, initially allow 20 simultaneous video sessions at 4 Mbps each direction (80 Mbps), ten external voice calls at 0.1 Mbps each direction (1 Mbps), and a further 100 Mbps download / 50 Mbps upload for other concurrent activity. These are conservative design allowances to test, not vendor performance guarantees. Internal file-server traffic is not added wholesale to internet demand because most of it remains within the LAN.

## 7.3 Five-year capacity and implementation

The upgrade combines faster network interfaces with right-sized memory, resilient storage and service migration. It separates the immediate 70-user Brisbane deployment from the five-year 108-user planning horizon. Department subnet capacity, switch ports, software licences and storage are reviewed together, not treated as interchangeable measures. \[P1, P2\]

| **Stage**               | **Timing** | **Work and acceptance outcome**                                                                                                                                                      |
|-------------------------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Discovery and approval  | Month 1    | Inventory devices/data; confirm the case-study assumptions, site eligibility, permissions, service dependencies and supplier quotes. Obtain CIO design/budget approval.              |
| Build and pilot         | Month 2    | Install network and host infrastructure; create pilot identity, file, email, voice and backup services. Validate application and client compatibility before moving production data. |
| Controlled migration    | Month 3    | Move departments in agreed windows; migrate shared data and numbers; retain rollback copies and the old service until the relevant acceptance tests pass.                            |
| Acceptance and handover | Month 4    | Test authorisation, VPN, two-core-path behaviour, recovery, calls/video and backup restoration. Train staff, issue diagrams/support records and obtain CIO acceptance.               |

These are proposed deployment activities for the business, not additional configuration tasks required from the student for the design-only Packet Tracer submission.

## 7.3 Five-year capacity (continued)

The IT team reviews capacity monthly and the full design annually. Proposed triggers are sustained busy-period interface utilisation above 70%, CPU above 70%, memory above 80%, or less than 25% free working storage. Investigate application latency and error rates as well as utilisation; these thresholds are operational targets to agree with the CIO, not observations of the current system.

Review high-priority security and backup alerts daily. Schedule operating-system, application and device updates under change control, maintain device configuration backups, and check new firmware against a test device or pilot group. Review access permissions and conduct a representative restoration exercise quarterly. Conduct a wider recovery rehearsal annually, including loss of one host and an unavailable internet path. \[R27; proposed schedule\]

Before sign-off, prove that HR data cannot be read by unauthorised departments, guests cannot access internal subnets, authorised clients can authenticate against either domain controller, files are available from supported Windows and Linux clients, and a deleted file and representative VM/database can be restored. Measure application response during simultaneous file transfer and video/voice use. Record actual results rather than stating that a plan or diagram has already passed testing.

Capacity can be expanded by adding supported access ports, memory/storage within the host limits, more guest addresses where appropriate, and additional user licences. A physical CPU/platform limit, a substantially larger database or stricter recovery target may require a new host or a different availability design. The five-year recommendation therefore includes review and upgrade actions instead of guaranteeing unchanged equipment will meet every future workload.

## 7.4 Conclusion

The proposed infrastructure addresses HelpYou's immediate two-floor expansion and the five-year demand supplied in the customer interview. It replaces the bottlenecked access network, introduces departmental and service segmentation, provides controlled remote/guest access and centralises business data, monitoring and communications. The two core switches and dual core links improve the network design, while two domain-service instances, a recovery-capable host pair and protected backups provide distinct forms of service resilience.

The proposal retains a single ISP service per site and recognises its interruption risk. The first-year planning budget of \$350,601.81 remains within the \$500,000 ceiling, with published prices separated from allowances and a four-month delivery schedule. Implementation should proceed after the CIO approves the configured quotations, application compatibility, recovery targets and final diagrams. Successful installation, testing and acceptance must then be documented; this report does not claim they have already occurred. \[P1\]

# 8. Bibliography

Assessment sources retain the supplied titles. Vendor and industry pages below were accessed on 7 October 2026. Product prices are reference observations, not binding quotations. In-text references \[P#\] identify supplied case material; \[R#\] identify external research.

\[P1\] TAFE Queensland. ICTNWK529_546_AT2_PE_TQM_v2: Portfolio of Evidence. HelpYou case study and task instructions. Supplied assessment document.

\[P2\] TAFE Queensland. ICTNWK529_546_AT2_Student Handout 2_TQB_v1: HelpYou Mortgage Customer Interview Answers. Supplied assessment document.

\[P3\] TAFE Queensland. ICTNWK529_546_AT2_MC_TQM_v2: Assessment Marking Criteria; and ICTNWK529_546_AT2_Template_SH_TQM_v2. Supplied assessment documents.

\[P4\] Lobley, R. FINAL FLOOR PLAN.png. Supplied student-created two-floor Packet Tracer overlay.

\[R1\] Cisco. Catalyst 1300 and 1300X Series Switches: data sheet.

[<u>https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-1300-series-switches/nb-06-cat1300-ser-data-sheet-cte-en.html</u>](https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-1300-series-switches/nb-06-cat1300-ser-data-sheet-cte-en.html)

\[R2\] The Telecom Shop. Cisco Catalyst C1300-12XS: Australian retail listing.

[<u>https://www.thetelecomshop.com/au/cisco-catalyst-1300-12-port-sfp-2x10ge-shared-c1300-12xs</u>](https://www.thetelecomshop.com/au/cisco-catalyst-1300-12-port-sfp-2x10ge-shared-c1300-12xs)

\[R3\] PB Tech Australia. Cisco C1300-48P-4X: Australian retail listing.

[<u>https://www.pbtech.com/au/product/SWHCIS0185/Cisco-Catalyst-1300-Switch-48-port-GE-PoE-4x10G-SF</u>](https://www.pbtech.com/au/product/SWHCIS0185/Cisco-Catalyst-1300-Switch-48-port-GE-PoE-4x10G-SF)

\[R4\] The Telecom Shop. Cisco C1300-24P-4X: Australian retail listing.

[<u>https://www.thetelecomshop.com/au/cisco-catalyst-1300-24-port-ge-poe-managed-network-switch-c1300-24p-4x</u>](https://www.thetelecomshop.com/au/cisco-catalyst-1300-24-port-ge-poe-managed-network-switch-c1300-24p-4x)

\[R5\] Fortinet. Next-Generation Firewall product information.

[<u>https://www.fortinet.com/products/next-generation-firewall</u>](https://www.fortinet.com/products/next-generation-firewall)

\[R6\] Technology Centre. FG-70G-BDL-950-12 hardware and one-year UTP bundle: reference listing.

[<u>https://www.technologycentre.com.au/products/fortinet-fortigate-70g-hardware-plus-1-year-forticare-premium-and-fortiguard-unified-threat-protection-utp-2530043</u>](https://www.technologycentre.com.au/products/fortinet-fortigate-70g-hardware-plus-1-year-forticare-premium-and-fortiguard-unified-threat-protection-utp-2530043)

\[R7\] Dell Australia. PowerEdge R360 configuration and starting price.

[<u>https://www.dell.com/en-au/shop/ipovw/poweredge-r360</u>](https://www.dell.com/en-au/shop/ipovw/poweredge-r360)

\[R8\] Techbuy. Windows Server 2025 Standard 16-core OEM pack EP2-25187: reference price.

[<u>https://www.techbuy.com.au/p/553348/OPERATING_SYSTEMS_LICENCES/Microsoft/EP2-25187.asp</u>](https://www.techbuy.com.au/p/553348/OPERATING_SYSTEMS_LICENCES/Microsoft/EP2-25187.asp)

\[R9\] Microsoft. Windows Server 2025 licensing and pricing.

[<u>https://www.microsoft.com/en-au/windows-server/pricing</u>](https://www.microsoft.com/en-au/windows-server/pricing)

\[R10\] Dell Australia. PowerEdge R450 configurator: Windows Server User CAL reference price.

[<u>https://www.dell.com/en-au/shop/servers-storage-and-networking/poweredge-r450-rack-server/spd/poweredge-r450/per45020a</u>](https://www.dell.com/en-au/shop/servers-storage-and-networking/poweredge-r450-rack-server/spd/poweredge-r450/per45020a)

\[R11\] Microsoft. Small and medium business security solutions pricing: Defender for Business and server add-on.

[<u>https://www.microsoft.com/en-au/security/small-medium-business/pricing</u>](https://www.microsoft.com/en-au/security/small-medium-business/pricing)

\[R12\] Synology. RackStation RS2423+ / RS2423RP+ product information.

[<u>https://www.synology.com/en-global/products/RS2423%2B</u>](https://www.synology.com/en-global/products/RS2423%2B)

\[R13\] Techbuy. Synology RS2423RP+ diskless NAS: Australian retail listing.

[<u>https://www.techbuy.com.au/p/529889/HARD_DRIVE\_-\_EXTERNAL_NAS_DRIVES/Synology/RS2423RP\_.asp</u>](https://www.techbuy.com.au/p/529889/HARD_DRIVE_-_EXTERNAL_NAS_DRIVES/Synology/RS2423RP_.asp)

\[R14\] Grandstream. UCM6300 Series IP PBX product information.

[<u>https://www.grandstream.com/products/ip-pbxs/ucm-series-ip-pbxs/product/ucm6300-series-ip-pbx</u>](https://www.grandstream.com/products/ip-pbxs/ucm-series-ip-pbxs/product/ucm6300-series-ip-pbx)

\[R15\] Telrex. Grandstream UCM6302 IP PBX: Australian retail listing.

[<u>https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users</u>](https://www.telrex.com.au/grandstream-ucm6302-2-fxo-2fxs-1000-users)

\[R16\] MyITHub. Grandstream GRP2612P IP phone: Australian retail listing.

[<u>https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone</u>](https://www.myithub.com.au/grandstream-grp2612p-2-4-colour-lcd-display-22-line-keys-2-sip-accounts-poe-support-100mbps-port-ip-phone)

\[R17\] Microsoft. Teams Essentials for Small Businesses: Australian pricing.

[<u>https://www.microsoft.com/en-au/microsoft-teams/essentials</u>](https://www.microsoft.com/en-au/microsoft-teams/essentials)

\[R18\] Video Conferencing Australia. Logitech MeetUp 2: Australian retail listing.

[<u>https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/</u>](https://www.videoconferencingaustralia.com.au/product/logitech-meetup-2/)

\[R19\] TP-Link Australia. EAP650 V1.30 specifications.

[<u>https://www.tp-link.com/au/business-networking/omada-wifi-ceiling-mount/eap650/v1.30/</u>](https://www.tp-link.com/au/business-networking/omada-wifi-ceiling-mount/eap650/v1.30/)

\[R20\] Umart. EAP650 access point: Australian retail listing.

[<u>https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658</u>](https://www.umart.com.au/product/tp-link-ceiling-mount-ax3000-dual-band-wifi-6-access-point-eap650-72658)

\[R21\] Zabbix. On-premise platform and network monitoring.

[<u>https://www.zabbix.com/network_monitoring</u>](https://www.zabbix.com/network_monitoring)

\[R22\] Wazuh. Getting started: platform documentation.

[<u>https://documentation.wazuh.com/current/getting-started/index.html</u>](https://documentation.wazuh.com/current/getting-started/index.html)

\[R23\] Canonical. Ubuntu Server documentation: Mail services.

[<u>https://ubuntu.com/server/docs/how-to/mail-services/</u>](https://ubuntu.com/server/docs/how-to/mail-services/)

\[R24\] Aussie Broadband. Business nbn plans, including Business Assurance Ultrafast Plus 1000/400.

[<u>https://www.aussiebroadband.com.au/business/internet/nbn-plans/</u>](https://www.aussiebroadband.com.au/business/internet/nbn-plans/)

\[R25\] Aussie Broadband / Nexgen. SIP Trunks: quotation and service information.

[<u>https://www.aussiebroadband.com.au/business/voice/sip-trunks/</u>](https://www.aussiebroadband.com.au/business/voice/sip-trunks/)

\[R26\] Microsoft Learn. Hyper-V Replica overview.

[<u>https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-overview</u>](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-overview)

\[R27\] Australian Signals Directorate. Essential Eight maturity model.

[<u>https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model</u>](https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight/essential-eight-maturity-model)

\[R28\] Microsoft. Windows Server 2025 Licensing Guide.

[<u>https://www.microsoft.com/licensing/docs/documents/download/Licensing_guide_PLT_Windows_Server_2025.pdf</u>](https://www.microsoft.com/licensing/docs/documents/download/Licensing_guide_PLT_Windows_Server_2025.pdf)

\[R29\] Zabbix. On-premise open-source deployment and licence-fee information.

[<u>https://www.zabbix.com/</u>](https://www.zabbix.com/)

\[R30\] i-Tech. Cisco C1300-24T-4X: reference listing for the DMZ switch.

[<u>https://www.i-tech.com.au/c1300-24t-4x-cisco-c1300-24t-4x-catalyst-1300-24-port-ge-419371.html</u>](https://www.i-tech.com.au/c1300-24t-4x-cisco-c1300-24t-4x-catalyst-1300-24-port-ge-419371.html)
