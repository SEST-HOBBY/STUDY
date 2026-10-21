# Cisco devices: capture, erase, verify blank, then rebuild (decision of 2026-10-21)

Decision: the Cisco devices start from a blank configuration. Nothing old on them is reused. Reasons recorded:
the rack is uncabled (report B.0), what is on the devices is unknown, the recovered VMs never touched the
rack, and a clean build is faster to verify than an archaeology of someone else's config.

Revised 2026-10-21 after an IOS review (18 corrections applied; the main ones: boot-loader deletes need `y`
not Enter, the blank-device test now uses concrete filters, locked-console and recovery-disabled cases added,
console speed sweep, 3750 stack number, serial card names from `show inventory`).

This document is the procedure. The build configuration itself is written as a separate step once the devices
are confirmed blank and the two design choices in Part 4 are made.

## Part 0. Before touching anything

1. **Shared equipment.** The rack carries other people's labels. Confirm with the teacher that these seven
   devices may be erased. Erasing is irreversible for whoever's configuration is on them.
2. **Console kit.** Console cable (RJ45 rollover or the USB mini-B console port), PuTTY or Tera Term, serial
   settings 9600 baud, 8 data bits, no parity, 1 stop bit, no flow control. In PuTTY set Session > Logging >
   "All session output" with a file name per device (`01_2911_before_erase.txt`, ...) so every screen is kept.
3. **Nothing on screen, or garbage?** A previous owner may have changed the console speed. Try 115200, 57600,
   38400 and 19200 in PuTTY before concluding a device is dead. This applies to the `switch:` boot loader too.
4. **Power.** Routers were powered in the photo; the two plain 2960s looked dark. Switches have no power
   switch: if the cord is in and nothing lights, the cord is not live. Check before concluding a switch is dead.
   On the 3750, look at the rear RPS connector: if a redundant-power cable is attached, disconnect it or the
   Mode-button power cycle in Part 3 will not work.
5. **Locked console.** If the console asks for a username or password before the `>` prompt, or `enable` asks
   for a password nobody knows, skip Part 1 for that device (record "not captured, locked" in Part 5) and go to
   Part 3, which ends in the same blank state.

## Part 1. Capture what is there (SKIPPED by decision of 2026-10-21: no capture, straight to Part 2)

The student chose a clean slate with no capture. Three items from this part are still needed and are folded
into Part 2: the config register check before each router reload, and `show inventory` plus `show ip interface
brief` after the blank boot to confirm the interface names used in the build. The rest of Part 1 is kept for
reference only.

Even though nothing will be reused, keep a record: it costs nothing and settles any later "what was on it"
question, and three of the answers decide later steps (config register, serial cards, boot settings). On each
device, with logging on:

Routers (2911 and both 1941s):
```
enable
terminal length 0
show version
show version | include register|ROM|uptime
show inventory
show running-config
show startup-config
dir flash:
show ip interface brief
show controllers serial 0/0/0 | include cable
show controllers serial 0/0/1 | include cable
```
(Repeat the `show controllers` line for every serial interface that `show ip interface brief` lists; the names
depend on which slot the card sits in: slot 0 gives Serial0/0/0 and 0/0/1, slot 1 gives Serial0/1/0 and 0/1/1.)

Switches (2960, 2960 Plus, 3750):
```
enable
terminal length 0
show version
show inventory
show running-config
show startup-config
dir flash:
show ip interface brief
show vlan brief
show vtp status
show boot
show switch                (3750 only)
```

What to note from the capture: the exact model from `show inventory` (decides the uplink port names in the
build); the config register (routers; anything but 0x2102 is fixed in Part 2); the ROMMON version (routers;
matters only if Part 3 is needed); whether `dir flash:` lists `vlan.dat` (switches always, routers only with an
EtherSwitch card); `show boot` on switches (if it prints `Manual Boot: yes`, run `configure terminal`, `no boot
manual`, `end`, `write memory` before Part 2, or the reload will stop at `switch:` and need `boot`).

Save the logs to `02_student_work/network/before_erase/` with passwords, if any appear, replaced by
`<redacted>`.

## Part 2. Erase

### Routers (the 2911 and both 1941s)

```
enable
erase startup-config
```
Prompt: `Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]` -> press Enter.
Expect `[OK]` and `Erase of nvram: complete`. This erases the whole `nvram:` filesystem (startup-config and
private-config); files on `flash0:` are deliberately left alone.

If `dir flash:` in Part 1 listed `vlan.dat` (only with an EtherSwitch card fitted): `delete flash:vlan.dat`,
same prompts as on the switches below.

```
show version | include register
```
Expect `Configuration register is 0x2102`. **If it shows anything else** (0x2142 from a password recovery,
0x2100, 0x2101, or an odd value that also sets the console speed), fix it before reloading:

```
configure terminal
config-register 0x2102
end
show version | include register
```
The last line must now read `... 0x<old> (will be 0x2102 at next reload)`.

Then:

