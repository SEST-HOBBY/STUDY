# Rollover state check (run at the start of Lab 9, before relying on anything from Lab 8)

Each row is one read-only check. Fill in the result and the date. A failed check means that asset is rebuilt
from the Lab 8 documents before Lab 9 uses it; nothing is assumed from screenshots.

## Network

| Check | How | Pass looks like | Result / date |
|---|---|---|---|
| Rack still cabled | compare with `rack_cabled_2026-10-21.jpg` | same six cables in the same ports | |
| Devices still configured | console: Enter twice | prompts `SB#`, `ISP#`, `MG#`, `SB-S1#`, `MG-S1#` (not `Router>` / `Switch>`) | |
| Routing | ISP: `show ip ospf neighbor` | 1.1.1.1 and 3.3.3.3 FULL | |
| Site to site | SB: `ping 172.16.0.1`; MG: `ping 192.168.2.1` | `!!!!!` both ways | |
| VLAN 90 / trunk | SB-S1: `show interfaces trunk`, `show interfaces status` | Gi0/2 trunk 20,30,90; Gi0/1 connected vlan 90 | |

## Computers and VMware

| Check | How | Pass looks like | Result / date |
|---|---|---|---|
| Lab NIC on each PC | ping its gateway from the host with a temporary address (walkthrough A) | reply from 192.168.2.1 (SB PC) / 172.16.0.1 (MG PC) | |
| Bridging | Edit > Virtual Network Editor > VMnet0 | bridged to the lab NIC by name (SB PC) | |
| VM files present | Workstation Library; folder `E:\Lab8-VMs\` | DC1 on the SB PC, DC2 on the MG PC, outside OneDrive | |

## Domain

| Check | How | Pass looks like | Result / date |
|---|---|---|---|
| DC1 is a DC of the agreed domain | on DC1: `Get-ADDomain`; Server Manager > Local Server | DNSRoot = `<student1>.<student2>`; roles AD DS, DNS | |
| DC2 is a DC of the same domain | on DC2: `Get-ADDomainController -Filter *` | DC1 and DC2 listed | |
| Replication | either DC: `repadmin /replsummary` | 0 fails | |
| DNS | on DC2: `nslookup dc1.<domain>` | 192.168.2.2 | |
| Sites, OUs, DFS, FSRM, GPO (only what Lab 9 needs) | `Get-ADReplicationSite -Filter *`, `Get-ADOrganizationalUnit -Filter *`, `Get-DfsnRoot`, `Get-FsrmQuotaTemplate`, `Get-GPO -All` | as built in Lab 8 | |
| Passwords known | domain Administrator, DSRM, local Administrator on member servers | yes / no (never the passwords themselves) | |

## Resources available for new servers

| Resource | Where | Checked |
|---|---|---|
| Server 2019 Datacenter ISO | `E:\OS ISO Files\Windows Server 2019\...199664ce.iso` | |
| TAFE templates SERVERA, SERVERB, WIN10 (2024) | `E:\TAFE VM's for home\...` (OS, Tools and passwords unknown; boot one isolated to find out) | |
| Ubuntu 18.04.5 VM | `E:\Ubuntu 18.04.5` (snapshot chain 000003 / 000004; copy the whole folder) | |
