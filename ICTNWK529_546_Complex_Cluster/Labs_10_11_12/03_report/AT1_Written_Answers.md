# AT1 written answers

The twelve written questions from the AT1 template, in the order of my question list of 24 Nov 2026, followed
by Part 10.1. The template sets each question in red under the lab it belongs to; the lab is noted beside each
heading so the answer can be pasted in the right place. Remove the red instruction text when the answer goes in.

---

## 1. Briefly describe what is proxy (Lab 4)

A proxy server is an intermediary that sits between client computers and the servers they want to reach,
usually between a LAN and the internet. The client sends its request to the proxy, the proxy makes the request
to the destination on the client's behalf, and then passes the reply back. The destination sees the proxy's
address and never the client's own.

Organisations use a forward proxy to control and log which websites users can reach, to filter content, to
cache pages that are requested often so they load faster and use less bandwidth, and to hide internal
addresses. A reverse proxy does the same job in the other direction: it stands in front of web servers and
receives requests from the internet for them, which allows load balancing and protects the servers. In the lab
the Windows PC was pointed at the proxy by entering the proxy's IP address and port in its proxy settings, so
its web traffic went through the proxy server.

## 2 and 3. Briefly describe the following: what are the steps to configure the firewall in Lab 3?

The Lab 3 firewall is a Cisco IOS zone-based policy firewall (ZPF) on the SB and MG routers. Interfaces are
placed into security zones, and traffic between two zones is blocked unless a policy allows it. The steps are:

1. **Create the security zones**, one for the trusted LAN and one for the untrusted side:
   `zone security INSIDE` and `zone security OUTSIDE`.
2. **Identify the traffic with a class map**: `class-map type inspect match-any <name>` followed by
   `match protocol tcp`, `match protocol udp`, `match protocol icmp`, or a match on an access list.
3. **Set the action in a policy map**: `policy-map type inspect <name>`, then `class type inspect <class>` and
   the action `inspect` (allow and track the session so that replies are let back in), `pass` or `drop`.
4. **Create a zone pair and attach the policy**: `zone-pair security <name> source INSIDE destination OUTSIDE`,
   then `service-policy type inspect <policy>`. A zone pair works in one direction only, so traffic that starts
   from the outside stays blocked unless a second pair is made for it.
5. **Assign the interfaces to the zones**: on each interface, `zone-member security INSIDE` or
   `zone-member security OUTSIDE`.
6. **Verify**: `show zone security` (zones and their member interfaces), `show zone-pair security`, and
   `show policy-map type inspect zone-pair` (class maps, actions and match counters). Then test: a ping or web
   session from inside to outside succeeds, and one started from outside to inside fails.

## 4. What are firewall applications (functions of firewalls)?

A firewall is placed between networks with different levels of trust and decides which traffic may pass. Its
main functions are:

* **Packet filtering**: permit or deny packets by source and destination IP address, protocol and port.
* **Stateful inspection**: track each connection so that only replies to sessions started from the trusted
  side are allowed back in.
* **Application inspection**: examine the application-layer content (for example HTTP, FTP, DNS) to block
  misuse of a permitted port and to filter URLs or content.
* **Network address translation (NAT/PAT)**: hide internal private addresses behind a public address.
* **Segmentation**: divide the network into zones such as inside, outside and a DMZ for public servers, and
  control traffic between them.
* **VPN termination**: act as the endpoint for site-to-site and remote-access VPN tunnels.
* **Logging and alerting**: record permitted and denied traffic for monitoring, audit and troubleshooting.
* **Threat prevention** on next-generation firewalls: intrusion prevention, malware scanning and
  application and user identification.

Firewalls are applied at the network perimeter between the LAN and the internet, between internal segments
(for example between user VLANs and servers), in front of a DMZ, and on individual computers as host-based
firewalls such as Windows Defender Firewall.

## 5. Briefly describe what is VPN (Lab 5)

A VPN (virtual private network) is a secure, private connection made across a public or untrusted network such
as the internet. It builds a tunnel between two endpoints: the original packets are encapsulated inside new
packets, and are encrypted and authenticated, so that anyone in the middle can neither read nor alter them.
This gives confidentiality (encryption), integrity (hashing) and authentication of the two ends (pre-shared
keys or certificates).

