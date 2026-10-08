# 3. Physical Topology

Figure 1 is the Packet Tracer physical view of the two Brisbane floors, drawn on the floor plan HelpYou supplied. The drawing uses that plan as the workspace background, stacked twice. The top half is the first floor, with Executive Room 1 and 2, and the bottom half is the second floor, with Meeting Room 1 and 2. Each floor has its own server room on the right-hand side. Figure 1b redraws the same layout at full size from the device positions and cable list in FLOOR_PLAN_FINAL.pkt, in Packet Tracer's own icon style, so every label stays readable when the report is printed.

![Packet Tracer physical topology: first floor (top) and second floor (bottom) on the supplied floor plan](figures/fig1_packet_tracer_physical_view.png)

*Figure 1. Packet Tracer physical topology: first floor (top) and second floor (bottom) on the supplied floor plan.*

![The same physical layout redrawn at full size from FLOOR_PLAN_FINAL.pkt](figures/fig1b_physical_layout_render.png)

*Figure 1b. The same physical layout redrawn at full size from FLOOR_PLAN_FINAL.pkt.*

Packet Tracer's device library stops at the Cisco 2960 switch and the ASA firewall, so those icons stand in for the proposed Catalyst 1300 switches and the FortiGate 70G. The drawing shows what connects to what, with copper cabling. The VLAN, address and security detail for each device lives in sections 2 and 5.

On the first floor, IT-1 and IT-2 sit in the IT cube at the top of the plan and CUST-1 and CUST-2 in the Customer Service cube. MGMT-2 is in the manager cube beside them and MRKT-2 in the marketing cube at the top right. The guest Wi-Fi access point sits in the corridor between the two rows of cubicles, VoIP-2 is the floor's sample handset, and a laptop near the entry door stands for a visitor's device.

On the second floor, HR-1 and HR-2 sit in the HR cube on the left and ADMIN-1 and ADMIN-2 in the centre of the floor beside the copier column. MRKT-1 is in the marketing cube at the top right, EXEC-2 and MGMT-1 in the cube below it and EXEC-1 in the cube beside them, with VoIP-1 as that floor's handset. Each department is drawn as a sample of one or two PCs; the full head counts drive the subnet sizes in section 5.

The second-floor server room holds the server cluster: six server icons (WEB SERVER, DHCP + DNS, NET MONITOR SERVER, APP SERVER, Server0 and Server2) and two switches, Switch0 and Switch1. The ISP cloud (Cloud0) sits at the bottom of the room and the firewall (ASA0) sits between the cloud and Switch1. The drawn path is therefore ISP, then firewall, then switch, which matches the placement described in section 2.

The first-floor server room holds the other two switches, Switch2 and Switch3. Four of the servers cable to Switch1 and the other two, WEB SERVER and NET MONITOR SERVER, cable up to Switch3. The firewall and four of the server icons sit just past the plan's edge at the bottom right, next to the second-floor server room, where there was room to label them.

Every cable in the drawing is copper, and every desk cable runs straight back to a switch in one of the two server rooms. That star layout is the one the production build keeps. The four switches are cross-connected on their gigabit ports, so each floor's pair reaches the other floor's pair, and the two switches on each floor are joined to each other; Figure 1b draws these switch-to-switch cables dashed. The drawing shows two switches per floor to illustrate the pattern. The production build has the two core switches and six access switches of Figure 2, placed in the racks described in section 4.

In the building itself, the 96 existing Cat 5e runs on floor 1 already terminate on the first-floor server-room patch panels. The 120 Cat 6 runs on floor 2 terminate in the patch-panel rack there, which makes 216 runs in total [P1]. Each floor's outlets patch across to the three access switches in that floor's rack. Each access switch then has two 10 Gbps uplinks, one to each core in the floor-1 network rack, and the floor-2 uplinks run down to floor 1 on SFP+ links covered by the optics allowance in section 6.9. Before cutover, the existing runs are tested and certified, and new runs go in only where the port count in section 4.1 calls for them.

Department placement follows the customer interview: Customer Service and IT on floor 1; Executives, Admin and HR on floor 2; Managers and Marketing split across both floors, with 35 staff on each floor [P1, P2]. The room names printed on the supplied plan are the building's own labels, so the cubicle a department occupies follows this allocation rather than the printed name. Six ceiling-mounted access points across the two floors carry the staff and guest Wi-Fi. The single Guest WiFi icon in the first-floor corridor stands for them, and the coverage survey in section 6.8 sets their final positions.

# 4. Racks Diagram

