"""Build HelpYou_Proposed_Network.pkt from the student's own Packet Tracer files.

Base: Helpyou_Network_Topology.pkt (decrypted to topo.xml). Extra device templates
(lightweight access point, VoIP phone) are cloned from FLOOR_PLAN_FINAL.pkt (floor.xml).
Every new device is a clone of an existing device of the same Packet Tracer type with a
new name, save-ref-id, MAC addresses, serial number, logical position and physical
location. All cables are rebuilt from the LINKS table below.

Usage: python3 -I make_design.py topo.xml floor.xml out.xml out.pkt
"""
import copy, os, random, re, sys, uuid
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pktdecrypt import encrypt, decrypt  # noqa: E402

TOPO, FLOOR, OUT_XML, OUT_PKT = sys.argv[1:5]
rng = random.Random(529546)

tree = ET.parse(TOPO)
root = tree.getroot()
net = root.find('NETWORK')
devs_el = net.find('DEVICES')
floor_root = ET.parse(FLOOR).getroot()

def dname(d): return d.find('ENGINE').findtext('NAME')
by = {dname(d): d for d in devs_el.findall('DEVICE')}
fby = {dname(d): d for d in floor_root.find('NETWORK/DEVICES').findall('DEVICE')}

# ---------------------------------------------------------------- uniqueness pools
used_macs = set(re.findall(r'[0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4}', ET.tostring(root, encoding='unicode')))
used_ids = {d.find('ENGINE').findtext('SAVE_REF_ID') for d in devs_el.findall('DEVICE')}
used_addr = set(re.findall(r'>(24\d{11})<', ET.tostring(root, encoding='unicode')))

def new_mac(old):
    while True:
        oui = old[:7]  # keep the vendor prefix (e.g. 0060.2F)
        tail = rng.randrange(0, 1 << 24)
        mac = f'{oui}{tail >> 16:02X}.{tail & 0xFFFF:04X}'
        if mac not in used_macs:
            used_macs.add(mac); return mac

def eui64_ll(mac):
    h = mac.replace('.', '')
    b = bytearray.fromhex(h); b[0] ^= 0x02
    e = b[:3] + b'\xff\xfe' + b[3:]
    groups = [f'{(e[i] << 8) | e[i+1]:X}' for i in range(0, 8, 2)]
    return 'FE80::' + ':'.join(groups)

def new_ref():
    while True:
        r = f'save-ref-id:{rng.randrange(10**18, 2**64 - 1)}'
        if r not in used_ids:
            used_ids.add(r); return r

def new_addr():
    while True:
        a = str(rng.randrange(2432400000000, 2432699999999))
        if a not in used_addr:
            used_addr.add(a); return a

def new_uuid(): return '{' + str(uuid.UUID(int=rng.getrandbits(128), version=4)) + '}'

# ---------------------------------------------------------------- physical tree helpers
pw = root.find('PHYSICALWORKSPACE')
nodes = {n.findtext('UUID_STR'): n for n in pw.iter('NODE')}
parent_of = {}
for n in pw.iter('NODE'):
    ch = n.find('CHILDREN')
    if ch is not None:
        for c in ch.findall('NODE'):
            parent_of[c.findtext('UUID_STR')] = n.findtext('UUID_STR')

def chain(uid):
    out = [uid]
    while out[-1] in parent_of: out.append(parent_of[out[-1]])
    return list(reversed(out))

def find_node(name, typ):
    for n in pw.iter('NODE'):
        if n.findtext('NAME') == name and n.findtext('TYPE') == str(typ): return n
    raise KeyError(name)

def set_text(e, tag, val):
    x = e.find(tag); x.text = str(val)

def add_container(template, parent_uid, name, x, y):
    """Clone a building/closet/rack node (without its children) under parent."""
    n = copy.deepcopy(template)
    ch = n.find('CHILDREN')
    for c in list(ch): ch.remove(c)
    uid = new_uuid()
    set_text(n, 'NAME', name); set_text(n, 'UUID_STR', uid); set_text(n, 'X', x); set_text(n, 'Y', y)
    nodes[parent_uid].find('CHILDREN').append(n)
    nodes[uid] = n; parent_of[uid] = parent_uid
    return uid

