# Lab 8 walkthrough: cabling, console and configs, then the PCs and VMs (2026-10-21)

Companion to `Cisco_reset_and_rebuild_2026-10-21.md` (erase) and `Cisco_build_SB_ISP_MG_2026-10-21.md` (the
full configs). This file is the order of operations with what to look for at each step. Chassis labels are used
only as handles for which box is which.

What you need on the bench: 2 smart-serial back-to-back cables; 4 straight-through Ethernet patch leads
(2 router-to-switch, 2 for the computers); 1 console cable (blue RJ45 rollover with a USB-to-serial adapter, or
a USB A-to-mini-B lead for the routers' mini-USB console); the two computers with VMware Workstation; the
Server 2019 ISO on `E:`.

---

## Part A. Cabling

Do this with the devices powered on; nothing is configured yet, so nothing can go wrong, and the link LEDs tell
you each cable is good.

### A.1 Serial links (routers only)

Each back-to-back smart-serial cable has one connector moulded **DTE** and one moulded **DCE** (read the
moulding; some cables also have a label). The HWIC-2T card in slot 0 has two small smart-serial sockets,
left = Serial0/0/0, right = Serial0/0/1 (the card prints `0` and `1`, or `SERIAL 0` / `SERIAL 1`).

| Cable | Plug the DCE end into | Plug the DTE end into |
|---|---|---|
| 1 | **ISP** (1941, tape ISP), Serial0/0/0 (left socket) | **SB** (2911, tape BNE/R1), Serial0/0/0 (left socket) |
| 2 | **ISP**, Serial0/0/1 (right socket) | **MG** (1941, tape CNS/R2), Serial0/0/1 (right socket) |

The connector only goes in one way; push until the thumb screws reach the socket, then tighten them finger-tight.
Serial ports have no link LED until configured; you will check them in Part B with `show controllers`.

### A.2 Router to switch

| Cable | From | To |
|---|---|---|
| 3 | SB (2911) **GE 0/0** (the RJ45 marked GE 0/0, in the block near the console port) | SB-S1 (2960, tape BNE S1) **Gi0/2**, the second of the two gigabit uplink ports at the far right of the switch |
| 4 | MG (1941) **GE 0/1** | MG-S1 (2960, tape CNS S1) **Gi0/1**, the first gigabit uplink port at the far right |

On the 2960 the two uplinks are the two larger-spaced RJ45 ports at the right end; the left one is Gi0/1, the
right one Gi0/2 (the port numbers are printed above them). If your 2960 has four openings at the right (two
SFP cages over two RJ45), it is a 2960 Plus or -TC: use the RJ45 ones; same numbering.

What you should see within about 30 seconds: the port LED on the switch turns green (it may blink amber first
for spanning tree, then green), and the router's GE port shows a link light. No light at all means a dead
lead or the router interface is shut down (it is, until Part B; the switch LED may still light because the
router's PHY is up: if it does not, swap the lead to rule it out and carry on).

### A.3 Computers to switches

| Cable | From | To |
|---|---|---|
| 5 | SB computer, built-in wired NIC (or its USB Ethernet adapter) | SB-S1 **Gi0/1** (the first gigabit uplink port) |
| 6 | MG computer, wired NIC (or USB adapter) | MG-S1 **Fa0/1** (the first port in the 24-port block, top-left) |

Both switch port LEDs go green once the computer's NIC is up.

**TAFE lab PC note.** A lab PC's built-in NIC is cabled to the TAFE network (student.tafe, 172.30.96.x). If you
unplug that cable to reach the switch, the PC loses the TAFE network for the session (you are already logged
on; that is fine). If you need both at once, use a USB Ethernet adapter for the lab cable and leave the TAFE
cable in. Either way, note which adapter is on the lab cable: it is the one VMware bridges to in Part C.

### A.4 Console

The console cable goes to one device at a time. RJ45 rollover: into the port marked **CONSOLE** (light blue
on the routers, on the far right of the 1941/2911 front panel; on the 2960 it is the RJ45 at the far left of the
front, marked CONSOLE). USB: the mini-B socket next to it on the routers (the LED beside it lights when the USB
console is active and the RJ45 console then goes silent; unplug the USB to get the RJ45 back).

### A.5 Photo

Photograph the cabled rack front-on so every cable is visible. It is evidence for the network part and it
is the picture you will cable from again next session.

---

## Part B. Console preparation and device configuration

### B.1 Console on the computer

1. Plug the USB-to-serial adapter (or the mini-USB lead) into the computer. Windows: Device Manager > Ports
   (COM & LPT) shows `USB Serial Port (COM3)` or `Cisco USB Console (COM4)`; note the COM number. If the
   router's USB console shows with a yellow triangle, the Cisco USB console driver is missing; use the RJ45
   rollover with the USB-to-serial adapter instead.
2. Open PuTTY. Connection type **Serial**; Serial line `COM3` (your number); Speed `9600`. In Category >
   Connection > Serial: Data bits 8, Stop bits 1, Parity None, Flow control **None**.
3. Category > Session > Logging: All session output; Log file name `C:\Lab8\<device>_<date>.txt` (create
   `C:\Lab8` first). This keeps every screen as evidence and for me to read.
4. Save the session as `Cisco console` so you only change the COM number next time. Click Open. Press Enter
   twice; a prompt appears. Nothing on screen: try speeds 115200, 57600, 38400, 19200; still nothing: check the
   COM number and that the cable is in CONSOLE, not AUX.
5. The Networking VM in your Workstation library has Serial Port 2 on COM1: do not run it during this work or
   it will take the console port from PuTTY.

### B.2 Erase (per device, five devices; the 3750 and spare 2960 can stay as they are)

Console into the device. Routers:

```
enable                                   (if it asks for a password nobody knows: reset doc Part 3)
erase startup-config                     -> Enter at [confirm]; expect [OK]
show version | include register          -> must say 0x2102; if not: configure terminal / config-register 0x2102 / end
reload                                   -> "Save?" type no ; "Proceed with reload? [confirm]" Enter
```
Wait 3 to 5 minutes (quiet console during decompression; do not power-cycle before 6). Then:
`Would you like to enter the initial configuration dialog? [yes/no]:` type `no`; if asked to terminate
autoinstall, `yes`; Enter until you see `Router>`.

Switches:

```
enable
erase startup-config                     -> Enter ; [OK]
delete flash:vlan.dat                    -> Enter at "Delete filename [vlan.dat]?" and again at "[confirm]"
                                            ("%Error deleting ... No such file" is fine)
reload                                   -> "Save?" no ; Enter
```
1 to 3 minutes; `no` to the setup dialogue; `Switch>`. If it stops at `switch:` instead, type `boot`.

Blank check (one line each): router `show running-config | include hostname|username|enable |^ ip address|^router `
prints only `hostname Router`; switch `show running-config | include hostname|^vlan |^interface Vlan` prints only
`hostname Switch` and `interface Vlan1`, and `show vlan brief` shows VLAN 1 plus 1002 to 1005 only.

Then on each router `show inventory` (confirms `HWIC-2T` in slot 0, so Serial0/0/0 and 0/0/1) and on each
switch `show inventory` (model: a `-24TT-L` or `-24TC-L` has Gi0/1 and Gi0/2; a `-24-S` has no gigabit ports,
in which case replace Gi0/1 with Fa0/23 and Gi0/2 with Fa0/24 everywhere in Part B.3 and re-plug cables 3 and
5 accordingly).

### B.3 Configure, in this order: SB, ISP, MG, SB-S1, MG-S1

How to paste: copy a block from `Cisco_build_SB_ISP_MG_2026-10-21.md`, replace every `<placeholder>` with your
own value first (enable secret, console and vty passwords, device name in the banner), then in PuTTY
right-click once in the window to paste. Watch the screen: a line that answers `% Invalid input` or
`% Incomplete command` is a line to fix by hand. Paste the **common block** (section 3 of the build doc) first
on each device, then the device's own block, then `write memory`.

**SB (2911).** After pasting: `show ip interface brief`. Expect `GigabitEthernet0/0` and `.20`, `.30`, `.90`
all `up / up` with 192.168.1.1, 192.168.1.65, 192.168.2.1 (the sub-interfaces come up only when the trunk to
SB-S1 is cabled and the switch port is up; if they show `down`, continue and re-check after SB-S1 is done).
`Serial0/0/0` shows 209.165.200.1 and `down / down` until ISP is configured: normal.

**ISP (1941).** After pasting: `show controllers serial 0/0/0 | include cable` and `... 0/0/1 ...` must both
say `DCE`; if one says DTE, that cable is the wrong way round: swap its ends (power stays on). Then
`show ip interface brief`: both serials `up / up` (SB side is already configured; MG side comes up after the
next step). `show ip ospf neighbor`: `1.1.1.1 ... FULL/  -   Serial0/0/0` within about 40 seconds.

**MG (1941).** After pasting: `show ip interface brief`: `Serial0/0/1 209.165.200.18 up / up`,
`GigabitEthernet0/1 172.16.0.1 up / up` (up only once cable 4 and MG-S1 are in place; if down, carry on).
`show ip ospf neighbor`: `2.2.2.2 FULL`. `ping 192.168.2.1`: five `!` = routing across the three routers
works. `show ip route`: `O 192.168.2.0/28 [110/...] via 209.165.200.17`.

Back on ISP: `show ip ospf neighbor` now lists both 1.1.1.1 and 3.3.3.3 FULL. Screenshot it (evidence).

**SB-S1 (2960).** After pasting: `show vlan brief` (20 CS: Fa0/1-8; 30 Marketing: Fa0/11-18; 90 Server:
Fa0/9-10 and Gi0/1), `show interfaces trunk` (Gi0/2, mode on, encapsulation 802.1q, VLANs 20,30,90),
`ping 192.168.2.1` from the switch (five `!`: the SVI, the trunk and the router sub-interface all agree).
Screenshot `show vlan brief` and `show interfaces trunk` (evidence). Now on SB, `show ip interface brief`
shows the three sub-interfaces up.

**MG-S1 (2960).** After pasting: `show interfaces status` (Fa0/1 and Gi0/1 `connected`, vlan 1);
`ping 172.16.0.1` from the switch.

**Final router check.** SB: `ping 172.16.0.1` (five `!`), `show ip route` (O route to 172.16.0.0/24, screenshot).
MG: `show ip route` (O routes to 192.168.1.0/26, 192.168.1.64/26, 192.168.2.0/28, screenshot).
`write memory` on all five devices once more, then `show startup-config | include hostname` on each to prove it
is saved.

If a check fails: stop there, copy the exact output into a message to me, and do not keep pasting. The usual
suspects: cable in the wrong socket (`show ip interface brief` says down/down), DCE/DTE swapped (`clock rate`
refused or line protocol down), a `<placeholder>` left in a pasted line, or a sub-interface that was typed
before `encapsulation dot1Q`.

---

## Part C. Computers and VMs

### C.1 Quick network test from the computers themselves (before any VM)

This proves cables 5 and 6 and the switch ports without touching VMware.

SB computer: Settings > Network & Internet > Ethernet (the lab adapter) > IP assignment Manual, IPv4 on:
IP `192.168.2.13`, mask `255.255.255.240` (prefix 28), gateway `192.168.2.1`, DNS `192.168.2.1` for now.
Command prompt: `ping 192.168.2.1` then `ping 172.16.0.1`.

MG computer: IP `172.16.0.253`, mask `255.255.255.0`, gateway `172.16.0.1`. `ping 172.16.0.1`,
`ping 192.168.2.1`, `ping 192.168.2.13` (the other computer; Windows Firewall blocks ping by default on a
Public network: if the router pings work and only the PC-to-PC ping fails, that is the firewall, not the
network; `tracert -d 192.168.2.13` still shows the three router hops).

Both computers reach both gateways: the network is done. Set the adapters back to Automatic (DHCP) afterwards,
or leave them: an address in the same subnet as the VM does no harm.

### C.2 VMware bridging (each computer)

1. Workstation > Edit > Virtual Network Editor (click "Change Settings" for administrator rights).
2. Select **VMnet0**. Set Type Bridged and **Bridged to: the lab adapter by name** (the built-in NIC or the USB
   adapter from A.3), not Automatic. Apply, OK.
3. For each VM you will run here: VM > Settings > Network Adapter > **Bridged** (not NAT, not Host-only,
   not Custom), Connect at power on ticked.

A VM bridged this way behaves exactly like a second computer on the same cable, in the same VLAN as the port.

### C.3 Where the VMs live

Create `E:\Lab8-VMs\` on the USB SSD (outside OneDrive) or, better for speed, on the computer's internal drive
(`D:\Lab8-VMs\` on a lab PC; it may not survive a re-image, so copy the folder to `E:` at the end of each
session). One sub-folder per VM: `DC1`, `DC2`, `SB-DNS-2`, `SB-FS2`, `CS-PC-1`, `Ubuntu`. Never two VMs in one
folder (that is what wrecked the 2025 logs and answer floppy).

### C.4 Building DC1 (SB computer) and DC2 (MG computer): the VM shell

Wait for the teacher's answer on Server 2019 Datacenter versus 2012 R2 before installing Windows. The VM
shell can be prepared now. File > New Virtual Machine > Typical > **"I will install the operating system
later"** (this avoids Easy Install, which would create an unnamed account with a blank password and apply its
own product key; a domain controller wants the built-in Administrator with a password you set) > Guest
Windows Server 2019 (or 2012 R2) > Name `DC1`, Location `...\Lab8-VMs\DC1` > disk 60 GB, single file >
Customize Hardware: 2 processors, **4096 MB** memory (2 GB works but is slow for a DC with DNS), CD/DVD >
Use ISO image file > the Server 2019 ISO, Connect at power on ticked; Network Adapter > Bridged. Finish.
Same for `DC2` on the MG computer.

Windows install (when cleared): power on, press a key to boot from the CD if asked, choose **Datacenter
(Desktop Experience)**, Custom install, the single disk, let it run (10 to 20 minutes), set the Administrator
password at the end (record it privately: it becomes the domain Administrator password on DC1). Then VM >
Install VMware Tools, reboot.

### C.5 Inside each DC: name and address (Work Package 1 and 2 start here)

DC1: Server Manager > Local Server > Computer name > rename to `DC1`, restart. Ethernet > Properties > IPv4:
`192.168.2.2` / `255.255.255.240` / gateway `192.168.2.1` / preferred DNS `192.168.2.2` / alternate `127.0.0.1`.
Time zone Brisbane; check the clock. `ping 192.168.2.1` and `ping 172.16.0.1`.

DC2: rename to `DC2`, restart. IPv4: `172.16.0.2` / `255.255.255.0` / gateway `172.16.0.1` / preferred DNS
`192.168.2.2` (DC1) / alternate blank for now. `ping 172.16.0.1`, `ping 192.168.2.2`.

From DC2, before any domain join (the video's rule): `nslookup dc1.<domain>` must answer, which it can only do
after DC1 has been promoted and its DNS zone exists. That is Work Package 1 on DC1 (Add Roles > AD DS >
Promote > **Add a new forest** > `<student1>.<student2>`), then Work Package 2 on DC2. Those steps are the
report's Section E and the brief; they start once the teacher's OS answer is in and the network above passes.

### C.6 Evidence for the network part (collect before leaving the rack)

* Photo of the cabled rack (A.5).
* ISP `show ip ospf neighbor` with two FULL neighbours.
* SB and MG `show ip route`.
* SB-S1 `show vlan brief` and `show interfaces trunk`.
* The computer-to-gateway and computer-to-far-gateway pings from both computers (C.1), later repeated from
  inside DC1 and DC2.
* The PuTTY log files from `C:\Lab8\` copied into `02_student_work/network/` (replace the enable secret and
  passwords with `<redacted>` if a `show running-config` is in them).
