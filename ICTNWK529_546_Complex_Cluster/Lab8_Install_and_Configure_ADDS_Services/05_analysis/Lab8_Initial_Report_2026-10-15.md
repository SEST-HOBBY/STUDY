# Lab 8 initial report: recovered assets, existing network, existing AD, completion matrix

Date: 2026-10-15. Status: nothing verified yet. This report records what is known, what is assumed, and the
read-only steps that turn assumptions into facts. It is updated as results come back. No configuration is to be
changed until Sections A to C are filled in from live output.

How to read the statuses: **Verified complete** (seen working, evidence captured), **Partially complete**,
**Not started**, **Cannot determine** (no live output yet), **Blocked** (waiting on a missing source or decision).

Two kinds of statement appear below. Facts from the handoff (file names, sizes, dates, the briefs) are stated
plainly. Product knowledge about how Windows, Active Directory, VMware and Cisco IOS behave is general and has
been checked, but how it applies to these particular machines is inference until the live output confirms it.

## 0. Current-state inventory (as known today)

Updated 2026-10-21 from the recovered `.vmx`, `.vmsd`, `.vmxf`, `.nvram`, `autoinst.flp`, `vmware.log` and
`vmware-1.log` files and a screenshot of the folder (details in A.11).

| Item | Known | Source | Verified |
|---|---|---|---|
| Folder | One flat folder `SERVER VM FOR LAB 8-9` holding both VMs; a `caches` folder dated 16/03/2026 | Screenshot | Yes |
| VM `DC2.Eric.Roly` | Created 21/10/2025 19:25 by Easy Install; Windows at the desktop by 19:40; configured until 21:05 (two guest restarts 20:23 and 20:24); ran again 22/10 19:16 to 20:55 with no restart. **Both sessions ended with the Workstation Power Off button, not a Windows shutdown.** No snapshots; UEFI; 2 vCPU, 2 GB; 60 GB NVMe disk, 10,090,304 KB used; VMware Tools 11.1.5 installed | .vmx, .vmsd, .vmxf, logs | Yes |
| VM `Windows Server 2019` | Created 22/10/2025 19:03 by Easy Install; hard-stopped from the host at 19:16:42 after 12 to 13 minutes, mid-Setup, before first logon; Tools never installed; floppy and install ISO still attached; NAT; no snapshots. Not a server, not a template: do not boot; rebuild from the ISO if a VM is needed | .vmx, .vmxf, logs | Yes |
| Snapshots, delta disks, suspend files, lock folders | None of any of them, for either VM. (`cleanShutdown = TRUE` only means the VMware process exited normally; Windows inside DC2 was not shut down cleanly) | .vmsd (empty), .vmx, logs, screenshot | Yes |
| VMware host product and version | VMware Workstation 16.1.0 build 17198959; TAFE lab PCs TQ-D62ZRJ3 (21/10) and TQ-7SXZNJ3 (22/10): Dell, Windows 10 Education, i7-11700, about 64 GB RAM; VM files on a USB external SSD (Realtek RTL9210B bridge) mounted as `E:`, with very slow writes (8 to 10 s, one 75 s) | vmware-1.log, vmware.log | Yes |
| Guest OS inside DC2 | Windows Server 2019 **Datacenter** (Desktop Experience), build 17763, from the full (non-evaluation) Sept 2019 ISO; the key applied at first logon is VMware Easy Install's default, not a KMS client key; activation state unknown; no shutdown timer either way | vm3d lines (build, suite mask), autoinst.flp image name, .vmx ISO path | Yes |
| Windows computer name of DC2 | Not in any file. Easy Install auto-generates a name; whether it was renamed to DC2 is unknown | | No |
| Domain name | Not in any file. Possibly `Eric.Roly` (VM name). Must be read inside Windows | | No |
| DC1 | NOT the `Windows Server 2019` VM (an unfinished 13-minute install). The VM running beside DC2 on 22/10 was the lab PC's own `Networking_VM_2022` (`D:\Shared_VMs\...`, holding the USB console cable), not DC1. The only unidentified VM in the logs is a 2 GB VM that ran on TQ-D62ZRJ3 for the whole of 21/10 beside DC2: the sole DC1 candidate, if DC1 ever existed. Nothing shows DC1 on 22/10 | vmware.log 19:16:33 (USB ownership), MemSched lines | Yes (what it is not) |
| DC2 a domain controller? | **Almost certainly not.** At every recorded boot, including the last (22/10 19:16), Windows reported product type 3 = a server that is not a DC (a DC reports 2), and no restart followed on 22/10, so no promotion completed. It may have been renamed and joined to a domain on 21/10 (two restarts); unproven | vm3d lines in both logs | Yes (not a DC at last boot) |
| DC2 network | All on 21/10 while running: NAT (19:25) -> host-only (20:11) -> custom `VMnet0`, the default bridged network (20:43) -> custom `VMnet1` (20:45, kept). VMnet1 is host-only by default; whether the lab PC had it re-bridged cannot be read from the files | logs | Yes (settings), No (what VMnet1 was) |
| DC2 identity change | On 22/10 the moved-or-copied prompt was answered as COPIED: new SMBIOS UUID, new VM Generation ID, new MAC (00:0c:29:2e:2b:c6 became 00:0c:29:32:7c:40) | vmware.log | Yes |
| Local logon account | Easy Install created local administrator `471562641` (the student number) with an EMPTY password; auto-logon for the first logon only. Certain for the 22/10 wizard values; very probably the same on DC2 (same wizard, same ISO, first logon ran the same template) | autoinst.flp; logs | Probable (DC2) |
| SB-DNS-2, SB-FS2, SB-DNS-1/SB-FS1, CS-PC-1, Ubuntu | No VM in the folder matches any of these | Screenshot | Yes |
| Domain and DSRM passwords | Unknown whether the student has them | | No |
| Rack hardware | Cisco 2911 and two 1941s, each with an HWIC-2T two-port serial card; Catalyst 3750G PoE-24, 2960 Plus, two 2960s. Labels on the shared rack are meaningless and are ignored | Photo 2026-10-21 (B.0) | Yes (from photo) |
| Rack cabling | **None.** No serial or Ethernet cables connected; routers, 3750 and 2960 Plus powered; the two 2960s dark | Photo 2026-10-21, two independent readings | Yes (from photo) |
| Cisco configurations now on the devices | Unknown: could be the SB/ISP/MG Lab 1 to 3 configs, the later 192.168.1.x / 192.168.2.0/28 work, a Brisbane/Cairns (BNE/CNS) build, or defaults | Config files; project memory; labels | No |
| Routing SB to MG, VPN/OSPF, ACLs or zone firewall | Not testable until re-cabled | | No |
| Which switch port the VM host uses; VLAN 90 membership | No host is cabled to any switch today (brief says Gi0/1; early config makes Gi0/1 a trunk). The recovered VMs were never bridged (NAT, then VMnet1) | Photo; .vmx | Yes (none today) |
| Time since the VMs last ran | 364 days (last power-off 22/10/2025 20:55) | vmware.log | Yes |

Sections A to F below are the detailed plan for each row. Section G is the one thing to do next.

---

## A. Recovered VMware assets and safe recovery procedure

Rule for the whole section: **the original folder is the backup and is never opened in VMware.** Reading its
files as text is fine. Everything else happens on a copy. The only changes this section allows, all on the copy
and in this order: untick "Connect at power on", answer "I Moved It", boot, save command output inside the
guest, shut down cleanly. One exception, A.8, only after all read-only output is saved: `slmgr /rearm`.

### A.1 What each file is

Seen in the listing:

| File | What it is | Why it matters |
|---|---|---|
| `.vmx` | Plain-text VM configuration (3 KB is normal): display name, guest OS type, firmware, memory, which disk is attached, network mode and MAC, UUIDs | Answers "which disk, which network, any snapshot" without booting. Read it in Notepad; never save |
| `.vmdk` | The virtual disk. A single file of 9 to 10 GB with no `-s001` or `-flat` companions is consistent with a monolithic sparse disk (inference from the phone listing) | If `-00000N.vmdk` delta files exist, the base `.vmdk` is NOT the current state: booting or mounting it alone shows an older machine |
| `.nvram` | BIOS or UEFI variables (boot order). Both files are 271 KB; VMware's UEFI nvram files are usually this size and BIOS ones much smaller, so UEFI is suggested; confirm with the `firmware` key | Matters only if a disk is ever attached to another VM configuration, which this plan never does |
| `autoinst.flp` | Almost certainly VMware "Easy Install" answer floppy (confirm from `floppy0.fileName` in a `.vmx`). It holds the unattended answer file with the local Administrator password typed at build time | Means a desktop VMware product (Workstation, Player or Fusion) built that VM from an ISO. Which VM, and what that VM later became, is Cannot determine. A copy opened with 7-Zip may give back a forgotten build-time password; keep it private |

Not seen but must be looked for (the listing came from a phone and may be incomplete):

| File | Meaning | Consequence |
|---|---|---|
| `.vmsd` | Snapshot database (text) | Content beyond `.encoding` and `snapshot.lastUID` means snapshots exist |
| `.vmsn` | One per snapshot | Confirms a snapshot |
| `name-000001.vmdk` ... | Snapshot delta disks | The live disk is the newest delta; do not boot or mount the base alone |
| `.vmss`, `.vmem` | Suspended state and memory | The VM was suspended, not shut down. Stop and report; do not resume a suspended DC without discussing it |
| `vmware.log`, `vmware-0/1/2.log` | Logs of the last four runs | First lines name the VMware product, version and host OS; later lines show the disk files opened and how the VM was powered off. Cheapest way to learn the host product |
| `name.vmx.lck/`, `name.vmdk.lck/` | Lock folders | Present on a powered-off VM means an unclean close or a copy taken while running. Never delete them in the original |
| `.vmxf` | Supplementary XML | Harmless |

### A.2 The two VMs as currently known

Updated 2026-10-21 (see A.11 for the evidence behind each cell).

| Item | DC2.Eric.Roly | Windows Server 2019 |
|---|---|---|
| Files | `.vmx` 4 KB, `.vmdk` 10,090,304 KB, `.nvram` 265 KB, `.vmsd` 0 KB, `.vmxf` 4 KB | `.vmx` 3 KB, `.vmdk` 9,227,968 KB, `.nvram` 265 KB, `.vmsd` 0 KB, `.vmxf` 1 KB |
| Created | 21/10/2025 19:25 (Easy Install, lab PC TQ-D62ZRJ3) | 22/10/2025 19:03 (Easy Install, lab PC TQ-7SXZNJ3) |
| Runs | 21/10 19:25 to 21:05 (desktop by 19:40; guest restarts 20:23 and 20:24); 22/10 19:16 to 20:55 (no restart). Both ended with the Workstation Power Off button while Windows was running | 22/10 19:03 to 19:16:42 only; how it was stopped is unknown (its log was overwritten) |
| Easy Install floppy | Used on 21/10, detached at the 22/10 power-on (`floppy0.present = FALSE`) | Still attached (`floppy0.fileName = "autoinst.flp"`); the floppy in the folder (22/10 19:04) is this VM's |
| Snapshot chain, suspend file, lock folders | None | None |
| Firmware, guestOS, hardware | UEFI (Secure Boot certs present), `windows2019srv-64`, HW version 18, 2 vCPU, 2048 MB, NVMe 60 GB disk | Same |
| Network mode, MAC | custom `VMnet1`, e1000e, MAC 00:0c:29:32:7c:40 (regenerated 22/10; was 00:0c:29:2e:2b:c6) | NAT, e1000e, MAC 00:0c:29:b5:dc:ba |
| VMware Tools | 11.1.5.22735 installed and running on 22/10 | Never installed (`tools.remindInstall = TRUE`, no manifest) |
| Windows computer name | Cannot determine (not in any file; Easy Install generates `WIN-xxxx`; renaming to DC2 is unverified) | Cannot determine (almost certainly the generated `WIN-xxxx`) |
| OS edition and build | Server 2019 Datacenter (Desktop Experience), build 17763, full non-evaluation media; VMware default key, activation unknown | Same media and image; Setup did not finish (stopped mid-Setup at 12 to 13 minutes) |
| Domain membership and name | Cannot determine (possibly Eric.Roly, to be read inside Windows) | None (incomplete install) |
| Power-on hazard | Expect "Windows did not shut down properly" and, if AD DS is present, database soft recovery on first boot; let it finish | Floppy with the wipe-disk answer file and the install ISO are still attached: detach both before any power-on of a copy or Setup re-runs and wipes the disk |
| Role: DC / member / workgroup | Not a DC at its last boot (product type 3); workgroup or domain member unknown | Mid-Setup; not usable |
| IP, mask, gateway, DNS | Cannot determine (tutorial final DC2 is 172.16.0.2/24; unverified) | DHCP from VMware NAT, if anything |
| Local logon | Very probably local admin `471562641`, empty password (same wizard as the other VM; unproven) | Account never created (no first logon) |
| Domain / DSRM passwords known to the student | Cannot determine | Not applicable |