# Rename the existing hierarchy and add the extra rooms and racks
building = find_node('Corporate Office', 2); bld_uid = building.findtext('UUID_STR')
closet1 = find_node('Main Wiring Closet', 3); c1_uid = closet1.findtext('UUID_STR')
rack1 = find_node('Rack', 4); r1_uid = rack1.findtext('UUID_STR')
city_uid = parent_of[bld_uid]
set_text(building, 'NAME', 'HelpYou Brisbane Head Office')
set_text(closet1, 'NAME', 'Floor 1 Server Room')
set_text(rack1, 'NAME', 'F1 Network Rack')
r1b_uid = add_container(rack1, c1_uid, 'F1 Server Rack', 150, 0)
c2_uid = add_container(closet1, bld_uid, 'Floor 2 Server Room', 861, 600)
r2a_uid = add_container(rack1, c2_uid, 'F2 Patch Panel Rack', 0, 0)
r2b_uid = add_container(rack1, c2_uid, 'F2 Equipment Rack', 150, 0)
cbld_uid = add_container(building, city_uid, 'HelpYou Cairns Branch', 600, 100)
cc_uid = add_container(closet1, cbld_uid, 'Cairns Comms Cabinet', 300, 300)
rc_uid = add_container(rack1, cc_uid, 'Cairns Cabinet', 0, 0)

def device_node(dev):
    path = dev.find('WORKSPACE').findtext('PHYSICAL').split(',')
    return nodes[path[-1]]

def move_physical(dev, container_uid, x, y):
    """Place a device (its physical node) inside a container at x,y."""
    node = device_node(dev)
    old_parent = nodes[parent_of[node.findtext('UUID_STR')]]
    old_parent.find('CHILDREN').remove(node)
    nodes[container_uid].find('CHILDREN').append(node)
    parent_of[node.findtext('UUID_STR')] = container_uid
    set_text(node, 'X', x); set_text(node, 'Y', y)
    ws = dev.find('WORKSPACE')
    ws.find('PHYSICAL').text = ','.join(chain(node.findtext('UUID_STR')))
    cp = ws.find('PHYSICAL_CPUR')
    set_text(cp, 'X', x); set_text(cp, 'Y', y)
    cp.find('PARENT_PATH').text = ','.join(chain(container_uid))
    cp.find('CONTAINER_ID').text = container_uid

def clone(src, name, lx, ly, container_uid, px, py):
    d = copy.deepcopy(src)
    e = d.find('ENGINE')
    xml = ET.tostring(d, encoding='unicode')
    # MAC addresses (and the IPv6 link-local addresses derived from them)
    for old in sorted(set(re.findall(r'[0-9A-F]{4}\.[0-9A-F]{4}\.[0-9A-F]{4}', xml))):
        new = new_mac(old)
        xml = xml.replace(old, new).replace(eui64_ll(old), eui64_ll(new))
    d = ET.fromstring(xml)
    e = d.find('ENGINE')
    e.find('NAME').text = name
    e.find('SAVE_REF_ID').text = new_ref()
    sn = e.find('SERIALNUMBER')
    if sn is not None and sn.text:
        sn.text = sn.text[:-4] + ''.join(rng.choice('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ') for _ in range(4))
    ws = d.find('WORKSPACE'); lg = ws.find('LOGICAL')
    lg.find('X').text = str(lx); lg.find('Y').text = str(ly)
    lg.find('DEVCLUSTERID').text = '1-1'
    lg.find('MEM_ADDR').text = new_addr(); lg.find('DEV_ADDR').text = new_addr()
    # physical node: clone the template device's node, new uuid
    src_path = src.find('WORKSPACE').findtext('PHYSICAL').split(',')
    tmpl_node = nodes[src_path[-1]] if src_path[-1] in nodes else floor_nodes[src_path[-1]]
    nn = copy.deepcopy(tmpl_node)
    uid = new_uuid()
    set_text(nn, 'NAME', name); set_text(nn, 'UUID_STR', uid)
    nodes[container_uid].find('CHILDREN').append(nn)
    nodes[uid] = nn; parent_of[uid] = container_uid
    set_text(nn, 'X', px); set_text(nn, 'Y', py)
    ws.find('PHYSICAL').text = ','.join(chain(uid))
    cp = ws.find('PHYSICAL_CPUR')
    set_text(cp, 'X', px); set_text(cp, 'Y', py)
    cp.find('PARENT_PATH').text = ','.join(chain(container_uid))
    cp.find('CONTAINER_ID').text = container_uid
    devs_el.append(d)
    by[name] = d
    return d

