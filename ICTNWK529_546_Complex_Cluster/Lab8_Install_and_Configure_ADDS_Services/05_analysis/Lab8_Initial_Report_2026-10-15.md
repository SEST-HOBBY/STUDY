# Lab 8 initial report: recovered assets, existing network, existing AD, completion matrix

Date: 2026-10-15. Status: nothing verified yet. This report records what is known, what is assumed, and the
read-only steps that turn assumptions into facts. It is updated as results come back. No configuration is to be
changed until Sections A to C are filled in from live output.

How to read the statuses: **Verified complete** (seen working, evidence captured), **Partially complete**,
**Not started**, **Cannot determine** (no live output yet), **Blocked** (waiting on a missing source or decision).

## 0. Current-state inventory (as known today)

| Item | Known | Source | Verified |
|---|---|---|---|
| VM `DC2.Eric.Roly` | .vmx 3 KB, .vmdk 10.33 GB, .nvram 271 KB, dated 2025-10-22 | iPhone directory listing | No |
| VM `Windows Server 2019` | .vmx 3 KB, .vmdk 9.45 GB, .nvram 271 KB, `autoinst.flp` 884 KB | iPhone directory listing | No |
| Snapshots, delta disks, logs, lock folders | Unknown; the listing may be incomplete | | No |
| VMware host product and version | Unknown | | No |
| Guest OS of each VM | Probably Windows Server 2019 (folder names); brief requires 2012 R2 | Filenames only | No |
| Windows computer names | Possibly DC2 and unknown | Filename only | No |
| Domain name | Possibly `Eric.Roly` (filename). Must be read inside Windows | Filename only | No |
| DC1 | No VM identifiable as DC1 in the listing. `Windows Server 2019` might be it | | No |
| DC2 promoted as a DC? | Unknown | | No |
| SB-DNS-2, SB-FS2, SB-DNS-1/SB-FS1, CS-PC-1, Ubuntu | No VM in the listing matches any of these | | No |
| Cisco SB, ISP, MG, SB-S1, MG-S1 | Early Lab 1 to 3 configs in hand (192.168.10.x). Later re-addressing to 192.168.1.x / 192.168.2.0/28 believed current | Config files; project memory | No |
| Routing SB to MG, VPN/OSPF, ACLs or zone firewall | Unknown today | | No |
| Which switch port the VM host uses; VLAN 90 membership | Unknown (brief says Gi0/1; early config makes Gi0/1 a trunk) | | No |
| Time since the VMs last ran | About 358 days (if file dates are last-modified dates) | File dates | No |

Sections A to F below are the detailed plan for each row.

<!-- SECTIONS A TO F ARE INSERTED BELOW -->

## G. Next single action

**Do this first, on the computer that holds the old VMware folder. It changes nothing.**

1. Copy the whole VMware folder to a second location (another drive or folder) and do not touch the copy or the
   original again until this report has Sections A to C filled in. Copy, do not move.
2. In the ORIGINAL folder, produce a full listing including hidden files and sizes:
   * Windows: `dir /a /s /-c "<path to folder>" > "%USERPROFILE%\Desktop\vm_listing.txt"`
   * macOS or Linux: `ls -laR "<path to folder>" > ~/Desktop/vm_listing.txt`
3. Open `DC2.Eric.Roly.vmx` and `Windows Server 2019.vmx` in Notepad (they are plain text) and copy their
   contents in full. Also copy the newest `vmware.log` if one exists (text).
4. Send back: the listing, both `.vmx` files, the log, and the name and version of the VMware product installed
   (Help > About). Do not send the `.vmdk` files.

What this answers: which disk belongs to which VM; whether snapshot or delta disks exist (`*.vmsd`, `*.vmsn`,
`*-000001.vmdk`); the guest OS each VM was created as; the network adapter mode (bridged, NAT, host-only) and
MAC address; whether the VMs were cleanly shut down (no `.lck` folders). With that, the first boot can be
planned safely (NIC disconnected, "I Moved It"), and Sections A and C get their first real entries.

Nothing in Work Packages 1 to 12 starts before this.