```
reload
```
Prompt: `System configuration has been modified. Save? [yes/no]:` -> type `no`. (Answering `yes` writes the
old running configuration back into NVRAM and undoes the erase; if that happens, erase and reload again. If the
prompt does not appear, carry on.) Prompt: `Proceed with reload? [confirm]` -> Enter.

The router takes 3 to 5 minutes to boot and the console is quiet during image decompression; do not
power-cycle before 6 minutes. Answer the dialogue:
`Would you like to enter the initial configuration dialog? [yes/no]:` -> `no`
`Would you like to terminate autoinstall? [yes]:` -> `yes` (if it appears)
Press Enter; expect the prompt `Router>`.

### Switches (both 2960s, the 2960 Plus and the 3750)

Switches keep VLANs in a separate file, so two things are erased:

```
enable
erase startup-config
```
Confirm with Enter; expect `[OK]`. (On these Catalysts this deletes `flash:config.text` and
`flash:private-config.text`.)

```
delete flash:vlan.dat
```
Prompt: `Delete filename [vlan.dat]?` -> Enter. `Delete flash:/vlan.dat? [confirm]` -> Enter.
If it prints `%Error deleting flash:/vlan.dat (No such file or directory)`, the VLAN database was never
modified; that is fine. Do not touch VLAN or VTP settings between this delete and the reload (any change
writes the file again).

```
reload
```
Save? -> `no` (same warning as for the routers). Proceed? -> Enter. Boot takes 1 to 3 minutes (the 3750 longer).
If the switch stops at `switch:` instead of booting, `boot manual` was set (Part 1): type `boot`. Answer `no` to
the initial configuration dialogue. Expect `Switch>`.

### Verify blank, every device

A blank device is not an empty configuration: it prints its default hostname, `no ip address` and `shutdown`
under every interface, and on 15.x a few default lines (`ip cef`, `license udi`, `spanning-tree mode pvst`,
`ip http server`, a `line vty 0 4` block). Use these filters instead of reading the whole file.

Routers:
```
show running-config | include hostname|username|enable |^ ip address|^router |^ip route|^crypto
show ip interface brief
show startup-config
```
Pass: the first command prints only `hostname Router`; every interface is `unassigned` and `administratively
down`; the third prints `startup-config is not present`.

Switches:
```
show running-config | include hostname|username|enable |^ ip address|^vlan |^interface Vlan|switchport|^ip route
dir flash:
show vlan brief
show vtp status
show startup-config
```
Pass: the first command prints only `hostname Switch` and `interface Vlan1`; `dir flash:` lists no
`config.text`, no `private-config.text` and no `vlan.dat`; `show vlan brief` shows VLAN 1 (all ports) and only
1002 to 1005 besides; VTP mode Server with an empty domain name; `startup-config is not present`.

3750 only: the line `switch 1 provision ws-c3750g-24ps` is default and expected. Run `show switch`: the stack
member number and priority live in ROMMON variables and survive every erase. If the number is not 1 and the
build wants `Gi1/0/x` port names, in config mode run `switch <n> renumber 1`, accept the warning, `reload`
(no to save). Record the number in Part 5.

## Part 3. Password recovery (only if the console or `enable` is locked)

This also ends blank, which is what is wanted anyway.

### 1941 and 2911

1. Connect the console, power the router off and on, and watch for the ROMMON banner.
2. From the moment the banner appears, send Break every second or two (PuTTY: right-click the title bar >
   Special Command > Break, or Ctrl+Break; Tera Term: Control > Send break) and keep going through image
   decompression, up to 60 seconds, until `rommon 1 >` appears. A single Break at power-on is often ignored.
3. `confreg 0x2142` then `reset`. The router boots ignoring its startup-config.
4. Answer `no` to the setup dialogue, then `enable` (no password now).
5. `erase startup-config` (confirm), then `configure terminal`, `config-register 0x2102`, `end`, `reload`,
   answer `no` to save. It comes back blank with the normal register; check with `show version | include register`.

If the boot prints `PASSWORD RECOVERY FUNCTIONALITY IS DISABLED`, Break will not give ROMMON. Keep sending
Break in the first seconds after the image decompresses; at `Do you want to reset the router to factory
default configuration and proceed [y/n] ?` type `y`. The router erases NVRAM and boots blank; answer `no` to the
setup dialogue, then check and set the register as in step 5.

If Break is never recognised at all (some USB-to-serial adapters do not pass it; ISR G2 routers with ROMMON
15.0(1r)M1 ignore it until the ROMMON is upgraded, Cisco field notice FN-63355): power off, remove the
CompactFlash card from the rear slot, power on so the router stops in ROMMON for lack of an image,
`confreg 0x2142`, power off, refit the card, power on and continue at step 4.

### 2960, 2960 Plus and 3750

1. Unplug the power cord (on the 3750 also any RPS cable). Plug the cord back in. **While the SYST LED is still
   flashing green (within the first 15 seconds) press and hold the Mode button** on the front left. Keep holding
   until SYST turns amber briefly and then solid green, however long that takes, then release. The console
   prints that the system was interrupted prior to initialising the flash file system, lists `flash_init` and
   `boot`, and shows `switch:`. If you miss the window the switch simply boots normally; pull the cord and try
   again, nothing is harmed.
