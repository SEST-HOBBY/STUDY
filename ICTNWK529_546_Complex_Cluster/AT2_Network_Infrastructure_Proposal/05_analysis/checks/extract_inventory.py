#!/usr/bin/env python3
"""Extract devices, links, IP configuration and the physical workspace tree
from a decrypted Packet Tracer 8.2.1 XML file. Run with: python3 -I extract_inventory.py <xml> <out.json>
The XML is untrusted data; it is parsed with the stdlib ElementTree only.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]
tree = ET.parse(src)
root = tree.getroot()

net = root.find("NETWORK")
devices = []
ref2name = {}
IP_TAGS = {"IP", "IP_ADDRESS", "SUBNET", "SUBNET_MASK", "GATEWAY", "IP_GATEWAY", "PORT_GATEWAY", "DNS_SERVER", "IPADDRESS", "IP_ADDR", "MASK"}

for dev in net.find("DEVICES").findall("DEVICE"):
    eng = dev.find("ENGINE")
    t = eng.find("TYPE")
    name = eng.findtext("NAME", "")
    ref = eng.findtext("SAVE_REF_ID", "")
    ws = dev.find("WORKSPACE")
    lg = ws.find("LOGICAL")
    ph = ws.findtext("PHYSICAL", "")
    cpur = ws.find("PHYSICAL_CPUR")
    # hostname / sys name
    sysname = eng.findtext("SYS_NAME", "")
    hostname = eng.findtext("HOSTNAME", "")
    desc = eng.findtext("DESCRIPTION", "")
    # Ports with any IP set
    ips = []
    for port in eng.iter("PORT"):
        ip = port.findtext("IP")
        mask = port.findtext("SUBNET")
        if ip and ip not in ("", "0.0.0.0"):
            ips.append({"port": port.findtext("TYPE", ""), "ip": ip, "mask": mask or ""})
    # any non-default IPv4 anywhere else in the engine (gateway, dns, dhcp pools, vlan interfaces)
    other_ips = []
    for el in eng.iter():
        if el.tag in IP_TAGS and el.text and el.text.strip() and el.text.strip() not in ("0.0.0.0", "255.255.255.0", "255.255.255.255"):
            other_ips.append({"tag": el.tag, "value": el.text.strip()})
    # module models (first non-empty)
    modules = sorted({m.text for m in eng.iter("MODEL") if m.text})
    # running-config lines, if any (routers/switches)
    rc = eng.find("RUNNINGCONFIG")
    running = [l.text for l in rc.findall("LINE")] if rc is not None else []
    sc = eng.find("STARTUPCONFIG")
    startup = [l.text for l in sc.findall("LINE")] if sc is not None else []
    vlans = []
    for v in eng.iter("VLAN"):
        n = v.findtext("NUMBER") or v.findtext("ID")
        vn = v.findtext("NAME")
        if n and vn:
            vlans.append({"id": n, "name": vn})
    d = {
        "name": name,
        "pt_type": t.text if t is not None else "",
        "model": t.get("model", "") if t is not None else "",
        "custom_model": t.get("customModel", "") if t is not None else "",
        "save_ref_id": ref,
        "x": float(lg.findtext("X")),
        "y": float(lg.findtext("Y")),
        "dev_cluster_id": lg.findtext("DEVCLUSTERID", ""),
        "physical_path": ph,
        "physical_cpur": {k: cpur.findtext(k) for k in ("X_PN", "Y_PN", "X", "Y", "CONTAINER_ID")} if cpur is not None else None,
        "sys_name": sysname,
        "hostname": hostname,
        "description": desc,
        "modules": modules,
        "port_ips": ips,
        "other_ip_values": other_ips,
        "running_config_lines": running,
        "startup_config_lines": startup,
        "vlans": vlans,
    }
    devices.append(d)
    ref2name[ref] = name

links = []
for ln in net.find("LINKS").findall("LINK"):
    cab = ln.find("CABLE")
    ports = [p.text for p in cab.findall("PORT")]
    links.append({
        "link_type": ln.findtext("TYPE", ""),
        "cable_type": cab.findtext("TYPE", ""),
        "length": cab.findtext("LENGTH", ""),
        "functional": cab.findtext("FUNCTIONAL", ""),
        "from_ref": cab.findtext("FROM", ""),
        "from_device": ref2name.get(cab.findtext("FROM", ""), "?"),
        "from_port": ports[0] if ports else "",
        "to_ref": cab.findtext("TO", ""),
        "to_device": ref2name.get(cab.findtext("TO", ""), "?"),
        "to_port": ports[1] if len(ports) > 1 else "",
    })

# Physical workspace tree
pw = root.find("PHYSICALWORKSPACE")

def node_to_dict(n, depth=0):
    d = {
        "name": n.findtext("NAME", ""),
        "type": n.findtext("TYPE", ""),
        "x": n.findtext("X", ""),
        "y": n.findtext("Y", ""),
        "w": n.findtext("W", ""),
        "h": n.findtext("H", ""),
        "uuid": n.findtext("UUID_STR", ""),
        "path": n.findtext("PATH", ""),
        "children": [],
        "devices": [],
    }
    ch = n.find("CHILDREN")
    if ch is not None:
        for c in ch.findall("NODE"):
            d["children"].append(node_to_dict(c, depth + 1))
    # devices placed directly in this node, if the file records them
    for tag in ("DEVICES", "DEVICE_PATHS", "DEVICE"):
        for e in n.findall(tag):
            d["devices"].append(ET.tostring(e, encoding="unicode")[:300])
    # Record any other child tags for inspection
    d["other_tags"] = sorted({c.tag for c in n if c.tag not in ("NAME", "TYPE", "X", "Y", "W", "H", "UUID_STR", "PATH", "CHILDREN", "SX", "SY", "D")})
    return d

phys = {
    "homerack": pw.findtext("HOMERACK", "") if pw is not None else "",
    "tree": node_to_dict(pw.find("NODE")) if pw is not None and pw.find("NODE") is not None else None,
}

# Other top-level sections (names only) for reference
top = [c.tag for c in root]

# logical workspace / cluster info
lw = root.find("LOGICALWORKSPACE")
logical = None
if lw is not None:
    logical = ET.tostring(lw, encoding="unicode")
    logical = re.sub(r"(<IMAGE_CONTENT>)[^<]{40}[^<]*", r"\1...base64...", logical)[:6000]

result = {
    "source": src,
    "pt_version": root.findtext("VERSION", ""),
    "top_level_sections": top,
    "device_count": len(devices),
    "link_count": len(links),
    "devices": devices,
    "links": links,
    "physical_workspace": phys,
    "logical_workspace_excerpt": logical,
}
with open(out, "w") as f:
    json.dump(result, f, indent=1)
print("devices", len(devices), "links", len(links))
print("top-level:", top)