### A.3 Reading the `.vmx` files (read-only, on the originals)

Open with Notepad (right-click > Open with) or `type "DC2.Eric.Roly.vmx"` in a command prompt. Do not
double-click: the file association opens it in VMware. Do not save. Keys to read:

| Key | Look for |
|---|---|
| `displayName`, `guestOS`, `firmware` (`efi` = UEFI; absent = BIOS), `virtualHW.version`, `memsize`, `numvcpus` | Identity and hardware. If the host VMware is older than `virtualHW.version` the VM will not open; report, do not downgrade. Decline any offer to upgrade hardware |
| `scsi0:0.fileName` / `sata0:0.fileName` / `nvme0:0.fileName` / `ide0:0.fileName` | The boot disk: the `fileName` whose value ends in `.vmdk`. If it is `name-000001.vmdk` a snapshot chain exists. If it names a file not in the folder, the VM is broken as recovered |
| `nvram` | Should name the `.nvram` seen |
| `floppy0.fileName`, `floppy0.present`, `floppy0.startConnected` | The VM that names `autoinst.flp` was Easy-Installed. Harmless if still connected |
| `ethernet0.present`, `ethernet0.virtualDev`, `ethernet0.connectionType` (`bridged` / `nat` / `hostonly` / `custom`), `ethernet0.vnet`, `ethernet0.addressType`, `ethernet0.generatedAddress` or `ethernet0.address`, `ethernet0.startConnected`; any `ethernet1.*` | Bridged means the VM touches the real lab network the moment it boots connected: that is why A.5 boots disconnected. The MAC is the identity Windows ties the static IP to |
| `uuid.bios`, `uuid.location` | Machine UUID (keep) and file location (changes on move; triggers the moved/copied prompt) |
| `vm.genid`, `vm.genidX` | VM Generation ID present means the host supports the DC snapshot safeguard (A.7) |
| `checkpoint.vmState` | Non-empty names a `.vmss`: the VM is suspended. Stop and report |
| `tools.syncTime`, `time.synchronize.*` | Clock sync behaviour (A.9) |

Then read the `.vmsd` if it exists: `snapshot.numSnapshots`, `snapshot.current`, and per snapshot
`snapshotN.displayName`, `snapshotN.filename`, `snapshotN.disk0.fileName`.

Optional disk-chain check that reads 64 KB and writes nothing (PowerShell; path is a placeholder):

```
$f=[IO.File]::OpenRead('E:\Original\DC2.Eric.Roly\DC2.Eric.Roly.vmdk'); $b=New-Object byte[] 65536; $n=$f.Read($b,0,65536); $f.Close()
[Text.Encoding]::ASCII.GetString($b,0,$n) -split "`n" | ? { $_ -match 'createType|parentFileNameHint|parentCID|^CID|^RW ' }
```

`createType="monolithicSparse"` confirms a single-file disk; `parentFileNameHint` appears only in deltas. The chain
is complete when the `.vmx` disk key names file X, X's parent (if any) exists, and so on to the base, and the `.vmsd`
agrees. Any gap: do not boot.

### A.4 Preserve first: copy everything before any boot

1. Find the real folder structure (each VM normally has its own folder; the phone view may have flattened two
   folders). Record the paths. Confirm VMware is closed and no `.lck` folders are appearing.
2. Check free space: at least the total size of all VM files (about 20 GB; more if deltas exist).
3. Copy the whole folder(s), including hidden files, to a second location. Windows (paths are placeholders):
   ```
   mkdir D:\VM-work
   robocopy "E:\Original\DC2.Eric.Roly" "D:\VM-work\DC2.Eric.Roly" /E /COPY:DAT /DCOPY:T /R:2 /W:5 /LOG:D:\VM-work\copy-DC2.log
   robocopy "E:\Original\Windows Server 2019" "D:\VM-work\Windows Server 2019" /E /COPY:DAT /DCOPY:T /R:2 /W:5 /LOG:D:\VM-work\copy-WS2019.log
   ```
   macOS or Linux: `cp -a` or `rsync -a`. Compare counts and sizes (`dir /s /a` both sides, or the robocopy
   summary: Copied = Total, Failed = 0). `Get-FileHash` on the disks is optional and slow but definitive.
4. Leave the original alone. Open only the copy in VMware (File > Open > the `.vmx` under `D:\VM-work`). Do not
   power on yet.
5. At the first power on of the copy, VMware asks whether the VM was moved or copied. Answer **I Moved It**.
   "I Copied It" generates a new `uuid.bios` and (when `addressType = generated`) a new MAC; Windows may then
   present the NIC as a new adapter with DHCP defaults while the static IP stays on the old hidden one, and on
   a DC that also disturbs DNS server bindings. "I Moved It" keeps the identity. Afterwards confirm
   `ethernet0.generatedAddress` in the copy's `.vmx` is unchanged.
6. If VMware says the VM "appears to be in use" because of stale `.lck` folders in the copy, choose Take Ownership
   only after confirming nothing else has it open.
7. Optional (Workstation Pro or Fusion; Player cannot): take a NEW snapshot of the copy before the first power on,
   named "as-recovered 2026-10-15". Note this legitimately creates a `-000001.vmdk` and a `.vmsn` in the copy. It is
   a way back to the never-booted state while the VM is still isolated. See A.7 for when it must never be used.

### A.5 Safe first boot: network disconnected, read-only commands, clean shutdown

One VM at a time. Start with the one whose `.vmx` has been read.

Before power on: VM > Settings > Network Adapter > untick **Connect at power on** (Fusion: untick Connect
Network Adapter). Leave the adapter present. With the cable "unplugged", a stale DC cannot answer DNS or Kerberos
for the live lab and a duplicate IP cannot collide with anything. Confirm the host clock and time zone are right
(A.9). Plan to finish within an hour (A.8).

Power on and wait. A DC with no network can take several minutes to reach the logon screen ("Applying computer
settings", "Please wait for the Group Policy Client"). Do not force power off: that is an unclean shutdown of a
directory database.

What the screen may show, and what it means:

* A logon screen with "Other user" and a **Sign in to:** line: the NetBIOS domain name is right there. Screenshot
  it before typing. This is the first real evidence of the domain (possibly Eric.Roly; only what the screen shows
  counts). Log in as `<DOMAIN>\Administrator` on a DC, or `.\Administrator` on a member or standalone server.
* **Windows OOBE** (region, licence, Administrator password set-up): the VM is a fresh or generalised install,
  not a DC. Screenshot, power off cleanly from the OOBE screen (Shift+F10 then `shutdown /s /t 0`), record.
  Completing OOBE is a write action; do not do it in this pass.
* **"The user's password must be changed before signing in"**: the 42-day password policy working after a year.
  Changing it is unavoidable to log in; do it at the console, record the new password privately. Not a fault.
* **"Windows License is expired"** or a black desktop: Evaluation expired (A.8). Keep going; capture the licence
  state first.
* Password unknown: stop, shut down cleanly (Ctrl+Alt+Del is not available; VM > Power > Shut Down Guest works
  only with Tools; otherwise wait and use the power button on the logon screen), report. No password reset tools.

Then run this in an elevated PowerShell window and save output (`mkdir C:\Lab8-Evidence` first;
`<command> | Out-File C:\Lab8-Evidence\<name>.txt`). Screenshot each. This is the ONE first-boot command list used
everywhere in this report (Sections C, D and E refer back to it).

| Command | What it answers |
|---|---|
| `hostname`; `whoami` | Computer name; logged-on account and domain |
| `Get-CimInstance Win32_ComputerSystem \| Select Name,Domain,PartOfDomain,DomainRole` | DomainRole: 0/1 workstation, 2 standalone server, 3 member server, 4 backup DC, 5 primary DC (holds PDC emulator) |
| `systeminfo` | OS name, version, build (6.3.9600 = 2012 R2; 10.0.17763 = 2019), Evaluation or not, Domain or WORKGROUP, install date, time zone |
| `ipconfig /all` | Host name, primary DNS suffix (the domain FQDN), adapter name, MAC (compare with the `.vmx`). "Media disconnected" is expected; in that state IP, mask, gateway and DNS are hidden, so also run the next row |
| `netsh interface ipv4 show config`; `Get-NetIPAddress -AddressFamily IPv4 -PrefixOrigin Manual`; `Get-DnsClientServerAddress -AddressFamily IPv4` | The configured static address, mask, gateway and DNS servers even while disconnected |
| `Get-WindowsFeature \| Where Installed \| Select Name,DisplayName` | Installed roles: AD-Domain-Services, DNS, FS-FileServer, FS-DFS-Namespace, FS-DFS-Replication, FS-Resource-Manager, UpdateServices, Web-Server, GPMC. These map directly to the work packages |
| `Get-Service NTDS,DNS,DFSR,Netlogon,KDC,W32Time -ErrorAction SilentlyContinue` | NTDS exists only on a DC |
| `Get-ADDomain -Server localhost`; `Get-ADForest -Server localhost`; `Get-ADDomainController -Filter * -Server localhost \| Select Name,HostName,IPv4Address,Site,IsGlobalCatalog,OperationMasterRoles,OperatingSystem` (DC only; `-Server localhost` lets the cmdlets work offline) | Domain DNS and NetBIOS names, DomainMode, ForestMode, PDC emulator, all DCs with sites and FSMO roles |
| `repadmin /showrepl`; `Get-ADReplicationPartnerMetadata -Target $env:COMPUTERNAME -Scope Server \| Select Partner,LastReplicationSuccess,LastReplicationResult` (DC only) | Replication partners and the date of the last success (expect around 2025-10-22). Decides Section C |
| `Get-ADObject -Server localhost -Identity "CN=Directory Service,CN=Windows NT,CN=Services,$((Get-ADRootDSE -Server localhost).configurationNamingContext)" -Properties tombstoneLifetime` (DC only) | The forest tombstone lifetime (expect 180) |
| `Get-WinEvent -LogName "Directory Service" -MaxEvents 300 \| ? { $_.Id -in 2042,1388,1988,2095,2170,1864 } \| ft TimeCreated,Id,Message -Wrap` (DC only) | Replication-health events (C.1) |
| `dfsrmig /getglobalstate`; `Get-WinEvent -LogName "DFS Replication" -MaxEvents 100 \| ft TimeCreated,Id,Message -Wrap` (DC only) | SYSVOL replication state; Event 4012 (offline too long) or 2213 (dirty database) need a decision before GPO work (C.5) |
| `Get-DnsServerZone \| Select ZoneName,ZoneType,IsDsIntegrated,ReplicationScope` (DNS role only) | Zone type and replication scope (WP5) |
| `cscript //nologo C:\Windows\System32\slmgr.vbs /dlv`; `... /xpr` | Licence channel, status, remaining rearm count, expiry (A.8) |
| `w32tm /query /status`; `w32tm /query /source`; `Get-Date`; `tzutil /g` | Time source and zone (A.9) |
| `Get-WinEvent -FilterHashtable @{LogName='System'; Id=1,12,13,41,1074,6005,6006,6008} -MaxEvents 60 \| ft TimeCreated,Id,ProviderName` | How the VM was shut down in 2025 (6006 clean, 6008/41 unclean) and the clock correction at this boot (Id 1) |

Do NOT run `dcdiag` or `netdom query fsmo` in this disconnected boot: they stall or fail without DNS and prove
nothing. They belong to Phase 2 (C.7) once the NIC is connected. A cmdlet that is "not recognized" is itself a
finding (role or tools not installed); record it, install nothing.

Shut down cleanly (Start > Power > Shut down, or `shutdown /s /t 0`) and wait for VMware to show powered off.
Repeat for the second VM. Do not reconnect either NIC until Section B has confirmed switch port, VLAN and
addressing, and both identities are known.

### A.6 Optional alternative that never boots: read a disk copy offline

