# 5. IP Scheme

This section sets out the private IPv4 addressing for every VLAN in my design, and the fixed addresses I assign to the servers, the network equipment and the other devices that need one. The departmental host requirements come from the interview handout; the sizes of the supporting zones (voice, guest, DMZ, services, management, backup, staff Wi-Fi and transit) are my own allowances. [P2] VLAN numbers follow the department order 10 to 70, then 80 voice, 90 guest, 100 to 140 services, 210 to 280 Cairns and 900 transit. For Brisbane I have made the third octet match the VLAN number, so VLAN 30 is 192.168.30.0 and VLAN 120 is 192.168.120.0, which makes a packet capture or a routing table easy to read. Cairns uses the 10.20.0.0 range so that branch routes stand out on both firewalls and across the VPN. Figure 2 in section 2 carries the same VLAN numbers and subnets; my Packet Tracer drawings show what connects to what, and the addressing lives in the two tables here.

I sized each subnet from its five-year device count and rounded up to the next prefix that leaves headroom. Executives (30 devices), Managers, Admin and IT user devices (40 each) sit in /26 networks with 62 usable addresses. A /27 would give Executives only 30 usable addresses, and the gateway takes one of them, so a /26 is the smallest prefix that fits. Marketing and Customer Service each forecast 50 devices, so I have used /25 networks with 126 usable addresses, which leaves both departments room to keep growing past the five-year figure. HR, at 20 devices, fits a /27 with 30 usable addresses.

The supporting zones follow the same approach. Brisbane voice is a /25 so that 126 addresses cover one phone for each of the 108 forecast staff plus the PBX. Guests and staff Wi-Fi each get a /24, because visitor and laptop numbers are the hardest to predict and private address space costs nothing. The DMZ and the backup network are /27s, since each holds a handful of servers and interfaces. Internal services and device management are /26s, giving 62 addresses each for the 11 virtual servers, two hosts, NAS, PBX, switches, access points and firewall. The core-to-firewall transit is a /29 with six usable addresses, of which two are used. Cairns has a /26 for its staff devices, a /27 for its switch and access point, and a /27 for its eight phones.

| VLAN | Name | Network / prefix | Gateway | Requirement / usable |
|---|---|---|---|---|
| 10 | Executives | 192.168.10.0/26 | 192.168.10.1 | 30 / 62 |
| 20 | Managers | 192.168.20.0/26 | 192.168.20.1 | 40 / 62 |
| 30 | Marketing | 192.168.30.0/25 | 192.168.30.1 | 50 / 126 |
| 40 | Customer Service | 192.168.40.0/25 | 192.168.40.1 | 50 / 126 |
| 50 | Admin | 192.168.50.0/26 | 192.168.50.1 | 40 / 62 |
| 60 | HR | 192.168.60.0/27 | 192.168.60.1 | 20 / 30 |
| 70 | IT user devices | 192.168.70.0/26 | 192.168.70.1 | 40 / 62 |
| 80 | Brisbane voice | 192.168.80.0/25 | 192.168.80.1 | 108 assumed / 126 |
| 90 | Brisbane guests | 192.168.90.0/24 | 192.168.90.1 | 100 assumed / 254 |
| 100 | DMZ | 192.168.100.0/27 | 192.168.100.1 | 10 allowed / 30 |
| 110 | Internal services | 192.168.110.0/26 | 192.168.110.1 | 30 allowed / 62 |
| 120 | Device management | 192.168.120.0/26 | 192.168.120.1 | 40 allowed / 62 |
| 130 | Backup / replication | 192.168.130.0/27 | None - isolated | 10 allowed / 30 |
| 140 | Staff Wi-Fi | 192.168.140.0/24 | 192.168.140.1 | 150 allowed / 254 |
| 210 | Cairns staff | 10.20.10.0/26 | 10.20.10.1 | 16 allowed / 62 |
| 220 | Cairns management | 10.20.20.0/27 | 10.20.20.1 | 10 allowed / 30 |
| 280 | Cairns voice | 10.20.80.0/27 | 10.20.80.1 | 8 required / 30 |
| 900 | Core / firewall transit | 192.168.254.0/29 | 192.168.254.1 | 2 used / 6 |

*Table 5. VLAN and subnet plan for Brisbane and Cairns.*

In every routed subnet the first usable address is the gateway. The usable ranges are .1 to .62 in a /26, .1 to .126 in a /25, .1 to .30 in a /27, .1 to .254 in a /24 and .1 to .6 in the /29 transit. The network and broadcast addresses stay unused, and the gateway takes one usable address from each range, which is why I compare each requirement against the usable count rather than the subnet size.

The guest and DMZ gateways (192.168.90.1 and 192.168.100.1) are interfaces on FW-HQ, so visitor and mail-relay traffic is inspected by the firewall before it reaches anything else. Every other Brisbane gateway is an interface on the core stack, and the stack's default route points at the firewall's transit address, 192.168.254.1. VLAN 130 is my isolated backup and replication network: the hosts' replication interfaces and the NAS backup port talk only to each other, with no gateway configured, so backup traffic stays off the routed network. At Cairns, FW-BR holds the three branch gateways and carries the site-to-site VPN. Public addresses come from the ISP.

