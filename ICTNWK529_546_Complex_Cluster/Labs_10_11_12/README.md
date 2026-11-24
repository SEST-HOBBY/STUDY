# ICTNWK529 / ICTNWK546, Complex Cluster: Labs 10, 11 and 12

Lab 10: Security Onion, plus a troubleshooting report (Part 10.1). Lab 11: install a simple FTP server.
Lab 12: email server, plus four short questions on AD DS sites, NTP, user authentication and Active Directory
services. Status at 24 Nov 2026: Lab 11 completed, with its two screenshots filed and written up. Lab 10 and
Lab 12 are still to do.

## File register and provenance

| File | Folder | Provenance | Notes |
|---|---|---|---|
| `Lab_10_11_12_Results_task_text.md` | 00_assessment_documents | Text of the results template as I pasted it on 11 Nov 2026 | The Word template with the teacher's demonstration screenshots is not in the repository |
| `Lab_10_11_12_Prep_Runbook.md` | 02_student_work | Written with AI assistance on 11 Nov 2026 | Build order, screens to capture, likely faults and how to diagnose them, a troubleshooting log to fill in, and mark-off questions. Security Onion, hMailServer, Windows time and DC Locator details were checked against the vendors' own documentation sources; the FileZilla Server details could not be opened and are flagged in the text |
| `screenshots/lab11_*.png` | 02_student_work | My screenshots, received 24 Nov 2026 | `lab11_02_dc2_client_login_upload_dir.png`: DC2 logging in to the Microsoft FTP Service at 172.16.0.50 as `ftp_lab11`, uploading `DC2-to-FTP.txt` and listing the folder. `lab11_01_ftp_server_ip_and_uploaded_file.png`: the server's address being set and the uploaded file read back from `C:\FTP-Lab11` |
| `AT1_Written_Answers.md` | 03_report | Written with AI assistance on 24 Nov 2026 | The twelve written questions of the AT1 template (proxy, Lab 3 firewall steps, firewall functions, VPN, NTP, AD DS sites, authentication and Active Directory, FTP, web services, VoIP, SNMP), each marked with its lab. The Lab 3 answer uses generic zone and policy names; swap in the names from my own configuration. Part 10.1 is the last section, written from my answers on 24 Nov |
| `Lab_10_11_12_Results_draft.md` | 03_report | Written with AI assistance on 11 Nov 2026, revised 24 Nov | Screenshot slots for Labs 10 to 12, each marked **AFTER LAB**, with pointers to the written answers |
| `Lab10_template_demonstration_screenshots/` | 04_extracted_views | Images 27 and 28 of the AT1 template (teacher's 2021 examples) | Show what the two Lab 10 snips are: the nmap scan on the Ubuntu client and the Sguil alert list |
| `reference_snips/*.png` and `raw/*.txt` | 05_analysis | Real runs on a Linux test machine, 11 Nov 2026 | 13 reference examples (3 for Lab 10, 5 each for Labs 11 and 12). Not lab evidence; see that folder's README |
| `tools/` | 05_analysis | Scripts behind the reference runs | `ftp_reference_*`, `mail_reference_*`, `ids_reference_capture.sh` produce `raw/`; `render_snips.js` draws the images |

## What is still needed

1. Lab 10 itself, then my own two Lab 10 snips (nmap scan on the Ubuntu client, Sguil alert list), marked off by
   the teacher.
2. Part 10.1 checked after Lab 10. It is drafted from my own answers (VMs could not ping; Cisco show commands;
   VM network adapter changed). Its details (host-only changed to Bridged, the three show commands named) come
   from the Lab 9 notes and need checking against what I did.
3. What caused the two refused FTP logins in the Lab 11 screenshot and what fixed them, if that is to go into
   the troubleshooting report.
4. Lab 12: which mail server the class uses (the runbook assumes hMailServer with Thunderbird), then my own
   screenshots.

The AT1 Word template itself (`ICTNWK529_ICTNWK546_AT1 WORKING ON.docx`) is on the branch
`sest-dev/laughing-hypatia-qnrqqs` under the Lab 8 folder; this branch does not contain the Lab 8 and Lab 9 folders.