2. `flash_init`
3. `dir flash:` and note which of `config.text`, `private-config.text` and `vlan.dat` exist.
4. For each one that exists: `del flash:config.text` and **type `y`** at `Are you sure you want to delete
   "flash:config.text" (y/n)?` (Enter means no here, unlike the IOS `[confirm]` prompts). Repeat for
   `private-config.text` and `vlan.dat`. Names are case-sensitive. `dir flash:` again: all three gone.
5. `boot`. Answer `no` to the setup dialogue. The switch is blank; run the Part 2 verification.

If the console says the password-recovery mechanism has been triggered but is currently disabled, **type `y`**
at `Would you like to reset the system back to the default configuration (y/n)?`. The switch deletes
`config.text` and `vlan.dat` and drops to `switch:`. Then `flash_init`, `dir flash:` (delete any of the three
files that remain, with `del` and `y`), `boot`, and answer `no` to the setup dialogue.

## Part 4. Two design choices before the build is written

The build will follow the Lab 1 to 3 topology (SB-S1 -> SB -> ISP -> MG -> MG-S1) with the later addressing:
VLAN 20 192.168.1.0/26, VLAN 30 192.168.1.64/26, VLAN 90 192.168.2.0/28 (gateway 192.168.2.1) at SB;
172.16.0.0/24 (gateway 172.16.0.1) at MG; serial links 209.165.200.0/28 (SB-ISP) and 209.165.200.16/28
(ISP-MG). Two choices are open:

1. **Routing between sites: OSPF or static routes.** The later lab work used OSPF; static routes are three
   lines and nothing to troubleshoot. Either satisfies Lab 8 and neither needs an extra licence on these
   routers. Default proposal: OSPF area 0 on all three routers, because it matches the earlier assessments and
   the teacher expects it; say if you prefer static.
2. **How the two VM hosts attach.** DC1 must be on 192.168.2.0/28 (SB-S1, VLAN 90 access port) and DC2 on
   172.16.0.0/24 (MG-S1 access port). That is two physical switch ports, so either two computers (one at each
   switch) or one computer with two wired NICs (built-in plus a USB Ethernet adapter), each bridged to its own
   VMnet. Say which you have.

Device roles. The photo shows a two-port serial card (HWIC-2T) in slot 0 of all three routers, so any router
can take any role; the names below are what that gives and are confirmed from `show inventory` and `show ip
interface brief` in Part 1 (a card in slot 1 would be Serial0/1/0 and 0/1/1 instead). The build is written from
the captured names, not from this table. Chassis labels are used only as handles.

| Role | Chassis | Why |
|---|---|---|
| SB | 2911 (tape BNE / R1) | three GigabitEthernet ports; G0/0 carries the VLAN sub-interfaces, S0/0/0 to ISP |
| ISP | 1941 (tape ISP) | needs both serial ports: S0/0/0 to SB, S0/0/1 to MG |
| MG | 1941 (tape CNS / R2) | S0/0/1 to ISP, G0/1 to MG-S1 |
| SB-S1 | 2960 (tape BNE S1) | 24 FE access ports; trunk to SB on a Gi uplink if the model has one (a -24-S has FE only; read `show inventory`) |
| MG-S1 | 2960 (tape CNS S1) or the 2960 Plus | access ports for the MG host |
| spare | 3750G, the other 2960 | not needed |

Cables needed: 2 serial back-to-back cables (smart-serial to smart-serial, CAB-SS-2626X type: one connector
moulded DTE, the other DCE); 2 Ethernet router-to-switch; 1 Ethernet per VM host; 1 console. **Put the DCE end
of both serial cables on the ISP router.** The router interface that has the DCE end supplies the clock; IOS
15.x on a HWIC-2T inserts `clock rate 2000000` by itself when it sees a DCE cable, and the build will set the
lab's value explicitly (for example `clock rate 128000`) so the configs are deliberate. Confirm which end is
fitted with `show controllers serial 0/0/0 | include cable` (`DCE V.11 (X.21) cable`, `DTE ... cable` or
`No serial cable`). Leave the serial `bandwidth` default (1544) unless the worksheet says otherwise.

## Part 5. Record

| Chassis (label as handle) | Model from `show inventory` | Serial ports (names) | Captured before erase | Erased | Verified blank | Prompt after reload | 3750 member no. | Date |
|---|---|---|---|---|---|---|---|---|
| 2911 (BNE / R1) | | | | | | | - | |
| 1941 (ISP) | | | | | | | - | |
| 1941 (CNS / R2) | | | | | | | - | |
| 2960 (BNE S1) | | - | | | | | - | |
| 2960 (CNS S1) | | - | | | | | - | |
| 2960 Plus (MG-S1) | | - | | | | | - | |
| 3750G | | - | | | | | | |
