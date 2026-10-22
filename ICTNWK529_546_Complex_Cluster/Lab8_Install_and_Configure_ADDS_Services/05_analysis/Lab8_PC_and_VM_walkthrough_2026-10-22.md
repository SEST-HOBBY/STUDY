# Lab 8 walkthrough, part 2: the two computers and the DC1 / DC2 virtual machines (2026-10-22)

Read top to bottom; each step says what you click, what you should see, and what to screenshot. Nothing here
touches the Cisco side once the network checks in the config file have passed.

What you are building:

| | SB computer (your PC) | MG computer (the independent PC) |
|---|---|---|
| Lab cable | green, add-in NIC -> SB-S1 Gi0/1 (VLAN 90) | yellow -> MG-S1 Fa0/1 |
| Other NIC | onboard, yellow, TAFE network: stays | none on the lab |
| VM | **DC1** 192.168.2.2 /28, gateway 192.168.2.1, DNS itself | **DC2** 172.16.0.2 /24, gateway 172.16.0.1, DNS 192.168.2.2 |
| Role | first domain controller, new forest `<student1>.<student2>` | second domain controller in that domain |

The domain name is your two first names as the brief says (`student1firstname.student2firstname`). The 2025 VM
was called `DC2.Eric.Roly`, which suggests `Eric.Roly`; confirm the order with Eric and the teacher before step
E, because it cannot be changed afterwards without rebuilding. Windows media: the Server 2019 Datacenter ISO at
`E:\OS ISO Files\Windows Server 2019\en_windows_server_2019_updated_sept_2019_x64_dvd_199664ce.iso`. If the
teacher insists on 2012 R2 you need that ISO instead; every step below is the same apart from the edition
screen.

---

## A. Prove the computer is on the lab network (5 minutes, no VM)

Do this on the SB computer first, then the same on the MG computer with the MG values.

1. Identify the lab adapter. Settings > Network & Internet > Ethernet (or Control Panel > Network and Sharing
   Center > Change adapter settings). You will see two Ethernet adapters on your PC: the onboard one says
   "student.tafe" or similar; the add-in one says **"Unidentified network"** or "Network cable unplugged" if
   the switch port is down. Right-click the add-in one > Rename > call it **LAB**. (Write down its driver name
   too: right-click > Properties, the "Connect using" line, for example "Realtek PCIe GbE Family Controller #2".
   VMware shows the same name later.)
2. Give LAB a temporary address: right-click LAB > Properties > Internet Protocol Version 4 > Properties >
   Use the following IP address: `192.168.2.13`, mask `255.255.255.240`, gateway `192.168.2.1`, preferred DNS
   `192.168.2.1`. OK, OK.
3. Command prompt: `ping 192.168.2.1` (SB router) then `ping 172.16.0.1` (MG router, across the three routers).
   Four replies each = the cable, the switch port, the VLAN and the routing all work. Screenshot it (evidence).
   No reply from 192.168.2.1: the switch port LED, `show interfaces status` on SB-S1 (Gi0/1 must be
   `connected` in vlan 90) and the SB sub-interface are the three things to look at. Reply from .1 but not
   from 172.16.0.1: OSPF; go back to the router checks.
4. MG computer: same with `172.16.0.253`, mask `255.255.255.0`, gateway `172.16.0.1`; ping `172.16.0.1` then
   `192.168.2.1`.
5. Afterwards set LAB back to **Obtain an IP address automatically** on both computers. The VM will own the
   lab address, not the host. (It will then show "Unidentified network" with a 169.254.x address; that is
   correct and does not matter for bridging.)

## B. Tell VMware which NIC to bridge (your PC only; the MG PC has one NIC and needs nothing)

Your PC has two live NICs. VMware's default "Automatic" bridging may choose the TAFE one and put DC1 on the
campus network, so pin it:

1. Workstation > **Edit > Virtual Network Editor**. Click **Change Settings** at the bottom (Windows asks for
   administrator approval).
2. In the list select **VMnet0** (Type: Bridged). Below, "Bridged to:" is a drop-down showing "Automatic":
   open it and pick the **add-in adapter by its driver name** (the one you noted in A.1).
