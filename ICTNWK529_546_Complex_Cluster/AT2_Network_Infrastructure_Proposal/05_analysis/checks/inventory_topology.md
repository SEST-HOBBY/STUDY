# Packet Tracer inventory: Helpyou_Network_Topology.pkt (topo.xml)

Source: `/tmp/claude-0/-home-user-STUDY/f8a3790f-8c1d-5a3f-8f9c-d2abf23b0604/scratchpad/pkt/topo.xml` (decrypted from Helpyou_Network_Topology.pkt, Packet Tracer 8.2.1.0118). Everything below is read from the XML; nothing is inferred from the screenshot.

## Headline answers

- Devices: **31** (2 x 2960 switches named CORE 1/CORE 2, 1 generic DMZ switch, 1 ASA 5505 named FortiGate, 1 ISP cloud, 4 servers, 21 PCs, 1 power distribution unit).
- Links: **27**, all copper (26 straight-through, 1 crossover).
- Core-to-core links: **1** (CORE 1 GigabitEthernet0/1 <-> CORE 2 GigabitEthernet0/1, crossover). The draft and brief say two; the file has one.
- Firewall to core switch: **no**. The firewall's only cable is ISP-1 Cloud:Ethernet6 <-> Firewall – FortiGate:Ethernet0/0 (the ISP cloud). It touches neither CORE 1 nor CORE 2 nor the DMZ switch.
- DMZ Switch connected to anything: **no**. Zero cables on it.
- Departments with PCs (by device name): Executive 5, Customer Service 2, Managers 2, Admin 4, Marketing 4, HR 2, IT 2 (total 21 PCs). Each department has a few representative PCs with '. . .' notes between them, matching the case-study head counts 5/5/5/10/10/3/2.
- Author-configured IP addresses: **none**. Every PC and server port has blank IP, mask and gateway with DHCP off. Both 2960s and the DMZ switch run the untouched PT default config (hostname Switch, VLAN 1 only, Vlan1 shut). The only IPv4 address in the file is the ASA 5505 factory default (inside 192.168.1.1/24, outside DHCP, dhcpd pool 192.168.1.5-36), which PT writes into every new ASA 5505.
- VLANs beyond default: **none** on any switch (VLAN 1, 1002-1005 only).
- Physical workspace: **PT default hierarchy only** (Intercity > Home City > Corporate Office > Main Wiring Closet > Rack). No custom building, no second floor, no Cairns. 10 rack-mounted devices sit in the single default Rack; the 21 PCs sit on the Corporate Office floor outside the closet.

## 1. Device inventory

