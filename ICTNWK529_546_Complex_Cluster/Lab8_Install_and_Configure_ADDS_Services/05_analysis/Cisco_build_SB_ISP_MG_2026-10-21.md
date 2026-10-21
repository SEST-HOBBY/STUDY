# Cisco build for Lab 8: SB-S1 - SB - ISP - MG - MG-S1 (written 2026-10-21)

Decisions recorded 2026-10-21: devices start blank (no capture); OSPF between sites; two computers, one at
each site. This is the complete configuration, in the order to type it, with the checks after each step.
Passwords are placeholders in angle brackets: choose them, type them, record them privately, never in the repo.

Interface names below assume the serial card in slot 0 (Serial0/0/0 and 0/0/1), as the photo shows on all
three routers, and gigabit uplinks on the 2960s. After the blank boot, `show inventory` and `show ip interface
brief` on each device confirm the names; if a 2960 turns out to have no GigabitEthernet ports (a -24-S model),
use FastEthernet0/23 and 0/24 where the build says Gi0/1 and Gi0/2.

## 1. Addressing (from the brief and the later lab work)

| Network | Where | Gateway | Hosts |
|---|---|---|---|
| 192.168.1.0/26 | SB VLAN 20 "CS" | 192.168.1.1 (SB G0/0.20) | clients, DHCP optional |
| 192.168.1.64/26 | SB VLAN 30 "Marketing" | 192.168.1.65 (SB G0/0.30) | clients, DHCP optional |
| 192.168.2.0/28 | SB VLAN 90 "Server" | 192.168.2.1 (SB G0/0.90) | DC1 .2, SB-DNS-2 .4, SB-FS2 .5, SB-S1 management .14 |
| 209.165.200.0/28 | SB to ISP serial | - | SB S0/0/0 .1, ISP S0/0/0 .2 |
| 209.165.200.16/28 | ISP to MG serial | - | ISP S0/0/1 .17, MG S0/0/1 .18 |
| 172.16.0.0/24 | MG LAN | 172.16.0.1 (MG G0/1) | DC2 .2, MG-S1 management .254 |

OSPF process 1, area 0 on all three routers; router IDs 1.1.1.1 (SB), 2.2.2.2 (ISP), 3.3.3.3 (MG). LAN
interfaces passive. Serial encapsulation HDLC (default), clock supplied by ISP (DCE ends) at 128000.

## 2. Cabling

| # | From | To | Cable |
|---|---|---|---|
| 1 | SB (2911) Serial0/0/0, **DTE** end | ISP (1941) Serial0/0/0, **DCE** end | smart-serial back-to-back |
| 2 | MG (1941) Serial0/0/1, **DTE** end | ISP (1941) Serial0/0/1, **DCE** end | smart-serial back-to-back |
| 3 | SB GigabitEthernet0/0 | SB-S1 GigabitEthernet0/2 (trunk) | straight-through Ethernet |
| 4 | MG GigabitEthernet0/1 | MG-S1 GigabitEthernet0/1 (access VLAN 1) | straight-through Ethernet |
| 5 | SB computer, wired NIC | SB-S1 GigabitEthernet0/1 (access VLAN 90) | straight-through Ethernet |
| 6 | MG computer, wired NIC | MG-S1 FastEthernet0/1 (access VLAN 1) | straight-through Ethernet |
| 7 | console | each device in turn | rollover or USB |

Why the host is on SB-S1 Gi0/1: the written assessment names Gi0/1 for the host (register item 9), and a gigabit
access port in VLAN 90 is the right place for a server; the trunk to the router moves to Gi0/2. Both are
gigabit, nothing is lost, and the brief's wording is met.

Both DCE ends go on ISP, so ISP supplies the clock on both links. Check each end after cabling:
`show controllers serial 0/0/0 | include cable` prints `DCE V.11 (X.21) cable` on ISP and `DTE ...` on SB.

## 3. Common first block (type on every device, routers and switches)

```
enable
configure terminal
no ip domain-lookup
service password-encryption
enable secret <enable-secret>
line console 0
 password <console-password>
 login
 logging synchronous
 exec-timeout 30 0
line vty 0 4
 password <vty-password>
 login
banner motd # Lab 8 <device> - authorised use only #
end
```

Then the device's own block below, then `write memory` (or `copy running-config startup-config`), then the
checks. (`end` is used at the end of each block so that `show` commands run from privileged mode.)

## 4. SB (Cisco 2911, chassis tape BNE / R1)