floor_pw = floor_root.find('PHYSICALWORKSPACE')
floor_nodes = {n.findtext('UUID_STR'): n for n in floor_pw.iter('NODE')}

def rename(old, new):
    d = by.pop(old); d.find('ENGINE').find('NAME').text = new; by[new] = d
    device_node(d).find('NAME').text = new
    return d

def place_logical(name, x, y):
    lg = by[name].find('WORKSPACE/LOGICAL'); lg.find('X').text = str(x); lg.find('Y').text = str(y)

# ---------------------------------------------------------------- devices
SW, ASA, CLOUD, SRV, PC, PDU = by['CORE 1'], by['Firewall – FortiGate'], by['ISP-1 Cloud'], by['SRV-WEB'], by['HR-1'], by['Power Distribution Device0']
AP, VOIP = fby['Guest WiFi'], fby['VoIP-1']

rename('Firewall – FortiGate', 'FW-HQ')
rename('ISP-1 Cloud', 'Brisbane ISP')
rename('DMZ Switch', 'DMZ-SW')
rename('Power Distribution Device0', 'PDU-F1-NET')
for k in range(1, 6): rename(f'Excutive-{k}', f'Executive-{k}')

# logical layout (device icon positions, Packet Tracer workspace pixels)
L = {
 'Brisbane ISP': (1000, 55), 'FW-HQ': (1000, 205), 'DMZ-SW': (790, 215), 'SMTP-GW': (620, 215),
 'CORE 1': (860, 400), 'CORE 2': (1140, 400), 'NAS-BACKUP': (690, 560), 'PBX-01': (1310, 560),
 'HYP-01': (490, 500), 'DC1': (90, 450), 'SRV-WEB': (210, 450), 'SRV-HRDB': (330, 450), 'SRV-LOG': (90, 555),
 'HYP-02': (1510, 500), 'DC2': (1670, 450), 'SRV-MKT-FS': (1790, 450), 'SRV-CS-FS': (1910, 450),
 'SRV-MAIL': (1670, 555), 'SRV-MON': (1790, 555), 'WLAN-CTRL': (1910, 555),
 'ASW-1': (440, 760), 'ASW-2': (640, 760), 'ASW-3': (830, 760),
 'ASW-4': (1100, 760), 'ASW-5': (1300, 760), 'ASW-6': (1530, 760),
 'IT-1': (390, 900), 'IT-2': (490, 900), 'CS-1': (390, 1010), 'CS-5': (490, 1010),
 'Manager-1': (590, 900), 'Marketing-1': (690, 900), 'Marketing-5': (640, 1010),
 'AP-F1': (790, 900), 'VoIP-F1': (880, 900),
 'Executive-1': (1050, 900), 'Executive-2': (1150, 900), 'Executive-3': (1050, 1010), 'Executive-4': (1150, 1010), 'Executive-5': (1100, 1110),
 'Admin-1': (1250, 900), 'Admin-5': (1350, 900), 'Admin-6': (1250, 1010), 'Admin-10': (1350, 1010),
 'HR-1': (1440, 900), 'HR-3': (1540, 900), 'Manager-5': (1440, 1010), 'Marketing-6': (1540, 1010), 'Marketing-10': (1440, 1110),
 'AP-F2': (1540, 1110), 'VoIP-F2': (1620, 1010),
 'Cairns ISP': (1990, 720), 'FW-BR': (1990, 840), 'CAIRNS-SW': (1990, 960),
 'CNS-PC1': (1810, 1090), 'CNS-PC2': (1910, 1090), 'VoIP-CNS': (2020, 1090), 'AP-CNS': (2120, 1090),
}
for n in ('Brisbane ISP', 'FW-HQ', 'DMZ-SW', 'CORE 1', 'CORE 2', 'SRV-WEB', 'SRV-HRDB', 'SRV-MKT-FS', 'SRV-CS-FS',
          'IT-1', 'IT-2', 'CS-1', 'CS-5', 'Manager-1', 'Marketing-1', 'Marketing-5', 'Executive-1', 'Executive-2', 'Executive-3',
          'Executive-4', 'Executive-5', 'Admin-1', 'Admin-5', 'Admin-6', 'Admin-10', 'HR-1', 'HR-3', 'Manager-5', 'Marketing-6', 'Marketing-10'):
    place_logical(n, *L[n])