Figure 3 shows the racks as they are built in the physical view of HelpYou_Proposed_Network.pkt: the F1 Network Rack and F1 Server Rack in the Floor 1 Server Room, the F2 Patch Panel Rack and F2 Equipment Rack in the Floor 2 Server Room, and the 12U Cairns Cabinet. Packet Tracer racks hold active devices only. Patch panels and cable managers are not Packet Tracer devices, so the floor-2 patch-panel rack appears empty, and a Packet Tracer power distribution device stands in for each UPS. Table 4 lists the full contents of every rack, patch panels and UPS included. The design uses the existing server-room rack space on both floors. Floor 2 already has one rack of patch panels and one empty equipment rack, and both are reused as they stand [P1]. In every rack the patching sits at the top, the network equipment below it and the heavier servers and the UPS lower down, so a technician can work on the patching without reaching past a server.

![Rack layout from the physical view of HelpYou_Proposed_Network.pkt](figures/fig3_rack_diagram.png)

*Figure 3. Rack layout from the physical view of HelpYou_Proposed_Network.pkt, Brisbane floors 1 and 2 and the Cairns cabinet.*

In the building, four 24-port patch panels and a cable manager sit at the top of the floor-1 network rack and terminate the 96 Cat 5e runs. Below them is the equipment Figure 3 shows, starting with CORE 1 and CORE 2. Directly under the cores is a shelf holding the nbn NTD and FW-HQ side by side, so the internet path runs from the NTD into the firewall and on to the cores within three rack units. Below them sit the DMZ switch, PBX-01 on its own shelf and the three floor-1 access switches, ASW-1 to ASW-3. A 2U UPS sits at the base and 27U stay spare for growth. HYP-01 takes the top of the floor-1 server rack, with a KVM drawer beneath it and its own UPS at the base.

On floor 2, five 24-port panels in the existing patch-panel rack terminate the 120 Cat 6 runs, with a cable manager between each pair of panels. The equipment rack that is empty today takes ASW-4 to ASW-6, HYP-02, the 2U NAS-BACKUP and a UPS, leaving 34U spare. The Cairns cabinet is a 12U secured wall cabinet holding the nbn NTD, FW-BR, the C1300-24P-4X branch switch, a 24-port patch panel for the branch outlets and a UPS, with 6U spare. The table below summarises each rack.

| Rack | Equipment from top to bottom | What it does |
|---|---|---|
| Floor 1 network rack | Patch panels and cable management; CORE 1; CORE 2; FW-HQ on a shelf with the nbn NTD; DMZ switch; PBX on a shelf; the three floor-1 access switches; UPS at the base. | WAN security, the two core interconnects, floor-1 access and telephone control. |
| Floor 1 server rack | HYP-01; labelled service, management and backup connections; spare expansion space; UPS-backed power. | First domain controller and the first application-host workload. |
| Floor 2 patch-panel rack (existing) | Retained patch panels; labelled outlets and cable management. | Terminates the existing floor-2 horizontal cabling. |
| Floor 2 equipment rack (existing, empty today) | The three floor-2 access switches; HYP-02; NAS-BACKUP; spare space; UPS at the base. | Second domain controller, recovery host and the separate backup appliance. |
| Cairns secured cabinet | ISP handoff, FW-BR, branch access switch and UPS; local patch termination. | Branch VPN, workstation and phone access, and controlled management. |

*Table 4. Rack contents from top to bottom.*

Rack access is restricted to authorised IT staff. Every patch lead is labelled with its floor, panel and outlet, and every device label matches Figure 2 and the static-IP register in section 5.1. Installation includes a check of the power loading, earthing, ventilation and UPS runtime of each rack, and an on-site confirmation of the usable height of the floor-2 racks before the final rack-unit positions are fixed. Putting one host on each floor means a local problem on one floor, such as a failed air-conditioner, leaves the other host running. Both floors share one building, so the off-site backup copies in section 2.2 remain the protection against loss of the site.

## 4.1 Port and outlet provision

Six 48-port access switches, three per floor, give Brisbane 288 copper access ports (6 x 48 = 288). HelpYou's five-year forecast is 270 departmental end devices. Each desk uses two access ports, one for the PC and one for its phone; the 270-device forecast already counts the phones, which is why 270 devices plus six access points come to 276 ports. Each PC keeps its own 1 Gbps port and each phone its own PoE port, so the phone's 100 Mbps pass-through port stays unused. That leaves 12 spare ports across the six switches [P1, P2].

The uplinks use the SFP+ slots on each switch, two of its four, so they take none of the 48 copper ports and two 10 Gbps slots remain on every access switch. The building has 216 horizontal runs today (96 on floor 1 and 120 on floor 2). If every planned connection is wired, up to 60 further runs are needed (276 minus 216), and the $6,000 cabling allowance in section 6.9 covers them [P1, P2].

The 24-port C1300-24P-4X at Cairns serves eight PCs, eight phones and one access point, 17 ports used and seven spare. Its PoE budget powers the phones and the access point, and the spare ports leave room for a branch printer, the meeting-room video PC and a few extra desks.
