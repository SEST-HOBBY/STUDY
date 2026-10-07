# 2. Logical Topology

My logical design for Brisbane is one nbn service, one perimeter firewall, two core switches and six floor-based access switches. The Brisbane nbn handoff terminates on the WAN port of FW-HQ, a FortiGate 70G, which sits directly behind the ISP and in front of the two core switches; every flow to or from the internet, the DMZ, the guest network and Cairns passes through it before it reaches the core stack. The core stack connects to the firewall's LAN side over the VLAN 900 transit (192.168.254.0/29), and the stack's default route points at the firewall's address, 192.168.254.1. Every packet between the LAN and the internet therefore crosses the firewall and its IPS/IDS inspection. Cairns has the same arrangement on a smaller scale: the branch nbn service terminates on FW-BR, a second FortiGate 70G, which fronts the branch switch and carries the site-to-site VPN back to FW-HQ.

Behind the firewall, CORE 1 and CORE 2 are joined by two 10 Gbps links and run as one stack. Each access switch carries several departmental VLANs, so the three switches on a floor serve every department on that floor and I avoid a separate switch per department. The VLAN numbers and subnets in this section are the ones I allocate in section 5, and the link table below gives the capacity of each connection.

| Connection | Purpose and capacity |
|---|---|
| Brisbane ISP handoff -> FW-HQ | One 1000/400 Mbps business nbn service; FW-HQ is the WAN, IPS/IDS and VPN boundary. |
| FW-HQ -> core pair | One 1 GbE transit link to each core in VLAN 900 (192.168.254.0/29); the core stack's default route points at 192.168.254.1. |
| CORE 1 <-> CORE 2 | Two 10 Gbps links, run as a supported stack so the pair is one logical switch. |
| Each access switch -> core pair | Two 10 Gbps uplinks per switch, one to each core; 1 Gbps PC access ports; PoE ports for phones and APs. |
| HYP-01 / HYP-02 -> core pair | Two 10 Gbps links per host, one to each core, carrying the service, management and backup VLANs; a separate 1 GbE link from each host to the DMZ switch for the SMTP gateway. |
| FW-HQ -> DMZ switch -> SMTP-GW | Separate firewall zone (VLAN 100) for the mail relay. |
| Cairns LAN -> FW-BR -> VPN -> FW-HQ | One branch internet service and a site-to-site VPN; only the required branch-to-server flows are permitted. |

*Table 2. Connections and link capacities in my design.*

Figure 2 draws the whole design on one page, with the VLAN IDs, subnets and link speeds marked on it.

![Proposed logical topology for HelpYou Mortgage](figures/fig2_logical_topology.png)

*Figure 2. Proposed logical topology for HelpYou Mortgage.*

The diagram follows the path a packet takes. The nbn handoff (1000/400 Mbps) enters FW-HQ, which carries the IPS/IDS and VPN roles. The VLAN 900 transit then leads to CORE 1 and CORE 2, joined by their two 10 Gbps links. The six access switches hang off the cores, each with two 10 Gbps uplinks.

The access switches carry the departmental VLANs: 10 Executives (192.168.10.0/26), 20 Managers (192.168.20.0/26), 30 Marketing (192.168.30.0/25), 40 Customer Service (192.168.40.0/25), 50 Admin (192.168.50.0/26), 60 HR (192.168.60.0/27) and 70 IT (192.168.70.0/26). Voice runs on VLAN 80 (192.168.80.0/25) and staff Wi-Fi on VLAN 140 (192.168.140.0/24). Guests sit on VLAN 90 (192.168.90.0/24), with their gateway on the firewall, so a visitor's traffic goes straight out to the internet.

On the server side, HYP-01 on floor 1 and HYP-02 on floor 2 each connect to both cores at 10 Gbps. Those links carry the services VLAN 110 (192.168.110.0/26), the management VLAN 120 (192.168.120.0/26) and the backup VLAN 130 (192.168.130.0/27). DC1 runs on HYP-01 and DC2 on HYP-02, so domain logon, DNS and DHCP keep working if either host is lost. SRV-MON, my Zabbix monitoring server at 192.168.120.20, polls every switch, firewall, host and server over SNMPv3. NAS-BACKUP connects to both cores, with its backup-data interface on the isolated VLAN 130.

The DMZ switch hangs off FW-HQ on VLAN 100 (192.168.100.0/27), with its gateway on the firewall, and holds SMTP-GW. A 1 GbE link from each host reaches the DMZ switch, so the gateway and its replica can both run there. Cairns appears as its own site: FW-BR, the C1300-24P-4X access switch and one access point on VLANs 210, 220 and 280 (10.20.10.0/26, 10.20.20.0/27 and 10.20.80.0/27), joined to Brisbane by the site-to-site VPN.