# physical: existing rack devices re-ordered in the floor-1 network rack, servers become VMs on the floor
RACK1 = [('CORE 1', 3), ('CORE 2', 7), ('Brisbane ISP', 11), ('FW-HQ', 15), ('DMZ-SW', 19)]
for n, x in RACK1: move_physical(by[n], r1_uid, x, 0)
move_physical(by['PDU-F1-NET'], r1_uid, 63, 0)
for k, n in enumerate(('SRV-WEB', 'SRV-HRDB', 'SRV-MKT-FS', 'SRV-CS-FS')):
    move_physical(by[n], bld_uid, 760 + 50 * k, 420)

OFF = (3900, 3900)  # Packet Tracer parks power devices off the logical canvas
new = [
 # name, template, container, physical x, y
 ('PBX-01', SRV, r1_uid, 23, 0), ('ASW-1', SW, r1_uid, 39, 0), ('ASW-2', SW, r1_uid, 43, 0), ('ASW-3', SW, r1_uid, 47, 0),
 ('HYP-01', SRV, r1b_uid, 3, 0), ('PDU-F1-SRV', PDU, r1b_uid, 23, 0),
 ('ASW-4', SW, r2b_uid, 3, 0), ('ASW-5', SW, r2b_uid, 7, 0), ('ASW-6', SW, r2b_uid, 11, 0),
 ('HYP-02', SRV, r2b_uid, 15, 0), ('NAS-BACKUP', SRV, r2b_uid, 31, 0), ('PDU-F2-EQ', PDU, r2b_uid, 51, 0),
 ('Cairns ISP', CLOUD, rc_uid, 3, 0), ('FW-BR', ASA, rc_uid, 7, 0), ('CAIRNS-SW', SW, rc_uid, 11, 0), ('PDU-CNS', PDU, rc_uid, 19, 0),
]
vm_pos = 0
for name in ('DC1', 'DC2', 'SRV-MAIL', 'SMTP-GW', 'SRV-MON', 'SRV-LOG', 'WLAN-CTRL'):
    new.append((name, SRV, bld_uid, 760 + 50 * (4 + vm_pos), 420)); vm_pos += 1
new += [('AP-F1', AP, bld_uid, 300, 150), ('VoIP-F1', VOIP, bld_uid, 340, 150),
        ('AP-F2', AP, bld_uid, 300, 450), ('VoIP-F2', VOIP, bld_uid, 340, 450),
        ('CNS-PC1', PC, cbld_uid, 100, 100), ('CNS-PC2', PC, cbld_uid, 150, 100),
        ('VoIP-CNS', VOIP, cbld_uid, 200, 100), ('AP-CNS', AP, cbld_uid, 250, 100)]
for name, tmpl, cont, px, py in new:
    lx, ly = L.get(name, OFF)
    clone(tmpl, name, lx, ly, cont, px, py)

# ---------------------------------------------------------------- links
links = net.find('LINKS')
for l in list(links): links.remove(l)
template_link = None
LINKS = [
 # (a, port, b, port, crossover?)
 ('Brisbane ISP', 'Ethernet6', 'FW-HQ', 'Ethernet0/0', False),
 ('FW-HQ', 'Ethernet0/1', 'CORE 1', 'FastEthernet0/24', False),
 ('FW-HQ', 'Ethernet0/2', 'CORE 2', 'FastEthernet0/24', False),
 ('FW-HQ', 'Ethernet0/3', 'DMZ-SW', 'FastEthernet0/1', False),
 ('SMTP-GW', 'FastEthernet0', 'DMZ-SW', 'FastEthernet1/1', False),
 ('CORE 1', 'GigabitEthernet0/1', 'CORE 2', 'GigabitEthernet0/1', True),
 ('CORE 1', 'GigabitEthernet0/2', 'CORE 2', 'GigabitEthernet0/2', True),
]
for k in range(1, 7):
    LINKS.append((f'ASW-{k}', 'GigabitEthernet0/1', 'CORE 1', f'FastEthernet0/{k}', True))
    LINKS.append((f'ASW-{k}', 'GigabitEthernet0/2', 'CORE 2', f'FastEthernet0/{k}', True))