Only on a copy of the disk, never read-write, and not useful on the base disk if a snapshot chain exists. 7-Zip
opens a `.vmdk` directly (right-click > 7-Zip > Open archive; browse the NTFS partition to
`Windows\System32\config\`; copy out `SYSTEM` and `SOFTWARE` only, into `C:\HiveCopy\`). Workstation Pro also has
File > Map Virtual Disks with "Open file in read-only mode". Then, on any Windows machine, elevated:

```
reg load HKLM\OFFSYS C:\HiveCopy\SYSTEM
reg query HKLM\OFFSYS\Select /v Current
reg query HKLM\OFFSYS\ControlSet001\Control\ComputerName\ComputerName /v ComputerName
reg query HKLM\OFFSYS\ControlSet001\Services\Tcpip\Parameters
reg query HKLM\OFFSYS\ControlSet001\Services\Tcpip\Parameters\Interfaces /s
reg query HKLM\OFFSYS\ControlSet001\Services\NTDS\Parameters
reg query HKLM\OFFSYS\ControlSet001\Services\DNS\Parameters
reg unload HKLM\OFFSYS
reg load HKLM\OFFSOFT C:\HiveCopy\SOFTWARE
reg query "HKLM\OFFSOFT\Microsoft\Windows NT\CurrentVersion" /v ProductName
reg query "HKLM\OFFSOFT\Microsoft\Windows NT\CurrentVersion" /v EditionID
reg query "HKLM\OFFSOFT\Microsoft\Windows NT\CurrentVersion" /v CurrentBuild
reg unload HKLM\OFFSOFT
```

`reg load` writes to the hive file it opens, so it must run against the copied-out hive, never a read-only mapped
volume. `Tcpip\Parameters\Domain` is the joined domain (empty = workgroup). `Interfaces\{GUID}` with `EnableDHCP`
= 0 holds `IPAddress`, `SubnetMask`, `DefaultGateway`, `NameServer`. `Services\NTDS\Parameters` exists only on a
machine that is or was a DC. `EditionID` ending in `Eval` means Evaluation. Copy out nothing else (SAM, SECURITY
and NTDS.dit hold password material) and delete `C:\HiveCopy` when done.

### A.7 Snapshot caution for domain controllers

* Never revert a DC to an older snapshot and never boot it from an older delta. Windows Server 2012+ DCs on a
  VM-Generation-ID-aware hypervisor (VMware Workstation 10+, ESXi 5.0 U2+) detect it (event 2170) and reset
  their invocation ID, which limits the damage; without it the result is USN rollback (event 2095) and a
  quarantined DC. Either way the latest directory state is lost. So no revert.
* Do not delete or consolidate snapshots on the copy until A.3 has documented the chain. A VM running on a
  delta works fine; leave it.
* Do not attach either disk to another VM configuration. Not needed by this plan; forbidden by the rules.
* The optional "as-recovered" snapshot (A.4 step 7) may be used only while the VM is still isolated. Once a DC has
  talked to the other DC again, never revert to it.

### A.8 Evaluation licence expiry

**Update 2026-10-21: does not apply to these two VMs.** Both were installed from the full (non-evaluation)
Server 2019 media, Datacenter edition (A.11 item 6). The key applied at first logon is VMware Easy Install's
default, not a KMS client key, so expect an unactivated server: 30-day grace, then the "Activate Windows"
watermark and prompts, with no 180-day timer and no hourly shutdown. Capture `slmgr /dlv` and `/xpr` on first
boot to confirm. The paragraph below is kept for any Evaluation VM built later.

Server 2012 R2 and 2019 Evaluation editions run 180 days from install or last rearm, calendar time, so after
about a year off they have very probably expired unless rearmed within 180 days of the last use (Cannot
determine). An expired evaluation still boots and logs on, shows "Windows License is expired", may black the
desktop, and **shuts down once an hour**; on a DC that is an unclean interruption. Plan A.5 to finish within the
hour and capture `slmgr /dlv` and `/xpr` first. `slmgr /rearm` plus a restart resets the 180 days; the remaining
count printed by `/dlv` is the only number to trust. It is the only change to Windows this section allows, on the
copy, only after the read-only output is saved. Do not convert an evaluation DC to retail with DISM (unsupported
on a DC). Record channel, status, expiry and rearm count per VM.

### A.9 Clock jump and time agreement

VMware sets the guest clock from the host at power on, so a VM off for a year starts with today's date. That jump
is normal (System event Id 1 shows it). The risk is disagreement between machines: Kerberos tolerates 5 minutes
of skew; beyond that joins, replication and logons fail with confusing errors. The host clock must be right
first; every VM must agree to within seconds and share a time zone before any domain operation. Check with
`w32tm /query /status`, `w32tm /query /source`, `Get-Date`, `tzutil /g`. The PDC emulator is the domain's time
source and normally follows external NTP; offline it falls back to its own (host-aligned) clock. Fixing a wrong
clock is a Section C.6 step, not a first-boot step.

### A.10 What to send back (text and screenshots only; no disk images)

1. Full recursive listing of each VM folder, from a computer, with hidden files and sizes: PowerShell
   `Get-ChildItem -Recurse -Force "<folder>" | Select FullName,Length,LastWriteTime | Format-Table -AutoSize | Out-File -Width 500 listing.txt`, or `dir /a /s`.
2. Both `.vmx` files verbatim; any `.vmsd`.
3. `vmware.log` and `vmware-0/1/2.log` from each folder (or first and last 40 lines of each if large).
4. The disk-descriptor lines from A.3 if run.
5. VMware product and version (Help > About) and host OS, for the original host if available and for the host to
   be used now; host RAM and number of wired NICs.
6. Confirmation the backup copy exists (destination path, robocopy summary) and that the original was never
   opened in VMware.
7. After A.5 per VM: the logon-screen screenshot and the saved outputs of the A.5 table.
8. Or, after A.6 per disk copy: `ComputerName`, `Domain`, the static `Interfaces\{GUID}` block, whether
   `NTDS\Parameters` and `DNS\Parameters` exist, `ProductName`, `EditionID`, `CurrentBuild`.
9. Which Administrator passwords (local, domain, DSRM) the student has, as a yes/no per VM, never the passwords.

Received 2026-10-21: items 1 (as a screenshot), 2, 3 and the `.nvram` files and `autoinst.flp`. Still open:
items 5 (the host to be used now, its RAM and NICs), 6, 7 and 9.

### A.11 What the recovered files say (read 2026-10-21; checked against the raw logs by two independent passes the same day)

Copies of the text files are in `02_student_work/vm_inventory/SERVER_VM_FOR_LAB_8-9/`. The `.vmdk`, `.nvram`
and `autoinst.flp` stay with the originals.

**Timeline (Brisbane time, from the two logs and the file dates)**

| When | Event | Evidence |
|---|---|---|
| 21/10/2025 19:25 | `DC2.Eric.Roly` created and powered on by Easy Install on lab PC TQ-D62ZRJ3 (VMware Workstation 16.1.0 build 17198959; Dell, Windows 10 Education 22H2, i7-11700, about 64 GB RAM, LAN 172.30.96.x). Disk empty, boot from the Server 2019 ISO; NAT network; answer floppy attached. Two other VMs already running on the PC: the lab's 8 GB shared `Networking VM` (shown as "PC A") and an unidentified 2 GB VM, both there all evening | `vmware-1.log`; `.vmsd` date |
| 21/10/2025 19:36 to 19:40 | Setup reboots 19:36 and 19:37; Easy Install installs Tools 19:38; Tools reboot 19:39; **Windows at the desktop, auto-logged on, by 19:40** (15 minutes after power-on). Windows reports itself as build 17763, Datacenter, **product type 3 = a server that is not a domain controller** | `vmware-1.log` vm3d lines |
| 21/10/2025 19:40 to 21:05 | Configuration session: network changed while running from NAT to host-only (20:11), to custom `VMnet0` (the default bridged network, 20:43), to custom `VMnet1` (20:45, kept); guest-initiated restarts at 20:23 and 20:24 (84 s apart); the lab's USB console cable was passed into DC2 at 20:28 and back to the Networking VM by 20:30. After each restart Windows still reports product type 3 | `vmware-1.log` |
| 21/10/2025 21:05 | **Hard power-off from the Workstation Power Off button** while Windows was running (Tools heartbeat 0 s old, no guest shutdown) | `vmware-1.log` tail |
| 22/10/2025 19:03 | `Windows Server 2019` VM created by Easy Install on lab PC TQ-7SXZNJ3; its answer floppy overwrote `autoinst.flp` at 19:04 | `.vmsd`, `.vmxf`, floppy dates |
| 22/10/2025 19:14 | DC2 opened on TQ-7SXZNJ3 (different PC, same USB SSD mounted as `E:`). Moved-or-copied prompt answered by a click 2.9 s later as **copied** (reply=2): new `uuid.bios`, new `vm.genid`, new MAC `00:0c:29:32:7c:40`. A 75 s write to the `.vmx` on the slow USB drive delayed the guest; it actually booted at 19:16:33 | `vmware.log` |
| 22/10/2025 19:16:42 | `Windows Server 2019` VM hard-stopped from the host after 12 to 13 minutes, mid-Setup (DC2's image-apply phase alone took 11 minutes on the same drive); it never reached first logon or the Tools step. Its own log was overwritten | `vmware.log` tail, `.vmx`, `.vmxf` |
| 22/10/2025 19:16:51 to 19:17:18 | DC2's guest reports build 17763, Datacenter, **product type 3 (not a DC)**; Tools 11.1.5 running; user session up | `vmware.log` |
| 22/10/2025 19:17 to 20:55 | DC2 runs 1 h 38 min with **no reboot**; the only other VM on the PC is the lab's shared `Networking_VM_2022` (`D:\Shared_VMs\Networking_VM_2023\Networking VM.vmx`, which held the USB console cable). No DC1 ran on this PC that evening | `vmware.log` USB ownership 19:16:33; MemSched |
| 22/10/2025 20:55 | **Hard power-off from the Power Off button** again. Nothing has been powered on since | `vmware.log` tail; file dates |

**What this settles**

1. **DC2 was not a domain controller when it was last running.** Windows tells VMware's display driver its
   product type at every boot: 2 means domain controller, 3 means a server that is not one. DC2 reported 3
   after every restart on 21/10 and at its only boot on 22/10, and no restart followed on 22/10 before the
   hard power-off. A promotion needs a restart to complete, so the only way DC2 could hold a directory is a
   promotion started on 22/10 whose restart was lost to the Power Off button at 20:55, which would also have
   left it half-promoted. Expect a plain server: possibly renamed, possibly joined to a domain (the two quick
   restarts on 21/10 fit a rename plus a join), not a DC. The first boot (A.5) confirms it with
   `Get-CimInstance Win32_ComputerSystem` (DomainRole) in one line.
2. **Consequence for the plan.** Sections C.1 to C.3 (tombstone lifetime, force-demotion, role seizure) apply
   only if a DC turns up. The expected branch is C.4 / E Branch C: a fresh build of DC1 and DC2 (WP1 and WP2
   from the start), unless DC2's first boot or the search in Section G shows a domain or a DC1 somewhere. If
   DC2 is a member of a domain whose DC1 is lost, it still tells us the 2025 domain name.
3. **Host software**: VMware Workstation 16.1.0 (Pro) on TAFE lab PCs. Any Workstation or Player 16.1 or
   newer opens these VMs without a hardware upgrade (HW version 18). Workstation 17 will offer to upgrade the
   hardware version: decline. Keep `firmware = "efi"`: both are GPT/EFI installs and will not boot as BIOS.
4. **No snapshots, nothing suspended, no lock folders.** Both VMs can be copied. Copy to an internal SSD (the
   original USB SSD wrote at 8 to 75 seconds per operation on the lab PCs) and **put each VM in its own
   folder**: sharing one folder is what destroyed the second VM's log and overwrote DC2's answer floppy.
5. **DC2's Windows was never shut down cleanly.** Both sessions ended with the Workstation Power Off button
   (`cleanShutdown = TRUE` in the `.vmx` only means the VMware process exited normally). On first boot expect
   "did not shut down properly" and an NTFS log replay; let them run.
6. **Edition and media.** Windows Server 2019 **Datacenter** (Desktop Experience), build 17763, on both VMs:
   the answer file selects the image "Windows Server 2019 SERVERDATACENTER" and DC2's reported suite mask
   includes the Datacenter flag. The ISO `en_windows_server_2019_updated_sept_2019_x64_dvd_199664ce.iso` is
   full (MSDN-named) media, not the Evaluation ISO, so there is no 180-day timer and no hourly shutdown (A.8
   updated). The key that `slmgr /ipk` applied at first logon is VMware Easy Install's default key for that
   edition, not a Microsoft KMS client key; expect an unactivated server (30-day grace, then "Activate
   Windows" watermark and prompts, no shutdown). Read the real state with `slmgr /dlv` on first boot. No
   Server 2012 R2 media was ever used under this VMware profile. Register item 8 goes to the teacher with
   "2019 Datacenter" as the fact.
7. **`Windows Server 2019` is an interrupted install, not a server and not a template.** It was hard-stopped
   from the host 12 to 13 minutes after creation, before first logon; if booted it would try to resume Setup.
   **Hazard**: its answer floppy (wipes disk 0 without asking) and the install ISO are still attached. Do not
   boot it; rebuild from the ISO instead of trying to Sysprep it.
8. **DC2 was never bridged to the lab network for more than two minutes** (VMnet0 from 20:43 to 20:45 on
   21/10), then custom `VMnet1`. VMnet1 is host-only by default; each lab PC had three VMware host adapters on
   different random 192.168.x.0/24 subnets, so a host-only static address set on the first PC would not even
   have matched the second PC's VMnet1. Whether a lab PC had VMnet1 re-bridged lives in `C:\ProgramData\VMware`
   on that PC, not in these files. The first boot reads DC2's static IP, mask, gateway and DNS.
9. **DC2's identity changed on 22/10.** The student clicked "I Copied It" (the button the dialog itself
   recommends): new SMBIOS UUID, new VM Generation ID, new MAC. Windows keys the NIC on its PCI location (slot
   160, unchanged), so the same adapter and its IP settings survived. For our own first boot of the copy the
   answer is **I Moved It**.
10. **Logon account.** Easy Install created local administrator `471562641` (the student number) with an
    empty password; the auto-logon in the answer file is for the first logon only (`STOREPWD.INI` has
    `Enabled=0`), and `net accounts /MAXPWAGE:UNLIMITED` ran at that first logon on DC2. Proven for the wizard
    values of 22/10; DC2 was built by the same wizard from the same ISO the day before and its first logon
    demonstrably ran the same template, so very probably the same account and empty password. If DC2 was
    joined to a domain, the domain credentials are in no file.
11. **Hardware**: 2 vCPU and 2 GB RAM per VM. The guest never reported a hostname, IP, domain or edition name
    to VMware (`guestOS.detailed.data` is empty), so those come only from inside Windows.
12. **The `.nvram` files** hold UEFI boot entries and the VMware firmware's default certificate store; Secure
    Boot is not enabled (no `uefi.secureBoot.enabled` key). Harmless.
13. **A cheap extra lead.** Workstation took console screenshots for the VM thumbnail during both sessions
    (the last on 22/10 at 20:39). If a thumbnail image survives in the folder or its `caches` sub-folder, it
    shows DC2's screen near the end of the session. The `caches` date (16/03/2026) only shows the folder tree
    was copied or opened then; neither VM has been powered on since 22/10/2025.

**What remains unknown until a boot (A.5)**: DC2's Windows name, whether it is joined to a domain and which,
its static IP and DNS settings, its activation state, and whether any domain credentials are known.

---

## B. Existing network: read-only verification plan

Nothing here is confirmed until the commands have been run on the live devices and pasted back. Rules: only
`show` commands and `terminal length 0` in this pass (no `configure terminal`, `write`, `copy`, `reload`, `clear`,
`debug`, `erase`); never paste the five early CONFIG.txt files onto a live device (they would merge Lab 1 to 3
addresses over the current ones while leaving later OSPF, VPN and DHCP lines in place); no VM powered on for this
section until Section A's copy exists.

### B.0 The rack as photographed (2026-10-21)

Photo: `02_student_work/network/rack_photo_2026-10-21.jpg`. **The tape and marker labels on this shared rack
say nothing about what is configured on a device or what role it had** (the student's own statement; the
equipment is relabelled by whoever used it last). They are kept in the table only as physical handles, so that
cabling instructions can say "the 1941 labelled ISP, port S0/0/1" and be unambiguous.

| Position | Device (from the front panel) | Chassis label (physical handle only) | Slots and ports | Cables |
|---|---|---|---|---|
| 1 (top) | Cisco 2911 ISR (`PWR-2911-AC`) | rail tape `BNE`, marker `R1` | EHWIC 0 = HWIC-2T (two smart-serial ports, S0/0/0 and S0/0/1); EHWIC 1 to 3 blank; GE0/0, GE0/1, GE0/2; console RJ45 and USB; AUX | No network cables; powered (EN LED lit) |
| 2 | Cisco 1941 | rail tape `ISP` | EHWIC 0 = HWIC-2T (S0/0/0, S0/0/1); EHWIC 1 blank; GE0/0, GE0/1; console | Power cord only |
| 3 | Cisco 1941 | rail tape `CNS`, marker `3` / `R2` | EHWIC 0 = HWIC-2T; GE0/0, GE0/1; console | Power cord only |
| 4 | empty shelf | | | |
| 5 | Catalyst 3750G PoE-24 | none (old owner's asset and IP stickers) | 24 x GE, 4 x SFP | None; SYST LED lit (powered) |
| 6 | Catalyst 2960 Plus | marker `MG-S1`, sticker `5` | 24 x FE, 2 x SFP, 2 x GE | None; SYST LED lit (powered) |
| 7 | Catalyst 2960 | tape `BNE S1` | 24 x FE, 2 x GE | None; no LEDs (probably unpowered) |
| 8 (bottom) | Catalyst 2960 | tape `CNS S1` | 24 x FE, 2 x GE | None; no LEDs (probably unpowered) |

Two independent readings of the photo (2026-10-21) agree with this table on every device, port and cable; the
only additions were the switch LED states above and that the 1941s' `EHWIC 1` opening is double-width with two
blanks.

What this means:

1. **The rack is not cabled.** No serial cables between the HWIC-2T cards, no Ethernet between routers and
   switches, nothing into any switch port. The routers, the 3750 and the 2960 Plus show power; the two 2960s
   are dark (check their power cords before concluding anything about them). The "existing
   working lab network" in the brief does not exist in cabled form today. Routing, VLAN trunking and the host
   port cannot be tested until the topology is re-cabled, and that re-cabling is a physical change to record.
2. **Any router can take any role.** All three have a two-port serial card, so any of them can be the ISP
   (S0/0/0 to SB, S0/0/1 to MG). The 2911 has three GigabitEthernet ports; SB needs one (router-on-a-stick
   sub-interfaces on G0/0) and MG needs one (G0/1 in the early config). Roles are assigned when the devices are
   cabled and configured, and recorded in B.10; nothing on the chassis decides it.
3. **Switches.** Any two of the three 2960s can be SB-S1 and MG-S1; the 3750 is spare. Which switch, if any,
   still holds the SB-S1 configuration (VLANs 20/30/90, Gi0/1 trunk, Fa0/9-10 access VLAN 90) is unknown until
   `show running-config` is read on each.
4. **What is on the devices now is unknown**: the Lab 1 to 3 configs, the later 192.168.1.x / 192.168.2.0/28
   work, another class's build, or factory defaults. The prompt and `show running-config` decide (B.1, B.2).
5. **Consistency with the VM findings.** DC2 was on NAT and then VMnet1, never bridged; with the rack uncabled,
   the 2025 Lab 8 work almost certainly happened inside one PC's VMware networks and never touched these
   devices. For 2026, connecting DC1 at SB and DC2 at MG through this rack means: cable it, confirm or load the
   configs, then bridge each VM host to the right switch port (B.3, B.4).

Read-only lab step to add alongside Section G (no cables need moving to do this): console into each of the
seven devices in turn and capture `show version` and `show running-config` (B.2). The prompt alone answers
item 4 above.

### B.1 Known versus believed

| Item | Known early state (Lab 1 to 3 configs) | Believed current (UNVERIFIED) | Read it from |
|---|---|---|---|
| SB VLAN 20 (CS) | G0/0.20 192.168.10.1/26 | 192.168.1.0/26 | SB `show ip interface brief`, `show running-config` |
| SB VLAN 30 (Marketing) | G0/0.30 192.168.10.65/26 | 192.168.1.64/26 | SB same |
| SB VLAN 90 (Server) | G0/0.90 192.168.10.129/29 | 192.168.2.0/28, gateway 192.168.2.1 | SB same |
| SB to ISP | S0/0/0 209.165.200.1/28 | unknown | SB same |
| ISP | S0/0/0 209.165.200.2/28; S0/0/1 209.165.200.17/28 | unknown | ISP same |
| MG to ISP | S0/0/1 209.165.200.18/28 | unknown | MG same |
| MG LAN | G0/1 172.16.0.1/24 | 172.16.0.0/24, gateway 172.16.0.1 | MG same |
| SB-S1 | VLAN 20, 30, 90; Fa0/9-10 access VLAN 90; Gi0/1 trunk | believed unchanged | `show vlan brief`, `show interfaces trunk`, `show interfaces status` |
| MG-S1 | access ports Fa0/1-2; uplink port not recorded | believed unchanged | `show vlan brief`, `show cdp neighbors detail` |
| Routing between sites | not recorded | OSPF added later; areas, static routes unknown | `show ip route`, `show ip protocols`, `show ip ospf neighbor` |
| VPN / tunnel, DHCP, ACL, NAT, zone firewall | none in early configs | added later (VPN, DHCP known; ACL/ZBF/NAT unknown) | `show running-config` |
| VM host switch port | brief says SB-S1 Gi0/1 | unknown | `show mac address-table dynamic` (B.3) |

First sanity check: the prompt. `SB>`/`SB#`, `ISP#`, `MG#`, `SB-S1#`, `MG-S1#` mean the devices still carry the
lab configuration. `Router>`, `Switch>` or "Would you like to enter the initial configuration dialog?" means the
device has been reset or re-used by another class: answer `no` to the dialog, type nothing else, stop and report;
the rest of this plan changes.

### B.2 Read-only commands per device

Console at 9600 8N1 (PuTTY or Tera Term), or whatever remote access exists. `show running-config` needs `enable`.
Passwords are not known here; if the early config files hold a plain-text (type 0) one, try it; do not decode
type 7 strings or run password recovery (it needs a reload and a config-register change) without the teacher.
Start every session with `terminal length 0` (session-only; stops `--More--`). Before pasting output into the
repo, replace every `enable secret`, `username ... secret`, `crypto isakmp key`, `pre-shared-key`, `ip ospf
message-digest-key`, `key-string`, `tunnel key`, SNMP community and similar with `<redacted>`.

Routers SB, ISP, MG (SB also gets `show vlans` for its sub-interfaces):

```
terminal length 0
show version
show running-config
show ip interface brief
show ip route
show ip protocols
show ip ospf neighbor
show access-lists
show cdp neighbors detail
show vlans                                   (SB only)
show ip interface <intf> | include access list     (for every addressed interface)
```

Conditional, only if the running-config contains the named lines:

| If running-config has | Run |
|---|---|
| `interface Tunnel<n>` | `show interfaces tunnel <n>` |
| `crypto isakmp` / `crypto map` / `tunnel protection` | `show crypto isakmp sa`, `show crypto ipsec sa` (`crypto ikev2` -> also `show crypto ikev2 sa`) |
| `zone security` | `show zone security`, `show zone-pair security`, `show policy-map type inspect zone-pair` |
| `ip nat` | `show ip nat translations`, `show ip nat statistics` |
| `ip dhcp pool` | `show ip dhcp pool`, `show ip dhcp binding` |
| a serial interface not `up/up` | `show interfaces serial <x/y/z>`, `show controllers serial <x/y/z>` |

Switches SB-S1, MG-S1 (Layer 2; routing, tunnel and crypto commands do not apply):

```
terminal length 0
show version
show running-config
show ip interface brief
show interfaces status
show vlan brief
show interfaces trunk
show mac address-table dynamic          (older IOS: show mac-address-table dynamic)
show spanning-tree                      (older IOS: show spanning-tree brief)
show cdp neighbors detail
```

If a switch config unexpectedly has `ip routing`, an `interface Vlan90` with an IP, or `ip dhcp pool`, paste it
and we reassess.

### B.3 Which switch port has the VMware host, without touching cables

1. Host MAC (no VM needed): on the VMware host, `ipconfig /all`. Record every adapter's name, Physical Address,
   media state and IPv4. Ignore "VMware Network Adapter VMnet1/VMnet8" (MAC 00-50-56-C0-xx-xx); they are
   host-side virtual adapters. If the host has Wi-Fi and Ethernet, the cabled one matters.
2. VM MAC (no VM needed): from the `.vmx` lines read in A.3 (`ethernet0.generatedAddress` or `ethernet0.address`).
   VMware-generated MACs start 00:0C:29; static ones usually 00:50:56. Also note any `ethernet1.*` lines.
3. Format: Windows prints `00-0C-29-AB-CD-EF`; Cisco prints `000c.29ab.cdef`.
4. On SB-S1 and MG-S1: `show mac address-table dynamic` (entries age out after 300 s, so run it right after the
   host has sent traffic, e.g. a ping to its gateway). Columns `Vlan`, `Mac Address`, `Type`, `Ports`. The host MAC's
   row gives the physical port and the VLAN the switch puts its frames into. Targeted:
   `show mac address-table address <mac>`.
5. Cross-check the router uplink with `show cdp neighbors detail` (the port where SB appears is the uplink; the
   host cannot be on it). If CDP is off: `show cdp`, `show lldp neighbors detail`; or read the router's interface
   MAC (`show interfaces GigabitEthernet0/0` on SB) and look it up in the switch MAC table. Do not enable CDP.

The Gi0/1 conflict. If the host is cabled to a trunk port, its untagged frames land in the native VLAN (VLAN 1
unless `show interfaces trunk` says otherwise), not VLAN 90, so DC1 could never reach 192.168.2.1 whatever IP it
has. You will know because the host MAC shows `Vlan 1` on a port that `show interfaces trunk` lists. If instead it
shows `Vlan 90` on Fa0/9 or Fa0/10, the host is where the early config expects it and the brief's port name is
what is wrong. Either way: record it against register item 9 and raise it with the teacher. Fix options, only
after the mapping is confirmed and only with the teacher's agreement: (1) move the host cable to a free access
port in VLAN 90 (a physical change that differs from the brief's named port); (2) not recommended, VLAN tagging on
the host NIC or in VMware. Do not change switch port configuration in this pass.

### B.4 VMware side

* Per VM, the evidence before Section A's copy exists is the `.vmx` line `ethernet0.connectionType`. After the
  copy exists, VM Settings > Network Adapter on the copy, screenshot, close with Cancel. Expected: Bridged. NAT
  (VMnet8) or Host-only (VMnet1) puts the VM behind the host on a private network: it would not appear in the
  switch MAC table and would be off the lab network whatever IP is typed in Windows.
* Workstation Pro: Edit > Virtual Network Editor > VMnet0 > "Bridged to:". If it says Automatic and the host has
  Wi-Fi, record that as a risk (VMware may bridge to Wi-Fi, and many Wi-Fi drivers drop frames with a foreign
  source MAC). Player has no Virtual Network Editor by default; use Network Adapter > Bridged > Configure Adapters
  on the copy instead. Fusion and ESXi differ; say which.
* One host or two? If both DCs run on one host with one NIC on one switch port, both land in the same VLAN at
  the same site, and DC2 cannot be on 172.16.0.0/24 at MG without a second NIC on a second VMnet, a second host,
  or a temporary SB address. Do not decide now; record how many hosts, how many wired NICs, which switch each
  cable reaches, and whether either `.vmx` has `ethernet1.*` lines.

### B.5 What each result proves

| Output | Look for | Proves |
|---|---|---|
| `show ip interface brief` | Serials `up/up`; sub-interfaces with the believed addresses; `administratively down` = shutdown; `down/down` = cable, clock or far end; `up/down` = encapsulation or keepalive | Layer 1/2 of SB-ISP-MG is alive; 192.168.2.1 (SB G0/0.90) and 172.16.0.1 (MG G0/1) actually exist |
| `show ip route` on SB / MG / ISP | SB: route to 172.16.0.0/24 (`O`, `S` or via `Tunnel`); MG: route to 192.168.2.0/28 (and 192.168.1.x); ISP: private routes (routed design) or only 209.165.200.x (transit-only, tunnel design) | The server subnets reach each other; which design is in use |
| `show ip protocols`, `show ip ospf neighbor` | `ospf <n>`, networks, passive interfaces; neighbours `FULL` | OSPF running and adjacencies complete; anything but FULL is broken |
| `show interfaces tunnel <n>` | `up/up`, source and destination, counters rising; `ip mtu` / `ip tcp adjust-mss` in config | Tunnel carries traffic. Large Kerberos and LDAP packets can fail over a tunnel while pings pass |
| `show crypto isakmp sa` / `ipsec sa` | `QM_IDLE` (or `READY` for IKEv2); encaps and decaps both rising | VPN phases up, traffic both ways |
| `show access-lists`, `show ip interface ... access list` | `deny` lines, hit counters, where applied | An ACL in the path between the server subnets, or an anti-spoofing ACL on ISP, would block AD. ICMP must allow unreachable (type 3 code 4) and time-exceeded, not only echo |
| zone commands | zones on LAN/WAN/tunnel, `inspect`/`pass`/`drop`, drop counters | A zone-based firewall that only inspects some protocols blocks the B.6 port set |
| `show ip nat ...` | translations for the server subnets | AD across NAT is unsupported; inter-site traffic must bypass it |
| `show ip dhcp pool/binding` | pool ranges and exclusions | Whether 192.168.2.2 to .5 or 172.16.0.2 fall inside a pool without exclusion (record only) |
| `show cdp neighbors detail` | device, platform, local and remote port | Confirms SB-S1 -> SB -> ISP -> MG -> MG-S1 port by port |
| `show interfaces trunk`, `show vlan brief`, `show interfaces status` | trunk ports and native VLAN; VLAN 90 members; `connected`/`notconnect` | Server VLAN exists; which ports carry it; which ports have live cables |
| `show mac address-table dynamic` | host MAC and VM MAC with port and VLAN | The definitive host-to-port mapping (B.3) |

Section B passes when: serials up/up along SB-ISP-MG; OSPF FULL or static routes such that SB reaches
172.16.0.0/24 and MG reaches 192.168.2.0/28; 192.168.2.1 and 172.16.0.1 configured; no ACL, zone policy or NAT
in the path of the B.6 ports in either direction; the host MAC on a VLAN 90 access port on SB-S1 (or the Gi0/1
conflict confirmed and recorded).

### B.6 Ports that must pass between 192.168.2.0/28 and 172.16.0.0/24, both directions

| Protocol / port | Use |
|---|---|
| TCP + UDP 53 | DNS |
| TCP + UDP 88 | Kerberos |
| TCP 135 | RPC endpoint mapper |
| TCP + UDP 389 | LDAP (UDP 389 is also the DC locator ping) |
| TCP 445 | SMB (SYSVOL, DFS-R, Group Policy) |
| TCP + UDP 464 | Kerberos password change |
| TCP 636 | LDAP over SSL |
| TCP 3268-3269 | Global Catalog |
| TCP 49152-65535 | RPC dynamic range, Server 2008+ (replication, DFS-R, Netlogon) |
| UDP 123 | Windows Time |
| ICMP echo/echo-reply; ICMP type 3 code 4 and type 11 | ping; path MTU discovery across a tunnel; tracert hops |
| TCP 9389 | AD Web Services (PowerShell AD module against the other DC); administration only |

TCP 5722 (DFS-R on Server 2008 only) is not needed on 2012 R2 or 2019.

### B.7 End-to-end tests from Windows (only after B.2 to B.5 are read and the VMs run from copies)

Use the addresses read inside each VM; 192.168.2.2 and 172.16.0.2 are tutorial expectations. From the DC at SB:
`ping 192.168.2.1`, `ping 172.16.0.1`, `ping 172.16.0.2`, `tracert -d 172.16.0.2`, then
`Test-NetConnection 172.16.0.2 -Port 389` (and 445, 53, 88, 135). From the DC at MG the mirror set against
192.168.2.x, plus `nslookup dc1.<domain> 192.168.2.2` and `nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain> 192.168.2.2`.

Reading: gateway ping fails -> VLAN or VMware mapping (B.3, B.4), not routing. `tracert` hops should match router
interfaces; with a tunnel the ISP hop is absent (expected); `*` hops with a final answer = ICMP time-exceeded
filtered. `TcpTestSucceeded : True` proves the port end to end; `PingSucceeded : False` with TCP True = ICMP
filtered somewhere (record, do not change). `Test-NetConnection` is TCP only; `nslookup` exercises UDP 53. A TCP
failure can also be Windows Firewall on the target: `Get-NetFirewallProfile | ft Name,Enabled` (record only).

### B.8 Change rule

Nothing from the early files is pasted. Any later change is proposed as a minimal diff (current lines, lines to
add, why), applied only after the running-config is saved to the repo and, for any physical change or anything
touching the brief's stated topology or addressing, only after the teacher agrees. Existing OSPF, VPN, DHCP, ACL
and NAT stay; if one blocks AD traffic the proposal is the smallest addition (one `permit` line in the right
position, one class-map entry), never a removal.

### B.9 What to paste back

1. Per router: prompt line, the common block (passwords redacted), `show ip interface ... access list` per
   interface, every conditional block its config justified, and one line per block NOT run and why.
2. Per switch: prompt line, the switch block (say which MAC-table spelling the switch accepted), CDP fallback if
   CDP printed nothing.
3. From the VMware host: `ipconfig /all`, host OS, VMware product and version, number of cabled NICs.
4. All `ethernet0.*` (and `ethernet1.*`) lines from both `.vmx` files.
5. The Virtual Network Editor / Configure Adapters screenshot.
6. Your reading of the host port: switch, port, VLAN column, trunk or not.
7. Anything that did not match the "believed" column, verbatim.
8. Only after 1 to 7 are reviewed: the B.7 outputs.

Field table for Section B (fill from pasted output; blank rather than guess; replace interface names with what the
device prints):

| Device | Interface | IP / mask | Status | VLAN | Connected to |
|---|---|---|---|---|---|
| SB | G0/0.20 / .30 / .90 | | | 20 / 30 / 90 | SB-S1 trunk port: |
| SB | S0/0/0 | | | - | ISP S0/0/0 (confirm) |
| SB | Tunnel (if any) | | | - | Peer: |
| ISP | S0/0/0, S0/0/1 | | | - | SB / MG (confirm) |
| MG | S0/0/1 | | | - | ISP S0/0/1 (confirm) |
| MG | G0/1 | | | - | MG-S1 port: |
| MG | Tunnel (if any) | | | - | Peer: |
| SB-S1 | Gi0/1 | - | | trunk or access? | |
| SB-S1 | Fa0/9, Fa0/10 | - | | | |
| SB-S1 | Host port (from MAC table) | - | | | host MAC: |
| MG-S1 | Uplink to MG | - | | | MG G0/1 (confirm) |
| MG-S1 | Fa0/1, Fa0/2 | - | | | |
| MG-S1 | Host port (if a host is at MG) | - | | | host MAC: |
| VMware host | wired NIC | | | | switch and port: |
| DC1 VM (name as read) | Ethernet0 (MAC) | | | | bridged to: |
| DC2 VM (name as read) | Ethernet0 (MAC) | | | | bridged to: |

---

## C. Existing Active Directory: what can be reused after a year offline

Nothing about the domain is confirmed. Until the name has been read on a booted machine it is written `<domain>`
in every command (possibly Eric.Roly; the filename is not evidence). This section is a decision tree: "if we find
X, then Y". Three rules for every branch: (1) nothing powers on before the Section A copy exists; (2) read-only
first (A.5, C.7); no write action (demotion, seizure, metadata cleanup, registry change, join, promotion, DNS
deletion) until the read-only output is saved and the teacher has been told; (3) one machine, one step at a time;
first boot always with the NIC disconnected and "I Moved It" (A.5).

**Expected branch (2026-10-21).** The VMware logs show Windows inside DC2 reporting itself as a non-DC server
at every recorded boot (A.11 item 1). Unless DC2's first boot or the Section G search shows otherwise, the
path is C.4 / E Branch C: a fresh build of DC1 and DC2. C.1 to C.3 stay in this report for the case that a DC
turns up after all.

### C.1 The 180-day problem: tombstone lifetime

Deleted AD objects become tombstones and are kept for the tombstone lifetime (TSL), then garbage-collected. The
default TSL is 180 days for forests created on Windows Server 2003 SP1 or later, so for a 2012 R2 or 2019 forest
unless someone changed it. Each DC records the last successful replication with each partner; if that is older
than the TSL, inbound replication from that partner is refused. **This is a time check, not a data check**: two DCs
switched off together with identical databases still refuse each other after 180 days. 358 days is well past it.

What it looks like: Directory Service log, Event ID 2042 "It has been too long since this machine last replicated
with the named source machine..."; `repadmin /showrepl` and `/replsummary` show the partner failing with result
8614; `dcdiag` fails the Replications test with the same text.

Read-only confirmation is already in the A.5 table (tombstoneLifetime, `Get-ADReplicationPartnerMetadata`,
`repadmin /showrepl`, the Directory Service events). If `LastReplicationSuccess` is around 2025-10-22, the 8614
refusal is certain once the DCs meet on the network with today's date.

Do NOT: set clocks back to 2025, raise the TSL, revert a snapshot, or leave the bypass key (C.2) set afterwards.

### C.2 Branch 1: both recovered VMs are DCs of the same domain

Finding: both boot; both show `DomainRole` 4 or 5; `Get-ADDomain` returns the same `DNSRoot` on both;
`repadmin /showrepl` on each lists the other.

Two documented ways past the 8614 refusal. Both go to the teacher with the saved A.5 output before anything runs;
the teacher's choice is recorded first.

**Option (b), least destructive: temporarily allow replication with a divergent partner.** Appropriate when both
DCs were off for the same period (as the identical file dates suggest), because then no deletion can have been
garbage-collected on one side only. Keeps both DCs, their 2025 promotion and configuration, and all existing
evidence. Steps: (1) advisory-mode lingering-object check, read-only, on each DC for each partition
(`repadmin /removelingeringobjects <DC-to-check> <GUID-of-reference-DC> <NC-DN> /advisory_mode`; the GUID is the
"DSA object GUID" printed by `repadmin /showrepl <referenceDC>`; partitions: the domain, Configuration, Schema,
DomainDnsZones, ForestDnsZones; results in Directory Service events 1938, 1946, 1942). If it reports lingering
objects, stop and discuss. (2) On the DC logging 2042 (both if both): `repadmin /regkey <DC> +allowDivergent`
(sets `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters\Allow Replication With Divergent and Corrupt Partner`
= 1). (3) `repadmin /syncall /AdeP` on each DC, then `repadmin /replsummary` until zero fails. (4) Immediately
`repadmin /regkey <DC> -allowDivergent` on every DC where it was set, and confirm `Strict Replication Consistency`
is still 1. (5) Save before and after `repadmin /showrepl`. Risk: lingering objects return if a deletion happened
on one side only; the advisory check in step 1 is what rules that out.

**Option (a): force-demote one DC, clean up, re-promote.** Appropriate if option (b) still fails, if `dcdiag`
shows database errors on one DC, or if one DC ran alone for part of the year. Keep the DC that holds the FSMO
roles (`netdom query fsmo`, C.7 Phase 2; should be DC1 if the brief was followed) and is a Global Catalog. On the
stale DC (NIC still disconnected): `Uninstall-ADDSDomainController -ForceRemoval -DemoteOperationMasterRole`
(the supported method on 2012 R2 and 2019; dcpromo is gone from 2012 on), or Server Manager > Remove Roles and
Features > AD DS > Demote > "Force the removal". Reboot; it is now a standalone server with its old name. On the
survivor: seize any role the stale DC held (`Move-ADDirectoryServerOperationMasterRole -Identity <survivor>
-OperationMasterRole <roles> -Force`); metadata cleanup (AD Users and Computers > Domain Controllers > delete the
stale DC > "Delete this Domain Controller anyway"; then AD Sites and Services > its site > Servers > delete the
NTDS Settings object and server object; or `ntdsutil` > `metadata cleanup`); remove its A, NS, SRV and `_msdcs`
GUID CNAME records in DNS; confirm `Get-ADDomainController -Filter *` shows the survivor only. Then time check
(C.6), connect the demoted machine's NIC to its confirmed segment (Section B), DNS client -> survivor,
`nslookup dc1.<domain>` screenshot (WP2 evidence), join, reboot, and promote into the EXISTING domain:
`Install-ADDSDomainController -DomainName "<domain>" -InstallDns -Credential (Get-Credential) -SiteName "<site read from Get-ADReplicationSite>"`.
Never `Install-ADDSForest`. This re-creates WP2 evidence; whether re-created evidence is accepted is the teacher's
call and is recorded as such.

My recommendation to put to the teacher: (b) first, (a) as the fallback. It follows the rule "do not rebuild what
works", it is reversible (the key is unset again), and it keeps the original 2025 work intact.

### C.3 Branch 2: only one DC comes back

Finding: one VM is a DC of `<domain>`; the other is not a DC (C.4) or does not boot; no further DC disk is found.
A single DC holds the complete directory (schema, configuration, domain, both DNS partitions). The domain is
expected intact; `dcdiag /v` in C.7 Phase 2 confirms it. What follows preserves it; it is not a rebuild.

* **The survivor is DC1** (whatever its VMware folder is called): if `Get-ADDomainController -Filter *` or
  `repadmin /showrepl` still lists a DC2 that no longer exists, metadata cleanup for that DC2 (C.2 option (a),
  survivor steps) once the teacher agrees, then build DC2 fresh and promote it into the existing domain (WP2).
* **The survivor is DC2 only**: `netdom query fsmo`. If any of the five roles sits on the missing DC1, seize them
  to DC2 (`Move-ADDirectoryServerOperationMasterRole -Identity DC2 -OperationMasterRole SchemaMaster,
  DomainNamingMaster,PDCEmulator,RIDMaster,InfrastructureMaster -Force`); the PDC emulator brings the time role
  with it (C.6). Metadata cleanup and DNS cleanup for DC1 as above. Save `nltest /dclist:<domain>` showing one DC.
  Build a new DC1 at SB (address read from the old DNS records; tutorial 192.168.2.2/28, confirm), DNS client ->
  DC2, time within 5 minutes, `nslookup dc2.<domain>` screenshot, join, promote into the existing domain with
  `Install-ADDSDomainController` (never a new forest). Optionally transfer the roles back to DC1 gracefully
  (`Move-ADDirectoryServerOperationMasterRole -Identity DC1 -OperationMasterRole ...` without `-Force`) once
  replication is healthy, so the end state matches the brief (DC1 at SB, DC2 at MG).
* Which OS the new DC runs is the teacher's call (C.8): a Server 2012 R2 machine cannot be promoted into a forest
  whose functional level is Windows2016.
* If DC1's old disk ever turns up after cleanup, it must never be booted on the network (it would be a rogue DC);
  keep it as a backup, inspect offline only.

### C.4 Branch 3: the VM is a plain member or a workgroup machine

From the A.5 output (`DomainRole`, installed roles, `Get-Service NTDS`):

* **DomainRole 3, member server of `<domain>`**: record hostname and roles. It may be SB-DNS-2 (DNS role),
  SB-FS2 (File Server, DFS, FSRM) or SB-DNS-1/SB-FS1; identify it only from what Windows shows. Its computer
  account still works (C.5). Do not Sysprep, do not rejoin "to be safe". Once a DC is reachable,
  `Test-ComputerSecureChannel` should be True; only if False, `Test-ComputerSecureChannel -Repair -Credential (Get-Credential)`.
* **DomainRole 2, workgroup server**: possibly a base template (the Easy Install floppy would fit a from-scratch
  unattended install, but that is inference). The only kind of machine on which Sysprep (OOBE, Generalize) is
  appropriate, and only on clones made from it, before they are joined. It can become the new DC1, SB-DNS-2 or
  SB-FS2 once C.8 is answered. Never a new forest on it while `<domain>` exists on another disk.
* **DomainRole 4 or 5 with a different domain name from the other VM**: two domains exist. Stop, record both
  names and both FSMO outputs, ask the teacher which is assessed.
* **The `Windows Server 2019` VM is DC1**: the VMware name and the Windows name differ; cosmetic. Do not rename
  files. Continue with C.2 (if the other VM is DC2) or C.3 (if it is not).

### C.5 What does not break after a year offline, and must not be "fixed"

| Item | Why it still works | Do not |
|---|---|---|
| Computer account passwords (DCs and members) | The machine itself initiates the 30-day change; offline it changes nothing, so its secret still matches AD | reset accounts; leave and rejoin |
| DSRM password | Stored locally, no expiry | reset it pre-emptively |
| Static IPs | In the registry per adapter. If an adapter shows no IP after the move, the likely cause is "I Copied It" (new MAC), not AD | re-address DC2 to 192.168.2.3 "because the video did"; it stays where it answers |
| AD-integrated DNS zones | In the directory partitions; come back with the database. Netlogon re-registers SRV records at start | delete or recreate zones; switch on scavenging |
| Sites, subnets, site link schedule, OUs, groups, GPOs | Directory data; confirm in C.7 | recreate them to "refresh" |
| User passwords past the 42-day maximum age | Windows asks for a new one at logon; policy working. Use the VM console (RDP with NLA refuses expired passwords) | change the policy to avoid the prompt |

Two things that MAY need a decision before GPO work: SYSVOL replicates with DFS-R on 2008+ domains
(`dfsrmig /getglobalstate`, expect Eliminated). DFS-R logs **Event 4012** when a member has been disconnected
longer than `MaxOfflineTimeInDays` (default 60) and stops replicating that folder; a hard power-off can leave the
database dirty, **Event 2213**, which on 2012 R2+ waits for the manual resume command printed in the event text.
Both are in the A.5 table. If either appears, record the exact text and take it to the teacher before acting;
Group Policy (WP9) depends on SYSVOL. The same check applies to Rep1 (WP7) if SB-DNS-1 and SB-FS2 are found.

### C.6 Time first

Kerberos tolerates 5 minutes of skew; aim for seconds. Read-only on every VM before its NIC is connected:
`w32tm /query /status`, `w32tm /query /source`, `w32tm /query /configuration` (Type NT5DS = domain hierarchy;
NTP = manual peer list). Healthy shape: the PDC emulator follows an external or manual NTP source; every other
machine shows NT5DS and a DC as source. "Local CMOS Clock" or "Free-running System Clock" on the PDC emulator
means the whole domain follows an undisciplined clock; record it (it feeds the WP2 written answers on NTP and
stratum). Which time source the lab should use is a question for the teacher, not a guess.

After NICs are connected: `w32tm /monitor` (all DCs with offsets) and `w32tm /stripchart /computer:<otherDC>
/samples:3 /dataonly`. If a clock is wrong: `w32tm /resync`; if the offset is too large for the service to accept,
set date and time manually once, PDC emulator first, then resync. Nothing joins, promotes or replicates until
every machine agrees.

### C.7 Phase 2 read-only health check (NIC connected)

Preconditions: A.5 saved for this machine; C.6 done; Section B has confirmed the port, VLAN and routing for this
VM; from another host on the segment `ping` and `arp -a` show the VM's IP is not already in use. Save every output
to `C:\Lab8-Evidence\<hostname>_<command>.txt` and copy the files into `02_student_work/`.

```
Test-NetConnection <gateway> ; Test-NetConnection <otherDC> -Port 389
nslookup dc1.<domain> ; nslookup dc2.<domain> ; nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain>
nltest /dsgetdc:<domain> ; nltest /dclist:<domain>
netdom query fsmo
dcdiag /v ; dcdiag /test:dns /v
repadmin /showrepl ; repadmin /replsummary
Get-ADReplicationSite -Filter * ; Get-ADReplicationSubnet -Filter * | Select Name,Site
Get-ADReplicationSiteLink -Filter * -Properties Cost,ReplicationFrequencyInMinutes,SitesIncluded,ReplicationSchedule
Get-DnsServerZone | Select ZoneName,ZoneType,IsDsIntegrated,ReplicationScope,DynamicUpdate
Get-DnsServerResourceRecord -ZoneName <domain> -RRType Soa | Format-List
Get-DnsServerZoneAging -Name <domain> ; Get-DnsServerScavenging
Get-ADOrganizationalUnit -Filter * | Select Name,DistinguishedName
Get-ADGroup -Filter 'Name -like "global_*"' | Select Name,GroupScope,GroupCategory,DistinguishedName
Get-ADComputer -Filter * -Properties OperatingSystem,IPv4Address,LastLogonDate | Select Name,OperatingSystem,IPv4Address,LastLogonDate
Get-DfsnRoot ; Get-DfsReplicationGroup ; Get-DfsReplicatedFolder ; Get-DfsrMembership
Get-FsrmQuotaTemplate ; Get-FsrmFileGroup ; Get-FsrmQuota ; Get-FsrmFileScreen        (FSRM server only)
Get-GPO -All | Select DisplayName,GpoStatus,CreationTime,ModificationTime
Get-SmbShare
```

| Command | Tells us | WP |
|---|---|---|
| `Get-ADDomain`, `Get-ADForest`, `Get-ADDomainController -Filter *` | Real domain name, functional levels, which DCs exist, sites, GC, FSMO, OS | 1, 2, 3, C.8 |
| `dcdiag /v`, `dcdiag /test:dns`, `netdom query fsmo`, `nltest /dclist` | DC health, DNS registration, role holders | 1, 2, 5 |
| `repadmin /showrepl`, `/replsummary` | Partners, last success, 8614; the exact evidence the brief asks for | 2, 4 |
| `Get-ADReplicationSite/Subnet/SiteLink` | SB and MG; four subnets; DEFAULTIPSITELINK 180 min and schedule (easier read in AD Sites and Services > Inter-Site Transports > IP > DEFAULTIPSITELINK > Change Schedule) | 3, 4 |
| `Get-ADOrganizationalUnit`, `Get-ADGroup global_*` | Admin, Server, global_computers (video used Servers/global_servers: register item 2) | 4 |
| `Get-DnsServerZone`, SOA record, aging | Primary, AD-integrated, ReplicationScope Domain (not Forest: item 3), refresh 30 min | 5, 6 |
| `Get-ADComputer -Filter *` | Which members exist: SB-DNS-2, SB-FS2, SB-DNS-1, CS-PC-1, any Linux object | 6, 7, 8, 9, 12 |
| DFS and FSRM cmdlets | Namespace `\\<domain>\Shares`, Rep1, Share1; QT-1, FG-1, screen on C:\share4 | 7, 8 |
| `Get-GPO -All`, `Get-SmbShare` | Desktop GPO, any AV or WSUS GPO; Share1, Share2, share4, Shared_Wallpaper$ | 7, 8, 9, 10, 11 |
| `w32tm` set | Time hierarchy | 2 (written answers), precondition for all |

A cmdlet "not recognized" means that role or its tools is not installed on that machine: record it, install nothing.

### C.8 The OS question: read exact edition and build, then stop

`systeminfo | findstr /B /C:"OS Name" /C:"OS Version"`; `Get-ComputerInfo | Select OsName,OsBuildNumber`
(2016+ only); `(Get-ADDomain).DomainMode ; (Get-ADForest).ForestMode`. Builds: 6.3.9600 = 2012 R2; 10.0.14393 =
2016; 10.0.17763 = 2019; 10.0.20348 = 2022.

The brief specifies Windows Server 2012 R2. On a 2012 R2 DC the promotion wizard's highest level is Windows Server
2012 R2. On a 2019 DC the wizard offers 2008 to 2016 and defaults to 2016 (there is no 2019 level), so
`Get-ADForest` on a 2019-built forest will most likely report `Windows2016Forest`, and no 2012 R2 machine can ever
be promoted into it. Record exactly what is reported and give it to the teacher together with register item 8. Do
not lower levels, rebuild or reinstall to match the brief.

### C.9 What must NOT be done

No Sysprep on a DC or any machine already joined (clones of a never-joined install only). No snapshot revert of a
DC. No new forest while an old domain exists on any disk (`Install-ADDSForest` and "Add a new forest" are off the
table, even "to get DC1 back quickly"). No re-addressing without a demonstrated reason. No clock set back, no TSL
increase, no bypass key left at 1. No deletion of DC objects, DNS records or site servers before the survivor is
chosen and recorded (C.2) or the missing DC is confirmed missing (C.3). No join, promotion or forced replication
before C.6 agrees. No attaching a DC's disk to another VM. No work with the NIC connected until A.5 is saved for
that machine.

### C.10 Decision table (every status today is Cannot determine)

| If we find ... | Next action | WP1 / WP2 once confirmed with evidence |
|---|---|---|
| Both VMs are DCs of the same `<domain>`; `repadmin` shows 8614 both ways | Save A.5 on both; record FSMO holder, TSL, LastReplicationSuccess; put C.2 (b) then (a) to the teacher; run the chosen option; capture | WP1 Blocked on the OS ruling (C.8) until answered, then Verified complete if healthy; WP2 Verified complete when `repadmin /replsummary` shows zero fails (re-promotion evidence accepted at the teacher's discretion) |
| Both are DCs and replication already works (no 2042) | Save `dcdiag /v`, `repadmin /replsummary`, `Get-ADDomainController`; move to WP3 | WP1 Blocked on the OS ruling; WP2 Verified complete |
| Only `DC2.Eric.Roly` is a DC; the other VM is workgroup or member; no DC1 disk | A.5 and C.7 on DC2; FSMO; teacher; C.8 answer; then C.3: seize, clean up, new DC1 into the existing domain | WP1 Blocked on the OS ruling, then Partially complete (new DC1 evidence); WP2 Partially complete (original join evidence to be located or explained) |
| The `Windows Server 2019` VM is DC1 and the other VM is DC2 | Cosmetic name difference; proceed as the first row | as the first row |
| The `Windows Server 2019` VM is DC1 and the other VM is not a DC | C.3 "survivor is DC1": clean any stale DC2 object; build DC2 fresh | WP1 Blocked on the OS ruling, then Verified complete; WP2 Not started |
| A VM is a member server (DomainRole 3) | Record hostname and roles; identify only from Windows; no Sysprep, no rejoin | WP6, WP7 or WP8 may move to Partially complete |
| A VM is a workgroup machine (DomainRole 2) | A resource (template or base for a new server), not evidence; Sysprep only its clones | unchanged |
| Two different domain names | Stop; record both; ask which is assessed | Blocked |
| The domain read inside Windows differs from the filename hint | Use the Windows name everywhere | unchanged |
| `Windows2016Forest` and build 17763 | Record; register item 8 to the teacher; no rebuild | WP1 Blocked on the OS ruling |
| Clocks differ by more than 5 minutes | C.6 first | precondition only |
| Event 4012 or 2213 in the DFS Replication log | Record exact text; teacher; resume only as the event instructs | WP9 at risk until SYSVOL replicates |
| Neither VM boots or contains AD DS | Section F asks; a new forest (WP1 from scratch) is planned only once no old domain exists on any disk | WP1, WP2 Not started |

---

## D. Lab completion matrix (12 work packages)

As of 2026-10-15 nothing has been booted or inspected, so no WP can be Verified complete or Partially complete.
"Existing evidence" lists only what physically exists; a filename or an installation is not evidence.

| WP | Official lab | Status | Existing evidence | Missing requirements | Required action now | Machine / device |
|---|---|---|---|---|---|---|
| 1 | 8.1 Install and promote DC1 (new forest, DNS, GC) | Cannot determine | No DC1 VM found. The `Windows Server 2019` VM is an unfinished install (A.11), not DC1. The VM beside DC2 on 22/10/2025 was the lab PC's own Networking VM. Only an unidentified 2 GB VM on 21/10 could be DC1 | The DC1 VM files, if any exist; its name, domain, roles; teacher ruling on 2019 vs 2012 R2 (Server 2019 now confirmed in DC2) | Search for other VM folders (Section G); if none, DC2's first boot decides between C.3 and a fresh build | Unknown; SB VLAN 90 |
| 2 | 8.1 Join and promote DC2 (additional DC, DNS, GC) | Cannot determine (expected: Not started) | `DC2.Eric.Roly` VM: Server 2019 Datacenter build 17763, Tools installed, last run 22/10/2025 20:55, no snapshots; Windows reported itself a non-DC server at every boot and no restart followed on 22/10, so the promotion almost certainly never happened; a rename and a domain join on 21/10 are possible | Proof DC2 is an additional DC with DNS and GC; `nslookup` of DC1 before join; replication health after a year offline (C.1); written answers NTP, stratum, authentication, AD DS | A.4 copy (to an internal SSD); A.5 first boot of the copy (NIC disconnected, "I Moved It", let recovery finish, the A.5 command table); then C.2 / C.3 with the teacher | `DC2.Eric.Roly` VM; last network custom VMnet1 (not the lab); MG LAN per tutorial, unverified |
| 3 | 8.2 Sites SB and MG, four subnets | Cannot determine | None | Sites SB, MG; subnets 192.168.1.0/26, 192.168.1.64/26, 192.168.2.0/28 -> SB; 172.16.0.0/24 -> MG; DC1 under SB, DC2 under MG; written answer on site-based client routing | After a DC is up: `Get-ADReplicationSite/Subnet`, screenshot dssite.msc; create only what is missing | DC1 preferred |
| 4 | 8.3 Site link, OUs, group, replication | Cannot determine | None | DEFAULTIPSITELINK 180 min, Mon-Fri 09:00-18:00 unavailable; OU Admin, OU Server, `global_computers` (Global, Security) in Server; Replicate Now; `repadmin /syncall /AdeP`, `/replsummary`; objects seen on DC2 | Read current site link, OUs, groups first; use the brief's names, not Servers/global_servers (item 2) | DC1 (create), DC2 (verify) |
| 5 | 8.4A DC1 DNS zone | Cannot determine | None | Primary, AD-integrated, scope "all DNS servers on DCs in this domain" (not forest: item 3); SOA refresh 30 min | `Get-DnsServerZone`, SOA; screenshot General and SOA tabs; change only what differs | DC1 |
| 6 | 8.4B SB-DNS-2 secondary zone | Cannot determine | None (no VM identifiable as SB-DNS-2) | SB-DNS-2 192.168.2.4, joined, DNS role, secondary zone with master DC1; SB-DNS-2 in Name Servers on DC1; transfers to Name Servers only; populated zone | Check the full listing for more VMs; else plan a new VM (fresh install, or a Sysprepped clone of a VM proven to be a never-joined workgroup install; never a clone of a DC or member) | SB-DNS-2 (find or build); DC1 |
| 7 | 8.5 DFS | Cannot determine | None | DFS roles on SB-DNS-1/SB-FS1 and SB-FS2; Share1/Share2 Everyone read-write on share and NTFS; `\\<domain>\Shares` (2008 mode); Rep1 memberships; Doc1.txt replicated | Teacher: which server is SB-DNS-1/SB-FS1 (item 6; not assumed to be DC1); `Get-WindowsFeature *FS*`, `Get-SmbShare` on any recovered server | SB-DNS-1/SB-FS1 (undecided); SB-FS2 192.168.2.5 (find or build) |
| 8 | 8.6 FSRM on SB-FS2 | Cannot determine | None | FSRM role; QT-1 100 KB soft, 85% event log (final value, not the 100 MB hard shown mid-wizard: item 4); C:\share4 shared; Event 12325; FG-1 (*.txt, exclude hello.txt); active screen; Event 8215; Quota Usage report DHTML on C:\share4 (confirm with the tutorial which report setting carries the "1000 files" value) | Depends on WP7's server; if a candidate exists, `Get-FsrmQuotaTemplate`, `Get-FsrmFileScreen` | SB-FS2 |
| 9 | 8.7 Desktop GPO | Cannot determine | None (no client VM in the listing) | `Shared_Wallpaper$` (read) with background.jpg; GPO "Deploy Desktop Background GPO" with wallpaper UNC `\\DC1\Shared_Wallpaper$\background.jpg` and the prevent-changing-background setting, linked; `gpupdate /force`, `gpresult /r`, rsop.msc on the test machine; teacher ruling CS-PC-1 vs DNS server (item 5) | `Get-GPO -All`, `Get-SmbShare` on DC1; ask the teacher about the endpoint | DC1; test endpoint |
| 10 | 8.8 Antivirus via GPO | Blocked | None | The 8.8 tutorial or package (product, installer, UNC, MSI or not, target OU); a target computer. Not started | Obtain the tutorial; no configuration until then | DC1 (GPO); target unknown |
| 11 | 8.9 WSUS, IIS, Windows Update GPO | Blocked | None | The 8.9 tutorial (host, content path, products, classifications, schedule, port); internet access; written answer "web application". Not started | Obtain the tutorial; the written answer can be drafted now | WSUS host unknown; DC1 (GPO) |
| 12 | 8.10 Join Ubuntu | Blocked | None | The 8.10 tutorial (version, commands, SSSD); an Ubuntu VM; `realm list` showing the domain. Not started | Obtain the tutorial; build the VM only after the domain is confirmed healthy | new Ubuntu VM; a DC for DNS |

---

## E. Minimum work remaining: shortest safe path

Rules for every step: work on the copy, read before you write, change only what differs from the brief, capture
evidence as you go (screenshot plus saved output, hostname and date visible), stop at the stop condition.

1. **Inventory and back up the VM files** (A.4, A.10 items 1 to 6). Stop if: the copy fails or space is short; the
   ORIGINAL folder listing shows `-00000N.vmdk` or `.vmsn` (snapshots), `.vmss`/`.vmem` (suspended) or `.lck`
   folders: record and do not boot until the chain is understood.
2. **Read both `.vmx` files as text** (A.3). Stop if: a disk or parent named there is missing; `guestOS` is not a
   Windows Server type (`windows8srv-64` = 2012/2012 R2; `windows9srv-64` or `windows2019srv-64` = 2016/2019).
3. **First boot of each copy, NIC disconnected, "I Moved It", the A.5 command table, clean shutdown.** The domain
   name is whatever Windows shows. Stop if: no working password (do not reset or bypass; ask the second student or
   the teacher); OOBE appears (not a DC; record); the two VMs report different domains.
4. **Confirm the live Cisco state, read-only** (Section B). Stop if: a device is reset or unreachable; the server
   subnets differ from the believed addressing; the host port is a trunk (item 9); an ACL, zone or NAT sits in the
   path. No config changes; no pasting of the early files.
5. **Decide the AD branch** from step 3 and put it to the teacher with the saved output:
   * **Branch A, both VMs are DCs of one domain**: C.2, option (b) first, (a) as fallback, teacher's choice
     recorded. Stop before any write if the backup is unverified or the teacher has not chosen.
   * **Branch B, one DC and the other confirmed not a DC**: C.3. If the other VM is a DC that merely cannot be
     logged into, that is Branch A with a blocker, not Branch B: stop and ask; do not seize or clean up.
   * **Branch C, no working DC**: fresh WP1 and WP2 builds. Stop if: the accepted OS (item 8) or the domain name is
     not confirmed by the teacher.
6. **C.6 time, then C.7 Phase 2 on each DC with its NIC connected.** Stop if: `dcdiag` database errors; 8614 not
   yet handled; clocks disagree.
7. **WP3 to WP8 in order**, each: inspect read-only (C.7), change only what differs, capture, move on. Stops: WP3 if
   DC2 is not healthy; WP4 if `/replsummary` shows failures; WP5 if the zone is not AD-integrated (record why
   before changing); WP6 if `nslookup <domain>` from SB-DNS-2 fails; WP7 if the SB-DNS-1/SB-FS1 identity is
   undecided (and SB-FS2, if cloned, is Sysprepped from a never-joined install before first boot on the lab
   network and before join); WP8 if Events 12325 / 8215 do not appear (fix, then screenshot).
8. **WP9 desktop GPO on DC1**, tested on the endpoint the teacher names (both if possible). Wallpaper is a user
   setting: link to the domain or the OU holding the test user, log on as that user, `gpupdate /force`,
   `gpresult /r` (User Settings section), rsop.msc, wallpaper on screen. Stop if `gpresult /r` does not list the GPO.
9. **WP10 to WP12 only once the 8.8 to 8.10 tutorials or teacher notes are in hand.** Suggested order: 8.9 WSUS
   (needs internet), 8.8 antivirus (needs the package), 8.10 Ubuntu (needs a new VM). Stop if any setting would
   have to be guessed.

VMs needed (6 or 7; most steps need two or three running at once; host RAM unknown):

| Machine | Purpose | Where it stands |
|---|---|---|
| DC1 | WP1, 3, 4, 5, 9; SB (tutorial 192.168.2.2) | Possibly the `Windows Server 2019` VM; unverified |
| DC2 | WP2, 3, 4; MG (tutorial 172.16.0.2) | Possibly `DC2.Eric.Roly`; unverified |
| SB-DNS-1 / SB-FS1 | WP7 primary member | Identity undecided; not necessarily DC1 |
| SB-DNS-2 | WP6; 192.168.2.4 | Not in the listing; likely new |
| SB-FS2 | WP7, 8; 192.168.2.5 | Not in the listing; likely new |
| Client (CS-PC-1 or teacher's choice) | WP9 test; possibly WP10 target | Not in the listing |
| Ubuntu | WP12 | None known; new |

Written answers the portfolio needs: NTP and why DCs depend on it (WP2); the NTP stratum hierarchy (WP2); user
authentication in the domain (WP2); what AD DS is (WP2); how AD sites direct clients to a nearby DC and share load
(WP3); what a web application is (WP11). These can be drafted now, independent of the VMs.

---

## F. Missing files and facts

Size classes: tiny (< 100 KB), small (< 5 MB), medium (5 to 50 MB), fact (an answer, not a file). **The two
`.vmdk` files (10.33 GB and 9.45 GB) must NOT be uploaded.** Everything below is text, a listing, a screenshot or
an answer.

| Item | Why | Unblocks | Size | Save to |
|---|---|---|---|---|
| Full recursive listing of the VMware folder with hidden files (A.10 item 1) | Reveals snapshots, suspend files, lock folders, logs, further VMs, folder structure | Section A; boot safety; WP6 to WP9 VM existence | tiny | `02_student_work/vm_inventory/` |
| `DC2.Eric.Roly.vmx`, `Windows Server 2019.vmx`, any `.vmsd` | Disk, network, firmware, snapshot facts | A.3; B.3 | tiny | `02_student_work/vm_inventory/` |
| `vmware.log`, `vmware-0/1/2.log` per VM | Host product and version; last power-off; disk chain | Host identification; boot safety | tiny to small | `02_student_work/vm_inventory/` |
| VMware host product and version; host OS; RAM; number of cabled NICs | Snapshot, mapping and network options; how many VMs can run | A.4, A.6, B.4, E scheduling | fact | report Section 0 |
| Which Administrator passwords are known (local, domain, DSRM), yes/no per VM | Without a logon nothing inside Windows can be read | A.5; branch choice | fact (never the passwords) | report Section 0 |
| The five Cisco `complete CONFIG.txt` files | Early baseline for comparison; never pasted onto devices | B.1 comparison; item 9 | tiny | `01_supplied_reference/cisco_configs/` |
| Current `show running-config` and the B.2 show output from each live device (redacted) | The only true picture of VLANs, routing, OSPF, VPN, ACLs, host port | Section B; DC1 to DC2 reachability | tiny | `02_student_work/network/` |
| `Week 7 Assess Lab 8 Install and Configure ADDS Services.docx` | Official wording and exact settings for 8.1 to 8.10 | Confirms the 12-WP mapping; WP4 to WP9 values | small | `00_assessment_documents/` |
| `ICTNWK529_ICTNWK546_AT1 WORKING ON.docx` (keep this filename until the teacher confirms the label) | Evidence format expected; what may already be captured | D "Existing evidence"; portfolio layout | small to medium | `02_student_work/` |
| `Fix_how to fix the SID when clone a Windows VM from a template.txt` | Sysprep procedure for fresh clones only | WP6, WP7 if a server is cloned | tiny | `01_supplied_reference/` |
| Tutorial videos or teacher notes for 8.8 to 8.10 | Exact antivirus, WSUS and Ubuntu settings | WP10 to WP12 (Blocked) | share a link; do not upload video | reference only |
| Second student's first name and the agreed domain | FQDNs, DFS namespace, written evidence; must match what Windows shows | Naming (verified in step 3) | fact | report Section 0 |
| Teacher: is Server 2019 accepted, or is 2012 R2 required (item 8) | Decides whether the recovered VMs can be reused at all | Branch choice; WP1, WP2 | fact | register |
| Teacher: final portfolio label (item 7) | Prevents mislabelling | Submission naming | fact | register |
| Teacher: GPO test endpoint (item 5) | Decides whether a client VM must exist | WP9; VM count | fact | register |
| Teacher: does the 12-sub-lab count match these 12 WPs (item 1) | Prevents missing or inventing a sub-lab | Section D | fact | register |
| Teacher: which server is SB-DNS-1/SB-FS1 (item 6) | Decides the DFS primary | WP7 | fact | register |
| `autoinst.flp` opened locally with 7-Zip: file list and whether `autounattend.xml` sets a ComputerName | How the Easy-Installed VM was named | WP1 identity | tiny, local only; do not upload (may contain a password) | note in Section 0 |

---

## G. Next single action

Done 2026-10-21: the folder listing, both `.vmx` files, the logs and the floppy were received and read (A.11).
Corrections the same day: the VM beside DC2 on 22/10/2025 was the lab PC's own Networking VM, not DC1; and
Windows inside DC2 reported itself as a non-DC server at every recorded boot (A.11 items 1 and 2).

**Now: make the working copy on an internal SSD, one folder per VM, and do the first isolated boot of the DC2
copy.** This is 15 minutes of work and answers the question everything else waits on: does a domain exist.

1. **Copy** (A.4). On an internal SSD create `D:\VM-work\DC2.Eric.Roly\` and copy into it ONLY the DC2 files:
   `DC2.Eric.Roly.vmx`, `.vmdk`, `.nvram`, `.vmsd`, `.vmxf`, plus `vmware.log` and `vmware-1.log`. Create
   `D:\VM-work\Windows Server 2019\` and copy that VM's five files into it (it will not be booted; keep it
   only as a record). Leave `autoinst.flp` and `caches` with the originals. Check the `.vmdk` sizes match
   (10,090,304 KB and 9,227,968 KB). The original folder is never opened in VMware again.
2. **Open the DC2 copy** in Workstation (File > Open > `D:\VM-work\DC2.Eric.Roly\DC2.Eric.Roly.vmx`). Do not
   power on yet. VM > Settings > Network Adapter > untick **Connect at power on**. Decline any offer to upgrade
   the virtual hardware. Take a snapshot named "as-recovered 2026-10-21" (Workstation Pro only).
3. **Power on.** At "moved or copied", click **I Moved It**. Expect "Windows did not shut down properly"; let
   it boot. Log in as `471562641` with an empty password (if that fails, `.\Administrator`; if nothing works,
   stop and report what the logon screen shows, especially any "Sign in to:" domain line).
4. **Run the A.5 table** in an elevated PowerShell and save the output. The four lines that matter most:
   `hostname`; `Get-CimInstance Win32_ComputerSystem | Select Name,Domain,PartOfDomain,DomainRole`
   (DomainRole 2 = workgroup server, 3 = member server, 4 or 5 = DC); `Get-WindowsFeature | Where Installed`;
   `netsh interface ipv4 show config`. Screenshot them. Then `shutdown /s /t 0` from inside Windows.
5. **Send back** the screenshots. What they decide:
   * DomainRole 2 (workgroup), no AD DS: no domain exists on this VM. Expected. Path: fresh build of DC1 and
     DC2 (E Branch C). The VM can be reused as the DC2 base (rename if needed; no Sysprep, it is not a clone)
     or rebuilt from the ISO; the teacher's OS ruling (item 8) decides which media.
   * DomainRole 3 (member of a domain): a DC1 existed in 2025. Record the domain name (it is the 2025
     `student1.student2` choice). Then the search below matters: find DC1 before building anything, so that
     a second forest with the same name is never created.
   * DomainRole 4 or 5: a DC after all. Stop and go to Section C.
   * `AD-Domain-Services` installed but DomainRole 3 or 2: a promotion that never finished. Stop and report.

**In parallel, low effort, no VM touched:** search for other VM folders and list the `caches` folder, because
if DC2 turns out to be a domain member, DC1 must be found or declared lost:

* Plug in every drive used for TAFE in 2025. File Explorer > This PC > search `*.vmx`, then `*.vmdk`;
  screenshot the results (right-click > Open file location shows the folder).
* Open Workstation; screenshot the Library pane (F9 if hidden); right-click each entry > Open VM directory.
* `dir /s /a` of the `caches` folder inside `SERVER VM FOR LAB 8-9`; send any `.png`, `.jpg` or `.bmp` in it.
* Ask Eric whether his drive has any `.vmx` (especially one named like `DC1...`); if so, the same lightweight
  files: folder listing, `.vmx`, `.vmsd`, `vmware*.log`.
* The only lead in the logs is an unidentified 2 GB VM that ran on lab PC TQ-D62ZRJ3 on 21/10/2025 beside
  DC2; TAFE lab PCs are usually re-imaged, so expect nothing from the PC itself.

**At the rack (decision 2026-10-21: start blank):** follow `05_analysis/Cisco_reset_and_rebuild_2026-10-21.md`:
capture each device's running-config to a log, erase, reload, verify blank, fill in its Part 5 table. The
build configuration follows once the two choices in its Part 4 (OSPF or static; one host with two NICs or
two hosts) are made.

---

## Appendix 1. Discrepancy register

| # | Source A | Source B | Use |
|---|---|---|---|
| 1 | Official labs 8.1 to 8.10 | Teacher: 12 sub-labs | 12 WPs internally; official headings in the portfolio; confirm mapping with the teacher |
| 2 | Video OUs `Admin`, `Servers`; group `global_servers` | Brief: `Admin`, `Server`; `global_computers` | Brief |
| 3 | Video DNS zone replication: forest-wide | Brief: all DNS servers on DCs in this domain | Brief |
| 4 | Video mid-wizard quota 100 MB hard | Video final: QT-1 100 KB soft, 85% event log | Final value |
| 5 | Desktop GPO test on CS-PC-1 | Later step: "Test it on DNS Server" | Both if possible; ask the teacher |
| 6 | SB-DNS-1 / SB-FS1 | Not stated to be DC1 | Identify from the live VMs; do not assume |
| 7 | Portfolio label AT1 / AT2 / AT4 Part 2 | | Keep the supplied filename; ask the teacher |
| 8 | Brief: Windows Server 2012 R2 | Recovered VMs appear to be Server 2019 | Verify in Windows (C.8); ask the teacher; do not rebuild |
| 9 | Brief: host on SB-S1 Gi0/1 | Early config: Gi0/1 is a trunk | Verify with the MAC table (B.3); do not assume |
| 10 | Video domain `Maggie.Zhong` | Brief: `student1firstname.student2firstname` | Our domain, read from Windows |
| 11 | Video DC2 temporarily 192.168.2.3 | Lab already routed SB to MG | Stay on 172.16.0.2 if DNS and routing work |
| 12 | Brief and early configs assume a cabled SB / ISP / MG network | Rack photographed 2026-10-21 is uncabled; the devices' current configs are unknown; chassis labels are meaningless | Lab 8 site and subnet names follow the brief (SB, MG). Device roles are assigned when cabled and configured; re-cabling is a recorded physical change |

## Appendix 2. Work packages to official labs

| WP | Lab | | WP | Lab |
|---|---|---|---|---|
| 1 | 8.1 DC1 | | 7 | 8.5 DFS |
| 2 | 8.1 DC2 | | 8 | 8.6 FSRM |
| 3 | 8.2 Sites and subnets | | 9 | 8.7 Desktop GPO |
| 4 | 8.3 Replication | | 10 | 8.8 Antivirus GPO |
| 5 | 8.4 Primary DNS zone | | 11 | 8.9 WSUS |
| 6 | 8.4 Secondary DNS | | 12 | 8.10 Ubuntu |

## Appendix 3. Method

Drafted 2026-10-15 from the student's handoff notes. Four technical sections were drafted independently, each
checked by two reviewers (technical accuracy; rule compliance and provenance) and revised, then a completeness
pass compared the set against the briefs. Contradictions found by that pass were resolved here: one first-boot
procedure (NIC disconnected, "I Moved It", the A.5 command table); both tombstone-lifetime options presented, with
a stated recommendation for the teacher; product-knowledge inferences labelled as such. Updated as live output
arrives.