| # | Name | PT type | PT model | Logical X,Y | Ports | Used | Physical location | Config beyond default |
|---|------|---------|----------|-------------|-------|------|-------------------|-----------------------|
| 0 | CORE 1 | Switch | 2960-24TT | 1041,636 | 26 | 13 | Corporate Office > Main Wiring Closet > Rack (offset 7) | no |
| 1 | Power Distribution Device0 | Power Distribution Device | Power Distribution Device | 3897,3900 | 0 | 0 | Corporate Office > Main Wiring Closet > Rack (offset 3) | no |
| 2 | CORE 2 | Switch | 2960-24TT | 1556,638 | 26 | 14 | Corporate Office > Main Wiring Closet > Rack (offset 11) | no |
| 3 | SRV-WEB | Server | Server-PT | 1569.5,872 | 1 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 19) | no |
| 4 | SRV-HRDB | Server | Server-PT | 1681.5,873 | 1 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 35) | no |
| 5 | SRV-MKT-FS | Server | Server-PT | 1871.5,867 | 1 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 51) | no |
| 6 | SRV-CS-FS | Server | Server-PT | 1774.5,873 | 1 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 67) | no |
| 7 | Excutive-3 | Pc | PC-PT | 1032.5,760 | 1 | 1 | Corporate Office | no |
| 8 | Excutive-1 | Pc | PC-PT | 703.5,768 | 1 | 1 | Corporate Office | no |
| 9 | Excutive-2 | Pc | PC-PT | 705.5,863 | 1 | 1 | Corporate Office | no |
| 10 | Excutive-4 | Pc | PC-PT | 1038.5,858 | 1 | 1 | Corporate Office | no |
| 11 | Excutive-5 | Pc | PC-PT | 1133.5,760 | 1 | 1 | Corporate Office | no |
| 12 | CS-1 | Pc | PC-PT | 894.5,355 | 1 | 1 | Corporate Office | no |
| 13 | CS-5 | Pc | PC-PT | 892.5,478 | 1 | 1 | Corporate Office | no |
| 14 | Manager-5 | Pc | PC-PT | 1136.5,470 | 1 | 1 | Corporate Office | no |
| 15 | Manager-1 | Pc | PC-PT | 1138.5,347 | 1 | 1 | Corporate Office | no |
| 16 | Admin-1 | Pc | PC-PT | 1565.5,325 | 1 | 1 | Corporate Office | no |
| 17 | Admin-5 | Pc | PC-PT | 1579.5,450 | 1 | 1 | Corporate Office | no |
| 18 | Admin-6 | Pc | PC-PT | 1817.5,328 | 1 | 1 | Corporate Office | no |
| 19 | Admin-10 | Pc | PC-PT | 1815.5,451 | 1 | 1 | Corporate Office | no |
| 20 | Marketing-10 | Pc | PC-PT | 1821.5,196 | 1 | 1 | Corporate Office | no |
| 21 | Marketing-1 | Pc | PC-PT | 1587.5,72 | 1 | 1 | Corporate Office | no |
| 22 | Marketing-5 | Pc | PC-PT | 1585.5,195 | 1 | 1 | Corporate Office | no |
| 23 | Marketing-6 | Pc | PC-PT | 1823.5,73 | 1 | 1 | Corporate Office | no |
| 24 | HR-3 | Pc | PC-PT | 886.5,192 | 1 | 1 | Corporate Office | no |
| 25 | HR-1 | Pc | PC-PT | 888.5,69 | 1 | 1 | Corporate Office | no |
| 26 | IT-2 | Pc | PC-PT | 1134.5,174 | 1 | 1 | Corporate Office | no |
| 27 | IT-1 | Pc | PC-PT | 1131.5,76 | 1 | 1 | Corporate Office | no |
| 28 | Firewall – FortiGate | ASA | 5505 | 1328.5,1017 | 8 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 83) | ASA factory default only |
| 29 | ISP-1 Cloud | Cloud | Cloud-PT | 1017,1326 | 8 | 1 | Corporate Office > Main Wiring Closet > Rack (offset 102) | no |
| 30 | DMZ Switch | Switch | Switch-PT | 1504,1016 | 6 | 0 | Corporate Office > Main Wiring Closet > Rack (offset 15) | no |

Notes on the table: 'Logical X,Y' is the Logical workspace position. 'Offset' is the PT internal rack position (lower = higher in the rack). PT does not store port names in the PORT element; names are taken from each switch's running-config interface list, the Cloud-PT template (type sequence matches) and the PC-PT/Server-PT single FastEthernet0. PCs also carry a PT Bluetooth virtual port, which is not a network port and is not listed.

### 1.1 Port and interface detail

All ports on every device, with IP settings as stored. Blank means empty in the XML.

**[0] CORE 1** (Switch 2960-24TT), port names from RUNNINGCONFIG interface list.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Excutive-1:FastEthernet0 |
| FastEthernet0/2 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Excutive-2:FastEthernet0 |
| FastEthernet0/3 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | CS-5:FastEthernet0 |
| FastEthernet0/4 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | CS-1:FastEthernet0 |
| FastEthernet0/5 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/6 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/7 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/8 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Admin-5:FastEthernet0 |
| FastEthernet0/9 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/10 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/11 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/12 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Admin-1:FastEthernet0 |
| FastEthernet0/13 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Marketing-5:FastEthernet0 |
| FastEthernet0/14 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/15 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/16 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/17 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Marketing-1:FastEthernet0 |
| FastEthernet0/18 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | HR-1:FastEthernet0 |
| FastEthernet0/19 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/20 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | HR-3:FastEthernet0 |
| FastEthernet0/21 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/22 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/23 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | SRV-HRDB:FastEthernet0 |
| FastEthernet0/24 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | SRV-WEB:FastEthernet0 |
| GigabitEthernet0/1 | eCopperGigabitEthernet | 1000 Mbps | n/a (L2 port) | off | CORE 2:GigabitEthernet0/1 |
| GigabitEthernet0/2 | eCopperGigabitEthernet | 1000 Mbps | n/a (L2 port) | off | - |