There are two main types. A site-to-site VPN joins two networks, router to router or firewall to firewall, so
the users on each side need no special software. A remote-access VPN connects a single user's device to the
company network through a VPN client. In Lab 5 the SB and MG routers were joined by a site-to-site VPN: a GRE
tunnel across the ISP, protected by IPsec, so that SB and MG devices could reach each other through the tunnel
and the routing protocol could run over it.

## 6. Briefly explain the purpose of NTP in computer networks. Describe what an NTP stratum level is and how the stratum hierarchy works

NTP (Network Time Protocol) keeps the clocks of computers and network devices synchronised to a common
reference, normally UTC. It runs over UDP port 123. A client exchanges timestamped packets with one or more
time servers, works out the offset and the network delay, and gradually corrects its own clock. Accurate,
matching time matters because log and syslog entries from different devices have to line up when
troubleshooting or investigating a security event, certificates depend on the date, and Kerberos in Active
Directory by default rejects a logon when the clocks differ by more than five minutes.

The stratum level is the number of steps between a device and a reference clock, so it shows how far the
device is from the original time source:

* Stratum 0 devices are the reference clocks themselves, such as atomic clocks and GPS receivers. They are not
  on the network.
* A stratum 1 server is connected directly to a stratum 0 device.
* A stratum 2 server synchronises over the network from a stratum 1 server, a stratum 3 server from stratum 2,
  and so on down to stratum 15.
* Stratum 16 means the device is unsynchronised.

Each server is a client of the level above it and a server to the level below it. This spreads the load so
that a small number of reference clocks can serve millions of devices, and a device that can see several
sources prefers the one with the lower stratum number. A device always reports a stratum one higher than its
source: a Cisco router configured with `ntp master 5` announces itself as stratum 5, and the devices that
synchronise from it become stratum 6. In Lab 9 the SB router was the NTP master and SB-S1, the MG router and
MG-S1 were its clients. In an Active Directory domain the DC holding the PDC emulator role in the forest root
domain takes its time from an external source, the other DCs follow it, and member computers follow their DC.

## 7. Describe how AD DS sites implement load balancing across DCs to share client AD requests (Lab 8.2)

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

## 8. Briefly describe what user authentication is. Briefly describe what Active Directory is (Lab 8.1)

**User authentication** is the process of proving that a user is who they claim to be before the system gives
them access. The user presents an identity, usually a user name, and one or more credentials: something they
know (a password or PIN), something they have (a smart card, phone app or security key) or something they are
(a fingerprint or face). Using two or more of these types together is multi-factor authentication.
Authentication answers the question "who are you?". Authorisation follows it and decides what that user is
allowed to do. In an Active Directory domain the domain controller authenticates users with Kerberos, with NTLM
as a fallback, and issues tickets that the user's computer presents to file, mail and other servers, so the
user enters the password once and is signed in to every service in the domain (single sign-on).

**Active Directory** is Microsoft's directory service for Windows networks. It is a central, replicated
database of the objects on the network (users, groups, computers, printers, shared folders) organised into
domains, trees and forests, with organisational units inside each domain. Domain controllers hold the database
and replicate changes to each other. Active Directory lets administrators manage accounts and permissions in
one place, authenticates and authorises every logon, and applies Group Policy settings to users and computers.
It depends on DNS to locate domain controllers. The core role is Active Directory Domain Services (AD DS);
the related roles are Certificate Services (AD CS, issues digital certificates), Federation Services (AD FS,
single sign-on to outside web applications), Lightweight Directory Services (AD LDS, an LDAP directory for
applications) and Rights Management Services (AD RMS, protects documents and email).

## 9. Briefly describe what is FTP protocol (Lab 11)

FTP (File Transfer Protocol) is an application-layer protocol for copying files between a client and a server
over TCP. It is defined in RFC 959. FTP uses two connections. The control connection goes to TCP port 21 on the
server and carries the login and the commands, such as USER, PASS, LIST, RETR (download) and STOR (upload). A
separate data connection is opened for each directory listing or file transfer. In active mode the server opens
the data connection from its port 20 back to the client. In passive mode the client opens it to a high port
that the server nominates, which is the mode that works through NAT and client firewalls.

Standard FTP sends the user name, password and file contents in clear text, so anyone capturing the traffic can
read them. On a production network I would use FTPS (FTP over TLS) or SFTP (file transfer over SSH on port 22).

