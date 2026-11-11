#!/bin/bash
# Lab 10 reference run. Security Onion itself needs a full VM and cannot run in this test container, so this
# runs Suricata (the IDS engine inside Security Onion) on its own against real captured traffic.
# The traffic is the same test Security Onion documents (a web page that returns "uid=0(root) ..."), served
# from a local web server because the container has no direct internet route for the monitor capture.
# The rule is the standard GPL rule sid 2100498 that the Security Onion test triggers.
# Usage: ids_reference_capture.sh <outdir>
set -euo pipefail
OUT="${1:?outdir}"; W=/tmp/idsref; mkdir -p "$W/www/uid" "$W/logs"
PS='root@vm:~# '
echo 'uid=0(root) gid=0(root) groups=0(root)' > "$W/www/uid/index.html"
cat > "$W/local.rules" <<'RULE'
alert ip any any -> any any (msg:"GPL ATTACK_RESPONSE id check returned root"; content:"uid=0|28|root|29|"; classtype:bad-unknown; sid:2100498; rev:7;)
RULE
(cd "$W/www" && exec python3 -m http.server 8080 --bind 192.0.2.2 >/dev/null 2>&1) & WEB=$!
tcpdump -i lo -U -w "$W/test.pcap" 'tcp port 8080' >/dev/null 2>&1 & CAP=$!
sleep 2
{
  echo "${PS}curl http://192.0.2.2:8080/uid/index.html"
  curl -s --noproxy '*' http://192.0.2.2:8080/uid/index.html
} > "$OUT/lab10_01_test_traffic.txt"
sleep 1; kill $CAP $WEB 2>/dev/null || true; wait 2>/dev/null || true
: > "$W/logs/fast.log"; rm -f "$W/logs/eve.json"
{
  echo "${PS}suricata -V"; suricata -V
  echo "${PS}cat local.rules"; cat "$W/local.rules"
  echo "${PS}suricata -r test.pcap -S local.rules -k none -l logs/ | tail -2"
  (cd "$W" && suricata -r test.pcap -S local.rules -k none -l logs/ 2>&1 | tail -2)
  echo "${PS}cat logs/fast.log"; cat "$W/logs/fast.log"
} > "$OUT/lab10_02_suricata_alert.txt"
{
  echo "${PS}jq 'select(.event_type==\"alert\") | {timestamp, src_ip, src_port, dest_ip, dest_port, proto, alert: {signature_id: .alert.signature_id, signature: .alert.signature, category: .alert.category, severity: .alert.severity}}' logs/eve.json"
  jq 'select(.event_type=="alert") | {timestamp, src_ip, src_port, dest_ip, dest_port, proto, alert: {signature_id: .alert.signature_id, signature: .alert.signature, category: .alert.category, severity: .alert.severity}}' "$W/logs/eve.json"
} > "$OUT/lab10_03_alert_detail_eve_json.txt"