Running config: PT default (IOS 12.2, hostname Switch, pvst, every interface bare, Vlan1 no ip address + shutdown, vty login). VLAN database: 1 default, 1002 fddi-default, 1003 token-ring-default, 1004 fddinet-default, 1005 trnet-default. VTP: domain blank, mode server, revision 0.

**[1] Power Distribution Device0** (Power Distribution Device Power Distribution Device), port names unknown template.

No network ports (power accessory).

**[2] CORE 2** (Switch 2960-24TT), port names from RUNNINGCONFIG interface list.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Excutive-3:FastEthernet0 |
| FastEthernet0/2 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Excutive-4:FastEthernet0 |
| FastEthernet0/3 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Excutive-5:FastEthernet0 |
| FastEthernet0/4 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Manager-5:FastEthernet0 |
| FastEthernet0/5 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/6 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/7 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/8 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Manager-1:FastEthernet0 |
| FastEthernet0/9 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Admin-10:FastEthernet0 |
| FastEthernet0/10 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/11 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/12 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/13 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Admin-6:FastEthernet0 |
| FastEthernet0/14 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Marketing-10:FastEthernet0 |
| FastEthernet0/15 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/16 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/17 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/18 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | Marketing-6:FastEthernet0 |
| FastEthernet0/19 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | IT-2:FastEthernet0 |
| FastEthernet0/20 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | IT-1:FastEthernet0 |
| FastEthernet0/21 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/22 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet0/23 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | SRV-MKT-FS:FastEthernet0 |
| FastEthernet0/24 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | SRV-CS-FS:FastEthernet0 |
| GigabitEthernet0/1 | eCopperGigabitEthernet | 1000 Mbps | n/a (L2 port) | off | CORE 1:GigabitEthernet0/1 |
| GigabitEthernet0/2 | eCopperGigabitEthernet | 1000 Mbps | n/a (L2 port) | off | - |

Running config: PT default (IOS 12.2, hostname Switch, pvst, every interface bare, Vlan1 no ip address + shutdown, vty login). VLAN database: 1 default, 1002 fddi-default, 1003 token-ring-default, 1004 fddinet-default, 1005 trnet-default. VTP: domain blank, mode server, revision 0.

**[3] SRV-WEB** (Server Server-PT), port names Server-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/24 |

**[4] SRV-HRDB** (Server Server-PT), port names Server-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/23 |

**[5] SRV-MKT-FS** (Server Server-PT), port names Server-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/23 |

**[6] SRV-CS-FS** (Server Server-PT), port names Server-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/24 |

**[7] Excutive-3** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/1 |

**[8] Excutive-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/1 |

**[9] Excutive-2** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/2 |

**[10] Excutive-4** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/2 |

**[11] Excutive-5** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/3 |

**[12] CS-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/4 |

**[13] CS-5** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/3 |

**[14] Manager-5** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/4 |

**[15] Manager-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/8 |

**[16] Admin-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/12 |

**[17] Admin-5** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/8 |

**[18] Admin-6** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/13 |

**[19] Admin-10** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/9 |

**[20] Marketing-10** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/14 |

**[21] Marketing-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/17 |

**[22] Marketing-5** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/13 |

**[23] Marketing-6** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/18 |

**[24] HR-3** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/20 |

**[25] HR-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 1:FastEthernet0/18 |

**[26] IT-2** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/19 |

**[27] IT-1** (Pc PC-PT), port names Pc-PT template.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0 | eCopperFastEthernet | 100 Mbps | none | off | CORE 2:FastEthernet0/20 |

**[28] Firewall – FortiGate** (ASA 5505), port names from RUNNINGCONFIG interface list.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| Ethernet0/0 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | ISP-1 Cloud:Ethernet6 |
| Ethernet0/1 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/2 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/3 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/4 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/5 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/6 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |
| Ethernet0/7 | eCopperEthernet | 10 Mbps | n/a (L2 port) | off | - |