3. Apply, OK.

If Change Settings is refused (no administrator rights on this PC): leave Automatic, and **unplug the yellow
TAFE lead from your PC whenever DC1 is running**; with one connected NIC, Automatic picks it. Do not run both
cables with Automatic.

On the MG computer: if it has Workstation, the same dialog is optional (one NIC); if it only has Player there
is no editor and Automatic is correct.

## C. Where the VM files go

Make a folder that is **not inside OneDrive** and, if the PC has an internal data drive, on that drive:
`D:\Lab8-VMs\` (fast) or `E:\Lab8-VMs\` on the USB SSD (works, slower). One sub-folder per VM. If you use the
internal drive of a lab PC, copy the VM folder to `E:\Lab8-VMs\` at the end of every session; lab PCs get
re-imaged.

Memory check: Task Manager > Performance > Memory shows the total. DC1 wants 4 GB; the Networking VM (console)
wants 8 GB. On a 16 GB PC close the Networking VM before powering on DC1. On a 32 GB or 64 GB PC both run.

## D. Create the DC1 virtual machine (shell only; Windows is installed in E)

Workstation Home > **Create a New Virtual Machine**:

1. **Typical** > Next.
2. **I will install the operating system later** > Next. (Do NOT pick "Installer disc image file" here: that
   triggers Easy Install, which creates an account named after you with no password and applies its own
   product key. A domain controller wants the built-in Administrator with a password you set.)
3. Guest operating system **Microsoft Windows**, Version **Windows Server 2019** > Next.
4. Virtual machine name `DC1`; Location `D:\Lab8-VMs\DC1` (Browse, make the folder) > Next.
5. Maximum disk size **60** GB; **Store virtual disk as a single file** > Next.
6. Click **Customize Hardware**:
   * Memory: **4096** MB.
   * Processors: 2.
   * New CD/DVD (SATA): **Use ISO image file** > Browse to the Server 2019 ISO; tick **Connect at power on**.
   * Network Adapter: **Bridged** (not NAT, not Host-only); tick Connect at power on.
   * Close.
7. Untick "Power on this virtual machine after creation" if it is shown; Finish.
8. With DC1 selected: **VM > Snapshot > Take Snapshot**, name `0-empty`. (Snapshots are safe until the VM
   becomes a domain controller; after promotion never revert one.)

Same on the MG computer with the name `DC2`.

## E. Install Windows Server in DC1 (about 20 minutes)

1. **Power on this virtual machine**. Click inside the window and press a key immediately when it says
   "Press any key to boot from CD or DVD". If you miss it and get "EFI Network" or a boot failure: VM > Power >
   Restart Guest and press a key sooner.
2. Windows Setup: language English, time and currency **English (Australia)**, keyboard US > Next > **Install
   now**.
3. Select the operating system: **Windows Server 2019 Datacenter (Desktop Experience)**. Not "Datacenter"
   alone, which is Server Core with no desktop. (If the teacher mandates 2012 R2: "Windows Server 2012 R2
   Standard (Server with a GUI)".) Next.
4. Accept the licence > **Custom: Install Windows only (advanced)** > Drive 0 Unallocated Space > Next.
5. Wait. Setup reboots two or three times by itself; do not press keys at the "Press any key" prompt during
   those reboots or it boots the CD again.
6. At **Customize settings**, type the built-in **Administrator** password twice. Write it down privately: on
   DC1 this becomes the domain Administrator password.
7. Press Ctrl+Alt+Del: in VMware use **VM > Send Ctrl+Alt+Del** (or Ctrl+Alt+Insert). Log in as
   Administrator. Server Manager opens by itself.
8. **VM > Install VMware Tools** > inside Windows a D: drive appears; if setup does not start, open This PC >
   DVD Drive > setup64.exe > Typical > Install > Finish > Yes to restart. (Proper mouse, screen size and clock
   sync.) After the restart, **VM > Snapshot > Take Snapshot** `1-windows-installed`.
9. Take the VMware CD out of the picture: VM > Settings > CD/DVD > untick Connect at power on (otherwise every
   boot offers to start Setup again).

Same on the MG computer for DC2.

## F. Name, address and time (both VMs)

In Server Manager > **Local Server** (left pane):

1. Click the computer name (WIN-XXXXXXXX) > Change > Computer name **DC1** > OK > OK > Close > **Restart Now**.
   (DC2 on the other PC.)
2. After the restart, click the **Ethernet0** value ("IPv4 address assigned by DHCP") > right-click Ethernet0 >
   Properties > Internet Protocol Version 4 > Properties > Use the following IP address:

   | | DC1 | DC2 |
   |---|---|---|
   | IP address | 192.168.2.2 | 172.16.0.2 |
   | Subnet mask | 255.255.255.240 | 255.255.255.0 |
   | Default gateway | 192.168.2.1 | 172.16.0.1 |
   | Preferred DNS | 192.168.2.2 | 192.168.2.2 |
   | Alternate DNS | 127.0.0.1 | (leave empty until DC2 is promoted, then 127.0.0.1) |

   OK, Close. Windows may ask "Do you want to allow your PC to be discoverable": Yes.
3. Time zone: click the Time zone value > Change time zone > **(UTC+10:00) Brisbane** > OK. Check the clock
   matches the host.
4. Allow ping (an unpromoted server ignores it): right-click Start > **Windows PowerShell (Admin)** and run
   `Enable-NetFirewallRule -DisplayName "File and Printer Sharing (Echo Request - ICMPv4-In)"`
5. Tests, in that PowerShell window:
   * DC1: `ping 192.168.2.1`, `ping 172.16.0.1`, `ping 172.16.0.2` (once DC2 has its address).
   * DC2: `ping 172.16.0.1`, `ping 192.168.2.1`, `ping 192.168.2.2`.
   * From DC1: `tracert -d 172.16.0.2` -> 192.168.2.1, 209.165.200.2, 209.165.200.18, 172.16.0.2.
   Screenshot the ping results on both (evidence: the two hosts reach each other across the sites).
6. Optional but tidy: Local Server > **IE Enhanced Security Configuration** > Off for Administrators; it stops
   the browser nagging later.
7. **Snapshot** `2-named-addressed` on both. This is the last snapshot you will take on DC1.

Stop here if the teacher has not yet answered on the OS: everything above is reusable whatever the answer.

## G. Work Package 1: promote DC1 (new forest)

On DC1, Server Manager > **Manage > Add Roles and Features**:

1. Before you begin > Next. **Role-based or feature-based installation** > Next. Select DC1 (the only server)
   > Next.
2. Server Roles: tick **Active Directory Domain Services** > a pop-up lists the management tools > **Add
   Features** > Next. Features > Next. AD DS > Next. Confirmation > tick "Restart the destination server
   automatically if required" > Yes > **Install**. Wait for "Configuration required. Installation succeeded".
3. In the same window (or the yellow flag at the top of Server Manager) click **Promote this server to a
   domain controller**.
4. Deployment Configuration: **Add a new forest**, Root domain name: `<student1>.<student2>` (your two first
   names, all lower case is fine) > Next.
5. Domain Controller Options: Forest functional level and Domain functional level: on Server 2019 the list
   offers 2008 to **Windows Server 2016** and defaults to 2016; there is no 2019 entry and no 2012 R2 entry
   above it is needed. Leave 2016 (the video's "2012 R2" was on 2012 R2 media; note it as register item 8 in
   the portfolio). Tick **Domain Name System (DNS) server** (ticked) and **Global Catalog** (ticked, greyed).
   Leave Read-only DC unticked. Type the **DSRM password** twice and record it privately > Next.
6. DNS Options: the warning "A delegation for this DNS server cannot be created" is expected (no parent zone
   exists) > Next.
7. Additional Options: NetBIOS name is filled in from the domain (for example ERIC) > Next.
8. Paths > Next. Review Options > Next. Prerequisites Check: warnings about cryptography and the DNS
   delegation are normal; a red error is not: read it and stop > **Install**.
9. DC1 restarts by itself. Log in as `<NETBIOS>\Administrator` (same password as before; the local
   Administrator became the domain Administrator).

Verify and screenshot (these are the Lab 8.1 evidence for DC1):

* Server Manager > Local Server: Computer name DC1, Domain `<student1>.<student2>`; Roles tile shows AD DS and DNS.
* Tools > **Active Directory Users and Computers** > expand the domain > **Domain Controllers** contains DC1.
* Tools > **DNS** > DC1 > Forward Lookup Zones: `_msdcs.<domain>` and `<domain>`; inside `<domain>` the A
  record for dc1 at 192.168.2.2 and the `_tcp` / `_udp` folders.
* PowerShell: `dcdiag /q` (prints nothing when all tests pass) and `nslookup dc1.<domain>` (answers 192.168.2.2).

Do not take or revert snapshots of DC1 from now on.

## H. Work Package 2: join and promote DC2 (additional DC)

On DC2, first the rule from the video: it must resolve DC1 before anything else.

1. PowerShell (Admin): `nslookup dc1.<domain>` -> 192.168.2.2; `nslookup <domain>` -> 192.168.2.2;
   `Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.<domain>` -> dc1.<domain>. Screenshot. If these fail,
   DC2's Preferred DNS is not 192.168.2.2 or the network test in F.5 did not pass; fix that first.
2. Join: Server Manager > Local Server > click the Workgroup value > Change > Member of **Domain**:
   `<student1>.<student2>` > OK > credentials `<NETBIOS>\Administrator` and the password > "Welcome to the
   domain" > OK > Restart Now.
3. Log in as `<NETBIOS>\Administrator` (choose "Other user" if the login screen shows the local account).
4. Manage > Add Roles and Features > Active Directory Domain Services (as in G.1 and G.2) > Install.
5. **Promote this server to a domain controller** > Deployment Configuration: **Add a domain controller to an
   existing domain**; Domain: `<student1>.<student2>` (Select... if it does not fill in); Credentials: Change >
   `<NETBIOS>\Administrator` > Next.
6. Domain Controller Options: DNS server ticked, Global Catalog ticked, RODC unticked; Site name:
   **Default-First-Site-Name** (the SB and MG sites are made in Lab 8.2 and DC2 is moved then); DSRM password
   (record it) > Next.
7. DNS Options > Next (delegation warning expected). Additional Options: Replicate from **Any domain
   controller** > Next. Paths > Next. Review > Next. Prerequisites > Install. DC2 restarts.
8. Log in as `<NETBIOS>\Administrator`. Then set DC2's DNS: Ethernet0 > IPv4 > Preferred `172.16.0.2`,
   Alternate `192.168.2.2`. (Each DC uses itself first and the other DC as backup.)

Verify and screenshot (Lab 8.1 evidence for DC2 and "two load-sharing DCs"):

* On DC2: Local Server shows Domain `<domain>`, roles AD DS and DNS.
* On DC1: Active Directory Users and Computers > Domain Controllers shows **DC1 and DC2**. This is the
  screenshot the brief asks for (two DCs with the student-specific names and the domain visible).
* On either: PowerShell `repadmin /replsummary` (both DCs listed, 0 fails) and `repadmin /showrepl`.
* On DC2: Tools > DNS > DC2 > Forward Lookup Zones shows the same two zones (the AD-integrated zone replicated).
* AD Sites and Services (Tools) shows both servers under Default-First-Site-Name: the starting point for Lab 8.2.

## I. Housekeeping at the end of every session

* Shut the VMs down from inside Windows (Start > Power > Shut down), never with VMware's Power Off button,
  especially the DCs.
* Copy `D:\Lab8-VMs\` to `E:\Lab8-VMs\` if the VMs live on a lab PC's internal drive.
* Put the screenshots in `02_student_work/screenshots/` with the names from the README
  (`Lab8-01A-DC1-Promoted.png`, `Lab8-01B-DC2-Promoted.png`, ...).
* The written answers for Lab 8.1 (NTP, stratum hierarchy, user authentication, AD DS) can be drafted any
  time; `w32tm /query /status` on DC1 and DC2 gives you real stratum numbers to quote.
