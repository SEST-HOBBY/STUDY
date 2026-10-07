# ICTNWK529 / ICTNWK546, Complex Cluster, Assessment Task 2 of 3: Network Infrastructure Proposal (HelpYou Mortgage)

Units: ICTNWK529 Install and manage complex ICT networks; ICTNWK546 Manage network security.
Assessment type: Portfolio. Case study: HelpYou Mortgage, Brisbane head office (two floors) plus a Cairns branch.
Agreed design scope: design only, one ISP per site, two links between the two core switches, copper cabling drawn in Packet Tracer; no CLI configuration.

## File register and provenance

| File | Folder | Provenance | Notes |
|---|---|---|---|
| `ICTNWK529_546_AT2_MC_TQM_v2.docx` | 00_assessment_documents | TAFE Queensland marking criteria (created 2020, revised 2023) | 20 numbered criteria across Parts 1 to 5. Markdown copy in `04_extracted_views/Marking_Criteria_MC_TQM_v2.md` |
| `HelpYou_1st_Floor_Plan.vsd` | 01_supplied_reference | TAFE reference asset (Visio, authored by TAFE staff in 2020) | First-floor plan with HR/IT/Marketing/CS/Manager/Admin cubes, two executive rooms and the server room. PDF and PNG in `04_extracted_views/` |
| `Helpyou_Network_Topology.pkt` | 02_student_work/packet_tracer | My Packet Tracer file (PT 8.2.1), earlier working version | 31 devices, 27 links: CORE 1 / CORE 2, four servers, 21 department PCs, an ASA icon labelled FortiGate, ISP cloud and a DMZ switch. One core-to-core link only; firewall not yet linked to the cores; DMZ switch unconnected |
| `FLOOR_PLAN_FINAL.pkt` | 02_student_work/packet_tracer | My Packet Tracer file (PT 8.2.1), latest version | 33 devices, 32 links, two-floor floor-plan background embedded. This is the file behind the screenshot |
| `FINAL_FLOOR_PLAN.png` | 02_student_work/screenshots | My screenshot of the physical view in `FLOOR_PLAN_FINAL.pkt` | Used as Figure 1 in the report |
| `Roly_Lobley_ICTNWK529_546_AT2_Proposal_Report.docx` | 03_report | Earlier draft produced with AI assistance on 7 Oct 2026 | Superseded. Third-person wording, two INSERT placeholders. Kept for comparison; markdown copy in `04_extracted_views/Proposal_Report_draft_2026-10-07.md` |
| `Roly_Lobley_ICTNWK529_546_AT2_Network_Infrastructure_Proposal.docx` | 03_report | Rebuilt report, first person | Current version to submit after filling in the student number and due date on the cover |

### Derived views (`04_extracted_views/`)
* `packet_tracer_xml/*.xml`: both `.pkt` files decrypted to Packet Tracer XML so the device and link lists can be read without opening Packet Tracer.
* `FLOOR_PLAN_FINAL_embedded_background.jpg`: the two-floor background image embedded in `FLOOR_PLAN_FINAL.pkt`.
* `HelpYou_1st_Floor_Plan.pdf/.png`: the supplied Visio plan rendered.

### Tools and analysis (`05_analysis/`)
* `tools/pktdecrypt.py`: decrypts a `.pkt`/`.pka` (PT 7.x and 8.x) to XML. Needs the `twofish` Python package (the C extension; on Python 3.12+ patch its `import imp` line as the tool's comments describe) and is run as `python3 -I pktdecrypt.py in.pkt out.xml`. Scheme as published by the pka2xml project: reversed XOR stage, Twofish-EAX with a 16-byte key of 0x89 and IV of 0x10, XOR stage, zlib.
* `checks/`: the arithmetic, reference-link and consistency checks that were run before the rebuild, plus the consolidated corrections used by the rebuilt report.
* `figures/`: the logical topology diagram, rack diagram and the full-size render of the physical layout, with the scripts that drew them.

## What is NOT in this collection yet (needed to verify the report against its sources)
1. `ICTNWK529_546_AT2_PE_TQM_v2.docx`, the Portfolio of Evidence with the HelpYou case study and task instructions (cited as [P1]).
2. `ICTNWK529_546_AT2_Student Handout 2_TQB_v1`, the customer interview answers (cited as [P2]); every headcount, floor placement and server bandwidth figure in the report comes from this.
3. `ICTNWK529_546_AT2_Template_SH_TQM_v2`, the report template (cited with the marking criteria as [P3]).
4. The four tutorial recordings (Section 1 gap analysis, Section 6 investment, Section 7 bandwidth, Session 6 sections 4 to 7). Not needed in the repository; they are teaching examples for other case studies.
5. Any assessor feedback or a submission receipt for an earlier attempt.

Until items 1 to 3 are added under `00_assessment_documents/`, the case-study facts in the report are carried over from the earlier draft and have not been re-checked against the source documents.
