# Lab 10, 11 and 12 Results

Draft prepared before the labs. Lab 10 is now done; Labs 11 and 12 are still to do. The written answers are kept in one place,
`AT1_Written_Answers.md`, and this file tracks the screenshots. Every line that starts
with **AFTER LAB** is a slot that can only be filled from what happens on the day (my screenshots and my
troubleshooting notes). Search for "AFTER LAB" before submitting; none should be left.

---

## Lab 10 Results

Lab completed on or before 24 Nov 2026. The two snips match the two demonstration screenshots in the template
(copies in `04_extracted_views/Lab10_template_demonstration_screenshots/`).

**AFTER LAB** Screenshot 10-A: a terminal on my domain-joined Ubuntu client running the `nmap` scan
(`sudo nmap -O <target>`), with my domain name visible in the prompt and the scan report below it.

**AFTER LAB** Screenshot 10-B: the Sguil console on Security Onion, RealTime Events tab, showing the alerts
raised by that scan (`GPL ICMP_INFO PING` and `ET SCAN ...` rows with my scanning machine as the source), and
the Agent Status panel with the agents UP.

### Part 10.1 Troubleshooting report

In `AT1_Written_Answers.md`, last section.

---

## Lab 11 Results

**AFTER LAB** Screenshot 11-A: FTP server installed and running (service status or the server's admin window).

**AFTER LAB** Screenshot 11-B: the FTP user and the shared folder configured on the server.

**AFTER LAB** Screenshot 11-C: a client logged in and listing the folder (the 230 login reply and the directory listing).

**AFTER LAB** Screenshot 11-D: a file uploaded and a file downloaded, with the server log showing the transfer.

(Reference examples of each: `05_analysis/reference_snips/lab11_ref1` to `lab11_ref5`. They are examples only;
the snips that go here are my own.)

### What is the FTP protocol?

Answer 9 in `AT1_Written_Answers.md`.

---

## Lab 12 Results

**AFTER LAB** Screenshot 12-A: the mail server running with my domain and user mailboxes created.

**AFTER LAB** Screenshot 12-B: the DNS records for the mail domain (MX record and the mail server's A record).

**AFTER LAB** Screenshot 12-C: a mail client account set up for one user (incoming and outgoing server settings).

**AFTER LAB** Screenshot 12-D: a message sent from one user and received by another, and the reply coming back.

(Reference examples: `05_analysis/reference_snips/lab12_ref1` to `lab12_ref5`. They are examples only; the
snips that go here are my own.)

### Written questions

| Template question | Answer in `AT1_Written_Answers.md` |
|---|---|
| How AD DS sites implement load balancing across DCs | 7 |
| What is NTP, and how the stratum hierarchy works | 6 |
| What is user authentication | 8 |
| What are Active Directory services | 8 |
