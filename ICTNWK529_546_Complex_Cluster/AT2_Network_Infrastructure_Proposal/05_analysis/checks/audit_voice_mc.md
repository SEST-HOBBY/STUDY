# Audit of the draft report: voice, placeholders, disclaimers, AI tells and marking-criteria coverage

Audited file: /tmp/claude-0/-home-user-STUDY/f8a3790f-8c1d-5a3f-8f9c-d2abf23b0604/scratchpad/extract/report.md (607 lines)
Marking criteria: /tmp/claude-0/-home-user-STUDY/f8a3790f-8c1d-5a3f-8f9c-d2abf23b0604/scratchpad/extract/mc.md (20 criteria: Part 1 x5, Part 2 x4, Part 3 x5, Part 4 x3, Part 5 x3)

Line numbers (L##) refer to report.md. Quotes are given as plain text with the markdown backslash escapes removed (the file writes `\[P1\]` and `\$`).

Tags used in sections C and D:
- DELETE = sentence or clause exists only to say what something is not, or is an author/assessor-facing note; remove.
- REWRITE = carries a real design point but is framed as "X, not Y"; keep the point, state it positively, in first person where natural.
- CAVEAT = a natural caveat that may stay once per topic, shortened.

---

## A. Third-person references to the student

| L | Quote | Verdict |
|---|-------|---------|
| 5 | "Prepared by Roly Lobley" | KEEP. The one permitted use (cover block; repeat in the page header only). |
| 9 | "Student number: [insert]" | KEEP the label as a cover field; becomes "Student number: ________". Not a third-person reference. |
| 130 | "INSERT: your final Packet Tracer Logical View screenshot. Include VLANs/subnets, link-capacity notes, firewall/IPS, DMZ, domain controllers, monitoring and the two core links. Use the service roles below as the diagram labels. No CLI configuration is required for this design-only submission." | DELETE. Author-facing instruction ("your") plus "design-only submission". Replace with prose introducing Figure 2. |
| 157 | "The existing student-created overlay is retained below." | REWRITE as "My Packet Tracer physical view (Figure 1) shows..." |
| 157 | "... provide the detailed proposed deployment. [P4]" | DELETE the [P4] citation. |
| 159 | img alt text: "Student-created HelpYou floor plan, duplicated vertically for two floors, with representative Packet Tracer devices and visible connections." | REWRITE alt text: "Figure 1. My Packet Tracer physical view of the two Brisbane floors." |
| 161 | "Figure 1. Existing two-floor Packet Tracer overlay supplied by Roly Lobley. [P4]" | REWRITE caption: "Figure 1. My Packet Tracer physical view of the two Brisbane floors." Drop [P4]. |
| 267 | "Packet Tracer 2960 icons may represent the proposed switches in a design-only drawing, but their simulated interfaces are not evidence of the commercial models or the proposed speeds. The diagram needs a short model-substitution note." | DELETE. "design-only drawing" plus an author note. If a substitution note is wanted, put one clause in the Figure 1 caption ("2960 icons stand in for the C1300 models"). |
| 459 | "These are proposed deployment activities for the business, not additional configuration tasks required from the student for the design-only Packet Tracer submission." | DELETE the whole sentence ("required from the student", "design-only Packet Tracer submission"). |
| 487 | "[P4] Lobley, R. FINAL FLOOR PLAN.png. Supplied student-created two-floor Packet Tracer overlay." | DELETE the bibliography entry (brief: drop [P4]). |

Excluded as not references to the student: L249 "guest addresses are supplied by the firewall"; L483 "ICTNWK529_546_AT2_Student Handout 2_TQB_v1" (the supplied document's own title, keep); L1-3 unit and task header lines.

Voice check: the draft contains no first-person pronoun at all (0 x "I ...", 0 x "my"). The only "you/your" is the author note at L130. The CIO is never addressed directly. HelpYou is named 7 times; "the business" 4 times; "the client" once.

---

## B. Placeholders

| # | L | Text | What is missing |
|---|---|------|-----------------|
| 1 | 9 | "Student number: [insert]" | Cover field. Becomes a plain blank "Student number: ________" (allowed by the brief). |
| 2 | 9 | "Assessment due date: [insert]" | Cover field. Becomes "Assessment due date: ________" (allowed by the brief). |
| 3 | 130 | "INSERT: your final Packet Tracer Logical View screenshot. Include VLANs/subnets, link-capacity notes, firewall/IPS, DMZ, domain controllers, monitoring and the two core links. Use the service roles below as the diagram labels. No CLI configuration is required for this design-only submission." | Figure 2, the logical topology diagram, is absent. Section 2 must introduce and explain Figure 2. |
| 4 | 179 | "INSERT: Packet Tracer Physical View rack screenshot(s), showing the actual equipment arrangement and visible connections. Use normal device names; do not relabel an unrelated server icon as a working UPS. Rack tables above remain as the written arrangement explanation." | Figure 3 (rack diagram) and Figure 4 (Packet Tracer rack view, if available) are absent. Section 4 must introduce and explain them. |

No "TBC", "TBD", "TODO" or "???" found.

Related artefacts that are not placeholders but must be fixed in the rebuild:
- Contents (L23-65) carries static page numbers copied from the .docx; regenerate.
- Six duplicate page-break headings: L92 "# 1. Gap Analysis (continued)", L132 "# 2. Logical Topology (continued)", L216 "# 5. IP Scheme (continued)", L367 "## 6.9 Total Costings (continued)", L436 "# 7. Traffic Bandwidth Prediction (continued)", L461 "## 7.3 Five-year capacity (continued)". Remove; the gap-analysis organiser (L83-105) and the costing tables are each split in two by these.
- Unnumbered "## Proposal basis" section (L67-69) sits between Contents and section 1 and is not in the required structure.

---

## C. Defensive disclaimers and meta sentences (quoted in full)

Count: 80 occurrences of ", not / ; not / is not / are not / does not / do not / rather than" in the draft. Every sentence listed below was read in context; the tag says what to do with it.

### Executive summary and preamble (L11-69)

1. L15 [CAVEAT, shorten] "A single firewall and internet service remain recognised points of failure at each site."
2. L15 [DELETE] "These are design choices, not claims of continuous availability."
3. L17 [CAVEAT, one price caveat for the whole report] "Published reference prices and proposal allowances are separated in section 6.9; supplier configuration and availability must be confirmed before purchase."
4. L19 [DELETE] "The following report contains the proposed design and calculations. It does not claim that the network has been configured, tested or installed."
5. L69 [DELETE the section; fold source attribution into the executive summary] "Existing conditions and business requirements are drawn from the HelpYou case study [P1]. Departmental location, headcount and bandwidth inputs come from the customer interview handout [P2]. Equipment selections, recovery targets, subnet allocations and workload forecasts are proposed engineering decisions. They are not reported measurements or additional customer instructions. Vendor sources [R1-R30] support the selected capabilities and reference prices."

### Section 1 Gap Analysis

6. L75 [DELETE] "These are separate stages, not competing totals."
7. L79 [REWRITE] "These existing assets should be assessed for reuse rather than described as absent."
8. L79 [CAVEAT] "The precise existing VLAN, firewall and disk-RAID configurations are not documented."
9. L88 (table cell) [REWRITE] "Stable access to cloud services and branch resources; the residual risk of one service remains explicit."
10. L104 (table cell) [REWRITE] "Company-hosted email with security and recovery arrangements; cloud video does not replace this requirement."
11. L107 [DELETE] "Middle-column actions are proposed responses, not claims that these controls already exist."

### Section 2 Logical Topology

12. L111 [REWRITE] "Access switches serve multiple departmental VLANs; a separate switch per department is not necessary."
13. L111 [DELETE] "IP addresses in section 5 are proposed labels and documentation, not Packet Tracer configuration."
14. L116 (table cell) [REWRITE] "Two proposed 10 Gbps core interconnections; implement as the supported stack design, not an unmanaged loop."
15. L119 (table cell) [REWRITE] "Separate firewall zone; the DMZ is not an unfiltered extension of the internal network."
16. L120 (table cell) [REWRITE] "One branch internet service, not a second Brisbane ISP. Only required branch-to-server flows are permitted."
17. L126 [DELETE the clause after the semicolon] "The firewall provides IPS/IDS functionality at the perimeter; this does not claim inspection of every internal LAN flow."
18. L128 [REWRITE first sentence as an implementation step; DELETE second] "The production implementation must validate supported dual-link stacking and loop prevention. A drawing of two cables alone is not an operational failover test."
19. L138 (table cell) [REWRITE] "DC2 on the other host; AD/DNS replication and DHCP failover are proposed."
20. L139 (table cell) [REWRITE] "Independently running second domain-service instance, not only a stopped VM copy."
21. L145 (table cell) [REWRITE] "Controller backup; NAS is a backup target, not single shared storage for live VMs."
22. L147 [REWRITE] "Recovery requires controlled activation and verification; it is not automatic clustered failover."
23. L147 [CAVEAT] "Both hosts are sized to run the essential services after one host fails, subject to workload acceptance tests."
24. L149 [CAVEAT] "RAID protects against some disk failures but is not the backup strategy."
25. L149 [CAVEAT] "Final retention and recovery targets require CIO approval."
26. L151-153 [REWRITE the whole subsection into two plain sentences of risk statement; rename the heading] "## 2.3 Limits of the simplified design" / "A single head-office firewall, ISP service and PBX remain single points of failure. Two core links do not remove those risks, and the two-floor building remains a shared site risk. The proposal includes saved device configurations, supplier replacement arrangements, tested recovery and off-site copies rather than claiming zero downtime. A future requirement for uninterrupted internet or telephony would require further investment."

### Section 3 Physical Topology

27. L157 [DELETE the clause after the semicolon] "It presents the two floors and representative device connections; it is not a measured cable-route drawing."
28. L157 [DELETE] "The final logical diagram and quantities in section 6 provide the detailed proposed deployment."
29. L163 [DELETE] "Existing room labels on a reused background do not override this departmental allocation."

### Section 4 Racks Diagram

30. L167 [REWRITE; keep only the dependency on measurement] "Final rack-unit positions depend on the measured dimensions and usable height; the table is a placement design, not an assertion about existing rack dimensions."
31. L177 [DELETE, or keep as the one caveat for the section] "Locating the hosts on different floors reduces some localised risks but does not create a second disaster-recovery site."
32. L179 [DELETE] "Use normal device names; do not relabel an unrelated server icon as a working UPS. Rack tables above remain as the written arrangement explanation."
33. L183 [REWRITE] "The forecast is 270 departmental end devices; it is not automatically 270 PCs plus another 108 phones."
34. L183 [DELETE the annotation inside the citation] "[P1, P2; proposed port arithmetic]"
35. L185 [DELETE] "Branch growth beyond the stated eight staff is not supplied in the case study and is not represented as a confirmed requirement."

### Section 5 IP Scheme

36. L189 [REWRITE] "Departmental host requirements come from the interview; supporting-zone sizes are design allowances."
37. L212 [DELETE] "Voice and Wi-Fi capacity are supporting address pools; adding their pool sizes to 270 would double-count devices that move from departmental addressing to those services."
38. L214 [REWRITE] "Public addressing is assigned by the ISP, not invented for this proposal."
39. L234 (table cell) [REWRITE, e.g. "n/a (firewall interface)"] "Not a host gateway"

### Section 6 Investment of Hardware and Software

40. L255 [DELETE] "All recommendations below are proposed selections, not existing case-study assets."
41. L255 [DELETE or merge into one sentence] "Section 6.9 distinguishes published reference prices from configured-system and service allowances. Price-source references link to the specific product or service in the bibliography."
42. L259 [REWRITE] "Twelve physical ports must not be counted as fourteen because combo connectors share ports."
43. L261 [DELETE] "Failure of the entire stack or its shared environment remains a residual risk."
44. L265 [REWRITE] "PoE load is assessed from the actual connected devices, not merely the total number of ports."
45. L267 [DELETE] "Packet Tracer 2960 icons may represent the proposed switches in a design-only drawing, but their simulated interfaces are not evidence of the commercial models or the proposed speeds. The diagram needs a short model-substitution note."
46. L269 [CAVEAT] "Its reference listing is $1,578; allow $1,750 pending tax, shipping and quote confirmation."
47. L273 [CAVEAT, shorten to one clause] "The reference FG-70G-BDL-950-12 listing shows $2,038 and is out of stock. The budget uses $2,250 per site as a GST-inclusive procurement allowance, pending tax, stock and configuration confirmation."
48. L275 [REWRITE] "Required throughput must be checked with the selected security inspection enabled, not by the headline basic-firewall forwarding figure alone."
49. L275 [CAVEAT] "A $2,500 setup and $500 annual MFA allowance covers the remote-access authentication solution, subject to the final user count and supplier selection."
50. L279 [DELETE] "This separates desktop entitlement from server protection."
51. L281 [DELETE both; replace with "I have used the ASD Essential Eight as the baseline for these controls [R27]."] "Purchasing antivirus alone does not establish compliance with an industry framework. ASD Essential Eight is used as a baseline for those controls, not as a certification claim."
52. L285 [DELETE] "This is a proposed configured specification, not the basic web-store configuration."
53. L285 [DELETE the annotation inside the citation] "[R7; proposed configuration]"
54. L287 [CAVEAT] "The initial storage planning envelope is 4 TB for the total live service dataset, including mail and business files; this is an allowance until a data inventory is taken."
55. L287 [DELETE] "It does not require twice the complete live dataset."
56. L287 [REWRITE] "Growth beyond the tested storage/CPU envelope triggers an upgrade rather than an unconditional five-year capacity claim."
57. L298 [DELETE] "Virtualisation does not itself fix poorly performing application queries."
58. L302 [CAVEAT] "OEM/stacking entitlement, CAL type and replica use must be confirmed in the supplier licence statement before purchase."
59. L304 [REWRITE] "The HR database engine and application licence are not identified in the case study. An $8,000 compatibility/licence allowance and $2,000 annual maintenance allowance are included, rather than claiming that a particular database edition is sufficient or free."
60. L308 [DELETE] "NAS snapshots, versioned backups and offline copies have different purposes."
61. L312 [REWRITE or drop] "Phones do not need gigabit throughput to carry voice."
62. L314 [REWRITE] "These are USB/BYOD meeting rooms, not a separately licensed Teams Rooms deployment."
63. L314 [REWRITE] "Teams Essentials is for meetings and does not include the external PSTN service in this proposal."
64. L316 [REWRITE] "Lower bills are an objective, not a quantified saving: no existing call-cost baseline was supplied."
65. L320 [DELETE the clause after the semicolon] "These have separate operational roles; a bandwidth monitor is not assumed to be a full security-event platform."
66. L326 [DELETE] "This is the proposed implementation of the client's need-to-know and cross-platform requirements."
67. L328 [REWRITE] "This retains company-hosted email rather than silently replacing it with a hosted mailbox subscription."
68. L332 [REWRITE; merge with the earlier "subject to a coverage survey" so the survey is mentioned once] "A coverage survey, rather than the floor-plan picture alone, determines final AP positions."
69. L336 [REWRITE] "P = published reference price; A = proposal allowance, not a supplier quotation."
70. L336 [CAVEAT, shorten to one sentence] "Retail references are dated 7 October 2026; delivery, stock, licensing channel and final tax treatment are confirmed at procurement. Software subscriptions published ex-GST are multiplied by 1.10. The listed ISP tariff is provisionally treated as GST-inclusive until its service summary confirms the tax basis."
71. L365 [REWRITE] "The endpoint fund is a ceiling for replacing or upgrading the 78 current user workstations and necessary room peripherals; it is not a verified quotation for 78 identical PCs."
72. L365 [DELETE] "These allowances prevent mandatory supporting costs from being omitted or hidden in an unsupported round total."
73. L383 (table cell) [REWRITE, e.g. "From year 2; year 1 is in the bundle"] "Annual allowance; not charged twice in year 1"
74. L394 [REWRITE] "It is a baseline, not a fixed-price guarantee: it excludes inflation, electricity, additional future employees, storage growth beyond the allowances and replacement equipment."
75. L398 [REWRITE] "This is a 1000 Mbps download / 400 Mbps upload access tier, not symmetric 1 Gbps dedicated fibre."
76. L400 [REWRITE] "There are no dual Brisbane ISPs and no mobile backup counted in the design."
77. L400 [DELETE] "An included backup feature in a provider plan is not treated as a deployed second path."
78. L400 [CAVEAT] "If either site's single service fails, internet-dependent calls and branch access may be interrupted until restoration."

### Section 7 Traffic Bandwidth Prediction and Expected Performance

79. L406 [DELETE] "The case study does not provide measured CPU load, disk latency or application response times."
80. L408 [DELETE] "Those values are retained as planning baselines, not represented as measurements from installed servers."
81. L408 [REWRITE] "Although the handout lists IT Admin only for certain infrastructure roles, normal clients still require their authorised DHCP/DNS/domain functions; administrative control and service consumption are different permissions."
82. L410 [REWRITE first; DELETE second] "The 10% factor and rounding are proposal assumptions. The source documents do not prescribe a single mandatory multiplier."
83. L419 [REWRITE] "Shared infrastructure uses staff growth as a workload proxy, not as an asserted packet-rate relationship."
84. L419 [REWRITE] "Cairns access and changes in application behaviour are then validated in the pilot rather than silently added to head-office demand."
85. L434 [REWRITE] "A 1,000 Mbps service benchmark is a proposed throughput-capacity target, not a configured speed limit or dedicated bandwidth reservation."
86. L434 [DELETE the annotation inside the citation] "[P2; calculations above]"
87. L438 [REWRITE] "This deliberately assumes that all listed services could peak together; it is a conservative LAN planning envelope, not measured simultaneous utilisation."
88. L440 [REWRITE] "Department-specific growth avoids understating the six-fold growth in Customer Service while applying the same arbitrary multiplier to every service."
89. L444 [REWRITE] "This is an example workload assumption, not a measured daily change rate."
90. L446 [DELETE] "These are conservative design allowances to test, not vendor performance guarantees."
91. L446 [REWRITE] "Internal file-server traffic is not added wholesale to internet demand because most of it remains within the LAN."
92. L450 [REWRITE] "Department subnet capacity, switch ports, software licences and storage are reviewed together, not treated as interchangeable measures."
93. L459 [DELETE] "These are proposed deployment activities for the business, not additional configuration tasks required from the student for the design-only Packet Tracer submission."
94. L463 [REWRITE] "Investigate application latency and error rates as well as utilisation; these thresholds are operational targets to agree with the CIO, not observations of the current system."
95. L465 [DELETE the annotation inside the citation] "[R27; proposed schedule]"
96. L467 [DELETE] "Record actual results rather than stating that a plan or diagram has already passed testing."
97. L469 [REWRITE] "The five-year recommendation therefore includes review and upgrade actions instead of guaranteeing unchanged equipment will meet every future workload."
98. L475 [REWRITE; drop the clause after the semicolon] "Successful installation, testing and acceptance must then be documented; this report does not claim they have already occurred."

### Section 8 Bibliography

99. L479 [DELETE] "Assessment sources retain the supplied titles."
100. L479 [DELETE] "Product prices are reference observations, not binding quotations."
101. L479 [KEEP, shortened] "In-text references [P#] identify supplied case material; [R#] identify external research."

---

## D. AI-sounding tells and clichés

1. Negation-contrast construction "X, not Y" / "X; it is not Y" / "does not claim": 80 occurrences across the draft (every instance is itemised in section C). This is the single strongest tell; the writer constantly argues with an imagined objector instead of stating the design.
2. "rather than" x12: L15, 79, 90, 153, 287, 304, 312, 328, 332, 419, 467, 469.
3. Hedge-stacking vocabulary: "proposed/proposal" 41 times (L13, 17, 19, 67, 69, 83, 94, 107, 111 x2, 113, 116, 126, 138, 147, 149, 153, 157, 167, 183, 189, 214, 255, 267 x2, 269, 285 x2, 298, 314, 322, 326, 328, 336, 410, 434, 459, 463, 465, 473, 475); "allowance" 23; "subject to" 7 (L147, 275, 285, 292, 293, 322, 332); "pending" 4 (L269, 273, 316, 400); "must be confirmed / validated / checked" (L17, 128, 275, 302, 308, 316); "remain(s)" 14; "retain" 15; "controlled" 10; "documented" 6; "proposal allowance" x2 (L17, 336).
4. No first person and no direct address. Zero "I" / "my"; the only "you/your" is the author note at L130. Product sections open with bare imperatives in a specification/recipe register: "Select two Cisco Catalyst C1300-12XS..." (L259), "Select six Cisco C1300-48P-4X..." (L265), "Select one FortiGate 70G..." (L273), "Select Microsoft Defender..." (L279), "Propose central alerts..." (L279), "Select two Dell PowerEdge R360..." (L285), "Select a Synology RS2423RP+..." (L308), "Validate the selected disks..." (L308), "Select one Grandstream UCM6302..." (L312), "Provide Microsoft Teams Essentials..." (L314), "Add three Logitech MeetUp 2..." (L314), "Allow ten simultaneous external calls..." (L316), "Use Zabbix on SRV-MON..." / "Use Wazuh on SRV-LOG..." (L320), "Synchronise device time..." / "Propose 90 days..." (L322), "Retain Windows file services..." / "Keep HR-DB separate..." (L326), "Use Ubuntu Server LTS..." / "Validate account integration..." (L328), "Provide six TP-Link EAP650 APs..." / "Use a local controller..." (L332), "Check the site address..." (L398), "Schedule backups..." (L444), "Review high-priority..." / "Schedule operating-system..." / "Conduct a wider recovery rehearsal..." (L465), "Measure application response..." / "Record actual results..." (L467), "Use departmental DHCP reservations..." (L251), "For departmental /26 networks, reserve..." (L249).
5. Consultant jargon and nominalisations: "capacity-limited network" and "segmented access, two core switches, centralised services, protected backups and managed communications" (L13); "recognised points of failure" (L15); "Proposal basis" (L67); "stated support/restoration arrangement" (L88); "residual risk" (L88, 261); "explicit access policy" (L90); "traceable authorised access" (L99); "maintained security baseline" (L101); "costed alternative" (L102); "controlled activation and verification" (L147); "procurement allowance" (L273); "storage planning envelope" (L287); "unconditional five-year capacity claim" (L287); "degraded-operation test" (L298); "unsupported round total" (L365); "planning baselines" (L408); "workload proxy" and "asserted packet-rate relationship" (L419); "throughput-capacity target" (L434); "conservative LAN planning envelope" (L438); "right-sized memory" (L450); "recovery-capable host pair" and "distinct forms of service resilience" (L473).
6. Emphatic adverbs that argue with the reader: "expressly absent" (L79), "remains explicit" (L88), "explicitly labels" (L408), "deliberately assumes" (L438), "silently" (L328, 419), "wholesale" (L446), "merely" (L265), "headline" (L275), "automatically" (L183), "arbitrary" (L440), "unconditional" (L287).
7. Rubric echo copied from the marking criteria: column headers "Current system - left", "Changes required - middle", "Business need / proposed system - right" (L83, 94); "respecting privacy, IP and organisational procedures" (L105); "This is the proposed implementation of the client's need-to-know and cross-platform requirements." (L326); "design-only submission" (L130, 459).
8. Semicolon density: 101 semicolons on 74 lines, often chaining two unrelated clauses (L126, 147, 149, 153, 157, 167, 177, 183, 212, 249, 265, 298, 308, 320, 332, 336, 365, 394, 406, 434, 438, 463).
9. Meta section-pointer sentences instead of content: "Published reference prices and proposal allowances are separated in section 6.9" (L17); "The final logical diagram and quantities in section 6 provide the detailed proposed deployment." (L157); "Rack tables above remain as the written arrangement explanation." (L179); "Section 6.9 distinguishes published reference prices from configured-system and service allowances. Price-source references link to the specific product or service in the bibliography." (L255); "Port arithmetic is in section 4.1." (L265).
10. Non-standard annotated citation brackets: "[P1, P2; proposed port arithmetic]" (L183), "[R7; proposed configuration]" (L285), "[P2; calculations above]" (L434), "[R27; proposed schedule]" (L465). Normalise to plain [P1, P2], [R7], [P2], [R27].
11. Self-deprecating or defensive headings: "## Proposal basis" (L67), "## 2.3 Limits of the simplified design" (L151).
12. Balanced triads and noun-stack lists: "configured, tested or installed" (L19), "deletion, corruption and site loss" (L149), "Inventory devices/data; confirm the case-study assumptions, site eligibility, permissions, service dependencies and supplier quotes." (L454), "authorisation, VPN, two-core-path behaviour, recovery, calls/video and backup restoration" (L457).
13. Repeated sourcing tags in place of plain statements: "case study" x9, "interview" x9, "handout" x6, "the business" x4, "the client" x1, against "HelpYou" x7 and "you" x0. A student writing to the CIO would say "you told us" / "HelpYou needs".
14. Colon-led contrast sentences: "Lower bills are an objective, not a quantified saving: no existing call-cost baseline was supplied." (L316); "It is a baseline, not a fixed-price guarantee: it excludes..." (L394).
15. Connective tics: "respectively" (L265), "therefore" (L183, 469), "approximately" (L285, 444), "for example" (L440). Minor on their own; they add to the register.
16. The executive summary (L13-19) reads as an abstract: dense noun phrases, no sentence a CIO would hear from a staff member, and it ends on a disclaimer.
17. Heavy hyphenated compound modifiers: "design-only", "right-sized", "degraded-operation", "throughput-capacity", "recovery-capable", "address-qualified", "site-specific", "GST-inclusive", "application-consistent", "capacity-limited", "need-to-know", "two-core-path".
18. Em dashes: none (good). En dashes: none.

---

## E. Marking criteria mapping (20 criteria)

Status key: FULL = fully met in the draft text as it stands; PART = partly met; MISSING = not met (the two INSERT placeholders mean the logical diagram and rack diagram are currently absent).

| # | Criterion (mc.md) | Draft section(s) / lines | Status | Note |
|---|-------------------|--------------------------|--------|------|
| 1.1 | Compare and contrast graphical organiser illustrating differences between current and desired future infrastructure | 1.2 three-column tables L83-90 and L94-105; supporting prose 1.1 L73-79 | FULL | One organiser is split into two tables by a page break with a duplicate "# 1. Gap Analysis (continued)" heading (L92); merge into one table in the rebuild. |
| 1.2 | Comparison contains both qualitative and quantitative perspectives | Same tables | FULL | Quantitative: 40/70/8 staff, 108 staff, 270 devices, 100 Mbps, 24-port, 1 Gbps, 96/120/216 cable runs, four months, $500,000. Qualitative: slow responses, unreliable ADSL, visitor connection problems, no backup, local file saving, expensive international calls. The word "quantitative" never appears; one introductory sentence could say the organiser covers both. |
| 1.3 | Current conditions summary on the left-hand side | Left column L83/L94 | FULL | Header literally reads "Current system - left" (rubric echo); rename to "Current infrastructure". |
| 1.4 | Summary of business needs (future infrastructure) on the right-hand side | Right column L83/L94 | FULL | Header reads "Business need / proposed system - right"; rename to "Future infrastructure HelpYou needs". |
| 1.5 | Summary of changes needed in the middle | Middle column L83/L94 | FULL | Header reads "Changes required - middle"; rename to "Changes required". Delete the L107 disclaimer under the table. |
| 2.1 | Logical topology diagram with VLANs, IP subnet/prefix, bandwidth of connections; firewall, IPS/IDS, SNMP management server, AD DS DCs, DMZ; redundancy in infrastructure and servers | Section 2 L109-153: connection table L113-120, 2.1 L122-128, 2.2 table L136-145; VLAN table in section 5 L191-210 | MISSING | The diagram itself is the INSERT placeholder at L130. The supporting text already names every required element: VLANs/subnets (sec 5), link capacities (L115-118), FW-HQ with IPS/IDS (L126), Zabbix SNMPv3 server (L144, L320), DC1/DC2 (L138-139), DMZ with SMTP-GW (L119, L126), two core links, two hosts with replicas, NAS (L116-118, L147). Figure 2 must show all of these with VLAN IDs, subnet/prefix labels, link speeds and the two core links, and section 2 must introduce it. |
| 2.2 | Packet Tracer screenshot of the physical topology showing physical layout of devices, servers, end devices and cabling | Section 3 L155-163; Figure 1 image L159, caption L161 | PART | The screenshot is present (the student's Packet Tracer physical view, 496x651 px). The prose does not walk the CIO through it (server room and rack positions, three access switches per floor, APs, patch panels, cable runs to desks, Cairns), the caption credits it in third person, and L157 disclaims it as "not a measured cable-route drawing". Check legibility of labels and cables at that resolution; export larger if possible. |
| 2.3 | Diagram of the racks showing physical arrangement of network devices and servers | Section 4 rack table L169-175; prose L167, L177 | MISSING | The diagram is the INSERT placeholder at L179; the table is a written arrangement only. Figure 3 (rack elevation with RU positions for the floor-1 network rack, floor-1 server space, the two floor-2 racks and the Cairns cabinet) and Figure 4 (Packet Tracer rack view, if available) are required; the table can stay as the legend. |
| 2.4 | IP address arrangement per VLAN and static IPs for servers and end devices needing static IP | Section 5 VLAN table L191-210, prose L212-214; 5.1 static table L220-245; 5.2 DHCP L247-251 | FULL | Tidy the two odd gateway cells ("Uses transit route" L233, "Not a host gateway" L234). Printers are handled as DHCP reservations (L251), which is acceptable. Delete the L212 double-count sentence and the L214 "not invented" clause. |
| 3.1 | Hardware and software suggestions give make and model and where deployed | 6.1 L259, 6.2 L265-269, 6.3 L273, 6.4 L279, 6.5 L285-308, 6.6 L312-316, 6.7 L320, 6.8 L326-332, 6.10 L398-400 | FULL | Models and placement are all stated (C1300-12XS x2 Brisbane core; C1300-48P-4X x6, three per floor; C1300-24P-4X Cairns; C1300-24T-4X DMZ; FortiGate 70G at each site; Dell R360 one per floor; Synology RS2423RP+ floor-2 rack; UCM6302 + 82 GRP2612P; MeetUp 2 x3, two Brisbane one Cairns; EAP650 x7; Defender, Teams Essentials, Windows Server 2025, Zabbix, Wazuh, Ubuntu). UPS has no make/model (allowance L350) and endpoints are a fund; neither is in the required coverage list. |
| 3.2 | Evaluate and verify against industry best practice and briefly explain why each product was selected | Scattered: L128/L261 stacking, L265 PoE and uplinks, L273-275 NGFW IPS/VPN, L281 Essential Eight, L285/L147 RAID 10 and replica, L320 SNMPv3, L332 guest isolation | PART | The phrase "best practice" never appears and the only named standard (ASD Essential Eight) is introduced defensively. No stated reason beyond price for: Synology NAS, Logitech MeetUp 2, Teams Essentials, Dell R360 (spec only), Grandstream PBX/phones (only the 100 Mbps port note), ISP plan (speeds only). Rebuild: one or two first-person sentences per product tying it to a named practice (hierarchical collapsed-core/access design and stacking; NGFW with IPS at the perimeter and a DMZ for public-facing services; Essential Eight for endpoint controls; 3-2-1 backup rule for NAS plus off-site copies; two domain controllers; SNMPv3 over v2c; separate voice VLAN and PoE; enterprise Wi-Fi authentication with guest isolation; business-grade nbn with eSLA and static IP). |
| 3.3 | Price and website link for each product | Prices in 6.1-6.8 and 6.9 tables L338-363, L369-383; links in Bibliography [R2]-[R30] L493-607, keyed from the Basis column | FULL | Every suggested product has a price and an [R#] whose bibliography entry carries the URL. Links are not printed beside each product; keep the [R#] beside each price and the Basis column so the assessor can follow them. Allowance lines (UPS/rack fit-out, NAS disks, optics, cabling, labour, training, MFA, Cairns ISP, support) have no link by nature. |
| 3.4 | Coverage of core switches, access switches, firewall, anti-virus, servers, VoIP and videoconferencing, network monitoring, ISP plan | 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.10 | FULL | All eight categories have their own subsection. 6.8 (file sharing, email, wireless) is an extra. |
| 3.5 | Table of total costing with hardware and software cost and ongoing cost | 6.9 initial table L338-363, recurring table L369-383, summary L385-392 | FULL | Hardware and software rows are interleaved in one list; grouping under Hardware / Software and licences / Services and labour sub-totals would make the split explicit. Remove the "6.9 Total Costings (continued)" split heading (L367). Arithmetic is being checked by the verification agent. |
| 4.1 | Discussion that under the current infrastructure server performance is struggling | 1.1 L77-79; 7.1 L406 | FULL | Covers the Web server's memory and disk shortage, slow access to other servers, 100BaseT interfaces, and Web and Marketing peaking at the full 100 Mbps. Brief but adequate; keep the explanation in 7.1 in first person. Delete the L406 "case study does not provide" sentence. |
| 4.2 | Predict server bandwidth on expansion; table of current bandwidth, predicted future bandwidth, benchmark design | 7.1 method L410, growth-factor table L412-417; 7.2 table L423-432; worked examples L440; L438 totals | FULL | Table has current average, current peak, growth and allowance, five-year peak and service benchmark. The benchmark column is 1,000 for every row; explain once that the benchmark is the 1 Gbps per-server allocation inside the 10 Gbps host uplink. Remove the L434 disclaimer. |
| 4.3 | Describe the actions that make the upgraded IT sufficient for the next five years | 7.3 L448-469 (four-stage plan L452-457, review triggers L463, maintenance and testing schedule L465-467, expansion paths L469); 7.4 L473 | FULL | Content is there but hedged; delete L459, and strip the defensive clauses in L463, L467 and L469. |
| 5.1 | Formal report structure with a header | Header L1-9; executive summary L11-19; contents L21-65; numbered sections 1-8; conclusion 7.4; bibliography 8 | FULL | Remove the unnumbered "Proposal basis" section (L67-69) and the six "(continued)" duplicate headings; regenerate contents page numbers; put name and title in the running page header. |
| 5.2 | Header includes your name, the date, who the report is submitted to, and the topic | Name L5; date L7; submitted to L6; unit codes L1-2; "Assessment Task 2 of 3" L3 | PART | Name, date and recipient are present. The topic is only implied by the unit names; there is no report title. Add a title line such as "Network Infrastructure Proposal for HelpYou Mortgage". Student number and due date remain cover blanks. |
| 5.3 | Conclusion and relevant references | 7.4 L471-475; 8 L477-607 ([P1]-[P3], [R1]-[R30], all R entries with URLs) | FULL | Drop [P4] (L487) and its citations (L157, L161); delete the closing disclaimer in L475 and the two bibliography preamble disclaimers at L479. |

Tally: 15 FULL, 3 PART (2.2, 3.2, 5.2), 2 MISSING (2.1, 2.3).

---

## F. Summary counts

- Third-person references to the student: 10 occurrences on 8 lines (one permitted: L5 cover block).
- Placeholders: 4 (two cover blanks allowed; two INSERT figure placeholders, logical diagram and rack diagram).
- Defensive disclaimer / meta sentences: 101 items (approx. 45 DELETE, 42 REWRITE, 14 CAVEAT).
- "X, not Y" family: 80 occurrences; "rather than" 12; "proposed/proposal" 41; "allowance" 23; semicolons 101.
- First person: 0. Direct address to the CIO: 0.
- Marking criteria: 15 fully met, 3 partly met, 2 missing.