The diagram shows two kinds of redundancy. In the infrastructure, the two core links and the stack mean that a failed core switch or a failed interconnect still leaves every access switch, both hosts and the firewall with a working path. In the services, two hosts, two domain controllers, Hyper-V replicas of every application VM and a separate NAS mean that a failed host or a deleted file is recovered from a copy that already exists.

My Packet Tracer topology file (Helpyou_Network_Topology.pkt) is the companion to this diagram. It draws the two core switches with their first interconnect, the four existing servers, sample PCs for each of the seven departments, the DMZ switch, the firewall and the ISP cloud, with the firewall cabled to the ISP cloud. Packet Tracer has no Catalyst 1300 or FortiGate models, so the cores are drawn with 2960 icons and the firewall with an ASA icon. The file shows what connects to what with copper cabling, and the configuration detail sits in sections 2 and 5. The second core link and the firewall-to-core transit links are drawn in Figure 2.

## 2.1 Security zones and service access

Each departmental VLAN reaches the internal services its staff need and stops there. The HR database answers only to the HR group and authorised administrators, and Marketing and Customer Service each have their own file shares and permissions. Every corporate client can reach domain authentication, DNS and DHCP, while administration of those services stays with IT. [P1, P2]

The existing Web role stays an internal intranet, as the case study specifies. The SMTP gateway sits in the DMZ as a relay and filter, so inbound mail is inspected before it reaches SRV-MAIL in the services VLAN. Guest traffic goes straight to the internet and is isolated from company subnets and from other guests. Management interfaces answer only to approved IT administrative devices. FW-HQ runs IPS/IDS on every flow that crosses the perimeter, including the DMZ, the guest network and the VPN. [P1, R5]

The two C1300-12XS cores run as a managed front-panel stack, so they behave as one logical switch and one routing system. Every departmental gateway is an interface on the stack, and the two interconnects carry stack traffic between the members. During the build I will confirm the dual-link stacking and loop prevention on the real hardware, and the month-4 acceptance tests include pulling one core link while traffic is running. [R1]

## 2.2 Server services and redundancy

The table below sets out where each service runs and how it is protected. I have split the services across the two hosts so that each host carries roughly half the load. The two domain controllers sit on different hosts, as do the mailbox server and its SMTP gateway, and the monitoring and logging servers.

| Service or device | Runs on | Resilience and security |
|---|---|---|
| DC1 (AD DS, DNS, DHCP) | HYP-01 | DC2 on the other host; AD and DNS replication and DHCP failover between the two. |
| DC2 (AD DS, DNS, DHCP) | HYP-02 | A second live domain-service instance that answers logons, DNS and DHCP in its own right. |
| SRV-WEB (internal intranet) | HYP-01 | Services VLAN 110; replica on HYP-02 and application-consistent backup. |
| SRV-HRDB | HYP-01 | HR-only application access; replica on HYP-02 plus vendor-supported database backup. |
| SRV-MKT-FS / SRV-CS-FS | HYP-02 | Separate shares and permissions; replicas on HYP-01 and versioned backup. |
| SRV-MAIL / SMTP-GW | HYP-02 / HYP-01 | Mailbox server in VLAN 110; relay and filter in the DMZ; controlled SMTP path and replicas on the opposite host. |
| SRV-MON / SRV-LOG | Opposite hosts | Zabbix for availability and capacity; Wazuh for central security events; both backed up to the NAS. |
| WLAN-CTRL / NAS-BACKUP | HYP-02 / physical NAS | Controller configuration backed up; the NAS holds backups only, while live VMs stay on each host's RAID 10 SSDs. |

*Table 3. Where each service runs and how it is protected.*

I use Hyper-V Replica to keep a recoverable copy of every application VM on the other host, replicating every 15 minutes, with a four-hour recovery-time target. Failover is a manual, verified step: an IT administrator confirms the primary host is down, starts the replica and checks the service before users are pointed at it. Application-consistent backups of the HR database continue alongside replication. Each host is sized to run all 11 services on its own after the other fails, and I will prove that in the acceptance tests. [R26]

RAID 10 on each host covers a failed disk. Deletion, corruption and loss of the building need a separate answer, so the NAS takes a daily versioned backup of every VM and share, and four encrypted removable targets rotate off site each week. My targets are an off-site gap of one business day at most and a documented restoration exercise every quarter. I would like you to confirm the retention and recovery targets before the build starts. [R27]

## 2.3 Single points of failure I have accepted

Each site keeps a single firewall, a single internet service and a single PBX, and the two-floor Brisbane building is one shared site. The two core links protect the LAN from a switch or cable failure; an ISP outage or a failed firewall still takes the site offline until the service is restored or the unit is replaced. I have accepted those risks for this budget and covered them with saved device configurations, a supplier replacement arrangement for the firewall, tested recovery and off-site copies, so a failure becomes a short, planned recovery. If HelpYou later needs uninterrupted internet or telephony, a second service and a second firewall at Brisbane would be the next investment.
