# Lab 10, 11 and 12 preparation runbook

What to have ready, the order to do things in, what to screenshot, and how to diagnose the problems these
three labs usually throw up. The teacher's tutorial video is the authority for each lab: where the video
differs from this runbook (product, version, addresses), follow the video.

Contents: [Before the labs](#1-before-the-labs) · [Lab 10 Security Onion](#2-lab-10-security-onion) ·
[Lab 11 FTP server](#3-lab-11-ftp-server) · [Lab 12 email server](#4-lab-12-email-server) ·
[Troubleshooting toolkit](#5-troubleshooting-toolkit) · [Mark-off questions](#6-questions-i-should-be-able-to-answer-at-mark-off)

---

## 1. Before the labs

### 1.1 Things to find out from the videos first

| Question | Why it matters | Answer |
|---|---|---|
| Which Security Onion version and install type does the video use (Import, Eval, Standalone)? | Decides the VM size and the setup wizard answers | |
| Which hypervisor (VMware Workstation, VirtualBox, Hyper-V) and which virtual networks? | Decides how the management and monitor adapters are attached | |
| Which two screens are the demonstration screenshots in the Lab 10 template? | These are the two I must reproduce | |
| Which FTP server does the class use (FileZilla Server, IIS FTP, vsftpd)? | Section 3 has all three | |
| Which mail server does the class use (hMailServer, Exchange, other) and which client? | Section 4 is written around hMailServer with Thunderbird | |
| Is Lab 12 built on my existing AD DS domain? What is the domain name? | Mail domain, DNS records and the theory questions tie to it | |

### 1.2 Downloads and host checks (do these at home; the Security Onion ISO is very large)

* Hardware virtualisation (VT-x / AMD-V) enabled in the BIOS, and enough free RAM and disk for the Security Onion VM (sizes in 2.1).
* Security Onion ISO from the official download page, with the checksum verified.
* FTP server installer and an FTP client (FileZilla Client or WinSCP).
* Mail server installer and a mail client (Thunderbird).
* Wireshark on the client VM. It is the quickest way to prove what is or is not on the wire.

### 1.3 Address plan (fill in before starting; most lab faults are a wrong value in this table)

| Machine | Role | Adapter / virtual network | IP address / mask | Gateway | DNS |
|---|---|---|---|---|---|
| | Security Onion management | | | | |
| | Security Onion monitor (no IP) | | none | none | none |
| | Analyst / client PC | | | | |
| | Windows Server (DC, DNS) | | | | |
| | FTP server | | | | |
| | Mail server | | | | |

### 1.4 Evidence habits

* Screenshot the whole window so the hostname, the IP address or URL, and the clock are visible. A screenshot
  that could be anyone's is weak evidence.
* Save as `lab10_01_so-status.png`, `lab11_03_client-login.png` and so on, into
  `02_student_work/screenshots/`.
* Screenshot a fault before fixing it. Part 10.1 needs the symptom as well as the fix.

### 1.5 Troubleshooting log (keep this open during every lab; Part 10.1 is written from it)

| # | Time | What I was doing | Symptom (exact message) | Tool / command | What the output showed | Cause | Fix | Proof it worked |
|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |

---

## 2. Lab 10 Security Onion

### 2.1 What it is

Security Onion is a free Linux distribution for network security monitoring, threat hunting and log
management. One install brings together an intrusion detection engine (Suricata, which raises alerts from
rules), a network metadata engine (Zeek, which logs every connection, DNS query, HTTP request and so on), full
packet capture, the Elastic stack for storage and search, and the Security Onion Console (SOC), a web interface
with Alerts, Dashboards, Hunt, Cases, PCAP and Grid pages.

An Eval or Standalone install needs two network adapters (an Import install, which only analyses saved packet
captures, needs just the management one):

* **Management**: has an IP address. I browse to it and it reaches the internet for updates.
* **Monitor (sniffing)**: has no IP address and runs in promiscuous mode. It only listens to a copy of the
  traffic, like a switch SPAN port.

VM sizing. Security Onion 2.4 minimums from its hardware requirements page:

| Install type | CPU cores | RAM | Disk | Adapters |
|---|---|---|---|---|
| Import (load saved packet captures only) | 2 | 4 GB | 50 GB | 1 |
| Eval | 4 | 8 GB | 200 GB | 2 |
| Standalone | 4 | 24 GB | 200 GB | 2 |

Check the version in the video before downloading. In November 2026 the 2.4 line was at 2.4.211 and a newer 3.x
line exists; the commands below are the 2.4 ones.

### 2.2 Build order

1. Create the VM with the two adapters. Note which adapter is which (MAC address) before booting.
2. Put the monitor adapter on the network whose traffic I want to see, and allow promiscuous mode on it
   (VirtualBox: Adapter > Advanced > Promiscuous Mode > Allow All. VMware Workstation: the adapter sees its own
   virtual network; on a Linux host the user needs permission on `/dev/vmnetX`. Hyper-V: enable port mirroring).
3. Boot the ISO, install, reboot, log in. The setup wizard starts by itself.
4. Wizard answers (write each one in the address plan first): install type as in the video, accept the Elastic
   licence, hostname, **management** adapter, static IP / mask / gateway / DNS, **monitor** adapter (space bar
   to tick it), web admin email and password, access by IP or hostname, and the IP address or subnet of the
   analyst PC that is allowed to reach the web interface.
5. Wait. The install takes a long time and looks stalled in places. Leave it.
6. `sudo so-status` and wait until every service shows as running.
7. From the analyst PC browse to `https://<management-IP>` (the same name or address chosen in the wizard),
   accept the self-signed certificate warning and log in with the email and password from step 4.
8. Generate something to look at. On the Security Onion VM run `so-test`, which replays sample packet captures
   (it needs internet access). Or, from a machine whose traffic the monitor adapter can see, run
   `curl testmynids.org/uid/index.html`, which should raise the alert
   `GPL ATTACK_RESPONSE id check returned root`. A saved capture can be loaded with
   `sudo so-import-pcap /full/path/to/file.pcap`.
9. In SOC: open **Alerts**, drill into the alert, pivot to **PCAP** or **Hunt**, then look at **Dashboards**.

### 2.3 Screens worth capturing (take them all; pick the two that match the template)

1. The VM settings showing two adapters.
2. The setup summary screen before the install starts.
3. `sudo so-status` with all services running.
4. `ip a` showing the management address and the monitor adapter with no address.
5. The SOC login page with the address bar visible, then the SOC overview after login.
6. **Alerts** page with alerts listed.
7. One alert drilled down (rule name, source and destination IP, ports).
8. **Dashboards** page with data in the charts.
9. **Hunt** or **PCAP** view of the same event.
10. **Grid** page showing the node healthy.

### 2.4 Problems this lab usually produces

Each row is a likely Part 10.1 entry. Record the real output when it happens.

| Symptom | Check with | Usual cause | Fix |
|---|---|---|---|
| Setup stops with a network error, or cannot download updates | `ip a`, `ip route`, `ping <gateway>`, `ping 8.8.8.8`, `nslookup securityonion.net` | Wrong adapter picked as management; wrong static address, mask, gateway or DNS; adapter on a host-only network with no internet | Correct the adapter attachment or the address and re-run setup |
| Ping to an IP works but names fail | `nslookup`, `cat /etc/resolv.conf` | Wrong or missing DNS server | Set the right DNS server |
| Browser on the analyst PC times out on `https://<management-IP>` | `ping <management-IP>`, then `Test-NetConnection <management-IP> -Port 443` | Ping fails: the two machines are on different virtual networks or subnets. Ping works but port 443 fails: the analyst IP is not allowed through the Security Onion firewall | Put both on the same network, or allow the analyst address with `sudo so-firewall includehost analyst <analyst-IP>` on the Security Onion VM (in SOC the same setting is Administration > Configuration > firewall > hostgroups; the older `so-allow` command is retired in 2.4) |
| Page opens but redirects, or login fails | Compare the URL with the name or IP chosen in the wizard | Browsing by IP when the wizard was set to hostname, or the reverse | Use the same form as the wizard; add a hosts-file entry on the analyst PC if it is a hostname |
| SOC loads but shows errors, or pages are empty straight after install | `sudo so-status` | Services still starting, or the VM has too little RAM and containers keep restarting | Wait for all services; give the VM more RAM and cores |
| Everything is running but there are no alerts and no dashboard data | `sudo tcpdump -i <monitor-adapter> -c 20` while pinging between two other machines | No packets: the monitor adapter is on the wrong virtual network or promiscuous mode is off. Packets seen: nothing has triggered a rule yet | Fix the adapter attachment and promiscuous mode; generate test traffic (2.2 step 8) |
| Alerts exist but the page looks empty | Time picker at the top right of SOC; `timedatectl` | Time range too short, or the VM clock or time zone is wrong | Widen the time range; correct the clock (ties in with the NTP question) |
| Install fails late, or services stop after a while | `df -h`, `free -h` | Disk or memory exhausted | Enlarge the disk or RAM and reinstall |

Re-running setup after a wrong answer: log out and back in and the wizard offers to run again. If it does not,
run `sudo SecurityOnion/setup/so-setup iso`.

Reference snips `lab10_ref1` to `lab10_ref3` in `05_analysis/reference_snips/` show the test traffic and the
resulting `GPL ATTACK_RESPONSE id check returned root` alert as Suricata itself reports it. Security Onion could
not be run in the test container, so there is no reference picture of the SOC web pages: those come from the
tutorial video and the template.

---

## 3. Lab 11 FTP server

### 3.1 FileZilla Server on Windows (the usual "simple FTP server")

1. Make the folder to share, for example `C:\FTP`, and put a test file in it.
2. Install FileZilla Server. During install, set an administration password and leave the server to start as a
   service. The administration port is normally 14148.
3. Open the Administration Interface and connect to `127.0.0.1` with that password.
4. In the server settings open Rights management > Users, add a user (for example `ftpuser1`) with a password,
   and give it a mount point: virtual path `/`, native path `C:\FTP`, with read and write access.
5. Look at the FTP listener (0.0.0.0, port 21) and its protocol setting. Recent versions default to "Require
   explicit FTP over TLS", which works with FileZilla Client once the self-signed certificate is accepted. To
   demonstrate plain FTP, or to use a client without TLS, change it to "Explicit FTP over TLS and insecure plain
   FTP". In the passive mode settings tick the custom port range and note it for the firewall rule (it normally
   offers 49152 to 65534). I could not open the FileZilla site while preparing this, so check these three
   settings against what the fresh install shows.
6. Windows Defender Firewall on the server: allow inbound TCP 21 and the passive port range.
   ```powershell
   New-NetFirewallRule -DisplayName "FTP control 21" -Direction Inbound -Protocol TCP -LocalPort 21 -Action Allow
   New-NetFirewallRule -DisplayName "FTP passive data" -Direction Inbound -Protocol TCP -LocalPort 49152-65534 -Action Allow
   ```
7. Prove the service is listening, on the server:
   ```powershell
   Get-Service *filezilla*
   netstat -ano | findstr :21
   ```
8. Test from a different machine:
   ```powershell
   Test-NetConnection <server-IP> -Port 21
   ```
   Then connect with FileZilla Client (host, user name, password, port 21), list the folder, upload one file and
   download one file.
9. Open the server log in the Administration Interface and find the login and the two transfers.

Optional and worth doing: run Wireshark on the client with the display filter `ftp`, log in over plain FTP,
and screenshot the `USER` and `PASS` lines in clear text. It demonstrates the weakness named in the written answer.

### 3.2 If the class uses IIS FTP on Windows Server

```powershell
Install-WindowsFeature Web-Server, Web-Ftp-Server, Web-Mgmt-Console
```

IIS Manager > Sites > Add FTP Site: name, physical path, binding (IP, port 21), SSL "No SSL" or "Allow SSL" for a
lab, Basic authentication, allow the chosen user Read and Write. The Windows account also needs NTFS permission
on the folder. Check with `Get-Service ftpsvc` and `netstat -ano | findstr :21`.

### 3.3 If the class uses vsftpd on Linux

```bash
sudo apt install vsftpd
sudo nano /etc/vsftpd.conf      # local_enable=YES, write_enable=YES
sudo systemctl restart vsftpd
systemctl status vsftpd
ss -tlnp | grep :21
sudo ufw allow 21/tcp
```

### 3.4 Screens to capture

Reference snips `lab11_ref1` to `lab11_ref5` in `05_analysis/reference_snips/` show a real run of each of these
on a Linux test server, with the lines to look for numbered.

1. The service running (`Get-Service` output or the admin window showing the server online).
2. The user and its shared folder in the server configuration.
3. `netstat` on the server showing port 21 listening.
4. The client connected: the `230` login reply and the directory listing.
5. One upload and one download completed in the client.
6. The server log showing the same session.

### 3.5 Problems this lab usually produces

| Symptom | Check with | Usual cause | Fix |
|---|---|---|---|
| Connection times out | `Test-NetConnection <server-IP> -Port 21` | Server firewall blocking port 21, or the service is stopped | Add the firewall rule; start the service |
| Connection refused | `netstat -ano \| findstr :21` on the server | Nothing listening on 21, or listening on a different address | Start the service; check the listener address |
| `530 Login incorrect` | Server log | Wrong user name or password, or the user is disabled | Correct the credentials or the user |
| Login works, then the directory listing hangs or fails | Client log (look at the lines after `PASV` or `PORT`); Wireshark | Passive ports blocked by the server firewall; or active mode blocked by the client firewall | Open the passive range on the server and use passive mode in the client |
| Listing hangs only in the Windows command-line `ftp` | Try the same login in FileZilla Client | The built-in Windows `ftp.exe` only does active mode, which the client firewall blocks | Use a client that supports passive mode |
| Client refuses to log in and the server asks for TLS | Server listener protocol setting | The server requires FTP over TLS and the client is sending plain FTP | Use explicit FTP over TLS in the client, or allow plain FTP on the listener for the lab |
| `550` permission denied on upload | Mount point access mode; NTFS permissions on the folder | Folder shared read-only, or the service account cannot write to it | Give write access in both places |

---

## 4. Lab 12 email server

The pasted task does not name the mail server. The steps below fit hMailServer on Windows Server with
Thunderbird as the client, which is the common pairing for a lab that sits next to AD DS. The order and the
checks are the same for any product.

### 4.1 Build order

1. **DNS first** (DNS Manager on the domain controller): an A record for the mail server (for example `mail`)
   and an MX record for the domain that points to it.
   ```powershell
   nslookup -type=mx <domain>
   nslookup mail.<domain>
   ```
2. **Install the mail server.** For hMailServer, version 5.6.x wants .NET Framework 3.5 installed first on
   Windows Server (`Install-WindowsFeature NET-Framework-Core`); version 5.7.x needs .NET Framework 4.5 or later,
   which current Windows Server already has. Choose the built-in database, set an administrator password, then
   open hMailServer Administrator and connect.
3. **Add the domain**, using the same name as the MX record, then **add two mailboxes** (for example
   `user1@<domain>` and `user2@<domain>`) with passwords.
4. **Check the listeners.** Standard ports: SMTP 25 (server to server) and 587 (client submission), POP3 110,
   IMAP 143. With TLS they are 465, 995 and 993.
   ```powershell
   netstat -ano | findstr ":25 :110 :143 :587"
   ```
5. **Firewall** on the mail server: allow the ports in use.
   ```powershell
   New-NetFirewallRule -DisplayName "Mail SMTP POP3 IMAP" -Direction Inbound -Protocol TCP -LocalPort 25,110,143,587 -Action Allow
   ```
6. **Client**: in Thunderbird add each account with manual settings. Incoming IMAP `mail.<domain>` port 143,
   outgoing SMTP `mail.<domain>` port 25 or 587, user name is the full email address, connection security and
   authentication to match the server (None and "Normal password" on a plain lab server).
7. **Test**: send from user1 to user2, receive, reply, receive the reply.
8. **Server log**: find the SMTP session for the message.

A quick test that needs no mail client (Telnet client feature installed):

```
telnet mail.<domain> 25
EHLO client
MAIL FROM:<user1@domain>
RCPT TO:<user2@domain>
DATA
Subject: test

hello
.
QUIT
```

A `220` banner proves the server is reachable, and `250` after the final dot proves it accepted the message.

### 4.2 Screens to capture

Reference snips `lab12_ref1` to `lab12_ref5` in `05_analysis/reference_snips/` show a real mail server sending
and receiving between two mailboxes, with the lines to look for numbered.

1. DNS Manager showing the MX and A records, or the `nslookup -type=mx` output.
2. The mail server administrator showing the domain and both mailboxes, and the server status as running.
3. The client account settings (incoming and outgoing server).
4. user1's Sent folder with the test message.
5. user2's Inbox with the same message open, headers visible, then the reply arriving back at user1.
6. The server log lines for that delivery.

### 4.3 Problems this lab usually produces

| Symptom | Check with | Usual cause | Fix |
|---|---|---|---|
| Client cannot find the server | `nslookup mail.<domain>`; `ipconfig /all` on the client | Client is using a DNS server other than the domain controller, or the A record is missing | Point the client's DNS at the DC; add the record |
| Client times out connecting | `Test-NetConnection mail.<domain> -Port 143` (and 25) | Firewall on the mail server, or the service is stopped | Add the rule; start the service |
| Login rejected | Server log | User name entered without the `@domain` part, or the wrong password | Use the full address |
| Sending fails with an authentication or relay error (`530`, `550`) | Server log; SMTP settings in the client | Server requires SMTP authentication and the client is not sending it, or the IP range rules forbid relaying | Turn on authentication in the client's outgoing server |
| Message sent, never arrives | Server log and delivery queue; `nslookup -type=mx <domain>` | Domain name on the server does not match the address domain, or the MX record is wrong | Make the names match |
| TLS or certificate warning | Client connection security setting | Client set to SSL/TLS or STARTTLS when the server has no certificate | Match the client setting to the server |

### 4.4 Five-minute checks that show the Lab 12 theory on my own domain

Run these on a domain-joined machine. They turn the four written answers into things I have seen.

| Command | What it shows | Theory question |
|---|---|---|
| `nltest /dsgetsite` | The AD site this computer is in | AD DS sites |
| `nltest /dsgetdc:<domain>` | The DC that DC Locator picked for me, and its site | AD DS sites |
| `nslookup -type=srv _ldap._tcp.dc._msdcs.<domain>` | The SRV records with each DC's priority and weight | AD DS sites |
| `nslookup -type=srv _ldap._tcp.<SiteName>._sites.dc._msdcs.<domain>` | The site-specific SRV records | AD DS sites |
| `w32tm /query /status` | This machine's stratum, time source and offset | NTP and stratum |
| `w32tm /query /source` | Who this machine takes its time from | NTP and stratum |
| `netdom query fsmo` | Which DC holds the PDC emulator role (the domain's time master) | NTP and stratum |
| `klist` | The Kerberos tickets issued at logon | User authentication |
| `whoami /groups` | The group memberships used to authorise me | User authentication |
| `Get-WindowsFeature AD-*, ADFS*, ADLDS, ADRMS` (on the server) | The Active Directory roles and which are installed | Active Directory services |

---

## 5. Troubleshooting toolkit

Method: start at the bottom and work up, change one thing at a time, and re-run the test that failed after
every change.

| Layer | Question | Windows | Linux |
|---|---|---|---|
| Physical / virtual link | Is the adapter connected and on the right virtual network? | `Get-NetAdapter`, VM settings | `ip link`, VM settings |
| IP addressing | Do I have the right address, mask and gateway? | `ipconfig /all` | `ip a`, `ip route` |
| Local reachability | Can I reach the gateway and the other host? | `ping`, `arp -a` | `ping`, `ip neigh` |
| Path | Where does it stop? | `tracert`, `pathping` | `traceroute`, `mtr` |
| Name resolution | Does the name resolve, and to the right address? | `nslookup`, `Resolve-DnsName` | `nslookup`, `dig` |
| Port | Is the port open from here? | `Test-NetConnection <host> -Port <n>` | `nc -zv <host> <n>` |
| Service | Is the service running and listening? | `Get-Service`, `netstat -ano` | `systemctl status`, `ss -tlnp` |
| Firewall | Is a rule blocking it? | `Get-NetFirewallProfile`, `Get-NetFirewallRule` | `sudo ufw status`, `sudo iptables -L -n` |
| Packets | What is really on the wire? | Wireshark | `sudo tcpdump -i <if>`, Wireshark |
| Application | What does the log say? | Event Viewer, the application's own log | `journalctl -u <service>`, the application's own log |

Reading the result of the first three tests narrows most faults quickly:

* Ping to my own gateway fails: my address, mask or adapter attachment is wrong.
* Ping by IP works and ping by name fails: DNS.
* Ping works and the port test fails: firewall or the service is not listening.
* Port test works and the application fails: credentials, permissions or application settings.

---

## 6. Questions I should be able to answer at mark-off

**Lab 10**

* Why does Security Onion need two adapters, and why has the monitor adapter no IP address?
* What is the difference between a Suricata alert and a Zeek log?
* Where did this alert come from (source IP, destination IP, rule) and how did I get from the alert to the packets?
* What did I check, in what order, when something did not work?

**Lab 11**

* Which ports does FTP use, and what is the difference between active and passive mode?
* Why is plain FTP insecure, and what are FTPS and SFTP?
* Where in my screenshots is the proof that the server is running and that a transfer happened?

**Lab 12**

* What does an MX record do? Which protocol sends mail and which ones retrieve it?
* How does a client choose a domain controller, and what keeps the choice inside its own site?
* What is my machine's stratum and where does it get its time (`w32tm /query /status`)?
* What is the difference between authentication and authorisation?
* Name the five Active Directory roles and say what AD DS does.