## 10. Describe briefly what is web services (Lab 8.9)

Web services are services that a server makes available to other computers over a network using the standard
web protocols, HTTP and HTTPS (TCP ports 80 and 443). A web server such as Microsoft IIS or Apache listens for
requests and answers them. The content it serves can be web pages for people to read in a browser, or data for
other programs to use.

In the narrower sense a web service is a function that one program calls on another across the network,
whatever operating system or programming language each side uses. The request and the reply are carried over
HTTP in a standard text format. The two common styles are SOAP, which exchanges XML messages described by a
WSDL file, and REST, which uses ordinary HTTP methods (GET, POST, PUT, DELETE) on URLs and usually returns JSON.
A web application is a complete application that runs on a web server and is used through a browser, and it
often calls web services behind the scenes. In Lab 8.9 the IIS role was installed on the WSUS server because
WSUS is delivered this way: client computers contact the WSUS web services over HTTP (port 8530 by default) to
find and download their approved updates.

## 11. Describe what is VoIP (Lab 7)

VoIP (Voice over Internet Protocol) carries telephone calls as data packets over an IP network in place of a
separate telephone network. The phone samples the voice, a codec such as G.711 or G.729 digitises and
compresses it, and the samples are sent in RTP packets over UDP to the other phone, which converts them back
to sound.

A signalling protocol sets up, manages and ends the calls: SIP is the open standard, H.323 is an older one, and
Cisco phones can use SCCP (Skinny). A call-control server, in the lab Cisco Unified Communications Manager
Express (CME) running on the router, registers the IP phones, gives each one its extension number and routes
calls between them. Voice needs low delay, jitter and packet loss, so VoIP networks put the phones in a voice
VLAN, apply QoS to give voice packets priority, and usually power the phones from the switch with PoE. The
benefits are one network for voice and data, lower call and cabling costs, and features such as voicemail,
call forwarding and softphones.

## 12. Briefly describe what is SNMP (Lab 9)

SNMP (Simple Network Management Protocol) is an application-layer protocol for monitoring and managing network
devices such as routers, switches, servers and printers. It has three parts. The SNMP manager is the network
management system (PRTG in Lab 9). The SNMP agent is software running on each managed device. The MIB
(Management Information Base) is the agent's database of variables, each identified by an OID, such as
interface status, traffic counters, CPU load and uptime.

The manager polls agents with Get, GetNext and GetBulk requests on UDP port 161 and can change a value with
Set. An agent can also report an event by itself, such as an interface going down, by sending a Trap or Inform
to the manager on UDP port 162. SNMPv1 and v2c protect access only with a community string sent in clear text,
normally a read-only one for monitoring. SNMPv3 adds user authentication and encryption. In Lab 9 the routers
and switches were configured as SNMP agents with a read-only community, and the PRTG core and remote probe
polled them to graph interface traffic.

---

## Part 10.1 Troubleshooting report

### Network symptoms

The virtual machines could not ping each other. A ping from one VM to another VM, and to the default gateway
on the router, got no replies, and the fault was constant, not intermittent. Until it was fixed the lab could
not continue, because the machines have to reach each other before any traffic can be generated and monitored.

### Troubleshooting tools and techniques

I used a divide-and-conquer approach: prove which parts of the path work, then look at what is left.

* **ping** established the scope of the problem. The VM could not reach its own gateway, so the fault was close
  to the VM and was not a routing problem further along the path.
* **Cisco show commands** on the router and switch ruled out the network devices. `show ip interface brief`
  showed the interfaces up/up with the correct addresses, `show ip route` showed the expected networks in the
  routing table, and `show running-config` confirmed the interface configuration was as intended.

With the Cisco devices shown to be working, the cause had to be between the VM and the switch. That pointed to
the VM's virtual network adapter in VMware, and its setting was the fault: the adapter was attached to the
wrong type of virtual network (host-only), which keeps the VM on a private network inside the host PC with no
connection to the physical switch.

### Resolution

I changed the VM's network adapter in the VMware settings to Bridged, so that the VM connects directly to the
physical network through the PC's network card that is cabled to the switch, and made sure the adapter was
connected. I then repeated the test that had failed: the VM could ping its gateway and the other VMs, and the
lab continued from there. The lesson is to check the adapter type of a new VM first, before looking for a
fault on the routers and switches.
