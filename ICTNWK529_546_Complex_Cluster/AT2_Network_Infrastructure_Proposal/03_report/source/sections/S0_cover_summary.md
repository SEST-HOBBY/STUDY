ICTNWK529 Install and manage complex ICT networks

ICTNWK546 Manage network security

Complex Cluster \| Assessment Task 2 of 3

**HelpYou Mortgage Network Infrastructure Proposal**

Prepared by Roly Lobley

Submitted to: Chief Information Officer, HelpYou Mortgage

Date: 7 October 2026

Student number: ________

Assessment due date: ________

# Executive summary

HelpYou is expanding its Brisbane head office from 40 to 70 staff across two floors, with 35 people on each floor, and the eight staff in Cairns need to reach the same systems. HelpYou's five-year estimates take the head office to 108 staff and 270 end devices. This proposal recommends a network that replaces the slow, flat switching with segmented 1 Gbps access, two 10 Gbps core switches, centralised identity and file services on two virtualisation hosts, protected backups and managed voice and video. The work is staged over the four months the client brief allows. [P1, P2]

Each site keeps one internet service. At Brisbane the nbn handoff terminates on a FortiGate 70G firewall that sits directly behind the ISP and in front of the two core switches, so every internet, guest, DMZ and Cairns flow is inspected before it reaches the core stack. The two cores run as one stack over two 10 Gbps links, two domain controllers share identity, DNS and DHCP, and each virtualisation host holds replicas of the other host's services. One firewall and one internet service per site remain an accepted residual risk, which section 2.3 explains.

The first-year cost is $350,601.81, including a 10% implementation contingency and the first year of operating costs, which leaves $149,398.19 of the $500,000 budget. The five-year baseline ownership estimate is $498,211.41, which adds four further years of operating costs and firewall renewals to the first-year figure. Section 6.9 separates the published retail prices from the design allowances, and those allowances need supplier quotes before anything is ordered. [P1]

# Introduction

HelpYou has asked for a network infrastructure proposal that supports the immediate two-floor expansion of the Brisbane head office, connects the Cairns branch, and gives HelpYou centralised DHCP and DNS, company-hosted email, a management server with activity logs, backups, remote access, wireless for staff and visitors, a better telephone service and videoconferencing, all within four months and a $500,000 budget. [P1] This report responds to that brief.

Section 1 compares the current network with the one HelpYou needs, in a three-column organiser with numbers in every row. Sections 2 to 5 set out the logical topology (Figure 2), the physical layout from the Packet Tracer physical view (Figure 1, with a full-size render as Figure 1b), the rack arrangement (Figure 3) and the IP scheme. Section 6 covers the selected hardware, software and services, with make, model, placement and price for each, and the total cost. Section 7 forecasts server bandwidth over the next five years, explains how the design keeps up with it and closes with the conclusion of the proposal, and section 8 lists the sources behind it.

I started from the client brief and the customer interview, built the gap analysis from them, and then designed each layer to close a gap: the firewall and segmentation at the boundary first, then switching, servers, identity, backup and communications. Subnets are sized from HelpYou's five-year device counts, so the address plan lasts the full five years. For every product I checked the vendor data sheet against the job it has to do and took the price from an Australian retail listing. Configured items such as the servers carry an allowance that is flagged for a supplier quote.

The current conditions and business requirements come from the HelpYou client brief [P1], the department locations, head counts and server bandwidth figures come from the customer interview answers [P2], and the equipment capabilities and prices come from the vendor and retail pages in the bibliography [R1-R30]. The equipment choices, the VLAN and subnet plan, the recovery targets and the bandwidth forecast are original design work prepared for this proposal.

Two Packet Tracer files accompany this report. FLOOR_PLAN_FINAL.pkt places the devices on the two Brisbane floors and is the source of Figure 1. HelpYou_Proposed_Network.pkt holds the complete proposed design: its logical view is Figure 2 and its physical view holds the racks in Figure 3. Packet Tracer has no Catalyst 1300, FortiGate or Dell R360 models, so Cisco 2960, ASA 5505 and generic server icons stand in for them. Both files show what connects to what with copper cabling, and the addressing, VLAN and security detail sits in notes on the logical view and in the tables of this report.