LINKS += [
 ('HYP-01', 'FastEthernet0', 'CORE 1', 'FastEthernet0/10', False),
 ('NAS-BACKUP', 'FastEthernet0', 'CORE 1', 'FastEthernet0/20', False),
 ('HYP-02', 'FastEthernet0', 'CORE 2', 'FastEthernet0/10', False),
 ('PBX-01', 'FastEthernet0', 'CORE 2', 'FastEthernet0/20', False),
]
ACCESS = {
 'ASW-1': ['IT-1', 'IT-2', 'CS-1', 'CS-5'], 'ASW-2': ['Manager-1', 'Marketing-1', 'Marketing-5'], 'ASW-3': ['AP-F1', 'VoIP-F1'],
 'ASW-4': ['Executive-1', 'Executive-2', 'Executive-3', 'Executive-4', 'Executive-5'], 'ASW-5': ['Admin-1', 'Admin-5', 'Admin-6', 'Admin-10'],
 'ASW-6': ['HR-1', 'HR-3', 'Manager-5', 'Marketing-6', 'Marketing-10', 'AP-F2', 'VoIP-F2'],
 'CAIRNS-SW': ['CNS-PC1', 'CNS-PC2', 'VoIP-CNS', 'AP-CNS'],
}
def host_port(n):
    t = by[n].find('ENGINE').findtext('TYPE')
    return {'HomeVoip': 'Ethernet', 'LightWeightAccessPoint': 'GigabitEthernet0'}.get(t, 'FastEthernet0')
for sw, hosts in ACCESS.items():
    for k, h in enumerate(hosts, start=1):
        LINKS.append((h, host_port(h), sw, f'FastEthernet0/{k}', False))
LINKS += [('Cairns ISP', 'Ethernet6', 'FW-BR', 'Ethernet0/0', False),
          ('FW-BR', 'Ethernet0/1', 'CAIRNS-SW', 'GigabitEthernet0/1', False)]

def dev_addr(n): return by[n].find('WORKSPACE/LOGICAL').findtext('DEV_ADDR')
def ref(n): return by[n].find('ENGINE').findtext('SAVE_REF_ID')
seen_ports = set()
for a, pa, b, pb, xo in LINKS:
    for k in ((a, pa), (b, pb)):
        assert k not in seen_ports, f'port used twice: {k}'
        seen_ports.add(k)
    lk = ET.SubElement(links, 'LINK')
    ET.SubElement(lk, 'TYPE').text = 'eCopper'
    c = ET.SubElement(lk, 'CABLE')
    for tag, val in (('LENGTH', '1'), ('FUNCTIONAL', 'true'), ('FROM', ref(a)), ('PORT', pa), ('TO', ref(b)), ('PORT', pb),
                     ('FROM_DEVICE_MEM_ADDR', dev_addr(a)), ('TO_DEVICE_MEM_ADDR', dev_addr(b)),
                     ('FROM_PORT_MEM_ADDR', new_addr()), ('TO_PORT_MEM_ADDR', new_addr()),
                     ('GEO_VIEW_COLOR', '#f7990d'), ('IS_MANAGED_IN_RACK_VIEW', 'true'),
                     ('TYPE', 'eCrossOver' if xo else 'eStraightThrough')):
        ET.SubElement(c, tag).text = val

# ---------------------------------------------------------------- notes and rectangles (logical view)
notes = pw.find('NOTES')
for n in list(notes): notes.remove(n)
rects = root.find('RECTANGLES')
for r in list(rects): rects.remove(r)
z = [40100]
def note(x, y, text):
    n = ET.SubElement(notes, 'NOTE', {'uuid': new_uuid()})
    ET.SubElement(n, 'X').text = str(x); ET.SubElement(n, 'Y').text = str(y)
    z[0] += 1; ET.SubElement(n, 'Z').text = str(z[0])
    ET.SubElement(n, 'TEXT', {'translate': 'true'}).text = text
    ET.SubElement(n, 'NOTECLUSTERID').text = '1-1'
    ET.SubElement(n, 'MEM_ADDR').text = new_addr()
def rect(x1, y1, x2, y2, rgb):
    r = ET.SubElement(rects, 'RECTANGLE', {'uuid': new_uuid()})
    for tag, v in (('TopLeftX', x1), ('TopLeftY', y1), ('BottomRightX', x2), ('BottomRightY', y2)):
        ET.SubElement(r, tag).text = str(v)
    col = ET.SubElement(r, 'Color')
    for tag, v in zip(('Red', 'Green', 'Blue'), rgb): ET.SubElement(col, tag).text = str(v)
    ET.SubElement(r, 'Filled', {'OUTLINECOLOR': '#000000', 'OUTLINED': 'true'}).text = '1'
    ET.SubElement(r, 'RECTCLUSTERID').text = '1-1'
    ET.SubElement(r, 'MEM_ADDR').text = new_addr()

