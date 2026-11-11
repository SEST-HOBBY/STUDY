# ICTNWK529 / ICTNWK546, Complex Cluster: Labs 10, 11 and 12

Lab 10: Security Onion, plus a troubleshooting report (Part 10.1). Lab 11: install a simple FTP server.
Lab 12: email server, plus four short questions on AD DS sites, NTP, user authentication and Active Directory
services. Status: prepared before the labs; the labs themselves are still to do.

## File register and provenance

| File | Folder | Provenance | Notes |
|---|---|---|---|
| `Lab_10_11_12_Results_task_text.md` | 00_assessment_documents | Text of the results template as I pasted it on 11 Nov 2026 | The Word template with the teacher's demonstration screenshots is not in the repository |
| `Lab_10_11_12_Prep_Runbook.md` | 02_student_work | Written with AI assistance on 11 Nov 2026 | Build order, screens to capture, likely faults and how to diagnose them, a troubleshooting log to fill in, and mark-off questions. Security Onion, hMailServer, Windows time and DC Locator details were checked against the vendors' own documentation sources; the FileZilla Server details could not be opened and are flagged in the text |
| `screenshots/` | 02_student_work | Mine, taken in the lab | Empty until the labs are done |
| `Lab_10_11_12_Results_draft.md` | 03_report | Written with AI assistance on 11 Nov 2026 | The five written answers are complete. Every screenshot and the whole of Part 10.1 are marked **AFTER LAB** |
| `reference_snips/*.png` and `raw/*.txt` | 05_analysis | Real runs on a Linux test machine, 11 Nov 2026 | 13 reference examples (3 for Lab 10, 5 each for Labs 11 and 12). Not lab evidence; see that folder's README |
| `tools/` | 05_analysis | Scripts behind the reference runs | `ftp_reference_*`, `mail_reference_*`, `ids_reference_capture.sh` produce `raw/`; `render_snips.js` draws the images |

## What is still needed

1. The original Word template, so the two demonstration screenshots for Lab 10 can be identified.
2. Which FTP server and which mail server the class uses. The runbook assumes FileZilla Server and hMailServer
   with Thunderbird and gives IIS FTP and vsftpd as alternatives.
3. My own screenshots from the three labs, marked off by the teacher.
4. My troubleshooting notes from the day. Part 10.1 has to describe what happened in my own lab, so it is
   written after the lab from the log in the runbook.
