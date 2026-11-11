# Lab 10, 11 and 12 Results

Draft prepared before the labs. The written answers for Labs 11 and 12 are complete. Every line that starts
with **AFTER LAB** is a slot that can only be filled from what happens on the day (my screenshots and my
troubleshooting notes). Search for "AFTER LAB" before submitting; none should be left.

---

## Lab 10 Results

**AFTER LAB** Screenshot 10-A: replace the first demonstration screenshot in the template with my own equivalent.

**AFTER LAB** Screenshot 10-B: replace the second demonstration screenshot in the template with my own equivalent.

(The runbook lists the Security Onion screens to capture so that whichever two the template shows, I have them.
Reference: `05_analysis/reference_snips/lab10_ref1` to `lab10_ref3` show the test alert itself.)

### Part 10.1 Troubleshooting report

**AFTER LAB** Write the three parts below from the troubleshooting log in the runbook (one row per problem:
time, symptom, command or tool, output, cause, fix, proof it worked). Report only what happened in my own lab.

#### Network symptoms

**AFTER LAB** For each problem: what I was trying to do, what I saw (exact error text, timeout, empty page, no
alerts), which machine I saw it on, and whether it was constant or intermittent.

#### Troubleshooting tools and techniques

**AFTER LAB** For each problem: the order I checked things in (I work up the layers: adapter and link, IP
address and mask, gateway, DNS, port, service, then the application), the utility used at each step, and the
line of output that pointed to the cause.

#### Resolution

**AFTER LAB** For each problem: the change I made, the command or setting, and the test that proved the fix
(the same test that failed before, now passing, with a screenshot).

---

## Lab 11 Results

**AFTER LAB** Screenshot 11-A: FTP server installed and running (service status or the server's admin window).

**AFTER LAB** Screenshot 11-B: the FTP user and the shared folder configured on the server.

**AFTER LAB** Screenshot 11-C: a client logged in and listing the folder (the 230 login reply and the directory listing).

**AFTER LAB** Screenshot 11-D: a file uploaded and a file downloaded, with the server log showing the transfer.

(Reference examples of each: `05_analysis/reference_snips/lab11_ref1` to `lab11_ref5`. They are examples only;
the snips that go here are my own.)

### What is the FTP protocol?

FTP (File Transfer Protocol) is an application-layer protocol for copying files between a client and a server
over TCP. It is defined in RFC 959. FTP uses two connections. The control connection goes to TCP port 21 on the
server and carries the login and the commands, such as USER, PASS, LIST, RETR (download) and STOR (upload). A
separate data connection is opened for each directory listing or file transfer. In active mode the server opens
the data connection from its port 20 back to the client. In passive mode the client opens it to a high port
that the server nominates, which is the mode that works through NAT and client firewalls.

Standard FTP sends the user name, password and file contents in clear text, so anyone capturing the traffic can
read them. On a production network I would use FTPS (FTP over TLS) or SFTP (file transfer over SSH on port 22).

---

## Lab 12 Results

**AFTER LAB** Screenshot 12-A: the mail server running with my domain and user mailboxes created.

**AFTER LAB** Screenshot 12-B: the DNS records for the mail domain (MX record and the mail server's A record).

**AFTER LAB** Screenshot 12-C: a mail client account set up for one user (incoming and outgoing server settings).

**AFTER LAB** Screenshot 12-D: a message sent from one user and received by another, and the reply coming back.

(Reference examples: `05_analysis/reference_snips/lab12_ref1` to `lab12_ref5`. They are examples only; the
snips that go here are my own.)

### How do AD DS sites implement load balancing across DCs to share client AD requests?

An AD DS site is a group of well-connected IP subnets, and every domain controller (DC) belongs to a site. When
a DC starts, its Netlogon service registers SRV records in DNS, including site-specific records in the form
`_ldap._tcp.<SiteName>._sites.dc._msdcs.<domain>`.

A client finds a DC through the DC Locator process. It asks DNS for the DCs in its own site and DNS returns all
of them. By default every DC registers with the same SRV priority (0) and weight (100), so the client chooses
among them at random in proportion to weight, sends an LDAP ping to the candidates and uses the first DC that
answers. Each client makes its own choice, so logons, LDAP queries and Group Policy requests end up spread
roughly evenly across the DCs in that site, and the traffic stays on the local network and off the WAN links.

If the chosen DC stops answering, the client repeats the lookup and moves to another DC. If a site has no DC,
the DCs in the nearest site by site-link cost register SRV records for it (automatic site coverage). An
administrator can change the share of load by adjusting a DC's SRV weight or priority, for example to send
fewer clients to the PDC emulator.

### What is NTP? How does the stratum hierarchical system work for NTP?

NTP (Network Time Protocol) keeps the clocks of computers and network devices synchronised to a common
reference, normally UTC. It runs over UDP port 123 and the current version is NTPv4 (RFC 5905). A client
exchanges timestamped packets with one or more time servers, works out the offset and the network delay, and
gradually corrects its own clock. Accurate time matters because log entries from different devices have to line
up when troubleshooting, certificates depend on the date, and Kerberos by default rejects a logon when the
clocks differ by more than five minutes.

Stratum is the number of steps between a device and a reference clock:

* Stratum 0 devices are the reference clocks themselves, such as atomic clocks and GPS receivers. They are not
  on the network.
* A stratum 1 server is connected directly to a stratum 0 device.
* A stratum 2 server synchronises over the network from a stratum 1 server, a stratum 3 server from stratum 2,
  and so on down to stratum 15.
* Stratum 16 means the device is unsynchronised.

Each server is a client of the level above it and a server to the level below it. This spreads the load so that
a small number of reference clocks can serve millions of devices, and the stratum number tells a device how far
a source is from a reference clock so it can prefer the closer one. In an Active Directory domain the DC holding
the PDC emulator role in the forest root domain takes its time from an external NTP source, the other DCs
follow it, and member computers follow their DC.

### What is user authentication?

User authentication is the process of proving that a user is who they claim to be before the system gives them
access. The user presents an identity, usually a user name, and one or more credentials: something they know
(a password or PIN), something they have (a smart card, phone app or security key) or something they are (a
fingerprint or face). Using two or more of these types together is multi-factor authentication.

Authentication answers the question "who are you?". Authorisation follows it and decides what that user is
allowed to do. In an Active Directory domain the domain controller authenticates users with Kerberos, with NTLM
as a fallback, and issues tickets that the user's computer presents to file, mail and other servers. The user
enters the password once and is then signed in to every service in the domain (single sign-on).

### What are Active Directory services?

Active Directory services are the Windows Server roles that provide identity and access management for a
network. There are five:

* **AD DS (Domain Services)** is the directory itself. It stores users, groups, computers and other objects,
  authenticates and authorises them, and applies Group Policy. Domain controllers hold the database and
  replicate it to each other.
* **AD CS (Certificate Services)** runs a public key infrastructure that issues and manages digital
  certificates for users, computers and services.
* **AD FS (Federation Services)** gives single sign-on to web applications in other organisations or in the
  cloud by passing claims in security tokens, so the password stays inside the home domain.
* **AD LDS (Lightweight Directory Services)** is an LDAP directory for applications that need directory data
  without a domain or domain controllers.
* **AD RMS (Rights Management Services)** protects documents and emails by controlling who can open, print,
  copy or forward them.