ASA 5505 running config (PT factory default, unchanged): hostname ciscoasa; Ethernet0/0 switchport access vlan 2; Ethernet0/1-0/7 switchport access vlan 1; interface Vlan1 nameif inside, security-level 100, ip address 192.168.1.1 255.255.255.0; interface Vlan2 nameif outside, security-level 0, ip address dhcp; dhcpd address 192.168.1.5-192.168.1.36 inside; dhcpd enable inside. Startup config is identical apart from two PT timestamp comment lines.

**[29] ISP-1 Cloud** (Cloud Cloud-PT), port names Cloud-PT template (type sequence matches).

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| Serial0 | eSerial | 1.544 Mbps | n/a | off | - |
| Serial1 | eSerial | 1.544 Mbps | n/a | off | - |
| Serial2 | eSerial | 1.544 Mbps | n/a | off | - |
| Serial3 | eSerial | 1.544 Mbps | n/a | off | - |
| Modem4 | eModem | 0.056 Mbps | n/a | off | - |
| Modem5 | eModem | 0.056 Mbps | n/a | off | - |
| Ethernet6 | eCopperEthernet | 10 Mbps | n/a | off | Firewall – FortiGate:Ethernet0/0 |
| Coax7 | eCopperCoaxial | 1.544 Mbps | n/a | off | - |

**[30] DMZ Switch** (Switch Switch-PT), port names from RUNNINGCONFIG interface list.

| Port | PT type | Speed | IP / mask / gateway | DHCP | Connected to |
|------|---------|-------|---------------------|------|--------------|
| FastEthernet0/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet1/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet2/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet3/1 | eCopperFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet4/1 | eFiberFastEthernet | 100 Mbps | n/a (L2 port) | off | - |
| FastEthernet5/1 | eFiberFastEthernet | 100 Mbps | n/a (L2 port) | off | - |

Running config: PT default (IOS 12.1, hostname Switch, pvst, every interface bare, Vlan1 no ip address + shutdown, vty login). VLAN database: 1 default, 1002 fddi-default, 1003 token-ring-default, 1004 fddinet-default, 1005 trnet-default. VTP: domain blank, mode server, revision 0.

### 1.2 Switch port usage

| Switch | Ports | Used | Used ports |
|--------|-------|------|------------|
| CORE 1 | 26 | 13 | FastEthernet0/1, FastEthernet0/2, FastEthernet0/3, FastEthernet0/4, FastEthernet0/8, FastEthernet0/12, FastEthernet0/13, FastEthernet0/17, FastEthernet0/18, FastEthernet0/20, FastEthernet0/23, FastEthernet0/24, GigabitEthernet0/1 |
| CORE 2 | 26 | 14 | FastEthernet0/1, FastEthernet0/2, FastEthernet0/3, FastEthernet0/4, FastEthernet0/8, FastEthernet0/9, FastEthernet0/13, FastEthernet0/14, FastEthernet0/18, FastEthernet0/19, FastEthernet0/20, FastEthernet0/23, FastEthernet0/24, GigabitEthernet0/1 |
| DMZ Switch | 6 | 0 | none |

## 2. Links

Every LINK in the file, resolved by SAVE_REF_ID to device names. Length is the metres PT auto-calculates from the physical view (1 m inside the rack; 31-45 m from the rack to PCs on the building floor). All 27 links are marked functional.

