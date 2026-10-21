# Cisco devices: capture, erase, verify blank, then rebuild (decision of 2026-10-21)

Decision: the Cisco devices start from a blank configuration. Nothing old on them is reused. Reasons recorded:
the rack is uncabled (report B.0), what is on the devices is unknown, the recovered VMs never touched the
rack, and a clean build is faster to verify than an archaeology of someone else's config.

This document is the procedure. The build configuration itself is written as a separate step once the devices
are confirmed blank and the two design choices in Part 4 are made.

## Part 0. Before touching anything

1. **Shared equipment.** The rack carries other people's labels. Confirm with the teacher that these seven
   devices may be erased. Erasing is irreversible for whoever's configuration is on them.
2. **Console kit.** Console cable (RJ45 rollover or the USB mini-B console port), PuTTY or Tera Term, serial
   settings 9600 baud, 8 data bits, no parity, 1 stop bit, no flow control. In PuTTY set Session > Logging >
   "All session output" with a file name per device (`01_2911_before_erase.txt`, ...) so every screen is kept.
3. **Power.** Routers were powered in the photo; the switches looked dark. Switches have no power switch: if the
   power cord is in and nothing lights, the cord is not live. Check before concluding a switch is dead.

## Part 1. Capture what is there (read-only, about 3 minutes per device)

Even though nothing will be reused, keep a record: it costs nothing and settles any later "what was on it"
question. On each of the seven devices, with logging on:

```
enable
terminal length 0
show version
show running-config
show startup-config
dir flash:
show ip interface brief
show vlan brief            (switches only)
show switch                (3750 only: confirms a single stack member)
```

If `enable` asks for a password nobody knows, skip to Part 3 (password recovery), which ends in the same blank
state. Save the logs to `02_student_work/network/before_erase/` with passwords, if any appear, replaced by
`<redacted>`.

## Part 2. Erase

### Routers (the 2911 and both 1941s)

```
enable
erase startup-config
```
Prompt: `Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]` -> press Enter.
Expect `[OK]` and `Erase of nvram: complete`.

```
show version | include register
```
Expect `Configuration register is 0x2102`. If it shows `0x2142` (left over from a password recovery), fix it
before reloading:

```
configure terminal
config-register 0x2102
end
```

Then:

```
reload
```
Prompt: `System configuration has been modified. Save? [yes/no]:` -> type `no`.
Prompt: `Proceed with reload? [confirm]` -> Enter.

The router boots in 2 to 3 minutes. Answer the dialogue:
`Would you like to enter the initial configuration dialog? [yes/no]:` -> `no`
`Would you like to terminate autoinstall? [yes]:` -> `yes` (if it appears)
Press Enter; expect the prompt `Router>`.

### Switches (both 2960s, the 2960 Plus and the 3750)

Switches keep VLANs in a separate file, so two things are erased:

```
enable
erase startup-config
```
Confirm with Enter; expect `[OK]`.

```
delete flash:vlan.dat
```
Prompt: `Delete filename [vlan.dat]?` -> Enter. `Delete flash:/vlan.dat? [confirm]` -> Enter.
If it says `No such file or directory`, there were no custom VLANs; that is fine.

```
reload
```
Save? -> `no`. Proceed? -> Enter. Boot takes 1 to 3 minutes (the 3750 longer). Answer `no` to the initial
configuration dialogue. Expect `Switch>`.

### Verify blank, every device

```
enable
show running-config
```
Expect only the default skeleton: no `hostname`, no `ip address` lines, no `vlan` lines, no `router` lines, no
`username`, no `enable secret`.

```
show startup-config
```
Expect `startup-config is not present`.

Switches only:
```
show vlan brief
```
Expect VLAN 1 (all ports) and only 1002 to 1005 besides.

Record the result per device in the table in Part 5.

## Part 3. Password recovery (only if `enable` is locked)

This also ends blank, which is what is wanted anyway.

### 1941 and 2911

