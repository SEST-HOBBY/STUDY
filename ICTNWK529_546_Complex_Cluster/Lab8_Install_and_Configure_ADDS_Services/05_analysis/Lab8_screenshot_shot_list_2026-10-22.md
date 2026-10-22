# Lab 8 screenshot shot list (from the AT1 template, read 2026-10-22)

Source: `00_assessment_documents/ICTNWK529_ICTNWK546_AT1 WORKING ON.docx`, the portfolio template with the
teacher's demonstration screenshots under each sub-lab instruction. The demonstration images are extracted to
`04_extracted_views/AT1_template_Lab8_teacher_examples/` so you can see what each of yours should look like.
They are the teacher's (domain `Maggie.Zhong`, one from another student, `sungho.hong`) and the template says
in red to remove them before submission: they are a model, never a submission.

The screenshots themselves can only come from your own VMs and devices: an assessor accepts them as evidence
that you did the work, so they cannot be drawn or generated. This list tells you exactly what to capture, how
to compose it, and what to name it, so that nothing is missed and nothing needs re-doing.

Composition rules the template repeats for every sub-lab:

* **The domain name must be visible** ("displays the domain name on the background"): keep Server Manager >
  Local Server behind the window you are capturing (it shows Computer name and Domain), or make sure the
  domain appears in the window title, tree or a column.
* Capture the whole window(s) with title bars, not a cropped detail; the teacher's examples are full-screen
  captures (Windows key + Shift + S, then Fullscreen, or PrtScn).
* Replace every `<domain>` below with your real domain (`student1.student2`), and the computer names are
  exactly DC1, DC2, SB-DNS-2, SB-FS2 (the teacher's example in 8.4 shows `sb-dns-1` as the secondary; the
  written brief and our plan use SB-DNS-2 at 192.168.2.4; the first DFS server is SB-DNS-1).
* Save as PNG into `02_student_work/screenshots/` with the names given, then paste into the template under
  the matching instruction and delete the teacher's example and the red text.

Teacher demonstration screenshots are labelled "demo" below.

---

## 8.1 Install domain controllers on sites (demo: `8.1_teacher_ADUC_domain_controllers.jpeg`)

Template text: "Paste screenshots of the two load sharing domain controllers. You should name the controllers
after the format ... dc1.student1firstname.student2firstname, dc2.student1firstname.student2firstname."

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-01-ADUC-two-DCs.png` | DC1: Server Manager > Tools > Active Directory Users and Computers > expand the domain > click **Domain Controllers** | Left tree with `<domain>` expanded; right pane listing **DC1** and **DC2**, Type Computer, DC Type **GC**, Site column (Default-First-Site-Name before 8.2, SB / MG after) |
| 2 | `Lab8-01-DC1-LocalServer.png` | DC1: Server Manager > Local Server | Computer name DC1, Domain `<domain>`, and the AD DS and DNS roles in the left pane |
| 3 | `Lab8-01-DC2-LocalServer.png` | DC2: same | Computer name DC2, Domain `<domain>` |
| 4 (optional, strong) | `Lab8-01-repadmin.png` | DC1 PowerShell: `repadmin /replsummary` | both DCs, 0 fails: proves the two DCs are live partners |

Written answers (red text in the template, write them in your own words, a paragraph each): what NTP is and
how the stratum hierarchy works (`w32tm /query /status` on DC1 gives you a real stratum number to quote);
what user authentication is; what Active Directory services are.

## 8.2 Create sites and subnets (demo: `8.2_teacher_AD_sites_and_services.png`)

Template: "take a screenshot at the end and paste it here ... similar to the one attached".

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-02-Sites-Subnets.png` | DC1: Tools > Active Directory Sites and Services; expand **Subnets**, **SB > Servers**, **MG > Servers**; click **SB > Servers** so the right pane shows DC1 with its **Domain** column | Subnets `192.168.2.0/28`, `192.168.1.0/26`, `192.168.1.64/26`, `172.16.0.0/24`; **DC1 under SB**, **DC2 under MG**; the Domain column showing `<domain>` (that is how the demo gets the domain name in) |

Tip: widen the right pane's Domain column before capturing. Written answer: how AD DS sites direct client
logon and directory requests to a DC in the client's own site (subnet to site mapping, DC locator, site
coverage), which spreads the load between SB and MG.

## 8.3 Configure DC replication between sites (demo: `8.3_teacher_site_link_replication.png`)