| # | A side | B side | Media | Cable | Length m | In rack view |
|---|--------|--------|-------|-------|----------|--------------|
| 0 | SRV-WEB:FastEthernet0 | CORE 1:FastEthernet0/24 | eCopper | eStraightThrough | 1 | yes |
| 1 | SRV-HRDB:FastEthernet0 | CORE 1:FastEthernet0/23 | eCopper | eStraightThrough | 1 | yes |
| 2 | SRV-CS-FS:FastEthernet0 | CORE 2:FastEthernet0/24 | eCopper | eStraightThrough | 1 | yes |
| 3 | SRV-MKT-FS:FastEthernet0 | CORE 2:FastEthernet0/23 | eCopper | eStraightThrough | 1 | yes |
| 4 | CORE 1:GigabitEthernet0/1 | CORE 2:GigabitEthernet0/1 | eCopper | eCrossOver | 1 | yes |
| 5 | Excutive-1:FastEthernet0 | CORE 1:FastEthernet0/1 | eCopper | eStraightThrough | 42.8258 | yes |
| 6 | Excutive-2:FastEthernet0 | CORE 1:FastEthernet0/2 | eCopper | eStraightThrough | 40.6441 | yes |
| 7 | Excutive-3:FastEthernet0 | CORE 2:FastEthernet0/1 | eCopper | eStraightThrough | 45.2756 | yes |
| 8 | Excutive-4:FastEthernet0 | CORE 2:FastEthernet0/2 | eCopper | eStraightThrough | 40.6441 | yes |
| 9 | Excutive-5:FastEthernet0 | CORE 2:FastEthernet0/3 | eCopper | eStraightThrough | 38.7757 | yes |
| 10 | CS-5:FastEthernet0 | CORE 1:FastEthernet0/3 | eCopper | eStraightThrough | 37.927 | yes |
| 11 | CS-1:FastEthernet0 | CORE 1:FastEthernet0/4 | eCopper | eStraightThrough | 40.3148 | yes |
| 12 | Manager-5:FastEthernet0 | CORE 2:FastEthernet0/4 | eCopper | eStraightThrough | 35.8518 | yes |
| 13 | Admin-5:FastEthernet0 | CORE 1:FastEthernet0/8 | eCopper | eStraightThrough | 34.1464 | yes |
| 14 | Admin-1:FastEthernet0 | CORE 1:FastEthernet0/12 | eCopper | eStraightThrough | 35.8518 | yes |
| 15 | Manager-1:FastEthernet0 | CORE 2:FastEthernet0/8 | eCopper | eStraightThrough | 37.927 | yes |
| 16 | Admin-10:FastEthernet0 | CORE 2:FastEthernet0/9 | eCopper | eStraightThrough | 32.8682 | yes |
| 17 | Admin-6:FastEthernet0 | CORE 2:FastEthernet0/13 | eCopper | eStraightThrough | 34.1464 | yes |
| 18 | Marketing-5:FastEthernet0 | CORE 1:FastEthernet0/13 | eCopper | eStraightThrough | 32.8682 | yes |
| 19 | Marketing-1:FastEthernet0 | CORE 1:FastEthernet0/17 | eCopper | eStraightThrough | 34.1464 | yes |
| 20 | Marketing-10:FastEthernet0 | CORE 2:FastEthernet0/14 | eCopper | eStraightThrough | 30.8777 | yes |
| 21 | Marketing-6:FastEthernet0 | CORE 2:FastEthernet0/18 | eCopper | eStraightThrough | 32.8682 | yes |
| 22 | IT-2:FastEthernet0 | CORE 2:FastEthernet0/19 | eCopper | eStraightThrough | 34.1464 | yes |
| 23 | IT-1:FastEthernet0 | CORE 2:FastEthernet0/20 | eCopper | eStraightThrough | 35.8518 | yes |
| 24 | HR-1:FastEthernet0 | CORE 1:FastEthernet0/18 | eCopper | eStraightThrough | 37.927 | yes |
| 25 | HR-3:FastEthernet0 | CORE 1:FastEthernet0/20 | eCopper | eStraightThrough | 35.8518 | yes |
| 26 | ISP-1 Cloud:Ethernet6 | Firewall – FortiGate:Ethernet0/0 | eCopper | eStraightThrough | 1 | no |

Link groups:

- Core-to-core: 1 (link 4, GigabitEthernet0/1 both ends, crossover). The Gi0/2 port on each core is free.
- Servers: SRV-WEB and SRV-HRDB on CORE 1 Fa0/24 and Fa0/23; SRV-CS-FS and SRV-MKT-FS on CORE 2 Fa0/24 and Fa0/23. All at 100 Mbps.
- PCs: 10 on CORE 1, 11 on CORE 2, all FastEthernet0 to a Fa0/x port at 100 Mbps.
- Firewall: 1 link, ISP-1 Cloud:Ethernet6 <-> Firewall – FortiGate:Ethernet0/0. Ethernet0/0 is the ASA's factory 'outside' VLAN 2 port, so the cable is on the correct side of the firewall, but the inside side goes nowhere.
- DMZ Switch: 0 links.
- ISP-1 Cloud: 1 link (to the firewall).
- Power Distribution Device0: no ports, no links.

