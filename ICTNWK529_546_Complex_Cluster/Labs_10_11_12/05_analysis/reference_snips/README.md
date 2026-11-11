# Reference snips for Labs 10, 11 and 12

These are reference examples: real runs captured on 11 Nov 2026 on a Linux test machine, rendered as images
with the lines to look for numbered. They show what a working result looks like. They are not my lab evidence
and do not go in the results document; each one carries a banner saying so. My own snips, taken in my lab and
marked off by the teacher, go in `02_student_work/screenshots/`.

`raw/` holds the exact terminal text behind each image. The scripts that produced the runs and the images are
in `05_analysis/tools/`.

## Lab 10 (Security Onion)

Security Onion needs its own virtual machine with 8 GB of RAM or more and could not be run on the test
machine, so there is no reference picture of the SOC web pages. What is here is Suricata, the detection engine
inside Security Onion, raising the same test alert that the lab produces.

| Reference snip | Shows | Where I see it in my lab |
|---|---|---|
| `lab10_ref1_test_traffic.png` | The test request and its reply `uid=0(root) ...` | `curl testmynids.org/uid/index.html` from a monitored machine |
| `lab10_ref2_suricata_alert.png` | The rule and the alert it raises, with source and destination | One row on the SOC **Alerts** page |
| `lab10_ref3_alert_detail.png` | The stored alert record field by field | The detail panel when the alert is expanded in SOC |

## Lab 11 (FTP server)

| Reference snip | Shows | Equivalent with FileZilla Server on Windows | Results slot |
|---|---|---|---|
| `lab11_ref1_server_running.png` | Server version, process running, listening on port 21 | `Get-Service *filezilla*` and `netstat -ano \| findstr :21`, or the admin window connected | 11-A |
| `lab11_ref2_user_and_folder.png` | The settings, the FTP user and its folder | Rights management > Users with the mount point | 11-B |
| `lab11_ref3_client_session.png` | Login (230), listing, upload, download, second listing | FileZilla Client message log and file panes | 11-C, 11-D |
| `lab11_ref4_transfer_proof_and_log.png` | Files present on both sides and the server log of the session | The server's log window | 11-D |
| `lab11_ref5_clear_text_login.png` | User name and password readable in a packet capture | Wireshark with the display filter `ftp` | supports the written answer |

## Lab 12 (email server)

The test machine has no DNS server, so there is no reference for the MX record (slot 12-B). The name
`mail.lab.local` was resolved from the hosts file.

| Reference snip | Shows | Equivalent with a Windows mail server and Thunderbird | Results slot |
|---|---|---|---|
| `lab12_ref1_server_running.png` | Mail domain, two mailboxes, listening on 25, 110 and 143 | The mail server administrator showing the domain and accounts; `netstat -ano` | 12-A |
| `lab12_ref2_smtp_send.png` | The SMTP conversation sending user1's message to user2 | user1's Sent folder; the telnet test in the runbook | 12-D |
| `lab12_ref3_imap_receive.png` | user2 logging in over IMAP and reading the message | user2's Inbox with the message open | 12-D |
| `lab12_ref4_reply_pop3_receive.png` | user2's reply collected by user1 over POP3 | user1's Inbox with the reply | 12-D |
| `lab12_ref5_server_logs.png` | Both deliveries and both mailbox logins in the server logs | The mail server's log | 12-A or 12-D |

The client settings (slot 12-C) are in the commands themselves: server `mail.lab.local`, IMAP 143, POP3 110,
SMTP 25, user name and password, no encryption.