Template: "a screenshot ... which demonstrates the subnets, sites, DCs, replication between SB & MG, and the
domain name on the background."

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-03-SiteLink.png` | DC1: Server Manager > Local Server **behind**; in front, AD Sites and Services with **Inter-Site Transports > IP** selected; tree expanded to show Subnets, SB > Servers > DC1, MG > Servers > DC2 > NTDS Settings | Right pane: **DEFAULTIPSITELINK**, Type Site Link, **Description "Replication between SB & MG"**, Cost 100, **Replication Interval 180**; Server Manager behind showing Computer name DC1 and Domain `<domain>` |
| 2 | `Lab8-03-Schedule.png` | DEFAULTIPSITELINK > Properties > **Change Schedule** | Mon to Fri 09:00 to 18:00 blocked (Replication Not Available), the rest available |
| 3 | `Lab8-03-Objects-DC2.png` | DC2: Active Directory Users and Computers | OUs **Admin** and **Server**, and inside Server the group **global_computers** (Global, Security), seen on DC2 after Replicate Now; Local Server behind showing DC2 and the domain |
| 4 (optional) | `Lab8-03-ReplicateNow.png` | AD Sites and Services > MG > DC2 > NTDS Settings > right-click the connection > Replicate Now | the confirmation dialog |

The demo's Description text "Replication between SB & MG" is typed by hand in DEFAULTIPSITELINK > Properties >
Description; do the same, it is what makes the screenshot "demonstrate replication between SB & MG".

## 8.4 DNS replication, AD-integrated zone, secondary server (demo: `8.4a`, `8.4b`, `8.4c`)

Template: "Take screenshots similar to the following which displays the domain name on the background", plus
"Screenshot of demonstrating that SB-DNS is successfully synchronized to DC1 needs to be presented as well."

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-04-Zone-General.png` | DC1: Tools > DNS > DC1 > Forward Lookup Zones > `<domain>` > Properties > **General** tab | Type: **Active Directory-Integrated**, **Primary**; Replication: **To all DNS servers running on domain controllers in this domain** (the written brief's wording; the video chose the forest option, do not) |
| 2 | `Lab8-04-SOA-30min.png` | same Properties > **Start of Authority (SOA)** tab | **Refresh interval 30 minutes**; Primary server dc1.`<domain>` |
| 3 | `Lab8-04-NameServers.png` | same Properties > **Name Servers** tab | dc1.`<domain>` [192.168.2.2], dc2.`<domain>` [172.16.0.2], **sb-dns-2.`<domain>` [192.168.2.4]** (demo 8.4b) |
| 4 | `Lab8-04-ZoneTransfers.png` | same Properties > **Zone Transfers** tab | **Allow zone transfers** ticked, **Only to servers listed on the Name Servers tab** selected (demo 8.4a); DNS Manager tree behind showing DC1 and the zones |
| 5 | `Lab8-04-SBDNS2-Secondary-Populated.png` | On SB-DNS-2 (or DC1's DNS Manager with **Connect to DNS Server** > SB-DNS-2 added, as in demo 8.4c): SB-DNS-2 > Forward Lookup Zones > `<domain>` after **Transfer from Master** | The zone **populated**: SOA, the NS records (dc1, dc2, sb-dns-2), the A records for dc1 192.168.2.2, dc2 172.16.0.2, sb-dns-2 192.168.2.4, and the `_msdcs`, `_sites`, `_tcp`, `_udp` folders. This is the "successfully synchronized to DC1" proof |
| 6 | `Lab8-04-SBDNS2-Zone-Properties.png` | SB-DNS-2 > zone > Properties > General | Type **Secondary**; Master server 192.168.2.2 |

Composition for 5: do it from DC1's DNS Manager with both servers in the tree (demo 8.4c) so DC1's primary zone
and SB-DNS-2's secondary zone are side by side in one picture.

## 8.5 DFS (demo: `8.5_teacher_DFS_Rep1_memberships.png`)

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-05-DFS-Rep1-Memberships.png` | SB-DNS-1: Server Manager > Tools > **DFS Management**; tree: Namespaces > `\\<domain>\Shares` expanded with the two folder targets; Replication > **Rep1** selected, **Memberships** tab | Title **Rep1 (`<domain>`)**; Replicated Folder: Share1 (2 items): `C:\Share1` Enabled **SB-DNS-1** Share1; `C:\Share2` Enabled **SB-FS2** Share1; staging quota 4.00 GB; namespace tree showing `\\<domain>\Shares` with **SB-DNS-1 Share1** and **SB-FS2 Share2** |
| 2 | `Lab8-05-DFS-Namespace.png` | same console, click `\\<domain>\Shares` | the Namespace tab with the folder targets `\\SB-DNS-1\Share1` and `\\SB-FS2\Share2` |
| 3 (optional, strong) | `Lab8-05-Doc1-replicated.png` | File Explorer on SB-FS2 showing `C:\Share2\Doc1.txt` next to File Explorer on SB-DNS-1 showing `C:\Share1\Doc1.txt` | functional proof the file replicated |

## 8.6 FSRM (demo: `8.6a_teacher_event_12325_quota.png`, `8.6b_teacher_event_8215_file_screen.png`)

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-06-Event-12325-Quota.png` | SB-FS2: Event Viewer > Windows Logs > Application > double-click the **SRMSVC 12325** event; Server Manager > Local Server behind | Text: "User `<NETBIOS>`\\Administrator has exceeded the **85%** quota threshold for the quota on **C:\share4** on server **SB-FS2**. The quota limit is 0.10 MB ..."; Level Warning; Computer **SB-FS2.`<domain>`** |
| 2 | `Lab8-06-Event-8215-FileScreen.png` | same log, the **SRMSVC 8215** event | "attempted to save **C:\share4\test.txt** to C:\share4 on the SB-FS2 server. This file is in the **"FG-1"** file group, which is not permitted"; Computer SB-FS2.`<domain>` |
| 3 | `Lab8-06-QT1-Template.png` | File Server Resource Manager > Quota Management > Quota Templates | **QT-1**, 100 KB, **Soft**, with the 85% Event Log notification |
| 4 | `Lab8-06-FG1-FileGroup.png` | File Screening Management > File Groups > FG-1 Properties | include `*.txt`, exclude `hello.txt` |
| 5 | `Lab8-06-FileScreen-share4.png` | File Screening Management > File Screens | `C:\share4`, Active, FG-1 |
| 6 | `Lab8-06-hello-allowed-test-blocked.png` | File Explorer on `C:\share4` with `hello.txt` present, and the "file is not allowed" error dialog from copying `test.txt` | the two outcomes side by side |
| 7 | `Lab8-06-QuotaUsage-Report.png` | Storage Reports Management > Generate Reports Now > Quota Usage (DHTML) on C:\share4 | the browser report heading **Quota Usage Report**, Machine SB-FS2, folder C:\share4, usage figures |

## 8.7 Desktop management via GPO (no demo image)

Template: "Take screenshot at the end of the lab which displays the domain name on the background."

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-07-GPO-Wallpaper-Setting.png` | DC1: Group Policy Management Editor for **Deploy Desktop Background GPO** > User Configuration > Policies > Administrative Templates > Desktop > Desktop > **Desktop Wallpaper** = Enabled, Wallpaper Name `\\DC1\Shared_Wallpaper$\background.jpg`, Style Fill/Stretch; and **Prevent changing desktop background** = Enabled (Control Panel > Personalization) | the GPO name with `[DC1.<domain>]` in the editor title, both settings Enabled |
| 2 | `Lab8-07-GPO-Linked.png` | Group Policy Management > `<domain>` (or the OU) | the GPO linked, Link Enabled |
| 3 | `Lab8-07-Client-Wallpaper-gpresult.png` | The test machine (CS-PC-1, or the DNS server as the later step says; ask the teacher which, do both if you can): the desktop showing the wallpaper, with a command prompt `gpresult /r` on top | "Applied Group Policy Objects: Deploy Desktop Background GPO" under User Settings, and the domain in the gpresult header; the wallpaper visible behind |

## 8.8 Anti-virus deployment via GPO (demo: `8.8a`, `8.8b`)

What the demo reveals (this fills most of the unknowns recorded in the report for WP10):

* Product: **Avast** (the free "Avast MicroInstaller"), repackaged as an **MSI with "MSI Wrapper" from
  www.exemsi.com** (Group Policy software installation can only deploy .msi, so the .exe is wrapped).
* Share: `\\DC1.<domain>\Shared Software\...` on DC1.
* GPO: named **Anti-Virus-End-Devices**, Computer Configuration > Policies > Software Settings > **Software
  installation** > the package **Assigned** (so it installs at computer start-up, before logon).
* Client evidence: the boot screen "Installing managed software Avast MicroInstaller - UNREGISTERED - Wrapped
  using MSI Wrapper from www.exemsi.com..." on the client.

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-08-GPO-Software-Installation.png` | DC1: Group Policy Management Editor for the AV GPO > Computer Configuration > Policies > Software Settings > Software installation | the package name, version, **Deployment state Assigned**, **Source `\\DC1.<domain>\Shared Software\...msi`**; editor title `Anti-Virus-End-Devices [DC1.<domain>]` |
| 2 | `Lab8-08-Client-Installing.png` | the client (CS-PC-1) during start-up after `gpupdate /force` and restart | "Installing managed software <package>..." |
| 3 | `Lab8-08-Client-Installed.png` | the client after logon: Control Panel > Programs, or the AV icon in the tray | the AV present; domain visible (e.g. `whoami` in a command prompt, or System > Domain) |

Still to confirm with the teacher: whether Avast is still the expected product (or any free AV the teacher
accepts), where the installer comes from (the lab has no internet route; download it on a TAFE-connected PC
and copy to DC1), and which OU the GPO is linked to (the client must be in it).

## 8.9 WSUS and Windows Update via GPO (demo: `8.9a`, `8.9b`)

What the demo reveals (fills most of WP11's unknowns):

* WSUS was installed on **SB-FS2** (any member server will do; the console title is "Update Services" > SB-FS2).
* The template also wants: IIS role installed on the WSUS server; a successful synchronisation with Microsoft;
  selected updates downloaded; approvals.
* The Windows Update GPO (demo 8.9b) is a GPO named "Windows Update" linked at the domain, Computer
  Configuration > Policies > Administrative Templates > Windows Components > **Windows Update**, with these
  **Enabled**: Configure Automatic Updates; Specify intranet Microsoft update service location (both URLs
  `http://sb-fs2.<domain>:8530`); Automatic Updates detection frequency; Allow Automatic Updates immediate
  installation; Turn on recommended updates via Automatic Updates; No auto-restart with logged on users for
  scheduled automatic updates installations. Everything else Not configured.

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-09-IIS-WSUS-Roles.png` | SB-FS2: Server Manager > Local Server (roles pane) or Dashboard | **IIS** and **WSUS** roles installed; Domain `<domain>` |
| 2 | `Lab8-09-WSUS-Sync-Success.png` | Update Services > SB-FS2 > **Synchronizations** | a synchronisation with Result **Succeeded** |
| 3 | `Lab8-09-WSUS-Updates-Downloaded.png` | Update Services > Updates > All Updates (or the Approval Progress dialog as in demo 8.9a) | updates listed / "Approval completed without errors" with Success rows |
| 4 | `Lab8-09-GPO-WindowsUpdate.png` | DC1: Group Policy Management with the **Windows Update** GPO visible in the tree, and its editor open at Windows Components > Windows Update | the Enabled settings listed above; Forest/Domains `<domain>` in the tree (demo 8.9b) |
| 5 (optional) | `Lab8-09-Client-WSUS.png` | client: Update Services > Computers > All Computers | the client reporting to WSUS |

Practical point before this lab: WSUS synchronisation needs internet access from SB-FS2, and the lab network
has no route out. Give the SB-FS2 VM a second network adapter on VMware **NAT** (host internet) for the
synchronisation, or sync while temporarily bridged to the TAFE network, then remove it. Choose products
Windows Server 2019 (and Windows 10 if the client is Windows 10), classifications Critical and Security
updates, and let the first sync run (it can take an hour or more). Written answer: what a web application is
(WSUS itself is one: an IIS-hosted application the clients and console talk to over HTTP on port 8530).

## 8.10 Join Ubuntu to the AD domain (demo: `8.10_teacher_ubuntu_realm_list.png`)

What the demo reveals: the join uses **realmd with SSSD** (`realm list` shows type kerberos, configured
kerberos-member, server-software active-directory, client-software sssd, required packages sssd-tools, sssd,
libnss-sss, libpam-sss, adcli, samba-common-bin, login-formats %U@domain).

| # | File | Where | What must be visible |
|---|---|---|---|
| 1 | `Lab8-10-Ubuntu-realm-list.png` | Ubuntu terminal: `realm list` | `<domain>` as the realm with the lines above (demo 8.10) |
| 2 | `Lab8-10-Ubuntu-realm-discover-join.png` | terminal: `realm discover <domain>` then `sudo realm join -U Administrator <domain>` | the discovery output and the join without error |
| 3 (optional, strong) | `Lab8-10-Ubuntu-AD-user.png` | terminal: `id administrator@<domain>` or `getent passwd administrator@<domain>`, and ADUC on DC1 > Computers showing the Ubuntu computer object | the AD user resolved on Ubuntu; the Linux machine as a domain member |

Prerequisites on the Ubuntu VM: its DNS must be DC1 (192.168.2.2), so put it on the SB computer bridged like
DC1 with a static address such as 192.168.2.7/28, gateway 192.168.2.1; `sudo apt install realmd sssd
sssd-tools libnss-sss libpam-sss adcli samba-common-bin packagekit` needs internet (NAT adapter temporarily,
or a TAFE-connected host), and the clock must be within 5 minutes of DC1. The Ubuntu 18.04.5 VM found on the
E: drive is a candidate; copy its whole folder (it has a snapshot chain).

---

## Portfolio housekeeping

* File name for submission (template, first page): `Firstname_Lastname_AT1_Attempt_1` (the template calls
  itself AT1 while the labs say "AT4 Part 2"; register item 7, keep the supplied name until the teacher
  confirms).
* Remove every red instruction line and every teacher example image before submitting.
* Written answers required inside the Lab 8 section: NTP and stratum; user authentication; Active Directory
  services; how AD DS sites share client requests between DCs; what a web application is.
