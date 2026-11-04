# DC2 VM and PRTG remote probe on DC2 (MG side) - 2026-11-04

Values: DC2 172.16.0.2/24, gateway 172.16.0.1 (router SB-MG Gi0/1), DNS 192.168.0.2 (DC1), PRTG core on
SB-FS2 192.168.0.3, SNMP community ciscolab. Your PC's lab lead is in MG-S1 Fa0/1.

## 1. VM network

1. VM > Settings > Network Adapter > **Bridged**, *Connect at power on* ticked. (Remove the floppy and
   disconnect the CD if this is the old DC2.Eric.Roly VM.)
2. Edit > Virtual Network Editor > Change Settings > VMnet0 > Bridged to: your lab NIC by name. If that
   dialog is refused, unplug the TAFE lead so the lab NIC is the only connected one.
3. Power on, log in.

## 2. Inside DC2

1. Server Manager > Local Server > computer name > Change > `DC2` > restart.
2. Ethernet0 > Properties > IPv4: `172.16.0.2` / `255.255.255.0` / gateway `172.16.0.1` / preferred DNS
   `192.168.0.2` / alternate blank.
3. Time zone Brisbane. Local Server > IE Enhanced Security Configuration > Off (so the PRTG web page and
   download work in IE).
4. PowerShell (Admin):
   ```
   Enable-NetFirewallRule -DisplayName "File and Printer Sharing (Echo Request - ICMPv4-In)"
   New-NetFirewallRule -DisplayName "PRTG Syslog 514" -Protocol UDP -LocalPort 514 -Direction Inbound -Action Allow
   New-NetFirewallRule -DisplayName "PRTG SNMP Trap 162" -Protocol UDP -LocalPort 162 -Direction Inbound -Action Allow
   ping 172.16.0.1
   ping 192.168.0.1
   ping 192.168.0.3
   Test-NetConnection 192.168.0.3 -Port 23560
   ```
   All three pings reply and the last line says `TcpTestSucceeded : True` = ready for the probe. (If only
   the last fails: PRTG on SB-FS2 is not running yet, or its firewall blocks 23560.)
5. Domain join and promotion (Lab 8 part) when DC1 is up: `nslookup dc1.<domain>` must answer 192.168.0.2
   first; then join, then Promote > Add a domain controller to an existing domain. Not needed for the probe.

## 3. On the PRTG core (classmate, SB-FS2, 192.168.0.3), two minutes

1. Browser > `http://192.168.0.3` > log in (default prtgadmin / prtgadmin unless changed).
2. Setup > System Administration > **Core & Probes**: Probe Connection IPs = *All IPs available*; **Access
   Key**: note it (create one if empty); Allow IPs = `any` (or `172.16.0.2`). Save; let the core service restart.
3. Setup > **Downloads** (Downloads/Add-Ons) > **Remote Probe Installer** > Download. The file is
   `PRTG_Remote_Probe_Installer.exe` and carries the core address and access key.

## 4. Install the probe on DC2

1. On DC2 open `http://192.168.0.3` in the browser, log in, Setup > Downloads > Remote Probe Installer >
   Download (or copy the .exe over by USB).
2. Run it as Administrator > accept > Core Server: `192.168.0.3`, Probe Access Key: as noted (prefilled if
   downloaded from the core), Probe Name: `MG-Remote-Probe` > Install > Finish. The PRTG Probe service starts.
3. Back on the core web UI: a notification *New probe "MG-Remote-Probe" wants to connect* > **Approve**
   (also under Setup > Probe Approval if the pop-up is missed). The probe appears in Devices with its
   "Probe Device". Screenshot it (Lab 9.3 evidence).

## 5. Sensors on the remote probe (Lab 9.4)

1. Devices > right-click **MG-Remote-Probe** > Add Device > Name `SB-MG router (MG side)`, IPv4 `172.16.0.1`
   > Credentials for SNMP Devices: version **v2c**, community `ciscolab` > OK.
2. On that device: Add Sensor > **Ping** > OK. Add Sensor > **SNMP Traffic** > tick the interfaces
   (Gi0/0, Gi0/1) > OK. ("SNMP Traffic" is PRTG's bandwidth sensor.)
3. Add Device `MG-S1`, IPv4 `172.16.0.254`, same credentials > Ping + SNMP Traffic (Vlan1 and the
   FastEthernet ports you use).
4. On the **Probe Device** of MG-Remote-Probe: Add Sensor > **Syslog Receiver** (port 514) > OK; optionally
   **SNMP Trap Receiver** (162).
5. Make a syslog message: console into MG-S1, `configure terminal`, `end` -> `%SYS-5-CONFIG_I` arrives in
   the Syslog Receiver sensor within a minute. Screenshot the device tree with green sensors and the
   syslog sensor's messages (Lab 9.4 evidence).

Your classmate does the mirror on the local probe: devices SB-MG (192.168.0.1) and SB-S1 (192.168.0.254),
Ping + SNMP Traffic, plus a Syslog Receiver on the local Probe Device.
