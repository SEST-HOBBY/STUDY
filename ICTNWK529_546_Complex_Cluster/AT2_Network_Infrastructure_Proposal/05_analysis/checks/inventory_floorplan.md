# Inventory of FLOOR_PLAN_FINAL.pkt (decrypted as pkt/floor.xml)

Packet Tracer version in file: 8.2.1.0118. 33 devices (31 on the plan plus 2 off-plan Power Distribution Devices), 32 links, one scenario, no notes/shapes (LINES, RECTANGLES, ELLIPSES, POLYGONS all empty).
Raw extraction: `work/analysis/inventory_floorplan.json` (made by `work/analysis/extract_inventory.py`).

## 1. What the screenshot is, and how the background is positioned

- The floor plan is **not** in Packet Tracer's Physical workspace. It is the **Logical** workspace's root-cluster background: `CLUSTERS/ROOTCLUSTER/CLUSTER_BG_IMAGE` points at `E:/.../AT2/BACKGROUND FOR FLOOR PLAN.png` and `CLUSTER_EMBEDDED_BG_IMAGE` embeds it as a 604 x 813 px JPEG (`TILED_BG` = false). The same bytes sit in `PIXMAPBANK`; extracted copy: `pkt/floor_bg_0_IMAGE_CONTENT.jpg`.
- The image is one floor plan duplicated vertically with different room labels: top half (y 0-406) = first floor (Executive Room 1/2, Server Room), bottom half (y 406-813) = second floor (Meeting Room 1/2, Server Room).
- PT draws an untiled cluster background at the workspace origin at native size, so **device `<LOGICAL><X>/<Y>` are the icon centres in the background's own pixel grid** (origin top-left). I verified this against the student's screenshot by FFT cross-correlation of edge maps: screenshot = 0.75 x workspace + (1, 1) px, correlation peak 0.63 versus 0.48 at the next-best scale, and every mapped (X, Y) lands on the centre of its icon in the screenshot (`work/figures/tmp/overlay.png`).
- Links are drawn centre to centre. PT draws straight-through cables solid and crossover cables dashed; the render keeps that convention.
- The render `work/figures/fig1b_physical_layout_render.png` (2475 x 3407 px) uses a 3.75x upscale (604 -> 2265 px for the plan, plus a right margin and bottom strip for the devices that sit off the plan's edge and a legend). Script: `work/figures/render_physical.py`. Link width is 3 px rather than the 2 px suggested: 2 px was close to invisible against the plan's own linework at this size (`LINK_W` in the script).

## 2. Devices

Coordinates are the logical-workspace values from the .pkt (icon centre, background pixels). 'Where' is read off the background at that coordinate. 'Physical view' is where PT's Physical workspace holds the device (all auto-placed, see section 5).

| # | Name | PT type | Model | X | Y | Floor | Where on the plan | Cabled ports | Physical view |
|---|------|---------|-------|---|---|-------|-------------------|--------------|---------------|
| 1 | IT-1 | Pc | PC-PT | 282.5 | 22 | 1st | IT-Cube, top desk | FastEthernet0 <- Switch2 FastEthernet0/1 | Corporate Office floor (auto-placed) |
| 2 | MRKT-2 | Pc | PC-PT | 448.5 | 69 | 1st | Marketing-Cube-1 | FastEthernet0 <- Switch0 FastEthernet0/8 | Corporate Office floor (auto-placed) |
| 3 | IT-2 | Pc | PC-PT | 276.5 | 76 | 1st | IT-Cube, lower desk | FastEthernet0 <- Switch0 FastEthernet0/7 | Corporate Office floor (auto-placed) |
| 4 | VoIP-2 | HomeVoip | Home-VoIP-PT | 330 | 119 | 1st | corridor below the IT-Cube / Marketing wall | Ethernet <- Switch0 FastEthernet0/6 | Corporate Office floor (auto-placed) |
| 5 | Guest WiFi | LightWeightAccessPoint | LAP-PT | 231 | 123 | 1st | corridor between the two cubicle rows, below HR-Cube/IT-Cube | none | Main Wiring Closet > Rack (rack 1) |
| 6 | CUST-2 | Pc | PC-PT | 175.5 | 145 | 1st | CS-Cube, top desk | FastEthernet0 <- Switch0 FastEthernet0/4 | Corporate Office floor (auto-placed) |
| 7 | MGMT-2 | Pc | PC-PT | 282.5 | 157 | 1st | Manager-Cube, top desk | FastEthernet0 <- Switch0 FastEthernet0/5 | Corporate Office floor (auto-placed) |
| 8 | Laptop0 | Laptop | Laptop-PT | 48.5 | 197 | 1st | west side, beside the small office near the entry door | none | Corporate Office floor (auto-placed) |
| 9 | CUST-1 | Pc | PC-PT | 177.5 | 230 | 1st | CS-Cube, lower desk | FastEthernet0 <- Switch2 FastEthernet0/3 | Corporate Office floor (auto-placed) |
| 10 | Switch2 | Switch | 2960-24TT | 509 | 314 | 1st | Server Room, left | FastEthernet0/1 -> IT-1 FastEthernet0; FastEthernet0/2 <- Switch3 FastEthernet0/3; FastEthernet0/3 -> CUST-1 FastEthernet0; FastEthernet0/4 -> HR-1 FastEthernet0; FastEthernet0/5 -> ADMIN-1 FastEthernet0; FastEthernet0/6 -> MGMT-1 FastEthernet0; FastEthernet0/7 -> EXEC-1 FastEthernet0; FastEthernet0/8 -> VoIP-1 Ethernet; GigabitEthernet0/1 <- Switch0 GigabitEthernet0/1; GigabitEthernet0/2 <- Switch1 GigabitEthernet0/1; FastEthernet0/24 <- Switch0 FastEthernet0/24; FastEthernet0/9 <- HR 1 FastEthernet0 | Main Wiring Closet > Rack (rack 1) |
| 11 | Switch3 | Switch | 2960-24TT | 574 | 315 | 1st | Server Room, right | FastEthernet0/1 <- NET MONITOR SERVER FastEthernet0; FastEthernet0/2 <- WEB SERVER FastEthernet0; FastEthernet0/3 -> Switch2 FastEthernet0/2; GigabitEthernet0/1 <- Switch0 GigabitEthernet0/2; GigabitEthernet0/2 <- Switch1 GigabitEthernet0/2; FastEthernet0/24 <- Switch1 FastEthernet0/24 | Main Wiring Closet > Rack (rack 2) |
| 12 | MRKT-1 | Pc | PC-PT | 448.5 | 470 | 2nd | Marketing-Cube-1 | none | Corporate Office floor (auto-placed) |
| 13 | VoIP-1 | HomeVoip | Home-VoIP-PT | 317 | 527 | 2nd | corridor above CS-Cube | Ethernet <- Switch2 FastEthernet0/8 | Corporate Office floor (auto-placed) |
| 14 | HR 1 | Pc | PC-PT | 175.5 | 534 | 2nd | top edge of HR-Cube (corridor side); overlaps HR-1 | FastEthernet0 -> Switch2 FastEthernet0/9 | Corporate Office floor (auto-placed) |
| 15 | HR-1 | Pc | PC-PT | 187.5 | 557 | 2nd | HR-Cube, top desk; overlaps HR 1 | FastEthernet0 <- Switch2 FastEthernet0/4 | Corporate Office floor (auto-placed) |
| 16 | EXEC-2 | Pc | PC-PT | 455.5 | 561 | 2nd | Manager-Cube-1, upper desk | FastEthernet0 -> Switch0 FastEthernet0/9 | Corporate Office floor (auto-placed) |
| 17 | ADMIN-1 | Pc | PC-PT | 364.5 | 575 | 2nd | printer/copier column between CS-Cube and Manager-Cube-1, upper | FastEthernet0 <- Switch2 FastEthernet0/5 | Corporate Office floor (auto-placed) |
| 18 | HR-2 | Pc | PC-PT | 184.5 | 629 | 2nd | HR-Cube, lower desk | FastEthernet0 <- Switch0 FastEthernet0/2 | Corporate Office floor (auto-placed) |
| 19 | MGMT-1 | Pc | PC-PT | 454.5 | 632 | 2nd | Manager-Cube-1, lower desk | FastEthernet0 <- Switch2 FastEthernet0/6 | Corporate Office floor (auto-placed) |
| 20 | EXEC-1 | Pc | PC-PT | 553.5 | 633 | 2nd | Manager-Cube-2 | FastEthernet0 <- Switch2 FastEthernet0/7 | Corporate Office floor (auto-placed) |
| 21 | ADMIN-2 | Pc | PC-PT | 364.5 | 634 | 2nd | printer/copier column between CS-Cube and Manager-Cube-1, lower | FastEthernet0 <- Switch0 FastEthernet0/3 | Corporate Office floor (auto-placed) |
| 22 | WEB SERVER | Server | Server-PT | 608.5 | 697 | 2nd | off the right edge of the plan (x > 604), level with the Server Room | FastEthernet0 -> Switch3 FastEthernet0/2 | Main Wiring Closet > Rack (rack 1) |
| 23 | Server0 | Server | Server-PT | 566.5 | 704 | 2nd | just above the Server Room's top wall (Marketing-Cube-2 side) | FastEthernet0 -> Switch1 FastEthernet0/2 | Main Wiring Closet > Rack (rack 1) |
| 24 | Switch0 | Switch | 2960-24TT | 518 | 720 | 2nd | Server Room, top-left corner | FastEthernet0/1 <- Switch1 FastEthernet0/5; FastEthernet0/2 -> HR-2 FastEthernet0; FastEthernet0/3 -> ADMIN-2 FastEthernet0; FastEthernet0/5 -> MGMT-2 FastEthernet0; FastEthernet0/6 -> VoIP-2 Ethernet; FastEthernet0/7 -> IT-2 FastEthernet0; FastEthernet0/8 -> MRKT-2 FastEthernet0; FastEthernet0/4 -> CUST-2 FastEthernet0; FastEthernet0/9 <- EXEC-2 FastEthernet0; GigabitEthernet0/1 -> Switch2 GigabitEthernet0/1; GigabitEthernet0/2 -> Switch3 GigabitEthernet0/1; FastEthernet0/24 -> Switch2 FastEthernet0/24 | Main Wiring Closet > Rack (rack 1) |
| 25 | APP SERVER | Server | Server-PT | 478.5 | 753 | 2nd | just left of the Server Room's west wall (Meeting Room 2 side) | FastEthernet0 -> Switch1 FastEthernet0/4 | Main Wiring Closet > Rack (rack 1) |
| 26 | Server2 | Server | Server-PT | 613.5 | 757 | 2nd | off the right edge of the plan (x > 604), level with the Server Room | FastEthernet0 -> Switch1 FastEthernet0/6 | Main Wiring Closet > Rack (rack 1) |
| 27 | Switch1 | Switch | 2960-24TT | 551 | 761 | 2nd | Server Room, centre | FastEthernet0/1 <- ASA0 GigabitEthernet1/1; FastEthernet0/2 <- Server0 FastEthernet0; FastEthernet0/3 <- DHCP + DNS FastEthernet0; FastEthernet0/4 <- APP SERVER FastEthernet0; FastEthernet0/5 -> Switch0 FastEthernet0/1; FastEthernet0/6 <- Server2 FastEthernet0; GigabitEthernet0/1 -> Switch2 GigabitEthernet0/2; GigabitEthernet0/2 -> Switch3 GigabitEthernet0/2; FastEthernet0/24 -> Switch3 FastEthernet0/24 | Main Wiring Closet > Rack (rack 1) |
| 28 | Cloud0 | Cloud | Cloud-PT | 574 | 795 | 2nd | bottom of the Server Room | Ethernet6 -> ASA0 GigabitEthernet1/2 | Main Wiring Closet > Rack (rack 1) |
| 29 | DHCP + DNS | Server | Server-PT | 536.5 | 816 | 2nd | below the bottom edge of the plan (y > 813), under the Server Room | FastEthernet0 -> Switch1 FastEthernet0/3 | Main Wiring Closet > Rack (rack 1) |
| 30 | NET MONITOR SERVER | Server | Server-PT | 477.5 | 820 | 2nd | below the bottom edge of the plan (y > 813), under Meeting Room 2 | FastEthernet0 -> Switch3 FastEthernet0/1 | Main Wiring Closet > Rack (rack 1) |
| 31 | ASA0 | ASA | 5506-X | 609.5 | 824 | 2nd | off the bottom-right corner of the plan | GigabitEthernet1/1 -> Switch1 FastEthernet0/1; GigabitEthernet1/2 <- Cloud0 Ethernet6 | Main Wiring Closet > Rack (rack 1) |
| 32 | Power Distribution Device0 | Power Distribution Device | Power Distribution Device | 3900 | 3900 | - | off-plan at (3900, 3900); auto-created with the physical rack, not visible in the screenshot | none | Main Wiring Closet > Rack (rack 1) |
| 33 | Power Distribution Device1 | Power Distribution Device | Power Distribution Device | 3900 | 3900 | - | off-plan at (3900, 3900); auto-created with the physical rack, not visible in the screenshot | none | Main Wiring Closet > Rack (rack 2) |

Type counts: Pc (PC-PT) x15, Server (Server-PT) x6, Switch (2960-24TT) x4, HomeVoip (Home-VoIP-PT) x2, Power Distribution Device (Power Distribution Device) x2, Laptop (Laptop-PT) x1, LightWeightAccessPoint (LAP-PT) x1, ASA (5506-X) x1, Cloud (Cloud-PT) x1.

Module strings present: PCs/servers `PT-HOST-NM-1CFE` (one FastEthernet copper NIC), laptop `PT-LAPTOP-NM-1CFE`, access point `ACCESS_POINT_POWER_ADAPTER`, cloud `PT-CLOUD-NM-1S` x4, `PT-CLOUD-NM-1AM` x2, `PT-CLOUD-NM-1CE`, `PT-CLOUD-NM-1CX` (all PT defaults). Switch and ASA modules are fixed (2960-24TT: 24 x Fa + 2 x Gig; 5506-X: 8 x Gig + Management1/1).

## 3. Links

All 32 links are `eCopper`, length 1 (PT default), functional = true. Straight-through = host/server to switch (and cloud to ASA); crossover = switch to switch.

| # | From device | From port | To device | To port | Cable |
|---|-------------|-----------|-----------|---------|-------|
| 1 | ASA0 | GigabitEthernet1/1 | Switch1 | FastEthernet0/1 | StraightThrough |
| 2 | Cloud0 | Ethernet6 | ASA0 | GigabitEthernet1/2 | StraightThrough |
| 3 | Server0 | FastEthernet0 | Switch1 | FastEthernet0/2 | StraightThrough |
| 4 | DHCP + DNS | FastEthernet0 | Switch1 | FastEthernet0/3 | StraightThrough |
| 5 | NET MONITOR SERVER | FastEthernet0 | Switch3 | FastEthernet0/1 | StraightThrough |
| 6 | APP SERVER | FastEthernet0 | Switch1 | FastEthernet0/4 | StraightThrough |
| 7 | Switch1 | FastEthernet0/5 | Switch0 | FastEthernet0/1 | CrossOver |
| 8 | WEB SERVER | FastEthernet0 | Switch3 | FastEthernet0/2 | StraightThrough |
| 9 | Server2 | FastEthernet0 | Switch1 | FastEthernet0/6 | StraightThrough |
| 10 | Switch0 | FastEthernet0/2 | HR-2 | FastEthernet0 | StraightThrough |
| 11 | Switch0 | FastEthernet0/3 | ADMIN-2 | FastEthernet0 | StraightThrough |
| 12 | Switch0 | FastEthernet0/5 | MGMT-2 | FastEthernet0 | StraightThrough |
| 13 | Switch0 | FastEthernet0/6 | VoIP-2 | Ethernet | StraightThrough |
| 14 | Switch2 | FastEthernet0/1 | IT-1 | FastEthernet0 | StraightThrough |
| 15 | Switch0 | FastEthernet0/7 | IT-2 | FastEthernet0 | StraightThrough |
| 16 | Switch3 | FastEthernet0/3 | Switch2 | FastEthernet0/2 | CrossOver |
| 17 | Switch0 | FastEthernet0/8 | MRKT-2 | FastEthernet0 | StraightThrough |
| 18 | Switch0 | FastEthernet0/4 | CUST-2 | FastEthernet0 | StraightThrough |
| 19 | Switch2 | FastEthernet0/3 | CUST-1 | FastEthernet0 | StraightThrough |
| 20 | Switch2 | FastEthernet0/4 | HR-1 | FastEthernet0 | StraightThrough |
| 21 | Switch2 | FastEthernet0/5 | ADMIN-1 | FastEthernet0 | StraightThrough |
| 22 | Switch2 | FastEthernet0/6 | MGMT-1 | FastEthernet0 | StraightThrough |
| 23 | EXEC-2 | FastEthernet0 | Switch0 | FastEthernet0/9 | StraightThrough |
| 24 | Switch2 | FastEthernet0/7 | EXEC-1 | FastEthernet0 | StraightThrough |
| 25 | Switch2 | FastEthernet0/8 | VoIP-1 | Ethernet | StraightThrough |
| 26 | Switch0 | GigabitEthernet0/1 | Switch2 | GigabitEthernet0/1 | CrossOver |
| 27 | Switch0 | GigabitEthernet0/2 | Switch3 | GigabitEthernet0/1 | CrossOver |
| 28 | Switch1 | GigabitEthernet0/1 | Switch2 | GigabitEthernet0/2 | CrossOver |
| 29 | Switch1 | GigabitEthernet0/2 | Switch3 | GigabitEthernet0/2 | CrossOver |
| 30 | Switch0 | FastEthernet0/24 | Switch2 | FastEthernet0/24 | CrossOver |
| 31 | Switch1 | FastEthernet0/24 | Switch3 | FastEthernet0/24 | CrossOver |
| 32 | HR 1 | FastEthernet0 | Switch2 | FastEthernet0/9 | StraightThrough |

### 3.1 Port map per switch

- **Switch0** (2nd floor Server Room): FastEthernet0/1 <- Switch1 FastEthernet0/5; FastEthernet0/2 -> HR-2 FastEthernet0; FastEthernet0/3 -> ADMIN-2 FastEthernet0; FastEthernet0/4 -> CUST-2 FastEthernet0; FastEthernet0/5 -> MGMT-2 FastEthernet0; FastEthernet0/6 -> VoIP-2 Ethernet; FastEthernet0/7 -> IT-2 FastEthernet0; FastEthernet0/8 -> MRKT-2 FastEthernet0; FastEthernet0/9 <- EXEC-2 FastEthernet0; FastEthernet0/24 -> Switch2 FastEthernet0/24; GigabitEthernet0/1 -> Switch2 GigabitEthernet0/1; GigabitEthernet0/2 -> Switch3 GigabitEthernet0/1
- **Switch1** (2nd floor Server Room): FastEthernet0/1 <- ASA0 GigabitEthernet1/1; FastEthernet0/2 <- Server0 FastEthernet0; FastEthernet0/3 <- DHCP + DNS FastEthernet0; FastEthernet0/4 <- APP SERVER FastEthernet0; FastEthernet0/5 -> Switch0 FastEthernet0/1; FastEthernet0/6 <- Server2 FastEthernet0; FastEthernet0/24 -> Switch3 FastEthernet0/24; GigabitEthernet0/1 -> Switch2 GigabitEthernet0/2; GigabitEthernet0/2 -> Switch3 GigabitEthernet0/2
- **Switch2** (1st floor Server Room): FastEthernet0/1 -> IT-1 FastEthernet0; FastEthernet0/2 <- Switch3 FastEthernet0/3; FastEthernet0/3 -> CUST-1 FastEthernet0; FastEthernet0/4 -> HR-1 FastEthernet0; FastEthernet0/5 -> ADMIN-1 FastEthernet0; FastEthernet0/6 -> MGMT-1 FastEthernet0; FastEthernet0/7 -> EXEC-1 FastEthernet0; FastEthernet0/8 -> VoIP-1 Ethernet; FastEthernet0/9 <- HR 1 FastEthernet0; FastEthernet0/24 <- Switch0 FastEthernet0/24; GigabitEthernet0/1 <- Switch0 GigabitEthernet0/1; GigabitEthernet0/2 <- Switch1 GigabitEthernet0/1
- **Switch3** (1st floor Server Room): FastEthernet0/1 <- NET MONITOR SERVER FastEthernet0; FastEthernet0/2 <- WEB SERVER FastEthernet0; FastEthernet0/3 -> Switch2 FastEthernet0/2; FastEthernet0/24 <- Switch1 FastEthernet0/24; GigabitEthernet0/1 <- Switch0 GigabitEthernet0/2; GigabitEthernet0/2 <- Switch1 GigabitEthernet0/2

### 3.2 Switch-to-switch (crossover) links

- Switch1 FastEthernet0/5 <-> Switch0 FastEthernet0/1
- Switch3 FastEthernet0/3 <-> Switch2 FastEthernet0/2
- Switch0 GigabitEthernet0/1 <-> Switch2 GigabitEthernet0/1
- Switch0 GigabitEthernet0/2 <-> Switch3 GigabitEthernet0/1
- Switch1 GigabitEthernet0/1 <-> Switch2 GigabitEthernet0/2
- Switch1 GigabitEthernet0/2 <-> Switch3 GigabitEthernet0/2
- Switch0 FastEthernet0/24 <-> Switch2 FastEthernet0/24
- Switch1 FastEthernet0/24 <-> Switch3 FastEthernet0/24

So: the two second-floor switches (Switch0, Switch1) and the two first-floor switches (Switch2, Switch3) are fully meshed on their Gigabit ports (4 links), doubled up with Fa0/24-Fa0/24 links on two of those pairs, plus one horizontal link inside each floor pair (Switch1 Fa0/5 - Switch0 Fa0/1 and Switch3 Fa0/3 - Switch2 Fa0/2). That is 8 inter-switch links in total.

### 3.3 Host cabling crosses floors

11 of the 16 PC/phone links go to the switch on the *other* floor: MGMT-2 (1st) -> Switch0 (2nd); VoIP-2 (1st) -> Switch0 (2nd); IT-2 (1st) -> Switch0 (2nd); MRKT-2 (1st) -> Switch0 (2nd); CUST-2 (1st) -> Switch0 (2nd); HR-1 (2nd) -> Switch2 (1st); ADMIN-1 (2nd) -> Switch2 (1st); MGMT-1 (2nd) -> Switch2 (1st); EXEC-1 (2nd) -> Switch2 (1st); VoIP-1 (2nd) -> Switch2 (1st); HR 1 (2nd) -> Switch2 (1st).
Same-floor: HR-2 (2nd) -> Switch0 (2nd); ADMIN-2 (2nd) -> Switch0 (2nd); IT-1 (1st) -> Switch2 (1st); CUST-1 (1st) -> Switch2 (1st); EXEC-2 (2nd) -> Switch0 (2nd).

### 3.4 Devices with no cable

- Laptop0, Guest WiFi, Power Distribution Device0, MRKT-1, Power Distribution Device1. `Guest WiFi` is a LAP-PT lightweight AP with no Ethernet link and no wireless clients associated; `Laptop0` has only its wired NIC module and is not cabled. **`MRKT-1`** (second-floor Marketing-Cube-1) is a PC with no cable at all, while its first-floor twin MRKT-2 is on Switch0 Fa0/8.

## 4. IP addressing and configuration

**Nothing has been configured.** Specifically:

- Every PC, laptop and server port carries IP 0.0.0.0 (no static address, no DHCP lease); gateway and DNS client fields are empty.
- The two Home-VoIP-PT phones show 169.254.84.1/16 (VoIP-1) and 169.254.233.1/16 (VoIP-2). These are APIPA/link-local self-assignments that PT generates when a phone finds no DHCP server, not addresses the student entered.
- Switch0-3: the running-config is PT's factory default for a 2960 (`hostname Switch`, `interface Vlan1 / no ip address / shutdown`, every port at defaults, no `vlan`, `switchport`, `trunk`, `spanning-tree` tuning, passwords or management IP). Startup-config is empty (never saved).
- ASA0: PT's factory default for a 5506-X (`hostname ciscoasa`, every GigabitEthernet1/x and Management1/1 `shutdown` with `no nameif / no security-level / no ip address`, only the default `global_policy` inspection). No NAT, routes, ACLs or DHCP.
- The six Server-PT boxes carry byte-identical service blocks, all PT defaults: HTTP, HTTPS, FTP (stock cisco/cisco account), SMTP and POP3, Syslog, NTP and TFTP enabled as PT ships them; DHCP service **disabled** with only the empty stock `serverPool` (network 0.0.0.0); DNS service **disabled** with an empty name database; AAA/ACS disabled. The names (`WEB SERVER`, `DHCP + DNS`, `NET MONITOR SERVER`, `APP SERVER`) are labels only; no role-specific service, pool or record was added.
- Switch VLAN tables: Switch0: exactly the five stock entries (1 default, 1002-1005 FDDI/token-ring defaults), nothing user-defined; Switch1: exactly the five stock entries (1 default, 1002-1005 FDDI/token-ring defaults), nothing user-defined; Switch2: exactly the five stock entries (1 default, 1002-1005 FDDI/token-ring defaults), nothing user-defined; Switch3: exactly the five stock entries (1 default, 1002-1005 FDDI/token-ring defaults), nothing user-defined. The other `<VLAN>` tags in the file are the default '1' inside each host's wireless-profile template, not switch configuration.
- Hostnames: `SYS_NAME` is `PC` on every host/server, `Switch` on the switches, `ciscoasa` on the ASA, `AP0060.7036.c701` on the AP. Device *display* names (HR-1, APP SERVER, ...) are the only labelling.

So the .pkt is a connectivity picture only, which is consistent with the agreed design-only scope (no CLI configuration required).

## 5. Physical workspace tree

The Physical workspace is PT's untouched default hierarchy; nothing was created, renamed or moved by hand, and no physical background image is set (`BGPATH_TILED` false, no custom image on any node, all grids disabled, `GEOVIEW_GRAPHICSITEMS` empty).

- Intercity (node type 0, x=0, y=0, w=20000, h=12415.8)
  - Home City (node type 1, x=200, y=200, w=2000, h=1238.1)
    - Corporate Office (node type 2, x=100, y=100, w=200, h=125.261)
      - Main Wiring Closet (node type 3, x=861, y=300, w=20, h=20)
        - Rack (node type 4, x=0, y=0)
          - Power Distribution Device0 (node type 6, x=0, y=0) - Power Distribution Device Power Distribution Device
          - Guest WiFi (node type 6, x=4, y=0) - LightWeightAccessPoint LAP-PT
          - Switch0 (node type 6, x=9, y=0) - Switch 2960-24TT
          - Switch1 (node type 6, x=13, y=0) - Switch 2960-24TT
          - Server0 (node type 6, x=17, y=0) - Server Server-PT
          - WEB SERVER (node type 6, x=33, y=0) - Server Server-PT
          - Server2 (node type 6, x=49, y=0) - Server Server-PT
          - ASA0 (node type 6, x=65, y=0) - ASA 5506-X
          - Cloud0 (node type 6, x=70, y=0) - Cloud Cloud-PT
          - DHCP + DNS (node type 6, x=77, y=0) - Server Server-PT
          - NET MONITOR SERVER (node type 6, x=93, y=0) - Server Server-PT
          - APP SERVER (node type 6, x=109, y=0) - Server Server-PT
          - Switch2 (node type 6, x=125, y=0) - Switch 2960-24TT
        - Rack (node type 4, x=0, y=0)
          - Power Distribution Device1 (node type 6, x=0, y=0) - Power Distribution Device Power Distribution Device
          - Switch3 (node type 6, x=4, y=0) - Switch 2960-24TT
      - HR-2 (node type 6, x=86, y=215) - Pc PC-PT
      - HR-1 (node type 6, x=172, y=215) - Pc PC-PT
      - Laptop0 (node type 6, x=258, y=215) - Laptop Laptop-PT
      - VoIP-1 (node type 6, x=344, y=215) - HomeVoip Home-VoIP-PT
      - ADMIN-1 (node type 6, x=430, y=215) - Pc PC-PT
      - ADMIN-2 (node type 6, x=516, y=215) - Pc PC-PT
      - EXEC-2 (node type 6, x=602, y=215) - Pc PC-PT
      - MGMT-1 (node type 6, x=688, y=215) - Pc PC-PT
      - EXEC-1 (node type 6, x=774, y=215) - Pc PC-PT
      - CUST-2 (node type 6, x=860, y=215) - Pc PC-PT
      - CUST-1 (node type 6, x=946, y=215) - Pc PC-PT
      - MGMT-2 (node type 6, x=1032, y=215) - Pc PC-PT
      - VoIP-2 (node type 6, x=1118, y=215) - HomeVoip Home-VoIP-PT
      - IT-2 (node type 6, x=1204, y=215) - Pc PC-PT
      - IT-1 (node type 6, x=1290, y=215) - Pc PC-PT
      - MRKT-1 (node type 6, x=1376, y=215) - Pc PC-PT
      - MRKT-2 (node type 6, x=1462, y=215) - Pc PC-PT
      - HR 1 (node type 6, x=1548, y=215) - Pc PC-PT

Reading of the tree:

- `Intercity > Home City > Corporate Office > Main Wiring Closet` are the four containers PT creates in every new file, with their stock sizes and positions (Home City at (200, 200), Corporate Office at (100, 100), closet at (861, 300)). `HOMERACK` points at the Main Wiring Closet.
- Inside the closet are two `Rack` nodes. Rack 1 (slots left to right by `X`): Power Distribution Device0, Guest WiFi, Switch0, Switch1, Server0, WEB SERVER, Server2, ASA0, Cloud0, DHCP + DNS, NET MONITOR SERVER, APP SERVER, Switch2. Rack 2: Power Distribution Device1, Switch3. PT auto-racks every rack-mountable device (including the cloud and the AP) in creation order and spawns a second rack with its own PDD when the first fills; the student did not place anything.
- The 18 end devices (15 PCs, the laptop and the two phones) sit directly on the Corporate Office floor at PT's auto-placement positions: y = 215 for all, x = 86 x n in creation order (HR-2, HR-1, Laptop0, VoIP-1, ADMIN-1, ADMIN-2, EXEC-2, MGMT-1, EXEC-1, CUST-2, CUST-1, MGMT-2, VoIP-2, IT-2, IT-1, MRKT-1, MRKT-2, HR 1). This is also the order the devices were added to the file.
- There are no custom buildings, floors, wiring closets, racks or tables, so a Packet Tracer **rack view** screenshot from this file would show only the auto-filled default rack (Figure 4 would need to come from the other .pkt or be drawn).

## 6. Points worth knowing when writing the report

- `HR 1` (space) and `HR-1` (hyphen) are two separate PCs sitting almost on top of each other in the second-floor HR-Cube, each cabled to Switch2 (Fa0/9 and Fa0/4). It looks like a leftover duplicate rather than a third HR seat.
- `MRKT-1` is the one PC with no cable (section 3.4); if the report counts connected marketing seats from the .pkt, it will come up one short.
- Five devices sit outside the floor-plan image (WEB SERVER, Server2 to the right; NET MONITOR SERVER, DHCP + DNS below; ASA0 at the corner), which is why the student's screenshot shows them in white space at the bottom right.
- All four switches are the same 2960-24TT model; the PT file does not distinguish the proposed core switches from access switches, and the ASA is the only Layer-3 device (no router). The servers hang off Switch1 (Server0, DHCP + DNS, APP SERVER, Server2) and Switch3 (NET MONITOR SERVER, WEB SERVER); the ISP cloud connects to ASA0 Gi1/2 and ASA0 Gi1/1 goes to Switch1 Fa0/1.
- Host cabling is roughly half cross-floor (section 3.3). On a physical drawing that is a visual simplification of 'everything patches back to a core/access switch', not a cabling plan.
- Nothing in the file carries an IP address, VLAN or hostname, so the report cannot cite the .pkt for the IP scheme; the scheme has to stand on the report's own tables.