```
configure terminal
hostname SB
interface GigabitEthernet0/0
 description Trunk to SB-S1 Gi0/2
 no ip address
 no shutdown
interface GigabitEthernet0/0.20
 description VLAN 20 CS
 encapsulation dot1Q 20
 ip address 192.168.1.1 255.255.255.192
interface GigabitEthernet0/0.30
 description VLAN 30 Marketing
 encapsulation dot1Q 30
 ip address 192.168.1.65 255.255.255.192
interface GigabitEthernet0/0.90
 description VLAN 90 Server
 encapsulation dot1Q 90
 ip address 192.168.2.1 255.255.255.240
interface Serial0/0/0
 description WAN to ISP S0/0/0
 ip address 209.165.200.1 255.255.255.240
 no shutdown
router ospf 1
 router-id 1.1.1.1
 passive-interface GigabitEthernet0/0.20
 passive-interface GigabitEthernet0/0.30
 passive-interface GigabitEthernet0/0.90
 network 192.168.1.0 0.0.0.63 area 0
 network 192.168.1.64 0.0.0.63 area 0
 network 192.168.2.0 0.0.0.15 area 0
 network 209.165.200.0 0.0.0.15 area 0
end
write memory
```

Optional, only if a client on VLAN 20 or 30 should get an address automatically (CS-PC-1 for WP9). Type after
DC1 exists at 192.168.2.2, or now with the DNS line to be revisited:

```
configure terminal
ip dhcp excluded-address 192.168.1.1 192.168.1.10
ip dhcp excluded-address 192.168.1.65 192.168.1.74
ip dhcp pool VLAN20-CS
 network 192.168.1.0 255.255.255.192
 default-router 192.168.1.1
 dns-server 192.168.2.2
 domain-name <our-domain>
ip dhcp pool VLAN30-MARKETING
 network 192.168.1.64 255.255.255.192
 default-router 192.168.1.65
 dns-server 192.168.2.2
 domain-name <our-domain>
end
write memory
```

Checks on SB:
```
show ip interface brief        (G0/0 and its three sub-interfaces up/up with their addresses; S0/0/0 up/up once ISP is configured and cabled)
show ip ospf neighbor          (one neighbour, 2.2.2.2, state FULL/  -  on Serial0/0/0)
show ip route                  (after MG is configured: an O route to 172.16.0.0/24 via 209.165.200.2)
ping 209.165.200.2
ping 172.16.0.1
```

## 5. ISP (Cisco 1941, chassis tape ISP)

```
configure terminal
hostname ISP
interface Serial0/0/0
 description To SB S0/0/0 (DCE)
 ip address 209.165.200.2 255.255.255.240
 clock rate 128000
 no shutdown
interface Serial0/0/1
 description To MG S0/0/1 (DCE)
 ip address 209.165.200.17 255.255.255.240
 clock rate 128000
 no shutdown
router ospf 1
 router-id 2.2.2.2
 network 209.165.200.0 0.0.0.15 area 0
 network 209.165.200.16 0.0.0.15 area 0
end
write memory
```

If `clock rate` is refused with a message about the DTE end, the cable is the wrong way round on that link:
swap the ends, do not force it.

Checks on ISP:
```
show ip interface brief        (both serials up/up)
show controllers serial 0/0/0 | include cable     (DCE)
show controllers serial 0/0/1 | include cable     (DCE)
show ip ospf neighbor          (two neighbours, 1.1.1.1 and 3.3.3.3, both FULL)
show ip route                  (O routes to 192.168.1.0/26, 192.168.1.64/26, 192.168.2.0/28, 172.16.0.0/24)
```

## 6. MG (Cisco 1941, chassis tape CNS / R2)

```
configure terminal
hostname MG
interface GigabitEthernet0/1
 description MG LAN to MG-S1 Gi0/1
 ip address 172.16.0.1 255.255.255.0
 no shutdown
interface Serial0/0/1
 description WAN to ISP S0/0/1
 ip address 209.165.200.18 255.255.255.240
 no shutdown
router ospf 1
 router-id 3.3.3.3
 passive-interface GigabitEthernet0/1
 network 172.16.0.0 0.0.0.255 area 0
 network 209.165.200.16 0.0.0.15 area 0
end
write memory
```

Checks on MG:
```
show ip interface brief        (G0/1 up/up once MG-S1 is cabled; S0/0/1 up/up)
show ip ospf neighbor          (one neighbour, 2.2.2.2, FULL)
show ip route                  (O routes to 192.168.2.0/28, 192.168.1.0/26, 192.168.1.64/26)
ping 209.165.200.17
ping 192.168.2.1
```

## 7. SB-S1 (Catalyst 2960, chassis tape BNE S1)