## 5.1 Static server and infrastructure addresses

Table 6 lists every fixed address in the design. I keep the servers in the services VLAN 110 in the .10 to .24 block, with the two domain controllers first, and infrastructure management in VLAN 120 with a matching pattern: the hosts at .11 and .12, the monitoring and controller servers at .20 to .22, the NAS at .30, the access switches at .41 to .46, the DMZ switch at .47 and the access points at .51 to .56. Each block is numbered so that a device's role is obvious from its address alone.

| Device / role | VLAN | Static IP / prefix | Default gateway |
|---|---|---|---|
| DC1 / DNS / DHCP | 110 | 192.168.110.10/26 | 192.168.110.1 |
| DC2 / DNS / DHCP | 110 | 192.168.110.11/26 | 192.168.110.1 |
| SRV-WEB (internal) | 110 | 192.168.110.20/26 | 192.168.110.1 |
| SRV-HRDB | 110 | 192.168.110.21/26 | 192.168.110.1 |
| SRV-MKT-FS | 110 | 192.168.110.22/26 | 192.168.110.1 |
| SRV-CS-FS | 110 | 192.168.110.23/26 | 192.168.110.1 |
| SRV-MAIL | 110 | 192.168.110.24/26 | 192.168.110.1 |
| SMTP-GW (DMZ) | 100 | 192.168.100.10/27 | 192.168.100.1 |
| SRV-MON / Zabbix | 120 | 192.168.120.20/26 | 192.168.120.1 |
| SRV-LOG / Wazuh | 120 | 192.168.120.21/26 | 192.168.120.1 |
| WLAN-CTRL | 120 | 192.168.120.22/26 | 192.168.120.1 |
| Core stack management / SVI | 120 | 192.168.120.1/26 | n/a (core SVI; default route via 192.168.254.1) |
| FW-HQ management | 120 | 192.168.120.4/26 | n/a (firewall interface) |
| HYP-01 management | 120 | 192.168.120.11/26 | 192.168.120.1 |
| HYP-02 management | 120 | 192.168.120.12/26 | 192.168.120.1 |
| NAS management | 120 | 192.168.120.30/26 | 192.168.120.1 |
| PBX-01 | 80 | 192.168.80.10/25 | 192.168.80.1 |
| Brisbane access switches 1-6 | 120 | 192.168.120.41-.46/26 | 192.168.120.1 |
| Brisbane APs 1-6 | 120 | 192.168.120.51-.56/26 | 192.168.120.1 |
| DMZ switch management | 120 | 192.168.120.47/26 | 192.168.120.1 |
| Cairns switch / AP | 220 | 10.20.20.2-.3/27 | 10.20.20.1 |
| HYP-01 / HYP-02 replication | 130 | 192.168.130.11-.12/27 | None |
| NAS backup-data interface | 130 | 192.168.130.20/27 | None |
| Core transit / firewall inside | 900 | 192.168.254.2 / .1 /29 | Core next hop: .1 |

*Table 6. Static addresses for servers, network equipment and management interfaces.*

Every address in Table 6 sits inside its own subnet and is unique across the design. The device labels in the logical diagram (Figure 2) and the rack diagram (Figure 3) match these entries, so this table doubles as the static-IP register that IT will keep up to date after the build.

## 5.2 DHCP and reservations

DC1 and DC2 run DHCP for every Brisbane client VLAN, with failover between them, and I have set each scope to match Table 5. In the departmental /26 networks (Executives, Managers, Admin and IT) I reserve .1 to .9 for the gateway and any device that has to be set by hand, and give DHCP .10 to .62, which is 53 addresses for departments of 30 to 40 devices. HR's /27 uses .10 to .30, 21 addresses for the 20-device requirement. The Marketing and Customer Service /25 scopes run from .10 to .126, 117 addresses for 50 devices each. Brisbane voice uses .20 to .126 as its scope, 107 addresses, with PBX-01 static at .10 and .11 to .19 held back; if all 108 forecast phones arrive, adding that block takes the voice pool to 116. Staff Wi-Fi uses .10 to .254, 245 addresses for 150 devices.

FW-HQ runs the guest scope itself on VLAN 90, using the same .10 to .254 pattern, so visitor devices get their addresses from the firewall without touching the domain controllers. The Cairns staff and voice scopes (10.20.10.10 to .62 and 10.20.80.10 to .30) follow the same pattern and are served from DC1 and DC2 through the VPN, with FW-BR relaying the requests. The services, management, backup and transit networks have no scope at all; every address there is set by hand from Table 6, which keeps them out of every DHCP pool.

Printers are the end devices that need a fixed address. Rather than typing addresses into them, I give each printer a DHCP reservation in its department's scope once the printer inventory is confirmed, and record its MAC address and location against the reservation. The address stays fixed while all addressing remains under central control, and the same method covers any later device that needs a known address.

Every corporate client receives both DC1 (192.168.110.10) and DC2 (192.168.110.11) as its DNS servers, so name resolution continues if either host is down. Guest clients receive the approved external resolver from the firewall and stay outside the internal network.