1. Connect the console, power the router off and on.
2. Within the first 60 seconds send Break (PuTTY: right-click the title bar > Special Command > Break; Tera
   Term: Control > Send break). The prompt becomes `rommon 1 >`.
3. `confreg 0x2142` then `reset`. The router boots ignoring its startup-config.
4. Answer `no` to the setup dialogue, then `enable` (no password now).
5. `erase startup-config` (confirm), then `configure terminal`, `config-register 0x2102`, `end`, `reload`,
   answer `no` to save. It comes back blank with the normal register.

### 2960, 2960 Plus and 3750

1. Unplug the power cord. Press and hold the **Mode** button on the front left, plug the cord back in, keep
   holding until the SYST LED has gone amber and then solid green (about 15 seconds on a 2960; watch the LED),
   then release. The console shows the `switch:` prompt.
2. `flash_init`
3. `del flash:config.text` (confirm), `del flash:private-config.text` (confirm, if present), `del flash:vlan.dat`
   (confirm).
4. `boot`. Answer `no` to the setup dialogue. The switch is blank.
5. If the switch prints that password recovery is disabled and offers to erase the configuration instead,
   answer yes: that is the result wanted.

## Part 4. Two design choices before the build is written

The build will follow the Lab 1 to 3 topology (SB-S1 -> SB -> ISP -> MG -> MG-S1) with the later addressing:
VLAN 20 192.168.1.0/26, VLAN 30 192.168.1.64/26, VLAN 90 192.168.2.0/28 (gateway 192.168.2.1) at SB;
172.16.0.0/24 (gateway 172.16.0.1) at MG; serial links 209.165.200.0/28 (SB-ISP) and 209.165.200.16/28
(ISP-MG). Two choices are open:

1. **Routing between sites: OSPF or static routes.** The later lab work used OSPF; static routes are three
   lines and nothing to troubleshoot. Either satisfies Lab 8. Default proposal: OSPF area 0 on all three
   routers, because it matches the earlier assessments and the teacher expects it; say if you prefer static.
2. **How the two VM hosts attach.** DC1 must be on 192.168.2.0/28 (SB-S1, VLAN 90 access port) and DC2 on
   172.16.0.0/24 (MG-S1 access port). That is two physical switch ports, so either two computers (one at each
   switch) or one computer with two wired NICs (built-in plus a USB Ethernet adapter), each bridged to its own
   VMnet. Say which you have.

Device roles (any router can take any role; this is the proposal, using the chassis labels only as handles):

| Role | Chassis | Why |
|---|---|---|
| SB | 2911 (tape BNE / R1) | three GigabitEthernet ports; G0/0 carries the VLAN sub-interfaces, S0/0/0 to ISP |
| ISP | 1941 (tape ISP) | two serial ports: S0/0/0 to SB, S0/0/1 to MG |
| MG | 1941 (tape CNS / R2) | S0/0/1 to ISP, G0/1 to MG-S1 |
| SB-S1 | 2960 (tape BNE S1) | 24 FE access ports, Gi0/1 trunk to SB |
| MG-S1 | 2960 (tape CNS S1) or the 2960 Plus | access ports for the MG host |
| spare | 3750G, the other 2960 | not needed |

Cables needed: 2 serial DCE/DTE (smart-serial to smart-serial); 2 Ethernet router-to-switch; 1 Ethernet per VM
host; 1 console. The serial cable's DCE end goes on ISP (it supplies the clock); on the smart-serial cable the
DCE end is the one marked DCE on the connector moulding.

## Part 5. Record

| Chassis (label as handle) | Captured before erase | Erased | Verified blank | Prompt after reload | Date |
|---|---|---|---|---|---|
| 2911 (BNE / R1) | | | | | |
| 1941 (ISP) | | | | | |
| 1941 (CNS / R2) | | | | | |
| 2960 (BNE S1) | | | | | |
| 2960 (CNS S1) | | | | | |
| 2960 Plus (MG-S1) | | | | | |
| 3750G | | | | | |
