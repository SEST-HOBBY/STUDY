# Complex Cluster: Lab 8, Install and Configure AD DS Services

Official sub-labs 8.1 to 8.10 (teacher count: 12 sub-labs), worked here as 12 work packages (WPs). The
portfolio keeps the official 8.1 to 8.10 headings. The folder name carries no assessment number because the
supplied documents disagree (AT1 template, AT2 Portfolio, AT4 Part 2); the final label waits for the teacher.

Source priority: (1) current teacher directions and marking requirements, (2) the written Lab 8 instructions,
(3) portfolio evidence requirements, (4) the tutorial videos (8.1 to 8.6 reviewed; 8.7 to 8.10 not seen),
(5) the existing working lab configuration.

## Status (2026-10-15)

Old VMware files have been found and their configuration files and logs read (2026-10-21): `DC2.Eric.Roly` is a
Windows Server 2019 Datacenter VM built on 21/10/2025 and last run 22/10/2025 (hard power-offs, no snapshots)
that reported itself a non-DC server at every boot, so it was almost certainly never promoted; `Windows Server
2019` is an interrupted install; no DC1 has been found. Expected path: fresh build of both DCs, after one
confirming boot of the DC2 copy. The Cisco devices will be erased and rebuilt (decision 2026-10-21). See `05_analysis/Lab8_Initial_Report_2026-10-15.md` for the full report: recovered assets,
network verification plan, AD reuse decision tree, 12-WP completion matrix, minimum path, missing files, and the
single next action (Section G). The report was drafted with AI assistance and reviewed in two passes; product-knowledge
inferences are labelled as such and every fact about our machines is marked unverified until live output confirms it.

## File register

| File | Folder | Provenance | Notes |
|---|---|---|---|
| `Lab8_Initial_Report_2026-10-15.md` | 05_analysis | My analysis, drafted with AI assistance and reviewed | Initial report A to F plus the read-only procedures. Working document; updated as facts arrive |
| `Cisco_reset_and_rebuild_2026-10-21.md` | 05_analysis | My procedure, drafted with AI assistance | Decision to start the Cisco devices blank: capture, erase, verify, password recovery, the two design choices, device roles |
| `Cisco_build_SB_ISP_MG_2026-10-21.md` | 05_analysis | My build configuration, drafted with AI assistance | Addressing, cabling, full configs for SB, ISP, MG, SB-S1, MG-S1 (OSPF area 0), host bridging, checks and evidence |
| `vm_inventory/search_*.png`, `vm_inventory/workstation_library_2026-10-21.png` | 02_student_work | My screenshots | `*.vmx` and `*.vmdk` search of the 1 TB E: drive; Workstation library on the current PC |
| `network/before_erase/` | 02_student_work | Console logs captured before erasing each device | Passwords redacted |
| (wanted) `Week 7 Assess Lab 8 Install and Configure ADDS Services.docx` | 00_assessment_documents | TAFE | The written Lab 8 brief. Not yet in the repo |
| (wanted) `ICTNWK529_ICTNWK546_AT1 WORKING ON.docx` | 02_student_work | Student's working portfolio (template with teacher demo screenshots) | Not yet in the repo. Keep the filename until the teacher confirms the label |
| (wanted) `Fix_how to fix the SID when clone a Windows VM from a template.txt` | 01_supplied_reference | Teacher handout | Sysprep procedure for fresh clones only |
| (wanted) `SB / ISP / MG / SB-S1 / MG-S1 complete CONFIG.txt` | 01_supplied_reference/cisco_configs | Student's Lab 1 to 3 configs | Early addressing (192.168.10.x). Reference only; never paste onto live devices |
| `vm_inventory/SERVER_VM_FOR_LAB_8-9/` (`*.vmx`, `*.vmsd`, `*.vmxf`, `vmware.log`, `vmware-1.log`) | 02_student_work | Copied from the old VMware folder on 2026-10-21 | Text only, as received. The `.vmdk`, `.nvram` and `autoinst.flp` stay with the originals. Read in the report, Section A.11 |
| `network/rack_photo_2026-10-21.jpg` | 02_student_work | My photo of the lab rack | 2911, two 1941s (each with an HWIC-2T), 3750G, 2960 Plus, two 2960s; no cables connected; labels ignored. Read in the report, B.0 |
| (wanted) `show running-config` and show output per Cisco device, redacted | 02_student_work/network | Live devices, read-only | Text only; passwords and keys replaced with `<redacted>` |
| `screenshots/` | 02_student_work | My evidence screenshots | Suggested names `Lab8-01A-DC1-Promoted.png` ... `Lab8-10-Ubuntu-Realm.png` |

