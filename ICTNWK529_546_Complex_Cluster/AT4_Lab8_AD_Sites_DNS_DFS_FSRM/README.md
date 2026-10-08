# Complex Cluster, AT4 Part 2: Lab 8 (AD DS across two sites, DNS secondary, DFS, FSRM)

Labs 8.1 to 8.6, built on the existing SB/MG routed lab network. Procedure follows the ten instructor videos
(8.1 parts 1 to 4, 8.2, 8.3, 8.4 parts 1 and 2, 8.5, 8.6); names and scope follow the written brief. Lab 8.7 is
not covered by the videos and is out of scope here.

Folder name assumes this is AT4 of the ICTNWK529/546 cluster (the 8.6 video says "AT4 Part 2 template"). Rename
if the brief says otherwise.

Source priority: (1) written assessment and marking requirements, (2) the working lab network, (3) the videos.

## Missing before the build can be checked against the brief
1. The written Lab 8 brief and the AT4 Part 2 evidence template, into `00_assessment_documents/`.
2. The domain name: `<student1firstname>.<student2firstname>` from the brief. Not recorded here until confirmed.

## Current state (fill in from the live VMs; nothing assumed)

| Item | Recorded value | Checked |
|---|---|---|
| Domain FQDN | | |
| DC1 hostname / IP / mask / GW / DNS | target 192.168.2.2/28, GW .1 | |
| DC1 roles (AD DS, DNS) and domain | | |
| DC2 hostname / IP / mask / GW / DNS | target 172.16.0.2/24, GW 172.16.0.1 | |
| DC2 joined / promoted / same domain | | |
| SB-DNS-1 (also SB-FS1) IP and domain | | |
| SB-DNS-2 IP / domain | target 192.168.2.4/28 | |
| SB-FS2 IP / domain | target 192.168.2.5/28, DNS 192.168.2.2 | |
| Routing SB 192.168.2.0/28 to MG 172.16.0.0/24 (ping both ways) | | |
| DNS: DC2 and SB servers resolve DC1 and `_ldap._tcp.dc._msdcs.<domain>` | | |
| AD Sites and Services: sites, subnets, server placement | | |

## Stages (do not advance past a failed test)

1. Preflight networking
2. DC1
3. DC2 join and promotion (prove `nslookup DC1` first)
4. DC2 on MG, final addressing (skip the temporary 192.168.2.3 step if DC2 is already on MG and works)
5. Sites and subnets (8.2)
6. AD replication (8.3)
7. DNS secondary server (8.4)
8. DFS (8.5)
9. FSRM (8.6)
10. Evidence audit

## Video versus written brief: what to use

| # | Video shows | Use |
|---|---|---|
| 1 | Domain `Maggie.Zhong` | Our student domain |
| 2 | OUs `Admin`, `Servers`; group `global_servers` | `Admin`, `Server`; group `global_computers` (Global, Security) |
| 3 | Zone replication scope: forest-wide | All DNS servers on DCs **in this domain** |
| 4 | Quota briefly 100 MB hard | Final: `QT-1`, 100 KB, **soft**, 85% event-log warning |
| 5 | Rename screen briefly shows `FS2` | `SB-FS2` |

## Practical notes the videos do not spell out

* **DC2 readdress (stage 4).** After moving DC2 to 172.16.0.2: Preferred DNS 192.168.2.2 (DC1), Alternate
  127.0.0.1; then `ipconfig /registerdns` and `net stop netlogon && net start netlogon` so its A and SRV records
  update, and check DC1's zone no longer holds a stale 192.168.2.3 record for DC2.
* **Connection objects (8.3).** If DC2's NTDS Settings shows no connection from DC1 after the move to MG,
  right-click NTDS Settings > All Tasks > Check Replication Topology, refresh, then Replicate Now.
* **Schedule versus class hours (8.3).** The schedule blocks Mon to Fri 09:00 to 18:00, so scheduled inter-site
  replication will not happen during class. Replicate Now overrides the schedule; that is the test to use.
  CLI cross-check: `repadmin /replsummary` and `repadmin /showrepl DC2`.
* **Zone scope (8.4).** "All DNS servers running on domain controllers in this domain" is the default for the
  domain zone of a new forest; confirm it rather than change it, and do not pick the forest option the video picks.
* **DFS initial sync (8.5).** SB-DNS-1 `C:\Share1` is the primary (authoritative) member. Anything already in
  SB-FS2 `C:\Share2` is moved aside to `DfsrPrivate\PreExisting`, so start with it empty. Initial replication can
  take several minutes; `dfsrdiag pollad` on both members speeds it up; DFSR event 4104 on SB-FS2 confirms it.
* **Share versus NTFS (8.5).** Everyone needs Change/Full on the share **and** Modify on NTFS, or writes fail.
* **FSRM retests (8.6).** Event-log notifications are rate limited (60 minutes by default per notification).
  If a retest logs nothing, lower the interval in FSRM Options > Notification Limits, or wait.
* **Quota test (8.6).** 85% of 100 KB is 85 KB; copy a file of roughly 90 to 200 KB into `C:\share4`.
  File screens apply to Administrators too, so `test.txt` should be blocked whoever copies it.

## Evidence checklist (screenshots into `02_student_work/screenshots/`)

8.1
- [ ] DC1: name, domain, AD DS and DNS roles (Server Manager > Local Server and the roles tiles)
- [ ] DC2: same, same domain

8.2
- [ ] Sites SB and MG
- [ ] Subnets 192.168.1.0/26, 192.168.1.64/26, 192.168.2.0/28 to SB; 172.16.0.0/24 to MG
- [ ] DC1 under SB > Servers; DC2 under MG > Servers

8.3
- [ ] DEFAULTIPSITELINK: 180 minutes, schedule with Mon to Fri 09:00 to 18:00 unavailable
- [ ] Admin, Server, global_computers on DC1
- [ ] Replicate Now confirmation
- [ ] Same objects on DC2 (172.16.0.2 visible)

8.4
- [ ] DC1 zone: Primary, AD-integrated, replication scope "this domain"
- [ ] SOA refresh 30 minutes
- [ ] DC1 Name Servers tab listing SB-DNS-2; Zone Transfers "only to servers on the Name Servers tab"
- [ ] SB-DNS-2 secondary zone properties: Secondary, master 192.168.2.2
- [ ] SB-DNS-2 zone populated after Transfer from Master

8.5
- [ ] DFS roles installed on SB-DNS-1 and SB-FS2
- [ ] Namespace `\\<domain>\Shares` with targets `\\SB-DNS-1\Share1` and `\\SB-FS2\Share2`
- [ ] Rep1 (<domain>) Memberships: C:\Share1 SB-DNS-1 Share1; C:\Share2 SB-FS2 Share1
- [ ] Test file (Doc1.txt) present on both members

8.6
- [ ] QT-1: 100 KB, Soft, 85% event-log warning
- [ ] Quota on C:\share4 from QT-1
- [ ] Event 12325, SRMSVC, Warning: 85% threshold on C:\share4 on SB-FS2
- [ ] FG-1 file group: include `*.txt`, exclude `hello.txt`
- [ ] FG-1 file screen template (active) and file screen on C:\share4
- [ ] test.txt blocked; hello.txt saved
- [ ] Event 8215, SRMSVC, Warning: C:\share4\test.txt in FG-1
- [ ] Quota Usage report (DHTML): SB-FS2, C:\share4, usage figures