## 3. Departments and PC placement

| Department (device prefix) | PCs drawn | PC names | Uplink switch(es) |
|----------------------------|-----------|----------|-------------------|
| Executive (named 'Excutive' in the file) | 5 | Excutive-3, Excutive-1, Excutive-2, Excutive-4, Excutive-5 | CORE 1, CORE 2 |
| Customer Service (CS) | 2 | CS-1, CS-5 | CORE 1 |
| Managers | 2 | Manager-5, Manager-1 | CORE 2 |
| Admin | 4 | Admin-1, Admin-5, Admin-6, Admin-10 | CORE 1, CORE 2 |
| Marketing | 4 | Marketing-10, Marketing-1, Marketing-5, Marketing-6 | CORE 1, CORE 2 |
| HR | 2 | HR-3, HR-1 | CORE 1 |
| IT | 2 | IT-2, IT-1 | CORE 2 |

The PC numbering (for example Admin-1, Admin-5, Admin-6, Admin-10) with '. . .' notes between the icons shows that each department is drawn as a sample of its case-study head count: 5 executives, 5 managers, 5 customer-service, 10 admin, 10 marketing, 3 HR and 2 IT (the original 40-staff office). Executives, Admin and Marketing are split across both switches; CS and HR are on CORE 1 only; Managers and IT on CORE 2 only.

### 3.1 Logical-view annotations (notes and coloured rectangles)

Text notes on the logical view: Admin-Cube-1, Admin-Cube-2, CS-Cube, Executive Room 1, Executive Room 2, HR-Cube, IT-Cube, Manager-Cube, Marketing-Cube-1, Marketing-Cube-2, Server Room. Seven further notes contain only '. . .' (elided PCs) and seven are empty.

| Rectangle (x1,y1)-(x2,y2) | RGB | Filled | Label inside | Devices inside |
|---------------------------|-----|--------|--------------|----------------|
| (1492,678)-(1985,929) | 85,255,127 | no | Server Room | SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS |
| (590,658)-(851,929) | 85,170,255 | yes | Executive Room 1 | Excutive-1, Excutive-2 |
| (810,298)-(991,531) | 255,255,127 | yes | CS-Cube | CS-1, CS-5 |
| (1738,8)-(1923,254) | 170,0,255 | yes | Marketing-Cube-2 | Marketing-10, Marketing-6 |
| (1984,928)-(1985,929) | 85,255,127 | no | (degenerate 1x1 px, stray click) | - |
| (983,695)-(1229,929) | 85,170,255 | yes | Executive Room 2 | Excutive-3, Excutive-4, Excutive-5 |
| (1062,294)-(1233,533) | 255,170,255 | yes | Manager-Cube | Manager-5, Manager-1 |
| (1490,272)-(1681,529) | 85,255,127 | yes | Admin-Cube-1 | Admin-1, Admin-5 |
| (1740,266)-(1923,525) | 85,255,127 | yes | Admin-Cube-2 | Admin-6, Admin-10 |
| (815,18)-(989,266) | 0,0,255 | yes | HR-Cube | HR-3, HR-1 |
| (1499,6)-(1675,260) | 170,0,255 | yes | Marketing-Cube-1 | Marketing-1, Marketing-5 |
| (1078,22)-(1228,263) | 0,170,127 | yes | IT-Cube | IT-2, IT-1 |

The large unfilled green rectangle (1492,678)-(1985,929) is the 'Server Room' box and holds the four servers. Neither core is inside any box: CORE 1 (1041,636) sits just above the Executive Room 2 box and CORE 2 (1556,638) just above the Server Room box. The firewall (1328,1017), DMZ Switch (1504,1016) and ISP cloud (1017,1326) sit below everything with no box or label. The Power Distribution Device is parked far off-canvas at (3897,3900).

## 4. Physical workspace

The PHYSICALWORKSPACE tree is exactly the Packet Tracer default and nothing else:

