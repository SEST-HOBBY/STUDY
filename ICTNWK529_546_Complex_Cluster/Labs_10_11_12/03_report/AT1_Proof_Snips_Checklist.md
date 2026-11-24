# AT1: which written questions need a snip as proof

Checked on 24 Nov 2026 against the AT1 working template (`ICTNWK529_ICTNWK546_AT1 WORKING ON.docx`, on the
branch `sest-dev/laughing-hypatia-qnrqqs`). For each written question: whether the template asks for a
screenshot beside it, what that screenshot has to show, and whether I have it.

A proof snip has to come from my own lab equipment, with my own device names and domain name in it. That is
what the teacher marks off, and the template says the domain and controller names "vary from person to person".
None of them can be produced anywhere else. The images in `05_analysis/reference_snips/` are examples from a
test machine and are not proof.

"In the template" below means a screenshot is already pasted in the working template (its images 1 to 11).
Confirm each of those is my own and not a demonstration image before submitting.

| # | Written question | Lab | Snip required as proof? | What it has to show | Status |
|---|---|---|---|---|---|
| 1 | What is a proxy | 4 | Yes | The proxy service working: a web page fetched through the proxy, and the Windows manual proxy setup with the proxy's address and port | In the template (image 7): nginx page at 209.165.200.10, proxy set to 172.16.0.11 port 1234 |
| 2, 3 | Steps to configure the firewall | 3 | Yes | `show zone security` on **both SB and MG**; `show policy-map type inspect zone-pair` on **SB** | Partly in the template (image 5): both commands on **MG** only. The SB outputs are not there: check, and take them if missing |
| 4 | Firewall functions | 3 | No extra snip | Covered by the Lab 3 snips above | n/a |
| 5 | What is a VPN | 5 | Yes | `show ip route` on SB and MG; `tracert` from an SB PC to an MG PC; `show crypto isakmp sa`; `show crypto ipsec sa`; `show interface tunnel 0` | Mostly in the template: SB routing table with Tunnel0 (image 8), tracert (image 9), isakmp and ipsec SAs on SB and MG (images 10, 11). Not seen: `show ip route` on MG and `show interface tunnel 0`: check, and take them if missing |
| 6 | NTP and stratum | 8.1 | No | The question stands alone; no screenshot is asked for | n/a |
| 7 | AD DS sites and load balancing | 8.2 | Yes | Active Directory Sites and Services with my sites, subnets and both DCs, my domain name visible | Own snip needed (the template's image 13 is the teacher's example). Not in this repository |
| 8 | User authentication; Active Directory | 8.1 | Yes | The two load-sharing domain controllers, named `dc1.<name1>.<name2>` and `dc2.<name1>.<name2>` | Own snip needed (image 12 is the teacher's example). Not in this repository |
| 9 | What is FTP | 11 | Yes | The FTP service running | **Done.** Two snips filed in `02_student_work/screenshots/` |
| 10 | Web services | 8.9 | Yes | WSUS: IIS role installed on the WSUS server, synchronised to Microsoft, selected updates downloaded, domain name in the background | Own snips needed (images 23, 24 are the teacher's examples). Not in this repository |
| 11 | What is VoIP | 7 | Yes | Successful IP phone registration on the CMEs | Own snips needed; nothing in the template. Not in this repository |
| 12 | What is SNMP | 9 | Yes | PRTG device tree with my domain name in the background: SNMP traffic and syslog sensors on the local-probe devices and on the remote-probe devices | Own snip needed (image 26 is the teacher's example). Not in this repository |
| 10.1 | Troubleshooting report | 10 | No | Text only. The Lab 11 client snip happens to show problem 2 (the two `530` replies) and can be referred to | n/a |

## Commands for the snips still to take

| Snip | Where | Command or screen |
|---|---|---|
| Lab 3, SB side | SB router console | `show zone security` then `show policy-map type inspect zone-pair` |
| Lab 5, missing outputs | MG router; either router | `show ip route` on MG; `show interface tunnel 0` (look for "Tunnel protocol/transport IPSEC/IP") |
| Lab 7 | Each CME router | `show ephone registered` (or `show ephone summary`), showing each phone REGISTERED with its extension |
| Lab 8.1 | DC1 | Active Directory Users and Computers > Domain Controllers, both DCs listed |
| Lab 8.2 | DC1 | Active Directory Sites and Services, sites and subnets expanded |
| Lab 8.9 | WSUS server | Server Manager showing the IIS role; Update Services showing the last synchronisation succeeded and updates approved and downloaded |
| Lab 9 | PRTG core server | Devices tree expanded for the local probe and the remote probe |
