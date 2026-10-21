# Cisco build for Lab 8: SB-S1 - SB - ISP - MG - MG-S1 (written 2026-10-21)

Decisions recorded 2026-10-21: devices start blank (no capture); OSPF between sites; two computers, one at
each site. This is the complete configuration, in the order to type it, with the checks after each step.
Passwords are placeholders in angle brackets: choose them, type them, record them privately, never in the repo.

Revised 2026-10-21 after two reviews (syntax; design): `show controllers` filter fixed, checks qualified by build
order, vty 0 15, STP wait before switch pings, Windows firewall rule before host-to-host pings, VMware editor
fallback, CS-PC-1 placement, DNS tests before the join, evidence list completed, no-VPN and optional NTP notes.

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

No GRE/IPsec tunnel in this build: not required for Lab 8 and left out so there is nothing to troubleshoot; the
brief's `show interfaces tunnel 0` check is therefore not applicable. It can be added later without re-addressing.
There is no route out of the lab, so DC1 cannot reach an internet time source; that is normal for an isolated
lab (the VMs follow the host clocks). Optional, for the NTP and stratum written answers: on SB `clock set`
to the current time, then `ntp master 3`; on DC1 `w32tm /config /manualpeerlist:192.168.2.1
/syncfromflags:manual /reliable:yes /update` and `w32tm /resync`, giving a visible chain SB stratum 3, DC1
stratum 4, DC2 stratum 5.

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
`show controllers serial 0/0/0 | include DCE|DTE|cable`. Pass: a line beginning `DCE` on ISP and a line beginning
`DTE` on SB and MG (the rest of the line, V.35 or V.11, varies by cable and does not matter); `No serial cable
attached` means the plug is not seated.

Register item 9 is closed by design here: the devices are erased, so there is no old mapping left to verify;
Gi0/1 becomes the host access port in VLAN 90 and the trunk goes on Gi0/2, and Fa0/9-10 stay in VLAN 90 as in
the Lab 1 to 3 config. If `show inventory` shows an SB-S1 with no gigabit ports, record that the brief's port
name cannot be met on that chassis and name the FastEthernet port used.

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
line vty 0 15
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

Optional DHCP for VLANs 20 and 30. Note first: every VM on the SB computer is bridged through one cable into
SB-S1 Gi0/1, an access port in VLAN 90, so a CS-PC-1 VM on that computer lands in VLAN 90 and never sees these
pools. Default for CS-PC-1: static 192.168.2.6 (any of .6 to .13), mask 255.255.255.240, gateway 192.168.2.1,
DNS 192.168.2.2, and skip the pools. The pools are only useful if CS-PC-1 is given its own cable (a second NIC
on the SB computer into SB-S1 Fa0/1, VLAN 20, bridged to its own VMnet). Never run these pools together with a
Windows DHCP server on the same VLAN. If wanted, type after DC1 exists at 192.168.2.2:

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

Checks on SB, run now:
```
show ip interface brief        (G0/0 up/up showing "unassigned"; G0/0.20, .30, .90 up/up with 192.168.1.1, 192.168.1.65, 192.168.2.1 once SB-S1 is powered and cable 3 is in; S0/0/0 shows 209.165.200.1 and stays down until ISP is configured)
show ip protocols              (router-id 1.1.1.1; the three sub-interfaces listed as passive)
```
Run again after ISP is configured: `show ip ospf neighbor` (2.2.2.2, state FULL/  -  on Serial0/0/0) and
`ping 209.165.200.2`. Run again after MG is configured: `show ip route` (O routes to 172.16.0.0/24 and
209.165.200.16/28 via 209.165.200.2) and `ping 172.16.0.1`.

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

Checks on ISP, run now:
```
show controllers serial 0/0/0 | include DCE|DTE|cable     (a line beginning DCE)
show controllers serial 0/0/1 | include DCE|DTE|cable     (a line beginning DCE)
show ip interface brief        (S0/0/0 up/up now; S0/0/1 up/up only after MG is configured)
show ip ospf neighbor          (1.1.1.1 FULL now; 3.3.3.3 FULL only after MG is configured)
show ip route                  (O routes to 192.168.1.0/26, 192.168.1.64/26, 192.168.2.0/28 now; 172.16.0.0/24 after MG)
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

Checks on MG (SB and ISP already exist, so all of these should pass now):
```
show controllers serial 0/0/1 | include DCE|DTE|cable     (a line beginning DTE)
show ip interface brief        (G0/1 up/up once MG-S1 is powered and cabled; S0/0/1 up/up)
show ip ospf neighbor          (one neighbour, 2.2.2.2, FULL)
show ip route                  (four O routes: 192.168.2.0/28, 192.168.1.0/26, 192.168.1.64/26, 209.165.200.0/28)
ping 209.165.200.17
ping 192.168.2.1
```
Then back on ISP: `show ip ospf neighbor` now lists 1.1.1.1 and 3.3.3.3, both FULL (evidence screenshot).

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
 switchport nonegotiate
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

Checks on SB-S1 (wait 30 seconds after the uplink comes up: the trunk port spends that long in spanning-tree
listening and learning before it forwards; `show spanning-tree interface GigabitEthernet0/2` shows FWD when ready):
```
show vlan brief                (20, 30, 90 with the ports above; Gi0/2 absent because it is a trunk)
show interfaces trunk          (Gi0/2 trunking, 802.1q, VLANs 20,30,90 allowed and active)
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
 spanning-tree portfast
