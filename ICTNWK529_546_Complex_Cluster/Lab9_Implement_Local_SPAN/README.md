# Complex Cluster: Lab 9, Implement Local SPAN (Cisco Networking Academy lab CN 5.3.2.3)

Brief received 2026-11-04: `00_assessment_documents/Week_9_Teaching_Lab_CN-5.3.2.3_Implement_Local_SPAN.pdf`
(6 pages). It is a standalone Netacad lab: one 1941 router (R1), two 2960 switches (S1, S3), two PCs, flat
192.168.1.0/24 addressing, basic device settings, then a local SPAN session on S1 (source F0/5 = the router
port, destination F0/6 = PC-A running Wireshark), telnet from S1 to R1, pings from R1, ICMP capture, two
questions and a reflection (IDS vs IPS). It does NOT build on the Lab 8 network or domain; the earlier PRTG /
SNMP / syslog / IPsec notes in this folder came from ChatGPT guesses and are superseded (kept in
`02_student_work/network/` for the record, not for use).

Mapping to the rack (2026-11-04): R1 = the 1941 labelled ISP; S1 = the 2960 Plus (marker MG-S1); S3 = the 2960
labelled BNES1; PC-A (Wireshark) = the student's PC; PC-C = the classmate's PC. Configs and walkthrough:
`02_student_work/network/Lab9_SPAN_configs_2026-11-04.txt`. Same layout as Lab 8: `00_` supplied documents (never edit), `01_` supplied reference, `02_` my
work and screenshots, `03_` the report, `04_` extracted views, `05_` analysis and procedures.

## Rollover from the earlier labs

Lab 9 is expected to build on what Labs 1 to 8 left behind. What that is, as recorded in this repo:

| Asset | Where it is documented | State on record |
|---|---|---|
| Cisco network SB-S1 - SB - ISP - MG - MG-S1, OSPF area 0 | `../Lab8_.../02_student_work/network/Lab8_device_configs_2026-10-22.txt` and the rack photo | Configs issued 2026-10-22; verification output never received |
| SB computer (own PC, add-in NIC, green lead to SB-S1 Gi0/1) and MG computer (yellow lead to MG-S1 Fa0/1) | `../Lab8_.../05_analysis/Lab8_PC_and_VM_walkthrough_2026-10-22.md` | Cabled per photo |
| DC1 (192.168.2.2) and DC2 (172.16.0.2), domain `<student1>.<student2>` | same walkthrough, sections D to H; VM definitions in `../Lab8_.../02_student_work/vm_templates/` | Built per the student's evidence; not verified here |
| TAFE template VMs SERVERA / SERVERB / WIN10 and `Ubuntu 18.04.5` on the E: drive | `../Lab8_.../05_analysis/Lab8_Initial_Report_2026-10-15.md`, Section 0 | Exist; contents unknown |

Before any Lab 9 step that relies on one of these, run the matching check in `05_analysis/Rollover_state_check.md`
and record the result there.

## Known so far (2026-10-29, from the student's ChatGPT notes, not from the brief)

Lab 9 appears to be network monitoring with PRTG: a PRTG core on the SB side, a remote probe on DC2 at MG,
SNMP read-only on the Cisco devices, syslog from the devices to the probe/core, NTP from the SB router; an
IPsec VTI tunnel SB-MG is mentioned as possibly required. The DC2 VM was rebuilt on Workstation 17.6.4 (2 vCPU,
4 GB, 60 GB, e1000e) and was created with a host-only NIC, which must be changed to Bridged. The SB side is
being operated by the workmate at the same time: nothing on SB is erased or reloaded; SB gets additions only.
Device configurations: `02_student_work/network/Lab9_device_configs_2026-10-29.txt` (three-router SB-ISP-MG
version) and `02_student_work/network/Lab9_single_router_configs_2026-10-29.txt` (one 2911 serving both sites,
chosen 2026-10-29: Gi0/0 trunk to SB-S1, Gi0/1 to MG-S1, no serials, no OSPF).

## Waiting on

1. The written Lab 9 brief and its evidence template (into `00_assessment_documents/`).
2. Tutorial videos or the teacher's notes for Lab 9 (titles first).
3. Whether Lab 9 continues on the Lab 8 network and domain, or starts a new scenario.