```
Intercity (type 0)
  Home City (type 1)
    Corporate Office (type 2)
      Main Wiring Closet (type 3)
        Rack (type 4)
          Power Distribution Device0 (offset 3)
          CORE 1 (offset 7)
          CORE 2 (offset 11)
          DMZ Switch (offset 15)
          SRV-WEB (offset 19)
          SRV-HRDB (offset 35)
          SRV-MKT-FS (offset 51)
          SRV-CS-FS (offset 67)
          Firewall – FortiGate (offset 83)
          ISP-1 Cloud (offset 102)
      [21 PCs placed directly on the Corporate Office floor, outside the closet]
```

- Only the default Intercity / Home City / Corporate Office / Main Wiring Closet / Rack hierarchy exists. No additional building, floor, closet, rack, table or city was created. No Cairns site. HOMERACK points at the default Main Wiring Closet.
- No background image is attached to any physical node (the two-floor plan in the student's screenshot comes from floor.xml, not this file).

### 4.1 Rack contents, top to bottom (by PT offset)

| Order | Device | PT model | Offset |
|-------|--------|----------|--------|
| 1 | Power Distribution Device0 | Power Distribution Device | 3 |
| 2 | CORE 1 | 2960-24TT | 7 |
| 3 | CORE 2 | 2960-24TT | 11 |
| 4 | DMZ Switch | Switch-PT | 15 |
| 5 | SRV-WEB | Server-PT | 19 |
| 6 | SRV-HRDB | Server-PT | 35 |
| 7 | SRV-MKT-FS | Server-PT | 51 |
| 8 | SRV-CS-FS | Server-PT | 67 |
| 9 | Firewall – FortiGate | 5505 | 83 |
| 10 | ISP-1 Cloud | Cloud-PT | 102 |

The ISP-1 Cloud is mounted in the rack as if it were equipment. The DMZ Switch is racked between CORE 2 and SRV-WEB even though it is not cabled.

### 4.2 PCs on the building floor

| PC | Building X,Y |
|----|--------------|
| Excutive-3 | 86,215 |
| Excutive-1 | 136,165 |
| Excutive-2 | 186,115 |
| Excutive-4 | 186,115 |
| Excutive-5 | 236,65 |
| CS-1 | 172,215 |
| CS-5 | 222,165 |
| Manager-5 | 272,115 |
| Manager-1 | 222,165 |
| Admin-1 | 272,115 |
| Admin-5 | 322,65 |
| Admin-6 | 322,65 |
| Admin-10 | 372,15 |
| Marketing-10 | 422,0 |
| Marketing-1 | 322,65 |
| Marketing-5 | 372,15 |
| Marketing-6 | 372,15 |
| HR-3 | 272,115 |
| HR-1 | 222,165 |
| IT-2 | 322,65 |
| IT-1 | 272,115 |

Several PCs share identical floor coordinates (for example Excutive-2 and Excutive-4 at 186,115; Admin-5, Admin-6, Marketing-1 and IT-2 at 322,65), so they overlap in the physical view. PT derived the 31-45 m cable lengths from these positions.

## 5. Names that do not match the PT model

| Device name(s) | Actual PT model | Comment |
|----------------|-----------------|---------|
| CORE 1 / CORE 2 | Cisco Catalyst 2960-24TT (Switch) | Named as core switches but drawn with a 24-port 10/100 access switch (24 x FastEthernet 100 Mbps + 2 x GigabitEthernet 1 Gbps). The draft proposes Cisco C1300-12XS cores. |
| Firewall – FortiGate | Cisco ASA 5505 (ASA) | Named FortiGate but is a Cisco ASA 5505 with 8 x Ethernet0/0-0/7 ports (PT stores BANDWIDTH 10000 kbps on each). The draft proposes a FortiGate 70G. |
| DMZ Switch | Switch-PT (generic PT switch) | Generic 6-port Packet Tracer switch (FastEthernet0/1, 1/1, 2/1, 3/1 copper; 4/1, 5/1 fibre), not a Cisco model. The draft proposes a Cisco C1300-24T-4X. |
| ISP-1 Cloud | Cloud-PT | Generic PT WAN cloud (Serial0-3, Modem4, Modem5, Ethernet6, Coax7). |
| SRV-WEB, SRV-HRDB, SRV-MKT-FS, SRV-CS-FS | Server-PT | Generic PT servers named for the existing Web, HR database, Marketing file and Customer Service file server roles; no services or IPs set (HTTP service is on by PT default). |
| Excutive-*, CS-*, Manager-*, Admin-*, Marketing-*, HR-*, IT-* | PC-PT | Generic PT PCs; 'Excutive' is a misspelling of Executive in all five names. |
| Power Distribution Device0 | Power Distribution Device | PT default name, no network ports; rack accessory only. |

Keyword hits: FortiGate -> Firewall – FortiGate; DMZ -> DMZ Switch; ISP -> ISP-1 Cloud; CORE -> CORE 1, CORE 2.

Other naming points: 'Excutive' (sic) on all five executive PCs; the firewall name uses an en dash ('Firewall – FortiGate'); 'Power Distribution Device0' is the PT default name; the ASA hostname is still 'ciscoasa' and the switches' hostname is still 'Switch'.

## 6. Where the file differs from the draft report

- Draft section 2 states 'CORE 1 <-> CORE 2: two separate links' and the brief says two links between the core switches; topo.xml has exactly ONE core-to-core link (CORE 1 Gi0/1 <-> CORE 2 Gi0/1, crossover copper).
- Draft describes 'Brisbane ISP handoff -> FW-HQ -> core pair'; in topo.xml the firewall's only cable goes to ISP-1 Cloud (Ethernet6 <-> Ethernet0/0). No cable from the firewall to CORE 1 or CORE 2.
- Draft describes 'FW-HQ -> DMZ switch -> SMTP gateway'; in topo.xml the DMZ Switch has zero cables and nothing is attached to it.
- Draft proposes floor-based access switches feeding the cores; topo.xml has no access switches. All 21 PCs and all 4 servers cable directly into the two 2960s named CORE 1 / CORE 2 on 100 Mbps FastEthernet ports.
- Draft proposes DCs, DHCP/DNS, SNMP monitoring, mail, hypervisors, IP PBX, APs, Cairns site and VPN; none of these appear in topo.xml. The four servers present are the EXISTING roles (Web, HR DB, Marketing FS, CS FS).
- Topo.xml therefore reads as the existing 40-staff office (two cross-linked 24-port 10/100 switches with one 1 Gbps inter-switch link, four servers, statically named PCs) plus three proposed items (firewall, ISP cloud, DMZ switch) placed in the rack but not wired to the LAN.
- Draft section 3 says the two-floor Packet Tracer overlay is Figure 1; topo.xml has only the PT default single building and one rack, no second floor, no Cairns. (The two-floor overlay comes from floor.xml, a different, later file with 33 devices and 32 links and different device names.)
- Draft section 5 lists VLANs 10-210 and static IPs; topo.xml has no VLANs beyond PT defaults and no author-set IP on any device.

## 7. Cross-check: floor.xml (FLOOR_PLAN_FINAL.pkt) is a different drawing

Not inventoried in depth here, but to avoid conflating the two files: floor.xml has 33 devices and 32 links with different names (four 2960s named Switch0-3, an ASA 5506-X named ASA0, Cloud0, six servers including 'WEB SERVER', 'DHCP + DNS', 'NET MONITOR SERVER', 'APP SERVER', two VoIP phones, a laptop, a lightweight AP 'Guest WiFi', two PDUs and PCs named HR-1/HR-2, ADMIN-1/2, EXEC-1/2, MGMT-1/2, CUST-1/2, MRKT-1/2, IT-1/2). Switch-to-switch links in floor.xml: Switch1:FastEthernet0/5 <-> Switch0:FastEthernet0/1; Switch3:FastEthernet0/3 <-> Switch2:FastEthernet0/2; Switch0:GigabitEthernet0/1 <-> Switch2:GigabitEthernet0/1; Switch0:GigabitEthernet0/2 <-> Switch3:GigabitEthernet0/1; Switch1:GigabitEthernet0/1 <-> Switch2:GigabitEthernet0/2; Switch1:GigabitEthernet0/2 <-> Switch3:GigabitEthernet0/2; Switch0:FastEthernet0/24 <-> Switch2:FastEthernet0/24; Switch1:FastEthernet0/24 <-> Switch3:FastEthernet0/24. Author-set IPs in floor.xml: VoIP-1, VoIP-2.
