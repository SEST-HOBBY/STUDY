"""Structural checks on a generated Packet Tracer XML (python3 -I check_design.py design.xml)."""
import sys, re, collections
import xml.etree.ElementTree as ET
r = ET.parse(sys.argv[1]).getroot()
devs = r.find('NETWORK/DEVICES').findall('DEVICE')
errs = []
names = [d.find('ENGINE').findtext('NAME') for d in devs]
refs = [d.find('ENGINE').findtext('SAVE_REF_ID') for d in devs]
for label, seq in (('name', names), ('save-ref-id', refs)):
    dup = [k for k, v in collections.Counter(seq).items() if v > 1]
    if dup: errs.append(f'duplicate {label}: {dup}')
macs = collections.Counter()
for d in devs:
    for p in d.iter('PORT'):
        m = p.findtext('MACADDRESS')
        if m: macs[m] += 1
dupm = [m for m, c in macs.items() if c > 1]
if dupm: errs.append(f'duplicate MACs: {dupm[:5]}')
addrs = collections.Counter(d.find('WORKSPACE/LOGICAL').findtext('DEV_ADDR') for d in devs)
if any(c > 1 for c in addrs.values()): errs.append('duplicate DEV_ADDR')
# port names per device type
def port_names(d):
    t = d.find('ENGINE').findtext('TYPE')
    types = [p.findtext('TYPE') for p in d.iter('PORT') if p.findtext('TYPE')]
    if t == 'Switch' and types.count('eCopperFastEthernet') == 24:
        return {f'FastEthernet0/{i}' for i in range(1, 25)} | {'GigabitEthernet0/1', 'GigabitEthernet0/2'}
    if t == 'Switch':
        return {'FastEthernet0/1', 'FastEthernet1/1', 'FastEthernet2/1', 'FastEthernet3/1', 'FastEthernet4/1', 'FastEthernet5/1'}
    if t == 'ASA': return {f'Ethernet0/{i}' for i in range(8)}
    if t == 'Cloud': return {'Ethernet6'}
    if t in ('Server', 'Pc', 'Laptop'): return {'FastEthernet0'}
    if t == 'HomeVoip': return {'Ethernet'}
    if t == 'LightWeightAccessPoint': return {'GigabitEthernet0'}
    return set()
byref = {d.find('ENGINE').findtext('SAVE_REF_ID'): d for d in devs}
used = collections.Counter()
for l in r.find('NETWORK/LINKS').findall('LINK'):
    c = l.find('CABLE'); ps = [p.text for p in c.findall('PORT')]
    for end, port, addr in ((c.findtext('FROM'), ps[0], c.findtext('FROM_DEVICE_MEM_ADDR')), (c.findtext('TO'), ps[1], c.findtext('TO_DEVICE_MEM_ADDR'))):
        d = byref.get(end)
        if d is None: errs.append(f'link end missing device {end}'); continue
        n = d.find('ENGINE').findtext('NAME')
        if port not in port_names(d): errs.append(f'bad port {n}:{port}')
        if addr != d.find('WORKSPACE/LOGICAL').findtext('DEV_ADDR'): errs.append(f'mem addr mismatch {n}')
        used[(end, port)] += 1
if any(v > 1 for v in used.values()): errs.append('port used twice')
# physical tree consistency
pw = r.find('PHYSICALWORKSPACE')
nodes, parent = {}, {}
for n in pw.iter('NODE'):
    nodes[n.findtext('UUID_STR')] = n
    ch = n.find('CHILDREN')
    if ch is not None:
        for c in ch.findall('NODE'): parent[c.findtext('UUID_STR')] = n.findtext('UUID_STR')
def chain(u):
    out = [u]
    while out[-1] in parent: out.append(parent[out[-1]])
    return ','.join(reversed(out))
dev_nodes = set()
for d in devs:
    n = d.find('ENGINE').findtext('NAME'); ws = d.find('WORKSPACE')
    path = ws.findtext('PHYSICAL'); last = path.split(',')[-1]
    node = nodes.get(last)
    if node is None: errs.append(f'{n}: physical node missing'); continue
    dev_nodes.add(last)
    if node.findtext('NAME') != n: errs.append(f'{n}: node name {node.findtext("NAME")}')
    if node.findtext('TYPE') != '6': errs.append(f'{n}: node type {node.findtext("TYPE")}')
    if chain(last) != path: errs.append(f'{n}: path does not match tree')
    cp = ws.find('PHYSICAL_CPUR')
    if cp.findtext('CONTAINER_ID') != parent.get(last): errs.append(f'{n}: container id mismatch')
    if cp.findtext('PARENT_PATH') != chain(parent[last]): errs.append(f'{n}: parent path mismatch')
orph = [nodes[u].findtext('NAME') for u in nodes if nodes[u].findtext('TYPE') == '6' and u not in dev_nodes]
if orph: errs.append(f'orphan device nodes: {orph}')
uu = collections.Counter(n.findtext('UUID_STR') for n in pw.iter('NODE'))
if any(v > 1 for v in uu.values()): errs.append('duplicate node uuid')
print('devices', len(devs), 'links', len(r.find('NETWORK/LINKS')), 'MACs', len(macs))
print('ERRORS:' if errs else 'all structural checks passed', *errs[:30], sep='\n  ')
# rack contents
for n in pw.iter('NODE'):
    if n.findtext('TYPE') in ('2', '3', '4'):
        kids = [(c.findtext('NAME'), c.findtext('X')) for c in n.find('CHILDREN').findall('NODE') if c.findtext('TYPE') == '6']
        print(n.findtext('TYPE'), n.findtext('NAME'), kids if n.findtext('TYPE') == '4' else len(kids))