interface Vlan1
 description Management
 ip address 172.16.0.254 255.255.255.0
 no shutdown
ip default-gateway 172.16.0.1
end
write memory
```

Checks on MG-S1: `show interfaces status` (Fa0/1 and Gi0/1 connected, vlan 1); `ping 172.16.0.1` (wait 30
seconds after link-up if portfast was not applied).

## 9. The two computers

SB computer (runs DC1, later SB-DNS-2 and SB-FS2 as VMs): wired NIC cabled to SB-S1 Gi0/1. In VMware
Workstation: Edit > Virtual Network Editor > Change Settings (needs a local administrator) > VMnet0 > Bridged
to: **that NIC by name**, not Automatic. If the editor cannot be opened (TAFE lab PC without administrator
rights): keep exactly ONE wired NIC live (TAFE cable out, lab cable in the built-in NIC, Wi-Fi off) and leave
VMnet0 on Automatic; it bridges to the only connected adapter. Do not run two live NICs without the editor,
or VMware may bridge the DC onto the TAFE network. The host NIC needs no IP address of its own for bridging
("Unidentified network" on the host is fine). Each VM: Network Adapter = Bridged. Inside DC1: 192.168.2.2 / 255.255.255.240 / gateway 192.168.2.1 / DNS 192.168.2.2
(itself) once promoted, 127.0.0.1 as alternate.

MG computer (runs DC2): wired NIC cabled to MG-S1 Fa0/1, VMnet0 bridged to it the same way. Inside DC2:
172.16.0.2 / 255.255.255.0 / gateway 172.16.0.1 / DNS 192.168.2.2 (DC1), alternate 127.0.0.1 after promotion.

If a computer also needs the TAFE network (student.tafe, 172.30.96.x) at the same time, give it a USB
Ethernet adapter for the lab cable and bridge VMnet0 to the USB adapter; the built-in NIC stays on TAFE.

Quick test from the computers themselves, before any VM: SB computer 192.168.2.13 / 255.255.255.240 / gateway
192.168.2.1; MG computer 172.16.0.253 / 255.255.255.0 / gateway 172.16.0.1; each pings its own gateway and the
far gateway. Set the adapters back to automatic afterwards (never leave .2 or .3 on a host: those are DC
addresses).

End-to-end test from inside each DC (PowerShell). An unpromoted Windows Server does not answer ping (Public
profile), so first, as Administrator on each DC:
`Enable-NetFirewallRule -DisplayName "File and Printer Sharing (Echo Request - ICMPv4-In)"`. Then:
```
ping 192.168.2.1 ; ping 172.16.0.1 ; ping 172.16.0.2        (from DC1)
ping 172.16.0.1 ; ping 192.168.2.1 ; ping 192.168.2.2        (from DC2)
tracert -d 172.16.0.2                                        (from DC1: 192.168.2.1, 209.165.200.2, 209.165.200.18, 172.16.0.2)
```
A tracert that reaches 209.165.200.18 and then times out proves all three routers; only the far host's firewall
is left. Then, from DC2 before the domain join (after DC1 is promoted):
```
Test-NetConnection 192.168.2.2 -Port 53
Test-NetConnection 192.168.2.2 -Port 389
Resolve-DnsName dc1.<domain> -Server 192.168.2.2
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.<domain> -Server 192.168.2.2
```
and after DC2 is promoted, from DC1: `Test-NetConnection 172.16.0.2 -Port 389` and `-Port 445`. After
promotion the DC firewall rules allow AD, DNS, Kerberos, RPC 135 and the dynamic range; nothing on the routers
filters anything in this build.

## 10. Evidence to capture for the network part

* Every device, after `write memory`: `terminal length 0`, `show running-config`, `show ip interface brief` into
  the PuTTY log (these replace the five old CONFIG.txt files as the configuration record; check that only
  hashed secrets and type-7 line passwords appear before the log goes into the repo).
* ISP: `show ip ospf neighbor` with both neighbours FULL.
* SB and MG: `show ip route` showing the far site's networks as `O` routes.
* SB-S1: `show vlan brief`, `show interfaces trunk`, and with the SB computer and its VMs running
  `show mac address-table dynamic` and `show interfaces status` (VM MACs start 00:0c:29; proves the hosts sit
  on Gi0/1 in VLAN 90, register item 9). MG-S1: the same for Fa0/1 in VLAN 1.
* DC1 and DC2: the ping, tracert and DNS results above.
* A photo of the cabled rack matching the table in section 2.

## 11. Order of work at the rack

1. Erase all devices (`Cisco_reset_and_rebuild_2026-10-21.md`, Part 2; `show version | include register`
   before each router reload; after the blank boot `show inventory` (HWIC-2T in slot 0; switch model) and
   `show ip interface brief` (Serial0/0/0 and 0/0/1 listed; Gi0/1 and Gi0/2 on the 2960s) to confirm the names).
2. Cable per section 2, routers first.
3. Common block (section 3) on all five devices, then SB, ISP, MG, SB-S1, MG-S1 in that order, `write memory`
   after each, running the checks marked "run now" as you go and the deferred ones when their precondition is
   met. Stop at the first "run now" check that fails and report what it printed.
4. Cable the two computers, set VMware bridging, run the end-to-end test from the VMs (or from the computers
   themselves first, with a static address in the right subnet, if the VMs are not ready).
5. Capture the evidence in section 10.