```
configure terminal
hostname SB-S1
vlan 20
 name CS
vlan 30
 name Marketing
vlan 90
 name Server
interface range FastEthernet0/1 - 8
 description VLAN 20 CS clients
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
interface range FastEthernet0/11 - 18
 description VLAN 30 Marketing clients
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
interface range FastEthernet0/9 - 10
 description VLAN 90 servers
 switchport mode access
 switchport access vlan 90
 spanning-tree portfast
interface GigabitEthernet0/1
 description SB computer (DC1 host) - VLAN 90
 switchport mode access
 switchport access vlan 90
 spanning-tree portfast
interface GigabitEthernet0/2
 description Trunk to SB G0/0
 switchport mode trunk
 switchport trunk allowed vlan 20,30,90
interface Vlan1
 shutdown
interface Vlan90
 description Management
 ip address 192.168.2.14 255.255.255.240
 no shutdown
ip default-gateway 192.168.2.1
end
write memory
```

(The 2960 trunks are 802.1Q only, so there is no `switchport trunk encapsulation` command; if the switch
accepts it, it is harmless.) `spanning-tree portfast` prints a warning about hubs and loops; that is expected
on access ports.

Checks on SB-S1:
```
show vlan brief                (20, 30, 90 with the ports above; Gi0/2 absent because it is a trunk)
show interfaces trunk          (Gi0/2 trunking, VLANs 20,30,90 allowed and active)
show interfaces status         (Gi0/1 connected, vlan 90, once the SB computer is cabled)
ping 192.168.2.1               (from the switch, proves the SVI and the trunk)
```

## 8. MG-S1 (Catalyst 2960, chassis tape CNS S1, or the 2960 Plus)

```
configure terminal
hostname MG-S1
interface range FastEthernet0/1 - 2
 description MG computer (DC2 host)
 switchport mode access
 switchport access vlan 1
 spanning-tree portfast
interface GigabitEthernet0/1
 description Uplink to MG G0/1
 switchport mode access
 switchport access vlan 1
interface Vlan1
 description Management
 ip address 172.16.0.254 255.255.255.0
 no shutdown
ip default-gateway 172.16.0.1
end
write memory
```

Checks on MG-S1: `show interfaces status` (Fa0/1 and Gi0/1 connected, vlan 1); `ping 172.16.0.1`.

## 9. The two computers

SB computer (runs DC1, later SB-DNS-2 and SB-FS2 as VMs): wired NIC cabled to SB-S1 Gi0/1. In VMware
Workstation: Edit > Virtual Network Editor > VMnet0 > Bridged to: **that NIC by name**, not Automatic. Each VM:
Network Adapter = Bridged. Inside DC1: 192.168.2.2 / 255.255.255.240 / gateway 192.168.2.1 / DNS 192.168.2.2
(itself) once promoted, 127.0.0.1 as alternate.

MG computer (runs DC2): wired NIC cabled to MG-S1 Fa0/1, VMnet0 bridged to it the same way. Inside DC2:
172.16.0.2 / 255.255.255.0 / gateway 172.16.0.1 / DNS 192.168.2.2 (DC1), alternate 127.0.0.1 after promotion.

If a computer also needs the TAFE network (student.tafe, 172.30.96.x) at the same time, give it a USB
Ethernet adapter for the lab cable and bridge VMnet0 to the USB adapter; the built-in NIC stays on TAFE.

End-to-end test before any Windows domain work, from inside each DC (PowerShell):
```
ping 192.168.2.1 ; ping 172.16.0.1 ; ping 172.16.0.2        (from DC1)
ping 172.16.0.1 ; ping 192.168.2.1 ; ping 192.168.2.2        (from DC2)
tracert -d 172.16.0.2                                        (from DC1: 192.168.2.1, 209.165.200.2, 209.165.200.18, 172.16.0.2)
Test-NetConnection 192.168.2.2 -Port 389                     (from DC2, after DC1 is promoted: TcpTestSucceeded True)
```
Windows Firewall on a freshly promoted DC already allows AD, DNS and Kerberos; nothing on the routers filters
anything in this build.

## 10. Evidence to capture for the network part

* ISP: `show ip ospf neighbor` with both neighbours FULL.
* SB and MG: `show ip route` showing the far site's networks as `O` routes.
* SB-S1: `show vlan brief` and `show interfaces trunk`.
* DC1 and DC2: the ping and tracert results above.
* A photo of the cabled rack matching the table in section 2.

## 11. Order of work at the rack

1. Erase all devices (`Cisco_reset_and_rebuild_2026-10-21.md`, Part 2; `show version | include register`
   before each router reload; after the blank boot `show inventory` to confirm the interface names).
2. Cable per section 2, routers first.
3. Common block (section 3) on all five devices, then SB, ISP, MG, SB-S1, MG-S1 in that order, `write memory`
   after each, running the checks as you go. Stop at the first check that fails and report what it printed.
4. Cable the two computers, set VMware bridging, run the end-to-end test from the VMs (or from the computers
   themselves first, with a static address in the right subnet, if the VMs are not ready).
5. Capture the evidence in section 10.