RECTS = [
 (540, 150, 860, 280, (255, 242, 204)),     # DMZ
 (25, 300, 575, 610, (226, 239, 218)),      # HYP-01
 (1425, 300, 1975, 610, (226, 239, 218)),   # HYP-02
 (330, 680, 940, 1170, (222, 235, 247)),    # floor 1
 (990, 680, 1680, 1170, (222, 235, 247)),   # floor 2
 (1730, 640, 2180, 1170, (242, 242, 242)),  # Cairns
]
for r in RECTS: rect(*r)
NOTES = [
 (550, 155, 'DMZ  VLAN 100  192.168.100.0/27'),
 (1060, 30, 'Brisbane nbn Business 1000/400 Mbps, static IP'),
 (1060, 130, 'FW-HQ  FortiGate 70G (ASA icon)\nIPS/IDS, UTP, NAT, VPN\nguest VLAN 90 and DMZ gateways\nmgmt 192.168.120.4'),
 (1060, 240, 'Site-to-site IPsec VPN to FW-BR (Cairns)'),
 (1180, 300, 'VLAN 900 transit 192.168.254.0/29\n(1 Gbps to each core)'),
 (700, 460, 'CORE 1 + CORE 2  C1300-12XS stack\n2 x 10 Gbps stack links, VLAN gateways'),
 (35, 305, 'HYP-01  Dell R360, floor 1  (2 x 10 Gbps to CORE 1 + CORE 2)\nVMs: DC1 .110.10, WEB .110.20, HRDB .110.21,\nLOG (Wazuh) .120.21, SMTP-GW (DMZ NIC)'),
 (1435, 305, 'HYP-02  Dell R360, floor 2  (2 x 10 Gbps to CORE 1 + CORE 2)\nVMs: DC2 .110.11, MKT .110.22, CS .110.23, MAIL .110.24,\nMON (Zabbix SNMPv3) .120.20, WLAN-CTRL .120.22'),
 (35, 625, 'Server VLANs: 110 services 192.168.110.0/26 | 120 management 192.168.120.0/26\n130 backup 192.168.130.0/27 | each VM replicates to the other host'),
 (340, 690, 'Floor 1: ASW-1..3 C1300-48P-4X, 2 x 10 Gbps uplinks'),
 (1000, 690, 'Floor 2: ASW-4..6 C1300-48P-4X, 2 x 10 Gbps uplinks'),
 (340, 1185, 'Floor 1 VLANs: 70 IT 192.168.70.0/26 | 40 Customer Service 192.168.40.0/25\n20 Managers 192.168.20.0/26 | 30 Marketing 192.168.30.0/25\n80 Voice 192.168.80.0/25 | 140 Staff Wi-Fi 192.168.140.0/24 | 90 Guest 192.168.90.0/24'),
 (1000, 1185, 'Floor 2 VLANs: 10 Executives 192.168.10.0/26 | 50 Admin 192.168.50.0/26\n60 HR 192.168.60.0/27 | 20 Managers, 30 Marketing, 80 Voice,\n140 Staff Wi-Fi and 90 Guest as on floor 1'),
 (1740, 650, 'Cairns branch'),
 (1740, 800, 'FW-BR\nFortiGate 70G\n(ASA icon)'),
 (1740, 930, 'CAIRNS-SW\nC1300-24P-4X'),
 (1740, 1185, 'Cairns VLANs (gateways on FW-BR)\n210 Staff 10.20.10.0/26 | 220 Mgmt 10.20.20.0/27\n280 Voice 10.20.80.0/27 | 8 PCs, 8 phones, 1 AP'),
 (35, 1290, '2960, ASA 5505 and Server-PT icons stand in for the Catalyst 1300 switches, FortiGate 70G firewalls and Dell R360 hosts.\nProduction link speeds: access 1 Gbps; uplinks, stack links and host links 10 Gbps.'),
]
for n in NOTES: note(*n)

# ---------------------------------------------------------------- write
xml = ET.tostring(root, encoding='unicode').encode('utf-8')
open(OUT_XML, 'wb').write(xml)
open(OUT_PKT, 'wb').write(encrypt(xml))
back, ok, _ = decrypt(open(OUT_PKT, 'rb').read())
assert back == xml and ok
print(f'devices {len(devs_el.findall("DEVICE"))}, links {len(links.findall("LINK"))}, notes {len(notes)}, rectangles {len(rects)}')
