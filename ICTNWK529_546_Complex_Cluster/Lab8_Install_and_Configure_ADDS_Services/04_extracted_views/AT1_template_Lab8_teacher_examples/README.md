# Teacher demonstration screenshots from the AT1 template (Lab 8 section)

Extracted on 2026-10-22 from `00_assessment_documents/ICTNWK529_ICTNWK546_AT1 WORKING ON.docx` (word/media
image12 to image25) and renamed by the sub-lab they sit under. They are the TEACHER'S examples (domain
`Maggie.Zhong`; one from another student, `sungho.hong`). The template says in red to remove them before
submission. Reference only: what each of your own screenshots should resemble. The full shot list is in
`05_analysis/Lab8_screenshot_shot_list_2026-10-22.md`; the template's full text with the red instructions
is in `../AT1_template_text_walk.txt`.

| File | Sub-lab | Shows |
|---|---|---|
| `8.1_teacher_ADUC_domain_controllers.jpeg` | 8.1 | Active Directory Users and Computers, Domain Controllers: DC1 and DC2, GC, domain tree on the left |
| `8.2_teacher_AD_sites_and_services.png` | 8.2 | AD Sites and Services: four subnets, SB > Servers > DC1, MG > Servers > DC2, Domain column |
| `8.3_teacher_site_link_replication.png` | 8.3 | Server Manager (DC1, domain) behind; Inter-Site Transports > IP: DEFAULTIPSITELINK, description "Replication between SB & MG", cost 100, interval 180 |
| `8.4a_teacher_DNS_zone_transfers_tab.png` | 8.4 | Zone Properties > Zone Transfers: allow, only to servers on the Name Servers tab |
| `8.4b_teacher_DNS_name_servers_tab.png` | 8.4 | Zone Properties > Name Servers: dc1, dc2 and the secondary server (named sb-dns-1 at 192.168.2.4 in the demo; ours is SB-DNS-2) |
| `8.4c_other_student_secondary_zone_synchronised.jpeg` | 8.4 | DNS Manager with DC1 and the secondary server both connected; the secondary zone populated (SOA, NS, A records) |
| `8.5_teacher_DFS_Rep1_memberships.png` | 8.5 | DFS Management: namespace \\domain\Shares with two targets; Rep1 (domain) Memberships: C:\Share1 SB-DNS-1, C:\Share2 SB-FS2, replicated folder Share1 |
| `8.6a_teacher_event_12325_quota.png` | 8.6 | Event Viewer, SRMSVC 12325: 85% quota threshold on C:\share4 on SB-FS2 |
| `8.6b_teacher_event_8215_file_screen.png` | 8.6 | Event Viewer, SRMSVC 8215: test.txt in file group FG-1 not permitted |
| `8.8a_teacher_GPO_software_installation_avast.png` | 8.8 | GPO Anti-Virus-End-Devices: Software installation, Avast MicroInstaller 2.1, Assigned, source \\DC1.domain\Shared Software |
| `8.8b_teacher_client_installing_managed_software.png` | 8.8 | Client boot: "Installing managed software Avast MicroInstaller - UNREGISTERED - Wrapped using MSI Wrapper from www.exemsi.com" |
| `8.9a_teacher_WSUS_approval_progress.png` | 8.9 | Update Services on SB-FS2: All Updates (760), Approval Progress completed without errors |
| `8.9b_teacher_GPO_windows_update_settings.png` | 8.9 | GPO "Windows Update" at the domain: Windows Components > Windows Update settings Enabled (configure automatic updates, intranet update service location, detection frequency, immediate installation, recommended updates, no auto-restart) |
| `8.10_teacher_ubuntu_realm_list.png` | 8.10 | Ubuntu terminal: realm list for the domain (kerberos-member, active-directory, sssd, required packages, login formats) |

Not in the template: 8.7 has no example image (instruction only).
