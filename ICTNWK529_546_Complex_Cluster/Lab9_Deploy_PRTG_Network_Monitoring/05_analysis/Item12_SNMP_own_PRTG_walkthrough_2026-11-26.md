# Item 12: SNMP (Lab 9), screenshot required, from your own PRTG (2026-11-26)

Evidence list row: `12 | SNMP (Lab 9) | Yes | Your own PRTG - create this`.
The Lab 9 core on SB-FS2 was the classmate's install, so this item needs a PRTG that you installed yourself,
polling a device over SNMP, with the sensors live (green, with values). Two ways to get it. Use A if you can
get back on the rack; B works on your own PC with nothing else.

Values used below are the Lab 9 ones: community `ciscolab`, SNMP v2c, PRTG login `prtgadmin`.

## Route A: at the rack (best match to Lab 9)

1. Your PC on the MG side: lead in MG-S1 Fa0/1. Windows VM (DC2 is fine, or any Windows Server/10/11 VM)
   on Bridged, IP `172.16.0.2/24`, gateway `172.16.0.1`.
2. Paste the MG router and MG-S1 blocks from
   `../02_student_work/network/Lab9_PRTG_one_router_configs_2026-11-04.txt` (or the three-router file). The
   lines that matter for this item:
   ```
   ip access-list standard SNMP_ACL
    permit host 172.16.0.2
    exit
   snmp-server community ciscolab RO SNMP_ACL
   snmp-server location MG
   snmp-server contact Student
   snmp-server host 172.16.0.2 version 2c ciscolab
   snmp-server enable traps
   ```
   Check on the device: `show snmp community` and `show snmp host` (screenshot these too, they back up the PRTG shot).
3. Install PRTG on the VM as a full core (not a remote probe): see "Install PRTG" below.
4. Devices > Local Probe > Add Device: Name `MG router`, IPv4 `172.16.0.1`, Credentials for SNMP Devices:
   untick *Inherit*, SNMP **v2c**, community `ciscolab` > OK. Repeat for `MG-S1` / `172.16.0.254`.
5. On each device: Add Sensor > **Ping**; Add Sensor > **SNMP Traffic** (tick Gi0/0, Gi0/1 on the router;
   Vlan1 and the uplink on the switch); Add Sensor > **SNMP System Uptime**.
6. Wait 2 to 3 minutes for values, then take the shots (list at the end).

## Route B: your own PC only (no rack)

PRTG polls the Windows SNMP agent on the same machine. It is real SNMP v2c with the same community, so the
screenshots are genuine; just label it as polling the server's own SNMP agent, not a Cisco device.

1. Windows VM (Server 2016/2019/2022 or Windows 10/11), 4 GB RAM, 2 vCPU, NAT network is fine (it needs the
   internet only to download PRTG).
2. Install the Windows SNMP agent, PowerShell (Admin):
   ```
   # Windows Server:
   Install-WindowsFeature SNMP-Service -IncludeManagementTools
   # Windows 10/11 instead:
   # Add-WindowsCapability -Online -Name "SNMP.Client~~~~0.0.1.0"

   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities" -Name "ciscolab" -Value 4 -PropertyType DWord -Force
   Restart-Service SNMP
   Get-Service SNMP
   ```
   Value 4 = READ ONLY. The agent accepts only `localhost` by default (PermittedManagers), which is what we want.
   GUI check: `services.msc` > SNMP Service > Properties > **Security** tab shows `ciscolab  READ ONLY` and
   *Accept SNMP packets from these hosts: localhost* (screenshot this: it is the "agent" half of the evidence).
3. Install PRTG: see below.
4. Devices > Local Probe > Add Device: Name `SNMP agent (this server)`, IPv4 `127.0.0.1`, SNMP **v2c**,
   community `ciscolab` > OK.
5. Add Sensor on it: **SNMP System Uptime**, **SNMP Traffic** (pick the Ethernet adapter), **SNMP CPU Load**,
   **SNMP Memory**. Add a **Ping** sensor too.
6. Wait 2 to 3 minutes for values, then take the shots.

## Install PRTG (both routes)

1. Download from paessler.com (PRTG Network Monitor, free trial). Trial = unlimited sensors for 30 days,
   then it falls back to the free edition (100 sensors), which is plenty here. The download asks for an email
   and shows a licence key; keep both.
2. Run the installer as Administrator > language > accept > email for alerts > licence key > Install.
3. When it finishes it opens `http://localhost` (or `http://<VM IP>`). Log in `prtgadmin` / `prtgadmin`,
   change the password when asked. Skip the Smart Setup guide / auto-discovery so the tree shows only your devices.
4. If Windows' own **SNMP Trap** service is running, stop and disable it (`services.msc`): PRTG needs UDP 162
   for its trap receiver. Only matters if you add an SNMP Trap Receiver sensor.

## Shots for item 12

1. **Device tree**: Devices view expanded to your device(s) under Local Probe, every sensor green with a
   value (SNMP Traffic in kbit/s, Uptime in days/hours). This is the main screenshot.
2. **SNMP credentials**: the device's Settings tab, scrolled to *Credentials for SNMP Devices* showing v2c
   and the community. Crop or blur the community if the template says so.
3. **One SNMP sensor's Overview**: click the SNMP Traffic sensor; the page with the gauge and the 2-day /
   live graph.
4. **Agent side**: Route A `show snmp community` + `show snmp host` on the router/switch; Route B the SNMP
   Service Security tab.

Make sure the PRTG banner/URL bar or the Windows taskbar shows the date or your VM name in at least one shot,
so it is clearly your own install. Save the files into `../02_student_work/screenshots/` as
`Item12_SNMP_1_tree.png` ... `Item12_SNMP_4_agent.png`.

## If a sensor stays grey or red

| Symptom | Fix |
|---|---|
| SNMP sensor "No response (SNMP error # -2003)" | Community typo, wrong SNMP version (must be v2c), or the device ACL does not permit the PRTG IP (Route A) / PermittedManagers not localhost (Route B). |
| Ping green, SNMP red (Route A) | `show snmp community` on the device; `show access-lists SNMP_ACL` should show matches climbing. |
| Add Sensor list shows no interfaces for SNMP Traffic | Credentials not saved on the device: re-open Settings, untick Inherit, retype. Then *Recheck now*. |
| Route B: SNMP Service missing after install | Reboot once; on Windows 10/11 confirm `Get-WindowsCapability -Online -Name SNMP*` says Installed. |