Conventions: never edit files in `00_`/`01_`; derived views go in `04_`; tools and checks in `05_analysis`.

## Discrepancy register (do not resolve silently)

| # | Source A | Source B | Use |
|---|---|---|---|
| 1 | Official labs 8.1 to 8.10 | Teacher: 12 sub-labs | 12 WPs internally; official headings in the portfolio |
| 2 | Video OUs `Admin`, `Servers`; group `global_servers` | Brief: `Admin`, `Server`; `global_computers` | Brief |
| 3 | Video DNS zone replication: forest-wide | Brief: all DNS servers on DCs in this domain | Brief |
| 4 | Video mid-wizard quota 100 MB hard | Video final: `QT-1` 100 KB soft, 85% event log | Final value |
| 5 | Desktop GPO test on `CS-PC-1` | Later step: "Test it on DNS Server" | Test both if possible; ask teacher |
| 6 | `SB-DNS-1` / `SB-FS1` | Not stated to be DC1 | Identify from the live VMs; do not assume |
| 7 | Portfolio label AT1 / AT2 / AT4 Part 2 | | Keep the supplied filename; ask teacher |
| 8 | Brief: Windows Server 2012 R2 | Recovered VMs appear to be Server 2019 | Verify in Windows; ask teacher; do not rebuild |
| 9 | Brief: host on SB-S1 Gi0/1 | Early config: Gi0/1 is a trunk | Verify with `show mac address-table`; do not assume |
| 10 | Video domain `Maggie.Zhong` | Brief: `student1firstname.student2firstname` | Our domain, read from Windows |
| 11 | Video DC2 temporarily 192.168.2.3 | Lab already routed SB to MG | Stay on 172.16.0.2 if DNS and routing work |
| 12 | Brief and early configs assume a cabled SB / ISP / MG network | Rack is uncabled and its current configs are unknown (photo 2026-10-21); chassis labels are meaningless | Site names per the brief; device roles assigned when cabled and configured; re-cabling recorded |

## Tutorial addressing (for reference)

SB server network 192.168.2.0/28, gateway 192.168.2.1: DC1 .2, (DC2 .3 temporary in the video), SB-DNS-2 .4,
SB-FS2 .5. MG LAN 172.16.0.0/24, gateway 172.16.0.1: DC2 172.16.0.2. AD subnets: SB gets 192.168.1.0/26,
192.168.1.64/26, 192.168.2.0/28; MG gets 172.16.0.0/24.

## Evidence checklist (screenshots into `02_student_work/screenshots/`)

8.1: both DCs with student-specific names and domain; AD DS and DNS roles; written answers (NTP, stratum, user
authentication, AD DS).
8.2: sites SB and MG; four subnets; DC1 under SB; DC2 under MG; written answer on site-based request routing.
8.3: DEFAULTIPSITELINK 180 min and the Mon to Fri 09:00 to 18:00 blocked schedule; Admin, Server,
global_computers on DC1; Replicate Now; same objects on DC2.
8.4: DC1 zone Primary, AD-integrated, domain-scope replication, SOA refresh 30 min; SB-DNS-2 secondary zone
properties; DC1 Name Servers and Zone Transfers with SB-DNS-2; populated zone on SB-DNS-2.
8.5: DFS roles; namespace `\\<domain>\Shares` with `\\SB-DNS-1\Share1` and `\\SB-FS2\Share2`; Rep1
memberships (C:\Share1 SB-DNS-1, C:\Share2 SB-FS2, replicated folder Share1); test file on both.
8.6: QT-1 100 KB soft 85%; quota on C:\share4; Event 12325; FG-1 (*.txt, exclude hello.txt); file screen on
C:\share4; test.txt blocked, hello.txt allowed; Event 8215; Quota Usage report (SB-FS2, C:\share4).
8.7: GPO, wallpaper UNC, restriction policy, client desktop, gpresult.
8.8 to 8.10: blocked until the tutorials or teacher instructions are available.
